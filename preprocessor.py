# coding=utf-8
import re


def remove_special_chars(text):
    return re.compile(r'[\W]+', re.UNICODE).sub(' ', text)


def deduplicate_whitespace(text):
    return re.compile(r'[\s\n]+', re.UNICODE).sub(' ', text)


def clean(text):
    text = text.strip().lower()
    text = remove_special_chars(text)
    text = deduplicate_whitespace(text)
    words = text.split()
    return words


if __name__ == '__main__':
    text = u'To ja, czekoladowy niedźwiedź. Ala ma kota.'
    for word in clean(text):
        print word
