# coding=utf-8
import re


def split_into_sentences(text):
    return [s for s in re.split(r'[.;]', text) if len(s) > 0]


def remove_special_chars(text):
    return re.compile(r'[^\w.]+', re.UNICODE).sub(' ', text)


def deduplicate_whitespace(text):
    return re.compile(r'[\s\n]+', re.UNICODE).sub(' ', text)


def clean(text):
    text = text.strip().lower()
    text = remove_special_chars(text)
    text = deduplicate_whitespace(text)
    sentences = split_into_sentences(text)
    words = [s.split() for s in sentences]
    return words


if __name__ == '__main__':
    text = u'To ja, czekoladowy niedźwiedź. Ala ma kota.'
    for word in clean(text):
        print word
