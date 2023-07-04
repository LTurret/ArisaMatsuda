# ArisaMatsuda

A python based program that using `discord-py-interactions` hosting a discord bot for server managements.

## Configuration

Before hosting this bot directly from clone this repo, you have to change all the secret variable such as `channel_id` or `message_id` in [`./cogs`](./cogs/) and secrets in `.env`

### Secrets

The token is accessed with `dotenv.load_dotenv()` and `os.getenv()`, make sure you have prepare the following information in `.env`.

Here is a example where you should place your confidentials:

```env
BOT_TOKEN=
Production_anna=
Production_arisa=
Testing=
```

## Build

### [Requirements](./requirements.txt)

You can install packages with `pip install -r requirements.txt`

```plaintext
aiohttp==3.8.4
aiosignal==1.3.1
async-timeout==4.0.2
attrs==23.1.0
certifi==2023.5.7
charset-normalizer==3.1.0
discord-py-interactions==5.5.1
discord-typings==0.5.1
emoji==2.2.0
frozenlist==1.3.3
idna==3.4
multidict==6.0.4
python-dotenv==1.0.0
requests==2.30.0
tomli==2.0.1
tqdm==4.65.0
typing_extensions==4.5.0
urllib3==2.0.2
yarl==1.9.2
```

### Running

The `-B` prevents `__pycache__` being created

```shell
python3 -B main.py
```

## Todo

- [x] two-path communication method
  - [x] use the right condition to determine which guild
  - [x] attachment (JPG only)
  - [ ] reply method
  - [ ] delete method
  - [ ] edit method
  - [ ] mention method
  - [ ] support more attachment
- [x] redesign scope integration system
  > This is a small rewrite, consider using a reliable method to future maintenance
- [ ] fix all `desperate` functions
  - [x] join
  - [ ] ouen
  - [ ] buttons
- [ ] `zenMode` - Enabling will remove all channel to make less notification, disable it can put all roles back.
- [ ] Twitter url fix automations.
  - [x] resent with vx prefix.
  - [ ] fetch all information in the tweet then resent.

## License

Licensed under [MIT](LICENSE).
