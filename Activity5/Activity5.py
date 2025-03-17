def divide(x, y):
    return x / y if y != 0 else "Denominator cannot be zero"

def exponentiation(x, y):
    return x ** y

def remainder(x, y):
    return x % y if y != 0 else "Denominator cannot be zero"

def summation(x, y):
    return sum(range(x, y + 1)) if y > x else "Second number must be greater than the first number"

def main():
    while True:
        print("\nMain Menu:")
        print("1. Mathematical Functions")
        print("2. Exit")
        main_choice = input("Please Enter your choice: ")
        
        if main_choice == "1":
            print("\nMathematical Functions:")
            print("[D] Divide")
            print("[E] Exponentiation")
            print("[R] Remainder")
            print("[F] Summation")
            print("[B] Back")
            choice = input("Enter operation choice: ").upper()
            
            if choice in {"D", "E", "R"}:
                num1, num2 = float(input("Enter the first number: ")), float(input("Enter the second number: "))
            elif choice == "F":
                num1, num2 = int(input("Enter the first number: ")), int(input("Enter the second number: "))
            elif choice == "B":
                continue
            else:
                print("Invalid choice")
                continue
            
            operations = {"D": divide, "E": exponentiation, "R": remainder, "F": summation}
            print("Result:", operations[choice](num1, num2))
        
        elif main_choice == "2":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

main()
