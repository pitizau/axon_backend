# In file: prompts/planning_prompt.py

MIGRATION_PLAN_PROMPT = """
You are a database migration strategist. Based on the following JSON schema analysis, create a high-level, step-by-step migration plan in Markdown format.

The plan should include the following sections:
- **## 1. Executive Summary**: A brief overview of the migration goals.
- **## 2. Pre-Migration Steps**: Key actions to take before starting, like backups and environment setup.
- **## 3. Migration Sequence**: The recommended order for migrating tables, prioritizing dimension tables before fact tables. Justify your ordering.
- **## 4. Post-Migration Validation**: Steps to verify the migration was successful, such as data validation and integrity checks.

Here is the schema analysis:
```json
{schema_analysis_json}
```
"""
