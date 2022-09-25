1. Swap ETH for WETH
2. Deposit WETH to aave
3. Borrow some asset with the ETH colateral
    1. Sell borrowed asset (Short)
4. Repay everything back


Testign: 

Integration test nw: Goerli.
Unit test: Mainnet-fork (Mock all mainnet)

IMPORTANT: Currently, the goeli network is not working properly (09/25/2022) and when debugging the error ValueError: Estimated gas value, use mainnet-fork to test if the goerli network is not working properly.
Aave informatio: https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool