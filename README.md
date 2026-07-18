# CV-Job Matcher

An AI-powered application that analyzes job descriptions and compares them against a candidate's CV to provide detailed matching insights using Server-Sent Events (SSE) streaming.

## Features

- **AI-Powered Matching**: Uses LLM via LM Studio (OpenAI-compatible API) to analyze compatibility between jobs and CVs
- **Streaming Response**: Returns real-time token-by-token analysis via SSE
- **Detailed Analysis**: Provides match percentages, missing skills, and scoring reasons
- **JSON Output**: Final result is structured JSON data for easy integration
- **Browser Extension Support**: Includes a browser extension for seamless job application workflow
- **CV Caching**: Automatically caches extracted CV data to avoid redundant processing
- **Job Data Persistence**: Saves extracted job information to `data/job_data.json`

## How It Works

1. The system checks if a CV cache file exists and is valid
2. If no valid cache, extracts information from the CV (skills, experience, projects, education) and saves it to `cv_cache.json`
3. Extracts job description data and saves it to `data/job_data.json`
4. Compares extracted CV data against the job description using AI analysis via LangGraph workflow
5. Calculates match percentage and identifies missing skills
6. Returns structured analysis in SSE format with real-time token streaming

## API Endpoints

### GET `/`
Returns a welcome message confirming the server is running.

### POST `/job`
Accepts job information, extracts and saves it to `data/job_data.json`, then returns matching analysis via Server-Sent Events (SSE).

**Request Body:**
```json
{
  "url": "string",
  "title": "string",
  "description": "string"
}
```

**Response Format (Server-Sent Events):**
```
event: token
data: {"token": "..."}

event: token
data: {"token": "..."}

...

event: done
data: {"processing_time_sec": 1.23}
```

**Note:** The endpoint streams tokens in real-time as the AI generates the analysis. The final result includes match percentage, matching skills, missing skills, and score reason. Job data is automatically saved to `data/job_data.json` after extraction. CV data is cached from `cv_cache.json` if available.

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

```bash
python main.py
# or
python -m uvicorn main:app --reload
```

The server will start on `http://localhost:8000` by default.

## Data Files

- **cv_cache.json**: Cached CV data (skills, experience, projects, education) in the project root - avoids re-extraction
- **data/job_data.json**: Extracted job information saved after each `/job` request

## Requirements

- Python 3.8+
- LM Studio running locally (for LLM inference via OpenAI-compatible API)
- Qwen model configured in LM Studio at port 1234

## Dependencies

- **fastapi**: Web framework for the API server
- **pydantic**: Data validation and settings management
- **uvicorn**: ASGI server to run FastAPI applications
- **langchain-core**: Core LangChain functionality
- **langgraph**: Workflow orchestration with state management
- **pypdf**: PDF file parsing
- **python-docx**: Word document processing

## Browser Extension

The project includes a browser extension that integrates with the API:

- `job-extension/manifest.json`: Extension manifest configuration
- `job-extension/content.js`: Content script for page interaction
- `job-extension/modal/modal_window.js`: Modal window UI component

## Architecture

```
├── main.py              # FastAPI server entry point with SSE streaming
├── requirements.txt     # Python dependencies
├── cv_extractor/        # CV extraction module
│   └── extractor.py    # CV parsing logic and caching
├── LangChain/           # AI analysis components
│   ├── chain.py        # Chain orchestration
│   ├── llm.py          # LLM configuration (OpenAI-compatible)
│   └── prompt.py       # Prompt templates
├── graph/               # LangGraph workflow state management
│   ├── graph.py        # Graph definition
│   ├── nodes.py        # Node functions (extract_cv, extract_job, match)
│   ├── routers.py      # Route handlers with cache validation
│   └── state.py        # TypedDict for workflow state
├── job-extension/       # Browser extension files
├── data/                # Data storage directory
│   ├── cv_cache.json   # Cached CV extraction results
│   └── job_data.json   # Extracted job information
└── README.md            # This file
```

## Configuration

The LLM is configured to use LM Studio's OpenAI-compatible API:
- Base URL: `http://127.0.0.1:1234/v1`
- Model: Qwen (configured in LM Studio)
- API Key: `lm-studio`
- Temperature: 0.2 (for more deterministic responses)
- Max Tokens: 4000

## Usage Example

```bash
curl -X POST http://localhost:8000/job \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/job",
    "title": "Software Engineer",
    "description": "Looking for Python developer with AWS experience..."
  }'
```

**Note:** After the first request, CV data will be cached in `cv_cache.json` and job data saved to `data/job_data.json`. Subsequent requests will use these cached files. The response streams tokens in real-time via SSE format.

## License

MIT License
