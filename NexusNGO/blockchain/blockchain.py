import os  
from dotenv import load_dotenv  
from web3 import Web3, exceptions
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()


# Function to fetch transactions for an address in the past 5 minutes and save them to a CSV
def get_transactions_last_3_minutes(PUBLIC_KEY):
    infura_url = f'https://sepolia.infura.io/v3/{os.getenv("INFURA_API_KEY")}'
    web3 = Web3(Web3.HTTPProvider(infura_url))
    
    # Check if connected
    if not web3.is_connected():
        raise ConnectionError('Failed to connect to Infura.')
    else:
        print('Connected to Infura!')

    # Convert public key to checksum address
    address = web3.to_checksum_address(PUBLIC_KEY)
    latest_block = web3.eth.get_block('latest').number
    current_time = datetime.utcnow()
    
    transactions = []
    block_num = latest_block

    # Define a time limit (5 minutes ago)
    time_limit = current_time - timedelta(minutes=3)

    while True:
        try:
            block = web3.eth.get_block(block_num, full_transactions=True)
            block_timestamp = datetime.utcfromtimestamp(block.timestamp)

            # Stop if the block is older than 5 minutes
            if block_timestamp < time_limit:
                break

            for tx in block.transactions:
                # Check if the address is either the sender (from) or receiver (to)
                if tx['from'] == address or tx['to'] == address:
                    tx_data = {
                        'blockNumber': tx.blockNumber,
                        'from': tx['from'],
                        'to': tx['to'],
                        'value': web3.from_wei(tx['value'], 'ether'),
                        'hash': tx['hash'].hex(),
                        'gas': tx['gas'],
                        'gasPrice': web3.from_wei(tx['gasPrice'], 'gwei'),
                        'input': tx['input'].hex(),
                        'timestamp': block_timestamp
                    }
                    transactions.append(tx_data)

            block_num -= 1  # Move to the previous block

        except exceptions.BlockNotFound:
            print(f'Block {block_num} not found.')
            break

    # Save transactions to CSV if any are found
    if transactions:
        df = pd.DataFrame(transactions)
        if os.path.exists("transactions.csv"):
            df_existing = pd.read_csv("transactions.csv")
            df = pd.concat([df_existing, df], ignore_index=True)
            df.drop_duplicates(subset=['hash'], inplace=True)
        df.to_csv('transactions.csv', index=False)
        print(f"Saved {len(transactions)} transactions to 'transactions.csv'.")
    else:
        print("No transactions found in the past 5 minutes.")


