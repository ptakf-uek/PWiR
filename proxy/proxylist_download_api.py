import argparse
import json
import logging
from time import sleep

import requests
from utils.country_dict import country_dict


class ProxylistDownloadApi:
    def __init__(self):
        # Configure command line arguments.
        parser = argparse.ArgumentParser(
            description="Download a list of proxy from proxy-list.download using the official API."
        )
        parser.add_argument(
            "-q",
            "--quiet",
            dest="quiet",
            help="do not log debug info",
            action="store_true",
        )
        parser.add_argument(
            "-O", "--output", dest="output", help="save output to this file"
        )
        self.args = parser.parse_args()

        # Configure logging.
        self.logger = logging.getLogger("proxylist_download_api")
        self.logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(module)s] %(levelname)s: %(message)s")
        )
        self.logger.addHandler(console_handler)

        if self.args.quiet:
            console_handler.setLevel(logging.INFO)

    base_api_url = "https://www.proxy-list.download/api/v1/get?type=http"

    def download(self):
        self.logger.debug("Starting download from API...")
        proxy_list = []

        for country_code in country_dict:
            self.logger.debug("Waiting before request...")
            sleep(
                5
            )  # Wait 5 seconds before each request to avoid overloading the server.

            single_country_api_url = self.base_api_url + f"&country={country_code}"
            self.logger.debug(
                f"Sending an HTTP GET request to {single_country_api_url}..."
            )
            response = requests.get(single_country_api_url)

            if response.status_code == requests.codes.ok:
                self.logger.debug("Request completed successfully!")
                api_response = response.text

                if api_response != "":
                    self.logger.debug("Response is not empty!")
                    for line in api_response.splitlines():
                        proxy_dict = {
                            "ip_address": line.strip().split(":")[0],
                            "port": line.strip().split(":")[1],
                            "country": country_dict[country_code],
                        }

                        self.logger.debug(
                            f"Downloaded from <{response.status_code} {single_country_api_url}>\n{proxy_dict}"
                        )

                        proxy_list.append(proxy_dict)
                else:
                    self.logger.debug("Response is empty!")

            else:
                self.logger.debug(
                    f"Error on connection <{response.status_code} {single_country_api_url}>"
                )

                if response.status_code == "429":
                    sleep(25)

        if self.args.output:
            with open(f"{self.args.output}", "w", encoding="utf-8") as file:
                self.logger.debug("Saving output to file...")
                json.dump(proxy_list, file, indent=2)
                self.logger.debug("Output saved to file!")


if __name__ == "__main__":
    ProxylistDownloadApi().download()
