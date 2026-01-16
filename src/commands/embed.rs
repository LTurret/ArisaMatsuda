use crate::commands::{instagram::InstagramFetcher, twitter::TweetFetcher};
use async_trait::async_trait;
use regex::Captures;
use serenity::{builder::CreateMessage, prelude::*};

pub struct Embed;

#[async_trait]
pub trait ContentFetcher: Send + Sync {
    async fn fetch_json(&self, endpoint: &str, ctx: &Context) -> CreateMessage;
}

impl Embed {
    pub async fn new_embed(&self, ctx: &Context, caps: &Captures<'_>) -> CreateMessage {
        let endpoint: &str = caps
            .name("endpoint")
            .expect("Expected a valid haystack")
            .as_str();

        // Regex Pattern: (http|https)://(?<domain>.+)\.com(?<endpoint>(/.+)*)
        let fetcher: Box<dyn ContentFetcher + Send + Sync> = match caps
            .name("domain")
            .expect("Expacted a valid haystack")
            .as_str()
        {
            "x" | "twitter" => Box::new(TweetFetcher),
            "instagram" => Box::new(InstagramFetcher),
            _ => unimplemented!(),
        };

        let embed_message: CreateMessage = fetcher.fetch_json(&endpoint, ctx).await;

        embed_message
    }
}
