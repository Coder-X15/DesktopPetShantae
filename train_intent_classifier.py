from gensim.models import KeyedVectors
import numpy as np
from utils import preprocess
import pandas as pd
import os
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier # we'll use an MLP Classifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV
import tqdm
import joblib

# declaring some globals here
wv = KeyedVectors.load(os.path.join(Path(__file__).resolve().parent, 'vectors.wordvectors'))
TRAIN_PATH = os.path.join(Path(__file__).resolve().parent, 'intent_clf_dataset/', 'train.csv')
VAL_PATH = os.path.join(Path(__file__).resolve().parent, 'intent_clf_dataset/', 'val.csv')
TEST_PATH = os.path.join(Path(__file__).resolve().parent, 'intent_clf_dataset/', 'test.csv')
DEFAULT_TEXT_LABEL='text'
DEFAULT_INTENT_LABEL='intent'
EMBEDDING_SIZE=100 # default embedding size

# we'll fit the LabelEncoder on the parent dataset's `intent` column
labenc = LabelEncoder()
_ = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'intent_clf_dataset/', 'shantae_intents.csv'))
labenc = labenc.fit(_['intent'])

def sentence_embedding(sentence : str) -> np.ndarray:
    ''' generates sentence embeddings '''
    tokens = preprocess(sentence)
    result = np.zeros((EMBEDDING_SIZE,))
    for token in tokens:
        try:
            result = np.vstack(wv[token])
        except:
            result = np.vstack(np.full(result[0,:].shape, 0.01))
    return result.sum(axis=1)

def generate_dataset(dataset_path : str) -> tuple[np.ndarray, np.ndarray]:
    ''' construct the vector dataset for training and return as X, y '''
    df = pd.read_csv(dataset_path)
    df[DEFAULT_INTENT_LABEL] = labenc.transform(df[DEFAULT_INTENT_LABEL])
    embd = np.array([sentence_embedding(x) for x in tqdm.tqdm(df[DEFAULT_TEXT_LABEL])])
    return embd, df[DEFAULT_INTENT_LABEL].to_numpy()

def main() -> None:

    print("Loading training set: ", end=" ")
    trainX, trainy = generate_dataset(TRAIN_PATH)

    print("Loading validation set: ", end=" ")
    valX, valy = generate_dataset(VAL_PATH)

    print("Loading testing set: ", end=" ")
    testX, testy = generate_dataset(TEST_PATH)

    # construct the search grid
    search_grid = {
        'hidden_layer_sizes' : [(30, 30), (30, 30, 10), (100, 100, 100)], 
        'learning_rate_init':[0.00055, 0.001, 0.005, 0.007],
        'random_state' : [0, 42, 100],
        'learning_rate' : ['adaptive']
    }

    # declare the model
    mlp = GridSearchCV(
        estimator=MLPClassifier(max_iter=3000),
        param_grid=search_grid,
        scoring='f1_macro', # ,'balanced_accuracy'
        n_jobs=-1,
        refit=False
    )

    # train
    mlp.fit(trainX, trainy)

    # best fit model params
    best_params= mlp.best_params_
    print("Best fit model has params:", best_params)

    # replace mlp with best estimator
    mlp = MLPClassifier(
        hidden_layer_sizes=best_params['hidden_layer_sizes'],
        solver='adam',
        learning_rate=best_params['learning_rate'],
        learning_rate_init=best_params['learning_rate_init'],
        random_state=best_params['random_state'], max_iter=3000
    )

    mlp.fit(trainX, trainy)

    # check training results on validation set
    print("Training done. Report on validation set: \n==================")
    pred = mlp.predict(valX)
    print(classification_report(valy, pred))

    # print test accuracy
    pred = mlp.predict(testX)
    print(f"Test accuracy: %.2f"%(accuracy_score(testy, pred)))

    joblib.dump(mlp, 'mlp.joblib') # save the model

    

if __name__ == "__main__":
    print(labenc.classes_) # the classes will be printed in the order of their assignment
    main()


