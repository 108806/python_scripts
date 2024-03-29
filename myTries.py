import os
import sys

print(os.getcwd(), sys.executable, hex(id(globals())))


class MyTrie:
    class Node:
        def __init__(self):
            self.terminal = False
            self.lvl = 0
            self.dict = {}
            self.root = None

        def word(self):
            if self.dict:
                ret = list(self.dict.keys())[0]
                curr = self
                while curr.root:
                    curr = curr.root
                    ret += list(curr.dict.keys)[0]
                return ''.join(ret)

    def __init__(self):
        self.root = self.Node()
        self.nodes = 0
        self.longest_node = self.root

    def insert(self, string: str | list):
        if isinstance(string, str):
            print('Inserting:', string, len(string))
            curr, created, existing = self.root, 0, 0
            for char in string:
                if char not in curr.dict:
                    curr.dict[char] = self.Node()
                    created += 1
                else:
                    existing += 1
                curr.dict[char].lvl = curr.lvl +1
                curr.dict[char].root = curr
                curr = curr.dict[char]
            curr.terminal = True
            self.nodes += created + existing
            return f'Inserted successfully {created + existing}, nodes created:{created}, nodes existing:{existing}'
        else:
            for s in string:
                self.insert(s)

    def contains(self, string: str | list) -> bool:
        if isinstance(string, str):
            curr = self.root
            for character in string:
                if character in curr.dict:
                    curr = curr.dict[character]
                else:
                    return False
            return True
        else:
            for s in string:
                assert isinstance(s, str), f"ERR: s -> {s} is not a str"
                self.contains(s)

    def is_longest(self, node: Node):
        if node.lvl > self.longest_node.lvl:
            self.longest_node = node
            return True
        return False

    def set_longest(self, node=''):
        if not node:
            node = self.longest_node
        for key in node.dict:
            self.is_longest(node.dict[key])
            self.set_longest(node.dict[key])

    def get_longest(self):
        self.set_longest()
        return self.longest_node

    def has_others(self, node: Node) -> bool:
        if len(node) > 1:
            return True
        return False






if __name__ == '__main__':
    trie = MyTrie()
    trie.insert(['deadbeef', 'test', 'deadsummer'])
    print(trie, trie.contains('best'))
    longest = trie.get_longest()
    print(longest.lvl, longest.dict, longest, longest.root.dict, longest.word())
