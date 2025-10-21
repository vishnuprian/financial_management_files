import pandas as pd
import sys

def clean_upi_dataset(input_file, output_file):
    # Define essential fields for financial tracking
    essential_cols = [
        "transaction id",
        "timestamp",
        "transaction type",
        "merchant_category",
        "amount (INR)",
        "transaction_status"
    ]

    # Load dataset
    df = pd.read_csv(input_file)

    # Keep only essential columns
    df_cleaned = df[essential_cols]

    # Save cleaned dataset
    df_cleaned.to_csv(output_file, index=False)
    print(f"✅ Cleaned dataset saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_upi_data.py <input_file.csv> <output_file.csv>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        clean_upi_dataset(input_file, output_file)
