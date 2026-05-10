#If the bill was $150.00, split between 5 people, with 12% tip. 

#Each person should pay (150.00 / 5) * 1.12 = 33.6
#Format the result to 2 decimal places = 33.60

#Tip: There are 2 ways to round a number. You might have to do some Googling to solve this.💪

#Write your code below this line 👇
print('Welcome to the tip calculator')
bill = float(input("What was the total bill? "))
tip = int(input("What percentage tip would you like to give?  "))
people = int(input("How many people to split the bill? "))

tip_cal = (tip / 100)
tip_dollar = (bill * tip_cal)
final_bill = (bill + tip_dollar)
bill_split = (final_bill / people)
final_pay = round(bill_split, 2)
final_pay = "{:.2f}".format(bill_split)

print(f"Each person should pay ${final_pay}")