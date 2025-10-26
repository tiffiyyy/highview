import boto3
from lambdas.utils import make_student_id, normalize_email
import csv
from decimal import Decimal
import uuid

STUDENTS_TABLE = "Student"
SESSIONS_TABLE = "Session"
ATTENDANCE_TABLE = "Attendance"
BONUS_TABLE = "BonusPoints"

STUDENTS_CSV = "dummyData/students.csv"
ATTENDANCE_CSV = "dummyData/attendance.csv"
BONUS_POINTS_CSV = "dummyData/bonus_points.csv"
SESSIONS_CSV = "dummyData/sessions.csv"

def to_decimal(x):
    # dynamoDB requires Decimal
    return Decimal(str(x))

def batch_write(table, items, pk_hint=None):
    with table.batch_writer(overwrite_by_pkeys=pk_hint or []) as batch:
        for it in items:
            batch.put_item(Item=it)

def load_students(dynamodb):
    table = dynamodb.Table(STUDENTS_TABLE)
    email_to_sid = {}
    items = []
    with open(STUDENTS_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            first = r.get("First","")
            last  = r.get("Last","")
            email = r.get("email","")
            sid   = make_student_id(first, last, email)
            email_to_sid[normalize_email(email)] = sid
            items.append({
                "student_id": sid,
                "first": first,
                "last": last,
                "email": normalize_email(email),
                "company": r.get("Company",""),
            })
    batch_write(table, items, pk_hint=["student_id"])
    print(f"Loaded {len(items)} students.")
    return email_to_sid


def load_sessions(dynamodb):
    table = dynamodb.Table(SESSIONS_TABLE)
    items = []
    with open(SESSIONS_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            items.append({
                "session_id": str(uuid.uuid4()),
                # "session_id": r["session_id"],
                "session_name": r["session_name"],
                "session_type": r["session_type"],
                "session_date": r["session_date"],
            })
    batch_write(table, items, pk_hint=["session_id"])
    print(f"Loaded {len(items)} sessions.")

def load_attendance(dynamodb, email_to_sid):
    table = dynamodb.Table(ATTENDANCE_TABLE)
    items = []
    with open(ATTENDANCE_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            email = normalize_email(r["student_email"])
            sid = email_to_sid.get(email)
            if not sid:
                raise ValueError(f"Attendance references unknown student_email: {email}")
            points = to_decimal(r["points"])
            items.append({
                "student_id": sid,
                "session_id": r["session_id"],
                "points": points,
            })
    batch_write(table, items)
    print(f"Loaded {len(items)} attendance rows.")

def load_bonus_points(dynamodb, email_to_sid):
    table = dynamodb.Table(BONUS_TABLE)
    items = []
    with open(BONUS_POINTS_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            email = normalize_email(r["student_email"])
            sid = email_to_sid.get(email)
            if not sid:
                raise ValueError(f"Bonus references unknown student_email: {email}")
            points = to_decimal(r["points"])
            items.append({
                "student_id": sid,
                "bonus_type": r["bonus_type"],
                "points": points,
            })
    batch_write(table, items)
    print(f"Loaded {len(items)} bonus rows.")


if __name__ == "__main__":
    dynamodb = boto3.resource("dynamodb")
    email_to_sid = load_students(dynamodb)
    load_sessions(dynamodb)
    load_attendance(dynamodb, email_to_sid)
    load_bonus_points(dynamodb, email_to_sid)
