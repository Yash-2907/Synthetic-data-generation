import csv
import random
import os
from faker import Faker
import string
from datetime import datetime

# Output path
output_file = os.path.join(os.getcwd(), "benchmark_test", "schema_2", "schema_two_big.csv")
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Faker setup
fake = Faker(["th_TH", "id_ID"])
Faker.seed(2025)

# Size target: ~10GB
approx_row_size = 6700  # ~6.7KB
target_size_bytes = 10 * 1024 ** 3  # 10GB
num_rows = target_size_bytes // approx_row_size

# Email domains
email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

# Helper generators
def generate_thai_id():
    digits = [random.randint(0, 9) for _ in range(12)]
    total = sum((13 - i) * digit for i, digit in enumerate(digits))
    check_digit = (11 - total % 11) % 10
    return f"{digits[0]}-{''.join(map(str, digits[1:5]))}-{''.join(map(str, digits[5:10]))}-{''.join(map(str, digits[10:12]))}-{check_digit}"

def generate_email(name):
    clean_name = name.lower().replace(" ", ".").replace("'", "")
    return f"{clean_name}{random.randint(1,9999)}@{random.choice(email_domains)}"

def generate_passport(): return random.choice(["TH", "ID"]) + ''.join(random.choices(string.digits, k=7))
def generate_tin(): return f"{random.randint(1000000000000, 9999999999999)}"
def random_mac(): return ":".join([f"{random.randint(0x00, 0xFF):02x}" for _ in range(6)])
def generate_wallet(): return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

# Selected 150 fields
columns = [
    "Customer_ID", "Full_Name", "Gender", "Date_of_Birth", "Nationality",
    "Thai_ID", "Passport_Number", "TIN", "Phone_Number", "Email",
    "Address", "City", "Province", "Postal_Code", "Country",
    "Employment_Status", "Employer_Name", "Job_Title", "Department", "Monthly_Income",
    "Monthly_Expenses", "Credit_Score", "Risk_Level", "KYC_Completed", "KYC_Date",
    "Account_Number", "Bank_Name", "SWIFT_Code", "IBAN", "Currency",
    "Account_Type", "Opening_Date", "Account_Status", "Account_Locked", "Online_Banking_Enabled",
    "ATM_Withdrawal_Limit", "Overdraft_Enabled", "Linked_Accounts", "Loan_ID", "Loan_Amount",
    "Loan_Type", "Loan_Term_Months", "Loan_Start_Date", "Loan_End_Date", "Loan_Interest_Rate",
    "Loan_Status", "Collateral_Details", "Repayment_Amount", "Repayment_Frequency", "Repayment_Status",
    "Card_ID", "Card_Number", "Card_Type", "Card_Status", "Card_Limit",
    "Card_Expiry", "CVV", "Card_Issuer", "Billing_Cycle", "Reward_Points",
    "Transaction_ID", "Transaction_Date", "Transaction_Type", "Transaction_Amount", "Transaction_Currency",
    "Transaction_Status", "Merchant_Name", "Merchant_Category", "Merchant_Country", "Transaction_Channel",
    "Device_ID", "Device_Type", "Device_OS", "IP_Address", "MAC_Address",
    "Browser", "Location", "Login_Timestamp", "Logout_Timestamp", "Login_Method",
    "Failed_Login_Attempts", "Two_Factor_Enabled", "Biometric_Enabled", "Security_Question_Set", "Password_Last_Changed",
    "Crypto_Wallet_ID", "Crypto_Wallet_Address", "Crypto_Balance", "Crypto_Currency", "Wallet_Type",
    "Investment_Account_ID", "Investment_Type", "Investment_Amount", "Investment_Currency", "Investment_Return_Rate",
    "Insurance_Policy_ID", "Insurance_Provider", "Insurance_Type", "Coverage_Amount", "Premium_Amount",
    "Beneficiary_Name", "Policy_Start_Date", "Policy_End_Date", "Claim_History", "Policy_Status",
    "Support_Ticket_ID", "Issue_Category", "Issue_Description", "Resolution_Status", "Resolution_Date",
    "Feedback_Score", "Feedback_Comments", "Survey_Completed", "Survey_Date", "Newsletter_Subscribed",
    "Preferred_Contact_Method", "Last_Contact_Date", "Marketing_Opt_In", "Referral_Code", "Referral_Source",
    "Customer_Segment", "Loyalty_Tier", "Loyalty_Join_Date", "Loyalty_Expiry_Date", "Loyalty_Points",
    "Subscription_ID", "Subscription_Type", "Subscription_Status", "Subscription_Start_Date", "Subscription_End_Date",
    "Auto_Renew", "Payment_Method", "Last_Payment_Date", "Next_Billing_Date", "Billing_Address",
    "Shipping_Address", "Invoice_ID", "Invoice_Amount", "Invoice_Date", "Payment_Status",
    "Tax_ID", "Tax_Residency", "AML_Flag", "Watchlist_Flag", "PEP_Flag"
]

# Write CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    for _ in range(int(num_rows)):
        name = fake.name()
        row = {
            "Customer_ID": fake.uuid4(),
            "Full_Name": name,
            "Gender": random.choice(["Male", "Female", "Other"]),
            "Date_of_Birth": fake.date_of_birth(minimum_age=18, maximum_age=90),
            "Nationality": random.choice(["Thai", "Indonesian"]),
            "Thai_ID": generate_thai_id(),
            "Passport_Number": generate_passport(),
            "TIN": generate_tin(),
            "Phone_Number": fake.phone_number(),
            "Email": generate_email(name),
            "Address": fake.address(),
            "City": fake.city(),
            "Province": fake.state(),
            "Postal_Code": fake.postcode(),
            "Country": fake.country(),
            "Employment_Status": random.choice(["Employed", "Unemployed", "Freelancer"]),
            "Employer_Name": fake.company(),
            "Job_Title": fake.job(),
            "Department": random.choice(["Finance", "IT", "HR", "Sales"]),
            "Monthly_Income": round(random.uniform(5000, 50000), 2),
            "Monthly_Expenses": round(random.uniform(3000, 40000), 2),
            "Credit_Score": random.randint(300, 850),
            "Risk_Level": random.choice(["Low", "Medium", "High"]),
            "KYC_Completed": random.choice(["Yes", "No"]),
            "KYC_Date": fake.date_between(start_date='-5y', end_date='today'),
            "Account_Number": fake.bban(),
            "Bank_Name": fake.company(),
            "SWIFT_Code": fake.swift(),
            "IBAN": fake.iban(),
            "Currency": random.choice(["THB", "IDR", "USD"]),
            "Account_Type": random.choice(["Savings", "Current"]),
            "Opening_Date": fake.date_between(start_date='-10y', end_date='today'),
            "Account_Status": random.choice(["Active", "Dormant", "Closed"]),
            "Account_Locked": random.choice(["Yes", "No"]),
            "Online_Banking_Enabled": random.choice(["Yes", "No"]),
            "ATM_Withdrawal_Limit": random.randint(10000, 100000),
            "Overdraft_Enabled": random.choice(["Yes", "No"]),
            "Linked_Accounts": random.randint(0, 5),
            "Loan_ID": fake.uuid4(),
            "Loan_Amount": round(random.uniform(50000, 1000000), 2),
            "Loan_Type": random.choice(["Home", "Auto", "Personal"]),
            "Loan_Term_Months": random.choice([12, 24, 36, 60, 120]),
            "Loan_Start_Date": fake.date_between(start_date='-5y', end_date='-1y'),
            "Loan_End_Date": fake.date_between(start_date='-1y', end_date='today'),
            "Loan_Interest_Rate": round(random.uniform(2.0, 15.0), 2),
            "Loan_Status": random.choice(["Approved", "Pending", "Rejected"]),
            "Collateral_Details": fake.text(max_nb_chars=20),
            "Repayment_Amount": round(random.uniform(1000, 10000), 2),
            "Repayment_Frequency": random.choice(["Monthly", "Quarterly"]),
            "Repayment_Status": random.choice(["On Track", "Delayed", "Defaulted"]),
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
            "Merchant_Category": random.choice(["Retail", "Food", "Electronics"]),
            "Merchant_Country": fake.country(),
            "Transaction_Channel": random.choice(["Online", "POS", "ATM"]),
            "Device_ID": fake.uuid4(),
            "Device_Type": random.choice(["Mobile", "Laptop", "Tablet"]),
            "Device_OS": random.choice(["Android", "iOS", "Windows"]),
            "IP_Address": fake.ipv4_public(),
            "MAC_Address": random_mac(),
            "Browser": random.choice(["Chrome", "Safari", "Firefox"]),
            "Location": fake.city(),
            "Login_Timestamp": fake.date_time_this_year(),
            "Logout_Timestamp": fake.date_time_this_year(),
            "Login_Method": random.choice(["Password", "OTP", "Biometric"]),
            "Failed_Login_Attempts": random.randint(0, 5),
            "Two_Factor_Enabled": random.choice(["Yes", "No"]),
            "Biometric_Enabled": random.choice(["Yes", "No"]),
            "Security_Question_Set": random.choice(["Yes", "No"]),
            "Password_Last_Changed": fake.date_this_year(),
            "Crypto_Wallet_ID": fake.uuid4(),
            "Crypto_Wallet_Address": generate_wallet(),
            "Crypto_Balance": round(random.uniform(0.01, 50.0), 4),
            "Crypto_Currency": random.choice(["BTC", "ETH", "USDT"]),
            "Wallet_Type": random.choice(["Hardware", "Software"]),
            "Investment_Account_ID": fake.uuid4(),
            "Investment_Type": random.choice(["Stocks", "Mutual Funds", "Bonds"]),
            "Investment_Amount": round(random.uniform(1000, 50000), 2),
            "Investment_Currency": random.choice(["USD", "THB"]),
            "Investment_Return_Rate": round(random.uniform(2.0, 12.0), 2),
            "Insurance_Policy_ID": fake.uuid4(),
            "Insurance_Provider": fake.company(),
            "Insurance_Type": random.choice(["Health", "Life", "Vehicle"]),
            "Coverage_Amount": round(random.uniform(10000, 500000), 2),
            "Premium_Amount": round(random.uniform(500, 5000), 2),
            "Beneficiary_Name": fake.name(),
            "Policy_Start_Date": fake.date_between(start_date='-3y', end_date='-1y'),
            "Policy_End_Date": fake.date_between(start_date='-1y', end_date='today'),
            "Claim_History": random.choice(["Yes", "No"]),
            "Policy_Status": random.choice(["Active", "Expired", "Cancelled"]),
            "Support_Ticket_ID": fake.uuid4(),
            "Issue_Category": random.choice(["Login", "Transaction", "Card"]),
            "Issue_Description": fake.sentence(nb_words=6),
            "Resolution_Status": random.choice(["Resolved", "Unresolved"]),
            "Resolution_Date": fake.date_this_year(),
            "Feedback_Score": random.randint(1, 10),
            "Feedback_Comments": fake.sentence(nb_words=10),
            "Survey_Completed": random.choice(["Yes", "No"]),
            "Survey_Date": fake.date_this_year(),
            "Newsletter_Subscribed": random.choice(["Yes", "No"]),
            "Preferred_Contact_Method": random.choice(["Email", "Phone", "SMS"]),
            "Last_Contact_Date": fake.date_this_year(),
            "Marketing_Opt_In": random.choice(["Yes", "No"]),
            "Referral_Code": fake.lexify("REF#####"),
            "Referral_Source": random.choice(["Friend", "Email", "Ad"]),
            "Customer_Segment": random.choice(["Retail", "Corporate", "SME"]),
            "Loyalty_Tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
            "Loyalty_Join_Date": fake.date_between(start_date='-3y', end_date='today'),
            "Loyalty_Expiry_Date": fake.date_between(start_date='today', end_date='+3y'),
            "Loyalty_Points": random.randint(0, 10000),
            "Subscription_ID": fake.uuid4(),
            "Subscription_Type": random.choice(["Basic", "Pro", "Enterprise"]),
            "Subscription_Status": random.choice(["Active", "Expired", "Paused"]),
            "Subscription_Start_Date": fake.date_between(start_date='-2y', end_date='-6m'),
            "Subscription_End_Date": fake.date_between(start_date='-6m', end_date='+6m'),
            "Auto_Renew": random.choice(["Yes", "No"]),
            "Payment_Method": random.choice(["Credit Card", "Bank Transfer", "Wallet"]),
            "Last_Payment_Date": fake.date_between(start_date='-1y', end_date='today'),
            "Next_Billing_Date": fake.date_between(start_date='today', end_date='+1y'),
            "Billing_Address": fake.address(),
            "Shipping_Address": fake.address(),
            "Invoice_ID": fake.uuid4(),
            "Invoice_Amount": round(random.uniform(50, 1000), 2),
            "Invoice_Date": fake.date_this_year(),
            "Payment_Status": random.choice(["Paid", "Pending", "Overdue"]),
            "Tax_ID": f"TAX{random.randint(100000,999999)}",
            "Tax_Residency": random.choice(["Thailand", "Indonesia", "Other"]),
            "AML_Flag": random.choice(["Yes", "No"]),
            "Watchlist_Flag": random.choice(["Yes", "No"]),
            "PEP_Flag": random.choice(["Yes", "No"])
        }

        writer.writerow(row)

print("✅ Finished generating schema_2 big table (~10GB).")
