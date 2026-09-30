import random
import time

print("===================================")
print("      ROCK PAPER SCISSORS GAME")
print("===================================")
print("Welcome to the game!")
print("Choose: rock, paper, or scissors")
print()

player1 = input("Player 1: Enter rock, paper or scissors: ").lower()
player2 = input("Player 2: Enter rock, paper or scissors: ").lower()

print()
print("Checking the results...")
time.sleep(1)
print()

choices = ["rock", "paper", "scissors"]

if player1 not in choices:
    print("PLAYER 1 entered an invalid choice!")

elif player2 not in choices:
    print("PLAYER 2 entered an invalid choice!")

elif player1 == player2:
    print("DRAW!")

elif player1 == "rock" and player2 == "scissors":
    print("PLAYER 1 WINS!")

elif player1 == "paper" and player2 == "rock":
    print("PLAYER 1 WINS!")

elif player1 == "scissors" and player2 == "paper":
    print("PLAYER 1 WINS!")

else:
    print("PLAYER 2 WINS!")

print()
print("===================================")
print("           GAME OVER")
print("===================================")
