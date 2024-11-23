from binascii import hexlify, unhexlify
from bitcoin import *
import colorama
from colorama import Fore, Style
colorama.init()
import multiprocessing
import mnemonic
import bip32utils
from mnemonic import Mnemonic
from random import choice
import requests
import signal
import sys

# List of numbers used in the generation process
x = list(range(2, 257))
xx = [2, 3, 4]

# Counters
total_addresses_generated = multiprocessing.Value('i', 0)
addresses_with_balance = multiprocessing.Value('i', 0)
unchecked_addresses = multiprocessing.Value('i', 0)

# Multiple API URLs for balance checking
apis = [
    'https://blockchain.info/q/getreceivedbyaddress/',
    'https://api.blockcypher.com/v1/btc/main/addrs/',
    'https://api.blockchair.com/bitcoin/dashboards/address/'
]

def b2h(b):
    h = hexlify(b)
    return h if sys.version < "3" else h.decode("utf8")

# Function to generate mnemonic based on user choice (12-word or 24-word) and language
def generate_new(word_count, language):
    mnemo = Mnemonic(language)
    n = choice(x)
    nn = choice(xx)
    
    # Adjusting data size based on 12 or 24 word mnemonic
    if word_count == 12:
        entropy_bytes = 128 // 8  # For 12 words
    else:
        entropy_bytes = 256 // 8  # For 24 words
    
    data = "".join(chr(choice(range(0, int(n)))) for _ in range(entropy_bytes))
    if sys.version >= "3":
        data = data.encode("latin1")
    data = b2h(data)
    mnemonic_words = mnemo.to_mnemonic(unhexlify(data))
    return mnemonic_words
  
def generate_private_key(mnemonic_words, language):
    mobj = Mnemonic(language)
    seed = mobj.to_seed(mnemonic_words)
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)
    return bip32_child_key_obj.WalletImportFormat()
    
def generate_address(mnemonic_words, language):
    mobj = Mnemonic(language)
    seed = mobj.to_seed(mnemonic_words)
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)
    return bip32_child_key_obj.Address()

# Function to check balance using multiple APIs
def check_balance(address):
    for api in apis:
        try:
            response = requests.get(api + address)
            if 'blockchain.info' in api:
                balance = response.json() / 100000000  # Convert balance to BTC
            elif 'blockcypher' in api:
                balance = response.json().get('final_balance', 0) / 100000000
            elif 'blockchair' in api:
                data = response.json()
                balance = data.get('data', {}).get(address, {}).get('address', {}).get('balance', 0) / 100000000
            return balance
        except:
            continue  # If one API fails, move to the next
    # If none of the APIs succeed
    with unchecked_addresses.get_lock():
        unchecked_addresses.value += 1
    return 0

# Function to handle graceful shutdown on CTRL+C
def signal_handler(sig, frame):
    print(Fore.RED + "\nGracefully stopping the processes...")  # Inform the user
    sys.exit(0)  # Exit the script

def main(word_count, language):
    signal.signal(signal.SIGINT, signal_handler)  # Handle CTRL + C
    while True:
        new = generate_new(word_count, language)  # Generate new mnemonic based on choice
        private_key = generate_private_key(new, language)  # Generate private key
        address = generate_address(new, language)  # Generate address

        # Increment total addresses counter
        with total_addresses_generated.get_lock():
            total_addresses_generated.value += 1

        balance = check_balance(address)
        
        if balance > 0:
            # Increment addresses with balance counter
            with addresses_with_balance.get_lock():
                addresses_with_balance.value += 1

            print(Fore.BLUE + "KEY!","COMPRESSED   BTC:" + "\n\n" + str(address), str(private_key) + "\n\n" + "BTC:", balance)
            s3 = str(balance)
            with open("FOUND BTC.txt", "a") as f:
                f.write('Private Key: ' + str(private_key) + '\n' +'Word Seed: ' + str(new) + '\n' +'address: ' + str(address) + '\n\n' + "BTC:" + s3 + "\n\n")

        print(Fore.GREEN + "======================= [ SEED BIP32Key ] =======================")
        print(Fore.GREEN + 'Address = ', str(address), '\n')
        print(Fore.BLUE + 'Seed (Mnemonic) = ', str(new))  # Mnemonic displayed in selected language
        print(Fore.GREEN + "======================= [ BALANCE CHECK SEED BIP32Key] =======================")
        print(Fore.RED + "COMPRESSED   BTC:" + str(balance))

        # Display count of total addresses, those with balance, and unchecked ones
        print(Fore.YELLOW + "Total Addresses Generated: ", total_addresses_generated.value)
        print(Fore.CYAN + "Addresses with Balance: ", addresses_with_balance.value)
        print(Fore.MAGENTA + "Unchecked Addresses: ", unchecked_addresses.value)

if __name__ == '__main__':
    # User input for 12 or 24-word mnemonic choice
    word_choice = input("Enter 12 for 12-word mnemonic or 24 for 24-word mnemonic: ")
    if word_choice == '12':
        word_count = 12
    elif word_choice == '24':
        word_count = 24
    else:
        print("Invalid choice! Defaulting to 12-word mnemonic.")
        word_count = 12

    # User input for language selection
    print("Select language for mnemonic generation:")
    print("1: English")
    print("2: French")
    print("3: Italian")
    print("4: Japanese")
    print("5: Spanish")
    print("6: Chinese")  # Added Chinese language option
    
    lang_choice = input("Enter the number corresponding to your language choice: ")
    languages = {
        '1': 'english',
        '2': 'french',
        '3': 'italian',
        '4': 'japanese',
        '5': 'spanish',
        '6': 'chinese_simplified'  # Chinese language code
    }

    language = languages.get(lang_choice, 'english')  # Default to English if choice is invalid

    # Register signal handler for all threads
    signal.signal(signal.SIGINT, signal_handler)
    
    thread = 4  # Number of threads
    processes = []
    for cpu in range(thread):
        p = multiprocessing.Process(target=main, args=(word_count, language))
        processes.append(p)
        p.start()
    
    # Wait for processes to finish
    for p in processes:
        p.join()
