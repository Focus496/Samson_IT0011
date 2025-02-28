
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
age = input("Enter your Age: ")


full_name = first_name + " " + last_name


sliced_name = first_name[:4]


greeting_message = "Hello, {}! Welcome. You are {} years old.".format(sliced_name, age)


print("Full Name:", full_name)
print("Sliced Name:", sliced_name)
print("Greeting Message:", greeting_message)