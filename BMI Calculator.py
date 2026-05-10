height = input("Enter you height in meters: ")
weight = input("Enter you weight in kg: ")

bmi = float(weight) / float(height) ** 2
bmi_as_int = round(bmi, 2)
print(bmi_as_int)