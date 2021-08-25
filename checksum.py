#!/usr/bin/env python3
import random



def main():
	id="ABBA"
	cc=get_checksum(id)
	print ("Z%s-%s" % (id,cc))

	for i in range(1,10):
		c=get_checksum("16%s" % i)
		print ("16%s%s" % (c,i))

	for i in range(1,10):
		c=get_checksum("15%s" % i)
		print ("15%s%s" % (c,i))

"""
	
A 10	B 11	C 12	D 13	E 14	F 15	G 16	H 17	I 18	J 19	K 20	L 21	M 22
N 23	O 24	P 25	Q 26	R 27	S 28	T 29	U 30	V 31	W 32	X 33	Y 34	Z 35

Moduli 37

1. Annetaan kullekin tarkistettavalle kirjaimelle numeerinen arvo passien yhteydessä esitetyn taulukon mukaisesti. Kaikille merkeille jotka eivät ole numeroita 0..9 tai kirjaimia A..Z annetaan arvo 36 (pieniä kirjaimia ei käytetä).
2. Painotetaan tarkistettavia merkkejä oikealta alkaen kertoimilla 3, 1, 3, 1 jne.. Lasketaan tulot yhteen.
3. Tarkisteen numeerinen arvo on luku, joka summaan on lisättävä jotta tulos olisi tasan jaollinen 37:llä.
	Jos arvo on yksinumeroinen, se on tarkiste.
	Jos arvo on 10..35, tarkiste on kohdassa 1 mainitun taulukon mukainen kirjain.
	Jos arvo on 36, tarkiste on "#".

"""

def get(s):
	cv={"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"A":10,"B":11,"C":12,"D":13,"E":14,"F":15,"G":16,"H":17,"I":18,"J":19,"K":20,"L":21,"M":22,"N":23,"O":24,"P":25,"Q":26,"R":27,"S":28,"T":29,"U":30,"V":31,"W":32,"X":33,"Y":34,"Z":35,"#":36,"-":37}
	
	sum=0
	for i in range(0,len(s)):
		if i % 2 == 0:
			k = 1
		else:
			k = 3
		sum+=k*cv[s[i]]
		#print (i,s[i],k,cv[s[i]],k*cv[s[i]],sum)
	ad=sum % 37
	
	for i in cv.keys():
		if cv[i]==ad:
			cc = i
			break
	
	#print (cc)
	return(cc)



if __name__=='__main__':
	main()