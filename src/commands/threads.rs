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
}

impl Thread {
    async fn from_raw_response(raw_response: String) -> Self {
        let author: String =
            Regex::new(r"https://www\.threads\.com/(?<author>&#064;[a-zA-Z0-9._-]+)/")
                .expect("Regex syntax invalid")
                .captures(&raw_response)
                .expect("Expected a valid haystack")
                .name("author")
                .expect("String not match")
                .as_str()
                .to_string();

        let decoded_author_name: String = decode_html_entities(&author).to_string();
        let url: &String = &format!("https://www.threads.com/{}", decoded_author_name);
        let profile: String = HttpClient::new()
            .get(url)
            .header(
                USER_AGENT,
                "Rust Discord Bot (https://github.com/LTurret/ArisaMatsuda)",
            )
            .send()
            .await
            .expect("Connection error")
            .text()
            .await
            .expect("Failed to read response text");

        let author_alias: String =
            Regex::new(r"<title>(?<author_alias>.+)\s\(&#064;.+\)\s.\s.+</title>")
                .expect("Regex syntax invalid")
                .captures(&profile)
                .expect("Expected a valid haystack")
                .name("author_alias")
                .expect("String not match")
                .as_str()
                .to_string();

        let content: String = Regex::new(r"<title>(?<content>[\s\S]+)</title>")
            .expect("Regex syntax invalid")
            .captures(&raw_response)
            .expect("Expected a valid haystack")
            .name("content")
            .expect("String not match")
            .as_str()
            .to_string();

        Self {
            author: Author::from_str(url, &decoded_author_name, &author_alias, None),
            content,
        }
    }

    async fn into_embed(self) -> CreateMessage {
        let embed: CreateEmbed = CreateEmbed::new()
            .color(Color::new(0x181818))
            .author(
                CreateEmbedAuthor::new(format!(
                    "{} ({})",
                    self.author.screen_name, self.author.name
                ))
                .url(self.author.url),
            )
            .description(self.content)
            .footer(
                CreateEmbedFooter::new("Threads")
                    .icon_url("https://cdn-icons-png.flaticon.com/512/12105/12105338.png"),
            )
            .url("https://lturret.xyz");

        let builder: CreateMessage = CreateMessage::new()
            .allowed_mentions(CreateAllowedMentions::new().empty_users())
            .embed(embed);

        builder
    }
}

pub struct ThreadBuilder;

#[async_trait]
impl ContentBuilder for ThreadBuilder {
    async fn embed_message(&self, endpoint: &str, _ctx: &Context) -> CreateMessage {
        let clean_url = format!(
            "https://www.threads.com/{}",
            Regex::new(r"(?<thread_endpoint>@.+/post/[\w]+)/?")
                .expect("Expected a valid regex pattern")
                .captures(endpoint)
                .expect("Expected a valid haystack")
                .name("thread_endpoint")
                .expect("Expected a valid matching")
                .as_str()
        );

        let response_result: Result<reqwest::Response, reqwest::Error> = HttpClient::new()
            .get(clean_url)
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

        let embed_message: CreateMessage =
            Thread::from_raw_response(response).await.into_embed().await;

        embed_message
    }
}
