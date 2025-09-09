# In file: prompts/source_analysis_prompt.py

# Kept for compatibility with old tests if needed
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

# New prompt for structured output with escaped curly braces
SCHEMA_ANALYSIS_PROMPT_ADVANCED = """
Analyze the database schema provided below. Based on the table and column names, provide a structured analysis in JSON format.

The JSON output should strictly follow this structure:
{{
  "summary": "A brief, one-sentence summary of the database's likely purpose.",
  "key_tables": [
    {{
      "table_name": "string",
      "role": "Fact or Dimension",
      "description": "A short description of this table's purpose."
    }}
  ],
  "relationships": [
    {{
      "from_table": "string",
      "from_column": "string",
      "to_table": "string",
      "to_column": "string",
      "relationship_type": "One-to-Many or Many-to-One"
    }}
  ]
}}

Do not include any text or formatting outside of the main JSON object.

Schema:
```json
{schema_json}
```
"""

