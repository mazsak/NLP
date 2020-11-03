import sys
from collections import Counter

import spacy

nlp = spacy.load('en_core_web_sm')

with open('text.txt', 'r') as f:
    text = ' '.join(f.readlines())

doc = nlp(text)


def count_sentences():
    print(f'Amount sentences: {len(list(doc.sents))}')


def count_tokens():
    print(f'Amount tokens: {len(doc)}')


def mean_token_to_sentence():
    print(f'Mean (tokens/sentences): {len(doc) / len(list(doc.sents))}')


def number_part_of_sentence():
    pos = Counter()
    for token in doc:
        pos[token.pos_] += 1

    print(f'Amount nouns: {pos["NOUN"] + pos["PROPN"]}')
    print(f'Amount verbs: {pos["VERB"]}')
    print(f'Amount adjectives: {pos["ADJ"]}')
    print(f'Amount adverbs: {pos["ADV"]}')


def amount_nouns():
    nouns = Counter()
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN']:
            nouns[token.lemma_] += 1
    return nouns


def most_occurrences_of_nouns():
    nouns = amount_nouns()
    print(f'5 most common nouns: {nouns.most_common(5)}')


def adjectives_that_define_nouns():
    nouns = [noun[0] for noun in amount_nouns().most_common(2)]
    adjectives = {}
    for noun in nouns:
        adjectives[noun] = []
    for token in doc:
        if token.lemma_ in nouns:
            adjectives[token.lemma_].extend([child for child in token.children if child.pos_ == 'ADJ'])
    print('Adjectives that define nouns:')
    for adjective in adjectives.keys():
        print(f'{adjective}: {adjectives[adjective]}')


if __name__ == '__main__':
    stdoutOrigin = sys.stdout
    sys.stdout = open("nlp.txt", "w")
    count_sentences()
    count_tokens()
    mean_token_to_sentence()
    number_part_of_sentence()
    most_occurrences_of_nouns()
    adjectives_that_define_nouns()
    sys.stdout.close()
    sys.stdout = stdoutOrigin
