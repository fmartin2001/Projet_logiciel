import numpy as np
import random as rd

def check_yes(mat, num, att) :
    """
    Détermine si une photo possède une caractéristique
    Entrée : matrice, numéro de la photo, attibu en question
    Sortie : booléen, 1 si possède la caractéristique, 0 sinon
    """

    att = 0
    if mat[num][att] == 1 :
        att = 1

    return att

def check_sex(num, mat) :
    """
    Donne le sexe correspondant à une image
    Entrée : numéro de l'images
    Sortie : booléen, 1 si un homme, 0 si une femme
    """

    att = 0
    if mat[num][20] == 1 :
         att = 1

    return att

def enough_attribs(att, pic, matr) :
    """
    Détermine si une image correspond à au moins 2 critères de la liste en plus du sexe
    Entrée : liste d'indexes des attributs recherchés, numéro de l'images, matrice des caractéristiques
    Sortie : booleen, 1 si correspond; 0 sinon
    """

    ok = 0
    count = 0

    for i in range(1, len(att)) :
        if check_yes(matr, pic, att[i]) :
            count = count + 1

    if check_sex(pic, matr) == att[0] and count >= 2 :
        ok = 1

    return ok


def rank_attrib(att, all) :
    """
    Trouve les index des attributs voulus
    Entrée : liste d'attributs souhaités sous forme de strings, liste de tous les attributs
    Sortie : liste des indexes des attributs
    """

    indexes = []
    indexes.append(att[0])

    for i in range(1, len(att)) :
        for j in range(len(all)) :
            if att[i] == all[j] :
                indexes.append(j)

    return indexes

def make_list(attributs, nb_pic) :
    """
    Prend des images de façon aléatoire avec les caractéristiques souhaitées
    Entrée : liste des caractéristiques souhaitées, la première caractéristique doit être 1 si c'est un homme ou 0 si c'est une femme, nombre d'images souhaitées
    Il faut que la première caractéristique soit 0 ou 1 selon si c'est une femme ou homme
    Sortie : liste des index des images avec les caractéristques
    """
    usecols = []
    for i in range(1, 41) :
        usecols.append(i)

    matrice = np.loadtxt('list_attr_celeba.txt', skiprows = 2, usecols = usecols)
    all_att = np.loadtxt('list_attr_celeba.txt', dtype = str, skiprows = 1, max_rows = 1)

    pic_list = []
    rank_att = rank_attrib(attributs, all_att)


    for i in range(nb_pic) :

        while len(pic_list) < nb_pic :
            index = rd.randint(0, 202598)
            checked = enough_attribs(rank_att, index, matrice)
            if checked :
                pic_list.append(index)
                #print('added')
            #else :
                #print('rejected')

    return pic_list

#attibutos = (1, 'Bald', 'Big_Nose', 'Oval_Face', 'Brow_Hair', 'Mustache')

#res = make_list(attibutos, 4)
#print(res)
