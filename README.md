# ArisaMatsuda

A discord bot for private server management

## Configuration

Before hosting this bot directly from this repo, There are few steps need to do, or the bot will not work properly.
such as `channel_id` or `message_id` in `.env`, More detail is documented in [Secrets](#secrets) section

### Directory structure

```plain
.
├── main.py
├── requirements.txt
├── headers.json
├── .env
├── cogs/
│   ├── module/
│   │   └── ...
│   ├── desperate/
│   │   └── ...
│   ├── communication.py
│   ├── emotes.py
│   ├── goods.py
│   ├── join.py
│   ├── ping.py
│   ├── retweet.py
│   └── twitterFix.py
└── image/goods/
    └── ...
```

### Secrets

Token are accessed with `dotenv.load_dotenv()` and `os.getenv()`

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

### Requirements

Following packages and module are required

#### Packages

```plaintext
aiohttp==3.9.3
aiosignal==1.3.1
attrs==23.2.0
beautifulsoup4==4.12.3
click==8.1.7
discord-py-interactions==5.11.0
discord-typings==0.7.0
emoji==2.10.1
frozenlist==1.4.1
idna==3.6
multidict==6.0.5
mypy-extensions==1.0.0
packaging==23.2
pathspec==0.12.1
pillow==10.2.0
platformdirs==4.2.0
python-dotenv==1.0.1
soupsieve==2.5
tinydb==4.8.0
tomli==2.0.1
typing_extensions==4.9.0
yarl==1.9.4
```

#### Module

Clone [Twitter fetching module](https://github.com/LTurret/Twitter-fetching-module) to `./cogs` and rename folder to `module`

### Running

#### Local

```shell
python3 -B main.py
```

#### pm2

```shell
pm2 start main.py --name "arisa" --interpreter "python3" --interpreter-args "-B"
```

## Todo

- [x] two-path communication method
  - [x] use the right condition to determine which guild
  - [x] attachment handler
  - [x] advanced attachment handler
  - [ ] delete method
  - [ ] edit method
  - [ ] reply method
  - [ ] mention method
  - [ ] support more attachment
  - [ ] maintenance
- [ ] fix all `desperate` functions
  - [x] join
  - [ ] ouen
  - [ ] buttons
  - [x] retweet

## License

Licensed under [MIT](LICENSE)
