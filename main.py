
import load_words


NO = 'n'
MAYBE = 'm'
YES = 'y'

YMN_set = set([YES, MAYBE, NO])



bad_letters = set()
potential_letters = set()
found_letters = {} # 4 -> 'e'



# reduce the word list into a sublist of valid potential words
def reduce_word_list(words, found_letters, potential_letters, bad_letters):

    new_words = []

    for word in words:

        valid_word = True
        position = 0
        potential_letter_matches = dict.fromkeys(potential_letters, 0)

        for c in word:

            # if there is a bad letter, then don't use it
            if c in bad_letters:
                valid_word = False
                break

            # iterate over the found letters and ensure things are in the right spot
            if position in found_letters and c != found_letters[position]:
                valid_word = False
                break

            # found the potential position letter
            if c in potential_letters:
                potential_letter_matches[c] += 1

            position += 1

        # ensure that you find at least one match in the potential word
        if valid_word:
            for c in potential_letter_matches:
                if potential_letter_matches[c] == 0:
                    valid_word = False
                    break

        if valid_word is True:
            new_words.append(word)

    return new_words

def get_char_freq(words):
    d = {}
    for word in words:
        for c in word:
            if c not in d:
                d[c] = 0
            d[c] += 1
    return d

def get_scored_word_list(current_word_list, current_char_freq):

    """
        You get a higher score with more of a char freq
    """

    def _score(word, current_char_freq):
        score = 0
        for char in word:
            if char in current_char_freq:
                score += current_char_freq[char]

        return score


    scored_list = [(x, _score(x, current_char_freq)) for x in current_word_list]

    # sort based on score
    scored_list.sort(key=lambda x: x[1], reverse = True)

    return scored_list


def set_user_inputs_into_state(user_input):
    counter = 0
    for u in user_input:
        char = u[0]
        y_n_m = u[1]

        print(char)
        print(y_n_m)
        print('------')

        if y_n_m == YES:
            found_letters[counter] = char
        elif y_n_m == NO:
            bad_letters.add(char)
        else:
            potential_letters.add(char)

        counter += 1



# parts
# p-y a-n r-m t-y s-n
def get_user_input():
    user_input = input("Enter in the results from the previous guess:\n")
    parts = user_input.split(' ')

    if len(parts) != 5:
        return None

    ret_value = []
    for part in parts:
        mini_parts = part.split('-')
        if len(mini_parts) != 2:
            print(part + " is not of the format a-y")
            return None

        mini_parts[0] = mini_parts[0].lower()
        mini_parts[1] = mini_parts[1].lower()

        if not mini_parts[0].isalpha():
            print(mini_parts[0] + " is not alpha")
            return None

        if mini_parts[1] not in YMN_set:
            print(mini_parts[1] + " not in " + str(YMN_set))
            return None

        ret_value.append((mini_parts[0], mini_parts[1]))

    return ret_value



# w = reduce_word_list(load_words.load(), {0: 'e', 1: 'r'}, set(), set())
# w = reduce_word_list(load_words.load(), {}, set(['p', 'e']), set())
# w = reduce_word_list(load_words.load(), {}, set(), set(['a', 'b', 'c', 'd', 'e', 'f']))

current_word_list = load_words.load()
current_char_freq = get_char_freq(current_word_list)


current_counter = 0
while current_counter != 6:

    print("total potential words: {}".format(len(current_word_list)))
    print("found letters: {}".format(str(found_letters)))
    print("potential letters: {}".format(str(potential_letters)))
    print("bad letters: {} \n".format(str(bad_letters)))

    print("Potential options")
    print(str(get_scored_word_list(current_word_list, current_char_freq)[0:10]) + " \n")

    user_input = get_user_input()

    if user_input == None:
        print("invalid input\n")
        continue
    else:
        # increment the state
        set_user_inputs_into_state(user_input)

        # recalc the word-related values
        current_word_list = reduce_word_list(current_word_list, found_letters, potential_letters, bad_letters)
        current_char_freq = get_char_freq(current_word_list)



    current_counter += 1
