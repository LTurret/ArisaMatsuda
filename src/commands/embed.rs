use crate::commands::twitter::Tweet;
use regex::{Captures, Regex};
use reqwest::{header::USER_AGENT, Client as HttpClient, Error};
use serenity::{builder::CreateMessage, prelude::*};

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

pub async fn new_embed(ctx: &Context, raw_endpoint: String) -> CreateMessage {
    let raw_api_data: String = fetch_tweet_json(raw_endpoint)
        .await
        .expect("Expected a valid connection for fetching API data");

    let tweet: Tweet = Tweet::from_raw(&ctx, raw_api_data).await;
    let embed_message: CreateMessage = tweet.to_embed().await;

    embed_message
}
