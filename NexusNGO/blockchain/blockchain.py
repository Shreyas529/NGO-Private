import os  
from dotenv import load_dotenv  
from web3 import Web3, exceptions
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

import asyncio




def get_transactions_last_3_minutes(public_keys):
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    infura_url = f'https://sepolia.infura.io/v3/{os.getenv("INFURA_API_KEY")}'
    web3 = Web3(Web3.HTTPProvider(infura_url))

    # Check if connected
    if not web3.is_connected():
        return None

    latest_block = web3.eth.get_block('latest').number
    current_time = datetime.utcnow()

    all_transactions = []
    block_num = latest_block    

    # Define a time limit (3 minutes ago)
    time_limit = current_time - timedelta(minutes=3)

    # Loop over each public key
    for PUBLIC_KEY in public_keys:
        print(PUBLIC_KEY)
        address = web3.to_checksum_address(PUBLIC_KEY)
        transactions = []
        block_num = latest_block 

        while True:
            try:
                block = web3.eth.get_block(block_num, full_transactions=True)
                block_timestamp = datetime.utcfromtimestamp(block.timestamp)

                # Stop if the block is older than 3 minutes
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
                break

        # Append transactions of this public key to the main list
        if transactions:
            all_transactions.extend(transactions)

    # Save transactions to CSV if any are found
    if all_transactions:
        print("Transactions found!")
        df = pd.DataFrame(all_transactions)
        if os.path.exists("transactions.csv"):
            df_existing = pd.read_csv("transactions.csv")
            df = pd.concat([df_existing, df], ignore_index=True)
            df.drop_duplicates(subset=['hash'], inplace=True)
        df.to_csv('transactions.csv', index=False)
        return df
    else:
        return pd.DataFrame()


