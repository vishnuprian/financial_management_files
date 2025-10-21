import csv
import boto3
import random
from decimal import Decimal

# -------- CONFIG --------
CSV_FILE = "upi_transactions_2024_cleaned.csv"
DYNAMODB_TABLE = "financial_data"
SAMPLE_SIZE = 2000
USER_ID = "user1"  # <-- assign all transactions to this user
# -----------------------

table = boto3.resource("dynamodb").Table(DYNAMODB_TABLE)

with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = list(csv.DictReader(f))

sample_rows = random.sample(reader, SAMPLE_SIZE)

for i, row in enumerate(sample_rows, start=1):
    item = {
        "recordId": row["transaction id"],
        "user_id": USER_ID,                    # <-- Added user_id
        "transaction_date": row["timestamp"],  # Renamed for clarity
        "transactionType": row.get("transaction type", "Unknown"),
        "merchantCategory": row.get("merchant_category", "Unknown"),
        "amount": Decimal(row["amount (INR)"]),
        "status": row.get("transaction_status", "Unknown")
    }
    table.put_item(Item=item)

    if i % 100 == 0:
        print(f"{i} rows uploaded...")

print(f"✅ Finished uploading {SAMPLE_SIZE} random rows to DynamoDB!")
