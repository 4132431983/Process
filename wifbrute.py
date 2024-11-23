import hashlib
import base58
import ecdsa
import random

# BTC addresses ko set mein load karna
with open("btc_addresses.txt", "r") as file:
    btc_addresses = {line.strip() for line in file}

# Count variables
generated_count = 0
found_count = 0

# Uncompressed WIF private key generate karna
def generate_uncompressed_wif_private_key():
    private_key_hex = ''.join(random.choices("0123456789abcdef", k=64))
    extended_key = "80" + private_key_hex
    first_sha = hashlib.sha256(bytes.fromhex(extended_key)).digest()
    second_sha = hashlib.sha256(first_sha).digest()
    checksum = second_sha[:4]
    wif_key = extended_key + checksum.hex()
    wif_key = base58.b58encode(bytes.fromhex(wif_key)).decode('utf-8')
    return wif_key, private_key_hex

# Compressed WIF private key generate karna
def generate_compressed_wif_private_key():
    private_key_hex = ''.join(random.choices("0123456789abcdef", k=64))
    extended_key = "80" + private_key_hex + "01"
    first_sha = hashlib.sha256(bytes.fromhex(extended_key)).digest()
    second_sha = hashlib.sha256(first_sha).digest()
    checksum = second_sha[:4]
    wif_key = extended_key + checksum.hex()
    wif_key = base58.b58encode(bytes.fromhex(wif_key)).decode('utf-8')
    return wif_key, private_key_hex

# BTC address generate karna (compressed ya uncompressed)
def generate_btc_address(private_key_hex, compressed=False):
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = vk.to_string()

    if compressed:
        # Compressed public key
        prefix = b'\x03' if (public_key[-1] % 2 != 0) else b'\x02'
        public_key = prefix + public_key[:32]
    else:
        # Uncompressed public key
        public_key = b'\x04' + public_key

    sha256_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    extended_ripemd160 = b'\x00' + ripemd160_hash
    checksum = hashlib.sha256(hashlib.sha256(extended_ripemd160).digest()).digest()[:4]
    btc_address = base58.b58encode(extended_ripemd160 + checksum).decode('utf-8')
    return btc_address

# Script run karein aur matching address dhundein
found = False
while not found:
    if random.choice([True, False]):
        wif_key, private_key_hex = generate_uncompressed_wif_private_key()
        btc_address = generate_btc_address(private_key_hex, compressed=False)
    else:
        wif_key, private_key_hex = generate_compressed_wif_private_key()
        btc_address = generate_btc_address(private_key_hex, compressed=True)

    generated_count += 1
    print(f"Generated Address #{generated_count}: {btc_address} - WIF Key: {wif_key}")
    print(f"Total Found Count: {found_count}")

    if btc_address in btc_addresses:
        found_count += 1
        print("\nMatch found!")
        print(f"Address: {btc_address}")
        print(f"WIF Key: {wif_key}")
        with open("found.txt", "a") as found_file:
            found_file.write(f"Address: {btc_address}, WIF Key: {wif_key}\n")
        found = True
    else:
        print(f"Address '{btc_address}' checked - No match.\n")
