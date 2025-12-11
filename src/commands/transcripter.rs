use regex::{Captures, Regex};
use reqwest::Client as HttpClient;
use serde_json::json;
use std::env;
use tokio::time::{sleep, Duration};

use serenity::model::channel::Message;
use serenity::prelude::*;

fn twitter(caps: &Captures) -> String {
    let re = Regex::new(r"/(?<username>.+)/status/(?<snowflake>[0-9]+)(\?(s|t)=.+)*")
        .expect("Passed a invalid haystack");

    let properties: Captures = re
        .captures(
            caps.name("endpoint")
                .expect("Passed a invalid haystack")
                .as_str(),
        )
        .expect("Haystack not matching");

    let second_slice: Vec<String> = ["username", "snowflake"]
        .iter()
        .map(|p| {
            properties
                .name(p)
                .expect("One of the tag are not matching")
                .as_str()
                .to_string()
        })
        .collect();

    let after_message: String = format!(
        "https://fxtwitter.com/{}/status/{}",
        second_slice[0], second_slice[1]
    );

    after_message
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
    let re: Regex = Regex::new(r"(http|https)://(?<domain>.+)\.com(?<endpoint>(/.+)*)")
        .expect("Regex syntax invalid");
    let caps: Captures = re.captures(&msg.content).expect("Pattern not matching");
    let after_message = match caps.name("domain").as_str() {
        "x" | "twitter" => twitter(&caps),
        _ => twitter(&caps),
    };

    if let Err(why) = msg.channel_id.say(&ctx.http, after_message).await {
        println!("Error sending message: {why:?}");
    }

    let _ = remove_old_embed(&msg).await;
}
