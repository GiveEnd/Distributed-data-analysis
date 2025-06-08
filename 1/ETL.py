import pandas as pd
from datetime import datetime
import sqlite3

df_raw = pd.read_csv("customers-100.csv")
print("Исходный CSV:")
print(df_raw)

def transform_data(df):
    df = df.copy()

    # Объединение имени и фамилии в один столбец Full Name
    df["Full Name"] = df["First Name"] + " " + df["Last Name"]

    # Оставить только валидные телефоны: убрать null и дефисы
    for col in ["Phone 1", "Phone 2"]:
        df[col] = df[col].fillna("Нет данных")
        df[col] = df[col].astype(str).str.replace("-", "").str.replace("x", " доб. ")

    df_clean = df[["Customer Id", "Full Name", "Company", "City", "Country", "Phone 1", "Phone 2", "Email", "Subscription Date", "Website"]]

    return df_clean

df_clean = transform_data(df_raw)

print("Измененный CSV:")
df_clean.to_csv("customers_cleaned.csv", index=False)
print(df_clean.head())

conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    full_name TEXT,
    company TEXT,
    city TEXT,
    country TEXT,
    phone1 TEXT,
    phone2 TEXT,
    email TEXT,
    subscription_date TEXT,
    website TEXT
)
""")

# Загрузка данных из DataFrame в SQLite
df_clean.to_sql("customers", conn, if_exists='replace', index=False)

print("Данные из таблицы SQLite:")
for row in cursor.execute("SELECT * FROM customers"):
    print(row)

conn.close()