import os
import numpy as np
from PIL import Image
import pandas as pd
from tensorflow.keras.models import load_model

def charger_dataset(chemin_vers_data, nb_im):
    """
    Arguments:
        chemin_vers_data (str): Chemin vers le dataset
        nb_im (str): Nombre d'images à charger

    Return:
        img_pixel_list (np.array): 4D np array. Chaque ligne correspond à une image. Chaque case est un nombre de pixels.
    """

    img_list = os.listdir(chemin_vers_data)
    img_pixel_list = []

    for i in range(nb_im):
        img = Image.open(f'{chemin_vers_data}/{img_list[i]}')
        img = img.resize((128, 128))
        img = np.array(img)
        img_pixel_list.append(img)

    img_pixel_list = np.array(img_pixel_list)
    img_pixel_list = img_pixel_list.astype('float32') / 255.0  # il faut normaliser pour + de puissance

    return img_pixel_list


def create_dict(nose, hair_color, sex, lunettes, pilo):
    """
        Crée un dictionnaire en fonction des réponses de l'utilisateur (utilisé pour filtrer)
    Arguments : 
        Nose, hair_color, sex, lunettes, pilo (str) : résultats des choix initiaux de l'utilisateur concernant ces caractéristiques
    Return : 
        dic_sex (dict) : associe les caractéristiques avec un chiffre, 1 si la caractéristiques est présnte, -1 sinon
    """
    dic = {}
    if nose == "Oui":
        dic["Gros nez"] = 1
    elif nose == "Non":
        dic["Gros nez"] = -1

    if hair_color == "Brun":
        dic["Brun"] = 1
    elif hair_color == "Blond":
        dic["Blond"] = 1
    elif hair_color == "Noir":
        dic["Noir"] = 1
    elif hair_color == "Gris":
        dic["Gris"] = 1
    elif hair_color == "Chauve":
        dic["Chauve"] = 1

    if sex == "Homme":
        dic["Sexe"] = 1
    elif sex == "Femme":
        dic["Sexe"] = -1

    if lunettes == "Oui":
        dic["Lunettes"] = 1
    elif lunettes == "Non":
        dic["Lunettes"] = -1

    if pilo == "Barbe":
        dic["Barbe"] = 1
    elif pilo == "Moustache":
        dic["Moustache"] = 1
    elif pilo == "Ni barbe,ni moustache":
        dic["Ni_barbe_moustache"] = 1

    return dic


def create_sex_dict(sex):
    """
        Crée un dictionnaire selon le sexe pour filtrer ensuite
    Arguments : 
        sex (str) : sexe à partir duquel on veut obtenir le dictionnaire de sortie
    Return : 
        dic_sex (dict) : dictionnaire qui associe le string du sexe à la valeur -1 si c'est une femme ou 1 si c'est un homme
    """

    dic_sex = {}
    if sex == "Femme":
        dic_sex["Sexe"] = -1
    elif sex == "Homme":
        dic_sex["Sexe"] = 1

    return dic_sex
def save_encoded_img(img_pixel_list):
    """
        Enregistre les images encodées
    Parameters : 
        img_pixel_list (numpy.array) : images à enregistrer
    Return :
        Aucun
    """
    encoder=load_model("./model/Model/encoder_smallset_1024_100_8864")
    encoded_img = encoder.predict(img_pixel_list)
    np.save(f"Data/{len(encoded_img)}_encoded_img", encoded_img)
    
def filtre(dictionnaire, matrice):
    """
    Parameters:
        dictionnaire (dict): dictionnaire avec en clé l'attribut choisi et en valeur -1 ou 1
        matrice (numpy.ndarray) : matrice numpy des caractéristiques du jeu de données
    Return:
        return (list): liste des indexes des images correspondants aux critères choisis
    """

    index_img = []
    nb_caracteristic = []

    for key, value in dictionnaire.items():
        if key == "Sexe":
            nb_caracteristic.append((20, value))  # -1 pour une femme
        if key == "Gros nez":
            nb_caracteristic.append((7, value))
        if key == "Lunettes":
            nb_caracteristic.append((15, value))
        if key == "Moustache":
            nb_caracteristic.append((22, value))
        if key == "Barbe":
            nb_caracteristic.append((16, value))
        if key == "Ni_barbe_moustache":
            nb_caracteristic.append((24, value))
        if key == "Brun":
            nb_caracteristic.append((11, value))
        if key == "Blond":
            nb_caracteristic.append((9, value))  # on append un tuple avec le numéro de la colonne et la valeur
        if key == "Gris":
            nb_caracteristic.append((17, value))
        if key == "Noir":
            nb_caracteristic.append((8, value))
        if key == "Chauve":
            nb_caracteristic.append((4, value))

    for i in range(len(matrice)):
        count = 0
        for element in nb_caracteristic:
            if matrice[i][element[0]] == element[1]:
                count += 1

        if count == len(nb_caracteristic):
            index_img.append(i)
    return index_img


def data_img_filtrees(filtre, filtre_sex, nb):
    """
        On prend les img filtrées. S'il n'y en a pas assez, on complete avec des images random du meme sexe jusqu'a avoir nb images dans la liste
    Arguments : 
       filtre (numpy.array) : liste des images filtrées pour le moment, avec les critères de base
       filtre_sex (nympy.array) : liste d'images triées seulement selon le sexe
       nb (str) : nombre d'imges à atteindre
    Return : 
        list_img_filtre[0:nb] (numpy.array) : liste du bon nombre d'images
    """
    list_img_filtre = filtre.copy()
    if len(filtre) < nb:
        for i in range(nb - len(filtre)):
            list_img_filtre.append(np.random.choice(filtre_sex))

    return list_img_filtre[0:nb]

if __name__ == "__main__":

    nb_img_a_charger = 1000
    img_pixel_list = charger_dataset('./CelebA/img_align_celeba',nb_img_a_charger)

    # Sauvegarder les images en numpy
    #chemin = f"./Data/{nb_img_a_charger}_img_pixel_list"
    #if not os.path.isfile(chemin):
    #     np.save(chemin, img_pixel_list)

    # Sauvegarder les images encodées
    save_encoded_img(img_pixel_list)
    """


    # Charger le document contenant le fichier d'attributs
    nb_lignes = 1000 #le nombre d'images maximal à prendre en compte
    usecols = [i for i in range(1, 41)]
    mat = np.loadtxt('./Data/list_attr_celeba.txt', skiprows=1, max_rows=nb_lignes, usecols=usecols)

    #Créer une liste filtrée en fonction des caractéristiques
    liste_filtree = filtre(create_dict("Non", "Blond", "Homme", "Oui", "Barbe"), mat)
    #Créer une liste filtrée en fonction du sexe choisi
    liste_sex = filtre(create_sex_dict("Homme"), mat)

    #Renvoie une liste des indices des images à prendre dans la liste d'images encodées
    liste_img_filtre = data_img_filtrees(liste_filtree, liste_sex, 100)
    print(liste_img_filtre)"""
