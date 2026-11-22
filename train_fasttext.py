from gensim.models import FastText
from pathlib import Path
import os
import csv
from utils import preprocess


# == splitting processes down == #

def load_corpus(path : str) -> list[list[str]]:
    ''' loads the corpus from the said path '''
    result = []
    with open(path, mode = 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # skipping the header

        # preprocessing each line and adding the tokens to the dataset
        for row in reader:
            result.append(preprocess(row[0]))
        return row

def main():
    ''' learns the word2vec mappings and saves them '''
    # load the tokenized corpus
    tokenized_corpus = load_corpus(os.path.join(Path(__file__).resolve().parent, 'intent_clf_dataset/', 'shantae_intents.csv'))

    # learn the embedding
    model = FastText(vector_size=100, window=3, min_count=1)
    model.build_vocab(corpus_iterable = tokenized_corpus)
    model.train(corpus_iterable=tokenized_corpus, total_examples=len(tokenized_corpus), epochs = 5)

    # save the vector lookup
    wordvectors = model.wv
    wordvectors.save('vectors.wordvectors')

if __name__ == "__main__":
    main()