import csv
import random
import os
from faker import Faker
import string
from datetime import datetime

# Output file (current directory)
base_dir = os.path.join(os.getcwd(), "benchmark_test", "schema_1", "output")
os.makedirs(base_dir, exist_ok=True)
output_file = os.path.join(base_dir, "schema_one_big.csv")


# Faker setup
fake = Faker(["th_TH", "id_ID"])
Faker.seed(42)

# File size target: ~1GB
row_size_bytes = 1000  # Estimated size per row
target_size_mb = 1000
target_size_bytes = target_size_mb * 1024 ** 2
num_rows = target_size_bytes // row_size_bytes

# Email domains
email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com"]

# Column definitions (50)
columns = [
    "Customer_ID", "Full_Name", "Gender", "Date_of_Birth", "Nationality",
    "Thai_ID", "Passport_Number", "TIN", "Phone_Number", "Email",
    "Account_Number", "Bank_Name", "SWIFT_Code", "IBAN", "Account_Type",
    "Opening_Date", "Current_Balance", "Currency", "Credit_Score", "Risk_Level",
    "Loan_ID", "Loan_Amount", "Loan_Purpose", "Loan_Status", "Collateral_Type",
    "Repayment_Amount", "Repayment_Date", "Card_Type", "Card_Number", "Card_Status",
    "Transaction_ID", "Transaction_Amount", "Transaction_Date", "Merchant_Category", "Transaction_Channel",
    "MAC_Address", "IP_Address", "Device_Type", "Login_Timestamp", "Logout_Timestamp",
    "Employment_Status", "Monthly_Income", "Monthly_Expenses", "Employer_Name", "Job_Title",
    "Crypto_Wallet_Address", "Crypto_Balance", "Wallet_Type", "Account_Locked", "Customer_Segment"
]

# Helper functions
def generate_thai_id():
    digits = [random.randint(0, 9) for _ in range(12)]
    total = sum((13 - i) * digit for i, digit in enumerate(digits))
    check_digit = (11 - total % 11) % 10
    return '{}-{}-{}-{}-{}'.format(
        digits[0],
        ''.join(map(str, digits[1:5])),
        ''.join(map(str, digits[5:10])),
        ''.join(map(str, digits[10:12])),
        check_digit
    )

def generate_passport():
    return random.choice(["TH", "ID"]) + ''.join(random.choices(string.digits, k=7))

def generate_tin():
    return f"{random.randint(1000000000000, 9999999999999)}"

def generate_crypto_wallet():
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def random_mac():
    return ":".join([f"{random.randint(0x00, 0xFF):02x}" for _ in range(6)])

def generate_email(name):
    clean_name = name.lower().replace(" ", ".").replace("'", "")
    domain = random.choice(email_domains)
    return f"{clean_name}{random.randint(1,9999)}@{domain}"

# Write data
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    for _ in range(num_rows):
        profile = fake.simple_profile()
        name = profile["name"]
        row = {
            "Customer_ID": fake.uuid4(),
            "Full_Name": name,
            "Gender": profile["sex"],
            "Date_of_Birth": profile["birthdate"],
            "Nationality": random.choice(["Thai", "Indonesian"]),
            "Thai_ID": generate_thai_id(),
            "Passport_Number": generate_passport(),
            "TIN": generate_tin(),
            "Phone_Number": fake.phone_number(),
            "Email": generate_email(name),
            "Account_Number": fake.bban(),
            "Bank_Name": fake.company(),
            "SWIFT_Code": fake.swift(),
            "IBAN": fake.iban(),
            "Account_Type": random.choice(["Savings", "Current"]),
            "Opening_Date": fake.date_between(start_date='-10y', end_date='today'),
            "Current_Balance": round(random.uniform(100.0, 1000000.0), 2),
            "Currency": random.choice(["THB", "IDR", "USD"]),
            "Credit_Score": random.randint(300, 850),
            "Risk_Level": random.choice(["Low", "Medium", "High"]),
            "Loan_ID": fake.uuid4(),
            "Loan_Amount": round(random.uniform(1000.0, 500000.0), 2),
            "Loan_Purpose": random.choice(["Education", "Business", "Personal"]),
            "Loan_Status": random.choice(["Approved", "Pending", "Rejected"]),
            "Collateral_Type": random.choice(["None", "Vehicle", "Property"]),
            "Repayment_Amount": round(random.uniform(100.0, 10000.0), 2),
            "Repayment_Date": fake.date_between(start_date='-1y', end_date='today'),
            "Card_Type": random.choice(["Debit", "Credit"]),
            "Card_Number": fake.credit_card_number(),
            "Card_Status": random.choice(["Active", "Blocked", "Expired"]),
            "Transaction_ID": fake.uuid4(),
            "Transaction_Amount": round(random.uniform(10.0, 50000.0), 2),
            "Transaction_Date": fake.date_between(start_date='-1y', end_date='today'),
            "Merchant_Category": random.choice(["Retail", "Travel", "Food"]),
            "Transaction_Channel": random.choice(["Online", "ATM", "POS"]),
            "MAC_Address": random_mac(),
            "IP_Address": fake.ipv4_public(),
            "Device_Type": random.choice(["Mobile", "Laptop", "Tablet"]),
            "Login_Timestamp": fake.date_time_this_year(),
            "Logout_Timestamp": fake.date_time_this_year(),
            "Employment_Status": random.choice(["Employed", "Unemployed", "Self-employed"]),
            "Monthly_Income": round(random.uniform(400.0, 10000.0), 2),
            "Monthly_Expenses": round(random.uniform(300.0, 9000.0), 2),
            "Employer_Name": fake.company(),
            "Job_Title": fake.job(),
            "Crypto_Wallet_Address": generate_crypto_wallet(),
            "Crypto_Balance": round(random.uniform(0.01, 10.0), 4),
            "Wallet_Type": random.choice(["Hardware", "Software", "Online"]),
            "Account_Locked": random.choice([True, False]),
            "Customer_Segment": random.choice(["Retail", "SME", "Corporate"])
        }

        writer.writerow(row)

print(f"✅ Done! File saved at: {output_file}")