import pandas as pd

# Load CSVs
providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food_listings = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

# ---- 1) Quick preview ----
print("\nProviders:\n", providers.head())
print("\nReceivers:\n", receivers.head())
print("\nFood Listings:\n", food_listings.head())
print("\nClaims:\n", claims.head())

# ---- 2) Missing values ----
print("\nMissing values count:")
print({
    "providers": providers.isna().sum().to_dict(),
    "receivers": receivers.isna().sum().to_dict(),
    "food_listings": food_listings.isna().sum().to_dict(),
    "claims": claims.isna().sum().to_dict()
})

# ---- 3) Duplicates ----
print("\nDuplicate ID counts:")
print({
    "providers": providers["Provider_ID"].duplicated().sum(),
    "receivers": receivers["Receiver_ID"].duplicated().sum(),
    "food_listings": food_listings["Food_ID"].duplicated().sum(),
    "claims": claims["Claim_ID"].duplicated().sum()
})

# ---- 4) Foreign key checks ----
missing_providers = set(food_listings["Provider_ID"]) - set(providers["Provider_ID"])
print("\nProviders in listings but missing in providers table:", missing_providers)

missing_receivers = set(claims["Receiver_ID"]) - set(receivers["Receiver_ID"])
print("Receivers in claims but missing in receivers table:", missing_receivers)

missing_food = set(claims["Food_ID"]) - set(food_listings["Food_ID"])
print("Food IDs in claims but missing in food_listings table:", missing_food)

food_listings['Expiry_Date'] = pd.to_datetime(food_listings['Expiry_Date'])
claims['Timestamp'] = pd.to_datetime(claims['Timestamp'])

providers.to_csv("providers_clean.csv", index=False)
receivers.to_csv("receivers_clean.csv", index=False)
food_listings.to_csv("food_listings_clean.csv", index=False)
claims.to_csv("claims_clean.csv", index=False)


import sqlite3

conn = sqlite3.connect("food.db")
providers.to_sql("providers", conn, if_exists="replace", index=False)
receivers.to_sql("receivers", conn, if_exists="replace", index=False)
food_listings.to_sql("food_listings", conn, if_exists="replace", index=False)
claims.to_sql("claims", conn, if_exists="replace", index=False)
conn.close()
