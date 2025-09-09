# In file: prompts/source_analysis_prompt.py

SCHEMA_ANALYSIS_PROMPT = """
Analyze the following database schema provided in JSON format.
Your analysis should include:
1.  A high-level summary of the database's purpose.
2.  An identification of key tables and their likely roles (e.g., fact, dimension).
3.  An analysis of potential relationships between tables based on column names (e.g., foreign key relationships).
4.  Any potential data quality or design issues you notice.

Schema:
{schema_json}
"""