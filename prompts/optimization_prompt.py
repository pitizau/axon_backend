# In file: prompts/optimization_prompt.py

OPTIMIZATION_PROMPT = """
You are an expert database performance tuning specialist. Review the provided `CREATE TABLE` SQL script and its corresponding schema analysis.

Your task is to generate a new SQL script that provides recommendations for performance optimization. The script should primarily focus on:
1.  **Adding Indexes**: Identify all foreign key columns from the schema analysis and suggest creating indexes on them to speed up join operations.
2.  **General Recommendations**: Add commented-out suggestions for other potential optimizations, such as partitioning large fact tables (like 'orders') by date.

Use comments to explain why each index or optimization is beneficial.

CONTEXT FROM PREVIOUS RUN:
---
{context}
---

ORIGINAL SCHEMA ANALYSIS:
```json
{schema_analysis_json}
```

GENERATED `CREATE TABLE` SCRIPT:
```sql
{generated_sql}
```
"""
