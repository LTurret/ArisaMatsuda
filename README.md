# ArisaMatsuda

A discord bot for help domain content embedding.

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

## License

Licensed under [MIT](LICENSE).
