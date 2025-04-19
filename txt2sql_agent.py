from typing import Dict, Any, List, Optional
import time
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Custom prompt template for better SQL generation
SQL_PREFIX = open("system_prompt.txt", "r").read()

class Txt2SqlAgent:
    """
    A class to create and manage a text-to-SQL agent that converts natural language
    to SQL queries and executes them against a PostgreSQL database.
    """
    
    def __init__(self, 
                 db: SQLDatabase, 
                 model: ChatOpenAI,
                 verbose: bool = False):
        """
        Initialize the Txt2SqlAgent with database connection and language model.
        
        Args:
            db: SQLDatabase instance connected to a PostgreSQL database
            model: LangChain ChatOpenAI instance
            verbose: Whether to display verbose output from the agent
        """
        self.db = db
        self.model = model
        self.verbose = verbose
        self.agent = self._create_agent()
        
    def _create_agent(self):
        """Create the SQL agent using LangChain"""
        return create_sql_agent(
            llm=self.model,
            db=self.db,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            prefix=SQL_PREFIX,
            verbose=self.verbose
        )
    
    def query(self, text_input: str) -> Dict[str, Any]:
        """
        Process a natural language query to SQL and return results.
        
        Args:
            text_input: Natural language query
            
        Returns:
            Dict containing the generated SQL, results, and execution information
        """
        start_time = time.time()
        
        try:
            # Run the agent to process the query
            result = self.agent.invoke({"input": text_input})
            
            execution_time = time.time() - start_time
            
            # Return structured result
            return {
                "success": True,
                "output": result["output"],
                "execution_time": execution_time,
                "error": None
            }
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "output": None,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    def generate_sql_only(self, text_input: str) -> str:
        """
        Generate SQL from natural language without executing the query.
        
        Args:
            text_input: Natural language query
            
        Returns:
            str: The generated SQL query
        """
        prompt = PromptTemplate.from_template(
            """Given the following user question, generate a syntactically correct PostgreSQL query.
            Do not execute the query, just return it.
            
            User question: {question}
            
            PostgreSQL query:"""
        )
        
        chain = prompt | self.model | StrOutputParser()
        return chain.invoke({"question": text_input})
    
    def explain_query(self, sql_query: str) -> str:
        """
        Explain what a SQL query does in natural language.
        
        Args:
            sql_query: SQL query to explain
            
        Returns:
            str: Natural language explanation of the query
        """
        prompt = PromptTemplate.from_template(
            """Explain what the following PostgreSQL query does in simple terms:
            
            ```sql
            {query}
            ```
            
            Explanation:"""
        )
        
        chain = prompt | self.model | StrOutputParser()
        return chain.invoke({"query": sql_query})
    
    def suggest_improvements(self, text_input: str, sql_query: str) -> List[str]:
        """
        Suggest improvements for a SQL query based on the original question.
        
        Args:
            text_input: Original natural language query
            sql_query: Generated SQL query
            
        Returns:
            List[str]: List of suggested improvements
        """
        prompt = PromptTemplate.from_template(
            """
            Given the user question and the SQL query generated for it, suggest possible improvements to the query
            that might better address the user's intent or improve performance.
            
            User question: {question}
            
            SQL query: 
            ```sql
            {query}
            ```
            
            List each suggestion separately, numbered 1, 2, 3, etc."""
        )
        
        chain = prompt | self.model | StrOutputParser()
        result = chain.invoke({"question": text_input, "query": sql_query})
        
        # Process into a list of suggestions
        suggestions = [line.strip() for line in result.split("\n") if line.strip()]
        return suggestions