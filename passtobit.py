from hashlib import sha256
from bit import Key
from bit.format import bytes_to_wif
import random
import string
import time

def generate_password(num_digits, num_letters, num_special_chars):
    digits = ''.join(random.choices(string.digits, k=num_digits))
    letters = ''.join(random.choices(string.ascii_letters, k=num_letters))
    special_chars = ''.join(random.choices(string.punctuation, k=num_special_chars))
    password = digits + letters + special_chars
    password_list = list(password)
    random.shuffle(password_list)
    return ''.join(password_list)

num_passwords = int(input("Number of addresses: "))
num_digits = int(input("Number of digits in the password: "))
num_letters = int(input("Number of letters in the password: "))
num_special_chars = int(input("Number of special characters in the password: "))

generated_count = 0
found_count = 0
total_balance = 0

while generated_count < num_passwords:
    try:
        password = generate_password(num_digits, num_letters, num_special_chars)
        print("Generated password:", password)
        generated_count += 1

        private_key_hex = sha256(password.encode('utf-8')).hexdigest()
        Wallet_compressed = Key.from_hex(private_key_hex)
        Wallet_uncompressed = Key(bytes_to_wif(Wallet_compressed.to_bytes(), compressed=False))

        balance_compressed = int(Wallet_compressed.get_balance('btc'))
        balance_uncompressed = int(Wallet_uncompressed.get_balance('btc'))
        total_balance += balance_compressed + balance_uncompressed

        if balance_compressed != 0 or balance_uncompressed != 0:
            found_count += 1
            print("\033[92mBalance found!\033[0m")
        else:
            print("Balance not found.")

        print('PrivateKey (hex): ' + Wallet_compressed.to_hex())
        print('Bitcoin Address Compressed: ' + Wallet_compressed.address)
        print('Bitcoin Address Uncompressed: ' + Wallet_uncompressed.address)
        print('PrivateKey (wif) Compressed: ' + Wallet_compressed.to_wif())
        print('PrivateKey (wif) Uncompressed: ' + Wallet_uncompressed.to_wif())
        print()

        with open("WINTER.txt", "a") as f:
            f.write('PrivateKey (hex): ' + Wallet_compressed.to_hex() + '\n')
            f.write('Bitcoin Address Compressed: ' + Wallet_compressed.address + '\n')
            f.write('Bitcoin Address Uncompressed: ' + Wallet_uncompressed.address + '\n')
            f.write('PrivateKey (wif) Compressed: ' + Wallet_compressed.to_wif() + '\n')
            f.write('PrivateKey (wif) Uncompressed: ' + Wallet_uncompressed.to_wif() + '\n')
            f.write('\n')

        print(f"Number of passwords: {generated_count}")
        print(f"With balance: {found_count}")
        print(f"Total balance: {total_balance} BTC\n")
    except Exception as e:
        print(f"Error: {e}. Retrying in 5 seconds...")
        time.sleep(5)

print("Successfully written to file WINTER.txt.")
