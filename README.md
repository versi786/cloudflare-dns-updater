# cloudflare-dns-updater

# Instructions:
1. Clone this repo
1. Run:
    ```
    python3 -m pipenv install
    ```
1. Update `.env` to include `LEXICON_CLOUDFLARE_AUTH_TOKEN`, the api token should be created from instructions [here](https://github.com/AnalogJ/lexicon/blob/master/lexicon/providers/cloudflare.py)
1. Run the following command, update items between angle backets
    ```
    echo "cd ${PWD} && python3 -m pipenv run python cloudflare-dns-updater.py --domain example.com --subdomain test"

    ```
1.  Run `crontab -e` and add the following, which will run every 10 minutes:
    ```
    */10 * * * * <command from previous step>

    ```
