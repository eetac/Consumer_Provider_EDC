import json
import requests
import time

PROVIDER_URL = "http://localhost:19193/management"
CONSUMER_URL = "http://localhost:29193/management"

def register_asset(file_path):
    url = f"{PROVIDER_URL}/v3/assets"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers)
            
            response.raise_for_status()
            
            print("=" * 50)
            print(f"Respuesta del servidor register asset: {response.json()}")
            print("=" * 50)
            return response.json()
    except FileNotFoundError:
        print("=" * 50)
        print(f"Error register asset: Archivo no encontrado en la ruta: {file_path}")
        print("=" * 50)
        return None
    except json.JSONDecodeError:
        print("=" * 50)
        print(f"Error register asset: El archivo {file_path} no contiene JSON válido.")
        print("=" * 50)
        return None
    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error en la solicitud HTTP register asset: {e}")
        print("=" * 50)
        return None

# Función para crear una política en el proveedor
def create_policy(file_path):
    url = f"{PROVIDER_URL}/v3/policydefinitions"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers)
            
            response.raise_for_status()
            
            print("=" * 50)
            print(f"Respuesta del servidor create_policy: {response.json()}")
            print("=" * 50)
            return response.json()
    except FileNotFoundError:
        print("=" * 50)
        print(f"Error create_policy: Archivo no encontrado en la ruta: {file_path}")
        print("=" * 50)
        return None
    except json.JSONDecodeError:
        print("=" * 50)
        print(f"Error create_policy: El archivo {file_path} no contiene JSON válido.")
        print("=" * 50)
        return None
    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error en la solicitud HTTP create_policy: {e}")
        print("=" * 50)
        return None

# Función para crear un contrato en el proveedor
def create_contract(file_path):
    url = f"{PROVIDER_URL}/v3/contractdefinitions"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers)
            
            response.raise_for_status()
            
            print("=" * 50)
            print(f"Respuesta del servidor create_contract: {response.json()}")
            print("=" * 50)
            return response.json()
    except FileNotFoundError:
        print("=" * 50)
        print(f"Error create_contract: Archivo no encontrado en la ruta: {file_path}")
        print("=" * 50)
        return None
    except json.JSONDecodeError:
        print("=" * 50)
        print(f"Error create_contract: El archivo {file_path} no contiene JSON válido.")
        print("=" * 50)
        return None
    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error en la solicitud HTTP create_contract: {e}")
        print("=" * 50)
        return None

# Función para buscar el catálogo del proveedor desde el consumidor
def fetch_catalog(file_path):
    url = f"{CONSUMER_URL}/v3/catalog/request"
    try:
        # Leer el archivo JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers)
            
            response.raise_for_status()
            
            print("=" * 50)
            print(f"Respuesta del servidor fetch_catalog: {response.json()}")
            print("=" * 50)
            return response.json()
    except FileNotFoundError:
        print("=" * 50)
        print(f"Error fetch_catalog: Archivo no encontrado en la ruta: {file_path}")
        print("=" * 50)
        return None
    except json.JSONDecodeError:
        print("=" * 50)
        print(f"Error fetch_catalog: El archivo {file_path} no contiene JSON válido.")
        print("=" * 50)
        return None
    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error en la solicitud HTTP fetch_catalog: {e}")
        print("=" * 50)
        return None

""" The consumer now needs to initiate a contract negotiation sequence with the provider. That sequence looks as follows:

Consumer sends a contract offer to the provider (currently, this has to be equal to the provider's offer!)
Provider validates the received offer against its own offer
Provider either sends an agreement or a rejection, depending on the validation result
In case of successful validation, provider and consumer store the received agreement for later reference """

# Función para reemplazar {{contract-offer-id}} en negotiate-contract-toedit.json
def update_negotiate_contract(catalog_response, template_path, output_path):
    try:
        # Extraer el valor de dcat:dataset.odrl:hasPolicy.@id
        contract_offer_id = catalog_response.get("dcat:dataset", {}).get("odrl:hasPolicy", {}).get("@id")
        if not contract_offer_id:
            print("=" * 50)
            print("No se encontró 'contract-offer-id' en la respuesta del catálogo.")
            print("=" * 50)
            return False
        
        # Leer el archivo negotiate-contract.json
        with open(template_path, 'r', encoding='utf-8') as template_file:
            negotiate_contract = json.load(template_file)
        
        # Reemplazar {{contract-offer-id}} con el valor extraído
        negotiate_contract = json.loads(json.dumps(negotiate_contract).replace("{{contract-offer-id}}", contract_offer_id))
        
        # Guardar el archivo actualizado en output_path
        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(negotiate_contract, output_file, indent=4)
        
        print("=" * 50)
        print(f"Archivo negotiate-contract.json actualizado correctamente en: {output_path}")
        print("=" * 50)
        return True
    except FileNotFoundError:
        print("=" * 50)
        print(f"Error: No se encontró el archivo en la ruta: {template_path}")
        print("=" * 50)
        return False
    except json.JSONDecodeError:
        print("=" * 50)
        print(f"Error: El archivo {template_path} no contiene JSON válido.")
        print("=" * 50)
        return False
    except Exception as e:
        print("=" * 50)
        print(f"Error inesperado: {e}")
        print("=" * 50)
        return False

# Función para iniciar la negociación del contrato en el consumidor
def initiate_negotiation(file_path):
    url = f"{CONSUMER_URL}/v3/contractnegotiations"
    try:
        # Leer el archivo JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers)
            
            response.raise_for_status()
            
            print("=" * 50)
            print(f"Respuesta del servidor initiate_negotiation: {response.json()}")
            print("=" * 50)
            return response.json()
    except FileNotFoundError:
        print("=" * 50)
        print(f"Error initiate_negotiation: Archivo no encontrado en la ruta: {file_path}")
        print("=" * 50)
        return None
    except json.JSONDecodeError:
        print("=" * 50)
        print(f"Error initiate_negotiation: El archivo {file_path} no contiene JSON válido.")
        print("=" * 50)
        return None
    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error en la solicitud HTTP initiate_negotiation: {e}")
        print("=" * 50)
        return None

# Getting the contract agreement id
def get_contract_agreement_id(initiate_response, interval=5, timeout=60):
    try:
        # Extraer el ID de la negociación desde la respuesta de initiate_negotiation
        negotiation_id = initiate_response.get("@id")
        
        if not negotiation_id:
            print("=" * 50)
            print("Error: No se encontró '@id' en la respuesta de initiate_negotiation.")
            print("=" * 50)
            return None
        
        # Construir la URL
        url = f"{CONSUMER_URL}/v3/contractnegotiations/{negotiation_id}"
        headers = {'Content-Type': 'application/json'}
        
        start_time = time.time()
        while True:
            # Realizar la solicitud GET al endpoint
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Obtener el estado actual
            status = response.json()
            current_state = status.get("state")
            print("=" * 50)
            print(f"Estado actual de la negociación: {current_state}")
            print("=" * 50)
            
            # Verificar si el estado es FINALIZED o DECLINED
            if current_state == "FINALIZED":
                print("=" * 50)
                print(f"La negociación ha finalizado exitosamente: {status.get("contractAgreementId")}")
                print("=" * 50)
                return status.get("contractAgreementId")
            elif current_state == "DECLINED":
                print("=" * 50)
                print("La negociación fue rechazada.")
                print("=" * 50)
                return None
            
            # Verificar si se alcanzó el tiempo de espera
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print("=" * 50)
                print("Tiempo de espera agotado. La negociación no finalizó dentro del tiempo esperado.")
                print("=" * 50)
                return None
            
            # Esperar antes del próximo intento
            time.sleep(interval)
    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error al obtener el estado de la negociación: {e}")
        print("=" * 50)
        return None

####### Empezamos el "Consumer Pull" ######

# Función para reemplazar {{contract-agreement-id}} en start-transfer-toedit.json
def update_start_transfer(agreement_id, template_path, output_path):
    try:
        if not agreement_id:
            print("=" * 50)
            print("No se encontró 'agreement_id'.")
            print("=" * 50)
            return False
        
        # Leer el archivo start-transfer-toedit.json
        with open(template_path, 'r', encoding='utf-8') as template_file:
            start_transfer = json.load(template_file)
        
        # Reemplazar {{contract-agreement-id}} con el valor extraído
        start_transfer = json.loads(json.dumps(start_transfer).replace("{{contract-agreement-id}}", agreement_id))
        
        # Guardar el archivo actualizado en output_path
        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(start_transfer, output_file, indent=4)
        
        print("=" * 50)
        print(f"Archivo start-transfer.json actualizado correctamente en: {output_path}")
        print("=" * 50)
        return True
    except FileNotFoundError:
        print("=" * 50)
        print(f"Error: No se encontró el archivo en la ruta: {template_path}")
        print("=" * 50)
        return False
    except json.JSONDecodeError:
        print("=" * 50)
        print(f"Error: El archivo {template_path} no contiene JSON válido.")
        print("=" * 50)
        return False
    except Exception as e:
        print("=" * 50)
        print(f"Error inesperado: {e}")
        print("=" * 50)
        return False

# Función para iniciar la transferencia
def start_transfer(file_path):
    url = f"{CONSUMER_URL}/v3/transferprocesses"
    try:
        # Leer el archivo JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers)
            
            response.raise_for_status()
            
            print("=" * 50)
            """We will get a UUID in the response. 
            This time, this is the ID of the TransferProcess 
            ( process id) created on the consumer side, 
            because like the contract negotiation, the data transfer 
            is handled in a state machine and performed asynchronously."""
            print(f"Respuesta del servidor start_transfer: {response.json()}") 
            print("=" * 50)
            return response.json()
    except FileNotFoundError:
        print("=" * 50)
        print(f"Error start_transfer: Archivo no encontrado en la ruta: {file_path}") 
        print("=" * 50)
        return None
    except json.JSONDecodeError:
        print("=" * 50)
        print(f"Error start_transfer: El archivo {file_path} no contiene JSON válido.")
        print("=" * 50)
        return None
    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error en la solicitud HTTP start_transfer: {e}")
        print("=" * 50)
        return None

# Función saber el estado de la transferencia
def check_transfer_status(started_transfer, interval=5, timeout=60):
    try:
        # Extraer el ID de la transferencia desde la respuesta de start_transfer
        transfer_id = started_transfer.get("@id")
        
        if not transfer_id:
            print("=" * 50)
            print("Error: No se encontró '@id' en la respuesta de start_transfer.")
            print("=" * 50)
            return None
        
        # Construir la URL
        url = f"{CONSUMER_URL}/v3/transferprocesses/{transfer_id}"
        headers = {'Content-Type': 'application/json'}
        
        start_time = time.time()
        while True:
            # Realizar la solicitud GET al endpoint
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Obtener el estado actual
            status = response.json()
            current_state = status.get("state")
            print("=" * 50)
            print(f"Estado actual de la transferencia: {current_state}")
            print("=" * 50)
            
            # Verificar si el estado es FINALIZED o DECLINED
            if current_state == "STARTED":
                print("=" * 50)
                print(f"La transferencia se ha iniciado exitosamente: {status}")
                print("=" * 50)
                return current_state
            elif current_state == 'DEPROVISIONED':
                print("=" * 50)
                print(f"La transferencia no se ha iniciado: {current_state}.")
                print("=" * 50)
                return None
            
            # Verificar si se alcanzó el tiempo de espera
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print("=" * 50)
                print("Tiempo de espera agotado. La transferencia no finalizó dentro del tiempo esperado.")
                print("=" * 50)
                return None
            
            # Esperar antes del próximo intento
            time.sleep(interval)
    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error al obtener el estado de la transferencia: {e}")
        print("=" * 50)
        return None

# Función para comprobar la data
def check_data(started_transfer):
    try:
        # Extraer el ID de la transferencia desde la respuesta de start_transfer
        transfer_id = started_transfer.get("@id")
        
        if not transfer_id:
            print("=" * 50)
            print("Error: No se encontró '@id' en la respuesta de start_transfer.")
            print("=" * 50)
            return None

        # Construir la URL
        url = f"{CONSUMER_URL}/v3/edrs/{transfer_id}/dataaddress"
        headers = {'Content-Type': 'application/json'}
        
        # Realizar la solicitud GET al endpoint
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("=" * 50)
        print(f"Respuesta del check_data: {response.json()}")
        print("=" * 50)
        return response.json()

    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error en la solicitud HTTP check_data: {e}")
        print("=" * 50)
        return None

# Función para leer la data
def read_data(obtained_data, output_file="data_output.json"):
    try:
        # Extraer el ID de la transferencia desde la respuesta de start_transfer
        endpoint = obtained_data.get("endpoint")
        token = obtained_data.get("authorization")
        
        if not endpoint:
            print("=" * 50)
            print("Error: No se encontró 'endpoint' en la respuesta de check_data.")
            print("=" * 50)
            return None

        if not token:
            print("=" * 50)
            print("Error: No se encontró 'authorization' en la respuesta de check_data.")
            print("=" * 50)
            return None

        headers = {
            'Authorization': f'{token}'
        }
        
        # Realizar la solicitud GET al endpoint
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()

        # Guardar la respuesta en un archivo JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)

        print("=" * 50)
        print(f"Los datos se han guardado en '{output_file}'.")
        print("=" * 50)

    except requests.exceptions.RequestException as e:
        print("=" * 50)
        print(f"Error en la solicitud HTTP read_data: {e}")
        print("=" * 50)
        return None

# Ejemplo de uso
if __name__ == "__main__":
    # Registrar un asset en el proveedor
    asset = register_asset('create-asset.json')

    # Crear una política asociada al asset
    policy = create_policy('create-policy.json')

    # Crear un contrato que use la política
    contract = create_contract('create-contract-definition.json')

    # Buscar catàlogo
    catalog = fetch_catalog('fetch-catalog.json')

    update_negotiate_contract(catalog, 'negotiate-contract-toedit.json', 'negotiate-contract.json')

    negotiation = initiate_negotiation('negotiate-contract.json')

    agreement_id = get_contract_agreement_id(negotiation)

    # Solo continuar si la negociación fue exitosa
    if agreement_id:

        update_start_transfer(agreement_id, 'start-transfer-toedit.json', 'start-transfer.json')

        started_transfer = start_transfer('start-transfer.json')

        status = check_transfer_status(started_transfer)

        if status == 'STARTED':

            data_obtained = check_data(started_transfer)

            read_data(data_obtained)

        else:
            print("=" * 50)
            print("No se pudo obtener un started_transfer. La transferencia no puede continuar.")
            print("=" * 50)


    else:
        print("=" * 50)
        print("No se pudo obtener un contractAgreementId. La transferencia no puede continuar.")
        print("=" * 50)