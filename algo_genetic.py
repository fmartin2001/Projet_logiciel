
import numpy as np
import copy


# Mutation function
def mutation(encoded_img_list):
    """
       Args:
           encoded_img_list
           proba : must be between 0 and 1

       Returns:
           autoencoder, decoder, encoder compiled
    """
    proba=0.5
    n, m, o, q = encoded_img_list.shape
    encoded_img_list_copy = copy.deepcopy(encoded_img_list)
    for i in range(n):  # for each encoded image
        for j in range(m):
            p = np.random.random()
            if p < proba:
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
            tmp = new_encoded_img_list[i, posc_x:new_encoded_img_list.shape[1], posc_y:new_encoded_img_list.shape[2],
                  posc_z:new_encoded_img_list.shape[3]]
            new_encoded_img_list[i, posc_x:new_encoded_img_list.shape[1], posc_y:new_encoded_img_list.shape[2],
            posc_z:new_encoded_img_list.shape[3]] = new_encoded_img_list[indc_im,
                                                    posc_x:new_encoded_img_list.shape[1],
                                                    posc_y:new_encoded_img_list.shape[2],
                                                    posc_z:new_encoded_img_list.shape[3]]
            new_encoded_img_list[indc_im, posc_x:new_encoded_img_list.shape[1], posc_y:new_encoded_img_list.shape[2],
            posc_z:new_encoded_img_list.shape[3]] = tmp
            liste.append(indc_im)

    return new_encoded_img_list, liste


def new_img_generator(encoded_img_selected):
    """
    1 ou 2 img arrivent normalement sous forme de liste
    """

    new_img_proposed = mutation(encoded_img_selected)
    print("et1")
    new_img, indices = crossing_over(new_img_proposed)
    print("2")

    res=[]
    nb_modified = 6-len(encoded_img_selected)
    print(nb_modified)
    for i in range (nb_modified):
        res.append(new_img[i])
    for i in range (len(encoded_img_selected)):
        res.append(encoded_img_selected[i])
    return res

    # if len(encoded_img_selected) ==2:
    #     new_img_proposed = mutation(encoded_img_selected)
    #     new_img, indices = crossing_over(new_img_proposed)
    #     other_cross, ind = crossing_over(encoded_img_selected)
    #     res=[]#np.concatenate(new_img, encoded_img_selected,axis=0)
    #     for i in range (2):
    #         res.append(new_img[i])
    #     for i in range (2):
    #         res.append(encoded_img_selected[i])
    #     for i in range (2):
    #         res.append(other_cross[i])
    #     return res
    # if len(encoded_img_selected) == 1:
    #     new_img_proposed = []
    #     for i in range(4):
    #         new_img = mutation(encoded_img_selected)
    #         print("fa")
    #         new_im, indice = crossing_over(new_img)
    #         print("fi")
    #         new_img_proposed.append(new_im)
    #         print("fi")
    #     print("first")
    #     img = np.load('./Data/20_encoded_img.npy')
    #     print("first")
    #     rand=int(np.random.random()*20)
    #     print(rand)
    #     new_img_proposed.append(img[rand])
    #     print("trouvé")
    #     new_img_proposed.append(encoded_img_selected[0])
    #     new_img_proposed = np.asarray(new_img_proposed)

        # return new_img_proposed
    # else:
    #     return encoded_img_selected


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
