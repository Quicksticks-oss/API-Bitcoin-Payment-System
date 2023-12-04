import configparser
from bitcoinrpc.authproxy import AuthServiceProxy
from flask import Flask, request
import datetime
import uuid

app = Flask(__name__)

# Function to read configurations from the config file
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    rpc_user = config.get('RPC', 'rpc_user')
    rpc_password = config.get('RPC', 'rpc_password')
    rpc_port = config.getint('RPC', 'rpc_port')
    num_addresses = config.getint('RPC', 'num_addresses')

    port = config.getint('App', 'port')

    return rpc_user, rpc_password, rpc_port, num_addresses, port

def generate_receiving_address(rpc_user, rpc_password, rpc_port, transaction_amount=0.001):
    rpc_connection = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@localhost:{rpc_port}')
    address = rpc_connection.getnewaddress()
    label = generate_label_id(transaction_amount)
    rpc_connection.setlabel(address, label)
    addresses = (address, label)
    return addresses

def generate_label_id(transaction_amount):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y_%m_%d_%H_%M_%S")
    random_uuid = str(uuid.uuid4())
    formatted_amount = "{:.2f}".format(transaction_amount)
    label_id = f"{formatted_datetime}__{formatted_amount}__{random_uuid}"
    return label_id

@app.route('/')
def index():
    return 'API server for accepting Bitcoin payments using Bitcoin Core.\n /api for more detail.'

@app.route('/api')
def api():
    routes = '''/api/new_payment/<amount>
/api/check_payment'''
    return routes

@app.route('/api/new_payment', methods=['POST'])
def new_payment():
    # Extract amount from the POST request
    amount = request.json.get('amount')

    # Validate that amount is present in the request
    if amount is None:
        return {'error': 'Amount is required in the request'}, 400

    # Assuming generate_receiving_address is a function that generates an address
    receiving_address = generate_receiving_address(rpc_user, rpc_password, rpc_port, amount)
    return {'address': receiving_address}

@app.route('/api/check_payment', methods=['POST'])
def check_payment():
    address = request.json.get('address')
    rpc_connection = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@localhost:{rpc_port}')
        # List transactions for the given address
    transactions = rpc_connection.listtransactions("*", 1000, 0, True)
        
    # Filter transactions related to the specified address
    address_transactions = [tx for tx in transactions if address in tx.get("address", "")]
        
    for transaction in address_transactions:
        if transaction['category'] == 'receive':
            return {'status': True, 'transaction': transaction} #print(f"Received payment on Address: {address}, Label: {label}, Transaction ID: {transaction['txid']}, Amount: {transaction['amount']} BTC")
    return {'status': False, 'transaction': None}

if __name__ == "__main__":
    # Load configurations from the config file
    rpc_user, rpc_password, rpc_port, num_addresses, port = load_config()

    # Use the configurations in your application
    app.run(port=port)
