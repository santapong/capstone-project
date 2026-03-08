# Project Setup Guide

Follow these steps to get the CapStone-Project up and running on your local machine.

## Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18 or higher
- **uv**: Python package manager (recommended)
- **Ollama**: For local LLM processing (if using local models)

---

## 1. Backend Setup

### A. Clone and Prepare
```bash
git clone <repository-url>
cd capstone-project
```

### B. Environment Configuration
Create a `.env` file from the example:
```bash
cp .envExample .env
```
Update the following critical variables in `.env`:
- `TYPHOON_API_KEY`: Your API key for the Typhoon LLM.
- `LANGSMITH_API_KEY`: (Optional) For tracing and debugging.
- `PYTHONPATH`: Set to `.` (the current directory).

### C. Install Dependencies
Using `uv`:
```bash
uv sync
```

### D. Initialize Database
The database tables are automatically initialized on the first run of the application.

### E. Start the Backend
```bash
uv run python capstone/backend/app.py
```
The API will be available at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.

---

## 2. Frontend Setup

### A. Navigate to Frontend
```bash
cd capstone/frontend
```

### B. Install Dependencies
```bash
npm install
```

### C. Start the Frontend
```bash
npm run dev
```
The frontend will be available at `http://localhost:5173`.

## 3. External API Setup

### A. Google Custom Search Engine (CSE)
This project uses Google CSE for web-enhanced RAG. Follow these steps to obtain the required keys:

1. **Google Cloud API Key**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Navigate to **APIs & Services > Credentials**.
   - Click **Create Credentials > API Key**.
   - Copy the key and add it to `.env` as `GOOGLE_API_KEY`.
   - **Crucial**: Enable the "Custom Search API" in the [API Library](https://console.cloud.google.com/apis/library/customsearch.googleapis.com).

2. **Google Custom Search Engine ID (CX)**:
   - Go to the [Programmable Search Engine dashboard](https://programmablesearchengine.google.com/).
   - Click **Add** to create a new search engine.
   - Name your search engine and select "Search the entire web" (or specific sites if preferred).
   - Once created, go to **Overview** and copy the **Search engine ID**.
   - Add it to `.env` as `GOOGLE_CSE_ID`.

---

## 4. Running Tests

To verify the installation, run the automated test suite from the project root:
```bash
PYTHONPATH=. uv run pytest
```

## Troubleshooting

- **ModuleNotFoundError**: Ensure `PYTHONPATH=.` is set when running commands from the root.
- **Database Errors**: Check that the `database/history_database` directory exists and is writable.
- **API Connection**: Ensure the `VITE_API_URL` in the frontend (or defaults) matches your backend address.
