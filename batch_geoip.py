"""Batch GeoIP Lookup."""

import ipaddress
import sys
from collections.abc import Callable
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import requests
from colorama import Fore
from colorama import init

# console colors and formatting
init()
CYAN = Fore.CYAN
RESET = Fore.RESET


@contextmanager
def write_to_file(file_path: Path) -> Generator[Callable[[str], int], None, None]:
    """Context manager for writing to file."""
    with file_path.open("a", encoding="utf-8") as file:
        yield file.write


class BatchWorker:
    """Worker Functions."""

    def __init__(self: "BatchWorker", host: str) -> None:
        """Initialize the BatchWorker class."""
        self.host = host
        self.parent = Path(__file__).resolve().parent
        self.geo_results = self.parent / "geo_results.txt"
        self.kc_url = f"https://tools.keycdn.com/geo.json?host={self.host}"
        self.ipapi_url = f"http://ip-api.com/json/{self.host}"

    def connect(self: "BatchWorker", url: str) -> requests.models.Response:
        """Connect to a URL and return the response."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/65.0.3325.162 Safari/537.36",
        }
        return requests.get(url, headers=headers, timeout=5)

    def process(self: "BatchWorker") -> None:
        """Takes URLs, connects to them, and then writes the combined results to a file."""
        combined_results = {}

        # map similar keys from both sources to a single key
        key_mappings = {
            "country_name": "country",
            "country_code": "countrycode",
            "region_name": "regionname",
            "region_code": "region",
            "postal_code": "zip",
            "latitude": "lat",
            "longitude": "lon",
            "asn": "as",
            "isp": "isp",  # Separate 'isp' and 'org'
            "org": "org",
            "host": "ip",
            "query": "ip",
        }

        def add_to_combined_results(data: dict) -> None:
            for k, v in data.items():
                key = key_mappings.get(k.lower(), k.lower())
                if key not in combined_results or combined_results[key] != v:
                    combined_results[key] = v

        # tools.keycdn.com
        try:
            kc_data = self.keycdn()
            add_to_combined_results(kc_data)
        except Exception as err:
            print(err)

        # ip-api
        try:
            ipapi_data = self.ipapi()
            add_to_combined_results(ipapi_data)
        except Exception as err:
            print(err)

        # combine and Print Results
        self.print_and_save_results(combined_results)

    def keycdn(self: "BatchWorker") -> dict:
        """Connect to tools.keycdn.com and return the results."""
        headers = {"User-Agent": f"keycdn-tools:https://{self.host}"}
        kc_url = requests.get(self.kc_url, headers=headers, timeout=5).json()
        return kc_url["data"]["geo"]

    def ipapi(self: "BatchWorker") -> dict:
        """Connect to ip-api.com and return the results."""
        return self.connect(self.ipapi_url).json()

    def print_and_save_results(self: "BatchWorker", results: dict) -> None:
        """Print and save the combined results."""
        # if 'Isp' and 'Org' are the same, remove 'Org'
        if results["org"] == results["isp"]:
            results.pop("org", None)

        # define the order of the keys to be printed
        ordered_keys = [
            "ip",
            "org",
            "as",
            "isp",
            "rdns",
            "country",
            "countrycode",
            "regionname",
            "region",
            "city",
            "zip",
            "metro_code",
            "continent_name",
            "continent_code",
            "lat",
            "lon",
            "timezone",
            "datetime",
            # "status",
        ]

        # correcting keys to match the display format
        display_keys = {
            "metro_code": "Metro Code",
            "continent_name": "Continent Name",
            "continent_code": "Continent Code",
        }

        formatted_results = [f"\nCombined Results\n{('-' * 50)}\n"]
        print(f"\n{CYAN}Combined Results{RESET}\n{('-' * 50)}")

        for key in ordered_keys:
            display_key = display_keys.get(key, key.title().replace("_", " "))
            if key in results and results[key]:
                formatted_line = f"{display_key:15}: {results[key]}\n"
                formatted_results.append(formatted_line)
                print(formatted_line.strip())

        with write_to_file(self.geo_results) as writer:
            writer("".join(formatted_results))


def main() -> None:
    """Main function."""
    if len(sys.argv) < 2:
        sys.exit(f"{Fore.RED}[ERROR]{RESET} You forgot to include the host address.")
    else:
        host = sys.argv[1]

    # check if valid ip or network
    try:
        ip = ipaddress.ip_address(host) or ipaddress.ip_network(host)
    except ValueError as err:
        sys.exit(f"{Fore.RED}[ERROR]{RESET} {err}")

    worker = BatchWorker(str(ip))
    worker.process()


if __name__ == "__main__":
    main()
