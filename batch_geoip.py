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

# Console Colors
init()
CYAN = Fore.CYAN
RESET = Fore.RESET


@contextmanager
def write_to_file(file_path: Path) -> Generator[Callable[[str], int], None, None]:
    """Context manager for writing to file.

    Yields:
        [type]: [description]
    """
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
        """Takes a URL, connects to it, and then writes the results to a file."""
        # tools.keycdn.com
        try:
            self.keycdn()
        except Exception as err:
            print(err)

        # ip-api
        try:
            self.ipapi()
        except Exception as err:
            print(err)

    def keycdn(self: "BatchWorker") -> None:
        """Connect to tools.keycdn.com and write the results to a file."""
        headers = {"User-Agent": f"keycdn-tools:https://{self.host}"}
        kc_url = requests.get(self.kc_url, headers=headers, timeout=5).json()
        results = [f"\nKeyCDN Results\n{('-' * 50)}\n"]
        print(f"\n{CYAN}KeyCDN Results{RESET}\n{('-' * 50)}")

        for _key, _value in kc_url["data"]["geo"].items():
            if _value:
                formatted_line = f"{_key.title().replace('_', ' '):15}: {_value}\n"
                results.append(formatted_line)
                print(formatted_line.strip())

        with write_to_file(self.geo_results) as writer:
            writer("".join(results))

    def ipapi(self: "BatchWorker") -> None:
        """Connect to ip-api.com and write the results to a file."""
        ipapi_url = self.connect(self.ipapi_url).json()
        results = [f"\nIP-API Results\n{('-' * 50)}\n"]
        print(f"\n{CYAN}IP-API Results{RESET}\n{('-' * 50)}")

        for _key, _value in ipapi_url.items():
            if _value:
                formatted_line = f"{_key.title():15}: {_value}\n"
                results.append(formatted_line)
                print(formatted_line.strip())

        with write_to_file(self.geo_results) as writer:
            writer("".join(results))


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
