use crate::commands::{
    instagram::InstagramBuilder, threads::ThreadBuilder, twitter::TweetBuilder,
};
use async_trait::async_trait;
use regex::Captures;
use reqwest::Client as HttpClient;
use serde_json::json;
use serenity::{
    builder::CreateMessage, http::Typing, model::channel::Message, prelude::*,
};
use std::env;
use tokio::time::{Duration, sleep};

pub struct Embed;

#[async_trait]
pub trait ContentBuilder: Send + Sync {
    async fn embed_message(
        &self,
        endpoint: &str,
        ctx: &Context,
    ) -> CreateMessage;
}

impl Embed {
    async fn suppress_original_embed(msg: &Message) -> () {
        let token = env::var("DISCORD_TOKEN")
            .expect("Expected a token in the environment");
        sleep(Duration::from_millis(250)).await;

        let url: String = format!(
            "https://discord.com/api/v9/channels/{}/messages/{}",
            &msg.channel_id, &msg.id
        );

        let client: HttpClient = HttpClient::new();
        client
            .patch(&url)
            .header("accept", "*/*")
            .header("authorization", format!("Bot {}", token))
            .header("content-type", "application/json")
            .body(
                json!({
                    "flags": 4
                })
                .to_string(),
            )
            .send()
            .await
            .ok();
    }

    pub async fn process_url(
        ctx: &Context,
        msg: &Message,
        caps: &Captures<'_>,
    ) -> () {
        let typing = Typing::start(ctx.http.clone(), msg.channel_id);

        let embed_message = Self::new_embed(ctx, caps).await;
        if let Err(why) =
            msg.channel_id.send_message(&ctx.http, embed_message).await
        {
            eprintln!("Error sending message: {why:?}");
        }

        Self::suppress_original_embed(msg).await;
        typing.stop();
    }

    pub async fn new_embed(
        ctx: &Context,
        caps: &Captures<'_>,
    ) -> CreateMessage {
        let endpoint: &str =
            caps.name("endpoint").expect("Expected a valid haystack").as_str();

        // Regex Pattern: (http|https)://(?<domain>.+)\.com(?<endpoint>(/.+)*)
        let fetcher: Box<dyn ContentBuilder + Send + Sync> = match caps
            .name("domain")
            .expect("Expected a valid haystack")
            .as_str()
        {
            // ContentFetcher selector by domain
            "x" | "twitter" => Box::new(TweetBuilder),
            "threads" => Box::new(ThreadBuilder),
            "instagram" => Box::new(InstagramBuilder),
            _ => unimplemented!(),
        };

        let embed_message: CreateMessage =
            fetcher.embed_message(endpoint, ctx).await;

        embed_message
    }
}
