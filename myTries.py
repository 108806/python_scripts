import os
import sys

print(os.getcwd(), sys.executable)


class MyTrie:
    class Node:
        def __init__(self):
            self.terminal = False
            self.idx = 0
            self.dict = {}

    def __init__(self):
        self.root = self.Node()
        self.nodes = 0

    def insert(self, string: str|list):
        if isinstance(string, str):
            curr, created, existing = self.root, 0, 0
            for char in string:
                if char not in curr.dict:
                    curr.dict[char] = self.Node()
                    created += 1
                else:
                    existing += 1
                curr = curr.dict[char]
                curr.idx += 1
            curr.terminal = True
            self.nodes += created + existing
            return f'Inserted successfully {created + existing}, nodes created:{created}, nodes existing:{existing}'
        else:
            for s in string:
                self.insert(s)


if __name__ == '__main__':
    trie = MyTrie()
    trie.insert(['deadbeef', 'test', 'deadsummer'])
    print(trie)
