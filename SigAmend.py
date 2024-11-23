#!/usr/bin/env python3

from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.script import CScript, OP_DUP, OP_IF, OP_ELSE, OP_ENDIF, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL, SIGHASH_SINGLE
from bitcoinlib.config.opcodes import *
from bitcoinlib.encoding import *
from bitcoinlib.keys import Key
from bitcoinlib.keys import Signature, Key, HDKey
from bitcoinlib.main import *
from cryptos import *
import bitcoin
import bitcoinlib
import cryptos
import hashlib


c = Bitcoin(testnet=False)
# Step 1: Retrieve the transaction containing the input you want to sign
transaction_hex = "0200000001d1a06d6de8ae9ea26f4fa1e69fe0a65034b050571f6e5e607db71af7160b50e30100000000ffffffff0200752b7d0000000017a914a1fc517c18c3f2530a54ff337b2f7576cfc672688700b4c404000000001976a914c506ceef4892dff204adce76e2a7ec576bb8db3a88ac00000000"
index = 0  # Index of the input you want to sign

# Step 2: Deserialize the transaction
try:
    transaction = deserialize(transaction_hex)
except Exception as e:
    print(f"Error deserializing the transaction: {str(e)}")
    exit(1)

#print(transaction)

# Step 3: Replace the public key script of the input you want to sign
input_to_sign = transaction['ins'][index]
output_spent = input_to_sign['script']
#print(output_spent)
input_to_sign['script'] = output_spent

# Step 4: Set other input scripts to empty scripts
#for input in transaction['ins']:
#    if input != input_to_sign:
#        input['script'] = CScript([])

# Step 5: Define the SIGHASH type
sighash_type = SIGHASH_SINGLE  # SIGHASH_SINGLE = 0x03

# Step 6: Serialize the modified transaction
serialized = serialize(transaction)
serialized = bytes.fromhex(serialized)

# Step 7: Hash the serialized transaction
hash = hashlib.sha256(hashlib.sha256(serialized).digest()).digest()

# Step 8: Create a private key and sign the signature hash
private_key = Key("046b597d78150fd318bcb6133c2e24029ebfaab129711574a61d7cfb05f4699d")  # Replace with your private key
signature = bitcoinlib.keys.sign(hash,private_key)

print(f"Signature hash: {hash.hex()}")
print(f"Signature: {signature.hex()}")

