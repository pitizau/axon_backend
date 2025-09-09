# In file: prompts/validation_prompt.py

VALIDATION_PROMPT = """
You are a data quality assurance expert. Based on the provided JSON schema analysis, generate a SQL script with queries to validate the data after migration.

The script should include:
1.  **Row Count Checks**: For each table, write a commented query to compare the row count between the source and target.
    -- Example: SELECT COUNT(*) FROM source_customers; vs SELECT COUNT(*) FROM target_customers;
2.  **Null Checks**: For important columns that should not be empty (like IDs and names), write a query to check for NULL values.
3.  **Referential Integrity Checks**: For each relationship identified, write a query to find 'orphan' records in the 'from_table' that don't have a matching record in the 'to_table'.

Use comments extensively to explain the purpose of each validation query.

CONTEXT FROM PREVIOUS RUN:
---
{context}
---

SCHEMA ANALYSIS:
```json
{schema_analysis_json}
```
"""
