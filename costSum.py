"""
Simple cost counter,
 use the file with lines like 'tv 150(EOL),car 1500(EOL)'
"""

import itertools
from time import sleep
__author___ = "ansgar.snow"


dokument = input("Give me the file with the prices at the end of the lines\n")

v = []
lista_ = [x for x in open(dokument)]
for x in lista_:
    v.append(x.split()[-1:])

res = list(map(int, (itertools.chain.from_iterable(v))))
print(sum(res))
sleep(10)
exit()
