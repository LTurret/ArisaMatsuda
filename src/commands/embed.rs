use crate::commands::twitter::Tweet;
use regex::{Captures, Regex};
use reqwest::{header::USER_AGENT, Client as HttpClient, Error};
use serenity::{builder::CreateMessage, prelude::*};

pub struct Embed;

impl Embed {
    pub async fn new_embed(&self, ctx: &Context, caps: &Captures<'_>) -> CreateMessage {
        let endpoint: String = caps
            .name("endpoint")
            .expect("Expected a valid haystack")
            .as_str()
            .to_string();

        // Regex Pattern: (http|https)://(?<domain>.+)\.com(?<endpoint>(/.+)*)
        let raw_api_data: String = match caps
            .name("domain")
            .expect("Expacted a valid haystack")
            .as_str()
        {
            "x" | "twitter" => self
                .fetch_tweet_json(endpoint)
                .await
                .expect("Err while fetching FxTwitter API"),
            "instagram" => self
                .fetch_instagram_json(endpoint)
                .await
                .expect("Err while fetching Instagram post"),
            _ => unimplemented!(),
        };

        let tweet: Tweet = Tweet::from_raw(&ctx, raw_api_data).await;
        let embed_message: CreateMessage = tweet.to_embed().await;

        embed_message
    }

    async fn fetch_tweet_json(&self, endpoint: String) -> Result<String, Error> {
        let caps: Captures<'_> = Regex::new(r"(?<tweet_endpoint>/.+/status/[0-9]+)(\?.=.+)*")
            .expect("Expected a valid regex pattern")
            .captures(endpoint.as_str())
            .expect("Expected a valid haystack");

        let api_url: String = format!(
            "https://api.fxtwitter.com{}",
            caps.name("tweet_endpoint")
                .expect("Expected a valid haystack")
                .as_str()
        );

        let client: HttpClient = HttpClient::new();
        let api_json: String = client
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

    async fn fetch_instagram_json(&self, endpoint: String) -> Result<String, Error> {
        let clean_endpoint = format!(
            "https://www.instagram.com/{}/",
            Regex::new(r"(?<instagram_endpoint>(/p/.+)/(.+))")
                .expect("Expected a valid regex pattern")
                .captures(endpoint.as_str())
                .expect("Expected a valid haystack")
                .get(0)
                .expect("Expected a valid matching")
                .as_str()
                .to_string()
        );

        let client: HttpClient = HttpClient::new();
        let api_json: String = client.get(clean_endpoint).send().await?.text().await?;
        println!("{:#?}", &api_json);

        Ok(api_json)
    }
}
