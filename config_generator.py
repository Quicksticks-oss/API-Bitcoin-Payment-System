import configparser

def generate_config():
    config = configparser.ConfigParser()

    # RPC Configuration
    config['RPC'] = {
        'rpc_user': input('Enter RPC user: '),
        'rpc_password': input('Enter RPC password: '),
        'rpc_port': input('Enter RPC port (default: 8332): ') or '8332',
        'num_addresses': input('Enter the number of addresses: ')
    }

    # App Configuration
    config['App'] = {
        'port': input('Enter App port (default: 8976): ') or '8976'
    }

    # Write the configuration to a file
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

if __name__ == "__main__":
    generate_config()
