import hashlib
import base58
import random
import time
import requests
from ecdsa import SigningKey, SECP256k1

# Generate Bitcoin address from private key
def private_key_to_address(private_key, compressed=True):
    try:
        sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        vk = sk.verifying_key
        if compressed:
            public_key = b'\x02' + vk.to_string()[:32] if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()[:32]
        else:
            public_key = b'\x04' + vk.to_string()
        sha256_1 = hashlib.sha256(public_key).digest()
        ripemd160 = hashlib.new('ripemd160', sha256_1).digest()
        network_byte = b'\x00' + ripemd160
        checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
        address = base58.b58encode(network_byte + checksum).decode()
        return address
    except Exception as e:
        print(f"Error generating address: {e}")
        return None

# Check balance using Blockstream API
def check_balance(address):
    url = f"https://blockstream.info/api/address/{address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("chain_stats", {}).get("funded_txo_sum", 0)
        else:
            return 0
    except Exception as e:
        print(f"Error checking balance for address {address}: {e}")
        return 0

# Fill missing characters randomly
def fill_missing_characters(template):
    hex_chars = "0123456789abcdef"
    filled_key = list(template)
    for i in range(len(filled_key)):
        if filled_key[i] == "*":
            filled_key[i] = random.choice(hex_chars)
    return "".join(filled_key)

# Search for balance
def search_private_key_for_balance():
    private_key_template = input("Enter the private key with missing characters (use * for missing): ")

    if len(private_key_template.replace("*", "0")) != 64:
        print("Error: Invalid private key length. It should be 64 characters including missing ones.")
        return

    missing_count = private_key_template.count("*")
    print(f"Total missing characters: {missing_count}")

    found = False
    checked_combinations = set()  # To avoid repeating the same combination

    while not found:
        combination = fill_missing_characters(private_key_template)
        
        # Skip if the combination is already tested
        if combination in checked_combinations:
            continue
        checked_combinations.add(combination)

        print(f"Checking combination: {combination}")
        
        compressed_address = private_key_to_address(combination, compressed=True)
        uncompressed_address = private_key_to_address(combination, compressed=False)

        if compressed_address:
            compressed_balance = check_balance(compressed_address)
            print(f"Generated compressed address: {compressed_address}")
            print(f"Checked balance for address {compressed_address}: {compressed_balance} satoshis")

            if compressed_balance > 0:
                with open("found.txt", "a") as f:
                    f.write(f"Compressed Address: {compressed_address} | Private Key: {combination}\n")
                print(f"Found balance on compressed address: {compressed_address}")
                found = True

        if uncompressed_address:
            uncompressed_balance = check_balance(uncompressed_address)
            print(f"Generated uncompressed address: {uncompressed_address}")
            print(f"Checked balance for address {uncompressed_address}: {uncompressed_balance} satoshis")

            if uncompressed_balance > 0:
                with open("found.txt", "a") as f:
                    f.write(f"Uncompressed Address: {uncompressed_address} | Private Key: {combination}\n")
                print(f"Found balance on uncompressed address: {uncompressed_address}")
                found = True

        print(f"Total combinations tested: {len(checked_combinations)}\n")
        time.sleep(0.5)  # Optional delay for API rate limiting

    if found:
        print("Matching private key found. Check 'found.txt' for results.")
    else:
        print("No match found yet. Continuing search...")

search_private_key_for_balance()
