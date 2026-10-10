
import pandas as pd
import random
from datetime import datetime, timedelta

def load_data():
    random.seed(42)

    employees = [
        "Aarav", "Diya", "Kabir",
        "Priya", "Rohan", "Meera",
        "Ishaan", "Ananya"
    ]

    slices = ["Slice A", "Slice B", "Slice C", "Slice D"]

    records = []
    start_date = datetime(2026, 9, 1)

    for day in range(30):
        current_date = start_date + timedelta(days=day)

        for employee in employees:
            work_slice = random.choice(slices)
            assigned = 24
            completed = random.randint(18, 24)
            dents = random.randint(0, 4)
            quality = random.randint(82, 100)

            records.append({
                "date": current_date,
                "analyst": employee,
                "slice": work_slice,
                "tasks_assigned": assigned,
                "tasks_completed": completed,
                "dents": dents,
                "quality_score": quality
            })

    df = pd.DataFrame(records)

    df["completion_rate"] = (
        df["tasks_completed"] / df["tasks_assigned"] * 100
    ).round(1)

    df["pending_tasks"] = (
        df["tasks_assigned"] - df["tasks_completed"]
    )

    df["dent_rate"] = (
        df["dents"] / df["tasks_completed"] * 100
    ).round(2)

    return df
