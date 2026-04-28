mod commands;
use crate::commands::embed::Embed;
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
        let re: Regex = Regex::new(
            r"(http|https)://(www\.)*(?<domain>(instagram|twitter|threads|x))\.(cc|com)(?<endpoint>(/.+)*)",
        )
        .expect("Regex syntax invalid");

        if let Some(caps) = re.captures(&msg.content)
            && msg.author.id != UserId::new(1441446989362626772)
        {
            let _ = Embed::process_url(&ctx, &msg, &caps).await;
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
