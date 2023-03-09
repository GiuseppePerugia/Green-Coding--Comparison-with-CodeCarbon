from card_elements import Card, Deck, Pile
from codecarbon import EmissionsTracker
import itertools
import pprint

pp = pprint.PrettyPrinter(indent=4)


with EmissionsTracker() as tracker:
    class Game:
        
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        colors = ["red", "black"]
        signs = ["diamond", "spades", "hearts", "clubs"]
        deck = [f"Card: {value} Color: {color} Symbol: {sign}" for value, color, sign in itertools.product(values, colors, signs)]

        print("The cards in your deck are:")
        print('\n'.join(deck))

        suits = {
            u'\u2660': "black",
            u'\u2665': "red",
            u'\u2663': "black",
            u'\u2666': "red",
        }
        
        numPlayPiles = 7
        
        def __init__(self):
            self.deck = Deck(self.values,self.suits)
            self.playPiles = []
            for i in range(self.numPlayPiles):
                thisPile = Pile()
                [thisPile.addCard(self.deck.takeFirstCard(flip=False)) for j in range(i+1)]
                thisPile.flipFirstCard()  
                self.playPiles.append(thisPile)
            self.blockPiles = {suit: Pile() for suit in self.suits}
            self.deck.cards[0].flip()
        
        def getGameElements(self):
            returnObject = {
                "deck": str(self.deck),
                "playPiles": [str(pile) for pile in self.playPiles],
                "blockPiles": {suit: str(pile) for suit, pile in self.blockPiles.items()}
            }
            return returnObject
                
        
        def checkCardOrder(self,higherCard,lowerCard):
            suitsDifferent = self.suits[higherCard.suit] != self.suits[lowerCard.suit]
            valueConsecutive = self.values[self.values.index(higherCard.value)-1] == lowerCard.value
            return suitsDifferent and valueConsecutive

        def checkIfCompleted(self):
            deckEmpty = len(self.deck.cards)==0
            pilesEmpty = all(len(pile.cards)==0 for pile in self.playPiles)
            blocksFull = all(len(pile.cards)==13 for suit,pile in self.blockPiles.items())
            return deckEmpty and pilesEmpty and blocksFull
        
        def addToBlock(self, card):
            if card is None:
                return False
            elif len(self.blockPiles[card.suit].cards)>0:
                highest_value = self.blockPiles[card.suit].cards[0].value
                if self.values[self.values.index(highest_value)+1] == card.value:
                    self.blockPiles[card.suit].cards.insert(0,card)
                    return True
                else:
                    return False   
            else: 
                if card.value=="A":
                    self.blockPiles[card.suit].cards.insert(0,card)
                    return True
                else:
                    return False
    
        def takeTurn(self, verbose=False):
    
            #Pre: flip up unflipped pile end cards -> do this automatically
            [pile.cards[0].flip() for pile in self.playPiles if len(pile.cards)>0 and not pile.cards[0].flipped]

            # Store the result of getFirstCard() in a variable
            first_card = self.deck.getFirstCard()
            take_card = self.deck.takeFirstCard()

            #1: check if there are any play pile cards you can play to block piles
            for pile in self.playPiles:
                if len(pile.cards) > 0 and self.addToBlock(pile.cards[0]):
                    card_added = pile.cards.pop(0)
                    if verbose:
                        print("Adding play pile card to block: {0}".format(str(card_added)))
                    return True

            #2: check if cards in deck can be added
            if self.addToBlock(first_card):
                if verbose:
                    print("Adding card from deck to block: {0}".format(str(take_card)))
                return True
                

            #3: move kings to open piles
            for pile in self.playPiles:
                if len(pile.cards)==0: #pile has no cards
                    for pile2 in self.playPiles:
                        if len(pile2.cards)>1 and pile2.cards[0].value == "K":
                            card_added = pile2.cards.pop(0)
                            pile.addCard(card_added)
                            if verbose:
                                print("Moving {0} from Pile to Empty Pile".format(str(card_added)))
                            return True

                    if first_card is not None and first_card.value == "K":
                        pile.addCard(take_card)
                        if verbose:
                            print("Moving {0} from Deck to Empty Pile".format(str(take_card)))
                        return True

            #4: add drawn card to playPiles
            for pile in self.playPiles:
                if len(pile.cards)>0 and first_card is not None:
                    if self.checkCardOrder(pile.cards[0],first_card):
                        pile.addCard(take_card)
                        if verbose:
                            print("Moving {0} from Deck to Pile".format(str(take_card)))
                        return True

            #5: move around cards in playPiles
            for pile1 in self.playPiles:
                pile1_flipped_cards = pile1.getFlippedCards()
                if len(pile1_flipped_cards)>0:
                    for pile2 in self.playPiles:
                        pile2_flipped_cards = pile2.getFlippedCards()
                        if pile2 is not pile1 and len(pile2_flipped_cards)>0:
                            for transfer_cards_size in range(1,len(pile1_flipped_cards)+1):
                                cards_to_transfer = pile1_flipped_cards[:transfer_cards_size]
                                if self.checkCardOrder(pile2.cards[0],cards_to_transfer[-1]):
                                    pile1_downcard_count = len(pile1.cards) - len(pile1_flipped_cards)
                                    pile2_downcard_count = len(pile2.cards) - len(pile2_flipped_cards)
                                    if pile2_downcard_count < pile1_downcard_count:
                                        [pile2.cards.insert(0,card) for card in reversed(cards_to_transfer)]
                                        pile1.cards = pile1.cards[transfer_cards_size:]
                                        if verbose:
                                            print("Moved {0} cards between piles: {1}".format(
                                                transfer_cards_size,
                                                ", ".join([str(card) for card in cards_to_transfer])
                                                                                             ))
                                        return True
                                    elif pile1_downcard_count==0 and len(cards_to_transfer) == len(pile1.cards):
                                        [pile2.cards.insert(0,card) for card in reversed(cards_to_transfer)]
                                        pile1.cards = []
                                        if verbose:
                                            print("Moved {0} cards between piles: {1}".format(
                                                transfer_cards_size,
                                                ", ".join([str(card) for card in cards_to_transfer])
                                                                                             ))
                                        return True
            return False

        def simulate(self, draw = False, verbose=False):
        
            # clear cache if last turn was not card draw
            if not draw:
                self.deck.cache = []
        
            turnResult = self.takeTurn(verbose=verbose)
        
            if turnResult:
                self.simulate(verbose=verbose)
                    
            else:
                #End: draw from deck
                if len(self.deck.cards)>0:

                    currentCard = self.deck.cards[0]

                    if currentCard in self.deck.cache:
                        if verbose:
                            print("No more moves left!")
                        return 

                    else:
                        self.deck.drawCard()
                        #if verbose:
                            #print("Drawing new card: {0}".format(str(currentCard)))
                        self.deck.cache.append(currentCard)
                        return self.simulate(draw=True, verbose=verbose)
                else:
                    if verbose:
                        print("No more moves left!")
                    return

        def merge_sort(self):
            arr = self.deck.cards
            n = len(arr)
            temp_arr = [None] * n
            curr_size = 1
            while curr_size < n - 1:
                left = 0
                while left < n - 1:
                    mid = min((left + curr_size - 1), (n - 1))
                    right = ((2 * curr_size + left - 1,
                              n - 1)[2 * curr_size + left - 1 > n - 1])
                    i, j, k = left, mid + 1, left
                    while i <= mid and j <= right:
                        if arr[i].value <= arr[j].value:
                            temp_arr[k] = arr[i]
                            k += 1
                            i += 1
                        else:
                            temp_arr[k] = arr[j]
                            k += 1
                            j += 1
                    while i <= mid:
                        temp_arr[k] = arr[i]
                        k += 1
                        i += 1
                    while j <= right:
                        temp_arr[k] = arr[j]
                        k += 1
                        j += 1
                    for p in range(left, k):
                        arr[p] = temp_arr[p]
                    left = left + curr_size*2
                curr_size *= 2
            print("Sorted deck:")
            print('\n'.join([str(card) for card in arr]))
            return arr


    def main():

        thisGame = Game()
        thisGame.simulate(verbose=True)
        print()
        pp.pprint(thisGame.getGameElements())
        print()
        if(thisGame.checkIfCompleted()):
            print("Congrats! You won!")
        else:
            print("Sorry, you did not win")

        sorted_cards = thisGame.merge_sort()
        print("Sorted cards:", sorted_cards)
        return
    
    main()



