# 🤝 AI Personal Assistant — n8n + Streamlit

A fully functional AI-powered personal assistant that uses **n8n** as the AI workflow backend and **Streamlit** as the chat interface. The assistant can manage your calendar, emails, tasks, notes, expenses, and answer questions — all through natural conversation.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-Cloud-EA4B71?logo=n8n&logoColor=white)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [n8n Workflow Setup](#n8n-workflow-setup)
- [Usage](#usage)
- [Example Prompts](#example-prompts)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🔍 Overview

This project connects a **Streamlit** chat interface to an **n8n AI Agent** workflow via webhooks. When a user sends a message, it's forwarded to the n8n webhook, processed by an AI Agent (powered by Google Gemini), and the response is displayed back in the chat.

The AI Agent has access to multiple tools (Google Calendar, Gmail, Google Docs, Google Sheets, Google Tasks, and SerpAPI) allowing it to perform real actions based on user requests.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Chat Interface** | Clean Streamlit-based conversational UI with message history |
| 📅 **Calendar Management** | Create events, view schedule, get event details via Google Calendar |
| 📧 **Email Management** | Read, summarize, and send emails via Gmail |
| ✅ **Task Management** | Create, view, and delete tasks via Google Tasks |
| 📝 **Notes** | Create, update, and read documents via Google Docs |
| 💰 **Expense Tracking** | Log expenses and view history via Google Sheets |
| 🧮 **Calculator** | Perform arithmetic for budgeting and expense summaries |
| 🔍 **Web Search** | Search the web for real-time information via SerpAPI |
| 🧠 **Conversation Memory** | Maintains context across messages (15-message buffer window) |
| ⚡ **Error Handling** | Graceful handling of timeouts, connection errors, and unexpected responses |

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────────────────────────────┐
│                 │  POST   │              n8n Cloud                   │
│   Streamlit     │────────▶│                                          │
│   Chat UI       │  /webhook│  ┌─────────┐    ┌──────────┐    ┌─────┐│
│   (app.py)      │◀────────│  │ Webhook  │───▶│ AI Agent │───▶│Resp ││
│                 │  JSON   │  └─────────┘    └────┬─────┘    └─────┘│
└─────────────────┘         │                      │                  │
                            │         ┌────────────┼────────────┐     │
                            │         ▼            ▼            ▼     │
                            │   ┌──────────┐ ┌──────────┐ ┌────────┐ │
                            │   │ Calendar │ │  Gmail   │ │ Tasks  │ │
                            │   │ Sheets   │ │  Docs    │ │ Search │ │
                            │   └──────────┘ └──────────┘ └────────┘ │
                            └──────────────────────────────────────────┘
```

**Flow:**
1. User types a message in the Streamlit chat
2. Message is sent via `POST` request to the n8n webhook
3. n8n **AI Agent** (with Google Gemini LLM) processes the message
4. Agent decides which tool(s) to use based on user intent
5. Response flows back through the **Respond to Webhook** node
6. Streamlit displays the AI response in the chat

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit (Python) |
| **Backend / AI Workflow** | n8n Cloud |
| **LLM** | Google Gemini (via n8n LangChain node) |
| **Memory** | Buffer Window Memory (15 messages) |
| **Tools** | Google Calendar, Gmail, Google Docs, Google Sheets, Google Tasks, SerpAPI, Calculator |
| **Communication** | REST API (Webhook) |

---

## 📁 Project Structure

```
n8n-masterclass-main/
├── app.py              # Streamlit chat interface (main application)
├── sysprompt.md        # System prompt for the n8n AI Agent
├── README.md           # Project documentation (this file)
└── uv.lock             # Dependency lock file
```

| File | Purpose |
|------|---------|
| `app.py` | The Streamlit frontend — handles chat UI, sends messages to n8n webhook, displays AI responses |
| `sysprompt.md` | Detailed system prompt that defines the AI Agent's personality, capabilities, tool usage rules, and response format |

---

## 🚀 Setup & Installation

### Prerequisites

- **Python 3.10+** installed
- **n8n Cloud** account ([sign up here](https://n8n.io))
- API keys/OAuth credentials for:
  - Google Cloud (Calendar, Gmail, Docs, Sheets, Tasks)
  - Google Gemini API
  - SerpAPI

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/n8n-masterclass.git
cd n8n-masterclass-main
```

### 2. Install Dependencies

```bash
pip install streamlit requests
```

### 3. Update the Webhook URL

Open `app.py` and replace the webhook URL on **line 47** with your own n8n webhook URL:

```python
response = requests.post(
    "https://YOUR-INSTANCE.app.n8n.cloud/webhook/YOUR-WEBHOOK-ID",
    json={"msg": user_message},
    timeout=120
)
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ⚙️ n8n Workflow Setup

### Workflow Nodes

The n8n workflow consists of the following nodes:

| Node | Type | Purpose |
|------|------|---------|
| **Webhook** | Trigger | Receives POST requests from Streamlit (`/webhook/...`) |
| **AI Agent** | LangChain Agent | Processes user messages, decides which tools to call |
| **Google Gemini Chat Model** | LLM | Powers the AI Agent's reasoning |
| **Simple Memory** | Buffer Memory | Maintains conversation context (15-message window) |
| **Respond to Webhook** | Response | Sends the AI response back to Streamlit |
| **SerpAPI** | Tool | Web search for real-time information |
| **Calculator** | Tool | Arithmetic operations |
| **Google Calendar** (x3) | Tool | Create event, get single event, get many events |
| **Gmail** (x3) | Tool | Send message, get message, get many messages |
| **Google Docs** (x3) | Tool | Create document, update document, get document |
| **Google Sheets** (x2) | Tool | Get rows, append row |
| **Google Tasks** (x5) | Tool | Create, get single, get many, delete tasks |

### Webhook Configuration

- **HTTP Method:** POST
- **Response Mode:** Using 'Respond to Webhook' Node
- **Body Format:** JSON
- **Expected Input:** `{ "msg": "user message here" }`

### AI Agent Configuration

- **Prompt Source:** Define below
- **Prompt Expression:** `{{ $json.body.msg }}`
- **System Prompt:** Copy contents of `sysprompt.md` into the Agent's System Message (under Options)

### Important Notes

> ⚠️ **The workflow must be Active** (toggled ON in n8n) for the production webhook URL (`/webhook/...`) to work. Simply saving is not enough.

> 💡 Use the **Executions** tab in n8n to view past runs, debug issues, and see which tools the agent used.

---

## 💬 Usage

1. Start the Streamlit app: `streamlit run app.py`
2. Open `http://localhost:8501` in your browser
3. Type a message in the chat input box
4. Wait for the AI Agent to process and respond (may take a few seconds depending on tools used)

---

## 🧪 Example Prompts

### Calendar
```
Schedule a team meeting for tomorrow at 3 PM for 1 hour
What events do I have this week?
```

### Email
```
Show me my latest 5 emails and summarize them
Send an email to ali@example.com saying "Meeting confirmed for 3 PM"
```

### Tasks
```
Create a task: Submit project report by Friday
Show me all my pending tasks
Delete the groceries task
```

### Notes
```
Create a document called "Meeting Notes - March 18" and write the key discussion points
```

### Expenses
```
Add an expense: 2500 PKR for groceries today
Show me all my expenses this month
Calculate my total spending
```

### Web Search
```
What's the latest news about AI?
What's the weather in Karachi today?
```

### Multi-Tool
```
Check my calendar for today, show unread emails, and list my pending tasks
```

---

## 🔧 Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| **Empty response from webhook** | Workflow is not active | Toggle workflow to **Active** in n8n |
| **JSONDecodeError** | Webhook returning non-JSON | Check n8n Executions tab for errors |
| **"No prompt specified"** | Wrong expression in AI Agent | Use `{{ $json.body.msg }}` not `{{ $json.msg }}` |
| **Timeout error** | AI Agent taking too long | Increase timeout in `app.py` (default: 120s) |
| **Connection error** | n8n instance down or URL wrong | Verify webhook URL and n8n instance status |
| **Tool errors in n8n** | Expired OAuth tokens | Re-authenticate Google services in n8n credentials |

---

## 📄 License

This project is for educational purposes as part of the n8n Masterclass.

---

## 👤 Author

**Muhammad Mahad**

Built with ❤️ using n8n and Streamlit
