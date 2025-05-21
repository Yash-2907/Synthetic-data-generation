import csv
import random
import os
from faker import Faker
import string

# Output directory
base_dir = os.path.join(os.getcwd(), "benchmark_test", "schema_2", "output")
os.makedirs(base_dir, exist_ok=True)

# Faker with Thai and Indonesian only
fake = Faker(["th_TH", "id_ID"])
Faker.seed(2025)

# Config
num_files = 999
min_size_bytes = 2 * 1024 * 1024
max_size_bytes = 6 * 1024 * 1024
row_size_bytes = 500

email_domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]

# Valid sensitive fields
sensitive_fields = [
    "Thai_ID", "TIN", "Passport_Number", "Email", "Phone_Number", "Card_Number",
    "National_Insurance_ID", "Driver_License_Number", "SSN", "Medical_Record_ID"
]

# Column pool including financial/medical/edu/etc.
column_pool = [
    "Full_Name", "Gender", "Date_of_Birth", "Nationality",
    "MAC_Address", "IP_Address", "Device_OS", "Login_Method", "Device_ID", "App_Version",
    "Geolocation", "Browser_Type", "Blood_Type", "Allergies", "Chronic_Conditions",
    "Insurance_Provider", "Diagnosis_Code", "Last_Visit_Date", "Insurance_Status",
    "Highest_Degree", "Institution_Name", "Graduation_Year", "Field_of_Study", "Education_Level",
    "Enrollment_ID", "Current_CGPA", "Class_Rank", "Employment_Status", "Employer_Name",
    "Job_Title", "HR_Employee_ID", "Work_Email", "Order_ID", "Purchase_ID", "Product_Name",
    "Product_Category", "Product_Price", "Discount_Code", "Payment_Method", "Tracking_ID",
    "Shipping_Country", "Card_Type", "Card_Expiry", "SWIFT_Code", "IBAN", "Currency",
    "Support_Tickets", "Satisfaction_Score", "Complaint_Status", "Feedback_Notes",
    "Region", "City", "Postal_Code", "Session_ID", "Time_Spent_Minutes", "Device_Type"
]

# Field generators
def generate_thai_id():
    digits = [random.randint(0, 9) for _ in range(12)]
    total = sum((13 - i) * digit for i, digit in enumerate(digits))
    check_digit = (11 - total % 11) % 10
    return f"{digits[0]}-{''.join(map(str, digits[1:5]))}-{''.join(map(str, digits[5:10]))}-{''.join(map(str, digits[10:12]))}-{check_digit}"

def generate_passport(): return random.choice(["TH", "ID"]) + ''.join(random.choices(string.digits, k=7))
def generate_tin(): return str(random.randint(1000000000000, 9999999999999))
def generate_ssn(): return f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
def generate_driver_license(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
def generate_insurance_id(): return f"NI-{random.randint(1000000,9999999)}"
def generate_email(name): return f"{name.lower().replace(' ','.')}{random.randint(1,9999)}@{random.choice(email_domains)}"
def generate_mac(): return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
def generate_tracking_id(): return f"TRK{random.randint(1000000000, 9999999999)}"

# Generate files
for i in range(1, num_files + 1):
    file_name = f"table_{i:03d}.csv"
    file_path = os.path.join(base_dir, file_name)

    base_cols = random.sample([c for c in column_pool if c not in sensitive_fields], 16)
    sens_cols = random.sample(sensitive_fields, 4)
    columns = base_cols + sens_cols
    random.shuffle(columns)

    target_size = random.randint(min_size_bytes, max_size_bytes)
    num_rows = target_size // row_size_bytes

    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for _ in range(num_rows):
            name = fake.name()
            row = {
                "Full_Name": name,
                "Gender": random.choice(["Male", "Female", "Other"]),
                "Date_of_Birth": fake.date_of_birth(minimum_age=18, maximum_age=90),
                "Nationality": random.choice(["Thai", "Indonesian"]),
                "Phone_Number": fake.phone_number(),
                "Email": generate_email(name),
                "Thai_ID": generate_thai_id(),
                "TIN": generate_tin(),
                "Passport_Number": generate_passport(),
                "SSN": generate_ssn(),
                "Driver_License_Number": generate_driver_license(),
                "National_Insurance_ID": generate_insurance_id(),
                "Medical_Record_ID": fake.uuid4(),

                "MAC_Address": generate_mac(),
                "IP_Address": fake.ipv4_public(),
                "Device_ID": fake.uuid4(),
                "Device_OS": random.choice(["Windows", "Linux", "Android", "iOS"]),
                "Login_Method": random.choice(["Password", "OTP", "Biometric"]),
                "App_Version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
                "Browser_Type": random.choice(["Chrome", "Safari", "Firefox"]),
                "Geolocation": fake.city(),

                "Blood_Type": random.choice(["A", "B", "AB", "O"]),
                "Allergies": random.choice(["None", "Dust", "Peanuts"]),
                "Chronic_Conditions": random.choice(["None", "Diabetes", "Hypertension"]),
                "Insurance_Provider": fake.company(),
                "Diagnosis_Code": f"I{random.randint(10,99)}.{random.randint(0,9)}",
                "Last_Visit_Date": fake.date_this_year(),
                "Insurance_Status": random.choice(["Insured", "Uninsured"]),

                "Highest_Degree": random.choice(["Diploma", "Bachelors", "Masters"]),
                "Institution_Name": fake.company() + " University",
                "Graduation_Year": random.randint(2000, 2024),
                "Field_of_Study": random.choice(["IT", "Finance", "Biology"]),
                "Education_Level": random.choice(["Secondary", "Tertiary"]),
                "Enrollment_ID": fake.uuid4(),
                "Current_CGPA": round(random.uniform(2.0, 4.0), 2),
                "Class_Rank": random.randint(1, 100),

                "Employment_Status": random.choice(["Employed", "Freelancer"]),
                "Employer_Name": fake.company(),
                "Job_Title": fake.job(),
                "HR_Employee_ID": f"HR{random.randint(10000,99999)}",
                "Work_Email": generate_email(name),

                "Order_ID": fake.uuid4(),
                "Purchase_ID": fake.uuid4(),
                "Product_Name": fake.word().title(),
                "Product_Category": random.choice(["Tech", "Books", "Health"]),
                "Product_Price": round(random.uniform(10, 500), 2),
                "Discount_Code": fake.lexify(text="DISC????"),
                "Payment_Method": random.choice(["Credit", "Debit", "Wallet"]),
                "Tracking_ID": generate_tracking_id(),
                "Shipping_Country": random.choice(["Thailand", "Indonesia", "Singapore"]),

                "Card_Number": fake.credit_card_number(),
                "Card_Type": random.choice(["Debit", "Credit"]),
                "Card_Expiry": fake.credit_card_expire(),
                "SWIFT_Code": fake.swift(),
                "IBAN": fake.iban(),
                "Currency": random.choice(["THB", "IDR", "USD"]),

                "Support_Tickets": random.randint(0, 10),
                "Satisfaction_Score": round(random.uniform(1.0, 10.0), 1),
                "Complaint_Status": random.choice(["Open", "Closed", "Escalated"]),
                "Feedback_Notes": fake.sentence(),

                "Region": random.choice(["Bangkok", "Chiang Mai", "Jakarta"]),
                "City": fake.city(),
                "Postal_Code": fake.postcode(),

                "Session_ID": fake.uuid4(),
                "Time_Spent_Minutes": random.randint(1, 240),
                "Device_Type": random.choice(["Mobile", "Desktop", "Tablet"])
            }

            writer.writerow({col: row[col] for col in columns})

    print(f"✅ Created {file_name} with ~{num_rows} rows")

print("🎉 All 999 files for schema_2 generated and finalized.")
