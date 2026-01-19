use crate::commands::{
    author::Author,
    embed::{ContentFetcher, Embed},
};
use async_trait::async_trait;
use html_escape::decode_html_entities;
use regex::{Captures, Regex};
use reqwest::{
    header::{HeaderMap, HeaderValue, USER_AGENT},
    Client as HttpClient,
};
use serde_json::Value;
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

        let url: &String = &String::from(format!("https://www.instagram.com/{}", &author));
        let icon_url: String = InstagramPost::get_profile_pic_url(&author).await;

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
            author: Author::from_str(url, &author, &author, &icon_url),
            content: content,
            videos_supplementary: videos_supplementary,
        }
    }

    async fn get_profile_pic_url(username: &String) -> String {
        let mut headers = HeaderMap::new();
        headers.insert("x-ig-app-id", HeaderValue::from_static("936619743392459"));

        let response = reqwest::Client::new()
            .get(format!(
                "https://www.instagram.com/api/v1/users/web_profile_info/?username={}",
                username
            ))
            .headers(headers)
            .send()
            .await
            .expect("Request user manifest failed");

        let res: Value = response.json().await.expect("JSON parse failed");

        res["data"]["user"]["profile_pic_url"]
            .as_str()
            .unwrap_or(r#"Did not found "profile_pic_url" in the JSON"#)
            .to_string()
    }

    #[deprecated = "get_profile_pic_url() is enough to get user icon url"]
    #[cfg(false)]
    async fn get_icon_url(author: &String) -> String {
        use reqwest::{
            cookie::{CookieStore, Jar},
            header::HeaderName,
            Url,
        };
        use std::sync::Arc;

        let user_id: String = InstagramPost::get_user_id(author).await;
        let jar = Arc::new(Jar::default());
        let _client: Response = HttpClient::builder()
            .cookie_provider(jar.clone())
            .user_agent("Mozilla/5.0")
            .build()
            .unwrap()
            .get("https://www.instagram.com/")
            .send()
            .await
            .unwrap();

        let cookie_val: HeaderValue = jar
            .as_ref()
            .cookies(&Url::parse(format!("https://www.instagram.com/{}", author).as_str()).unwrap())
            .ok_or("no cookies found")
            .unwrap();

        let cookie_header: String = cookie_val.to_str().unwrap().to_string();
        let csrftoken: String = cookie_header
            .split(';')
            .find(|c| c.trim().starts_with("csrftoken="))
            .map(|c| {
                c.trim()
                    .strip_prefix("csrftoken=")
                    .unwrap_or("")
                    .to_string()
            })
            .expect("csrftoken not found");

        let body = format!("variables=%7B%22enable_integrity_filters%22%3Atrue%2C%22id%22%3A%22{}%22%2C%22render_surface%22%3A%22PROFILE%22%2C%22__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider%22%3Atrue%2C%22__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider%22%3Afalse%2C%22__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider%22%3Afalse%7D&doc_id=25980296051578533", user_id);

        let mut headers = HeaderMap::new();
        let cookie = format!("ig_did=B9C9BB5D-2753-46D0-9784-3C94B0FAD0C9;csrftoken={};datr=rl40aad9n6XXVIcGcEsaMfZU;mid=aTRergALAAGAj_Wk-MQWM3oJJrI3;ps_l=1; ps_n=1; ig_nrcb=1; wd=958x944", csrftoken);

        headers.insert(
            HeaderName::from_static("cookie"),
            HeaderValue::try_from(cookie).expect("cookie invalid"),
        );
        headers.insert(
            HeaderName::from_static("content-type"),
            HeaderValue::from_static("application/x-www-form-urlencoded"),
        );
        headers.insert(
            HeaderName::from_static("x-csrftoken"),
            HeaderValue::try_from(csrftoken).expect("x-csrftoken"),
        );

        let response = HttpClient::new()
            .post("https://www.instagram.com/graphql/query")
            .headers(headers)
            .body(body)
            .send()
            .await;

        match response {
            Ok(res) => {
                res.text().await.unwrap();
            }
            Err(e) => {
                eprintln!("Response parse error: {}", e);
            }
        }

        let response = String::from("gay");
        response
    }

    async fn to_embed(self) -> CreateMessage {
        let embed: CreateEmbed = CreateEmbed::new()
            .color(Color::new(0xce0071))
            .author(CreateEmbedAuthor::new(format!("{}", self.author.name)).icon_url(self.author.icon_url).url(self.author.url))
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
