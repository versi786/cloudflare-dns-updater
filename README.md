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
1. If you would like to se the output of the cron jobs you can install `postfix` and take a look at /var/mail/${USER}. It also would be useful to set max mailbox size as described [here](https://www.cyberciti.biz/tips/postfix-mail-server-limit-the-mailbox-size.html). The output of cronjobs is sent as mail to the user who is runnig the command.
