use crate::commands::{author::Author, embed::ContentBuilder};
use async_trait::async_trait;
use html_escape::decode_html_entities;
use regex::Regex;
use reqwest::{
    header::{HeaderMap, HeaderValue, USER_AGENT},
    Client as HttpClient,
};
use serenity::{
    builder::{
        CreateAllowedMentions, CreateEmbed, CreateEmbedAuthor,
        CreateEmbedFooter, CreateMessage,
    },
    model::Color,
    prelude::*,
};
use std::collections::HashSet;

#[derive(Debug)]
pub struct Thread {
    pub author: Author,
    pub content: String,
    pub images: Vec<CreateEmbed>,
}

impl Thread {
    async fn csrf_token() -> (String, String) {
        let url_str = "https://www.threads.net/";
        let mut headers = HeaderMap::new();
        headers.insert("User-Agent", HeaderValue::from_static("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"));
        headers.insert("Accept", HeaderValue::from_static("text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"));
        headers.insert(
            "Accept-Language",
            HeaderValue::from_static("en-US,en;q=0.9"),
        );
        headers.insert("Sec-Fetch-Dest", HeaderValue::from_static("document"));
        headers.insert("Sec-Fetch-Mode", HeaderValue::from_static("navigate"));
        headers.insert("Sec-Fetch-Site", HeaderValue::from_static("none"));
        headers
            .insert("Upgrade-Insecure-Requests", HeaderValue::from_static("1"));

        let client =
            reqwest::Client::builder().default_headers(headers).build();
        let response = client.unwrap().get(url_str).send().await.unwrap();
        let mut csrf_token = None;
        let mut ig_did = None;

        if response.status().is_success() {
            for cookie_header in response.headers().get_all("set-cookie") {
                if let Ok(cookie_str) = cookie_header.to_str() {
                    if let Some(first_part) = cookie_str.split(';').next() {
                        let parts: Vec<&str> =
                            first_part.trim().splitn(2, '=').collect();
                        if parts.len() == 2 {
                            match parts[0] {
                                "csrftoken" => {
                                    csrf_token = Some(parts[1].to_string())
                                }
                                "ig_did" => ig_did = Some(parts[1].to_string()),
                                _ => {}
                            }
                        }
                    }
                }
            }
        } else {
            panic!("Request failed with status: {}", response.status());
        }

        let token =
            csrf_token.expect("Failed to find csrftoken in response headers");
        let did = ig_did.expect("Failed to find ig_did in response headers");

        (token, did)
    }

    fn build_base_headers(csrf_token: &str, ig_did: &str) -> HeaderMap {
        let mut headers = HeaderMap::new();
        headers.insert("Host", HeaderValue::from_static("www.threads.com"));
        headers.insert(
            "Cookie",
            HeaderValue::from_str(&format!(
                "csrftoken={}; ig_did={}",
                csrf_token, ig_did
            ))
            .unwrap(),
        );
        headers.insert("Dpr", HeaderValue::from_static("1"));
        headers.insert("Viewport-Width", HeaderValue::from_static("958"));
        headers.insert(
            "Sec-Ch-Ua",
            HeaderValue::from_static(
                "\"Chromium\";v=\"145\", \"Not:A-Brand\";v=\"99\"",
            ),
        );
        headers.insert("Sec-Ch-Ua-Mobile", HeaderValue::from_static("?0"));
        headers.insert(
            "Sec-Ch-Ua-Platform",
            HeaderValue::from_static("\"Windows\""),
        );
        headers.insert(
            "Sec-Ch-Ua-Platform-Version",
            HeaderValue::from_static("\"\""),
        );
        headers.insert("Sec-Ch-Ua-Model", HeaderValue::from_static("\"\""));
        headers.insert(
            "Sec-Ch-Ua-Full-Version-List",
            HeaderValue::from_static("\"\""),
        );
        headers.insert(
            "Sec-Ch-Prefers-Color-Scheme",
            HeaderValue::from_static("dark"),
        );
        headers.insert(
            "Accept-Language",
            HeaderValue::from_static("en-US,en;q=0.9"),
        );
        headers
            .insert("Upgrade-Insecure-Requests", HeaderValue::from_static("1"));
        headers.insert("User-Agent", HeaderValue::from_static("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"));
        headers.insert("Accept", HeaderValue::from_static("text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"));
        headers.insert("Sec-Fetch-Site", HeaderValue::from_static("none"));
        headers.insert("Sec-Fetch-Mode", HeaderValue::from_static("navigate"));
        headers.insert("Sec-Fetch-User", HeaderValue::from_static("?1"));
        headers.insert("Sec-Fetch-Dest", HeaderValue::from_static("document"));
        headers.insert("Accept-Encoding", HeaderValue::from_static("identity"));
        headers.insert("Priority", HeaderValue::from_static("u=0, i"));
        headers.insert("Connection", HeaderValue::from_static("keep-alive"));

        headers
    }

    async fn get_author_names(profile_url: &String) -> (String, String) {
        let (csrf_token, ig_did) = Self::csrf_token().await;
        let headers = Self::build_base_headers(&csrf_token, &ig_did);
        let response_result: Result<reqwest::Response, reqwest::Error> =
            HttpClient::new().get(profile_url).headers(headers).send().await;

        let response: String = match response_result {
            Ok(res) => res.text().await.expect("Failed to read response text"),
            Err(e) => {
                eprintln!("{}", e);
                return (String::from("None"), String::from("None"));
            }
        };

        let author_screen_name: String = Regex::new(
            r#"<h1\sclass="x1lliihq x1plvlek xryxfnj x1n2onr6 xyejjpt x15dsfln x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x133cpev x1xlr1w8 xw2npq5 x1yc453h"(?:\s.{1,10}="[^"]+")*>(?P<author_name>[^<]+)<\/h1>"#,
        )
        .expect("Regex syntax invalid")
        .captures(&response)
        .expect("Expected a valid haystack")
        .name("author_name")
        .expect("String not match")
        .as_str()
        .to_string();

        let author_name: String = Regex::new(
            r#"<span\sclass="x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft">(?P<author_name>[^\/]+)<\/span>"#,
        )
        .expect("Regex syntax invalid")
        .captures(&response)
        .expect("Expected a valid haystack")
        .name("author_name")
        .expect("String not match")
        .as_str()
        .to_string();

        (author_screen_name, author_name)
    }

    async fn get_images(post_url: &String) -> Vec<CreateEmbed> {
        let (csrf_token, ig_did) = Self::csrf_token().await;
        let headers = Self::build_base_headers(&csrf_token, &ig_did);
        let response_result: Result<reqwest::Response, reqwest::Error> =
            HttpClient::new().get(post_url).headers(headers).send().await;

        let response: String = match response_result {
            Ok(res) => res.text().await.expect("Failed to read response text"),
            Err(e) => {
                eprintln!("{}", e);
                return vec![CreateEmbed::new().url("https://lturret.xyz")];
            }
        };

        let mut images_string: Vec<String> = vec![];
        let video_preview: Regex = Regex::new(
            r#"<img\sheight="100%"\swidth="100%"\sclass="(?:x15mokao x1ga7v0g x16uus16 xbiv7yw x1ey2m1c xtijo5x x1o0tod x10l6tqk x13vifvy xl1xv1r)"\salt="[^"]*"\sreferrer[p|P]olicy="origin-when-cross-origin"\ssrc="(?P<source_url>[^"]+)"\/>"#,
        )
        .expect("Regex syntax invalid");

        images_string.extend(
            video_preview.captures_iter(&response).filter_map(|cap| {
                cap.name("source_url")
                    .map(|m| m.as_str().to_string().replace("&amp;", "&"))
            }),
        );

        let high_quality_pictures: Regex = Regex::new(
            r#"<img(?:\s[^"]+="[^"]*")*\ssrc="(?P<source_url>https://instagram\.ftpe\d-\d\.fna\.fbcdn\.net\/v\/t\d{1,5}\.\d{1,10}-\d{1,3}\/[^_]{1,100}_[^_]{1,100}_[^_]{1,100}_[^\.]{1,100}\.(?:webp|jpg|jpeg|png|bmp)\?{1}[^"]+)""#,
        )
        .expect("Regex syntax invalid");

        images_string.extend(
            high_quality_pictures
                .captures_iter(&response)
                .filter_map(|cap| {
                    cap.name("source_url")
                        .map(|m| m.as_str().to_string().replace("&amp;", "&"))
                })
                .skip(1),
        );

        let mut seen = HashSet::new();
        let images: Vec<CreateEmbed> = images_string
            .into_iter()
            .filter(|url| seen.insert(url.clone()))
            .map(|m| CreateEmbed::new().url("https://lturret.xyz").image(m))
            .take(4)
            .collect();

        images
    }

    async fn from_raw_response(
        clean_url: String,
        raw_response: String,
    ) -> Self {
        let author: String = Regex::new(
            r"https://www\.threads\.com/(?<author>&#064;[a-zA-Z0-9._-]+)/",
        )
        .expect("Regex syntax invalid")
        .captures(&raw_response)
        .expect("Expected a valid haystack")
        .name("author")
        .expect("String not match")
        .as_str()
        .to_string();

        let decoded_author_name: String =
            decode_html_entities(&author).to_string();

        let url: &String =
            &format!("https://www.threads.com/{}", decoded_author_name);

        let (author_screen_name, author_name): (String, String) =
            Self::get_author_names(url).await;

        let images = Self::get_images(&clean_url).await;
        let content: String = Regex::new(r"<title>(?<content>[\s\S]+)</title>")
            .expect("Regex syntax invalid")
            .captures(&raw_response)
            .expect("Expected a valid haystack")
            .name("content")
            .expect("String not match")
            .as_str()
            .to_string();

        Self {
            author: Author::from_str(
                url,
                &format!("@{}", author_name),
                &author_screen_name,
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
                CreateEmbedAuthor::new(format!(
                    "{} ({})",
                    self.author.screen_name, self.author.name
                ))
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
            Regex::new(r"(?<thread_endpoint>@.+/post/[a-zA-Z0-9._-]+)/?{1}")
                .expect("Expected a valid regex pattern")
                .captures(endpoint)
                .expect("Expected a valid haystack")
                .name("thread_endpoint")
                .expect("Expected a valid matching")
                .as_str()
        );

        let response_result: Result<reqwest::Response, reqwest::Error> = HttpClient::new()
            .get(&clean_url)
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
            Thread::from_raw_response(clean_url, response)
                .await
                .into_embed()
                .await;

        embed_message
    }
}
