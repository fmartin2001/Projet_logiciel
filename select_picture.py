import numpy as np
import os
import random as rd
from PIL import Image

def check_yes(index, pic_id, val):
    """
    entrée = nom de l'attibut, numéro de l'image
    check si l'image a cette caractéristique
    Renvoie booléen
    """
    usecols = []
    for i in range(1, 41) :
        usecols.append(i)

    mat = np.loadtxt('/home/margaux/Documents/quatre_A/S2/dvp_logiciel/project/my_scripts/list_attr_celeba.txt', skiprows = 2, usecols = usecols)

    att = 0
    if mat[pic_id][index] == val :
        att = 1

    return att

def check_sex(sex, pic_id) :
    """
    Entrée : image souhaitée
    Renvoie 0 si femme 1 si homme
    """
    usecols = []
    for i in range(1, 41) :
        usecols.append(i)

    mat = np.loadtxt('/home/margaux/Documents/quatre_A/S2/dvp_logiciel/project/my_scripts/list_attr_celeba.txt', skiprows = 2, usecols = usecols)

    att = 0
    if mat[pic_id][20] == 1 :
         att = 1

    return att

def choose_yes(matrice, l_att, nb_pic, attribut) :
    """
    prend en entrée : matrice, liste d'attributs, nb d'images du datset, attribu souhaité
    donne une image random qui possède cette charactéristique
    """

    attr_matrice, attr_list = load_attr(attr_path)

    #Trouver le rang de l'attibu dans la liste
    index = 0
    for i in range(len(l_att)) :
        if l_att[i] == attribut :
            index = i

    #Trouver une image random avec cet attribut
    found = 0
    while found == 0 :
        num_pic = rd.randint(0, nb_pic)
        found = check_yes(matrice, num_pic, index)

    return num_pic

def sort_set(att, sam_size) :
    """
    Donne la liste des images correspondant au caractéristiques suivantes :
     - le sexe qui est donné par le premier attribut
     - au moins deux charactéristiques de la liste
     En entrée : liste des attributs, longueur de la liste à trier
    """

    final_sort = []
    num_attr = [1, 2, 3, 4]

    for i in range(sam_size) :
        print('--------')
        if check_sex(att[0] , i) == True :
            count = 0
            for j in range(1, len(att)) :
                if check_yes(num_attr[j], i, att[j]) == True :
                    count = count + 1
            if count >= 1 :
                final_sort.append(i)
                print(f'Added a {len(final_sort)}th pic to the list')

    return final_sort


def sort_data (attributs) :

    """
    Génère une liste de numéros d'images avec pour caractéristique le sexe, et au moins deux autres charactéristiques de la liste, parmi un certain nb d'images donné.
    Elle servira de base de données où piocher pour la suite.
    Si le nb d'images triées n'est pas suffisant dans le groupe trié, on agrandi le groupe et on retrie, jusqu'à atteindre une liste de n images.
    """
    #minumum_sample_size est la taille du dataset trié qu'on veut à la fin
    minimum_sample_size = 2
    sorted = []
    round = 0
    among_sample = 15 #subdivision du dataset qu'on va trier
    sorted = sort_set(attributs, among_sample)
    print('first round completed')

    #faire en sorte que ça s'arrete dès qu'on a minimum size atteint

    while len(sorted) < minimum_sample_size :

        among_sample = among_sample + 10
        sorted = sort_set(attributs, among_sample)
        round = round + 1
        print(f'round {round} completed')

    return sorted


attributos = [1, -1, -1, 1]
res = sort_data(attributos)
print(res)

usecols = []
for i in range(1, 41) :
    usecols.append(i)

mat = np.loadtxt('/home/margaux/Documents/quatre_A/S2/dvp_logiciel/project/my_scripts/list_attr_celeba.txt', skiprows = 2, usecols = usecols)

for i in range(len(res)):
    print('-----------')

    for j in range(1, 4) :
        print(mat[i][j])
