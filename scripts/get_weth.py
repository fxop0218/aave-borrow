# https://goerli.etherscan.io/address/0xb4fbf271143f4fbf7b91a5ded31805e42b2208d6#writeContract WETH Contract

from brownie import interface, config, network
from scripts.helpful_scripts import get_account

WETH_T = "weth_token"
NETWORKS = "networks"

def main():
    get_weth()

def get_weth():
    """
    Mint wETH deposition ETH

    Don't use get_contract funcition becuase we don't use mocks in this case
    """
    account = get_account()
    weth = interface.IWeth(config[NETWORKS][network.show_active()][WETH_T])
    transaction = weth.deposit({"from": account, "value" : 0.1 * 10 ** 18})
    transaction.wait(1)
    print(f"0.1 wETH recived")
    return transaction