import json
import requests

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
            
            print(f"Respuesta del servidor register asset: {response.json()}")
            return response.json()
    except FileNotFoundError:
        print(f"Error register asset: Archivo no encontrado en la ruta: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error register asset: El archivo {file_path} no contiene JSON válido.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP register asset: {e}")
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
            
            print(f"Respuesta del servidor create_policy: {response.json()}")
            return response.json()
    except FileNotFoundError:
        print(f"Error create_policy: Archivo no encontrado en la ruta: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error create_policy: El archivo {file_path} no contiene JSON válido.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP create_policy: {e}")
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
            
            print(f"Respuesta del servidor create_contract: {response.json()}")
            return response.json()
    except FileNotFoundError:
        print(f"Error create_contract: Archivo no encontrado en la ruta: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error create_contract: El archivo {file_path} no contiene JSON válido.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP create_contract: {e}")
        return None

# Función para buscar el catàleg del proveïdor des del consumidor
def fetch_catalog(file_path):
    url = f"{CONSUMER_URL}/v3/catalog/request"
    try:
        # Leer el archivo JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers)
            
            response.raise_for_status()
            
            print(f"Respuesta del servidor fetch_catalog: {response.json()}")
            return response.json()
    except FileNotFoundError:
        print(f"Error fetch_catalog: Archivo no encontrado en la ruta: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error fetch_catalog: El archivo {file_path} no contiene JSON válido.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP fetch_catalog: {e}")
        return None

# Función para iniciar la negociación del contrato en el consumidor
def initiate_negotiation(connector_id, connector_address, offer):
    url = f"{CONSUMER_URL}/v1/contractnegotiation"
    payload = {
        "connectorId": connector_id,
        "connectorAddress": connector_address,
        "protocol": "ids-multipart",
        "offer": offer,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    print(f"Negociación iniciada: {response.json()}")
    return response.json()

# Función para monitorear el estado de una negociación
def get_negotiation_status(negotiation_id):
    url = f"{CONSUMER_URL}/v1/contractnegotiation/{negotiation_id}"
    response = requests.get(url)
    response.raise_for_status()
    print(f"Estado de la negociación: {response.json()}")
    return response.json()

# Función para iniciar la transferencia de datos
def initiate_transfer(connector_id, connector_address, asset_id, data_destination):
    url = f"{CONSUMER_URL}/v1/transferprocess"
    payload = {
        "connectorId": connector_id,
        "connectorAddress": connector_address,
        "protocol": "ids-multipart",
        "assetId": asset_id,
        "dataDestination": data_destination,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    print(f"Transferencia iniciada: {response.json()}")
    return response.json()

# Función para monitorear el estado de una transferencia
def get_transfer_status(transfer_id):
    url = f"{CONSUMER_URL}/v1/transferprocess/{transfer_id}"
    response = requests.get(url)
    response.raise_for_status()
    print(f"Estado de la transferencia: {response.json()}")
    return response.json()

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

    # Iniciar negociación del contrato
    """ negotiation = initiate_negotiation(
        connector_id="provider-connector",
        connector_address="https://provider-edc.example.com",
        offer={
            "offerId": "contract-001",
            "assetId": "asset-001",
            "policy": policy["policy"]
        }
    ) """

    # Obtener el estado de la negociación
    """ negotiation_status = get_negotiation_status(negotiation["id"]) """

    # Iniciar transferencia de datos tras una negociación exitosa
    """ if negotiation_status["state"] == "CONFIRMED":
        transfer = initiate_transfer(
            connector_id="provider-connector",
            connector_address="https://provider-edc.example.com",
            asset_id="asset-001",
            data_destination={"type": "HttpProxy", "properties": {"baseUrl": "https://consumer-data.example.com"}}
        )
        transfer_status = get_transfer_status(transfer["id"]) """