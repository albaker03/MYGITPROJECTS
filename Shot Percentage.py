#Calculate field goal percentage

made = int(input("Enter number of made shots "))
missed = int(input("Enter number of total shot attempts "))

field_number = (made / missed) * 100
field_goal = round(field_number)
print(f"Field goal percentage is {field_goal}%")

