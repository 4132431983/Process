import secrets
import requests
import sys
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

# Define the range boundaries in hexadecimal
start_hex = int('20000000000000000', 16)
end_hex = int('3ffffffffffffffff', 16)
num_hex_values = 20000

# Create a progress bar
progress_bar = tqdm(total=num_hex_values, unit='hex', file=sys.stdout)

def check_website(hex_value):
    # Perform the search on the website
    url = f"https://privatekeys.pw/raw/{hex_value}"
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        # Extract the relevant information using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        result_elem = soup.find('div', {'class': 'result'})
        if result_elem:
            result = result_elem.text.strip()
            return result

    return None

# Open the file for writing the results
with open("winner.txt", "w") as output_file:
    for _ in range(num_hex_values):
        # Generate a random integer between start_hex and end_hex (both inclusive)
        random_int = secrets.randbelow(end_hex - start_hex + 1) + start_hex

        # Convert the integer to hexadecimal and remove the '0x' prefix
        random_hex = hex(random_int)[2:].zfill(16)

        # Check the website for the raw hexadecimal value
        result = check_website(random_hex)

        if result:
            # Write the result to the file "winner777.txt"
            print(f"Hex Value: {random_hex}, Result: {result}", file=output_file)

        # Update the progress bar
        progress_bar.update()

        # Add a delay of 1 second between consecutive requests
        time.sleep(1)

# Close the progress bar
progress_bar.close()
