use crate::commands::{
    author::Author,
    embed::{ContentFetcher, Embed},
};
use async_trait::async_trait;
use regex::{Captures, Regex};
use reqwest::{header::USER_AGENT, Client as HttpClient};
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
pub struct Tweet {
    pub author: Author,
    pub content: String,
    pub timestamp: Result<Timestamp, InvalidTimestamp>,
    pub images: Vec<CreateEmbed>,
    pub videos: Vec<CreateAttachment>,
    pub videos_supplementary: String,
}

impl Tweet {
    async fn from_raw_api(ctx: &Context, raw_api_data: String) -> Self {
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
            match CreateAttachment::url(&ctx.http, url).await {
                Ok(attachment) => videos.push(attachment),
                Err(err) => {
                    eprintln!("Entity too large, reason: {}", err)
                }
            }
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

    async fn to_embed(self) -> CreateMessage {
        let embed: CreateEmbed = CreateEmbed::new()
            .color(Color::new(0x00b0f4))
            .author(
                CreateEmbedAuthor::new(format!(
                    "{}(@{})",
                    self.author.name, self.author.screen_name
                ))
                .icon_url(self.author.icon_url)
                .url(self.author.url),
            )
            .description(self.content)
            .footer(
                CreateEmbedFooter::new("Twitter (X)")
                    .icon_url("https://abs.twimg.com/icons/apple-touch-icon-192x192.png"),
            )
            .url("https://lturret.xyz")
            .timestamp(
                self.timestamp
                    .as_ref()
                    .expect("Expected a valid Tweet timestamp"),
            );

        let builder: CreateMessage = CreateMessage::new()
            .content(&self.videos_supplementary)
            .allowed_mentions(CreateAllowedMentions::new().empty_users())
            .embed(embed)
            .add_files(self.videos)
            .add_embeds(self.images);

        builder
    }
}

pub struct TweetFetcher;

#[async_trait]
impl ContentFetcher for TweetFetcher {
    async fn embed_message(&self, endpoint: &str, ctx: &Context) -> CreateMessage {
        let caps: Captures<'_> = Regex::new(r"(?<tweet_endpoint>/.+/status/[0-9]+)(\?.=.+)*")
            .expect("Expected a valid regex pattern")
            .captures(endpoint)
            .expect("Expected a valid haystack");

        let api_url: String = format!(
            "https://api.fxtwitter.com{}",
            caps.name("tweet_endpoint")
                .expect("Expected a valid haystack")
                .as_str()
        );

        let client: HttpClient = HttpClient::new();
        let response_result = client
            .get(api_url)
            .header(
                USER_AGENT,
                "Rust Discord Bot (https://github.com/LTurret/ArisaMatsuda)",
            )
            .send()
            .await;

        let response = match response_result {
            Ok(resp) => resp,
            Err(err) => {
                eprintln!("{}", err);
                return CreateMessage::new().content("Failed to fetch tweet");
            }
        };

        let api_json = response.text().await.expect("Failed to read response text");
        let tweet: Tweet = Tweet::from_raw_api(&ctx, api_json).await;
        let embed_message: CreateMessage = tweet.to_embed().await;
        embed_message
    }
}

pub async fn handler(ctx: &Context, caps: &Captures<'_>) -> CreateMessage {
    let embed_message = Embed.new_embed(ctx, caps).await;
    embed_message
}
