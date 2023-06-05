from solcx import compile_standard, install_solc
import json
from web3 import Web3

def add_vehicle(vehicle_list, vid, speed, lat, lon, address, private_key, chain_id, nonce):
    add_vehicle_transaction = vehicle_list.functions.addVehicle(vid, speed, lat, lon).build_transaction(
        {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce}
    )

    # Sign the transaction
    sign_add_vehicle = w3.eth.account.sign_transaction(add_vehicle_transaction, private_key=private_key)
    # Send the transaction
    send_add_vehicle = w3.eth.send_raw_transaction(sign_add_vehicle.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_add_vehicle)

    print(f"New vehicle added! VID: {vid}, Speed: {speed}, Latitude: {lat}, Longitude: {lon}")
    print(vehicle_list.functions.retrieve().call())

def remove_vehicle(vehicle_list, vid, address, private_key, chain_id, nonce):
    remove_vehicle_transaction = vehicle_list.functions.removeVehicle(vid).build_transaction(
        {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce}
    )

    # Sign the transaction
    sign_remove_vehicle = w3.eth.account.sign_transaction(remove_vehicle_transaction, private_key=private_key)
    # Send the transaction
    send_remove_vehicle = w3.eth.send_raw_transaction(sign_remove_vehicle.rawTransaction)

    # Wait for the transaction to be mined, and get the transaction receipt
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_remove_vehicle)

    print(f"Vehicle removed! VID: {vid}")
    print(vehicle_list.functions.retrieve().call())

with open("VehicleList.sol", "r") as file:
    contact_list_file = file.read()

install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"VehicleList.sol": {"content": contact_list_file}},
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
bytecode = compiled_sol["contracts"]["VehicleList.sol"]["VehicleList"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["VehicleList.sol"]["VehicleList"]["metadata"]
)["output"]["abi"]

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
address = "0xE783008Ab078Dc551e0B7aC77A22785753543E62"
private_key = (
    "0xa955eea12cabb1abd3b3c7916652cd062b7600eb037138c986a30d8e1b6eeedc"
)  # leaving the private key like this is very insecure if you are working on real world project

# Create the contract in Python
VehicleList = w3.eth.contract(abi=abi, bytecode=bytecode)
print('Contract created')
# Get the latest transaction
nonce = w3.eth.get_transaction_count(address)
print('Got the latest transaction')
# build transaction
transaction = VehicleList.constructor().build_transaction(
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

vehicle_list = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

# Call add_vehicle function
vid = 1
speed = 100
latitude = "8.21462"
longitude = "10.26429"
add_vehicle(vehicle_list, vid, speed, latitude, longitude, address, private_key, chain_id, nonce + 1)

# Call add_vehicle function again with different data
vid = 2
speed = 80
latitude = "5.127386"
longitude = "13.98342"
add_vehicle(vehicle_list, vid, speed, latitude, longitude, address, private_key, chain_id, nonce + 2)

# Call remove_vehicle function to remove a vehicle
vehicle_id_to_remove = 1
remove_vehicle(vehicle_list, vehicle_id_to_remove, address, private_key, chain_id, nonce + 3)

