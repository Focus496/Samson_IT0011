def is_palindrome(num):
    return str(num) == str(num)[::-1]

import os

file_path = r'C:\Users\LENOVO\Documents\numbers.txt'  

if not os.path.exists(file_path):
    print("Error: File not found.")
else:
    with open(file_path, 'r') as file:
        file_lines = file.readlines()
        
    for index, line_content in enumerate(file_lines, start=1):
        try:
            num_list = list(map(int, line_content.strip().split(',')))
            sum_numbers = sum(num_list)
            check_result = "Palindrome" if is_palindrome(sum_numbers) else "Not a palindrome"
            print(f"Line {index}: {', '.join(map(str, num_list))} (sum {sum_numbers}) - {check_result}")
        except ValueError:
            print(f"Error: Invalid data on line {index}.")
