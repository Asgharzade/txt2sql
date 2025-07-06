import streamlit as st
import os
import time
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from src.txt2sql_agent import Txt2SqlAgent
from src.db_utils import test_connection, get_db_info, execute_sample_query
import polars as pl

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Agent",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agent():
    """Initialize the Txt2SqlAgent with caching"""
    try:
        # Load environment variables
        required_vars = ["OPENAI_API_KEY", "OPENAI_MODEL", "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            return None
        
        env_vars = {var: os.getenv(var) for var in required_vars}
        
        # Initialize OpenAI model
        model = ChatOpenAI(
            temperature=0,
            model=env_vars["OPENAI_MODEL"],
            api_key=env_vars["OPENAI_API_KEY"]
        )
        
        # Connect to the database
        db_uri = f"postgresql://{env_vars['DB_USER']}:{env_vars['DB_PASSWORD']}@{env_vars['DB_HOST']}:{env_vars['DB_PORT']}/{env_vars['DB_NAME']}"
        db = SQLDatabase.from_uri(db_uri)
        
        # Test database connection
        if not test_connection(db):
            st.error("Could not connect to the database. Please check your connection settings.")
            return None
        
        # Create the agent
        agent = Txt2SqlAgent(db, model, verbose=False)
        return agent, db
        
    except Exception as e:
        st.error(f"Error initializing agent: {e}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🗄️ Text-to-SQL Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Convert natural language to SQL queries and explore your database</p>', unsafe_allow_html=True)
    
    # Initialize agent
    agent_data = initialize_agent()
    if agent_data is None:
        st.stop()
    
    agent, db = agent_data
    
    # Sidebar for database information
    with st.sidebar:
        st.header("📊 Database Info")
        
        # Get database information
        try:
            db_info = get_db_info(db)
            st.metric("Tables", len(db_info["tables"]))
            
            st.subheader("Available Tables")
            for table in db_info["tables"]:
                if st.button(f"📋 {table}", key=f"table_{table}"):
                    st.session_state.selected_table = table
            
            if "selected_table" in st.session_state:
                st.info(f"Selected: {st.session_state.selected_table}")
                if st.button("Show Sample Data"):
                    try:
                        sample_data = execute_sample_query(db, st.session_state.selected_table)
                        df = pl.DataFrame(sample_data)
                        st.dataframe(df.to_pandas(), use_container_width=True)
                    except Exception as e:
                        st.error(f"Error retrieving sample data: {e}")
                        
        except Exception as e:
            st.error(f"Error getting database info: {e}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Natural Language Query")
        
        # Query input
        query = st.text_area(
            "Enter your question in natural language:",
            placeholder="e.g., Show me all users who signed up in the last month",
            height=100
        )
        
        # Query options
        col1_1, col1_2, col1_3 = st.columns(3)
        
        with col1_1:
            execute_query = st.button("🚀 Execute Query", type="primary", use_container_width=True)
        
        with col1_2:
            generate_sql_only = st.button("🔧 Generate SQL Only", use_container_width=True)
        
        with col1_3:
            explain_mode = st.button("📖 Explain Query", use_container_width=True)
    
    with col2:
        st.header("⚙️ Options")
        
        # Advanced options
        st.subheader("Query Settings")
        show_sql = st.checkbox("Show generated SQL", value=True)
        show_execution_time = st.checkbox("Show execution time", value=True)
        
        st.subheader("Quick Examples")
        examples = [
            "Show me the top 10 customers by order value",
            "Find all products with low stock (less than 10 units)",
            "Calculate total sales by month for this year",
            "List employees who joined in the last 6 months"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{example[:20]}"):
                st.session_state.query_text = example
                st.rerun()
    
    # Handle query input from examples
    if "query_text" in st.session_state:
        query = st.session_state.query_text
        del st.session_state.query_text
    
    # Process queries
    if query:
        if execute_query:
            with st.spinner("Processing your query..."):
                try:
                    start_time = time.time()
                    result = agent.query(query)
                    execution_time = time.time() - start_time
                    
                    if result["success"]:
                        st.markdown('<div class="success-message">✅ Query executed successfully!</div>', unsafe_allow_html=True)
                        
                        # Display results
                        st.subheader("📊 Results")
                        st.write(result["output"])
                        
                        if show_execution_time:
                            st.metric("Execution Time", f"{execution_time:.2f}s")
                            
                    else:
                        st.markdown('<div class="error-message">❌ Query failed</div>', unsafe_allow_html=True)
                        st.error(f"Error: {result['error']}")
                        
                except Exception as e:
                    st.error(f"Error processing query: {e}")
        
        elif generate_sql_only:
            with st.spinner("Generating SQL..."):
                try:
                    sql = agent.generate_sql_only(query)
                    
                    st.markdown('<div class="info-message">🔧 SQL Generated Successfully</div>', unsafe_allow_html=True)
                    st.subheader("Generated SQL")
                    
                    # Use st.code for better SQL formatting
                    st.code(sql, language="sql")
                    
                    # Add copy button functionality
                    st.button("📋 Copy SQL", on_click=lambda: st.write("SQL copied to clipboard!"))
                    
                except Exception as e:
                    st.error(f"Error generating SQL: {e}")
        
        elif explain_mode:
            with st.spinner("Explaining query..."):
                try:
                    # First generate SQL
                    sql = agent.generate_sql_only(query)
                    
                    st.subheader("Generated SQL")
                    st.code(sql, language="sql")
                    
                    # Then explain it
                    explanation = agent.explain_query(sql)
                    
                    st.subheader("📖 Explanation")
                    st.markdown(explanation)
                    
                except Exception as e:
                    st.error(f"Error explaining query: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ using Streamlit and LangChain</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 