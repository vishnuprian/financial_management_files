# backend/app.py
from fastapi import FastAPI, Query
from boto3.dynamodb.conditions import Key
import boto3
from collections import defaultdict
from decimal import Decimal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("financial_data")

def analyze_transactions(transactions):
    total_spent = Decimal("0.0")
    category_totals = defaultdict(Decimal)
    daily_totals = defaultdict(Decimal)

    for t in transactions:
        amount = Decimal(str(t["amount"]))
        total_spent += amount
        category_totals[t["merchantCategory"]] += amount
        daily_totals[t["transaction_date"][:10]] += amount

    return {
        "total_spent": float(total_spent),
        "by_category": {k: float(v) for k, v in category_totals.items()},
        "by_day": {k: float(v) for k, v in daily_totals.items()}
    }

@app.get("/analytics")
def get_analytics(user_id: str = Query(...), month: str = Query(...)):
    start = f"{month}-01"
    end = f"{month}-31"
    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id) &
                               Key("transaction_date").between(start, end)
    )
    transactions = response["Items"]
    if not transactions:
        return {"total_spent": 0, "by_category": {}, "by_day": {}}
    return analyze_transactions(transactions)
