# SQL Code Quality Improvement Tool

## Overview
**ref[AI]ne** is an AI-powered SQL Code Quality Improvement Tool designed to help developers enhance their SQL queries by fixing syntax errors, optimizing performance, standardizing code, and generating documentation. This tool integrates **Streamlit** for an interactive UI and **FastAPI** as a backend service powered by AWS Bedrock's Claude AI model.

## Features
- **Fix Syntax Errors**: Automatically detects and corrects SQL syntax errors.
- **Standardize Code**: Formats SQL queries according to best practices.
- **Optimize SQL Queries**: Enhances query performance by suggesting optimizations.
- **Generate Documentation**: Creates documentation for SQL queries.

## Tech Stack
- **Python**
- **Streamlit** (Frontend UI)
- **FastAPI** (Backend API Service)
- **AWS Bedrock Claude AI** (AI Model for SQL Analysis)
- **Boto3** (AWS SDK for Python)
- **Uvicorn** (ASGI Server)
- **Requests** (For API Calls)

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Pip (Python Package Manager)
- AWS Credentials Configured (`~/.aws/credentials`)

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/sql-code-quality-tool.git
   cd sql-code-quality-tool
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the FastAPI backend:**
   ```bash
   python main.py
   ```
4. **Run the Streamlit UI:**
   ```bash
   streamlit run app.py
   ```

## Usage
1. Paste your SQL query in the input box.
2. Click any of the buttons:
   - **Fix Syntax Errors**
   - **Standardize Code**
   - **Optimize SQL Code**
   - **Generate Documentation**
3. View the improved SQL output in the result area.

## API Endpoints
| Endpoint           | Method | Description |
|--------------------|--------|-------------|
| `/fix_syntax/`    | POST   | Fixes SQL syntax errors |
| `/standardize/`   | POST   | Standardizes SQL code |
| `/optimize/`      | POST   | Optimizes SQL queries |
| `/document/`      | POST   | Generates documentation for SQL code |

## Future Enhancements
- VS Code Extension for real-time SQL improvements
- Support for multiple SQL dialects (MySQL, PostgreSQL, etc.)
---
🚀 **Contributions & feedback are welcome!**

