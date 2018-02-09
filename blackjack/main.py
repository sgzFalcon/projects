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
        self.state = 'playing'

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

    def changeState(self,state):
        self.state = state
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
    player = Player(name.capitalize(), balance=10)
    return player

def checkPoints(points, counter, player):
    if points > 21:
        print(player.name,'has lost', sep=' ')
        player.changeState('exceed')
        return -1
    elif points == 21 and counter == 2:
        print(player.name,'has a Blackjack', sep=' ')
        player.changeState('blackjack')
        return -1
    elif points == 21:
        print('You have', points,'points', sep=' ')
        return -1
    else:
        print('You have', points,'points', sep=' ')

def main():
    players=[] #Store objects
    answer = 1
    Dealer = Player('dealer', balance=100) #Create dealer
    while answer in positiveAnswers:
        players += [createPlayer()]
        print('There is/are', len(players),'player(s).','\n', sep=' ')
        if len(players) == 6:
            print('The table is complete, no more players admited')
            break
        answer = input('Do you want to add another player? ')
    cards = createCards()

    #Dealer starts taking a card face up
    result = pickCard(cards)
    cards = result['cards']
    print('Dealer\'s card is:',result['card'],sep=' ')
    points = Dealer.addCard(result['card'])

    for player in players:
        #Turn of player: 0.Two Cards 1.Bet 2.Pick 3.Points
        counter = 2
        print('\n---',player.name,'is playing now', '---\n',sep=' ')
        result = pickCard(cards)
        cards = result['cards']
        points = player.addCard(result['card'])
        card1 = result['card']
        result = pickCard(cards)
        cards = result['cards']
        points = player.addCard(result['card'])
        print('Your cards are:',card1, 'and',result['card'],sep=' ')
        if checkPoints(points, counter, player) == -1:
            break
        moreCards = input('Do you want another card? ')
        while moreCards in positiveAnswers:
            print(cards)
            counter += 1
            result = pickCard(cards)
            cards = result['cards']
            print('Your card is:',result['card'],sep=' ')
            points = player.addCard(result['card'])
            if checkPoints(points, counter, player) == -1:
                break
            moreCards = input('Do you want another card? ')
    #Ckeck who won

main()
