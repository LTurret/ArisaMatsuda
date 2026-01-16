use crate::commands::{instagram, twitter};
use regex::{Captures, Regex};
use reqwest::Client as HttpClient;
use serde_json::json;
use serenity::{builder::CreateMessage, http::Typing, model::channel::Message, prelude::*};
use std::env;
use tokio::time::{sleep, Duration};

pub struct Patcher {
    ctx: Context,
    msg: Message,
}

impl Patcher {
    pub fn new(ctx: Context, msg: Message) -> Self {
        Self { ctx: ctx, msg: msg }
    }

    pub async fn parse(&self) -> () {
        let typing = Typing::start(self.ctx.http.clone(), self.msg.channel_id);

        let caps: Captures =
            Regex::new(r"(http|https)://(www\.)*(?<domain>.+)\.(cc|com)(?<endpoint>(/.+)*)")
                .expect("Regex syntax inv`alid")
                .captures(&self.msg.content)
                .expect("Expected a valid haystack");

        // Decide domain
        let embed_message: CreateMessage = match caps
            .name("domain")
            .expect("Expected domain in haystack")
            .as_str()
        {
            "x" | "twitter" => twitter::handler(&self.ctx, &caps).await,
            "instagram" => instagram::handler(&self.ctx, &caps).await,
            "facebook" => unimplemented!(),
            "threads" => unimplemented!(),
            "youtube" => unimplemented!(),
            "ptt" => unimplemented!(),
            _ => unimplemented!(),
        };

        // Sending embed message
        if let Err(why) = self
            .msg
            .channel_id
            .send_message(&self.ctx.http, embed_message)
            .await
        {
            eprintln!("Error sending message: {why:?}");
        }

        let _ = self.remove_old_embed().await;
        typing.stop();
    }

    async fn remove_old_embed(&self) -> () {
        let token = env::var("DISCORD_TOKEN").expect("Expected a token in the environment");
        sleep(Duration::from_millis(250)).await;

        let url: String = format!(
            "https://discord.com/api/v9/channels/{}/messages/{}",
            &self.msg.channel_id, &self.msg.id
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
}
