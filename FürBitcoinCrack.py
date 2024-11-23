import random
import requests
import logging
from hdwallet import HDWallet
from hdwallet.symbols import BTC
from colorama import init, Fore

# Initialisierung von Colorama
init()

# Logging-Konfiguration
logging.basicConfig(filename='program_log.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Liste der API-Endpunkte
API_ENDPOINTS = [
    "https://btc4.trezor.io/api/v2/address/",
    "https://blockstream.info/api/address/",
    "https://api.blockcypher.com/v1/btc/main/addrs/",
    # Fügen Sie hier weitere API-Endpunkte hinzu
]

TEST_ADDRESS = "16VDLWz5Hw8MY6eeBngVN5KXn62b6E7a5z"  # Eine bekannte Bitcoin-Adresse

# API-Überprüfungsfunktion
def check_apis():
    working_apis = []
    for endpoint in API_ENDPOINTS:
        try:
            url = f"{endpoint}{TEST_ADDRESS}"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                print(Fore.GREEN + f"API {endpoint} funktioniert." + Fore.RESET)
                working_apis.append(endpoint)
            else:
                print(Fore.RED + f"API {endpoint} hat mit Statuscode {response.status_code} geantwortet." + Fore.RESET)
        except Exception as e:
            print(Fore.RED + f"Fehler bei der Überprüfung der API {endpoint}: {e}" + Fore.RESET)
    return working_apis

# API-Abfragefunktion
def get_balance(address, apis):
    for endpoint in apis:
        try:
            url = f"{endpoint}{address}"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                data = response.json()
                # Anpassung an das Antwortformat der jeweiligen API
                balance = int(data.get('balance', 0)) / 100000000
                return balance
        except Exception as e:
            logging.error(Fore.RED + f"Fehler bei der API-Anfrage an {endpoint}: {e}" + Fore.RESET)
    return None

# Hauptfunktion
def main():
    working_apis = check_apis()
    if not working_apis:
        print(Fore.RED + "Keine APIs sind derzeit verfügbar." + Fore.RESET)
        return

    counter = 0  # Zähler für die generierten Hex-Zahlen (private Schlüssel)

    while True:
        try:
            hd_wallet = HDWallet(symbol=BTC)
            private_key = "".join(random.choice("0123456789abcdef") for _ in range(64))
            hd_wallet.from_private_key(private_key)
            btcaddr1 = hd_wallet.p2pkh_address()
            btcaddr2 = hd_wallet.p2wpkh_address()
            btcaddr3 = hd_wallet.p2wpkh_in_p2sh_address()
            btcaddr4 = hd_wallet.p2wsh_in_p2sh_address()
            btcaddr5 = hd_wallet.p2sh_address()

            value1 = get_balance(btcaddr1, working_apis)
            value2 = get_balance(btcaddr2, working_apis)
            value3 = get_balance(btcaddr3, working_apis)
            value4 = get_balance(btcaddr4, working_apis)
            value5 = get_balance(btcaddr5, working_apis)

            # Ausgabe der generierten Adressen und Salden
            print(Fore.BLUE + f"BTC Address (P2PKH): {btcaddr1} - Balance: {value1 if value1 is not None else 'Anfrage fehlgeschlagen'}" + Fore.RESET)
            print(Fore.BLUE + f"BTC Address (BECH32): {btcaddr2} - Balance: {value2 if value2 is not None else 'Anfrage fehlgeschlagen'}" + Fore.RESET)
            print(Fore.BLUE + f"BTC Address (P2WPKH): {btcaddr3} - Balance: {value3 if value3 is not None else 'Anfrage fehlgeschlagen'}" + Fore.RESET)
            print(Fore.BLUE + f"BTC Address (P2WSH): {btcaddr4} - Balance: {value4 if value4 is not None else 'Anfrage fehlgeschlagen'}" + Fore.RESET)
            print(Fore.BLUE + f"BTC Address (P2SH): {btcaddr5} - Balance: {value5 if value5 is not None else 'Anfrage fehlgeschlagen'}" + Fore.RESET)
            print(Fore.MAGENTA + f"Privater Schlüssel (HEX): {private_key}" + Fore.RESET)

            counter += 1  # Zähler erhöhen
            print(Fore.YELLOW + f"Bisher generierte Hex-Zahlen (private Schlüssel): {counter}\n" + Fore.RESET)

        except KeyboardInterrupt:
            print(Fore.YELLOW + "Programm wurde manuell beendet." + Fore.RESET)
            break
        except Exception as e:
            logging.error(Fore.RED + f"Unerwarteter Fehler im Hauptprogramm: {e}" + Fore.RESET)

if __name__ == "__main__":
    main()
