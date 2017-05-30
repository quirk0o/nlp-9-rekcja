import codecs
import re

from preprocessor import clean

corpus_filename = 'data/pap.txt'
document_sep = '#\d+'


class Corpus(object):
    def __init__(self):
        self.__documents = None

    def __load_documents(self):
        with codecs.open(corpus_filename, encoding='utf-8') as corpus_file:
            documents = re.split(document_sep, corpus_file.read())
            self.__documents = documents

    def get(self, key):
        if self.__documents is None:
            self.__load_documents()
            return self.__documents[key]

    def all_ids(self):
        if self.__documents is None:
            self.__load_documents()
        return range(0, len(self.__documents))

    def __iter__(self):
        with codecs.open(corpus_filename, encoding='utf-8') as corpus_file:
            text = ''
            for line in corpus_file:
                if re.match(document_sep, line):
                    yield self.transform_text(text), text
                    text = ''
                else:
                    text = text + line

            yield self.transform_text(text), text

    def transform_text(self, doc):
        return [word for word in clean(doc)]


if __name__ == '__main__':
    for text in Corpus():
        print text
