from gensim.models import FastText
from utils import preprocess
import nltk
from nltk.corpus import brown


# == splitting processes down == #

def load_corpus() -> list[list[str]]:
    ''' loads NLTK corpus '''
    result = []
    categories = ['fiction', 'news']
    corpus = [" ".join(sentence) for sentence in brown.sents(categories = categories)]
    
    for sentence in corpus:
        result.append(preprocess(sentence))
    return result

def main():
    ''' learns the word2vec mappings and saves them '''
    # load the tokenized corpus
    tokenized_corpus = load_corpus()

    # learn the embedding
    model = FastText(vector_size=100, window=3, min_count=1)
    model.build_vocab(corpus_iterable = tokenized_corpus)
    model.train(corpus_iterable=tokenized_corpus, total_examples=len(tokenized_corpus), epochs = 5)

    # save the vector lookup
    wordvectors = model.wv
    wordvectors.save('vectors.wordvectors')

if __name__ == "__main__":
    nltk.download('brown')
    main()