import bitcoin
import binascii
import multiprocessing
import pyfiglet
import textwrap
import time

banner_text = "SUPER VANITYGEN"
wrapped_text = "\n".join(textwrap.wrap(banner_text, width=40))
banner = pyfiglet.figlet_format(wrapped_text)
print(banner)

# Print the welcome message
print('Welcome to SUPER VANITYGEN!')

# Prompt the user for the Bitcoin address prefix
address_prefix = input("Enter the Bitcoin address prefix to search for: ")

# Prompt the user for the range exponent
exponent = int(input("Enter the range exponent: "))

# Prompt the user for the number of threads to use
num_threads = int(input("Enter the number of threads: "))

# Define a function to search for matching addresses within a given range
def search_private_keys(start, end):
    for i in range(start, end + 1):
        private_key = binascii.hexlify(i.to_bytes(32, 'big')).decode()
        public_key_uncompressed = bitcoin.privtopub(private_key)
        bitcoin_address_uncompressed = bitcoin.pubtoaddr(public_key_uncompressed)

        if bitcoin_address_uncompressed.startswith(address_prefix):
            print("Private Key Found!")
            print("Private Key:", private_key)
            print("Bitcoin Address (Uncompressed):", bitcoin_address_uncompressed)

        public_key_compressed = bitcoin.compress(public_key_uncompressed)
        bitcoin_address_compressed = bitcoin.pubtoaddr(public_key_compressed)

        if bitcoin_address_compressed.startswith(address_prefix) and bitcoin_address_compressed != bitcoin_address_uncompressed:
            print("Private Key Found!")
            print("Private Key:", private_key)
            print("Bitcoin Address (Compressed):", bitcoin_address_compressed)

# Define a function to search for unique matches until no more are found
def search_until_no_matches():
    # Calculate the total number of private keys to search
    total_keys = 2 ** exponent

    # Calculate the keys per thread based on the total keys and number of threads
    keys_per_thread = total_keys // num_threads

    # Create and start the search processes using multiprocessing
    processes = []
    for i in range(num_threads):
        start = 1 + i * keys_per_thread
        end = start + keys_per_thread - 1 if i < num_threads - 1 else total_keys
        process = multiprocessing.Process(target=search_private_keys, args=(start, end))
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()

# Main loop
continue_searching = True
while continue_searching:
    start_time = time.time()
    search_until_no_matches()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Total search time: {:.2f} seconds".format(elapsed_time))

    answer = input("No more matches found. Do you want to continue searching? (yes/no): ")
    if answer.lower() != "yes":
        continue_searching = False
        break

    # Prompt for new input
    print("\n-------------------\n")
    address_prefix = input("Enter the Bitcoin address prefix to search for: ")
    exponent = int(input("Enter the range exponent: "))
    num_threads = int(input("Enter the number of threads: "))