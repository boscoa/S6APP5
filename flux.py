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