import bit
from tqdm import tqdm
import time

def convert_private_key(private_key):
    wallet = bit.Key.from_hex(private_key).address
    return wallet

def save_progress(line_number):
    with open('d:/progress_privatekey.txt', 'w') as progress_file:
        progress_file.write(str(line_number))

def get_last_progress():
    try:
        with open('d:/progress_privatekey.txt', 'r') as progress_file:
            return int(progress_file.read())
    except FileNotFoundError:
        return 0

def write_to_file(wallet, private_key, filepath):
    for _ in range(3):  # Retry 3 times in case of errors
        try:
            with open(filepath, 'a') as file:
                file.write(f"{wallet}|{private_key}\n")
            return True
        except PermissionError:
            print("Permission denied. Retrying after 1 second...")
            time.sleep(1)  # Wait 1 second before retrying

    print("Failed to write to file after multiple retries.")
    return False

def main():
    with open('privatekey_list.txt', 'r') as hex_file:
        lines = hex_file.readlines()

    last_progress = get_last_progress()
    lines = lines[last_progress:]  # Read starting from last processed line
    total_lines = len(lines)

    with tqdm(total=total_lines, initial=last_progress) as pbar:
        for i, line in enumerate(lines, start=last_progress):
            private_key = line.strip()
            wallet = convert_private_key(private_key)

            if write_to_file(wallet, private_key, 'd:/wallets.txt'):
                if (i+1) % 500 == 0:  # Save progress every 100 lines
                    save_progress(i+1)  # Save progress after successfully processing 100 lines

            pbar.update(1)

    # Save progress after processing all lines
    save_progress(len(lines))

if __name__ == '__main__':
    main()
