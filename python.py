import csv
import random
import os
from faker import Faker
import string
from datetime import datetime, timedelta

# Save the DataFrame to a CSV file locally
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, 'extended_financial_dataset.csv')

# Initialize Faker
locales = ["th_TH", "id_ID"]
fake = Faker(locales)
Faker.seed(42)

# Data size config
total_target_size_bytes = 200 * 1024 ** 9
row_size_bytes = 6 * 1024
num_rows = total_target_size_bytes // row_size_bytes

# Thai ID generator
def generate_thai_id():
    digits = [random.randint(0, 9) for _ in range(12)]
    total = sum((13 - i) * digit for i, digit in enumerate(digits))
    check_digit = (11 - total % 11) % 10
    return '{}-{}-{}-{}-{}'.format(digits[0], ''.join(map(str, digits[1:5])), ''.join(map(str, digits[5:10])), ''.join(map(str, digits[10:12])), check_digit)

# Indonesian NIK generator
def generate_indonesian_nik():
    province_code = random.randint(10,99)
    city_code = random.randint(1000,9999)
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    dd = dob.day + 40 if random.choice([True, False]) else dob.day
    mm = dob.month
    yy = dob.year % 100
    suffix = random.randint(1000,9999)
    return f"{province_code}{city_code}{dd:02d}{mm:02d}{yy:02d}{suffix}"

# Helper field generators
def generate_tin():
    return f"{random.randint(1000000000000,9999999999999)}"

def generate_crypto_wallet():
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_bank_routing():
    return str(random.randint(100000000, 999999999))

def random_mac():
    return ":".join([f"{random.randint(0x00, 0xFF):02x}" for _ in range(6)])

def generate_passport():
    return random.choice(["TH", "ID"]) + ''.join(random.choices(string.digits, k=7))

def random_ratio(min_val=0.01, max_val=1.0):
    return round(random.uniform(min_val, max_val), 2)

# Base financial columns (100)
columns = [
    "Customer_ID", "Full_Name", "Gender", "Date_of_Birth", "Nationality",
    "Thai_ID", "NIC", "Phone_Number", "Email", "Address",
    "Account_Number", "Bank_Name", "SWIFT_Code", "IBAN", "Account_Type",
    "Opening_Date", "Current_Balance", "Currency", "Credit_Score", "Risk_Level",
    "Transaction_ID", "Transaction_Type", "Transaction_Amount", "Transaction_Date", "Transaction_Channel",
    "Merchant_Name", "Merchant_Category", "Card_Type", "Card_Number", "Card_Expiry",
    "Card_CVV", "Loan_ID", "Loan_Amount", "Loan_Purpose", "Loan_Term",
    "Interest_Rate", "Monthly_Payment", "Loan_Status", "Collateral_Type", "Collateral_Value",
    "Repayment_ID", "Repayment_Amount", "Repayment_Date", "Late_Fee", "Penalty_Charged",
    "ATM_Transaction_ID", "ATM_Location", "ATM_Date", "ATM_Amount", "ATM_Type",
    "Card_Issuer", "Card_Limit", "Card_Balance", "Card_Status", "Card_Usage_Category",
    "Forex_Transaction_ID", "From_Currency", "To_Currency", "Exchange_Rate", "Forex_Amount",
    "Fraud_Alert_ID", "Alert_Type", "Alert_Date", "Alert_Severity", "Alert_Status",
    "TIN", "Passport_Number", "MAC_Address", "IP_Address", "Device_Type",
    "Login_Timestamp", "Logout_Timestamp", "Failed_Login_Attempts", "Account_Locked", "Security_Questions_Set",
    "Last_Transaction_Location", "Annual_Income", "Monthly_Income", "Monthly_Expenses", "Employment_Status",
    "Employer_Name", "Employment_Start_Date", "Employment_Type", "Job_Title", "Industry",
    "Investment_Account", "Portfolio_Value", "Stock_Holdings", "Bond_Holdings", "Mutual_Funds",
    "Retirement_Account", "Retirement_Age", "Insurance_Policy_ID", "Insurance_Type", "Insurance_Premium",
    "Insurance_Coverage", "Beneficiary_Name", "Crypto_Wallet_Address", "Crypto_Balance", "Wallet_Type",
    "Digital_Banking_Enabled", "Online_Shopping_Spend", "Utility_Bill_Payments", "Loan_Refinanced", "Customer_Segment"
]
# Additional financial + behavioral columns (another 100)
columns += [
    "Vehicle_Loan_ID", "Vehicle_Type", "Vehicle_Value", "Vehicle_Registration", "Vehicle_Loan_Status",
    "Housing_Loan_ID", "Property_Type", "Property_Value", "Mortgage_Term", "Mortgage_Rate",
    "Rental_Status", "Monthly_Rent", "Lease_Term", "Landlord_Name", "Property_Location",
    "Overdraft_Protection", "Standing_Instructions", "Recurring_Transfers", "Nominee_Name", "Nominee_Relationship",
    "Digital_Signature_Setup", "Mobile_Banking_Enabled", "Last_Mobile_Login", "Preferred_Language", "SMS_Alerts_Enabled",
    "Email_Alerts_Enabled", "Region", "Branch_ID", "Branch_Location", "Service_Rating",
    "Customer_Feedback", "Support_Tickets", "Ticket_Resolution_Time", "Escalated_Tickets", "Support_Channel",
    "Cross_Border_Transactions", "Number_of_Beneficiaries", "Savings_Goal", "Savings_Progress", "Credit_Limit_Utilization",
    "Loan_Eligibility_Score", "Preapproved_Offers", "Debit_Card_Active", "Credit_Card_Active", "KYC_Completed",
    "AML_Flagged", "PEP_Status", "Watchlist_Match", "Transaction_Limit", "Custom_Limit_Set",
    "Annual_Spending", "Top_Spending_Category", "Frequent_Merchant", "Subscription_Services", "Recurring_Charges",
    "Unusual_Activity_Flag", "Fraud_Cases_Reported", "Blacklist_Status", "Account_Migration_Status", "Reactivation_Requests",
    "Marketing_Opt_In", "Push_Notifications_Enabled", "Two_Factor_Enabled", "Biometric_Auth_Enabled", "PIN_Changed_Recently",
    "Last_Password_Update", "Device_Count", "Primary_Device_OS", "Browser_Type", "Last_Login_Device",
    "Reward_Points", "Reward_Redemption_Rate", "Cashback_Earned", "Loyalty_Level", "Referral_Code",
    "Referred_By", "Campaign_Signup", "Survey_Participation", "Complaint_Status", "Satisfaction_Score",
    "Time_with_Bank", "Dormancy_Flag", "Tax_Compliance", "Interest_Accrued", "Penalty_Interest",
    "Loan_Restructure_Status", "Account_Type_Changed", "Credit_Score_Source", "Credit_Score_Update", "Income_Verification_Status",
    "Digital_Documents_Submitted", "Verification_Channel", "Digital_KYC_Flag", "Crypto_Transactions_Enabled", "Payment_Gateway_Used"
]
write_header = not os.path.exists(file_path)
with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        if write_header:
           writer.writeheader()
        for i in range(num_rows):
                profile = fake.profile()
                dob = profile['birthdate']
                gender = profile['sex']
                row = {
                "Customer_ID": fake.uuid4(),
                "Full_Name": profile["name"],
                "Gender": gender,
                "Date_of_Birth": dob,
                "Nationality": random.choice(["Thai", "Indonesian"]),
                "Thai_ID": generate_thai_id(),
                "NIC": generate_indonesian_nik(),
                "Phone_Number": fake.phone_number(),
                "Email": fake.free_email(),
                "Address": fake.address().replace("\n", ", "),
                "Account_Number": fake.bban(),
                "Bank_Name": fake.company(),
                "SWIFT_Code": fake.swift(),
                "IBAN": fake.iban(),
                "Account_Type": random.choice(["Savings", "Current", "Business"]),
                "Opening_Date": fake.date_between(start_date='-10y', end_date='today'),
                "Current_Balance": round(random.uniform(100.0, 1000000.0), 2),
                "Currency": random.choice(["THB", "IDR", "USD"]),
                "Credit_Score": random.randint(300, 850),
                "Risk_Level": random.choice(["Low", "Medium", "High"]),
                "Transaction_ID": fake.uuid4(),
                "Transaction_Type": random.choice(["Credit", "Debit"]),
                "Transaction_Amount": round(random.uniform(10.0, 50000.0), 2),
                "Transaction_Date": fake.date_between(start_date='-1y', end_date='today'),
                "Transaction_Channel": random.choice(["Online", "ATM", "Branch", "POS"]),
                "Merchant_Name": fake.company(),
                "Merchant_Category": random.choice(["Retail", "Food", "Electronics", "Travel"]),
                "Card_Type": random.choice(["Debit", "Credit"]),
                "Card_Number": fake.credit_card_number(),
                "Card_Expiry": fake.credit_card_expire(),
                "Card_CVV": fake.credit_card_security_code(),
                "Loan_ID": fake.uuid4(),
                "Loan_Amount": round(random.uniform(1000.0, 500000.0), 2),
                "Loan_Purpose": random.choice(["Education", "Business", "Personal", "Home", "Auto"]),
                "Loan_Term": random.randint(6, 60),
                "Interest_Rate": round(random.uniform(2.5, 12.0), 2),
                "Monthly_Payment": round(random.uniform(100.0, 5000.0), 2),
                "Loan_Status": random.choice(["Approved", "Pending", "Rejected", "Closed"]),
                "Collateral_Type": random.choice(["None", "Vehicle", "Property", "Gold"]),
                "Collateral_Value": round(random.uniform(0, 100000.0), 2),
                "Repayment_ID": fake.uuid4(),
                "Repayment_Amount": round(random.uniform(100.0, 10000.0), 2),
                "Repayment_Date": fake.date_between(start_date='-6M', end_date='today'),
                "Late_Fee": round(random.uniform(0, 500.0), 2),
                "Penalty_Charged": round(random.uniform(0, 200.0), 2),
                "ATM_Transaction_ID": fake.uuid4(),
                "ATM_Location": fake.city(),
                "ATM_Date": fake.date_between(start_date='-1y', end_date='today'),
                "ATM_Amount": round(random.uniform(100.0, 5000.0), 2),
                "ATM_Type": random.choice(["Withdrawal", "Deposit", "Balance Inquiry"]),
                "Card_Issuer": random.choice(["Visa", "Mastercard", "UnionPay", "JCB"]),
                "Card_Limit": round(random.uniform(5000.0, 100000.0), 2),
                "Card_Balance": round(random.uniform(0, 50000.0), 2),
                "Card_Status": random.choice(["Active", "Blocked", "Expired"]),
                "Card_Usage_Category": random.choice(["Travel", "Shopping", "Utilities"]),
                "Forex_Transaction_ID": fake.uuid4(),
                "From_Currency": random.choice(["THB", "IDR", "USD"]),
                "To_Currency": random.choice(["USD", "JPY", "EUR"]),
                "Exchange_Rate": round(random.uniform(0.01, 100.0), 4),
                "Forex_Amount": round(random.uniform(100.0, 10000.0), 2),
                "Fraud_Alert_ID": fake.uuid4(),
                "Alert_Type": random.choice(["Unusual Activity", "Login Attempt", "High Spend"]),
                "Alert_Date": fake.date_between(start_date='-1y', end_date='today'),
                "Alert_Severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "Alert_Status": random.choice(["Resolved", "Open", "Investigating"]),
                "TIN": generate_tin(),
                "Passport_Number": generate_passport(),
                "MAC_Address": random_mac(),
                "IP_Address": fake.ipv4_public(),
                "Device_Type": random.choice(["Mobile", "Laptop", "Tablet", "Desktop"]),
                "Login_Timestamp": fake.date_time_this_year(),
                "Logout_Timestamp": fake.date_time_this_year(),
                "Failed_Login_Attempts": random.randint(0, 10),
                "Account_Locked": random.choice([True, False]),
                "Security_Questions_Set": random.choice([True, False]),
                "Last_Transaction_Location": fake.city(),
                "Annual_Income": round(random.uniform(5000.0, 100000.0), 2),
                "Monthly_Income": round(random.uniform(400.0, 10000.0), 2),
                "Monthly_Expenses": round(random.uniform(300.0, 9000.0), 2),
                "Employment_Status": random.choice(["Employed", "Unemployed", "Self-employed", "Student"]),
                "Employer_Name": fake.company(),
                "Employment_Start_Date": fake.date_between(start_date='-15y', end_date='-1y'),
                "Employment_Type": random.choice(["Full-time", "Part-time", "Contract"]),
                "Job_Title": fake.job(),
                "Industry": random.choice(["Finance", "Healthcare", "Technology", "Retail"]),
                "Investment_Account": random.choice([True, False]),
                "Portfolio_Value": round(random.uniform(0, 100000.0), 2),
                "Stock_Holdings": random.randint(0, 50),
                "Bond_Holdings": random.randint(0, 30),
                "Mutual_Funds": random.randint(0, 20),
                "Retirement_Account": random.choice([True, False]),
                "Retirement_Age": random.randint(55, 65),
                "Insurance_Policy_ID": fake.uuid4(),
                "Insurance_Type": random.choice(["Health", "Life", "Auto", "Home"]),
                "Insurance_Premium": round(random.uniform(100.0, 1000.0), 2),
                "Insurance_Coverage": round(random.uniform(10000.0, 100000.0), 2),
                "Beneficiary_Name": fake.name(),
                "Crypto_Wallet_Address": generate_crypto_wallet(),
                "Crypto_Balance": round(random.uniform(0.01, 10.0), 4),
                "Wallet_Type": random.choice(["Hardware", "Software", "Online"]),
                "Digital_Banking_Enabled": random.choice([True, False]),
                "Online_Shopping_Spend": round(random.uniform(100.0, 10000.0), 2),
                "Utility_Bill_Payments": round(random.uniform(50.0, 1000.0), 2),
                "Loan_Refinanced": random.choice([True, False]),
                "Customer_Segment": random.choice(["Retail", "Corporate", "SME", "HNI"]),
                "Vehicle_Loan_ID": fake.uuid4(),
                "Vehicle_Type": random.choice(["Sedan", "SUV", "Truck", "Motorbike", "Van"]),
                "Vehicle_Value": round(random.uniform(3000.0, 100000.0), 2),
                "Vehicle_Registration": f"{fake.random_uppercase_letter()}{random.randint(1000,9999)}{fake.random_uppercase_letter()}",
                "Vehicle_Loan_Status": random.choice(["Active", "Closed", "Defaulted"]),

                "Housing_Loan_ID": fake.uuid4(),
                "Property_Type": random.choice(["Apartment", "House", "Condo", "Land"]),
                "Property_Value": round(random.uniform(20000.0, 500000.0), 2),
                "Mortgage_Term": random.randint(10, 30),
                "Mortgage_Rate": round(random.uniform(1.5, 7.5), 2),

                "Rental_Status": random.choice(["Rented", "Owned", "Mortgaged"]),
                "Monthly_Rent": round(random.uniform(100.0, 2000.0), 2),
                "Lease_Term": random.randint(6, 36),
                "Landlord_Name": fake.name(),
                "Property_Location": fake.city(),

                "Overdraft_Protection": random.choice([True, False]),
                "Standing_Instructions": random.choice([True, False]),
                "Recurring_Transfers": random.randint(0, 10),
                "Nominee_Name": fake.name(),
                "Nominee_Relationship": random.choice(["Spouse", "Parent", "Sibling", "Child", "Friend"]),

                "Digital_Signature_Setup": random.choice([True, False]),
                "Mobile_Banking_Enabled": random.choice([True, False]),
                "Last_Mobile_Login": fake.date_time_this_year(),
                "Preferred_Language": random.choice(["Thai", "Bahasa", "English"]),
                "SMS_Alerts_Enabled": random.choice([True, False]),

                "Email_Alerts_Enabled": random.choice([True, False]),
                "Region": random.choice(["Bangkok", "Jakarta", "Chiang Mai", "Surabaya", "Bali"]),
                "Branch_ID": fake.random_int(min=1000, max=9999),
                "Branch_Location": fake.city(),
                "Service_Rating": round(random.uniform(1.0, 5.0), 1),

                "Customer_Feedback": fake.sentence(nb_words=6),
                "Support_Tickets": random.randint(0, 10),
                "Ticket_Resolution_Time": random.randint(1, 48),
                "Escalated_Tickets": random.randint(0, 2),
                "Support_Channel": random.choice(["Email", "Phone", "Chat", "Branch"]),

                "Cross_Border_Transactions": random.randint(0, 20),
                "Number_of_Beneficiaries": random.randint(0, 5),
                "Savings_Goal": round(random.uniform(1000.0, 100000.0), 2),
                "Savings_Progress": round(random.uniform(0.0, 100.0), 2),
                "Credit_Limit_Utilization": round(random.uniform(0.0, 100.0), 2),

                "Loan_Eligibility_Score": random.randint(0, 100),
                "Preapproved_Offers": random.randint(0, 3),
                "Debit_Card_Active": random.choice([True, False]),
                "Credit_Card_Active": random.choice([True, False]),
                "KYC_Completed": random.choice([True, False]),

                "AML_Flagged": random.choice([True, False]),                "PEP_Status": random.choice(["Yes", "No"]),
                "Watchlist_Match": random.choice([True, False]),
                "Transaction_Limit": round(random.uniform(500.0, 10000.0), 2),
                "Custom_Limit_Set": random.choice([True, False]),

                "Annual_Spending": round(random.uniform(1000.0, 50000.0), 2),
                "Top_Spending_Category": random.choice(["Groceries", "Travel", "Dining", "Shopping"]),
                "Frequent_Merchant": fake.company(),
                "Subscription_Services": random.choice(["Netflix", "Spotify", "YouTube Premium", "None"]),
                "Recurring_Charges": round(random.uniform(10.0, 100.0), 2),

                "Unusual_Activity_Flag": random.choice([True, False]),
                "Fraud_Cases_Reported": random.randint(0, 5),
                "Blacklist_Status": random.choice(["None", "Suspect", "Confirmed"]),
                "Account_Migration_Status": random.choice(["Not Started", "In Progress", "Completed"]),
                "Reactivation_Requests": random.randint(0, 3),

                "Marketing_Opt_In": random.choice([True, False]),
                "Push_Notifications_Enabled": random.choice([True, False]),
                "Two_Factor_Enabled": random.choice([True, False]),
                "Biometric_Auth_Enabled": random.choice([True, False]),
                "PIN_Changed_Recently": random.choice([True, False]),

                "Last_Password_Update": fake.date_between(start_date='-1y', end_date='today'),
                "Device_Count": random.randint(1, 5),
                "Primary_Device_OS": random.choice(["Android", "iOS", "Windows", "macOS"]),
                "Browser_Type": random.choice(["Chrome", "Firefox", "Edge", "Safari"]),
                "Last_Login_Device": random.choice(["Phone", "Tablet", "Laptop", "Desktop"]),

                "Reward_Points": random.randint(0, 50000),
                "Reward_Redemption_Rate": round(random.uniform(0.0, 100.0), 2),
                "Cashback_Earned": round(random.uniform(0.0, 500.0), 2),
                "Loyalty_Level": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
                "Referral_Code": fake.lexify(text="??????"),

                "Referred_By": fake.name(),
                "Campaign_Signup": random.choice([True, False]),
                "Survey_Participation": random.choice([True, False]),
                "Complaint_Status": random.choice(["Open", "Closed", "Escalated", "Pending"]),
                "Satisfaction_Score": round(random.uniform(1.0, 10.0), 1),

                "Time_with_Bank": random.randint(1, 30),
                "Dormancy_Flag": random.choice([True, False]),
                "Tax_Compliance": random.choice(["Compliant", "Non-Compliant"]),
                "Interest_Accrued": round(random.uniform(0.0, 10000.0), 2),
                "Penalty_Interest": round(random.uniform(0.0, 200.0), 2),

                "Loan_Restructure_Status": random.choice(["None", "Requested", "Approved"]),
                "Account_Type_Changed": random.choice([True, False]),
                "Credit_Score_Source": random.choice(["Equifax", "TransUnion", "Experian"]),
                "Credit_Score_Update": fake.date_between(start_date='-1y', end_date='today'),
                "Income_Verification_Status": random.choice(["Verified", "Pending", "Failed"]),

                "Digital_Documents_Submitted": random.choice([True, False]),
                "Verification_Channel": random.choice(["Online", "Branch", "Phone"]),
                "Digital_KYC_Flag": random.choice([True, False]),
                "Crypto_Transactions_Enabled": random.choice([True, False]),
                "Payment_Gateway_Used": random.choice(["Stripe", "PayPal", "Bank API", "None"])
                }
                writer.writerow(row)
                if i % 10000 == 0:
                    print(f"  wrote {i} rows")


print(f"Dataset written to: {file_path}")