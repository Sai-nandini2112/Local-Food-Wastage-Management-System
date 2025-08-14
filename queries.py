import sqlite3
import pandas as pd

# Load cleaned CSVs
providers = pd.read_csv("providers_clean.csv")
receivers = pd.read_csv("receivers_clean.csv")
food_listings = pd.read_csv("food_listings_clean.csv")
claims = pd.read_csv("claims_clean.csv")

# Create SQLite DB
db_name = "food_waste.db"
conn = sqlite3.connect(db_name)

# Save each dataframe as a table
providers.to_sql("providers", conn, if_exists="replace", index=False)
receivers.to_sql("receivers", conn, if_exists="replace", index=False)
food_listings.to_sql("food_listings", conn, if_exists="replace", index=False)
claims.to_sql("claims", conn, if_exists="replace", index=False)

conn.close()
print(f"Database '{db_name}' created and populated successfully.")


import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("food_waste.db")

# Dictionary of queries
queries = {
    "providers_per_city": """
        SELECT city, COUNT(*) AS providers_count
        FROM providers
        GROUP BY city
        ORDER BY providers_count DESC
    """,
    "receivers_per_city": """
        SELECT city, COUNT(*) AS receivers_count
        FROM receivers
        GROUP BY city
        ORDER BY receivers_count DESC
    """,
    "provider_type_most_food": """
        SELECT provider_type, SUM(quantity) AS total_quantity
        FROM food_listings
        GROUP BY provider_type
        ORDER BY total_quantity DESC
    """,
    "provider_contacts_in_hyderabad": """
        SELECT name, type, contact
        FROM providers
        WHERE city = 'Hyderabad'
    """,
    "top_receivers_by_completed_qty": """
        SELECT r.receiver_id, r.name, SUM(fl.quantity) AS total_quantity_claimed
        FROM claims c
        JOIN receivers r ON r.receiver_id = c.receiver_id
        JOIN food_listings fl ON fl.food_id = c.food_id
        WHERE c.status = 'Completed'
        GROUP BY r.receiver_id, r.name
        ORDER BY total_quantity_claimed DESC
    """,
    "total_non_expired_qty": """
        SELECT SUM(quantity) AS total_available_non_expired
        FROM food_listings
        WHERE DATE(expiry_date) >= DATE('now')
    """,
    "city_with_most_listings": """
        SELECT location AS city, COUNT(*) AS listings_count
        FROM food_listings
        GROUP BY location
        ORDER BY listings_count DESC
    """,
    "most_common_food_types": """
        SELECT food_type, COUNT(*) AS cnt
        FROM food_listings
        GROUP BY food_type
        ORDER BY cnt DESC
    """,
    "claims_per_food_item": """
        SELECT fl.food_id, fl.food_name, COUNT(c.claim_id) AS claims_count
        FROM food_listings fl
        LEFT JOIN claims c ON c.food_id = fl.food_id
        GROUP BY fl.food_id, fl.food_name
        ORDER BY claims_count DESC
    """,
    "provider_with_most_completed_claims": """
        SELECT p.provider_id, p.name, COUNT(*) AS completed_claims
        FROM claims c
        JOIN food_listings fl ON fl.food_id = c.food_id
        JOIN providers p ON p.provider_id = fl.provider_id
        WHERE c.status = 'Completed'
        GROUP BY p.provider_id, p.name
        ORDER BY completed_claims DESC
    """,
    "claims_percentage_by_status": """
        SELECT status,
               ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) AS pct
        FROM claims
        GROUP BY status
        ORDER BY pct DESC
    """,
    "avg_quantity_per_receiver": """
        SELECT r.receiver_id, r.name,
               ROUND(AVG(fl.quantity), 2) AS avg_quantity_per_claim
        FROM claims c
        JOIN receivers r ON r.receiver_id = c.receiver_id
        JOIN food_listings fl ON fl.food_id = c.food_id
        WHERE c.status = 'Completed'
        GROUP BY r.receiver_id, r.name
        ORDER BY avg_quantity_per_claim DESC
    """,
    "most_claimed_meal_type": """
        SELECT fl.meal_type, COUNT(*) AS completed_claims
        FROM claims c
        JOIN food_listings fl ON fl.food_id = c.food_id
        WHERE c.status = 'Completed'
        GROUP BY fl.meal_type
        ORDER BY completed_claims DESC
    """,
    "total_quantity_by_provider": """
        SELECT p.provider_id, p.name, SUM(fl.quantity) AS total_quantity_donated
        FROM providers p
        JOIN food_listings fl ON fl.provider_id = p.provider_id
        GROUP BY p.provider_id, p.name
        ORDER BY total_quantity_donated DESC
    """,
    "listings_near_expiry": """
        SELECT *
        FROM food_listings
        WHERE DATE(expiry_date) <= DATE('now', '+1 day')
        ORDER BY expiry_date
    """,
    "unclaimed_listings": """
        SELECT fl.*
        FROM food_listings fl
        LEFT JOIN claims c ON c.food_id = fl.food_id
        WHERE c.claim_id IS NULL
    """
}

# Create folder for outputs
import os
os.makedirs("query_outputs", exist_ok=True)

# Run each query and save as CSV
for name, sql in queries.items():
    df = pd.read_sql_query(sql, conn)
    df.to_csv(f"query_outputs/{name}.csv", index=False)
    print(f"{name}:\n", df.head(), "\n")

# Close the connection
conn.close()

print("All queries executed and saved in 'query_outputs' folder.")
