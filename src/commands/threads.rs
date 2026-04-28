use crate::commands::{author::Author, embed::ContentBuilder};
use async_trait::async_trait;
use html_escape::decode_html_entities;
use regex::Regex;
use reqwest::{header::USER_AGENT, Client as HttpClient};
use serenity::{
    builder::{
        CreateAllowedMentions, CreateEmbed, CreateEmbedAuthor, CreateEmbedFooter, CreateMessage,
    },
    model::Color,
    prelude::*,
};

#[derive(Debug)]
pub struct Thread {
    pub author: Author,
    pub content: String,
    pub videos_supplementary: String,
}

impl Thread {
    async fn from_raw_response(raw_response: String) -> Self {
        let author: String =
            Regex::new(r"https://www\.threads\.com/(?<author>&#064;[a-zA-Z0-9._-]+)/")
                .expect("Regex syntax invalid")
                .captures(&raw_response)
                .expect("Expected a valid haystack")
                .name("author")
                .unwrap()
                .as_str()
                .to_string();

        let decoded_author_name: String = decode_html_entities(&author).to_string();
        let url: &String = &format!("https://www.threads.com/{}", decoded_author_name);
        let raw_content: &str = Regex::new(r"<title>(?<content>[\s\S]+)</title>")
            .expect("Regex syntax invalid")
            .captures(&raw_response)
            .expect("Expected a valid haystack")
            .name("content")
            .unwrap()
            .as_str();

        let content_chars: Vec<char> = decode_html_entities(&raw_content).chars().collect();
        let content: String = content_chars[2..content_chars.len()].iter().collect();
        let videos_supplementary: String = String::from("");

        Self {
            author: Author::from_str(url, &decoded_author_name, &decoded_author_name, None),
            content,
            videos_supplementary,
        }
    }

    async fn into_embed(self) -> CreateMessage {
        let embed: CreateEmbed = CreateEmbed::new()
            .color(Color::new(0x181818))
            .author(CreateEmbedAuthor::new(self.author.name).url(self.author.url))
            .description(self.content)
            .footer(
                CreateEmbedFooter::new("Threads")
                    .icon_url("https://cdn-icons-png.flaticon.com/512/12105/12105338.png"),
            )
            .url("https://lturret.xyz");

        let builder: CreateMessage = CreateMessage::new()
            .content(&self.videos_supplementary)
            .allowed_mentions(CreateAllowedMentions::new().empty_users())
            .embed(embed);

        builder
    }
}

pub struct ThreadBuilder;

#[async_trait]
impl ContentBuilder for ThreadBuilder {
    async fn embed_message(&self, endpoint: &str, _ctx: &Context) -> CreateMessage {
        let clean_endpoint = format!(
            "https://www.threads.com/{}/",
            Regex::new(r"(?<thread_endpoint>@.+/post/.+)")
                .expect("Expected a valid regex pattern")
                .captures(endpoint)
                .expect("Expected a valid haystack")
                .name("thread_endpoint")
                .expect("Expected a valid matching")
                .as_str()
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

        let thread_post: Thread = Thread::from_raw_response(response).await;
        let embed_message: CreateMessage = thread_post.into_embed().await;
        embed_message
    }
}
