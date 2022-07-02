class Bor:
    def __init__(self):
        self.children = {}
        self.term = False
        self.cnt = 0

    def add(self, word):
        cur = self
        for c in word:
            if c not in cur.children:
                cur.children[c] = Bor()
            cur = cur.children[c]
        cur.term = True

    def check(self, word):
        cur = self
        for c in word:
            if c not in cur.children:
                return False
            cur = cur.children[c]
        return cur.term


bor = Bor()


def build():
    with open("checker/word_rus.txt", 'r') as f:
        for word in f.readlines():
            bor.add(word.strip())


def check_word(word):
    return bor.check(word)
