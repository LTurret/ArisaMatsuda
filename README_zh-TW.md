# ArisaMatsuda

[[English](./README.md)｜繁體中文]

私人伺服器管理用 Discord 機器人。

> [!IMPORTANT]
> Python 與 Rust 的建構工作正同時進行開發。

## 設定

在直接從此儲存庫執行機器人之前，需要完成一些必要的步驟，否則機器人將無法正常運行。

### 目錄結構

```plain
ArisaMatsuda/
├── src
│   └── main.rs
├── Cargo.toml
├── LICENSE
├── README.md
└── README_zh-TW.md
```

### 機密資訊與設定

機器人權杖（Token）使用 `dotenv::dotenv.ok()` 和 `std::env::var()` 存取。

`.env` 檔案應包含以下設定：

```env
# 必需的設定
DISCORD_TOKEN="<your_token>"
```

請確保將 plcaeholders 替換為你的實際值。

## 建置

```sh
cargo build --release
```

### 執行

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

## 規劃路線圖

> [!NOTE]
> 某些功能在之前的 Python 版本中被規劃移除，因此不列入以下表中。
> 請參照主分支以獲得更多資訊。

接下來會再 project 中有更詳細的規劃！

| **File**         | **Status** |
|------------------|------------|
| **tweet_fix.py** | 實作中     |
| _emotes.py_      | 尚未實作   |
| _goods.py_       | 尚未實作   |
| _ping.py_        | 尚未實作   |
| fun.py           | 尚未實作   |
| tweet_subscribe  | 尚未實作   |
| ~~delete.py~~    | 已棄用     |
| ~~join.py~~      | 已棄用     |

## 授權

本專案採用 [MIT](LICENSE) 授權。
