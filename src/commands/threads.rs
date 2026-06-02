use crate::commands::{author::Author, embed::ContentBuilder};
use async_trait::async_trait;
use chromiumoxide::browser::{Browser, BrowserConfig};
use futures::StreamExt;
use html_escape::decode_html_entities;
use regex::Regex;
use reqwest::{Client as HttpClient, header::USER_AGENT};
use scraper::{Html, Selector};
use serenity::{
    builder::{
        CreateAllowedMentions, CreateEmbed, CreateEmbedAuthor,
        CreateEmbedFooter, CreateMessage,
    },
    model::Color,
    prelude::*,
};
use std::time::Duration;

#[derive(Debug)]
pub struct Thread {
    pub author: Author,
    pub content: String,
    pub images: Vec<CreateEmbed>,
}

impl Thread {
    async fn from_raw_response(
        raw_response: String,
        thread_url: String,
    ) -> Self {
        let raw_author_name: String = Regex::new(
            r"https://www\.threads\.com/(?<author>&#064;[a-zA-Z0-9._-]+)/",
        )
        .expect("Regex syntax invalid")
        .captures(&raw_response)
        .expect("Expected a valid haystack")
        .name("author")
        .expect("Not a valid tag")
        .as_str()
        .to_string();

        let safe_author_name: String =
            decode_html_entities(&raw_author_name).to_string();

        let url: &String =
            &format!("https://www.threads.com/{}", safe_author_name);

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

        let author_rich_name: String =
            Regex::new(r"<title>(?<author>.+)\s•\s.+</title>")
                .expect("Expected a valid regex")
                .captures(&profile)
                .expect("Expected a valid haystack")
                .name("author")
                .expect("Not a valid tag")
                .as_str()
                .to_string()
                .replace("&#064;", "@");

        let content: String = Regex::new(r"<title>(?<content>[\s\S]+)</title>")
            .expect("Regex syntax invalid")
            .captures(&raw_response)
            .expect("Expected a valid haystack")
            .name("content")
            .expect("String not match")
            .as_str()
            .to_string();

        let mut images_list: Vec<String> = vec![];
        let config = BrowserConfig::builder()
            .request_timeout(Duration::from_secs(15))
            .no_sandbox()
            .build()?;

        let (mut browser, mut handler) = Browser::launch(config).await?;

        tokio::task::spawn(async move {
            while let Some(event) = handler.next().await {
                if let Err(e) = event {
                    eprintln!("Handler loop encountered an error: {}", e);
                    break;
                }
            }
        });

        let page = browser.new_page(thread_url).await?;
        let rendered_html = page.content().await?;
        browser.close().await?;

        let document = Html::parse_document(&raw_response);
        let selector = Selector::parse(".x15mokao.x1ga7v0g")
            .expect("Expected a valid selector literal");

        for element in document.select(&selector) {
            let text: String = element.text().collect();
            images_list.push(text);
        }

        println!("{:?}", images_list);

        let images: Vec<CreateEmbed> = vec![CreateEmbed::new().url("https://lturret.xyz").image("https://scontent-tpe1-1.cdninstagram.com/v/t51.71878-15/710959513_1007242648708854_4983066876886763328_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=110&ig_cache_key=MzkxMDAzMTM5MTE1NzYwODE1Ng%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuNjQwLnNkci52aWRlb19kZWZhdWx0X2NvdmVyX2ZyYW1lLkMyIn0%3D&_nc_ohc=u-SXAT5_PNgQ7kNvwGzEQoS&_nc_oc=Adqbs73t3NUlARh9llt2OY6W-Gx_GWsgthXKBnczhkbHQO-2SYYusNnSBVEcWIKftOA&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent-tpe1-1.cdninstagram.com&_nc_gid=dvS0ETWH3mxRfmQPRX4Trw&_nc_ss=7a22e&oh=00_Af-IHZ4oS-837K1yBIORfScJRnhfIZ1R89vdOL8XDlISKA&oe=6A2431C4")];

        Self {
            author: Author::from_str(
                url,
                &String::from(""),
                &author_rich_name,
                None,
            ),
            content,
            images,
        }
    }

    async fn into_embed(self) -> CreateMessage {
        let embed: CreateEmbed = CreateEmbed::new()
            .color(Color::new(0x181818))
            .author(
                CreateEmbedAuthor::new(self.author.screen_name)
                    .url(self.author.url),
            )
            .description(self.content)
            .footer(CreateEmbedFooter::new("Threads").icon_url(
                "https://cdn-icons-png.flaticon.com/512/12105/12105338.png",
            ))
            .url("https://lturret.xyz");

        let builder: CreateMessage = CreateMessage::new()
            .allowed_mentions(CreateAllowedMentions::new().empty_users())
            .embed(embed)
            .add_embeds(self.images);

        builder
    }
}

pub struct ThreadBuilder;

#[async_trait]
impl ContentBuilder for ThreadBuilder {
    async fn embed_message(
        &self,
        endpoint: &str,
        _ctx: &Context,
    ) -> CreateMessage {
        let clean_url = format!(
            "https://www.threads.com/{}",
            Regex::new(r"(?<thread_endpoint>@.+/post/[a-zA-Z0-9._-]+)/?")
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
            Thread::from_raw_response(response, clean_url)
                .await
                .into_embed()
                .await;

        embed_message
    }
}
