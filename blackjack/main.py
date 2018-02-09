'''
Blackjack game:
* Can select number of players
* Can add computer controlled players
* Can track bets of players
'''
import random

positiveAnswers = [1, 'yes', 'Yes', 'y', 'si', 'sí']

class Player():
    """docstring for player."""
    def __init__(self, name, balance):
        self.name = name
        self.deck = []
        self.balance = balance

    def addCard(self,card):
        self.deck += [card]
        return self.totalPoints()

    def totalPoints(self):
        points = 0
        for i in self.deck:
            if i > 10:
                points += 10
            elif i == 1 and points + 11 <= 21:
                points += 11
            else:
                points += i
        return  points
    #Methods for adding and withdrawing balance

def createCards():
    cards = list(range(1,14)) * 4
    return cards

def pickCard(cards):
    index = random.randint(0,len(cards)-1)
    card = cards[index]
    cards.pop(index)
    return {'cards':cards, 'card':card}

def createPlayer():
    name = input('Introduce your name: ')
    player = Player(name, balance=10)
    return player
def main():
    players=[]
    answer = 1
    while answer in positiveAnswers:
        players += [createPlayer()]
        print('There is/are', len(players),'player(s).','\n', sep=' ')
        if len(players) == 6:
            print('The table is complete, no more players admited')
            break
        answer = input('Do you want to add another player? ')
    cards = createCards()
    for player in players:
        #Turn of player: 1.Bet 2.Pick 3.Points
        moreCards, counter = 1, 0
        print('\n---',player.name,'is playing now', '---\n',sep=' ')
        while moreCards in positiveAnswers:
            counter += 1
            result = pickCard(cards)
            cards = result['cards']
            card = result['card']
            print('Your card is:',card,sep=' ')
            points = player.addCard(card)
            if points > 21:
                print(player.name,'has lost', sep=' ')
                break
            elif points == 21 and counter == 2:
                print(player.name,'has a Blackjack', sep=' ')
                break
            elif points == 21:
                print('You have', points,'points', sep=' ')
                break
            else:
                print('You have', points,'points', sep=' ')
            moreCards = input('Do you want another card? ')
    #Ckeck who won


main()
