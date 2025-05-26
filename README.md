# 📬 EmailAssistant for Claude Desktop

EmailAssistant is an MCP-compatible server that integrates with the Gmail API to fetch and summarize emails based on custom queries or recent activity. It can be used with Claude Desktop to interact hands-free with your inbox.

---

## ⚙️ Setup Instructions

### 1. Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or use an existing one.
3. Enable the **Gmail API** under “APIs & Services”.
4. Create **OAuth 2.0 Client ID** credentials.
5. Download the `client_secret_XXXXX.json` file.

---

## 🔧 Configuration Summary

### 🔁 Replace These in `config.py`

- Replace `/absolute/path/to/your/project` with the **full path to your local EmailAssistant project directory**.
- Replace `"your_client_secret_file.json"` with the **exact filename** of your downloaded OAuth credentials from Google Cloud.

---

### 🖥️ 3. Claude Desktop Configuration

In your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "EmailAssistant": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "google-api-python-client",
        "--with",
        "google-auth-httplib2",
        "--with",
        "google-auth-oauthlib",
        "mcp",
        "run",
        "/absolute/path/to/your/project/emailassistant/main.py"
      ]
    }
  }
}
```

## ✅ Running It

Once configured:

1. **Start Claude Desktop**
2. Claude will automatically recognize the `EmailAssistant` MCP server.
3. You can now use Claude to call functions like:

```python
get_email_summary(time="newer_than:1d")
get_top_matching_email(query_keywords="project deadline")
```

## 📌 Requirements

- **Python 3.9+**
- [`uv`](https://github.com/astral-sh/uv) (or use `pip` if not using `uv`)
- The following Python packages:
  - `google-api-python-client`
  - `google-auth-httplib2`
  - `google-auth-oauthlib`
  - `mcp[cli]`





