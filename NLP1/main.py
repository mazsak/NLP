import random
import string

import spacy

nlp = spacy.load("en_core_web_sm")


def one():
    with open('przyklad.txt', 'r') as f:
        doc = nlp(''.join(f.readlines()))
    with open('slownik.txt', 'w') as f:
        f.write(''.join([token.text + "\n" for token in doc if token.is_alpha]))


def remove_letter(word):
    letters = list(word)
    del letters[random.randint(0, len(letters) - 1)]
    return ''.join(letters)


def add_letter(word):
    letters = list(word)
    letters.insert(random.randint(0, len(letters) - 1), random.choice(string.ascii_letters))
    return ''.join(letters)


def change_letters(word):
    letters = list(word)
    letters[random.randint(0, len(letters) - 1)] = random.choice(string.ascii_letters)
    return ''.join(letters)


def two():
    with open('przyklad.txt', 'r') as f:
        doc = nlp(''.join(f.readlines()))
    words = [token.text for token in doc if token.is_alpha]
    indexes = range(len(words))
    indexes = random.choices(population=indexes, k=int(0.2 * len(indexes)))

    for index in indexes:
        if len(words[index]) > 3:
            for i in range(random.randint(1, 3)):
                change = random.random()
                if change < 0.33:
                    words[index] = add_letter(words[index])
                elif 0.33 <= change < 0.66:
                    words[index] = remove_letter(words[index])
                elif change >= 0.66:
                    words[index] = change_letters(words[index])

    index = 0
    words_to_save = []
    for token in doc:
        if token.is_alpha:
            words_to_save.append(words[index])
            index += 1
        else:
            words_to_save.append(token.text)

    with open('przyklad_z_bledami.txt', 'w') as f:
        f.write(' '.join(words_to_save))


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def three():
    with open('przyklad_z_bledami.txt', 'r') as f:
        doc = nlp(''.join(f.readlines()))
    with open('slownik.txt', 'r') as f:
        dictionary = [word.replace('\n', '') for word in f.readlines()]
    words = []
    for token in doc:
        if token.is_alpha:
            distance = []
            for word in dictionary:
                distance.append(levenshtein(token.text, word))
                if distance[-1] == 0:
                    break
            words.append(dictionary[distance.index(min(distance))])
        else:
            words.append(token.text)

    with open('przyklad_poprawiony.txt', 'w') as f:
        f.write(' '.join(words))


def four():
    with open('przyklad.txt', 'r') as f:
        doc = nlp(' '.join(f.readlines()))
    with open('przyklad_poprawiony.txt', 'r') as f:
        doc_fix = nlp(' '.join(f.readlines()))

    number_error = 0
    for index in range(len(doc)):
        if not doc[index].text == doc_fix[index].text:
            number_error += 1

    print("Number error: " + str(number_error) + "/" + str(len(doc)))


if __name__ == '__main__':
    one()
    two()
    three()
    four()
