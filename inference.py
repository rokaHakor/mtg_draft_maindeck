import numpy as np
from pickle import load
from tensorflow import keras
import argparse

def specialround(deck, draft):
  copydeck = deck.copy()
  for index, value in enumerate(copydeck):
    if value < 0.5:
      copydeck[index] = 0
    else:
      copydeck[index] = min(np.ceil(value), draft[index])
  return copydeck

def totalcards(deck):
    x = 0
    for i in deck:
        x += i
    return x

def exporttodraft(deckexport):
  draft = np.zeros(343)
  maindeck = np.zeros(343)
  includemain = True
  for index, value in enumerate(deckexport):
    if value.startswith('Sideboard'):
      includemain = False
    split = value.split(" ", 1)
    if len(split) == 2:
      name = split[1].split("(", 1)
      card_name = name[0].strip()
      if card_name == "Mountain" or card_name == "Island" or card_name == "Plains" or card_name == "Swamp" or card_name == "Forest":
        continue
      cardindex = card_dict[card_name]
      draft[cardindex] = draft[cardindex] + int(split[0])
      if includemain:
        maindeck[cardindex] = maindeck[cardindex] + int(split[0])
  return draft, maindeck

def printcards(deck):
    for index, card in enumerate(deck):
        if card > 0:
            print(card_index[index] + ", " + str(card))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--model_path", action="store", dest="model_path",
        required=False,
        help=("path to the trained model ")
    )
    parser.add_argument(
        "--test_path", action="store", dest="test_path",
        required=False,
        help=("path to the test draft text file ")
    )

    args = parser.parse_args()
    model_path = args.model_path
    test_path = args.test_path

    if model_path is None:
        model_path = input("Enter path to the trained model: ")

    if test_path is None:
        test_path = input("Enter path to the test draft text file: ")

    with open('data/indextocard.pkl', 'rb') as f:
        f.seek(0)
        card_index = load(f)
    with open('data/cardtoindex.pkl', 'rb') as f:
        f.seek(0)
        card_dict = load(f)

    model = keras.models.load_model(model_path)

    f = open(test_path, "r")
    deckexport = f.readlines()
    draft, maindeck = exporttodraft(deckexport)
    result = model.predict(np.array([draft]))

    preddeck = specialround(result[0], draft)
    print("----- Drafted Cards: " + str(totalcards(draft)))
    printcards(draft)
    print("----- Predicted Deck: Cards " + str(totalcards(preddeck)))
    printcards(preddeck)
