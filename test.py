from wallet_connect import wallet_connect

connect_button = wallet_connect(label="wallet", key="wallet1")
send_transaction = wallet_connect(label="send", key="send", message="Send Transaction", contract_address="0x8362F6588682a8DDf898026B792B804AE7719895", amount="12033120", to_address="0x8362F6588682a8DDf898026B792B804AE7719895")
print(send_transaction)