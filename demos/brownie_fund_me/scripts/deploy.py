from brownie import FundMe, MockV3Aggregator, network, config
from scripts.utils import get_account


def deploy_fund_me():
    account = get_account()
    # pass the price feed address
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"active network is {network.show_active()}")
        print(f"Deploying Mocks")
        mock_aggregator = MockV3Aggregator.deploy(
            18, 2000000000000000000, {"from": account}
        )
        price_feed_address = mock_aggregator.address
        print(f"Mocks Deployed!")
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
