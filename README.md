# React Agent

A Python library for building reactive AI agents using LangChain, LangGraph, and OpenAI.

## Overview

React Agent provides a framework for creating intelligent agents that can process data, interact with AI models, and perform complex reasoning tasks. Built on top of LangChain and LangGraph, it offers a powerful toolkit for developing agent-based applications.


## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key

## Installation

### 1. Clone or Initialize the Project

```bash
# Navigate to your desired directory
cd ~/Documents

# Initialize the project with uv
uv init 
rm main.py
```

### 2. Set Up Project Structure

```bash
# Create configuration files
touch .flake8 .env
```

### 3. Activate Virtual Environment

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
# Install development dependencies
uv add --dev pytest ruff jupyter

# Install project dependencies
uv add python-dotenv langchain langchain-openai langgraph pandas numpy langchain-qdrant langfuse gradio fastembed langchain-text-splitters matplotlib torch seaborn umap-learn tiktoken
```

## Configuration

### Flake8 Configuration

Create or update `.flake8` with the following content:

```ini
[flake8]
max-line-length = 120
```

### Environment Variables

Create a `.env` file in the project root and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

**Important:** Never commit your `.env` file to version control. Ensure it's listed in `.gitignore`.

## Project Structure

```
react-agent/
├── src/
│   └── react_agent/
│       ├── __init__.py
│       └── py.typed
├── tests/
│   └── __init__.py
├── .flake8
├── .env
├── pyproject.toml
├── uv.lock
└── README.md
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting and Linting

```bash
# Run ruff linter
ruff check .

# Format code with ruff
ruff format .
```



[Optional]
pair to github project
# Initialize git if you haven't already
git init

# Add all your files
git add .

# Make your first commit
git commit -m "Initial commit: React agent project structure"

# Add the GitHub repo as remote origin
git remote add origin https://github.com/YOUR_USERNAME/react-agent-exercise.git

# Push to GitHub
git branch -M main
git push -u origin main