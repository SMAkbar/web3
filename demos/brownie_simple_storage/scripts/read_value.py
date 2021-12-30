from brownie import SimpleStorage, accounts, config


def read_contract():
    # print(SimpleStorage[0])
    simple_storage = SimpleStorage[-1]  # SimpleStorage is an array, -1 is the latest

    print(simple_storage.retreive())


def main():
    read_contract()
