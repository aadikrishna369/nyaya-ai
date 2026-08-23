# nyaya-ai
# Nyaya AI

### Know. Act. Empower.

Nyaya AI is an AI-powered legal and civic assistance tool built to make legal information, civic procedures, and documents easier to understand.

The idea behind Nyaya AI is simple: legal and government-related information can often be difficult to navigate, especially when you don't know where to start. Nyaya AI provides a conversational interface where users can ask questions, understand legal concepts, navigate civic procedures, or upload a document for analysis.

> **This project is a prototype and is intended for informational purposes only. It is not a substitute for professional legal advice.**

---

## What can Nyaya AI do?

Nyaya AI currently has three main modes:

### ⚖️ Legal

Ask general questions about legal concepts, rights, procedures, and everyday legal situations.

For example:

- "What is an FIR?"
- "What are my options if my landlord refuses to return my security deposit?"
- "What is the difference between a civil and criminal case?"
- "What should I do after receiving a legal notice?"

The AI attempts to explain the issue in simple language and provide practical next steps.

---

### 🏛️ Civic

The Civic mode focuses on helping users understand government and public-service procedures.

For example:

- "How do I apply for a passport?"
- "Where can I report a civic issue?"
- "How do I register a consumer complaint?"
- "Which authority handles this problem?"

The goal is to make civic processes easier to understand and navigate.

---

### 📄 Document

Upload a PDF and ask Nyaya AI to analyze it.

The document mode can help with things such as:

- Summarizing an agreement
- Explaining difficult clauses
- Identifying important sections
- Highlighting obligations and conditions
- Extracting relevant information from a document

### Current limitation

The document analyzer currently works as a **single-turn analysis**.

The uploaded PDF and question are analyzed together, but **follow-up questions about the same document are not currently supported**.

For example:

> Upload agreement → "Summarize this agreement"

works, but:

> "What does the termination clause mean?"

followed by:

> "Is that clause risky for me?"

is not currently maintained as a continuing document conversation.

This is something planned for a future version.

---

## 💬 Multiple Chats

Nyaya AI supports multiple independent chat instances.

Users can:

- Create a new chat
- Switch between existing chats
- Keep conversations separated
- Start a fresh conversation without affecting another one

The chat history is currently maintained using Streamlit's session state.

---

## 🧹 Session Management

Nyaya AI also includes a **Clear Session** option.

This allows the user to clear the current session data and start fresh.

This is particularly useful while experimenting with different conversations and documents.

---

## 🛠️ Built With

- **Python**
- **Streamlit** — Web interface and application framework
- **Google Gemini API** — AI reasoning and document analysis
- **Google GenAI Python SDK**
- **Streamlit Session State** — Chat and session management

---

## 🏗️ How it works

At a high level, the application follows this flow:

```text
                         ┌───────────────┐
                         │    User       │
                         └───────┬───────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │   Nyaya AI Interface │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
          ⚖ Legal          🏛 Civic        📄 Document
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                        ┌─────────────┐
                        │ Gemini API  │
                        └──────┬──────┘
                               │
                               ▼
                        Structured Answer
                               │
                               ▼
                         Streamlit UI
