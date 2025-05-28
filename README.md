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

### 🔁 Create `config.py` with these contents:

```python
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
PROJECT_DIR = "/absolute/path/to/your/project/directory/"
CREDENTIALS_FP = os.path.join(PROJECT_DIR, "client_secret_XXXXX.json")
TOKEN_FP = os.path.join(PROJECT_DIR, "token.json")
```

Note: Make sure to replace the placeholders in the above code---PROJECT_DIR & CREDENTIALS_FP

---

### 🖥️ 3. Claude Desktop Configuration

In your Claude Desktop configuration file (can find it in Developer Settings):

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
        "yake",
        "--with",
        "google-api-python-client",
        "--with",
        "google-auth-httplib2",
        "--with",
        "google-auth-oauthlib",
        "mcp",
        "run",
        "/absolute/path/to/your/project/directory/main.py"
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

4. All you need to do is ask Claude in plain english about your inbox

## 📌 Requirements

- **Python 3.9+**
- [`uv`](https://github.com/astral-sh/uv) (or use `pip` if not using `uv`)
- The following Python packages:
  - `google-api-python-client`
  - `google-auth-httplib2`
  - `google-auth-oauthlib`
  - `mcp[cli]`





