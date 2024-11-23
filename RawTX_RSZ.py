import bitcoin
import hashlib
import txnUtils
import keyUtils

tx = "01000000000101a5baeec1f82ae53464ac147e3c5b9ef9dd60183338b7ae65ca4bcc227a2d042d0000000023220020096def7756afb4dba661ec58602cf6af1f7881e48e4b8a8c12be9985073f5adeffffffff0276fa210d0000000017a914572290324c72e6842e8a77c2cbb9882a3b9c2a9f870af5502c000000001976a914f3183745fd504e1ed44e17ba802ba5f7b22fbd2988ac03483045022100a763df74b02b9a3fbe9a8f0e554e97a55dc3320945152ced74717b2ccd44e6d302202bac1a7800eaad0f2241b672bf7d94ce7fe5c5d2f45f2fa7939dd08b4a13a826012102a52b3f9958c0f4b57b99f287832ea75775ddf7c83fa0648b6b1545ec4881ef2d1976a91401121fe150c9b05f9146bac57ad9947ea5c1478e88ac00000000"

m = txnUtils.parseTxn(tx)
e = txnUtils.getSignableTxn(m)
z = hashlib.sha256(hashlib.sha256(e.decode('hex')).digest()).digest()
z1 = z[::-1].encode('hex_codec')
z = z.encode('hex_codec')
s = keyUtils.derSigToHexSig(m[1][:-2])
pub =  m[2]
sigR = s[:64]
sigS = s[-64:]
sigZ = z
print ('Signed TX is :', tx)
print ('Signature (r, s pair) is :', s)
print ('Public Key is :', pub)
print ("")
print ("#################################################################################################")
print ("")
print ('Unsigned TX is :', e)
print ('hash of message (sigZ) is USE This ONE :', z)
print ('reversed z :', z1)
print ("")
print ("#################################################################################################")
print ("##################################VALUES NEEDED ARE BELOW #######################################")
print ("#################################################################################################")
print ("")
print ('THE R VALUE is  :', sigR)
print ('THE S VALUE is  :', sigS)
print ('THE Z VALUE is  :', sigZ)
print ('THE PUBKEY is :', pub)


