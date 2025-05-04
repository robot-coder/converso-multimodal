# README.md

# Web-Based Chat Assistant

This project implements a web-based Chat Assistant that enables users to engage in continuous, themed conversations with selectable Large Language Models (LLMs). The application supports multimedia uploads, model comparisons, and is deployed on Render.com for scalable access.

## Features

- User-friendly web interface for chatting with LLMs
- Select and switch between different LLM models
- Upload and share multimedia files within conversations
- Maintain themed and continuous chat sessions
- Deployable on Render.com for reliable hosting

## Files

- `index.html`: Front-end UI for user interaction
- `app.py`: Back-end API server handling chat logic and multimedia uploads
- `requirements.txt`: Dependencies required for the project
- `README.md`: This documentation

## Setup Instructions

### Prerequisites

- Python 3.8+
- Render account for deployment

### Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Locally

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

Open your browser and navigate to `http://127.0.0.1:8000` to access the chat interface.

### Deployment on Render.com

- Push your code to a GitHub repository.
- Create a new Web Service on Render.
- Connect your repository.
- Set the start command to:

```bash
uvicorn app:app --host=0.0.0.0 --port=10000
```

- Ensure `requirements.txt` is included for dependency installation.

## Usage

- Access the web interface.
- Select your preferred LLM model.
- Upload multimedia files as needed.
- Engage in themed conversations.
- Compare responses across different models.

## Dependencies

Ensure the following libraries are installed:

- fastapi
- uvicorn
- liteLLM
- httpx
- starlette
- pydantic

## License

This project is licensed under the MIT License.

---

**Note:** Replace `<repository_url>` and `<repository_directory>` with your actual repository URL and directory name.