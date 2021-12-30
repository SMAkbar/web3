from brownie import accounts, config, SimpleStorage, network
from brownie.network.gas.strategies import GasNowStrategy


def deploy_simple_storage():
    gas_strategy = GasNowStrategy("fast")
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    # trax or call
    # print(simple_storage)
    store_value = simple_storage.retreive()
    print(store_value)

    transaction = simple_storage.store(15, {"from": account, "priority_fee": "2 gwei"})
    transaction.wait(1)
    updated_store_value = simple_storage.retreive()
    print(updated_store_value)


def get_account():
    if network.show_active == "developement":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
