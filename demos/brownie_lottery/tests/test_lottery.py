# 0.019

from brownie import Lottery, accounts, config, network
from web3 import Web3
from time import time


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    assert lottery.getEntranceFee() > Web3.toWei(0.00001, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(1.000, "ether")
