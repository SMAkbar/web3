from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

# compile our solidity

compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# print(compile_sol)
with open("compile_code.json", "w") as file:
    json.dump(compile_sol, file)

# get byte code
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# connecting to rinkeby
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/b27eb5f9ea0840a7ac7bcf10697c17bc")
)
chain_id = 4  # can be found on internet... chain id for rinkeby
my_address = "0x9BA7D5E019c2cA8C1ADd76980dd8da7379b68b98"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)


# create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)


# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# block confirmation --- wait for transaction to complete
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# working with contract you always need
# contract address
# contract abi

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call -> Simulate making a call and getting a value
# transact -> Make a state change

# initial value of contract
print(simple_storage.functions.retreive().call())

# transction
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
transaction_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)


# initial value of contract
print(simple_storage.functions.retreive().call())
