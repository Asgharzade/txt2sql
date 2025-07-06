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
- 🌐 Modern Web UI
- 📋 Schema Inspection


## Features
- Convert natural language questions to SQL queries
- Execute queries against a PostgreSQL database
- Generate SQL without executing it
- Explain SQL queries in plain language
- View database schema and sample data
- Interactive command-line interface
- **NEW: Beautiful web interface with Streamlit**

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

4. Create a `.env` file in the project root and add your credentials:
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

## Usage

### Web UI (Recommended) 🌐

Launch the modern web interface using one of these methods:

**Method 1: Using the launcher script (Recommended)**
```bash
python run_ui.py
```

**Method 2: Direct Streamlit command**
```bash
streamlit run app.py
```

**Method 3: With custom port and settings**
```bash
streamlit run app.py --server.port 8501 --server.address localhost
```

The UI will automatically open in your browser at `http://localhost:8501`

**Web UI Features:**
- 🎨 Modern, responsive design with beautiful styling
- 📊 Real-time database schema exploration in the sidebar
- 🔧 Multiple query modes:
  - **Execute Query**: Run queries and see results
  - **Generate SQL Only**: View generated SQL without execution
  - **Explain Query**: Get plain-language explanations of SQL
- 📋 Quick example queries for common use cases
- 📈 Execution time tracking and performance metrics
- 🎯 Interactive table selection and sample data viewing
- 📱 Mobile-friendly responsive design
- 🔄 Session state management for better UX
- 📋 Copy-to-clipboard functionality for SQL queries

**Web UI Navigation:**
- **Main Area**: Enter natural language queries and view results
- **Sidebar**: Explore database tables, view schema info, and see sample data
- **Options Panel**: Configure query settings and access quick examples

### Command Line Interface 💻

Run the traditional CLI:

```bash
python main.py
```

### Available Commands (CLI)

- `/help` - Display help information
- `/exit` - Exit the application
- `/tables` - List all tables in the database
- `/sample TABLE` - Show sample data from the specified table
- `/sql QUERY` - Generate SQL for a natural language query without executing it
- `/explain QUERY` - Explain what a SQL query does in plain language
- Any other input is treated as a natural language query to be processed

## Example Usage

### Web UI Examples:
1. **Basic Query**: Enter "Show me all users who signed up in the last month" and click "Execute Query"
2. **SQL Generation**: Enter "Find products with low stock" and click "Generate SQL Only" to see the SQL
3. **Query Explanation**: Enter "Calculate total sales by month" and click "Explain Query" to understand the SQL
4. **Schema Exploration**: Use the sidebar to browse tables and view sample data
5. **Quick Examples**: Click any example button to instantly populate the query field

### CLI Examples:
1. `/help`              - Display this help message
2. `/tables`            - List database tables
3. `/sample customer`   - Show sample data from the customer table
4. `/sample inventory`  - Show sample data from the inventory table
5. `/sql list of working staff with their corresponding number of sales`         - Generate SQL without executing it
6. `top 15 rented movies` - Run the query and get the results
7. `/explain top 15 rented movies` - Explain what a SQL query does

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

**Required Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key (get from https://platform.openai.com/)
- `OPENAI_MODEL`: The OpenAI model to use (default: gpt-4)
- `DB_HOST`: PostgreSQL database host
- `DB_PORT`: PostgreSQL database port (default: 5432)
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL database username
- `DB_PASSWORD`: PostgreSQL database password

## Troubleshooting

### Common Issues:

1. **Streamlit not found**: Install with `pip install streamlit`
2. **Database connection failed**: Check your `.env` file and database credentials
3. **OpenAI API errors**: Verify your API key and model name
4. **Port already in use**: Change the port with `--server.port 8502`

### Getting Help:
- Check the console output for error messages
- Verify all environment variables are set correctly
- Ensure your PostgreSQL database is running and accessible
- Make sure you have sufficient OpenAI API credits

## Project Structure
```bash
txt2sql/
├── app.py               # Streamlit web application
├── run_ui.py            # UI launcher script
├── main.py              # CLI application entry point
├── src/                 # Source code directory
│   ├── txt2sql_agent.py # Main agent implementation
│   ├── db_utils.py      # Database utility functions
│   └── system_prompt.txt # System prompt for AI model
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation
├── .env                 # Environment configuration (create this)
├── LICENSE              # MIT license file
├── REALEASE_NOTES.md    # Release notes
├── VERSION              # Version information
├── pyproject.toml       # Python project configuration
├── .python-version      # Python version specification
└── .gitignore           # Git ignore configuration
```

## Dependencies

The project uses the following key dependencies:
- `streamlit>=1.28.0` - Web UI framework
- `streamlit-ace>=0.1.1` - Code editor component
- `langchain>=0.1.0` - LLM framework
- `langchain-openai>=0.0.2` - OpenAI integration
- `openai>=1.10.0` - OpenAI API client
- `psycopg2-binary>=2.9.9` - PostgreSQL adapter
- `python-dotenv>=1.0.0` - Environment variable management
- `SQLAlchemy>=2.0.23` - Database ORM
- `polars>=0.19.1` - Fast data processing

## License
MIT
