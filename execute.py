import os
import configparser

from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import HexStr, HexAddress
from eth_utils import to_checksum_address
from web3 import Web3

from zksync2.account.wallet import Wallet
from zksync2.core.types import ZkBlockParams, EthBlockParams
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.signer.eth_signer import PrivateKeyEthSigner
from zksync2.transaction.transaction_builders import TxFunctionCall


def get_zk_eth_balance(zk_web3: ZkSyncBuilder, address: HexAddress) -> float:
    """
    Get ETH balance of ETH address on zkSync network

    :param zk_web3:
        Instance of ZkSyncBuilder that interacts with zkSync network

    :param address:
       ETH address that you want to get balance of.

    :return:
       Balance of ETH address.

    """

    # Get WEI balance of ETH address
    balance_wei = zk_web3.zksync.get_balance(
        address,
        EthBlockParams.LATEST.value
        )

    # Convert WEI balance to ETH
    balance_eth = Web3.from_wei(balance_wei, "ether")

    # Return the ETH balance of the ETH address
    return balance_eth


def get_l1_eth_balance(eth_web3: ZkSyncBuilder, address: HexAddress) -> float:
    """
    Get ETH balance of ETH address on zkSync network

    :param zk_web3:
        Instance of ZkSyncBuilder that interacts with zkSync network

    :param address:
       ETH address that you want to get balance of.

    :return:
       Balance of ETH address.

    """

    # Get WEI balance of ETH address
    balance_wei = eth_web3.eth.get_balance(
        address,
        EthBlockParams.LATEST.value
        )

    # Convert WEI balance to ETH
    balance_eth = Web3.from_wei(balance_wei, "ether")

    # Return the ETH balance of the ETH address
    return balance_eth


if __name__ == "__main__":

    # Get wallet addresses and primary keys from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    test_wallet_1 = config['zksync_test']['test_wallet_1']
    test_pk_1 = config['zksync_test']['test_primary_key_1']
    test_wallet_2 = config['zksync_test']['test_wallet_2']
    test_pk_2 = config['zksync_test']['test_primary_key_2']

    # Define RPC providers and network connector objects
    ZKSYNC_PROVIDER = "https://sepolia.era.zksync.dev"
    ETH_PROVIDER = "https://rpc.ankr.com/eth_sepolia"

    zk_web3 = ZkSyncBuilder.build(ZKSYNC_PROVIDER)
    eth_web3 = Web3(Web3.HTTPProvider(ETH_PROVIDER))

    # Get account object by providing from private key
    account1: LocalAccount = Account.from_key(test_pk_1)
    account2: LocalAccount = Account.from_key(test_pk_2)    

    # Show zk ETH balance before ETH transfer
    print(f"Account 1 zk ETH balance before transfer : {get_zk_eth_balance(zk_web3, account1.address)} ETH")
    print(f"Account 2 zk ETH balance before transfer : {get_zk_eth_balance(zk_web3, account2.address)} ETH")

    # Show zk ETH balance after ETH transfer
    print(f"Account 1 zk ETH balance before transfer : {get_zk_eth_balance(zk_web3, account1.address)} ETH")
    print(f"Account 2 zk ETH balance before transfer : {get_zk_eth_balance(zk_web3, account2.address)} ETH")

    # Show L1 ETH balance before ETH transfer
    print(f"Account 1 L1 ETH balance before transfer : {get_l1_eth_balance(eth_web3, account1.address)} ETH")
    print(f"Account 2 L1 ETH balance before transfer : {get_l1_eth_balance(eth_web3, account2.address)} ETH")

    # Show L1 ETH balance after ETH transfer
    print(f"Account 1 L1 ETH balance before transfer : {get_l1_eth_balance(eth_web3, account1.address)} ETH")
    print(f"Account 2 L1 ETH balance before transfer : {get_l1_eth_balance(eth_web3, account2.address)} ETH")

    nonce = zk_web3.zksync.get_transaction_count(account1.address, ZkBlockParams.COMMITTED.value)
    nonce = zk_web3.zksync.get_transaction_count(account2.address, ZkBlockParams.COMMITTED.value)

    print(nonce)
    
    wallet = Wallet(zk_web3, eth_web3, account1)
    amount_eth = 0
    amount_wei = Web3.to_wei(amount_eth, "ether")
    is_approved = wallet.approve_erc20(account1.address, amount_wei)

    print(amount_wei)
    print(is_approved)

