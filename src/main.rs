mod commands;
use crate::commands::patcher::Patcher;
use dotenv::dotenv;
use regex::Regex;
use serenity::{
    async_trait,
    model::{channel::Message, gateway::Ready, id::UserId},
    prelude::*,
};
use std::env;

struct Handler;

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, ctx: Context, msg: Message) {
        let re: Regex = Regex::new(r"(http|https)://(www\.)*(?<domain>(x|twitter|instagram|facebook|threads|ppt)\.(cc|com))")
            .expect("Regex syntax invalid");
        if msg.author.id != UserId::new(1441446989362626772) && re.is_match(&msg.content) {
            Patcher::new(ctx, msg).parse().await;
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
        eprintln!("Client error: {why:?}");
    }
}
