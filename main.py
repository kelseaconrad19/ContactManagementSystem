from re import search
app_is_on = True
contacts = {}


def validate_input(input_type, input_value):
    """Validate input based on the type of information being edited."""
    if input_type == 'phone number':
        return search(r"\d{3}-\d{3}-\d{4}", input_value)
    elif input_type == 'email address':
        return search(r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b", input_value)
    elif input_type == 'home address':
        return search(r"\b\d{1,8}(-)?[a-z]?\W[a-z|\W.]+", input_value)
    elif input_type in ['first name', 'last name', 'notes']:
        return True
    else:
        return False


def add_contact(contact_dict):
    """Takes the contact information from the user and adds it to the contact dictionary."""
    first_name = input("First Name: ").title()
    last_name = input("Last Name: ").title()
    phone_number = input("Phone Number (Use this format: ###-###-####): ")
    email_address = input("Email Address: ").lower()
    home_address = input("Home Address: ").capitalize()
    contact_notes = input("Notes: ")

    if validate_input('phone number', phone_number) and validate_input('email address', email_address) and validate_input('home address', home_address):
        contact_dict[email_address] = {
            "first name": first_name,
            "last name": last_name,
            "phone number": phone_number,
            "home address": home_address,
            "notes": contact_notes
        }
        print("Contact added.")
        return contact_dict
    else:
        print("Invalid input. Please try again.")


def edit_contact(contact_dict):
    """Searches for a contact using their unique identifier (email) and edits one of the values for that contact."""
    try:
        contact_to_edit = input('Enter the email address of the contact you need to edit: ')
        if contact_to_edit not in contact_dict:
            raise KeyError
        detail_to_edit = input("Do you need to edit the contact's First Name, Last Name, Phone Number, Home Address, or Notes?: ").lower()
        fields = ['first name', 'last name', 'phone number', 'home address', 'notes']
        if detail_to_edit not in fields:
            print("Invalid input. Please try again.")
            return
        while True:
            updated_info = input(f"Enter the new {detail_to_edit}: ")
            if validate_input(detail_to_edit, updated_info):
                contact_dict[contact_to_edit][detail_to_edit] = updated_info
                print("Successful.")
                break
            else:
                print(f"Invalid {detail_to_edit}. Please try again or enter 'cancel' to stop editing.")
                if updated_info.lower() == 'cancel':
                    break
    except KeyError:
        print("That email is not in your contact list.")


def delete_contact(contact_dict):
    """Searches for a contact using their unique identifier (email) and deletes it from the contact dictionary."""
    try:
        contact_to_delete = input('Enter the email address of the contact you need to delete: ')
        if contact_to_delete not in contact_dict:
            raise KeyError
        test_email = search(r"\b[\w.-]+@[\w.-]+\.\w{2,4}\b", contact_to_delete)
        if not test_email:
            print("Invalid input. Please try again.")
        else:
            contact_dict.pop(contact_to_delete)
            print(contact_dict)
    except KeyError:
        print("That email is not in your contact list.")


def search_contacts(contact_dict):
    """Searches for a contact using their unique identifier (email address) and displays their details."""
    try:
        contact_to_search = input('Enter the email address of the contact you need to search for: ')
        if contact_to_search not in contact_dict:
            raise KeyError
        test_email = search(r"\b[\w\.-]+@[\w.-]+\.\w{2,4}\b", contact_to_search)
        if not test_email:
            print("Invalid input. Please try again.")
        else:
            result = contact_dict.get(contact_to_search)
            print(result)
    except KeyError:
        print("That email is not in your contact list.")


def display_contact(contact_dict):
    """Displays a list of all contacts with their unique identifiers."""
    if len(contact_dict) == 0:
        raise Exception("No contacts to list.")
    for contact in contact_dict:
        print(f"{contact}: {contact_dict[contact]}")


def export_contacts(contact_dict, file_name):
    """Exports all contacts in the contact_dict to a text file to be stored."""
    with open(file_name, 'a') as file:
        for contact_email, details in contact_dict.items():
            file.write(f"{contact_email}: {details}\n")
    print(f"Saved to {file_name}.")


def import_contacts(contact_dict, file_name):
    """Imports all the contacts in a given text file and parses the data into a nested dictionary."""
    try:
        with open(file_name, 'r') as file:
            for line in file:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    contact_dict[key] = eval(value)
        print(contact_dict)
    except FileNotFoundError:
        print("That file does not exist. Please try again.")
    except ValueError as e:
        print(f"Error processing line {line}: {e}")


def main(user_choice, contact_dict, file_name):
    """If the user_choice is not 8 or Quit, checks the number and performs the appropriate function."""
    if user_choice == "1" or user_choice == "add a contact":
        add_contact(contact_dict)
    elif user_choice == "2" or user_choice == "edit a contact":
        edit_contact(contact_dict)
    elif user_choice == "3" or user_choice == "delete a contact":
        delete_contact(contact_dict)
    elif user_choice == "4" or user_choice == "search for a contact":
        search_contacts(contact_dict)
    elif user_choice == "5" or user_choice == "display all contacts":
        display_contact(contact_dict)
    elif user_choice == "6" or user_choice == "export contacts":
        export_contacts(contact_dict, file_name)
    elif user_choice == "7" or user_choice == "import contacts":
        import_contacts(contact_dict, file_name)
    else:
        print("Invalid input. Please try again.")


# User Interface - Welcome Message and Menu
print("Welcome to the Contact Management System!")
while app_is_on:
    menu = "Menu:\n1. Add a new contact\n2. Edit an Existing Contact\n3. Delete a Contact\n4. Search for a Contact\n5. Display All Contacts\n6. Export Contacts to a Text File\n7. Import Contacts from a Text File\n8. Quit"
    print(menu)
    user_input = input("Choose a number from the menu: ").lower()

    # Check if user wants to quit first. If input = 8 or "quit", application should end.
    if user_input == "8" or user_input == "quit":
        break
    else:
        main(user_input, contacts, 'contacts.txt')
        # Ask user if they want to do something else with the application. If yes, go back to the top of the loop and display the menu again. If not, end the application.
        another_task = input("\nDo you need anything else? Y or N: ").lower()
        if another_task == "y":
            app_is_on = True
        elif another_task == "n":
            app_is_on = False
        else:
            print("Invalid Input. Please try again.")

