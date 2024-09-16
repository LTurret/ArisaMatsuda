# ArisaMatsuda

A discord bot for private server management.

## Configuration

Before hosting this bot directly from this repo, There are few steps need to do, or the bot will not work properly.
such as `channel_id` or `message_id` in `.env`, More detail is documented in [Secrets](#secrets) section

### Directory Structure

```plain
ArisaMatsuda/
├── res/
│   ├── image/
│   │   └── ...
│   ├── database.json (Auto generate)
│   └── headers.json (Self provide)
└── src/
    ├── cogs/
    │   ├── delete.py
    │   ├── join.py
    │   ├── tweet_fix.py
    │   └── tweet_subscribe.py
    ├── module/
    │   └── ...
    └── main.py
```

#### database.json

All database features are hosted by **TinyDB**. The program checks if the database has been created at every startup.

#### headers.json

Please provide a detailed user-agent to facilitate further web access tasks. Here is an example:

```json
{
  "User-Agent": "Mozilla/5.0",
  ...
}

```

## Secrets

Token are accessed with `dotenv.load_dotenv()` and `os.getenv()`.

```env
# Reuire Configuration
BOT_TOKEN=

## Environment Variable
debug_flag=0

# Optional Tokens
GPT_TOKEN=
cdn_url=

## Channel Configuration
bi_channel_1=
bi-channel_2=
retweet_subscribe_channel=
```

### Confidential Scopes

| **Name**             | **Tend for**        | **Scopes**                     | **Additional Information** |
| -------------------- | ------------------- | ------------------------------ | -------------------------- |
| ~~communication.py~~ | 2 specific channels | `bi_channel_1`, `bi_channel_2` | Not implemented for v2.0   |
| ~~emotes.py~~        | global              | None                           | Not implemented for v2.0   |
| ~~goods.py~~         | global              | None                           | Not implemented for v2.0   |
| join.py              | private server      | `production_server_1`          |                            |
| ping.py              | global              | None                           |                            |
| tweet_fix.py         | global              | None                           |                            |
| tweet_subscribe      | global              | `retweet_subscribe_channel`    |                            |

#### communication.py

Also known as the bi-channel extension, this is a unique feature that enables the bot to transfer messages between `production_server_1` and `production_server_2`, specifically between `bi_channel_1` and `bi_channel_2`.

#### join.py

> [!WARNING]
> The roles are statically configured for my server; you will need to modify the source code to match your own roles.

This extension is designed for managing server members. A member with chat permissions can use this command to grant view access to selected channels.

> [!NOTE]  
> If your deployment doesn't require this feature, be sure to unload ./cogs/communication.py. You can also remove `bi_channel_1` and `bi_channel_2` from the `.env` file, as well as make similar changes for `cogs/join.py`.

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
> The following arguments are example of using `virtualenv`:

```shell
pm2 start src/main.py --name "arisa" --interpreter "venv/bin/python3" --interpreter-args "-B"
```

## License

Licensed under [MIT](LICENSE).
