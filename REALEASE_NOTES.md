# Release Notes

## [0.1.0] - 2025-04-19

### Added
- Initial release of TXT2SQL Agent
- Natural language to SQL query conversion using LangChain and OpenAI
- PostgreSQL database integration with secure connection handling
- Interactive CLI with commands for:
  - Viewing database tables
  - Sampling table data
  - Generating SQL without execution
  - Explaining SQL queries
  - Running natural language queries
- Environment configuration via .env file
- Database connection testing and validation
- Error handling for missing environment variables and failed connections
- Query result formatting and display
- Basic documentation and usage instructions
- Built with Python 3.8+
- Uses GPT-4o model for natural language processing
- Implements LangChain framework for AI agent capabilities
- PostgreSQL database connectivity
- Environment variable management with python-dotenv

### Known Limitations
- Limited to PostgreSQL databases only
- Requires OpenAI API key
- Query results capped at 10 rows by default
- No support for database modifications (INSERT, UPDATE, DELETE)
