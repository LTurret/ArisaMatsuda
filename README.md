# ArisaMatsuda

[English｜[繁體中文](./README_zh-TW.md)]

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
│   ├── video/
│   │   └── ...
│   ├── database.json (Generated by program)
│   ├── headers.json (Provide by yourself)
│   └── keywords.json
└── src/
    ├── cogs/
    │   ├── delete.py
    │   ├── fun.py
    │   ├── join.py
    │   ├── tweet_parser.py
    │   └── tweet_subscribe.py
    ├── module/
    │   └── ...
    ├── main.py
    └── mapping.py
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

#### keywords.json

Handles the keyword string matching and sends corresponding files to the channel.

## Secrets and Configurations

Token are accessed with `dotenv.load_dotenv()` and `os.getenv()`.

The `.env` file should contain the following configurations:

```env
# Required Configuration
BOT_TOKEN=<your_token>

# Optional Tokens
cdn_urls=<url1>, <url2>, ..., <urls>

## Channel Configuration
retweet_subscribe_channel=<channel_id>
```

Make sure to replace the placeholders with your actual values.

### Confidential Scopes

| **File**             | **Scope**           | **Channel**                 | **Additional Information**                                   |
|----------------------|---------------------|-----------------------------|--------------------------------------------------------------|
| _emotes.py_          | global              | None                        | Work in progress                                             |
| _goods.py_           | global              | None                        | Work in progress                                             |
| _join.py_            | private server      | `production_server_1`       | Work in progress                                             |
| ~~communication.py~~ | 2 specific channels | None                        | **Desperate**                                                |
| ~~ping.py~~          | global              | None                        | Not implemented                                              |
| delete.py            | global              | None                        |                                                              |
| fun.py               | global              | None                        | Disable this feature in [`src/config.toml`](src/config.toml) |
| tweet_fix.py         | global              | None                        |                                                              |
| tweet_subscribe      | global              | `retweet_subscribe_channel` | Disable this feature in [`src/config.toml`](src/config.toml) |

### Configurations

There are several user-side configurations available in [`src/config.toml`](src/config.toml) that control debugging mode and enable or disable features.

#### communication.py

> [!IMPORTANT]
> This feature has been discontinued.

Also known as the bi-channel extension, this is a unique feature that enables the bot to transfer messages between `production_server_1` and `production_server_2`, specifically between `bi_channel_1` and `bi_channel_2`.

#### join.py

> [!WARNING]
> The roles are statically configured for my server; you will need to modify the source code to enable this feature and match your own roles.

This extension is designed for managing server members. A member with chat permissions can use this command to grant view access to selected channels.

## Build

### Requirements

These [requirements](./requirements.txt) are essential. You can install them using the command `pip install -r requirements.txt`.

### Running

#### Debugging

launch.json:

```json
"launch": {
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}"
        }
    ]
}
```

#### Self Host

```shell
python3 -B src/main.py
```

#### Production

Hosting the bot with npm/pm2:

> [!NOTE]  
> The following arguments are examples of using `virtualenv`:

```shell
pm2 start src/main.py --name "arisa" --interpreter "venv/bin/python3" --interpreter-args "-B" --update-env
```

## License

Licensed under [MIT](LICENSE).
