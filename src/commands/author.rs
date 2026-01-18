use serde_json::Value;

#[derive(Debug)]
pub struct Author {
    pub url: String,
    pub name: String,
    pub screen_name: String,
    pub icon_url: String,
}

impl Author {
    pub fn from_json(json_data: &Value) -> Self {
        fn get_string(v: &Value, k: &str) -> String {
            v[k].as_str().unwrap_or("").to_string()
        }

        Self {
            url: get_string(json_data, "url"),
            name: get_string(json_data, "name"),
            screen_name: get_string(json_data, "screen_name"),
            icon_url: get_string(json_data, "avatar_url"),
        }
    }

    pub fn from_str(url: &String, name: &String, screen_name: &String, icon_url: &String) -> Self {
        Self {
            url: String::from(url),
            name: String::from(name),
            screen_name: String::from(screen_name),
            icon_url: String::from(icon_url),
        }
    }
}
