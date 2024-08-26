# ArisaMatsuda

A discord bot for private server management.

## Configuration

Before hosting this bot directly from this repo, There are few steps need to do, or the bot will not work properly.
such as `channel_id` or `message_id` in `.env`, More detail is documented in [Secrets](#secrets) section

### Directory Structure

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

#### Confidential and Scopes

| **Name**         | **Tend for**        | **Scopes**                 | **Additional Information**   |
| ---------------- | ------------------- | -------------------------- | ---------------------------- |
| communication.py | 2 specific channels | bi-channel_1, bi-channel_2 | Please check the source code |
| emotes.py        | global              |                            |                              |
| goods.py         | global              |                            |                              |
| join.py          | server              | production_server_1        | Please check the source code |
| ping.py          | global              |                            |                              |
| twitterFix.py    | global              |                            |                              |

#### communication.py

a.k.a bi-channel, this is a very special extension, This extension makes bot transfer message between `production_server_1` and `production_server_2` and their specific channels, which is `bi-channel_1` and `bi-channel_2`

#### join.py

This extension is build for server member managements, Member who has the chat permission, may decide to grant the access for selected channels view permission with this command

> [!NOTE]  
> If your deployment does not require this function, make sure to unload `./cogs/communication.py`, and you can remove `bi-channel_1` and `bi-channel_2` from `.env`, and so on for `./cogs/join.py`

## Build

### Requirements

These [requirements](./requirements.txt) are essential. You can install them using the command `pip install -r requirements.txt`.

### Running

#### Self Host

```shell
python3 -B main.py
```

#### pm2

> [!NOTE]  
> The following arguments are examples of using `virtualenv`.

```shell
pm2 start src/main.py --name "arisa" --interpreter "venv/bin/python3" --interpreter-args "-B"
```

## License

Licensed under [MIT](LICENSE).
