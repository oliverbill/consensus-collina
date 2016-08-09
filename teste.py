import sys
from collections import Counter

seq = sys.stdin.readline().split()
for letra in seq:
    mapa = Counter(letra)
seq_agrupada=""
for k in sorted(mapa.keys()):
    if(mapa.get(k) > 1):
        seq_agrupada += (str(k)+""+str(mapa.get(k)))
    else:
        seq_agrupada += (str(k))

print(seq_agrupada)
