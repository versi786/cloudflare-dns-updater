from typing import Optional
from requests import get
from lexicon.client import Client
from lexicon.config import ConfigResolver
import logging
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig()
logger = logging.getLogger("cloudflare-dns-updater")
logger.setLevel(logging.INFO)


CACHE_IP_FILE = os.path.dirname(os.path.abspath(__file__)) + "/dns_cache"


def cache_file(subdomain, domain):
    return CACHE_IP_FILE + ".{}.{}".format(subdomain, domain)


def get_cached_ip(subdomain, domain) -> Optional[str]:
    try:
        with open(cache_file(subdomain, domain)) as f:
            cached_ip = f.read()
            logger.debug("cached_ip: {}".format(cached_ip))
            return cached_ip
    except IOError:
        return None


def get_current_ip() -> Optional[str]:
    current_ip = get("https://api.ipify.org").text
    logger.debug("current_ip: {}".format(current_ip))
    return current_ip


def update_ip(subdomain: str, domain: str, current_ip: str):

    assert os.getenv("LEXICON_CLOUDFLARE_AUTH_TOKEN")

    # udpate file cache
    with open(cache_file(subdomain, domain), "w") as f:
        f.write(current_ip)
        logger.debug("updated cached_ip: {}".format(current_ip))

    # update cloudflare
    logger.debug(
        "Updated {}.{} in cloudflare to {}".format(subdomain, domain, current_ip)
    )
    action = {
        "provider_name": "cloudflare",
        "action": "create",
        "domain": "{}".format(domain),
        "type": "A",
        "name": "{}".format(subdomain),
        "content": "{}".format(current_ip),
        "ttl": 1,
    }
    config = ConfigResolver().with_env().with_dict(action)
    Client(config).execute()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Set subdomain and domain in cloudflare to point to "
            "current ip address, eg. test.example.com. "
            "Requires a environment variable or `.env` "
            "with LEXICON_CLOUDFLARE_AUTH_TOKEN "
        )
    )
    parser.add_argument(
        "--domain",
        help="domain to set ip address for, eg. example.com",
    )
    parser.add_argument(
        "--subdomain",
        help="subdomain to set ip address for, eg. test",
    )

    args = parser.parse_args()

    cached_ip = get_cached_ip(args.subdomain, args.domain)
    current_ip = get_current_ip()

    if cached_ip != current_ip:
        update_ip(args.subdomain, args.domain, current_ip)
        logger.info("Updated ip {}".format(current_ip))
    else:
        logger.info("Not updating ip is the same: {}".format(current_ip))


if __name__ == "__main__":
    main()
