#Write code to determin the grade for a student

examName = input("What is the name of the Exam? ")
maxScore = int(input("What is the max possible score? "))
myScore = int(input("What is you score? "))
gradePert = (myScore / maxScore) * 100

if gradePert >= 90 :
    print("You scored an A+ \U0001f600!")
elif gradePert >= 80 and gradePert < 90 :
    print("You scored an A- \U0001f600!")
elif gradePert >= 70 and gradePert < 80 :
    print("You scored a B \U0001f610!")
elif gradePert >= 60 and gradePert < 70 :
    print("You scored a C \U0001f615")
elif gradePert >= 50 and gradePert < 60 :
    print("You scored a D \U0001f620")
elif gradePert >= 40 and gradePert < 50 :
    print("You scored an U \U0001f630")
else:
    print("You faild the test \U0001f635.")