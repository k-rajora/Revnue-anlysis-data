import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)

# -----------------------------
# CONFIG (UPDATED)
# -----------------------------
START_DATE = "2019-01-01"
END_DATE = "2024-12-31"

BASE_EMPLOYEES = 40
EMPLOYEE_GROWTH_PER_YEAR = 4

NUM_PROJECTS = 35
WORK_HOURS_PER_DAY = 8

roles = {
    "Analyst": {"cost": 18},
    "Consultant": {"cost": 28},
    "Senior Consultant": {"cost": 45},
    "Manager": {"cost": 70}
}

practices = ["Consulting", "Risk", "Audit"]
locations = ["India", "US", "UK"]
industries = ["BFSI", "Tech", "Retail", "Healthcare"]






# -----------------------------
# CALENDAR TABLE
# -----------------------------
dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")
calendar = pd.DataFrame({"date": dates})
calendar["is_working_day"] = calendar["date"].dt.weekday < 5
calendar["month"] = calendar["date"].dt.to_period("M").astype(str)

calendar.to_csv("calendar.csv", index=False)

# -----------------------------
# EMPLOYEES TABLE
# -----------------------------

employees = []
employee_id = 100

for year in range(2019, 2025):
    num_employees = BASE_EMPLOYEES + (year - 2019) * EMPLOYEE_GROWTH_PER_YEAR
    
    for i in range(num_employees):
        role = random.choice(list(roles.keys()))
        employees.append({
            "employee_id": f"E{employee_id}",
            "employee_name": f"Employee_{employee_id}",
            "role": role,
            "practice": random.choice(practices),
            "location": random.choice(locations),
            "hourly_cost": roles[role]["cost"],
            "hire_date": pd.Timestamp(f"{year}-01-01") + 
                         pd.to_timedelta(random.randint(0, 300), unit="D")
        })
        employee_id += 1

employees_df = pd.DataFrame(employees)
employees_df.to_csv("employees.csv", index=False)


# -----------------------------
# PROJECTS TABLE
# -----------------------------
# -----------------------------
# PROJECTS TABLE (FIXED)
# -----------------------------
projects = []

for i in range(NUM_PROJECTS):
    start = pd.Timestamp("2019-01-01") + pd.to_timedelta(
        random.randint(0, 900), unit="D"
    )

    # LONG-RUNNING projects (2–4 years)
    end = start + pd.to_timedelta(
        random.randint(720, 1440), unit="D"
    )

    projects.append({
        "project_id": f"P{200+i}",
        "project_name": f"Project_{i+1}",
        "client_industry": random.choice(industries),
        "billing_rate": random.randint(100, 160),
        "project_start": start,
        "project_end": end,
        "practice": random.choice(practices)
    })

projects_df = pd.DataFrame(projects)
projects_df.to_csv("projects.csv", index=False)







# TIME ENTRIES TABLE
# -----------------------------

time_entries = []
entry_id = 1000

for _, emp in employees_df.iterrows():
    base_utilization = np.random.uniform(0.72, 0.85)

    for date in calendar[calendar["is_working_day"]]["date"]:
        # Seasonal dip in Nov–Dec
        if date.month in [11, 12]:
            utilization = base_utilization - 0.12
        else:
            utilization = base_utilization

        utilization = max(utilization, 0.6)

        is_billable = np.random.rand() < utilization
        hours = np.random.randint(6, 9)

        if is_billable:
            active_projects = projects_df[
                (projects_df["practice"] == emp["practice"]) &
                (projects_df["project_start"] <= date) &
                (projects_df["project_end"] >= date)
            ]

            if len(active_projects) > 0:
                project = active_projects.sample(1).iloc[0]
                project_id = project["project_id"]
                billable_flag = "Yes"
            else:
                project_id = ""
                billable_flag = "No"
        else:
            project_id = ""
            billable_flag = "No"

        time_entries.append({
            "entry_id": f"T{entry_id}",
            "employee_id": emp["employee_id"],
            "project_id": project_id,
            "work_date": date,
            "hours_logged": hours,
            "billable_flag": billable_flag
        })

        entry_id += 1

time_entries_df = pd.DataFrame(time_entries)
time_entries_df.to_csv("time_entries.csv", index=False)

print("LARGE realistic dataset generation complete!")


















