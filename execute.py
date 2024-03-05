import os

from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import HexStr
from web3 import Web3

from zksync2.core.types import Token
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.transaction.transaction_builders import TxWithdraw
