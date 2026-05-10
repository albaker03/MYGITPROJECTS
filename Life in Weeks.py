age = input("What is your current age? ")
your_age = int(age)
max_age = 90

days_left = (max_age - your_age) * 365
weeks_left = (max_age - your_age) *52
months_left = (max_age - your_age) * 12

print(f"You have {days_left} days, {weeks_left} weeks, and {months_left} months left")


