def main(): 
    students = [] 
 
    while True: 
        print("\nEnter student details:")
        lastname = input("Last Name: ") 
        firstname = input("First Name: ") 
        age = input("Age: ") 
        contact = input("Contact Number: ") 
        course = input("Course: ") 
        
        students.append(f"{lastname},{firstname},{age},{contact},{course}") 

        more = input("Do you want to add another student? (yes/no): ").strip().lower()
        if more != "yes":
            break
 
   
    with open("hello.txt", "w") as file: 
        for student in students: 
            file.write(student + "\n") 
 
  
    print("\nReading Student Information:")
    with open("hello.txt", "r") as file: 
        records = file.readlines() 
        for record in records: 
            lastname, firstname, age, contact, course = record.strip().split(',')
            print(f"\nLast Name: {lastname}")
            print(f"First Name: {firstname}")
            print(f"Age: {age}")
            print(f"Contact Number: {contact}")
            print(f"Course: {course}")

if __name__ == "__main__": 
    main()
