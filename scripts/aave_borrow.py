from dataclasses import dataclass
from brownie import accounts, network, config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import NETWORKS, WETH_T, get_weth
from web3 import Web3

amount = Web3.toWei(0.05, "ether")

def main():
    account = get_account()
    erc20_address = config[NETWORKS][network.show_active()][WETH_T]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # ABI
    # Address 
    lending_pool = get_landing_pool()
    # print(lending_pool)
    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing")
    transaction = lending_pool.deposit(erc20_address, amount , account.address, 0, {"from": account})
    transaction.wait(1)
    print("Deposit completed")
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    # 0.1 ETH deposited = 0.8 borrowable for Loan to value more information in: https://docs.aave.com/risk/v/aave-v2/asset-risk/risk-parameters
    print("Let's borrow") # Borrowing tutorial https://blog.chain.link/blockchain-fintech-defi-tutorial-lending-borrowing-python/
    if network.show_active() in ["mainnet-fork"]:
        dai_eth_price = get_assert_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
        amount_dai_to_borrow = (1/dai_eth_price) * (borrowable_eth * 0.95) # Borrowable ==> borrowable_dai * 95%
        print(f"We are going to borrow {amount_dai_to_borrow} DAI")
        # Now we borrow
        dai_address = config["networks"][network.show_active()]["dai_token"]
        borrow_transaction = lending_pool.borrow(dai_address,
            Web3.toWei(amount_dai_to_borrow, "ether"),
            1,
            0,
            account.address,
            {"from" : account}
        ) # More information https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#borrow
        borrow_transaction.wait(1)
        print("We borrowed some DAI")
        get_borrowable_data(lending_pool, account)

    else: 
        raise "Goerli network don't have this feature"

def get_assert_price(price_feed_address):
    #ABI
    #Address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1] # This function returns multiple values, so we specify the second value ==> [1]. 
    latest_price_eth = Web3.fromWei(latest_price, "ether")
    print(f"DAI/ETH actual price is {latest_price_eth}")
    return float(latest_price)
    #0.000767811356266655

def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))



def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token")
    erc20 = interface.IERC20(erc20_address)
    transaction = erc20.approve(spender, amount, {"from" : account, "gasLimit" : 1000000000000000000})
    transaction.wait(1)
    return transaction

def get_landing_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["landing_pool_address_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    # ABI
    # Address
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool