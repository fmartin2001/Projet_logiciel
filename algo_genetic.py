
import numpy as np
import copy


# Mutation function
# def mutation(encoded_img_list):
#     """
#        Args:
#            encoded_img_list
#            proba : must be between 0 and 1
#
#        Returns:
#            autoencoder, decoder, encoder compiled
#     """
#     proba=0.5
#     n, m, o, q = encoded_img_list.shape
#     encoded_img_list_copy = copy.deepcopy(encoded_img_list)
#     for i in range(n):  # for each encoded image
#         for j in range(m):
#             p = np.random.random()
#             if p < proba:
#                 for k in range(o):
#                     for l in range(q):
#                         p = np.random.random()
#
#                         if p < proba:
#                             encoded_img_list_copy[i, j, k, l] = 1 - encoded_img_list[i, j, k, l]
#     return encoded_img_list_copy
# Mutation function
def mutation(P, Tm):
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


def new_img_generator(encoded_img_selected):
    """
    1 ou 2 img arrivent normalement sous forme de liste
    """

    new_img_proposed = mutation(encoded_img_selected,0.1)
    new_img, indices = crossing_over_temp(new_img_proposed,0.6)

    res=[]
    nb_modified = 6-len(encoded_img_selected)
    for i in range (nb_modified):
        res.append(new_img[i])
    for i in range (len(encoded_img_selected)):
        res.append(encoded_img_selected[i])
    return res



# def algo_gen(encoded_img_selected) :
# selectionner des caractéristiques de départ pour réduire les données
# récupérer les img encodées correspondantes
# recupérer 4 images encodées parmi elles
#

# while cnt < 30 and nb_max_de_suite < 5:
# les afficher
# utilisateur choisit : on récupère lesquelles il choisit (1 ou 2)
# list_img_choisies.append(identifiant de l'img)
# cnt +=1
# if list_img_choisie[-1] == list_img_choisie[-2]: #si la dernière est la même que l'avant dernière
# nb_max_de_suite += 1
# new_img_generator(encoded_img_selected)


if __name__ == "__main__":
    liste_img_encoded = np.load("Data/20_encoded_img.npy")
    liste_mutations = mutation(liste_img_encoded)
    liste_crossing, indices = crossing_over(liste_img_encoded)  # c'est quoi indices ?

    new_img_generator(liste_img_encoded)
