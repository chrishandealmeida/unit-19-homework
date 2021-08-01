# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os
from pprint import pprint
from eth_account import Account

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3

from constants import *
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
#from eth_account import Account
from web3 import Web3, middleware, Account
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


# Create a function called `derive_wallets`

def derive_wallets(coin, numderive):
    command = f'./derive -g --mnemonic="{mnemonic}" --coin={coin} --numderive={numderive} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a dictionary object called coins to store the output from `derive_wallets`.

coins = {
    'btc-test': derive_wallets(BTCTEST, 3),
    'eth': derive_wallets(ETH, 3),
    'btc' : derive_wallets(BTC, 3),

}


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

    
# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.

def create_tx(coin, account, to, amount):
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": w3.eth.estimateGas({"from": account.address, "to": to, "value": amount}),
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainID": web3.eth.getChainId([callback])
        }
        
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

    
# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.

def send_tx(coin, account, to, amount):
    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin == ETH:
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction).hex()
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)


# BTCTEST Transaction

# btctest_wallet = priv_key_to_account(BTCTEST, priv_key='cN3z7qdY95N2zBG6gcnyDjjtw1W65gfHoA5HtynnA3zRc8VQH97J')
# create_tx(BTCTEST,btctest_wallet,"mzBG8RCFrvLySfBXjB9pozZUC3RFWgzAJY", 0.00001)
# send_tx(BTCTEST, btctest_wallet, 'mr5UkUZ5jZB9TSqgQtVLVi67HDQ8i395c6', 0.00001)

# ETH Transaction - Refer to ReadMe for reason why this section was not completable.

# eth_wallet = priv_key_to_account(ETH, priv_key='0x49f2dfd16c766cf63fdddd459664d120ad69fce6ffbb0d4d9d6516fd9f9841eb')
# create_tx(ETH,eth_wallet,"0x52968732EC964004a31D5c717D86390d7E218E19", 0.00001)
# send_tx(ETH, eth_wallet, '0x3956331AD54Fc606CbC9d8C4F1725A808d090c53', 0.00001)