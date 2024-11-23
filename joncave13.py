#!/usr/bin/env python3

import cryptos
from cryptos import *
from pprint import pprint
import subprocess
import sys

c = Bitcoin(testnet=False)

priv=b'\x12\x34... etc.'
addrmyfrom=''
addrmyto=''
target = ''
moje=c.unspent(addrmyfrom)
jego=c.unspent(target)

o=open('broadcast.txt','w')
z=1
for l in open('txes.txt'):
	l=l.strip()

	ins = moje + jego
	bal=0
	for i in jego:
		bal += i['value']
	outs = [{'address': addrmyto, 'value': bal}]
	tx = c.mktx(ins, outs)
	tx['ins'][1]['script']=l
	tx['ins'][2]['script']=l
	tx['locktime']=0
	tx['hash_type']=0x03
	tx = c.sign(tx, 0, priv)
	#pprint(tx)
	t=serialize(tx)
	#print(t)
	o.write(t+'\n')
	o.flush()
	print("Line: "+str(z),file=sys.stderr)
	subprocess.run(["/mnt/c/Program Files/Bitcoin/daemon/bitcoin-cli.exe","sendrawtransaction",t])
	print(file=sys.stderr)
	z=z+1
