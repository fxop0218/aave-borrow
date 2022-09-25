from scripts.aave_borrow import approve_erc20, get_landing_pool
from brownie import config, network
from web3 import Web3
from scripts.helpful_scripts import get_account

# approve_erc20(amount, spender, erc20_address, account)
def test_approve_erc20():
    # Arrange
    account = get_account()
    lending_pool = get_landing_pool()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    amount = Web3.toWei(1, "ether")
    # act
    tx = approve_erc20(amount, lending_pool.address, erc20_address, account)
    # assert
    assert tx is not True