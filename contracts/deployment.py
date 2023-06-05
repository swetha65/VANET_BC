from solcx import compile_standard, install_solc
import json
from web3 import Web3

def add_contact(contact_list, name, phone, address, private_key, chain_id, nonce):
    add_contact_transaction = contact_list.functions.addContact(name, phone).build_transaction(
        {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce}
    )

    # Sign the transaction
    sign_add_contact = w3.eth.account.sign_transaction(add_contact_transaction, private_key=private_key)
    # Send the transaction
    send_add_contact = w3.eth.send_raw_transaction(sign_add_contact.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_add_contact)

    print(f"New contact added! Name: {name}, Phone: {phone}")
    print(contact_list.functions.retrieve().call())

def remove_contact(contact_list, contact_id, address, private_key, chain_id, nonce):
    remove_contact_transaction = contact_list.functions.removeContact(contact_id).build_transaction(
        {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce}
    )

    # Sign the transaction
    sign_remove_contact = w3.eth.account.sign_transaction(remove_contact_transaction, private_key=private_key)
    # Send the transaction
    send_remove_contact = w3.eth.send_raw_transaction(sign_remove_contact.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_remove_contact)

    print(f"Contact removed! Contact ID: {contact_id}")
    print(contact_list.functions.retrieve().call())

with open("ContactList.sol", "r") as file:
    contact_list_file = file.read()

install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ContactList.sol": {"content": contact_list_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                        "abi",
                        "metadata",
                        "evm.bytecode",
                        "evm.bytecode.sourceMap",
                    ]  # output needed to interact with and deploy contract
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiler_output.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["ContactList.sol"]["ContactList"]["metadata"]
)["output"]["abi"]

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
address = "0xE783008Ab078Dc551e0B7aC77A22785753543E62"
private_key = (
    "0xa955eea12cabb1abd3b3c7916652cd062b7600eb037138c986a30d8e1b6eeedc"
)  # leaving the private key like this is very insecure if you are working on real world project

# Create the contract in Python
ContactList = w3.eth.contract(abi=abi, bytecode=bytecode)
print('Contract created')
# Get the latest transaction
nonce = w3.eth.get_transaction_count(address)
print('Got the latest transaction')
# build transaction
transaction = ContactList.constructor().build_transaction(
    {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": address, "nonce": nonce}
)
print('built transaction')
# Sign the transaction
sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send the transaction
transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

contact_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

new_name = "John Doe"
new_phone = "+123456789"
add_contact(contact_list, new_name, new_phone, address, private_key, chain_id, nonce + 1)

# Call add_contact function again with different data
another_name = "Jane Smith"
another_phone = "+987654321"
add_contact(contact_list, another_name, another_phone, address, private_key, chain_id, nonce + 2)

contact_id_to_remove = 0
remove_contact(contact_list, contact_id_to_remove, address, private_key, chain_id, nonce + 3)
