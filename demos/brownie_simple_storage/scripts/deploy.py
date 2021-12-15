from brownie import accounts, config, SimpleStorage


def deploy_simple_storage():
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # trax or call
    # print(simple_storage)
    store_value = simple_storage.retreive()
    print(store_value)

    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_store_value = simple_storage.retreive()
    print(updated_store_value)


def main():
    deploy_simple_storage()
