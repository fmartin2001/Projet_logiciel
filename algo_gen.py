import numpy as np


# Mutation function
def mutation(encoded_img_list, proba=0.5):
    """
       Args:
           encoded_img_list
           proba : must be between 0 and 1

       Returns:
           autoencoder, decoder, encoder compiled
       """
    n, m, o, q = encoded_img_list.shape
    encoded_img_list_copy = np.copy(encoded_img_list)
    for i in range(n):  # for each encoded image
        for j in range(m):
            for k in range(o):
                for l in range(q):
                    p = np.random.random()
                    if p < proba:
                        encoded_img_list_copy[i, j, k, l] = 1 - encoded_img_list[i, j, k, l]
    return encoded_img_list_copy


def crossing_over(encoded_img_list, proba=0.5):
    new_encoded_img_list = np.copy(encoded_img_list)
    liste = []

    for i in range(0, len(new_encoded_img_list)):
        if np.random.random() < proba:
            indc_im = np.random.randint(0, new_encoded_img_list.shape[0] - 1)
            posc_x = np.random.randint(0, new_encoded_img_list.shape[1] - 1)
            posc_y = np.random.randint(0, new_encoded_img_list.shape[2] - 1)
            posc_z = np.random.randint(0, new_encoded_img_list.shape[3] - 1)
            tmp = new_encoded_img_list[i, posc_x:new_encoded_img_list.shape[1], posc_y:new_encoded_img_list.shape[2], posc_z:new_encoded_img_list.shape[3]]
            new_encoded_img_list[i, posc_x:new_encoded_img_list.shape[1], posc_y:new_encoded_img_list.shape[2], posc_z:new_encoded_img_list.shape[3]] = new_encoded_img_list[indc_im,
                                                                                            posc_x:new_encoded_img_list.shape[1],
                                                                                            posc_y:new_encoded_img_list.shape[2],
                                                                                            posc_z:new_encoded_img_list.shape[3]]
            new_encoded_img_list[indc_im, posc_x:new_encoded_img_list.shape[1], posc_y:new_encoded_img_list.shape[2], posc_z:new_encoded_img_list.shape[3]] = tmp
            liste.append(indc_im)

    return new_encoded_img_list, liste

def new_img_generator(encoded_img_selected):
    """
    1 ou 2 img arrivent normalement sous forme de liste
    """

    if len(encoded_img_selected) == 2 :
        new_img_proposed = mutation(encoded_img_selected)
        new_img_proposed = crossing_over(new_img_proposed)
        return np.concatenate(new_img_proposed,encoded_img_selected)

    if len(encoded_img_selected) == 1 :
        new_img_proposed = []
        for i in range (3):
            new_img_proposed.append(crossing_over(mutation(encoded_img_selected)))

        new_img_proposed.append(encoded_img_selected[0])
        new_img_proposed = np.array(new_img_proposed)

        return new_img_proposed
    else :
        print("Np array should be of length 1 or 2")

#def algo_gen() :
    # selectionner des caractéristiques de départ pour réduire les données
    # récupérer les img encodées correspondantes
    # recupérer 4 images encodées parmi elles

    # while compteur < 30 et nb_max_de_suite < 5
        # les afficher
        # utilisateur choisit : on récupère lesquelles il choisit (1 ou 2)
        # list_img_choisies.append(identifiant de l'img)
        # compteur +=1
        # if list_img_choisie[-1] == list_img_choisie[-2]: si la dernière est la même que l'avant dernière
        # nb_max_de_suite += 1
        # on appelle new_img_generator


if __name__ == "__main__":
    liste_img_encoded = np.load("Data/20_encoded_img.npy")
    liste_mutations = mutation(liste_img_encoded)
    liste_crossing, indices = crossing_over(liste_img_encoded) #c'est quoi indices ?

    new_img_generator(liste_img_encoded)