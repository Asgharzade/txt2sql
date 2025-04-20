# TXT2SQL Agent 🤖📊🔍
A natural language to SQL query agent that uses LangChain, OpenAI, and PostgreSQL to convert plain text questions into SQL queries and provide answers.

- 🤖 Text-to-SQL Conversion
- 🔍 Natural Language Query Processing
- 📊 PostgreSQL Database Integration
- 🧠 OpenAI Language Model
- ⚡ High Performance
- 🔐 Secure Database Access
- 📝 Query Explanation
- 💡 Query Improvement Suggestions
- 🔄 Interactive CLI
- 📋 Schema Inspection


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

4. Create a `.env` file and add your credentials based on the `.env.example` file.

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

1. `/help`              - Display this help message
2. `/tables`            - List database tables
3. `/sample customer`   - Show sample data from the customer table
4. `/sample inventory`  - Show sample data from the inventory table
5. `/sql list of working staff with their corresponding number of sales`         - Generate SQL without executing it
6. `top 15 rented movies` - Run the query and get the results
7. `/explain top 15 rented movies` - Explain what a SQL query does

  Any other input will be treated as a natural language query to the database

## Project Structure
```bash
txt2sql/
├── main.py               # Main application entry point
├── src/                  # Source code directory
│   ├── txt2sql_agent.py  # Main agent implementation
│   ├── db_utils.py       # Database utility functions
│   └── system_prompt.txt # System prompt for AI model
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
├── .env.example          # Example environment configuration
├── LICENSE               # MIT license file
├── REALEASE_NOTES.md     # Release notes
├── VERSION               # Version information
├── pyproject.toml        # Python project configuration
├── .python-version       # Python version specification
└── .gitignore            # Git ignore configuration
```

## License
MIT
