'''
Created on 2009-07-14

@author: Administrateur
'''

import os.path
import sys
import array

sys.setrecursionlimit(1000000)

# Procedure qui doit etre modifiee pour que le systeme fonctionne
def get_masque_8bits(cle):
    masque = 0
    masque = cle & 0xff
    return masque

# Procedure qui doit etre modifiee pour que le systeme fonctionne
def get_cle_modifiee(cle):
    nouvelle_cle = 0
    nouvelle_cle = cle >> 8
    return nouvelle_cle

# Procedure qui doit etre modifiee pour que le systeme fonctionne
def chiffre_caractere(caractere,masque):
    nouveau_caractere = caractere
    nouveau_caractere = nouveau_caractere ^ masque
    return nouveau_caractere

# Procedure qui doit etre modifiee pour que le systeme fonctionne
def mise_a_jour_cle(tmpcle,cle):
    nouvelle_cle = 0
    if tmpcle == 0:
    	nouvelle_cle = cle
    else:
    	nouvelle_cle = tmpcle

    return nouvelle_cle


# Methode de chiffrement / dechiffrement par flux
# La cle est utilisee pour chiffrer le fichier d'entree (fichierin) et produire le fichier de sortie (fichierout)
# Si la cle est plus petite que la taille du fichier, elle doit etre repetee (est-ce une bonne idee?)
def chiffre_flux(cle,fichierin,fichierout):
    tmpcle = cle
    
    # Initialisation des fichiers en lecture et ecriture
    infileobj = open(fichierin,'rb')     # Lecture binaire du fichier
    outfileobj = open(fichierout,'wb')   # Ecriture binaire du fichier
    filesize = os.path.getsize(fichierin)
    
    # Initialisation des tableaux binaires, lecture du fichier d'entree (binaire)
    inbinvalues = array.array('B')
    inbinvalues.fromfile(infileobj, filesize)
    outbinvalues = array.array('B')
    
    # Traitement de tous les caracteres du fichier d'entree, un a la fois
    i = 0
    while (i < filesize):
        # Obtention du masque pour le prochain caractere, chiffrement de ce caractere
        mask = get_masque_8bits(tmpcle)
        tmpcle = get_cle_modifiee(tmpcle)
        newchar = chiffre_caractere(inbinvalues[i], mask)
        # Ecriture du cactere chiffre dans le tampon de sortie
        outbinvalues.append(newchar)
        
        i += 1
        tmpcle = mise_a_jour_cle(tmpcle,cle)

    # Ecriture dans le fichier de sortie, fermeture des fichiers
    infileobj.close()
    outbinvalues.tofile(outfileobj)
    outfileobj.close()

def pgcd(x, y):
	while y != 0:
		(x, y) = (y, x%y)
	return x

def xgcd(e, phi_n):
	x0, x1, y0, y1 = 1, 0, 0, 1
	while phi_n != 0:
		q, e, phi_n = e // phi_n, phi_n, e % phi_n
		x0, x1 = x1, x0 - q * x1
		y0, y1 = y1, y0 - q * y1

	return e, x0, y0

def puissance_mod(a, w, n):
	if w == 0:
		return 1
	r = puissance_mod(a, w//2, n)
	r = (r * r) % n

	if w % 2:
		r = (r * a) % n
	
	return r

def polynome(x):
	return x**2 + 1
	
def pollard_rho(n):
	x = 1; y = 1; z = 1; m = 100000
	while True:
		x = polynome(x) % n
		y = polynome(polynome(y) % n) % n
		z = (z * abs(x - y)) % n
		m = m - 1
		
		if m == 0:
			p = pgcd(n, z)
			if p != 1:
				return p
			
			z = 1; m = 100000
	
def pollard_pm1(n):
	m = 2
	max = 100000

	for i in range(1, max):
		m = puissance_mod(m, i, n)
		a = pgcd(n, m-1)
		if a != 1:
			return a

def euclide(e, phi_n):
	g, x, _ = xgcd(e, phi_n)
	if g == 1:
		return x % phi_n

n = 71632723108922042565754944705405938190163585182073827738737257362015607916694427702407539315166426071602596601779609881448209515844638662529498857637473895727439924386515509746946997356908229763669590304560652312325131017845440601438692992657035378159812499525148161871071841049058092385268270673367938496513
e = 1009
p = pollard_pm1(n)
q = n//p
phi_n = (p - 1) * (q - 1)

d = euclide(e, phi_n)


qdh_chiffre_avec_RSA = 70785482415899901219256855373079758876285923471951840038722877622097582944768442919300478197733262514534911901131859013939654902078384994979880540719293485131574905521151256806126737353610928922434810670654618891838295876181905553857594653764136067479449117470741836721372149447795646290103141292761424726007
pdh_chiffre_avec_RSA = 55044587110698448189468021909149190373421069219506981148292634221985403129928367209713497911359302701069378532959510957622709061077384648566361893749771744973388835727259855002207844685526295296408852878202498675158924213264474587673461598376054133832370354928763624202425050121409987087150490459351809040858
gdh_chiffre_avec_RSA = 43089172300844684958445369204000423742543038862350925279569289644298734265625491619486408239703259462606739540181409010715678916496299388069246398890469779970287613357772582024703107603034996120914490203805569384580718393586094166173301167583379300330660182750028000520221960355249560831414918130647224546308

q = puissance_mod(qdh_chiffre_avec_RSA, d, n)
p = puissance_mod(pdh_chiffre_avec_RSA, d, n)
g = puissance_mod(gdh_chiffre_avec_RSA, d, n)

print (p)
print (g)

# Appel de la methode de chiffrement / dechiffrement de fichiers
chiffre_flux(g, "salaires.mm","sortie.txt")

alain = 81530476374664351124876242644701327168836407987
michele = 83740877821201430552252653974153238737996745098
stephanie = 51373667846507963545859239582447701017826406175
fernand = 61167846837720209456441528754183777549647735855
angele = 42340513171888188994504759277496496710896088718
bernard = 65069303637151076134861115122997306654987857614
claude = 32785990179062766920584737848735367794508677603

n = 86062381025757488680496918738059554508315544797
e = 13
p = pollard_rho(n)
q = n//p
phi_n = (p - 1) * (q - 1)

d = euclide(e, phi_n)
alain_salaire = puissance_mod(alain, d, n)
michele_salaire = puissance_mod(michele, d, n)
stephanie_salaire = puissance_mod(stephanie, d, n)
fernand_salaire = puissance_mod(fernand, d, n)
angele_salaire = puissance_mod(angele, d, n)
bernard_salaire = puissance_mod(bernard, d, n)
claude_salaire = puissance_mod(claude, d, n)
print ("Salaire Alain: ", alain_salaire)
print ("Salaire Michele: ", michele_salaire)
print ("Salaire Stephanie: ", stephanie_salaire)
print ("Salaire Fernand: ", fernand_salaire)
print ("Salaire Angele: ", angele_salaire)
print ("Salaire Bernard: ", bernard_salaire)
print ("Salaire Claude: ", claude_salaire)
