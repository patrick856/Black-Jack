import random
import time


moves = ["Stand","Hit","Double down","Surrender","Spilt"]
money = 10000
deck1 = set()
deck2 = set()
card_count = 0
    
while True:
    split_1 = True
    split_2 = True
    player_cards = []
    player_cards_split = []
    dealer_cards = []
    split = False
    bet = 0
    bet2 = 0
    
    class Card():
        card_ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        card_suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']

        def __init__(self, hidden):
            x = random.randint(0,12)
            self.rank = Card.card_ranks[x]
            self.suit = Card.card_suits[random.randint(0,3)]
            self.value = min(x+1,10)
            self.hidden = hidden

        def __str__(self):
            if self.hidden:
                return "* ******"
            return f"{self.rank} {self.suit}"

    def new_card(hidden):
        global card_count
        card = Card(hidden)
        if card in deck1:
            if card in deck2:
                return new_card(hidden)
            card_count += 1
            deck2.add(card)
            return card
        card_count += 1
        deck1.add(card)
        return card

    def shuffle_decks():
        global card_count
        print("----- shuffling decks -----")
        deck1 = set()
        deck2 = set()
        card_count = 0
    
    def update_screen():
        print("dealer\n")
        for i in dealer_cards:
            print("        " + str(i))
        if split:
            print("\nplayer: " + str(split_no) + "\n")
            len1 = len(player_cards)
            len2 = len(player_cards_split)
            for i in range(0,max(len1,len2)):
                if i < len1:
                    if i < len2:
                        print("        " , player_cards[i] , end="        ")
                    else:
                        print("        " , player_cards[i])
                else:
                    print(end = "                        " )
                if(i<len2):
                    print(player_cards_split[i])

        else:    
            print("\nplayer\n")
            for i in player_cards:
                print("        " + str(i))

    def player_turn():
        global split
        global bet
        global bet2
        global split_no
        global split_1
        global split_2
        update_screen()

        if total_value(player_cards) == 21 and len(player_cards) == 2:
            if split:
                print("------- BJ -------")
                split_no = 2
                time.sleep(2)
                bet *= 2
            else:
                print("------- BJ -------")
                bet *= 2
                time.sleep(2)
                dealer_turn()
                return
        if split and split_no == 2 and total_value(player_cards_split) == 21:
            print("------- BJ -------")
            bet2 *= 2
            time.sleep(2)
            dealer_turn()
            return
        if split:
            if split_no == 1:
                if total_value(player_cards) > 21:
                    split_no = 2
                    print("------- Lost -------")
                    split_1 = False
                    time.sleep(2)
                    player_turn()
                    return
            else:
                if total_value(player_cards_split) > 21:
                    print("------- Lost -------")
                    time.sleep(2)
                    split_2 = False
                    if split_1:
                        dealer_turn()
                        return
                    else:
                        win_or_lose()
                        return
                
        elif total_value(player_cards) > 21:
            player_lost(bet)
            return
        can_split = split_option()
        if can_split and split == False:
            x = 5
        else:
            x = 4

        print("")
        for i in range(0,x):
            print(str(i+1) + ") " + moves[i])
        choice = 1
        try:
            choice = int(input())
            if choice < 1 or choice > x:
                print("Input an integer between (1 - " + str(x) + ")\n")
                player_turn()
        except ValueError:
            print("Input an integer between (1 - " + str(x) + ")\n")
            player_turn()
        if choice == 1:
            if split and split_no == 1:
                split_no = 2
                player_turn()
                return
            else:
                dealer_turn()
                return
        if choice == 2:
            if split and split_no == 2:
                player_cards_split.append(new_card(False))
                player_turn()
                return
            else:
                player_cards.append(new_card(False))
                player_turn()
                return
        if choice == 3:
            if split:
                if split_no == 1:
                    bet *= 2
                    player_cards.append(new_card(False))
                    split_no == 2
                else:
                    bet2 *= 2
                    player_cards_split.append(new_card(False))
                    dealer_turn()
                    return
            else:
                bet *= 2
                player_cards.append(new_card(False))
                dealer_turn()
                return
        if choice == 4:
            player_lost(bet + bet2)
            return
        if choice == 5:
            split = True
            split_no = 1
            bet2 = bet
            player_cards_split.append(player_cards[1])
            player_cards.pop(1)
            player_turn()
            return

    def dealer_turn():
        global bet
        global bet2
        update_screen()
        time.sleep(2)
        if dealer_cards[1].hidden:
            dealer_cards[1].hidden = 0
            dealer_turn()
            return
        if total_value(dealer_cards) == 21:
            if split:
                if total_value(player_cards) == 21:
                    bet = 0
                if total_value(player_cards_split) == 21:
                    bet2 = 0
        if total_value(dealer_cards) > 21:
            if total_value(player_cards) <= 21:
                player_won(bet)
            else:
                player_lost(bet)
            if total_value(player_cards_split) <= 21 and split:
                player_won(bet2)
            elif split:
                player_lost(bet2)
            return
        if total_value(dealer_cards) < 17:
            if split:
                if total_value(dealer_cards) > total_value(player_cards) and total_value(dealer_cards) > total_value(player_cards_split):
                    player_lost(bet + bet2)
                    return
            elif total_value(dealer_cards) > total_value(player_cards):
                player_lost(bet)
                return
            dealer_cards.append(new_card(False))
            print("------- Hit -------")
            dealer_turn()
            return
        else:
            print("------- Stand -------")
        win_or_lose()        

    def split_option():
        if len(player_cards) == 2 and player_cards[0].value == player_cards[1].value and money >= 2*bet:
            return True
        return False

    def place_bet():
        global bet
        print("Money: " + str(money) + " $$")
        try:
            bet = int(input("Place your bet\n"))
            if bet <= 0:
                print("Dont you want to play?")
                place_bet()
            if bet > money:
                print("You dont have that much")
                place_bet()
        except ValueError:
            print("Please insert an integer")
            place_bet()

    def win_or_lose():
        global bet
        global bet2
        if total_value(dealer_cards) > total_value(player_cards) or split_1 == False:
            player_lost(bet)
        elif total_value(dealer_cards) < total_value(player_cards):
            player_won(bet)
        else:
            player_won(0)
        if split:
            if total_value(dealer_cards) > total_value(player_cards_split) or split_2 == False:
                player_lost(bet2)
            elif total_value(dealer_cards) < total_value(player_cards_split):
                player_won(bet2)
            else:
                player_won(0)

    def player_lost(amount):
        global money
        print("You lost " + str(amount) + " Dollars")
        money -= amount

    def player_won(amount):
        global money
        print("You Won " + str(amount) + " Dollars")
        money += amount

    def total_value(cards):
        x = 0
        ace = 0
        for i in cards:
            if i.value == 1:
                ace+=1
                x+=11
            else:
                x += i.value
        if x > 21:
            while ace > 0:
                x-=10
                ace-=1
                if x < 22:
                    return x
        return x

    if card_count > 94:
        shuffle_decks()
    player_cards.append(new_card(False))
    player_cards.append(new_card(False))
    dealer_cards.append(new_card(False))
    dealer_cards.append(new_card(True))
    place_bet()
    player_turn()
    if money == 0:
        print("You cant play no more")
        break
            
