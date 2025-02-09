import random
import time
from art import text2art


class Hand:
    def __init__(self):
        self.d_hand = []
        self.p_hand = []
        self.d_total = 0
        self.p_total = 0
        self.p_aces = 0


def welcome():
    title = text2art("BLACKJACK")
    print(title)
    print("Welcome to the BlackJack Game")
    print("If you decide to play, you will start with a balance of $10,000\n")
    print("Enter the number corresponding to the choice you want to make")
    print("Do you want to play?")
    print("1 – Yes")
    print("2 – No")
    choice = input("Enter: ")

    return choice


def draw_card(hand, player): #player: 0 = Dealer, 1 = Player
    cards = [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10), ('A', 11)]

    new_card = random.choice(cards)
    if player == 0:
        hand.d_hand.append(new_card)
        hand.d_total += new_card[1]
    else:
        hand.p_hand.append(new_card)
        hand.p_total += new_card[1]
        if new_card[0] == 'A':
            hand.p_aces += 1
        
        if hand.p_total > 21 and hand.p_aces > 0:
            hand.p_total -= 10
            hand.p_aces -= 1


def place_bet(balance):
    bet = 99
    print("\n\n--- Place Bet -------------------------------------------------------------------------------")
    print()
    print(f"Current Balance:\t{balance}")
    print()
    print(f"You can bet in $100 increments between $100-{balance}")
    print("Note: If you lose the hand you will lose the bet, if you win the hand you will recieve the value of the bet from the dealer")
    print("\n(If bet is within valid range but not in correct increments, it will be rounded down)")

    while bet < 100 or bet > balance:
        bet = int(input("Type in bet and press enter: $"))

        if bet > balance:
            print(f"You don't have that much money too bet. Bet an amount less than or equal too your balance: {balance}")
        elif bet < 100:
            print(f"Bet must be at least $100.")

    bet = bet // 100
    bet = bet * 100

    return bet



def dealing(bet):

    # Initial hands
    hand = Hand()

    print("\n\n--- Rules ----------------------------------------------------------------")
    print("1. You and the dealer will both be dealt 2 cards but you will only be able to see one of the dealers cards")
    print("2. You will then decide whether to \"Hit\" (draw an additional card), or \"Stand\" (stick with the cards you have)")
    print("\t - The goal is to get the highes sum possible, without going over 21. If you go over 21 you bust and lose the hand.")
    print("\t\t(Card values are shown below)")
    print("3. The dealer will now draw their cards until they reach at least 17.")
    print("\t - If the dealer goes over 21, they bust and you win.")
    print("4. If neither of you went over 21, whoever has the greater sum will win the hand and the bet value. If you tie you will get your bet back.")
    print("\n--- Card Values -------------------------")
    print("(Card: Value)")
    print("Numbered cards: The value of their number")
    print("Face Cards: 10")
    print("Ace: 11 or 1 (It will have the value 11 until you go over 21, and then it's value will drop to 1)")

    print("\n\n--- DEALING --------------------------------------------------------------")
    print(f"Bet: ${bet}")

    for i in range(4):
        print(f"\n--- CARD {i + 1} ------------------------------")
        if i % 2 == 0: # Remainder
            draw_card(hand, 0)
        else:
            draw_card(hand, 1)
        
        dealing_print_hands(hand)
        
        # Wait 2 second before the next card
        time.sleep(2)

    if hand.p_total == 21:
        print("\nBLACKJACK!!!!!")
        print(f"Congratulations, you will be paid 1.5x your bet!")
        return 3

    print(f"\nYour total: \t\t{hand.p_total} \nDealer's Total: \t\t?")

    hand = decision(hand)

    if hand.p_total < 22:
        print("Dealer's Cards:\t\t", ", ".join(card[0] for card in hand.d_hand))
        print(f"Dealer's Total:\t\t{hand.d_total}")

        time.sleep(2)

        if hand.d_total < 17:
            hand = finish_dealer(hand)

    result = None # 0 - Loss, 1 - Tie, 2 - Win
    if hand.p_total > 21 or (hand.d_total < 22 and hand.d_total > hand.p_total):
        print(f"YOU LOST ${bet} :(")
        result = 0
    elif hand.d_total == hand.p_total:
        print(f"You tied the dealer and get you bet of ${bet} back.")
        result = 1
    else:
        print(f"YOU WON ${bet}!!! :)")
        result = 2
    return result





def dealing_print_hands(hand):
    if len(hand.p_hand) > 0:
        print("Your Cards:\t\t", ", ".join(card[0] for card in hand.p_hand))
    else:
        print("Your Cards:")
    
    if len(hand.d_hand) < 2:
        print("Dealer's Cards:\t\t ?")
    if len(hand.d_hand) == 2:
        print(f"Dealer's Cards:\t\t ?, {hand.d_hand[1][0]}")





def decision(hand):
    
    print("\n\n--- Decision Time ---------------------------------------------------------------------\n")
    
    # Display hands
    print("Your Cards:\t\t", ", ".join(card[0] for card in hand.p_hand))
    print(f"Dealer's Cards:\t\t ?, {hand.d_hand[1][0]}")
    
    # Display totals
    print(f"\nYour Total: \t\t{hand.p_total}\n")

    stop = 0
    
    while stop == 0:
        
        print("The numbers on the left correspond to the choices you can make:")
        print("1 – Hit (Draw another card)")
        print("2 – Stand (Stay with the cards you have)")

        choice = -1
        while choice != 1 and choice != 2:
            choice = int(input("Enter Choice: "))
            if choice != 1 and choice != 2:
                print("Choice must be 1 or 2, please try again.")
        
        if choice == 1:
            draw_card(hand, 1)            

            print(f"\n--- NEW CARD ---------------------------")
            print("Your Cards:\t\t", ", ".join(card[0] for card in hand.p_hand))
            print(f"\nYour Total: \t\t{hand.p_total}\n")

            if hand.p_total > 21:
                print("Waaamp Waaaaamp Waaaaaaaaamp :( \nYOU BUST!")
                stop = 1
        else:
            print("\nGreat! Now lets see what the dealer has!")
            stop = 1
            time.sleep(2)

    return hand


def finish_dealer(hand):
    while hand.d_total < 17:
        draw_card(hand, 0)
        print(f"\n--- NEW CARD ---------------------------")
        time.sleep(2)
        print("Dealer's Cards:\t\t", ", ".join(card[0] for card in hand.d_hand))
        print(f"\nDealer's Total:\t\t{hand.d_total}\n")
        

    if hand.d_total > 21:
        print("DEALER BUSTED!!! :)")

    return hand



def cashout(balance):
    print(f"\nWould you like to cashout with ${balance} or keep playing for a chance to win more?")
    print("1 - Play another hand")
    print("0 - Cashout")
    choice = int(input("Enter: "))

    if choice == 0:
        print(f"\nAre you sure you want to cashout with ${balance} and forgo a chance to win more?")
        print("1 - Play another hand")
        print("0 - Cashout")
        choice = int(input("Enter: "))
        
        if choice == 0:
            print("\nI'm going to give you one last chance.")
            print(f"Are you sure you want to cashout with just ${balance}, when an opportunity to achieve financial freedom could be just a few hands away?")
            print("1 - Play another hand")
            print("0 - Cashout")
            choice = int(input("Enter: "))
    
    if choice == 1:
        print("GREAT CHOICE!!!")
        print("Lets play another hand")
        time.sleep(1)

    return choice



def main():
    if welcome() == 2:
        print(f"Ok, program will exit now\n")
        return

    balance = 10000
    play = 1
    
    while play == 1 and balance > 0:
        bet = place_bet(balance)
        result = dealing(bet)

        if result == 2:
            balance += bet
        elif result == 3:
            if ((bet * 1.5) % 100) != 0:
                balance += (((bet * 1.5) // 100) * 100) + 100
            else:
                balance += bet * 1.5
        elif result == 0:
            balance -= bet

        print(f"Your balance is now: ${balance}")

        if balance > 0:
            play = cashout(balance)

    if balance <= 0:
        print("\nUHHHHHH OOOHHHHHHHHHHHHH!!!!!!!!!!!!!")
        print("You lost it all :(")
        print("Time to move back in with the parents.")

    return 0



if __name__ == "__main__":
    main()