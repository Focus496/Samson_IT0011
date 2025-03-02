import json

def validate_student_id(student_id):
    return len(student_id) == 6 and student_id.isdigit()

def validate_student_name(name):
    return isinstance(name, tuple) and len(name) == 2 and all(isinstance(n, str) for n in name)

def validate_grades(standing, exam):
    return isinstance(standing, int) and isinstance(exam, int) and 0 <= standing <= 100 and 0 <= exam <= 100

def calculate_final_grade(standing, exam):
    return (standing * 0.6) + (exam * 0.4)

def load_records(filename="students.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_records(records, filename="students.json"):
    with open(filename, "w") as file:
        json.dump(records, file, indent=4)

def show_all_records(records):
    if records:
        for record in records:
            print(record)
    else:
        print("No records available.")

def order_by_last_name(records):
    sorted_records = sorted(records, key=lambda x: x["name"][1])
    show_all_records(sorted_records)

def order_by_grade(records):
    sorted_records = sorted(records, key=lambda x: calculate_final_grade(x["standing"], x["exam"]), reverse=True)
    show_all_records(sorted_records)

def show_student_record(records, student_id):
    for record in records:
        if record["id"] == student_id:
            print(record)
            return
    print("Student not found")

def add_record(records, student_id, name, standing, exam):
    if validate_student_id(student_id) and validate_student_name(name) and validate_grades(standing, exam):
        records.append({"id": student_id, "name": name, "standing": standing, "exam": exam})
        print("Record added successfully.")
    else:
        print("Invalid input")

def edit_record(records, student_id, name, standing, exam):
    for record in records:
        if record["id"] == student_id:
            if validate_student_name(name) and validate_grades(standing, exam):
                record.update({"name": name, "standing": standing, "exam": exam})
                print("Record updated successfully.")
                return
            print("Invalid input")
            return
    print("Student not found")

def delete_record(records, student_id):
    for i, record in enumerate(records):
        if record["id"] == student_id:
            del records[i]
            print("Record deleted successfully.")
            return
    print("Student not found")

def main():
    records = load_records()
    while True:
        print("\nMenu:")
        print("1. Open File")
        print("2. Save File")
        print("3. Save As File")
        print("4. Show All Students Record")
        print("5. Order by last name")
        print("6. Order by grade")
        print("7. Show Student Record")
        print("8. Add Record")
        print("9. Edit Record")
        print("10. Delete Record")
        print("11. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            records = load_records()
            print("File loaded.")
        elif choice == "2":
            save_records(records)
            print("File saved.")
        elif choice == "3":
            filename = input("Enter new filename: ")
            save_records(records, filename)
            print("File saved as", filename)
        elif choice == "4":
            show_all_records(records)
        elif choice == "5":
            order_by_last_name(records)
        elif choice == "6":
            order_by_grade(records)
        elif choice == "7":
            student_id = input("Enter Student ID: ")
            show_student_record(records, student_id)
        elif choice == "8":
            student_id = input("Enter Student ID: ")
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            try:
                standing = int(input("Enter Class Standing: "))
                exam = int(input("Enter Exam Grade: "))
                add_record(records, student_id, (first_name, last_name), standing, exam)
            except ValueError:
                print("Invalid input: Grades must be numbers.")
        elif choice == "9":
            student_id = input("Enter Student ID: ")
            first_name = input("Enter New First Name: ")
            last_name = input("Enter New Last Name: ")
            try:
                standing = int(input("Enter New Class Standing: "))
                exam = int(input("Enter New Exam Grade: "))
                edit_record(records, student_id, (first_name, last_name), standing, exam)
            except ValueError:
                print("Invalid input: Grades must be numbers.")
        elif choice == "10":
            student_id = input("Enter Student ID to delete: ")
            delete_record(records, student_id)
        elif choice == "11":
            save_records(records)
            print("Exiting program. Data saved.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
