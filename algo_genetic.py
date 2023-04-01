
import numpy as np
import copy


# Mutation function
def mutation(P, Tm):
    """
    Change de manière aléatoire avec une probabilité Tm la valeur d'un pixel
    parameters :
        P (nDarray) : liste d'images
        Tm (float) : seuil, probabilité de mutations
    return :
        P_copy (nDarray) : liste d'images mutées
    """
    n, m = P.shape
    P_copy = np.copy(P)
    compt=0
    for i in range(n):
        for j in range(m):
            p = np.random.random()
            if p < Tm:
                P_copy[i, j] = 1- P[i, j]
                compt+=1
            if compt==30:
                j=m
    return P_copy


def crossing_over_temp(P, Tc):
    """
        Croise plusieurs images
        parameters :
            P (nDarray) : liste d'images
            Tc (float) : seuil, probabilité de mutations
        return :
            new_P (nDarray) : liste d'images croisées
            liste (nDarray) : listes d'indices
        """
    new_P = np.copy(P)
    liste = []

    for i in range(0, len(new_P)):
        if np.random.random() < Tc:
            indc_im = np.random.randint(0, new_P.shape[0] - 1)
            posc_x = np.random.randint(0, new_P.shape[1] - 1)
            tmp = new_P[i, posc_x:new_P.shape[1]]
            new_P[i, posc_x:new_P.shape[1]] = new_P[indc_im, posc_x:new_P.shape[1]]
            new_P[indc_im, posc_x:new_P.shape[1]] = tmp
            liste.append(indc_im)

    return new_P, liste


def new_img_generator_debut(encoded_img_selected,taille):
    """
    1 ou 2 img arrivent normalement sous forme de liste
    parameters :
        encoded_img_selected (nDarray) : liste d'images encodées et sélectionnées
        taille (int) : taille du tableau d'images choisies à l'initiale
    return :
        res (nDarray) : liste de 6 images mélange d'images choisies, mutées et nouvelles
    """
    taille=max(taille,2)
    new_img_proposed = mutation(encoded_img_selected[0:taille],0.1)
    new_img, indices = crossing_over_temp(new_img_proposed,0.6)
    res=[]
    nb_modified = 6-len(encoded_img_selected)
    print(nb_modified)
    for i in range (nb_modified):
        res.append(new_img[i])
    for i in range (len(encoded_img_selected)):
        res.append(encoded_img_selected[i])
    return res

def new_img_generator_fin(encoded_img_selected, taille):
    """
    1 ou 2 img arrivent normalement sous forme de liste
    parameters :
        encoded_img_selected (nDarray) : liste d'images encodées et sélectionnées
        taille (int) : taille du tableau d'images choisies à l'initiale
    return :
        res (nDarray) : liste de 6 images mélange d'images choisies, mutées et nouvelles
    """
    taille = max(taille, 2)
    new_img = mutation(encoded_img_selected[0:taille],0.1)
    res=[]
    nb_modified = 6-len(encoded_img_selected)
    for i in range (nb_modified):
        res.append(new_img[i])
    for i in range (len(encoded_img_selected)):
        res.append(encoded_img_selected[i])
    return res

if __name__ == "__main__":
    # Test des fonctions du fichier
    liste_img_encoded = np.load("Data/20_encoded_img.npy")
    liste_mutations = mutation(liste_img_encoded)
    liste_crossing, indices = crossing_over(liste_img_encoded)  # c'est quoi indices ?
    new_img_generator(liste_img_encoded)
