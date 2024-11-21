import sqlite3
from datetime import datetime, timedelta

# Updated shift times
SHIFT_TYPES = ["Morning", "Afternoon", "Night"]
SHIFT_HOURS = {
    "Morning": (6, 14),  # 6 AM to 2 PM
    "Afternoon": (14, 22),  # 2 PM to 10 PM
    "Night": (22, 6)  # 10 PM to 6 AM
}

def generate_weekly_schedule(cursor, start_date):
    """
    Generate a weekly schedule for all employees, respecting required_hours.
    """
    # Fetch all employees with their required hours
    cursor.execute("SELECT employee_id, name, required_hours FROM Employees")
    employees = cursor.fetchall()

    if not employees:
        print("No employees found in the database.")
        return

    # Initialize a dictionary to track scheduled hours for each employee
    scheduled_hours = {employee[0]: 0 for employee in employees}

    # Loop through each day of the week (7 days)
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    shifts = []

    for day in range(7):  # 7 days in a week
        for employee in employees:
            employee_id, name, required_hours = employee

            # Skip scheduling if the employee has met their required hours
            if scheduled_hours[employee_id] >= required_hours:
                continue

            # Assign a shift to the employee
            shift_type = SHIFT_TYPES[day % len(SHIFT_TYPES)]  # Rotate shifts
            start_hour, end_hour = SHIFT_HOURS[shift_type]

            # Calculate hours for the shift
            available_hours = required_hours - scheduled_hours[employee_id]
            shift_hours = min(end_hour - start_hour, available_hours, 8)  # Max shift is 8 hours

            # Handle the case where the Night shift crosses midnight (end time < start time)
            if shift_type == "Night" and end_hour < start_hour:
                # Schedule for 10 PM - 6 AM shift
                end_time = current_date.replace(hour=end_hour, minute=0, second=0)
                end_time += timedelta(days=1)  # Go to the next day for the Night shift end time
            else:
                # Regular shift
                end_time = current_date.replace(hour=end_hour, minute=0, second=0)

            start_time = current_date.replace(hour=start_hour, minute=0, second=0)

            # Add the shift to the schedule
            shifts.append((employee_id, start_time, end_time, shift_type, shift_hours, current_date.date()))
            scheduled_hours[employee_id] += shift_hours

        # Increment the date to the next day
        current_date += timedelta(days=1)

    # Insert the shifts into the database
    cursor.executemany("""
    INSERT INTO ShiftSchedules (employee_id, start_time, end_time, shift_type, hours, date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, shifts)
    print(f"Weekly schedule generated starting from {start_date}.")

if __name__ == "__main__":
    conn = sqlite3.connect("MES.db")
    cursor = conn.cursor()

    # Generate schedule for the week starting from a specific date
    start_date = "2024-11-13"  # Example start date (YYYY-MM-DD)
    generate_weekly_schedule(cursor, start_date)

    # Commit changes and close
    conn.commit()
    conn.close()