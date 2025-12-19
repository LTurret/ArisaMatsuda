use regex::Regex;
use reqwest::{header::USER_AGENT, Client as HttpClient, Error};
use serde_json::{from_str, Value};
use serenity::{
    builder::{
        CreateAllowedMentions, CreateAttachment, CreateEmbed, CreateEmbedAuthor, CreateEmbedFooter,
        CreateMessage,
    },
    model::{
        timestamp::{InvalidTimestamp, Timestamp},
        Color,
    },
    prelude::*,
};

#[derive(Debug)]
struct Author {
    url: String,
    name: String,
    screen_name: String,
    icon_url: String,
}

impl Author {
    fn from_json(json_data: &Value) -> Self {
        fn get_string(v: &Value, k: &str) -> String {
            v[k].as_str().unwrap_or("").to_string()
        }

        Self {
            url: get_string(json_data, "url"),
            name: get_string(json_data, "name"),
            screen_name: get_string(json_data, "screen_name"),
            icon_url: get_string(json_data, "avatar_url"),
        }
    }
}

#[derive(Debug)]
struct Tweet {
    author: Author,
    content: String,
    timestamp: Result<Timestamp, InvalidTimestamp>,
    images: Vec<CreateEmbed>,
    videos: Vec<CreateAttachment>,
    videos_supplementary: String,
}

impl Tweet {
    async fn from_raw(ctx: &Context, raw_api_data: String) -> Self {
        let json_api_data: Value =
            from_str(raw_api_data.as_str()).expect("Expected a valid payload");

        let content: String = json_api_data["tweet"]["text"]
            .as_str()
            .unwrap_or("")
            .to_string();

        let timestamp: Result<Timestamp, InvalidTimestamp> = Timestamp::from_unix_timestamp(
            json_api_data["tweet"]["created_timestamp"]
                .as_i64()
                .unwrap_or(0),
        );

        let images: Vec<CreateEmbed> = json_api_data["tweet"]["media"]["photos"]
            .as_array()
            .unwrap_or(&vec![])
            .iter()
            .map(|obj| {
                CreateEmbed::new().url("https://lturret.xyz").image(
                    Regex::new(r"(?<image_cdn_url>https://pbs.twimg.com/media/.+\.jpg)(\?.+)*")
                        .expect("Expected a valid regex")
                        .captures(&obj["url"].as_str().unwrap_or(""))
                        .expect("Expected a valid haystack")
                        .name("image_cdn_url")
                        .expect("Expected a valid matchig")
                        .as_str(),
                )
            })
            .collect();

        let raw_videos: Vec<String> = json_api_data["tweet"]["media"]["videos"]
            .as_array()
            .unwrap_or(&vec![])
            .iter()
            .filter_map(|arr| arr["url"].as_str())
            .map(|url| url.to_string())
            .map(|url| {
                Regex::new(r"https://video.twimg.com/.+\.mp4")
                    .expect("Expected a valid regex")
                    .captures(&url)
                    .expect("Expected a valid haystack")
                    .get(0)
                    .expect("Expected a valid matchig")
                    .as_str()
                    .to_string()
            })
            .collect();

        let mut videos: Vec<CreateAttachment> = Vec::new();
        for url in raw_videos.iter() {
            videos.push(CreateAttachment::url(&ctx.http, url).await.unwrap());
        }

        let mut videos_supplementary: String = String::new();
        let _ = raw_videos.iter().enumerate().for_each(|(i, url)| {
            videos_supplementary
                .push_str(format!("-# [推文影片連結 {}]({})\n", i + 1, url).as_str())
        });

        Self {
            author: Author::from_json(&json_api_data["tweet"]["author"]),
            content: content,
            timestamp: timestamp,
            images: images,
            videos: videos,
            videos_supplementary: videos_supplementary,
        }
    }
}

async fn fetch_tweet_json(raw_url: String) -> Result<String, Error> {
    let re = Regex::new(r"(?<tweet_endpoint>/.+/status/[0-9]+)(\?.=.+)*")
        .expect("Expected a valid regex pattern");

    let caps = re
        .captures(raw_url.as_str())
        .expect("Expected a valid haystack");

    let api_url = format!(
        "https://api.fxtwitter.com{}",
        caps.name("tweet_endpoint")
            .expect("Expected a valid haystack")
            .as_str()
    );

    let client = HttpClient::new();

    let api_json = client
        .get(api_url)
        .header(
            USER_AGENT,
            "Rust Discord Bot (https://github.com/LTurret/ArisaMatsuda)",
        )
        .send()
        .await?
        .text()
        .await?;

    Ok(api_json)
}

async fn embed_composer(tweet: Tweet) -> CreateMessage {
    let embed: CreateEmbed = CreateEmbed::new()
        .color(Color::new(0x00b0f4))
        .author(
            CreateEmbedAuthor::new(format!(
                "{}(@{})",
                &tweet.author.name, &tweet.author.screen_name
            ))
            .icon_url(&tweet.author.icon_url)
            .url(&tweet.author.url),
        )
        .description(&tweet.content)
        .footer(
            CreateEmbedFooter::new("Twitter (X)")
                .icon_url("https://abs.twimg.com/icons/apple-touch-icon-192x192.png"),
        )
        .url("https://lturret.xyz")
        .timestamp(&tweet.timestamp.expect("Expected a valid Tweet timestamp"));

    let builder: CreateMessage = CreateMessage::new()
        .content(tweet.videos_supplementary)
        .allowed_mentions(CreateAllowedMentions::new().empty_users())
        .embed(embed)
        .add_files(tweet.videos)
        .add_embeds(tweet.images);

    builder
}

pub async fn new_embed(ctx: &Context, raw_endpoint: String) -> CreateMessage {
    let raw_api_data: String = fetch_tweet_json(raw_endpoint)
        .await
        .expect("Expected a valid connection for fetching API data");

    let tweet: Tweet = Tweet::from_raw(&ctx, raw_api_data).await;
    let embed_message: CreateMessage = embed_composer(tweet).await;

    embed_message
}
