// use crate::commands::embed::ContentFetcher;
// use async_trait::async_trait;
// use regex::{Captures, Regex};
use regex::Captures;
// use reqwest::{Client as HttpClient, Error};
use serenity::{builder::CreateMessage, prelude::*};

// pub struct InstagramFetcher;

// #[async_trait]
// impl ContentFetcher for InstagramFetcher {
//     async fn fetch_json(&self, endpoint: &str, ctx: &Context) -> Result<String, Error> {
//         let clean_endpoint = format!(
//             "https://www.instagram.com/{}/",
//             Regex::new(r"(?<instagram_endpoint>(/p/.+)/(.+))")
//                 .expect("Expected a valid regex pattern")
//                 .captures(endpoint)
//                 .expect("Expected a valid haystack")
//                 .get(0)
//                 .expect("Expected a valid matching")
//                 .as_str()
//                 .to_string()
//         );

//         let client: HttpClient = HttpClient::new();
//         let api_json: String = client.get(clean_endpoint).send().await?.text().await?;
//         println!("{:#?}", &api_json);

//         Ok(api_json)
//     }
// }

pub async fn handler(_ctx: &Context, _caps: &Captures<'_>) -> CreateMessage {
    let message = CreateMessage::new();
    message
}
