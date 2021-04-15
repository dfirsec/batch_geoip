import ipaddress
import sys
from pathlib import Path

import requests
from colorama import Fore, init

# Console Colors
init()
CYAN = Fore.CYAN
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
YELLOW = Fore.YELLOW


class Batch_Worker:
    def __init__(self, host):
        self.host = host
        self.parent = Path(__file__).resolve().parent
        self.geo_results = self.parent.joinpath("geo_results.txt")
        self.fg_url = f"https://freegeoip.live/json/{self.host}"
        self.kc_url = f"https://tools.keycdn.com/geo.json?host={self.host}"
        self.ipg_url = f"https://ipgeolocation.io/ip-location/{self.host}"
        self.ipapi_url = f"http://ip-api.com/json/{self.host}"

    def connect(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
        }
        req = requests.get(f"{url}", headers=headers)
        return req

    def process(self):
        # freegeoip.live
        try:
            fg_url = self.connect(self.fg_url).json()
            print(f"\n{CYAN}Freegeoip Results{RESET}\n{('-' * 50)}")
            with open(self.geo_results, "w") as f:
                f.write(f"\nFreegeoip Results\n{('-' * 50)}\n")
            for k, v in fg_url.items():
                if v:
                    print(f"{k.title().replace('_', ' '):15}: {v}")
                    with open(self.geo_results, "a") as f:
                        f.write(f"{k.title().replace('_', ' '):15}: {v}\n")
        except Exception as err:
            print(err)

        # tools.keycdn.com
        try:
            headers = {"User-Agent": f"keycdn-tools:https://{self.host}"}
            kc_url = requests.get(self.kc_url, headers=headers).json()
            print(f"\n{CYAN}KeyCDN Results{RESET}\n{('-' * 50)}")
            with open("geo_results.txt", "a") as f:
                f.write(f"\nKeyCDN Results\n{('-' * 50)}\n")
            for k, v in kc_url["data"]["geo"].items():
                if v:
                    print(f"{k.title().replace('_', ' '):15}: {v}")
                    with open(self.geo_results, "a") as f:
                        f.write(f"{k.title().replace('_', ' '):15}: {v}\n")
        except Exception as err:
            print(err)

        # ip-api
        try:
            ipapi_url = self.connect(self.ipapi_url).json()
            print(f"\n{CYAN}IP-API Results{RESET}\n{('-' * 50)}")
            with open(self.geo_results, "a") as f:
                f.write(f"\nIP-API Results\n{('-' * 50)}\n")
            for k, v in ipapi_url.items():
                if v:
                    print(f"{k.title():15}: {v}")
                    with open(self.geo_results, "a") as f:
                        f.write(f"{k.title():15}: {v}\n")
        except Exception as err:
            print(err)


def main():
    if len(sys.argv) < 2:
        sys.exit(f"{RED}[ERROR]{RESET} You forgot to include the host address.")
    else:
        host = sys.argv[1]

    # check if valid ip
    try:
        ipaddress.ip_address(host) or ipaddress.ip_network(host)
    except ValueError as err:
        sys.exit(f"{RED}[ERROR]{RESET} {err}")

    worker = Batch_Worker(host)
    worker.process()


if __name__ == "__main__":
    main()
