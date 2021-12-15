from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retreive()
    expected = 0
    # Assert
    assert starting_value == expected


def test_update_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    expected = 15
    storing_value = simple_storage.store(expected, {"from": account})
    final_value = simple_storage.retreive()
    # Assert
    assert final_value == expected
