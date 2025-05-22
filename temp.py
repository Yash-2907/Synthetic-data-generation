import csv
import os
import random
import string
from faker import Faker
from datetime import datetime
from tqdm import tqdm
import time

# Setup Faker
fake = Faker(["th_TH", "id_ID"])
Faker.seed(2025)

# Output path
output_dir = os.path.join(os.getcwd(), "benchmark_test", "schema_2")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "schema_two_big.csv")

num_rows = 4904000

# Email domains
email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

# Helper generators
def generate_thai_id():
    digits = [random.randint(0, 9) for _ in range(12)]
    total = sum((13 - i) * digit for i, digit in enumerate(digits))
    check_digit = (11 - total % 11) % 10
    return f"{digits[0]}-{''.join(map(str, digits[1:5]))}-{''.join(map(str, digits[5:10]))}-{''.join(map(str, digits[10:12]))}-{check_digit}"

def generate_email(name):
    return f"{name.lower().replace(' ','.')}{random.randint(1,9999)}@{random.choice(email_domains)}"

def generate_wallet(): return '0x' + ''.join(random.choices('0123456789abcdef', k=40))
def generate_tin(): return str(random.randint(1000000000000, 9999999999999))
def random_mac(): return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])

# Final columns (80 core + 30+ new)
columns = [
    "Customer_ID", "Full_Name", "Gender", "Date_of_Birth", "Nationality",
    "Thai_ID", "TIN", "Phone_Number", "Email", "Passport_Number",
    "Address", "City", "Province", "Postal_Code", "Country",
    "Employment_Status", "Employer_Name", "Monthly_Income", "Monthly_Expenses", "Credit_Score",
    "KYC_Completed", "KYC_Date", "Account_Number", "Bank_Name", "SWIFT_Code",
    "IBAN", "Currency", "Account_Type", "Account_Status", "Online_Banking_Enabled",
    "ATM_Withdrawal_Limit", "Loan_ID", "Loan_Amount", "Loan_Type", "Loan_Status",
    "Loan_Term_Months", "Loan_Start_Date", "Loan_End_Date", "Loan_Interest_Rate", "Collateral_Details",
    "Card_ID", "Card_Number", "Card_Type", "Card_Status", "Card_Limit",
    "Card_Expiry", "CVV", "Card_Issuer", "Billing_Cycle", "Reward_Points",
    "Transaction_ID", "Transaction_Date", "Transaction_Type", "Transaction_Amount", "Transaction_Currency",
    "Transaction_Status", "Merchant_Name", "Transaction_Channel", "Device_ID", "Device_OS",
    "Device_Type", "MAC_Address", "IP_Address", "Login_Timestamp", "Logout_Timestamp",
    "Browser", "Location", "Login_Method", "Two_Factor_Enabled", "Failed_Login_Attempts",
    "Security_Question_Set", "Password_Last_Changed", "Crypto_Wallet_Address", "Crypto_Balance", "Crypto_Currency",
    "Investment_Account_ID", "Investment_Type", "Investment_Amount", "Investment_Return_Rate", "Investment_Currency",
    "Degree", "Graduation_Year", "Institution_Name", "Field_of_Study", "Work_Email",
    "Chronic_Conditions", "Diagnosis_Code", "Blood_Type", "Last_Visit_Date", "Insurance_Policy_ID",
    "Insurance_Type", "Coverage_Amount", "Policy_Status", "Policy_Start_Date", "Policy_End_Date",
    "Survey_Completed", "Survey_Date", "Feedback_Score", "Feedback_Comments", "Complaint_Status",
    "Referral_Code", "Preferred_Channel", "Customer_Segment", "Loyalty_Tier", "Loyalty_Join_Date",
    "Loyalty_Expiry_Date", "Loyalty_Points", "Auto_Renew", "Payment_Method", "Watchlist_Flag"
]

# Begin writing
start = time.time()
with open(output_file, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)

    for i in tqdm(range(int(num_rows)), desc="Generating schema_2 file"):
        name = fake.name()
        row = {
            "Customer_ID": fake.uuid4(),
            "Full_Name": name,
            "Gender": random.choice(["Male", "Female", "Other"]),
            "Date_of_Birth": fake.date_of_birth(minimum_age=18, maximum_age=90),
            "Nationality": random.choice(["Thai", "Indonesian"]),
            "Thai_ID": generate_thai_id(),
            "TIN": generate_tin(),
            "Phone_Number": fake.phone_number(),
            "Email": generate_email(name),
            "Passport_Number": random.choice(["TH", "ID"]) + ''.join(random.choices(string.digits, k=7)),
            "Address": fake.address(),
            "City": fake.city(),
            "Province": fake.state(),
            "Postal_Code": fake.postcode(),
            "Country": fake.country(),
            "Employment_Status": random.choice(["Employed", "Unemployed", "Freelancer"]),
            "Employer_Name": fake.company(),
            "Monthly_Income": round(random.uniform(5000, 50000), 2),
            "Monthly_Expenses": round(random.uniform(3000, 40000), 2),
            "Credit_Score": random.randint(300, 850),
            "KYC_Completed": random.choice(["Yes", "No"]),
            "KYC_Date": fake.date_between(start_date='-5y', end_date='today'),
            "Account_Number": fake.bban(),
            "Bank_Name": fake.company(),
            "SWIFT_Code": fake.swift(),
            "IBAN": fake.iban(),
            "Currency": random.choice(["THB", "IDR", "USD"]),
            "Account_Type": random.choice(["Savings", "Current"]),
            "Account_Status": random.choice(["Active", "Dormant", "Closed"]),
            "Online_Banking_Enabled": random.choice(["Yes", "No"]),
            "ATM_Withdrawal_Limit": random.randint(10000, 100000),
            "Loan_ID": fake.uuid4(),
            "Loan_Amount": round(random.uniform(50000, 1000000), 2),
            "Loan_Type": random.choice(["Home", "Auto", "Personal"]),
            "Loan_Status": random.choice(["Approved", "Pending", "Rejected"]),
            "Loan_Term_Months": random.choice([12, 24, 36, 60, 120]),
            "Loan_Start_Date": fake.date_between(start_date='-5y', end_date='-1y'),
            "Loan_End_Date": fake.date_between(start_date='-1y', end_date='today'),
            "Loan_Interest_Rate": round(random.uniform(2.0, 15.0), 2),
            "Collateral_Details": fake.word(),
            "Card_ID": fake.uuid4(),
            "Card_Number": fake.credit_card_number(),
            "Card_Type": random.choice(["Credit", "Debit"]),
            "Card_Status": random.choice(["Active", "Blocked", "Expired"]),
            "Card_Limit": round(random.uniform(10000, 100000), 2),
            "Card_Expiry": fake.credit_card_expire(),
            "CVV": random.randint(100, 999),
            "Card_Issuer": fake.company(),
            "Billing_Cycle": random.choice(["Monthly", "Quarterly"]),
            "Reward_Points": random.randint(0, 50000),
            "Transaction_ID": fake.uuid4(),
            "Transaction_Date": fake.date_between(start_date='-1y', end_date='today'),
            "Transaction_Type": random.choice(["Debit", "Credit", "Refund"]),
            "Transaction_Amount": round(random.uniform(10, 10000), 2),
            "Transaction_Currency": random.choice(["THB", "USD", "IDR"]),
            "Transaction_Status": random.choice(["Completed", "Failed", "Pending"]),
            "Merchant_Name": fake.company(),
            "Transaction_Channel": random.choice(["Online", "POS", "ATM"]),
            "Device_ID": fake.uuid4(),
            "Device_OS": random.choice(["Android", "iOS", "Windows"]),
            "Device_Type": random.choice(["Mobile", "Tablet", "Desktop"]),
            "MAC_Address": random_mac(),
            "IP_Address": fake.ipv4_public(),
            "Login_Timestamp": fake.date_time_this_year(),
            "Logout_Timestamp": fake.date_time_this_year(),
            "Browser": random.choice(["Chrome", "Safari", "Firefox"]),
            "Location": fake.city(),
            "Login_Method": random.choice(["Password", "OTP", "Biometric"]),
            "Two_Factor_Enabled": random.choice(["Yes", "No"]),
            "Failed_Login_Attempts": random.randint(0, 5),
            "Security_Question_Set": random.choice(["Yes", "No"]),
            "Password_Last_Changed": fake.date_this_year(),
            "Crypto_Wallet_Address": generate_wallet(),
            "Crypto_Balance": round(random.uniform(0.01, 50.0), 4),
            "Crypto_Currency": random.choice(["BTC", "ETH", "USDT"]),
            "Investment_Account_ID": fake.uuid4(),
            "Investment_Type": random.choice(["Stocks", "Mutual Funds", "Bonds"]),
            "Investment_Amount": round(random.uniform(1000, 50000), 2),
            "Investment_Return_Rate": round(random.uniform(2.0, 12.0), 2),
            "Investment_Currency": random.choice(["USD", "THB"]),
            "Degree": random.choice(["Bachelors", "Masters", "Diploma"]),
            "Graduation_Year": random.randint(2000, 2024),
            "Institution_Name": fake.company() + " University",
            "Field_of_Study": random.choice(["Finance", "Computer Science", "Nursing"]),
            "Work_Email": generate_email(name),
            "Chronic_Conditions": random.choice(["None", "Diabetes", "Asthma"]),
            "Diagnosis_Code": f"I{random.randint(10,99)}.{random.randint(0,9)}",
            "Blood_Type": random.choice(["A", "B", "AB", "O"]),
            "Last_Visit_Date": fake.date_this_year(),
            "Insurance_Policy_ID": fake.uuid4(),
            "Insurance_Type": random.choice(["Health", "Life", "Vehicle"]),
            "Coverage_Amount": round(random.uniform(10000, 500000), 2),
            "Policy_Status": random.choice(["Active", "Expired", "Cancelled"]),
            "Policy_Start_Date": fake.date_between(start_date='-3y', end_date='-1y'),
            "Policy_End_Date": fake.date_between(start_date='-1y', end_date='today'),
            "Survey_Completed": random.choice(["Yes", "No"]),
            "Survey_Date": fake.date_this_year(),
            "Feedback_Score": random.randint(1, 10),
            "Feedback_Comments": fake.sentence(nb_words=8),
            "Complaint_Status": random.choice(["Open", "Resolved", "Escalated"]),
            "Referral_Code": fake.lexify("REF#####"),
            "Preferred_Channel": random.choice(["Email", "SMS", "App"]),
            "Customer_Segment": random.choice(["Retail", "Corporate", "SME"]),
            "Loyalty_Tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
            "Loyalty_Join_Date": fake.date_between(start_date='-3y', end_date='today'),
            "Loyalty_Expiry_Date": fake.date_between(start_date='today', end_date='+3y'),
            "Loyalty_Points": random.randint(0, 10000),
            "Auto_Renew": random.choice(["Yes", "No"]),
            "Payment_Method": random.choice(["Card", "Bank", "Wallet"]),
            "Watchlist_Flag": random.choice(["Yes", "No"])
        }

        writer.writerow(row)

        if i % 1000 == 0:
            f.flush()

print("\n✅ Done. File saved at:", output_file)
