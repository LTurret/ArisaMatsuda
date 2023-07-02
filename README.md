# ArisaMatsuda

A python based program that using `discord-py-interactions` hosting a discord bot for server managements.

## Configuration

### Config folder

Your key such as `bot_token` or `server_scope` should be sort in `core/config` directory, You should create the folder for your own.

### Key manager

The current token and scope **are managed by integrated tool** `core/scopes.py` and `core/secrets.json`, They are kinda sucks and I will rewrite them in future sometime.

You should add your own configs in the directory `core/config` and redefine variables in the two tools mentioned above.

#### Token

```json
{
  "bot_token": YOUR_BOT_TOKEN_HERE
}
```

#### Scopes

```json
{
  "main_server": SERVER_SCOPE,
  "test_server": SERVER_SCOPE,
  "other_server": SERVER_SCOPE
}
```

## Build

### Requirements

```plaintext
[package] [version]
--------------------------------
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
requests==2.30.0
tomli==2.0.1
tqdm==4.65.0
typing_extensions==4.5.0
urllib3==2.0.2
yarl==1.9.2
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

## License

Licensed under [MIT](LICENSE).
