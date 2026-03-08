# CapStone-Project: Automation Gen AI

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/)

An advanced Automation-focused Generative AI system designed to provide expert knowledge in Automation Engineering at KMITL. This project leverages an Agentic RAG (Retrieval-Augmented Generation) architecture to deliver accurate, refined, and context-aware answers.

## 🚀 Key Features

- **Agentic RAG**: Implements a sophisticated LangGraph workflow for intelligent document retrieval and answer refinement.
- **Multi-Source Knowledge**: Combines local vector database (ChromaDB) retrieval with live web searching (Google/DuckDuckGo) when local data is insufficient.
- **Smart Grading**: Automatically evaluates the relevance of retrieved documents before generating answers.
- **Integrated Dashboard**: Monitor system performance, query logs, and time usage.
- **Document Management**: Manage and process knowledge source documents for the RAG system.
- **Modern UI**: A responsive and intuitive frontend built with React and Vite.

## 🏗️ Architecture

The backend utilizes **LangGraph** to manage the AI's decision-making process:
1. **Retrieval**: Searches the local vector store for relevant Automation Engineering documents.
2. **Grading**: Uses an LLM to determine if the retrieved context is sufficient.
3. **Web Search**: If context is missing, the agent triggers a web search (Google/DuckDuckGo).
4. **Generation**: Synthesizes a comprehensive answer from all available sources.
5. **Refinement**: Polishes the final response for clarity and technical accuracy.

![Workflow](/imgs/Workflow.png)

## 🛠️ Tech Stack

- **Backend**: FastAPI, LangChain, LangGraph, Uvicorn, SQLAlchemy.
- **Frontend**: React, Vite, Tailwind CSS (optional), NPM.
- **AI/ML**: Ollama (Local Embeddings/LLMs), OpenTyphoon (Cloud LLM), Google Search API.
- **Database**: SQLite (Logs/Management), ChromaDB (Vector Store).
- **Environment**: UV (Fast Python package manager).

## 📥 Getting Started

### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js & NPM](https://nodejs.org/en)
- [Ollama](https://ollama.com/download)
- [UV](https://docs.astral.sh/uv/getting-started/installation/) (Recommended for backend)

### 1. Clone the Repository

```bash
git clone https://github.com/santapong/CapStone-Project.git
cd CapStone-Project
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory based on `.envExample`:

```env
PYTHONPATH="."
LANGSMITH_API_KEY="your_key"
TYPHOON_API_KEY="your_key"
GOOGLE_CSE_ID="your_google_custom_search_engine_id"
GOOGLE_API_KEY="your_google_api_key"
LLM_MODEL="typhoon-v1.5x-70b-instruct"
MODEL_PROVIDER="openai"
MODEL_BASE_URL="https://api.opentyphoon.ai/v1"
EMBEDDING_MODEL="bge-m3"
```

### 3. Backend Setup

Synchronize dependencies using `uv`:

```bash
uv sync --no-group dev
```

Setup Ollama embeddings:
```bash
ollama pull bge-m3
```

Run the backend server:
```bash
cd capstone/backend
python app.py
```

### 4. Frontend Setup

```bash
cd capstone/frontend
npm install
npm run dev
```

## 📝 Usage

1. Open the frontend at `http://localhost:5173`.
2. Access the API documentation at `http://localhost:8000/docs`.
3. Use the management page to upload new documents for the RAG system.

## ❤️ Credits

- [Typhoon AI](https://opentyphoon.ai/) - LLM Provider.
- [Prompt Engineer Guide](https://www.promptingguide.ai/) - Learning resources.
- [LangChain](https://python.langchain.com/) - Framework for LLM development.

---
Developed as part of the Capstone project in Automation Engineering.