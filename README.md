# ArisaMatsuda

A discord bot for private server management.

## Configuration

> [!IMPORTANT]  
> Before hosting this bot directly from this repo, you have to change some secret and variable.  
> such as `channel_id` or `message_id` in `.env`  
> More detail will describe in [Secrets](#secrets) section

### Secrets

> [!NOTE]  
> **The token is accessed with `dotenv.load_dotenv()` and `os.getenv()`, make sure you have prepare the following confidentials in `.env`.**

This section documented some information about how and where to use your confidential.

> [!IMPORTANT]  
> The following table is all **REQUIRED** and make sure you place them well.

```env
BOT_TOKEN=
production_server_1=
production_server_2=
bi-channel_1=
bi-channel_2=
```

#### Confidential and scopes

> [!NOTE]  
> I use `.env` to store my `server_id` and `channel_id`, and this table will tell where this bot use these scopes.

| **Extension name** | **Use range**                | **Scopes set**                             | **Additional**                                          |
| ------------------ | ---------------------------- | ------------------------------------------ | ------------------------------------------------------- |
| communication.py   | 2 servers, specific channels | {production_server_1, production_server_2} | this extension is special, please check the source code |
| emotes.py          | global                       |                                            |                                                         |
| goods.py           | global                       |                                            |                                                         |
| join.py            | not global                   | {production_server_1}                      |                                                         |
| ping.py            | global                       |                                            |                                                         |
| twitterFix.py      | global                       |                                            |                                                         |

#### bi-channels

bi-channel is a very special extension, This extension makes bot transfer message between `production_server_1` and `production_server_2` and their specific channels, which is `bi-channel_1` and `bi-channel_2`

> [!NOTE]  
> If your deployment does not require this function, make sure to unload `./cogs/communication.py`, and you can remove `bi-channel_1` and `bi-channel_2` from `.env`

## Build

### [Requirements](./requirements.txt)

> [!NOTE]  
> You can install packages via `pip install -r requirements.txt`

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
Pillow==10.0.0
python-dotenv==1.0.0
requests==2.30.0
tomli==2.0.1
tqdm==4.65.0
typing_extensions==4.5.0
urllib3==2.0.2
yarl==1.9.2
```

### Running

> [!NOTE]
> The `-B` prevents `__pycache__` being created

```shell
python3 -B main.py
```

## Todo

- [x] two-path communication method
  - [x] use the right condition to determine which guild
  - [x] attachment handler
  - [x] advanced attachment handler
  - [ ] reply method
  - [ ] delete method
  - [ ] edit method
  - [ ] mention method
  - [ ] support more attachment
- [x] redesign scope integration system
  > [!NOTE]  
  > This is a small rewrite, consider using a reliable method to future maintenance
- [ ] fix all `desperate` functions
  - [x] join
  - [ ] ouen
  - [ ] buttons
- [ ] zenMode - Enabling will remove all channel to make less notification, disable it can put all roles back.
- [x] Twitter url fix automations.
  - [x] resent with vx prefix.
  - [x] fetch all information in the tweet then resend.
  - [x] rework a new one

## License

Licensed under [MIT](LICENSE).
