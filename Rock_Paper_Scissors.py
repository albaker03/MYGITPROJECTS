rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇
import random
player = int(input("What do you choose? Type 0 for Rock, 1 for Paper, and 2 for Scissors "))
choose_pick = 0, 1, 2
computer_pick = random.choice(choose_pick)

if player < 0 or player > 2:
    print("Invalaid request")
    elif player == 0:
        print(rock)
    elif player == 1:
        print(paper)
    elif player == 2:
        print(scissors)
    print("Computer chose: ")

    if computer_pick == 0:
        print(rock)
    elif computer_pick == 1:
        print(paper)
    elif computer_pick == 2:
        print(scissors)
    else:
        print("You entered an invalid request.")

    if computer_pick == 0 and player == 2:
        print("You loose.")
    elif computer_pick == 1 and player == 2:
        print("You Win!")
    elif computer_pick == 2 and player == 0:
        print("You Win!")
    elif computer_pick == 0 and player == 1:
        print("You win!")
    elif computer_pick == 2 and player == 1:
        print("You loose.")
    elif computer_pick == 1 and player == 0:
        print("You loose")
    else:
        print("It's a tie!")
else:
  print("You entered an invlaid request.")