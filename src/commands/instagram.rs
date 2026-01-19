use crate::commands::{
    author::Author,
    embed::{ContentFetcher, Embed},
};
use async_trait::async_trait;
use html_escape::decode_html_entities;
use regex::{Captures, Regex};
use reqwest::{header::USER_AGENT, Client as HttpClient};
use serenity::{
    builder::{
        CreateAllowedMentions, CreateEmbed, CreateEmbedAuthor, CreateEmbedFooter, CreateMessage,
    },
    model::Color,
    prelude::*,
};

#[derive(Debug)]
pub struct InstagramPost {
    pub author: Author,
    pub content: String,
    pub videos_supplementary: String,
}

impl InstagramPost {
    async fn from_raw_response(raw_response: String) -> Self {
        let author: String = Regex::new(
            r#"<meta\sproperty="og:url"\scontent="https://www.instagram.com/(?<author>.+)/p/"#,
        )
        .unwrap()
        .captures(&raw_response)
        .unwrap()
        .name("author")
        .unwrap()
        .as_str()
        .to_string();

        let raw_content: &str = Regex::new(
            r#"(?s)<meta\sproperty="og:title"\scontent=".+on Instagram:(?<content>.+)".+><meta\sproperty="og:image""#,
        )
        .unwrap()
        .captures(&raw_response)
        .unwrap()
        .name("content")
        .unwrap()
        .as_str();

        let content_chars: Vec<char> = decode_html_entities(&raw_content).chars().collect();
        let content: String = content_chars[2..content_chars.len() - 1].iter().collect();
        let videos_supplementary: String = String::from("");

        Self {
            author: Author::from_str(&String::from(""), &author, &author, &String::from("")),
            content: content,
            videos_supplementary: videos_supplementary,
        }
    }

    async fn to_embed(self) -> CreateMessage {
        let embed: CreateEmbed = CreateEmbed::new()
            .color(Color::new(0xce0071))
            .author(CreateEmbedAuthor::new(format!("{}", self.author.name)))
            .description(self.content)
            .footer(
                CreateEmbedFooter::new("Instagram")
                    .icon_url("https://images-ext-1.discordapp.net/external/C6jCIKlXguRhfmSp6USkbWsS11fnsbBgMXiclR2R4ps/https/www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png"),
            )
            .url("https://lturret.xyz");

        let builder: CreateMessage = CreateMessage::new()
            .content(&self.videos_supplementary)
            .allowed_mentions(CreateAllowedMentions::new().empty_users())
            .embed(embed);

        builder
    }
}

pub struct InstagramFetcher;

#[async_trait]
impl ContentFetcher for InstagramFetcher {
    async fn embed_message(&self, endpoint: &str, _ctx: &Context) -> CreateMessage {
        let clean_endpoint = format!(
            "https://www.instagram.com/p/{}/",
            Regex::new(r"/p/(?<post_id>.+)/")
                .expect("Expected a valid regex pattern")
                .captures(endpoint)
                .expect("Expected a valid haystack")
                .name("post_id")
                .expect("Expected a valid matching")
                .as_str()
                .to_string()
        );

        let response_result: Result<reqwest::Response, reqwest::Error> = HttpClient::new()
            .get(clean_endpoint)
            .header(
                USER_AGENT,
                "Rust Discord Bot (https://github.com/LTurret/ArisaMatsuda)",
            )
            .send()
            .await;

        let response: String = match response_result {
            Ok(res) => res.text().await.expect("Failed to read response text"),
            Err(e) => {
                eprintln!("{}", e);
                return CreateMessage::new().content("Failed to fetch post");
            }
        };

        let instagram_post: InstagramPost = InstagramPost::from_raw_response(response).await;
        let embed_message: CreateMessage = instagram_post.to_embed().await;
        embed_message
    }
}

pub async fn handler(ctx: &Context, caps: &Captures<'_>) -> CreateMessage {
    let embed_message = Embed.new_embed(ctx, caps).await;
    embed_message
}
