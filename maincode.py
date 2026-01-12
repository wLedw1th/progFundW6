import csv
from datetime import datetime

# Pricing table
PRICING = {
    "Standard": {"Child": 6.00, "Teen": 8.00, "Adult": 12.00, "VIP": 20.00},
    "Premium": {"Child": 8.00, "Teen": 10.00, "Adult": 15.00, "VIP": 25.00}
}
VAT_RATE = 0.20
MATCHES = [
    "Thunderbolts vs Hurricanes",
    "Iron Titans vs Steel Crushers",
    "Blaze Warriors vs Storm Riders",
    "Shadow Hawks vs Flame Strikers",
    "Titan Clash Championship"
]
BOOKINGS_FILE = "bookings.csv"

def display_matches():
    print("\nAvailable Matches:")
    for i, match in enumerate(MATCHES, 1):
        print(f"{i}. {match}")

def calculate_total(ticket_types, quantities, match_type):
    subtotal = 0
    for ticket_type, quantity in zip(ticket_types, quantities):
        subtotal += PRICING[match_type][ticket_type] * quantity
    vat = subtotal * VAT_RATE
    total = subtotal + vat
    return subtotal, vat, total

def book_tickets():
    print("\n--- Ticket Booking ---")
    
    # Select match
    display_matches()
    match_choice = int(input("Select match number: ")) - 1
    selected_match = MATCHES[match_choice]
    
    # Match type
    match_type = input("Select match type (Standard/Premium): ")
    
    # Match date
    match_date = input("Enter match date (YYYY-MM-DD): ")
    
    # Ticket quantities
    ticket_types = ["Child", "Teen", "Adult", "VIP"]
    quantities = []
    print("\nEnter quantity for each ticket type:")
    for ticket_type in ticket_types:
        qty = int(input(f"{ticket_type}: "))
        quantities.append(qty)
    
    # Customer details
    name = input("\nEnter your name: ")
    contact = input("Enter your contact number: ")
    
    # Calculate totals
    subtotal, vat, total = calculate_total(ticket_types, quantities, match_type)
    
    # Display summary
    print(f"\n--- Booking Summary ---")
    print(f"Match: {selected_match}")
    print(f"Date: {match_date}")
    print(f"Type: {match_type}")
    for ticket_type, qty in zip(ticket_types, quantities):
        print(f"{ticket_type}: {qty}")
    print(f"Subtotal: £{subtotal:.2f}")
    print(f"VAT (20%): £{vat:.2f}")
    print(f"Total: £{total:.2f}")
    
    # Save booking
    booking_data = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Contact": contact,
        "Match": selected_match,
        "Match Date": match_date,
        "Type": match_type,
        "Child": quantities[0],
        "Teen": quantities[1],
        "Adult": quantities[2],
        "VIP": quantities[3],
        "Total": f"£{total:.2f}"
    }
    
    save_booking(booking_data)
    print("\n✓ Booking saved successfully!")

def save_booking(booking_data):
    try:
        with open(BOOKINGS_FILE, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=booking_data.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(booking_data)
    except Exception as e:
        print(f"Error saving booking: {e}")

def view_bookings():
    print("\n--- All Bookings ---")
    try:
        with open(BOOKINGS_FILE, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if not rows:
                print("No bookings found.")
                return
            for i, row in enumerate(rows, 1):
                print(f"\nBooking {i}:")
                for key, value in row.items():
                    print(f"  {key}: {value}")
    except FileNotFoundError:
        print("No bookings file found.")

def main():
    while True:
        print("\n--- SportZone Events Booking System ---")
        print("1. Book Tickets")
        print("2. View All Bookings (Admin)")
        print("3. Exit")
        
        choice = input("Select option: ")
        
        if choice == "1":
            book_tickets()
        elif choice == "2":
            view_bookings()
        elif choice == "3":
            print("Thank you for using SportZone Events!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()