# coding:utf-8
import os

import gensim
import smart_open
from gensim.models.doc2vec import Doc2Vec
import logging


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        i = 0
        for fname in os.listdir(self.dirname):
            if fname.endswith('-str.txt'):
                with smart_open.open(os.path.join(self.dirname, fname)) as f:
                    for line in f:
                        tokens = gensim.utils.simple_preprocess(line)
                        i += 1
                        yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


def train():
    train_corpus = MySentences('../data')
    model = Doc2Vec(train_corpus, min_count=2, vector_size=50, epochs=40)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    model.save('model_all_string')

    return model


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    model_dm = train()
    vector = model_dm.infer_vector('vertical align middle'.split())
    print(vector)
