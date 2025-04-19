# TXT2SQL Agent
🤖 Text-to-SQL Conversion
🔍 Natural Language Query Processing
📊 PostgreSQL Database Integration
🧠 OpenAI Language Model
⚡ High Performance
🔐 Secure Database Access
📝 Query Explanation
💡 Query Improvement Suggestions
🔄 Interactive CLI
📋 Schema Inspection

A natural language to SQL query agent that uses LangChain, OpenAI, and PostgreSQL to convert plain text questions into SQL queries and provide answers.

## Features
- Convert natural language questions to SQL queries
- Execute queries against a PostgreSQL database
- Generate SQL without executing it
- Explain SQL queries in plain language
- View database schema and sample data
- Interactive command-line interface

## Requirements

- Python 3.8 or higher
- PostgreSQL database
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/txt2sql.git
cd txt2sql
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your credentials with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o #(default model)
DB_HOST=localhost #(if you are using a local database)
DB_PORT=5432 #(default port for PostgreSQL)
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

## Usage

Run the application:

```bash
python main.py
```

### Available Commands

- `/help` - Display help information
- `/exit` - Exit the application
- `/tables` - List all tables in the database
- `/sample TABLE` - Show sample data from the specified table
- `/sql QUERY` - Generate SQL for a natural language query without executing it
- `/explain QUERY` - Explain what a SQL query does in plain language
- Any other input is treated as a natural language query to be processed

## Example Usage



## Project Structure





- `main.py` - Main application entry point
- `txt2sql_agent.py` - Txt2SqlAgent implementation
- `db_utils.py` - Database utility functions
- `requirements.txt` - Project dependencies
- `.env.example` - Example environment configuration

## License

MIT
