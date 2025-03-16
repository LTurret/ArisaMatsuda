# ArisaMatsuda

[[English](./README.md)｜繁體中文]

私人伺服器管理用 Discord 機器人。

## 設定

在直接從此儲存庫執行機器人之前，需要完成一些必要的步驟，否則機器人將無法正常運行。

例如 `.env` 檔案中的 `channel_id` 或 `message_id`，詳細資訊請參閱 [Secrets](#機密資訊與設定) 部分。

### 目錄結構

```plain
ArisaMatsuda/
├── res/
│   ├── image/
│   │   └── ...
│   ├── video/
│   │   └── ...
│   ├── database.json (程式自動產生)
│   ├── headers.json (需自行提供)
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

所有資料庫功能由 **TinyDB** 提供。程式在每次啟動時都會檢查資料庫是否已建立。

#### headers.json

請提供詳細的 `User-Agent` 以便進行後續的網路存取作業。範例如下：

```json
{
  "User-Agent": "Mozilla/5.0",
  ...
}
```

#### keywords.json

負責關鍵字字串配對，並將相應的檔案發送至頻道。

## 機密資訊與設定

機器人權杖（Token）使用 `dotenv.load_dotenv()` 和 `os.getenv()` 存取。

`.env` 檔案應包含以下設定：

```env
# 必需的設定
BOT_TOKEN=<your_token>

# 可選的設定
cdn_urls=<url1>, <url2>, ..., <urls>

## 頻道設定
retweet_subscribe_channel=<channel_id>
```

請確保將佔位替換為你的實際值。

### 機密範圍

| **檔案**            | **範圍**             | **頻道**                    | **額外資訊**                                               |
|----------------------|---------------------|-----------------------------|------------------------------------------------------------|
| _emotes.py_         | 全域                | 無                          | 開發中                                                     |
| _goods.py_          | 全域                | 無                          | 開發中                                                     |
| _join.py_           | 私人伺服器          | `production_server_1`       | 開發中                                                     |
| ~~communication.py~~| 兩個特定頻道        | 無                          | **已棄用**                                                 |
| ~~ping.py~~         | 全域                | 無                          | 尚未實作                                                   |
| delete.py           | 全域                | 無                          |                                                            |
| fun.py              | 全域                | 無                          | 可在 [`src/config.toml`](src/config.toml) 中停用此功能     |
| tweet_fix.py        | 全域                | 無                          |                                                            |
| tweet_subscribe     | 全域                | `retweet_subscribe_channel` | 可在 [`src/config.toml`](src/config.toml) 中停用此功能     |

### 組態

使用者可在 [`src/config.toml`](src/config.toml) 進行多項設定，例如啟用／停用除錯模式或某些功能。

#### communication.py

> [!IMPORTANT]
> 此功能已棄用。

也稱為雙頻道延伸功能，此功能允許機器人在 `production_server_1` 和 `production_server_2` 之間傳遞訊息，特定於 `bi_channel_1` 和 `bi_channel_2` 之間。

#### join.py

> [!WARNING]
> 身分組為靜態設定且目前為禁用狀態。你需要修改原始碼來開啟功能和對應身分組。

此延伸模組用於管理伺服器成員。具有聊天權限的成員可以使用此指令來授予選定頻道的瀏覽權限。

## 建置

### 需求

這些[需求](./requirements.txt)是必要的。你可以使用以下指令安裝：

```shell
pip install -r requirements.txt
```

### 執行

#### 除錯

`launch.json` 設定：

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

#### 自行託管

```shell
python3 -B src/main.py
```

#### 正式環境

使用 npm/pm2 託管機器人：

> [!NOTE]  
> 以下範例使用 `virtualenv`：

```shell
pm2 start src/main.py --name "arisa" --interpreter "venv/bin/python3" --interpreter-args "-B" --update-env
```

## 授權

本專案採用 [MIT](LICENSE) 授權。
