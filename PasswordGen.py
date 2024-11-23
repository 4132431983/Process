import itertools
import pyfiglet
import textwrap

banner_text = "Password Generator"
wrapped_text = "\n".join(textwrap.wrap(banner_text, width=40))
banner = pyfiglet.figlet_format(wrapped_text)
print(banner)

# Print the welcome message
print('Welcome to Password Generator!')


def generate_wordlist(characters, min_length, max_length, output_file, size_limit, size_unit, last_password=None):
    size_multiplier = {'MB': 1024 ** 2, 'GB': 1024 ** 3, 'TB': 1024 ** 4, 'PB': 1024 ** 5, 'EB': 1024 ** 6,
                       'ZB': 1024 ** 7, 'YB': 1024 ** 8}

    with open(output_file, 'a') as file:
        total_size_bytes = 0
        size_reached = False
        start_writing = not last_password

        for length in range(min_length, max_length + 1):
            for combination in itertools.product(characters, repeat=length):
                word = ''.join(combination)
                if not start_writing:
                    if word == last_password:
                        start_writing = True
                    continue

                file.write(word + '\n')
                total_size_bytes += len(word) + 1

                if size_limit and total_size_bytes >= size_limit * size_multiplier[size_unit]:
                    size_reached = True
                    break

        if size_reached:
            print(f"Size limit of {size_limit} {size_unit} reached.")
            continue_prompt = input("Do you want to continue generating passwords? (y/n): ").lower()
            if continue_prompt == 'y':
                new_size_limit = float(input("Enter the new size limit for the wordlist file: "))
                new_size_unit = input("Select size unit for the new size limit (MB, GB, TB, PB, EB, ZB, YB): ")
                new_output_file = input("Enter the new output file name: ")
                last_password_input = input("Enter the last password to continue from: ")
                generate_wordlist(characters, min_length, max_length, new_output_file, new_size_limit, new_size_unit,
                                  last_password_input)
            else:
                print("Wordlist generation stopped.")
        else:
            print("All password combinations generated.")


if __name__ == "__main__":
    charset = input("Enter the charset for the wordlist: ")
    min_length = int(input("Enter minimum length: "))
    max_length = int(input("Enter maximum length: "))
    output_file = input("Enter output file name: ")

    use_size_limit = input("Do you want to set a size limit for the wordlist file? (y/n): ").lower()
    if use_size_limit == 'y':
        size_limit = float(input("Enter size limit for the wordlist file: "))
        size_unit = input("Select size unit (MB, GB, TB, PB, EB, ZB, YB): ")
    else:
        size_limit = None
        size_unit = None

    generate_wordlist(charset, min_length, max_length, output_file, size_limit, size_unit)