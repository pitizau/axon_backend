# In file: prompts/transformation_prompt.py

TRANSFORMATION_PROMPT = """
Act as an expert database architect. Your task is to convert the provided JSON schema analysis into a complete SQL script containing `CREATE TABLE` statements.

Follow these rules:
1.  Generate a `CREATE TABLE` statement for each table identified in the `key_tables` section.
2.  Use standard SQL data types (e.g., `VARCHAR(255)`, `INTEGER`, `TIMESTAMP`).
3.  Define a primary key for each table, typically the `_id` column (e.g., `customer_id` should be `PRIMARY KEY`).
4.  Add comments to the SQL script to explain each table's purpose.
5.  Do not include any text or formatting outside of the SQL code itself.

Here is the schema analysis:
```json
{schema_analysis_json}
```
"""
