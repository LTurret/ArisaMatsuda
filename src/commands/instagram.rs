use regex::Captures;
use serenity::{builder::CreateMessage, prelude::*};

pub async fn handler(_ctx: &Context, _caps: &Captures<'_>) -> CreateMessage {
    let message = CreateMessage::new();
    message
}
