# ============================================================================
# SPORTZONE EVENTS BOOKING SYSTEM - WITH LOGIN
# ============================================================================
# This program allows users to book sports event tickets and admins to view all bookings.
# Features: Login system with user/admin accounts, ticket booking, and booking management.
# ============================================================================

import csv
from datetime import datetime

# ============================================================================
# CONFIGURATION AND DATA SETUP
# ============================================================================

# Define the file where bookings will be saved
BOOKINGS_FILE = "bookings.csv"

# Define available sports matches that customers can book tickets for
MATCHES = [
    "Thunderbolts vs Hurricanes",
    "Iron Titans vs Steel Crushers",
    "Blaze Warriors vs Storm Riders",
    "Shadow Hawks vs Flame Strikers",
    "Titan Clash Championship"
]

# Define ticket prices for different ticket types and match types
# Structure: Match Type -> Ticket Category -> Price
PRICING = {
    "Standard": {"Child": 6.00, "Teen": 8.00, "Adult": 12.00, "VIP": 20.00},
    "Premium": {"Child": 8.00, "Teen": 10.00, "Adult": 15.00, "VIP": 25.00}
}

# VAT (Value Added Tax) rate - 20% in this case
VAT_RATE = 0.20

# Define login credentials - username and password for regular users and admins
# Format: "username": "password"
USER_ACCOUNTS = {
    "user": "password123"
}

ADMIN_ACCOUNTS = {
    "admin": "admin123"
}

# ============================================================================
# LOGIN FUNCTIONS
# ============================================================================

def login():
    """
    Handles the login process for the system.
    Allows users to log in as either a regular user or an admin.
    Returns a tuple: (login_type, username) where login_type is "user" or "admin"
    """
    # Keep asking for login until successful
    while True:
        print("\n" + "="*50)
        print("SPORTZONE EVENTS - LOGIN")
        print("="*50)
        print("1. Login as User")
        print("2. Login as Admin")
        print("3. Exit Program")
        
        # Get user's choice
        login_choice = input("\nSelect option (1-3): ")
        
        # If user wants to exit
        if login_choice == "3":
            print("\nGoodbye!")
            return None
        
        # If user wants to log in as a regular user
        elif login_choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            
            # Check if username and password match what's stored
            if username in USER_ACCOUNTS and USER_ACCOUNTS[username] == password:
                print(f"\nWelcome, {username}!")
                return ("user", username)
            else:
                print("Invalid username or password. Try again.")
        
        # If user wants to log in as an admin
        elif login_choice == "2":
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            
            # Check if username and password match what's stored for admins
            if username in ADMIN_ACCOUNTS and ADMIN_ACCOUNTS[username] == password:
                print(f"\nWelcome, Admin {username}!")
                return ("admin", username)
            else:
                print("Invalid admin username or password. Try again.")
        
        else:
            print("Invalid option. Please enter 1, 2, or 3.")

# ============================================================================
# BOOKING FUNCTIONS
# ============================================================================

def display_matches():
    """
    Shows the list of available matches to book tickets for.
    Displays each match with a number for easy selection.
    """
    print("\nAvailable Matches:")
    for i in range(len(MATCHES)):
        print(f"{i + 1}. {MATCHES[i]}")

def calculate_total(ticket_types, quantities, match_type):
    """
    Calculates the booking total including subtotal, VAT, and final total.
    
    Parameters:
        ticket_types: List of ticket categories (Child, Teen, Adult, VIP)
        quantities: List of quantities for each ticket type
        match_type: The type of match (Standard or Premium)
    
    Returns:
        A tuple with (subtotal, vat_amount, total_price)
    """
    # Start with zero subtotal
    subtotal = 0
    
    # Add up the cost of each ticket type
    for i in range(len(ticket_types)):
        ticket_type = ticket_types[i]
        quantity = quantities[i]
        price_per_ticket = PRICING[match_type][ticket_type]
        subtotal = subtotal + (price_per_ticket * quantity)
    
    # Calculate VAT (Value Added Tax)
    vat = subtotal * VAT_RATE
    
    # Calculate total price
    total = subtotal + vat
    
    return subtotal, vat, total

def book_tickets():
    """
    Main booking function - guides customer through the ticket booking process.
    Collects match selection, ticket quantities, customer details, and saves the booking.
    """
    print("\n" + "="*50)
    print("TICKET BOOKING")
    print("="*50)
    
    # Step 1: Customer selects which match they want to book
    display_matches()
    match_choice = int(input("Select match number: ")) - 1
    selected_match = MATCHES[match_choice]
    
    # Step 2: Customer selects whether they want Standard or Premium tickets
    match_type = input("\nSelect match type (Standard/Premium): ")
    
    # Step 3: Customer enters the match date
    match_date = input("Enter match date (YYYY-MM-DD): ")
    
    # Step 4: Customer specifies how many tickets of each type they want
    ticket_types = ["Child", "Teen", "Adult", "VIP"]
    quantities = []
    print("\nEnter quantity for each ticket type (or 0 for none):")
    for ticket_type in ticket_types:
        qty = int(input(f"{ticket_type}: "))
        quantities.append(qty)
    
    # Step 5: Collect customer's name and contact information
    name = input("\nEnter your name: ")
    contact = input("Enter your contact number: ")
    
    # Step 6: Calculate all the pricing information
    subtotal, vat, total = calculate_total(ticket_types, quantities, match_type)
    
    # Step 7: Display a summary of the booking so customer can verify
    print("\n" + "="*50)
    print("BOOKING SUMMARY")
    print("="*50)
    print(f"Match: {selected_match}")
    print(f"Date: {match_date}")
    print(f"Type: {match_type}")
    print("\nTickets:")
    for i in range(len(ticket_types)):
        if quantities[i] > 0:
            print(f"  {ticket_types[i]}: {quantities[i]}")
    print(f"\nSubtotal: £{subtotal:.2f}")
    print(f"VAT (20%): £{vat:.2f}")
    print(f"Total: £{total:.2f}")
    
    # Step 8: Create a dictionary with all booking information
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
    
    # Step 9: Save the booking to the CSV file
    save_booking(booking_data)
    print("\nBooking saved successfully!")

def save_booking(booking_data):
    """
    Saves a booking to the bookings CSV file.
    If the file doesn't exist, creates it with headers first.
    
    Parameters:
        booking_data: Dictionary containing all booking information
    """
    try:
        # Open the file in append mode (add to end of file)
        file = open(BOOKINGS_FILE, "a", newline="")
        
        # Create a CSV writer using the booking data keys as column names
        writer = csv.DictWriter(file, fieldnames=booking_data.keys())
        
        # If file is empty (new file), write the header row
        if file.tell() == 0:
            writer.writeheader()
        
        # Write the booking data as a new row
        writer.writerow(booking_data)
        
        # Close the file
        file.close()
    except Exception as e:
        print(f"Error saving booking: {e}")

# ============================================================================
# ADMIN FUNCTIONS
# ============================================================================

def view_bookings():
    """
    Displays all bookings from the CSV file.
    Only admins should be able to call this function.
    Shows each booking with all its details.
    """
    print("\n" + "="*50)
    print("ALL BOOKINGS - ADMIN VIEW")
    print("="*50)
    
    try:
        # Open and read the bookings file
        file = open(BOOKINGS_FILE, "r")
        reader = csv.DictReader(file)
        
        # Convert all rows to a list
        rows = list(reader)
        
        # If no bookings exist, tell the admin
        if not rows:
            print("No bookings found.")
            return
        
        # Display each booking
        for i in range(len(rows)):
            row = rows[i]
            print(f"\nBooking {i + 1}:")
            for key in row:
                print(f"  {key}: {row[key]}")
        
        file.close()
    except FileNotFoundError:
        print("No bookings file found yet.")

# ============================================================================
# MAIN PROGRAM MENU
# ============================================================================

def main():
    """
    Main program - runs the login screen and then shows the appropriate menu
    based on whether the user logged in as a regular user or admin.
    """
    # First, try to log in
    login_result = login()
    
    # If user chose to exit, stop the program
    if login_result is None:
        return
    
    # Extract login type and username
    login_type, username = login_result
    
    # If user is a regular user, show user menu
    if login_type == "user":
        user_menu()
    
    # If user is an admin, show admin menu
    elif login_type == "admin":
        admin_menu()

def user_menu():
    """
    Menu for regular users.
    Users can book tickets or exit the system.
    """
    while True:
        print("\n" + "="*50)
        print("USER MENU - SPORTZONE EVENTS BOOKING SYSTEM")
        print("="*50)
        print("1. Book Tickets")
        print("2. Logout and Exit")
        
        choice = input("\nSelect option (1-2): ")
        
        if choice == "1":
            book_tickets()
        elif choice == "2":
            print("Thank you for using SportZone Events!")
            break
        else:
            print("Invalid option. Please enter 1 or 2.")

def admin_menu():
    """
    Menu for administrators.
    Admins can view all bookings or exit the system.
    """
    while True:
        print("\n" + "="*50)
        print("ADMIN MENU - SPORTZONE EVENTS BOOKING SYSTEM")
        print("="*50)
        print("1. View All Bookings")
        print("2. Logout and Exit")
        
        choice = input("\nSelect option (1-2): ")
        
        if choice == "1":
            view_bookings()
        elif choice == "2":
            print("Thank you for using SportZone Events!")
            break
        else:
            print("Invalid option. Please enter 1 or 2.")

# ============================================================================
# PROGRAM START
# ============================================================================

if __name__ == "__main__":
    main()