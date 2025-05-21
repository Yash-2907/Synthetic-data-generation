import csv
import random
import os
from faker import Faker
import string

# Output directory
base_dir = os.path.join(os.getcwd(), "benchmark_test", "schema_3", "output")
os.makedirs(base_dir, exist_ok=True)

# Faker with Thai and Indonesian locales only
fake = Faker(["th_TH", "id_ID"])
Faker.seed(3033)

# Config
num_files = 4999
min_cols = 15
max_cols = 25
min_size = 1 * 1024 * 1024
max_size = 5 * 1024 * 1024
estimated_row_size = 500
email_domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]

# Sensitive fields (always include 3–4 per file)
sensitive_fields = [
    "Thai_ID", "TIN", "Passport_Number", "Phone_Number", "Email",
    "Card_Number", "SSN", "Driver_License_Number", "National_Insurance_ID", "Medical_Record_ID"
]

# Full column pool
field_pool = [
    "Full_Name", "Date_of_Birth", "Nationality", "Gender", "Region", "City", "Postal_Code",
    "Device_Type", "Device_OS", "App_Version", "Device_ID", "MAC_Address", "IP_Address",
    "Session_ID", "Login_Method", "Time_Spent_Minutes", "Session_Abandoned", "Top_Feature_Used",
    "Scroll_Depth", "Clicks", "Crash_Count", "Page_Visits", "In_App_Purchase", "Consent_Tracking",
    "Customer_Segment", "Preferred_Channel", "Last_Campaign", "Opted_Into_Offers", "Referral_Code",
    "Blood_Type", "Allergies", "Chronic_Conditions", "Diagnosis_Code", "Last_Visit_Date", "Insured",
    "Medical_Record_ID", "Satisfaction_Score", "Feedback_Summary", "Complaint_Status", "Reported_Bugs",
    "Degree", "Graduation_Year", "Institution_Name", "Field_of_Study", "Work_Email", "HR_ID",
    "Employer_Name", "Card_Type", "Card_Expiry", "IBAN", "SWIFT_Code", "Currency", "Account_Locked",
    "Order_ID", "Product_Name", "Product_Price", "Shipping_Country", "Payment_Method", "Discount_Code",
    "Tracking_ID", "Tax_File_Number"
]

# Generators
def generate_thai_id():
    digits = [random.randint(0, 9) for _ in range(12)]
    total = sum((13 - i) * digit for i, digit in enumerate(digits))
    check = (11 - total % 11) % 10
    return f"{digits[0]}-{''.join(map(str, digits[1:5]))}-{''.join(map(str, digits[5:10]))}-{''.join(map(str, digits[10:12]))}-{check}"

def generate_passport(): return random.choice(["TH", "ID"]) + ''.join(random.choices(string.digits, k=7))
def generate_tin(): return str(random.randint(1000000000000, 9999999999999))
def generate_ssn(): return f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
def generate_driver_license(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
def generate_insurance_id(): return f"NI-{random.randint(1000000,9999999)}"
def generate_email(name): return f"{name.lower().replace(' ','.')}{random.randint(1,9999)}@{random.choice(email_domains)}"
def generate_tracking_id(): return f"TRK{random.randint(1000000000, 9999999999)}"
def generate_tax_file(): return f"TFN{random.randint(100000,999999)}"

# Generate files
for i in range(1, num_files + 1):
    file_name = f"table_{i:04d}.csv"
    file_path = os.path.join(base_dir, file_name)

    n_cols = random.randint(min_cols, max_cols)
    base_cols = random.sample([f for f in field_pool if f not in sensitive_fields], n_cols - 4)
    sens_cols = random.sample(sensitive_fields, 4)
    columns = base_cols + sens_cols
    random.shuffle(columns)

    target_size = random.randint(min_size, max_size)
    num_rows = target_size // estimated_row_size

    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for _ in range(num_rows):
            name = fake.name()
            row = {
                "Full_Name": name,
                "Date_of_Birth": fake.date_of_birth(minimum_age=18, maximum_age=90),
                "Nationality": random.choice(["Thai", "Indonesian"]),
                "Gender": random.choice(["Male", "Female", "Other"]),
                "Phone_Number": fake.phone_number(),
                "Email": generate_email(name),
                "Thai_ID": generate_thai_id(),
                "TIN": generate_tin(),
                "Passport_Number": generate_passport(),
                "SSN": generate_ssn(),
                "Driver_License_Number": generate_driver_license(),
                "National_Insurance_ID": generate_insurance_id(),
                "Medical_Record_ID": fake.uuid4(),
                "Tax_File_Number": generate_tax_file(),

                # Device / session
                "Device_Type": random.choice(["Mobile", "Tablet", "Desktop"]),
                "Device_OS": random.choice(["Android", "iOS", "Windows", "Linux"]),
                "App_Version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
                "Device_ID": fake.uuid4(),
                "MAC_Address": ":".join([f"{random.randint(0,255):02x}" for _ in range(6)]),
                "IP_Address": fake.ipv4_public(),
                "Session_ID": fake.uuid4(),
                "Login_Method": random.choice(["Password", "OTP", "Biometric"]),
                "Time_Spent_Minutes": random.randint(1, 180),
                "Session_Abandoned": random.choice(["Yes", "No"]),
                "Top_Feature_Used": random.choice(["Search", "Cart", "Profile"]),
                "Scroll_Depth": random.choice(["25%", "50%", "75%", "100%"]),
                "Clicks": random.randint(5, 200),
                "Crash_Count": random.randint(0, 5),
                "Page_Visits": random.randint(1, 100),
                "In_App_Purchase": random.choice(["Yes", "No"]),
                "Consent_Tracking": random.choice(["Yes", "No"]),

                # Feedback / profile
                "Satisfaction_Score": round(random.uniform(1.0, 10.0), 1),
                "Feedback_Summary": fake.sentence(nb_words=5),
                "Complaint_Status": random.choice(["Open", "Resolved", "Escalated"]),
                "Reported_Bugs": random.randint(0, 5),
                "Customer_Segment": random.choice(["Retail", "SMB", "Enterprise"]),
                "Preferred_Channel": random.choice(["Email", "SMS", "App"]),
                "Last_Campaign": random.choice(["Q1Launch", "HolidayPromo"]),
                "Opted_Into_Offers": random.choice(["Yes", "No"]),
                "Referral_Code": fake.bothify(text='REF###??'),

                # Medical
                "Blood_Type": random.choice(["A", "B", "AB", "O"]),
                "Allergies": random.choice(["None", "Peanuts", "Dust", "Pollen"]),
                "Chronic_Conditions": random.choice(["None", "Diabetes", "Asthma"]),
                "Diagnosis_Code": f"I{random.randint(10,99)}.{random.randint(0,9)}",
                "Last_Visit_Date": fake.date_this_year(),
                "Insured": random.choice(["Yes", "No"]),

                # Education
                "Degree": random.choice(["Bachelors", "Masters", "Diploma"]),
                "Graduation_Year": random.randint(2000, 2024),
                "Institution_Name": fake.company() + " University",
                "Field_of_Study": random.choice(["Finance", "Computer Science", "Nursing"]),
                "Work_Email": generate_email(name),
                "HR_ID": f"HR{random.randint(10000,99999)}",

                # Finance / Orders
                "Card_Number": fake.credit_card_number(),
                "Card_Type": random.choice(["Debit", "Credit"]),
                "Card_Expiry": fake.credit_card_expire(),
                "IBAN": fake.iban(),
                "SWIFT_Code": fake.swift(),
                "Currency": random.choice(["THB", "IDR", "USD"]),
                "Account_Locked": random.choice(["Yes", "No"]),
                "Order_ID": fake.uuid4(),
                "Product_Name": fake.word().title(),
                "Product_Price": round(random.uniform(10, 500), 2),
                "Shipping_Country": random.choice(["Thailand", "Indonesia", "Vietnam"]),
                "Payment_Method": random.choice(["Card", "Wallet", "Cash"]),
                "Discount_Code": fake.lexify(text="DISC####"),
                "Tracking_ID": generate_tracking_id(),

                # Location
                "Region": random.choice(["Bangkok", "Jakarta", "Chiang Mai"]),
                "City": fake.city(),
                "Postal_Code": fake.postcode(),
                "Employer_Name": fake.company()
            }

            writer.writerow({col: row[col] for col in columns})

    print(f"✅ {file_name} generated with {num_rows} rows")

print("🎉 All 4,999 small tables for schema_3 generated successfully.")
