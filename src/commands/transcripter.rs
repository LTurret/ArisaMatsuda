use regex::{Captures, Regex};
use reqwest::Client as HttpClient;
use serde_json::json;
use serenity::{builder::CreateMessage, model::channel::Message, prelude::*};
use std::env;
use tokio::time::{sleep, Duration};

use crate::commands::embed::new_embed;

async fn twitter(ctx: &Context, caps: &Captures<'_>) -> CreateMessage {
    let embed_message = new_embed(
        &ctx,
        caps.name("endpoint")
            .expect("Expacted a valid haystack")
            .as_str()
            .to_string(),
    )
    .await;

    embed_message
}

async fn remove_old_embed(msg: &Message) -> () {
    let token = env::var("DISCORD_TOKEN").expect("Expected a token in the environment");
    sleep(Duration::from_millis(250)).await;

    let url: String = format!(
        "https://discord.com/api/v9/channels/{}/messages/{}",
        msg.channel_id, msg.id
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

pub async fn transcripter_factory(ctx: Context, msg: Message) -> () {
    let typing = Typing::start(ctx.http.clone(), msg.channel_id);

    let re: Regex = Regex::new(r"(http|https)://(?<domain>.+)\.com(?<endpoint>(/.+)*)")
        .expect("Regex syntax invalid");

    let caps: Captures = re
        .captures(&msg.content)
        .expect("Expected a valid haystack");

    let embed_message: CreateMessage = match caps
        .name("domain")
        .expect("Expected domain in haystack")
        .as_str()
    {
        "x" | "twitter" => twitter(&ctx, &caps).await,
        _ => twitter(&ctx, &caps).await,
    };

    if let Err(why) = msg.channel_id.send_message(ctx.http, embed_message).await {
        println!("Error sending message: {why:?}");
    }

    let _ = remove_old_embed(&msg).await;
    typing.stop();
}
