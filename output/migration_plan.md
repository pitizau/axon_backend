
        ```json
        {
          "summary": "This is a dummy analysis of a customer and orders database.",
          "key_tables": [
            {
              "table_name": "customers",
              "role": "Dimension",
              "description": "Stores customer information."
            },
            {
              "table_name": "orders",
              "role": "Fact",
              "description": "Stores order information, linking to customers."
            }
          ],
          "relationships": [
            {
              "from_table": "orders",
              "from_column": "customer_id",
              "to_table": "customers",
              "to_column": "customer_id",
              "relationship_type": "Many-to-One"
            }
          ]
        }
        ```
        