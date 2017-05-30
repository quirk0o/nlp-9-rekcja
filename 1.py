# coding=utf-8
from collections import Counter

from collections import defaultdict
from plp import PLP

from corpus import Corpus

prepositions = [u'z', u'na', u'w', u'pod', u'do', u'o']
cases = [u'mianownik', u'dopełniacz', u'celownik', u'biernik', u'narzędnik', u'miejscownik', u'wołacz']

p = PLP()


def possible_cases(word):
    ids = p.rec(word)
    wcases = set([cases[(pos - 1) % len(cases)] for id in ids for pos in p.vec(id, word)])
    return wcases


def is_verb(word):
    ids = p.rec(word)
    verb = [p.label(id)[0] == PLP.CZESCI_MOWY.CZASOWNIK for id in ids]
    return any(verb)


def is_noun(word):
    ids = p.rec(word)
    noun = [p.label(id)[0] == PLP.CZESCI_MOWY.RZECZOWNIK for id in ids]
    return any(noun)


def is_prexp(word):
    ids = p.rec(word)
    noun = [p.label(id)[0] == PLP.CZESCI_MOWY.LICZEBNIK or
            p.label(id)[0] == PLP.CZESCI_MOWY.PRZYSLOWEK or
            p.label(id)[0] == PLP.CZESCI_MOWY.ZAIMEK for id in ids]
    return any(noun)


def get(list, index):
    try:
        return list[index]
    except IndexError:
        return None


if __name__ == '__main__':
    # print 'domu: {}'.format(
    #     ', '.join(['{} {}'.format(k.encode('utf-8'), v) for k, v in Counter(possible_cases(u'domu')).items()]))
    # print 'kropki: {}'.format(
    #     ', '.join(['{} {}'.format(k.encode('utf-8'), v) for k, v in Counter(possible_cases(u'kropki')).items()]))
    # print 'zamkowi: {}'.format(
    #     ', '.join(['{} {}'.format(k.encode('utf-8'), v) for k, v in Counter(possible_cases(u'zamkowi')).items()]))
    # print u'żółwiem: {}'.encode('utf-8').format(
    #     ', '.join(['{} {}'.format(k.encode('utf-8'), v) for k, v in Counter(possible_cases(u'żółwiem')).items()]))

    preposition_cases = defaultdict(lambda: defaultdict(lambda: 0))
    occurences = Counter()

    for doc, text in Corpus():
        for i, word in enumerate(doc):
            if word in prepositions:
                expression = []
                noun = None
                for j in xrange(i + 1, len(doc)):
                    if is_noun(doc[j]):
                        expression.append(doc[j])
                        break
                    elif is_prexp(doc[j]):
                        expression.append(doc[j])
                    else:
                        break
                if len(expression) == 0:
                    continue
                occurences[word] += 1

                wcases = [possible_cases(w) for w in expression]
                matched_cases = set.intersection(*wcases)
                while len(matched_cases) == 0 and len(expression) > 1:
                    expression.pop()
                    wcases = [possible_cases(w) for w in expression]
                    matched_cases = set.intersection(*wcases)

                # if len(expression) > 1:
                #     print word, ' '.join(expression), wcases, matched_cases

                for case in matched_cases:
                    preposition_cases[word][case] += 1.0 / len(matched_cases)

    for p in prepositions:
        for case in preposition_cases[p]:
            preposition_cases[p][case] /= occurences[p]
        for case, count in preposition_cases[p].items():
            if count < 0.15:
                del preposition_cases[p][case]

        print p
        for case, count in preposition_cases[p].items():
            print case, count
