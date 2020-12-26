# cloudflare-dns-updater

# Instructions:
1. Create a Cloudflare API token with the permissions that are described [here](https://github.com/AnalogJ/lexicon/blob/985611b18ff8be389c500eb3021aef74ad48bf34/lexicon/providers/cloudflare.py#L19-L25) by Lexicon, using the Cloudflare instruction [here](https://support.cloudflare.com/hc/en-us/articles/200167836-Managing-API-Tokens-and-Keys)
1. Clone [cloudflare-dns-updater](https://github.com/versi786/cloudflare-dns-updater)
1. Create a `.env` file in the in the root directory of the cloned repo and insert a single line with `LEXICON_CLOUDFLARE_AUTH_TOKEN=<Token from Cloudflare>`
1. Install all the dependencies
    ```bash
    python3 -m pipenv install
    ```
1. Test maunally by running the following command:
    ```bash
    python3 -m pipenv run python cloudflare-dns-updater.py --domain example.com --subdomain test
    ```
1. Run the following command, update the domain and subdomain
    ```bash
    echo "cd ${PWD} && python3 -m pipenv run python cloudflare-dns-updater.py --domain example.com --subdomain test"
    ```
1. Run crontab -e and add the following, which will update our DNS every 10 minutes:
    ```crontab
    */10 * * * * <output from previous step>
    ```

1. If you would like to se the output of the cron jobs you can install postfix and take a look at `/var/mail/${USER}`.
1. After some time (about 30 minutes) has passed confirm that the DNS entry has been updated by running `dig test.example.com`
