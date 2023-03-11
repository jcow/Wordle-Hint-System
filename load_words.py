

def load():
    words = []
    with open('words.txt') as f:
        for line in f:
            words.append(line.strip())

    return words
