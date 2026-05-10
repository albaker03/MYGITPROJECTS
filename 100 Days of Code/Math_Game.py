print("Math Game!")
print()
multiple = int(input("Name your multiples: "))
print()
counter = 0
for i in range(1, 13):
    correct_answer = i*multiple
    print(i, "x", multiple)
    answer = int(input("> "))
    if answer == correct_answer:
        print("Yay! You got the answer correct!")
        counter += 1
    else:
        print("Nope. That was incorrect. The correct answer is", correct_answer)

if counter == 12:
    print("Wow! A perfect score! \U0001f600")
    