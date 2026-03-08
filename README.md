# CapStone-Project: Enterprise Automation Gen AI

An advanced, enterprise-ready Generative AI system specialized in Automation Engineering. This project leverages an Agentic RAG (Retrieval-Augmented Generation) architecture to provide refined, context-aware answers by combining local internal knowledge with real-time web search.

## 🌟 Key Features

- **Agentic RAG Flow**: Sophisticated decision-making via LangGraph for document grading and retrieval.
- **Enterprise Ready**: Centralized configuration (Pydantic), professional logging, and global error handling.
- **Multi-Source Intelligence**: Integrates ChromaDB for internal RAG and Google/DuckDuckGo for web-enhanced answers.
- **Automated Testing**: Comprehensive unit test suite covering core API logic.
- **Modern Dashboard**: Real-time monitoring of system performance and LLM usage logs.

## 🏗️ System Architecture

The core of the system is an intelligent agent that dynamically decides between local knowledge and web search:
1. **Retrieve**: Pulls context from the local vector database.
2. **Grade**: Evaluates context relevance using an LLM.
3. **Decide**: If context is sufficient, generate; otherwise, perform a web search.
4. **Refine**: Polishes the final response for high technical accuracy.

## 📥 Getting Started

For detailed installation and configuration instructions, please refer to the **[Setup Guide](SETUP_GUIDE.md)**.

### Quick Start (Development)
```bash
# Backend
uv sync
PYTHONPATH=. uv run python capstone/backend/app.py

# Frontend
cd capstone/frontend
npm install
npm run dev
```

## 📝 Testing

To run the automated test suite and verify the system's integrity:
```bash
PYTHONPATH=. uv run pytest
```

## 🛠️ Project Structure

- `capstone/backend`: FastAPI application, LangChain logic, and database management.
- `capstone/frontend`: React (Vite) dashboard and chatbot interface.
- `database`: SQLite for metadata and ChromaDB for vector storage.
- `tests`: Pytest-based unit testing framework.

---

## 📜 Changelog

Detailed records of all structural and feature updates can be found in the **[Changelog](CHANGELOG.md)**.

---
*Developed for the Automation Engineering program at KMITL.*