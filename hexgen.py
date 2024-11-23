import secrets
from tqdm import tqdm
import sys

# Define the range boundaries in hexadecimal
start_hex = int('20000000000000000', 16)
end_hex = int('3ffffffffffffffff', 16)

# Number of random hex numbers to generate
num_hex_values = 20

# Create a progress bar
progress_bar = tqdm(total=num_hex_values, unit='hex', file=sys.stdout)

# Open the file for writing
output_file = 'random_hex_values.txt'
with open(output_file, 'w') as file:
    # Generate random hexadecimal numbers
    for _ in range(num_hex_values):
        # Generate a random integer between start_hex and end_hex (both inclusive)
        random_int = secrets.randbelow(end_hex - start_hex + 1) + start_hex

        # Convert the integer to hexadecimal and remove the '0x' prefix
        random_hex = hex(random_int)[2:].zfill(16)

        # Write the generated hexadecimal value to the file
        file.write(random_hex + '\n')

        # Update the progress bar
        progress_bar.update()

# Close the progress bar
progress_bar.close()

print(f"Random hexadecimal values written to '{output_file}'.")
