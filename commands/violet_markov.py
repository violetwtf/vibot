# !!! I DON'T GET ANY OF THIS CODE !!!
# !!! i stole it: https://towardsdatascience.com/markov-models-and-trump-tweets-91b0d3f0f1eb !!!
import random
import numpy
import discord
from commands.commands import Command
from util.undoers import get_simple_delete_undoer

_undo, _log = get_simple_delete_undoer('violetmarkov')

messages = []


def clean_markov_line(line):
    clean_line = []

    if len(line) == 0:
        return False

    if line[0] == '>':
        return False

    txt = line.split()

    for word in txt:
        clean_word = get_clean_word(word)
        if not clean_word:
            return

        clean_line.append(clean_word)

    return clean_line


def get_clean_word(word):
    end = word[len(word) - 1]

    if word[0] == '@' or word[0] == '<' or word[:4] == 'http':
        return False
    #elif end == '.' or end == '!' or end == '?':
    #    word = word[:-1]

    return word.strip().lower()


def generate_first_order_markov(data):
    markov_model = {}

    for line in data:
        for i in range(0, len(line)):
            markov_model[line[i]] = {}

    for line in data:
        for i in range(0, len(line) - 1):
            if line[i+1] in markov_model[line[i]]:
                markov_model[line[i]][line[i+1]] += 1
            else:
                markov_model[line[i]][line[i+1]] = 1

    return markov_model


def generate_occurrence_dict(data):
    word_occurrences = {}
    for line in data:
        for word in line:
            if word in word_occurrences:
                word_occurrences[word] += 1
            else:
                word_occurrences[word] = 1

    return word_occurrences


def normalize_first_order(markov_model, word_occurrences):
    for word in markov_model:
        for transition_word in markov_model[word]:
            markov_model[word][transition_word] = \
                markov_model[word][transition_word] / word_occurrences[word]

    return markov_model


def generate_second_order_markov(data):
    markov_model = {}

    for line in data:
        for i in range(0, len(line)):
            markov_model[line[i]] = {}

    for line in data:
        for i in range(0, len(line) - 1):
            markov_model[line[i]][line[i+1]] = {}

    for line in data:
        for i in range(0, len(line) - 2):
            if line[i+2] in markov_model[line[i]][line[i+1]]:
                markov_model[line[i]][line[i+1]][line[i+2]] += 1
            else:
                markov_model[line[i]][line[i+1]][line[i+2]] = 1

    return markov_model


def normalize_second_order(second_order_markov, first_order_markov):
    for first_word in second_order_markov:
        for second_word in second_order_markov[first_word]:
            for num_transitions in \
                    second_order_markov[first_word][second_word]:
                second_order_markov[first_word][second_word][num_transitions] = \
                    second_order_markov[first_word][second_word][num_transitions] \
                    / first_order_markov[first_word][second_word]

    return second_order_markov


def generate_random_phrase_second_order(data, normalized_second_order, normalized_first_order):
    first_word = data[random.randint(0, len(data))][0]

    second_word_possibilities = []
    second_word_probabilities = []

    for word in normalized_first_order[first_word]:
        second_word_possibilities.append(word)
        second_word_probabilities.append(
            normalized_first_order[first_word][word])

    if len(second_word_possibilities) == 0:
        return first_word

    second_word = numpy.random.choice(second_word_possibilities, 1,
                                      second_word_probabilities)[0]

    phrase = first_word + " " + second_word

    for i in range(10):
        next_word_possibilities = []
        next_word_probabilities = []
        for word in normalized_second_order[first_word][second_word]:
            next_word_possibilities.append(word)
            next_word_probabilities.append(
                normalized_second_order[first_word][second_word][word])

        if len(next_word_possibilities) == 0:
            return phrase

        next_word = numpy.random.choice(next_word_possibilities, 1,
                                        next_word_probabilities)[0]

        phrase += " " + next_word

        first_word = second_word
        second_word = next_word

    return phrase


def generate_random_phrase_first_order(data, normalized_first_order):
    start_word = data[random.randint(0, len(data))][0]
    next_word = start_word
    phrase = start_word

    for i in range(10):
        words = []
        probabilities = []

        for word in normalized_first_order[next_word]:
            words.append(word)
            probabilities.append(normalized_first_order[next_word][word])

        if len(words) == 0:
            return phrase

        next_word = numpy.random.choice(words, 1, probabilities)[0]
        phrase += " " + next_word.strip()

    return phrase


async def _handle(_, channel: discord.TextChannel, ___, m):
    data = []

    with open('assets/violet.txt') as violet_file:
        for line in violet_file:
            line = clean_markov_line(line)
            if line:
                data.append(line)

    first_order_markov = generate_first_order_markov(data)
    second_order_markov = generate_second_order_markov(data)
    word_occurrences = generate_occurrence_dict(data)

    normalized_first_order = normalize_first_order(first_order_markov,
                                                   word_occurrences)

    normalized_second_order = normalize_second_order(second_order_markov,
                                                     first_order_markov)

    phrase_first = generate_random_phrase_first_order(data,
                                                      normalized_first_order)
    phrase = generate_random_phrase_second_order(data, normalized_second_order,
                                                 normalized_first_order)
    _log(await channel.send(
        f'**first order:** {phrase_first}\n**second order:** {phrase}'), m)


violet_markov_cmd = Command(_handle, ['violetmarkov'],
                            'Generate a Markov-chain Violet message (Circuit)',
                            undo_executor=_undo)
