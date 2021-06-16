# MTG Arena Draft Maindeck Assistant
Machine learning model to determine what cards to maindeck from a draft. Built using a neural network and uses maindeck data from decks that were able to win at least 3 games. This repository is currently setup to train and infer using the STX draft data from 17Lands.com and might be updated for future sets.

## Dependency Versions
These are not requirements just the versions I used.

    tensorflow==2.5.0
    keras==2.5.0
    numpy==1.19.5

## Pretrained model
The repository includes a pretrained model labeled PretrainedModel.h5. Just run the inference python file and input the path to use.

## Building the model
The training and validation dataset is "STX Premier Draft Game Data" located at [https://www.17lands.com/public_datasets](https://www.17lands.com/public_datasets) and is needed if you wish to build the modem yourself.
1. Unzip the dataset set from the tar.gz file linked above, place it in the same directory as the data_extraction.ipynb file.
2. Launch a Jupyter Notebook instance and run all the cells in data_extraction.ipynb.
3. It will preprocess and extract the relevant data from the dataset and generate a bunch of .npy files in the /data directory.
4. Run all the cells in modelling.ipynb in Jupyter. It will use all the data extracted and processed earlier to generate a model called MainDeckModel.h5. The training will automatically stop after 5 epochs without any improvement to the MAE of the validation data.

## Running the modem.
1. Obtain a draft from MTG Arena by completing an STX draft and exporting the drafted cards into a text file.
2. Run the inference.py file and input the draft export path and the trained model path.
3. You will then get an output of the ~22-25 cards to maindeck which does not include basic lands.