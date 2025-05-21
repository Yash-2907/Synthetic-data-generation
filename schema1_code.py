import csv
import random
import os
from faker import Faker
import string

# Output directory
base_dir = os.path.join(os.getcwd(), "benchmark_test", "schema_1", "output")
os.makedirs(base_dir, exist_ok=True)

# Faker setup
fake = Faker(["th_TH", "id_ID"])
Faker.seed(99)

# Number of files
num_files = 99

# Estimated size per row and file limits
min_size_bytes = 1 * 1024 * 1024  # 1 MB
max_size_bytes = 5 * 1024 * 1024  # 5 MB
row_size_bytes = 500              # estimated

# Email domain pool
email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com"]

# Full pool of diverse base columns
base_columns = [
    # Identity / Contact
    "Customer_ID", "Full_Name", "Gender", "Date_of_Birth", "Nationality",

    # Banking / Account
    "Account_Number", "Bank_Name", "SWIFT_Code", "IBAN", "Account_Type",
    "Opening_Date", "Current_Balance", "Currency",

    # Credit / Loan
    "Loan_ID", "Loan_Amount", "Loan_Purpose", "Loan_Status", "Collateral_Type",

    # Employment
    "Employment_Status", "Monthly_Income", "Monthly_Expenses", "Employer_Name", "Job_Title",

    # Device / Login
    "MAC_Address", "IP_Address", "Device_Type", "Login_Timestamp", "Logout_Timestamp",
    "Account_Locked", "Two_Factor_Enabled", "Biometric_Auth_Enabled",

    # Crypto
    "Crypto_Wallet_Address", "Crypto_Balance", "Wallet_Type",

    # Rewards / Spending
    "Reward_Points", "Reward_Redemption_Rate", "Loyalty_Level",
    "Online_Shopping_Spend", "Utility_Bill_Payments", "Subscription_Services",

    # Support / Feedback
    "Support_Tickets", "Customer_Feedback", "Satisfaction_Score", "Complaint_Status",

    # Transactions
    "Transaction_ID", "Transaction_Type", "Transaction_Amount", "Transaction_Date",
    "Transaction_Channel", "Merchant_Category", "Frequent_Merchant", "Top_Spending_Category"
]

# Sensitive fields to always mix in
sensitive_fields = ["Email", "Phone_Number", "TIN", "Thai_ID", "Passport_Number"]

# Field generators
def generate_thai_id():
    digits = [random.randint(0, 9) for _ in range(12)]
    total = sum((13 - i) * digit for i, digit in enumerate(digits))
    check_digit = (11 - total % 11) % 10
    return '{}-{}-{}-{}-{}'.format(digits[0], ''.join(map(str, digits[1:5])), ''.join(map(str, digits[5:10])), ''.join(map(str, digits[10:12])), check_digit)

def generate_passport():
    return random.choice(["TH", "ID"]) + ''.join(random.choices(string.digits, k=7))

def generate_tin():
    return f"{random.randint(1000000000000,9999999999999)}"

def generate_crypto_wallet():
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def random_mac():
    return ":".join([f"{random.randint(0x00, 0xFF):02x}" for _ in range(6)])

def generate_email(name):
    clean = name.lower().replace(" ", ".").replace("'", "")
    return f"{clean}{random.randint(1,9999)}@{random.choice(email_domains)}"

# Generate each file
for i in range(1, num_files + 1):
    file_name = f"table_{i:03d}.csv"
    file_path = os.path.join(base_dir, file_name)

    # Random 18 base + 2 sensitive columns
    non_sens_cols = random.sample(base_columns, 18)
    sens_cols = random.sample(sensitive_fields, 2)
    columns = non_sens_cols + sens_cols
    random.shuffle(columns)

    # Estimate number of rows
    target_size = random.randint(min_size_bytes, max_size_bytes)
    num_rows = target_size // row_size_bytes

    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
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
                "Phone_Number": fake.phone_number(),
                "Email": generate_email(name),
                "TIN": generate_tin(),
                "Thai_ID": generate_thai_id(),
                "Passport_Number": generate_passport(),
                "Account_Number": fake.bban(),
                "Bank_Name": fake.company(),
                "SWIFT_Code": fake.swift(),
                "IBAN": fake.iban(),
                "Account_Type": random.choice(["Savings", "Current"]),
                "Opening_Date": fake.date_between(start_date='-10y', end_date='today'),
                "Current_Balance": round(random.uniform(100.0, 100000.0), 2),
                "Currency": random.choice(["THB", "IDR", "USD"]),
                "Loan_ID": fake.uuid4(),
                "Loan_Amount": round(random.uniform(1000.0, 50000.0), 2),
                "Loan_Purpose": random.choice(["Education", "Business", "Personal"]),
                "Loan_Status": random.choice(["Approved", "Pending", "Rejected"]),
                "Collateral_Type": random.choice(["None", "Vehicle", "Property"]),
                "Employment_Status": random.choice(["Employed", "Unemployed", "Self-employed"]),
                "Monthly_Income": round(random.uniform(300.0, 10000.0), 2),
                "Monthly_Expenses": round(random.uniform(300.0, 9000.0), 2),
                "Employer_Name": fake.company(),
                "Job_Title": fake.job(),
                "Device_Type": random.choice(["Mobile", "Laptop", "Tablet", "Desktop"]),
                "MAC_Address": random_mac(),
                "IP_Address": fake.ipv4_public(),
                "Login_Timestamp": fake.date_time_this_year(),
                "Logout_Timestamp": fake.date_time_this_year(),
                "Account_Locked": random.choice([True, False]),
                "Two_Factor_Enabled": random.choice([True, False]),
                "Biometric_Auth_Enabled": random.choice([True, False]),
                "Crypto_Wallet_Address": generate_crypto_wallet(),
                "Crypto_Balance": round(random.uniform(0.01, 10.0), 4),
                "Wallet_Type": random.choice(["Hardware", "Software", "Online"]),
                "Reward_Points": random.randint(0, 10000),
                "Reward_Redemption_Rate": round(random.uniform(0.0, 100.0), 2),
                "Loyalty_Level": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
                "Online_Shopping_Spend": round(random.uniform(100.0, 5000.0), 2),
                "Utility_Bill_Payments": round(random.uniform(50.0, 1000.0), 2),
                "Subscription_Services": random.choice(["Netflix", "Spotify", "YouTube", "None"]),
                "Support_Tickets": random.randint(0, 10),
                "Customer_Feedback": fake.sentence(nb_words=6),
                "Satisfaction_Score": round(random.uniform(1.0, 10.0), 1),
                "Complaint_Status": random.choice(["Open", "Closed", "Escalated", "Pending"]),
                "Transaction_ID": fake.uuid4(),
                "Transaction_Type": random.choice(["Credit", "Debit"]),
                "Transaction_Amount": round(random.uniform(10.0, 2000.0), 2),
                "Transaction_Date": fake.date_between(start_date='-1y', end_date='today'),
                "Transaction_Channel": random.choice(["Online", "ATM", "POS", "Branch"]),
                "Merchant_Category": random.choice(["Retail", "Food", "Electronics", "Travel"]),
                "Frequent_Merchant": fake.company(),
                "Top_Spending_Category": random.choice(["Groceries", "Dining", "Utilities", "Shopping"])
            }

            # Write only selected columns
            writer.writerow({col: row[col] for col in columns})

    print(f"✅ Created {file_name} with {num_rows} rows")

print("🎉 Done generating all 99 small files in schema_1/output/")
