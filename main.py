import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from src.txt2sql_agent import Txt2SqlAgent
from src.db_utils import test_connection, get_db_info, execute_sample_query
import polars as pl
load_dotenv()

def load_environment():
    """Load environment variables from .env file"""
    
    required_vars = ["OPENAI_API_KEY", "OPENAI_MODEL", "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")    
    return {var: os.getenv(var) for var in required_vars}

def get_db_connection_string(env_vars):
    """Create database connection string from environment variables"""
    return f"postgresql://{env_vars['DB_USER']}:{env_vars['DB_PASSWORD']}@{env_vars['DB_HOST']}:{env_vars['DB_PORT']}/{env_vars['DB_NAME']}"


def display_commands():
    """Display available commands for the CLI"""
    print("\nAvailable commands:")
    print("  /help           - Display this help message")
    print("  /exit           - Exit the application")
    print("  /tables         - List database tables")
    print("  /sample TABLE   - Show sample data from a table")
    print("  /sql            - Generate SQL without executing it")
    print("  /explain QUERY  - Explain what a SQL query does")
    print("  Any other input will be treated as a natural language query to the database")


def main():
    print("Starting txt2sql agent...")
    
    try:
        # Load environment variables
        env_vars = load_environment()
        
        # Initialize OpenAI model
        model = ChatOpenAI(
            temperature=0,
            model=env_vars["OPENAI_MODEL"],
            api_key=env_vars["OPENAI_API_KEY"]
        )
        
        # Connect to the database
        db_uri = get_db_connection_string(env_vars)
        db = SQLDatabase.from_uri(db_uri)
        
        # Test database connection
        if not test_connection(db):
            print("Error: Could not connect to the database. Please check your connection settings.")
            return
        
        # Create the agent
        agent = Txt2SqlAgent(db, model, verbose=True)
        
        print("Database connected successfully.")
        display_commands()
        
        # Interactive query loop
        while True:
            query = input("\nEnter query or command: ")
            
            # Handle exit command
            if query.lower() in ("/exit", "/quit"):
                print("Exiting...")
                break
            
            # Handle help command
            elif query.lower() == "/help":
                display_commands()
                continue
            
            # Handle tables command
            elif query.lower() == "/tables":
                print("\nDatabase Tables:")
                db_info = get_db_info(db)
                for table in db_info["tables"]:
                    print(f"- {table}")
                continue
            
            # Handle sample command
            elif query.lower().startswith("/sample "):
                table = query[8:].strip()
                try:
                    sample_data = execute_sample_query(db, table)
                    print(f"\nSample data from {table}:")
                    print(pl.DataFrame(sample_data))
                    # for row in sample_data:
                    #     print(row)
                except Exception as e:
                    print(f"Error retrieving sample data: {e}")
                continue
                
            # Handle SQL-only generation
            elif query.lower().startswith("/sql "):
                nl_query = query[5:].strip()
                try:
                    sql = agent.generate_sql_only(nl_query)
                    print("\nGenerated SQL:")
                    print(sql)
                except Exception as e:
                    print(f"Error generating SQL: {e}")
                continue
                
            # Handle explain command
            elif query.lower().startswith("/explain "):
                sql_query = query[9:].strip()
                try:
                    explanation = agent.explain_query(sql_query)
                    print("\nExplanation:")
                    print(explanation)
                except Exception as e:
                    print(f"Error explaining query: {e}")
                continue
            
            # Process natural language query
            else:
                try:
                    start_time = time.time()
                    result = agent.query(query)
                    duration = time.time() - start_time
                    
                    print("\nResult:")
                    if result["success"]:
                        print(result["output"])
                    else:
                        print(f"Error: {result['error']}")
                    
                    print(f"\nQuery completed in {duration:.2f} seconds")
                    print("-----------")
                    print("/help  - Display this help message")
                except Exception as e:
                    print(f"Error processing query: {e}")
    
    except Exception as e:
        print(f"Error initializing txt2sql agent: {e}")


if __name__ == "__main__":
    main()
