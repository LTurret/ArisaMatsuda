# ArisaMatsuda

[English｜[繁體中文](./README_zh-TW.md)]

A discord bot for private server management.

> [!IMPORTANT]
> Both Python and Rust build are development simultaneously.

## Configuration

Before hosting this bot directly from this repo, There are few steps need to do, or the bot will not work properly.

### Directory Structure

```plain
ArisaMatsuda/
├── src
│   └── main.rs
├── Cargo.toml
├── LICENSE
├── README.md
└── README_zh-TW.md
```

### Secrets

Token are accessed with `dotenv::dotenv.ok()` and `std::env::var()`.

The `.env` file should contain the following configurations:

```env
# Required Configuration
DISCORD_TOKEN="<your_token>"
```

Replace the placeholders with your actual values.

## Build

```sh
cargo build --release
```

### Running

- npm/pm2:

    ```sh
    pm2 start target/release/arisa_rust --name "arisa" --update-env
    ```

- Background job:

    ```sh
    ./target/release/arisa_rust &
    ```

- Docker:

    ```sh
    wip
    ```

## Roadmap

> [!NOTE]
> Some of features are removed from the list since the last Python build.
> Please refer to the main branch for more information.

There would be more tracks in the project tab!

| **File**         | **Status**       |
|------------------|------------------|
| **tweet_fix.py** | Work in Progress |
| _emotes.py_      | Not implemented  |
| _goods.py_       | Not implemented  |
| _ping.py_        | Not implemented  |
| fun.py           | Not implemented  |
| tweet_subscribe  | Not implemented  |
| ~~delete.py~~    | Despreated       |
| ~~join.py~~      | Despreated       |

## License

Licensed under [MIT](LICENSE).
