# ArisaMatsuda

A discord bot for private server management.

## Configuration

Before hosting this bot directly from this repo, There are few steps need to do, or the bot will not work properly.
such as `channel_id` or `message_id` in `.env`, More detail is documented in [Secrets](#secrets) section

### Secrets

Token are accessed with `dotenv.load_dotenv()` and `os.getenv()`.

```env
BOT_TOKEN=
production_server_1=
production_server_2=

# Below are optional

bi-channel_1=
bi-channel_2=
retweet_subscribe_channel=
```

#### Confidential and scopes

| **Name**         | **Tend for**        | **Scopes set**               | **Additional Information**                              |
| ---------------- | ------------------- | ---------------------------- | ------------------------------------------------------- |
| communication.py | 2 specific channels | {bi-channel_1, bi-channel_2} | This extension is special, Please check the source code |
| emotes.py        | global              |                              |                                                         |
| goods.py         | global              |                              |                                                         |
| join.py          | server              | {production_server_1}        | Please check the source code                            |
| ping.py          | global              |                              |                                                         |
| twitterFix.py    | global              |                              |                                                         |

#### communication.py

a.k.a bi-channel, this is a very special extension, This extension makes bot transfer message between `production_server_1` and `production_server_2` and their specific channels, which is `bi-channel_1` and `bi-channel_2`

#### join.py

This extension is build for server member managements, Member who has the chat permission, may decide to grant the access for selected channels view permission with this command

> [!NOTE]  
> If your deployment does not require this function, make sure to unload `./cogs/communication.py`, and you can remove `bi-channel_1` and `bi-channel_2` from `.env`, and so on for `./cogs/join.py`

## Build

### [Requirements](./requirements.txt)

> [!NOTE]  
> You can install packages via `pip install -r requirements.txt`

```plaintext
aiohttp==3.8.4
aiosignal==1.3.1
async-timeout==4.0.2
attrs==23.1.0
beautifulsoup4==4.12.2
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
soupsieve==2.4.1
tomli==2.0.1
tqdm==4.65.0
typing_extensions==4.5.0
urllib3==2.0.2
yarl==1.9.2
```

### Running

#### Local

```shell
python3 -B main.py
```

#### PM2

```shell
pm2 start main.py --name "arisa" --interpreter "python3" --interpreter-args "-B"
```

> [!NOTE]
> The `-B` prevents `__pycache__` being created

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
  - [ ] maintenance
- [ ] fix all `desperate` functions
  - [x] join
  - [ ] ouen
  - [ ] buttons
  - [ ] retweet

## License

Licensed under [MIT](LICENSE).
