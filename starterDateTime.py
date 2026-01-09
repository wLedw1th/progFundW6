from datetime import datetime
import re

# Function without libraries
def time_remaining_manual(deadline_str):
    # Support formats: DD/MM/YYYY HH:MM, YYYY-MM-DD HH:MM
    match = re.match(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s+(\d{1,2}):(\d{2})', deadline_str)
    
    if match:
        day, month, year, hour, minute = map(int, match.groups())
        # Assume UK format if day > 12
        if day > 12:
            day, month = month, day
    else:
        print("Invalid format. Use DD/MM/YYYY HH:MM or YYYY-MM-DD HH:MM")
        return
    
    # Simple epoch calculation (not accounting for leap years perfectly)
    def to_seconds(d, m, y, h, mn):
        days = (y - 1970) * 365 + (y - 1969) // 4
        days += sum([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][:m-1]) + d
        return days * 86400 + h * 3600 + mn * 60
    
    now_seconds = to_seconds(1, 1, 1970, 0, 0)  # Placeholder
    deadline_seconds = to_seconds(day, month, year, hour, minute)
    
    remaining = deadline_seconds - now_seconds
    days = remaining // 86400
    hours = (remaining % 86400) // 3600
    minutes = (remaining % 3600) // 60
    
    print(f"Time remaining: {days} days, {hours} hours, {minutes} minutes")


# Function with datetime
def time_remaining_datetime(deadline_str, timezone=None):
    formats = ["%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M"]
    deadline = None
    
    for fmt in formats:
        try:
            deadline = datetime.strptime(deadline_str, fmt)
            break
        except ValueError:
            continue
    
    if not deadline:
        print("Invalid format. Use DD/MM/YYYY HH:MM or YYYY-MM-DD HH:MM")
        return
    
    now = datetime.now()
    remaining = deadline - now
    
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes = remainder // 60
    
    print(f"Time remaining: {days} days, {hours} hours, {minutes} minutes")


# Main
if __name__ == "__main__":
    deadline = input("Enter deadline (DD/MM/YYYY HH:MM or YYYY-MM-DD HH:MM): ")
    print("\nUsing datetime library:")
    time_remaining_datetime(deadline)