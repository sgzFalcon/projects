'''
Blackjack game:
* Can select number of players
* Can add computer controlled players
* Can track bets of players
'''
import random

positiveAnswers = [1, 'yes', 'Yes', 'y', 'si', 'sí']

positiveDecisions = ['Hit','hit','h','double','Double','d']

class Player():
    """docstring for player."""
    def __init__(self, name, balance, bet):
        self.name = name
        self.deck = []
        self.balance = int(balance)
        self.state = 'playing'
        self.bet = int(bet)

    def addCard(self,card):
        self.deck += [card]
        return self.totalPoints()

    def totalPoints(self):
        points = 0
        ace = 0
        for i in sorted(self.deck, reverse = True):
            if i > 10:
                points += 10
            elif i == 1 and points + 11 <= 21:
                points += 11
                ace += 1
            else:
                points += i
                if points > 21 and ace >= 1: #Double Ace fix
                    points -= 10
        return  points

    def changeState(self,state):
        self.state = state

    def doubleBet(self):
        self.bet += self.bet

    def payBet(self,amount):
        if self.totalPoints() == 21:
            self.balance += amount * 2
        else:
            self.balance += amount

    def withdrawBet(self,amount):
        self.balance -= amount

    def clearDeck(self):
        self.deck = []

def createCards():
    cards = list(range(1,14)) * 4
    return cards

def pickCard(cards):
    index = random.randint(0,len(cards)-1)
    card = cards[index]
    cards.pop(index)
    return {'cards':cards, 'card':card}

def createPlayer(initialBet):
    name = input('Introduce your name: ')
    balance = input('How much do you have to play? ')
    player = Player(name.capitalize(), balance,initialBet)
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
        print(player.name, 'has', points,'points', sep=' ')
        return -1
    else:
        print(player.name, 'has', points,'points', sep=' ')

def cardsName(card):
    names = {1:'Ace',2:'Two',3:'Three',4:'Four',5:'Five', 6:'Six',7:'Seven',
        8:'Eight', 9:'Nine', 10:'Ten', 11:'Jack',12:'Queen',13:'King'}
    return names[card]

def createGame():
    players=[] #Store objects
    answer = 1
    initialBet = input('What is the initial bet? ')
    Dealer = Player('Dealer', 1000,initialBet) #Create dealer
    while answer in positiveAnswers:
        players += [createPlayer(initialBet)]
        print('There is/are', len(players),'player(s).','\n', sep=' ')
        if len(players) == 6:
            print('The table is complete, no more players admited')
            break
        answer = input('Do you want to add another player? ')
    return players,Dealer

def game(players, Dealer):
    cards = createCards() #New deck pf cards

    #Dealer starts taking a card face up
    result = pickCard(cards)
    cards = result['cards']
    print('\n','Dealer\'s card is:',cardsName(result['card']),sep=' ')
    points = Dealer.addCard(result['card'])

    for player in players:
        #Turn of player:
        counter = 2
        print('\n---',player.name,'is playing now', '---\n',sep=' ')
        result = pickCard(cards)
        cards = result['cards']
        points = player.addCard(result['card'])
        card1 = result['card']
        result = pickCard(cards)
        cards = result['cards']
        points = player.addCard(result['card'])
        print('Your cards are:',cardsName(card1), 'and',
            cardsName(result['card']),sep=' ')
        if checkPoints(points, counter, player) == -1:
            continue
        decision = input('You can: Hit, Stand or Double: ')
        while decision in positiveDecisions:
            counter += 1
            result = pickCard(cards)
            cards = result['cards']
            print('Your card is:',cardsName(result['card']),sep=' ')
            points = player.addCard(result['card'])
            #Add if for double situation (bet and break)
            if checkPoints(points, counter, player) == -1:
                if decision in ['d','double','Double']:
                    player.doubleBet()
                break
            if decision in ['d','double','Double']:
                break
            decision = input('You can: Hit, Stand or Double: ')
    #Dealer finishes his hand
    print('\n--- Dealer is playing now', '---\n',sep=' ')
    situation = []
    for player in players:
        situation += [player.state]
    if 'playing' not in situation and 'blackjack' not in situation:
        print('Dealer has won everybody busted')
        #Add withdraws to every player
        for player in players:
            player.withdrawBet(player.bet)
            Dealer.payBet(player.bet)
            print(player.name,'lost',player.bet,sep=' ')
    else:
        result = pickCard(cards)
        cards = result['cards']
        print('Dealer\'s second card is:',cardsName(result['card']),sep=' ')
        dealerspoints = Dealer.addCard(result['card'])
        disposable = checkPoints(dealerspoints,2,Dealer)

        if Dealer.state == 'blackjack':
            print('Dealer has won with a Blackjack')
            #Add withdraws to every player
            for player in players:
                player.withdrawBet(player.bet)
                Dealer.payBet(player.bet)
                print(player.name,'lost',player.bet,sep=' ')

        elif 'playing' in situation:
            while dealerspoints < 17:
                result = pickCard(cards)
                cards = result['cards']
                print('Dealer\'s card is:',cardsName(result['card']),sep=' ')
                dealerspoints = Dealer.addCard(result['card'])
                if checkPoints(dealerspoints, counter, Dealer) == -1:
                    break

            if dealerspoints <= 21:
                for player in players:
                    if dealerspoints > player.totalPoints():
                        print('Dealer has won', player.name, sep=' ')
                        #Add withdraws
                        player.withdrawBet(player.bet)
                        Dealer.payBet(player.bet)
                        print(player.name,'lost',player.bet,sep=' ')
                    elif player.state == 'exceed':
                        print('Dealer has won',player.name, sep=' ')
                        #Add withdraws
                        player.withdrawBet(player.bet)
                        Dealer.payBet(player.bet)
                        print(player.name,'lost',player.bet,sep=' ')
                    elif dealerspoints < player.totalPoints():
                        print(player.name,'has won', Dealer.name, sep=' ')
                        #Add withdraws
                        player.payBet(player.bet)
                        if player.totalPoints() == 21:
                            Dealer.withdrawBet(2 * player.bet)
                            print(player.name,'won',2 * player.bet,sep=' ')
                        else:
                            Dealer.withdrawBet(player.bet)
                            print(player.name,'won',player.bet,sep=' ')
                    else:
                        print(player.name,'\'s bet is returned')

            else:
                print('Dealer busted')
                for player in players:
                    if player.state != 'exceed':
                        player.payBet(player.bet)
                        if player.totalPoints() == 21:
                            Dealer.withdrawBet(2 * player.bet)
                            print(player.name,'won',2 * player.bet,sep=' ')
                        else:
                            Dealer.withdrawBet(player.bet)
                            print(player.name,'won',player.bet,sep=' ')
                    else:
                        player.withdrawBet(player.bet)
                        Dealer.payBet(player.bet)
                        print(player.name,'lost',player.bet,sep=' ')
        else:
            print('Blackjack wins')
            #Add withdraws Blackjack
            for player in players:
                if player.state == 'exceed':
                    player.withdrawBet(player.bet)
                    Dealer.payBet(player.bet)
                    print(player.name,'lost',player.bet,sep=' ')
                else:
                    player.payBet(player.bet)
                    Dealer.withdrawBet(2 * player.bet)
                    print(player.name,'won',2 * player.bet,sep=' ')

    print('\n---','Balance of the game','---\n',sep=' ')
    for player in players + [Dealer]:
        print(player.name, 'has', player.balance,sep=' ')
        player.clearDeck()

def main():
    players, Dealer = createGame()
    answer = 'again'
    while answer in ['again', 'Again','a']:
        game(players, Dealer)
        answer = input('Do you want to play again, reset or close? ')
    if answer in ['reset','r','Reset']:
        main()
main()
