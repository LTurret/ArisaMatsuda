use dotenv::dotenv;
use regex::Regex;
use reqwest::Client as HttpClient;
use serde_json::json;
use serenity::async_trait;
use serenity::model::channel::Message;
use serenity::model::gateway::Ready;
use serenity::model::id::UserId;
use serenity::prelude::*;
use std::env;
use tokio::time::{sleep, Duration};

struct Handler;

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, ctx: Context, msg: Message) {
        let token = env::var("DISCORD_TOKEN").expect("Expected a token in the environment");
        let re: Regex = Regex::new(r"(?<protocol>https://)(?<domain>x\.com)/(?<username>\w+)/status/(?<snowflake>\d+)(?<suffix>\?s=\d+)*").unwrap();

        if msg.author.id != UserId::new(1441446989362626772) && re.is_match(&msg.content) {
            let after = re.replace_all(
                &msg.content,
                "${protocol}fxtwitter.com/${username}/status/${snowflake}",
            );

            if let Err(why) = msg.channel_id.say(&ctx.http, after).await {
                println!("Error sending message: {why:?}");
            }

            sleep(Duration::from_millis(250)).await;
            let url = format!(
                "https://discord.com/api/v9/channels/{}/messages/{}",
                msg.channel_id, msg.id
            );
            let client = HttpClient::new();
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

    async fn ready(&self, _: Context, ready: Ready) {
        println!("{} is connected!", ready.user.name);
    }
}

#[tokio::main]
async fn main() {
    dotenv().ok();

    let token: String = env::var("DISCORD_TOKEN").expect("Expected a token in the environment");

    let intents: GatewayIntents = GatewayIntents::GUILD_MESSAGES
        | GatewayIntents::DIRECT_MESSAGES
        | GatewayIntents::MESSAGE_CONTENT;

    let mut client = Client::builder(&token, intents)
        .event_handler(Handler)
        .await
        .expect("Err creating client");

    if let Err(why) = client.start().await {
        println!("Client error: {why:?}");
    }
}
