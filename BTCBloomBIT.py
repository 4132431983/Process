from bit import Key
from bit.format import bytes_to_wif
import random
from pathlib import Path
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate

mys = Path(__file__).resolve()
fil = 'found.txt'
myselff = Path(__file__).resolve()
ress = 'btc.bf'

a=1
with open(ress, "rb") as fp:
    bloom_filter = BloomFilter.load(fp)

while(True):
    list=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    d = random.choices(list, k=63)
    sect = "".join(d)
    xx = int(sect,16)
    key = Key.from_int(xx)
    wif = bytes_to_wif(key.to_bytes(), compressed=False)
    key1 = Key(wif)
    addrc = key.address
    addru = key1.ddress
    a += 1
    print("Top:",str(a), "priv:",sect, end='\r')
    if addrc in bloom_filter or addru in bloom_filter:
        print ("winner!!!!!!!!!!!!!!!!",sect)
        g=open(fil,"a")
        g.write("\n" + addrc)
        g.write("\n" + addru)
        g.write("\n" + str(sect))
        g.write("\n" + "DONATE: 3FerqQF5DVY1tPCEV7nXENoqxuVHGLjRh3")      
        g.close()