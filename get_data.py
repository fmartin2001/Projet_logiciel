import os
import numpy as np
from PIL import Image
import pandas as pd
import select_rand_pic


def load_dataset(path_to_data, num_list):
    """
     Args:
        path_to_data (str): Path to the dataset
        nb_im (str): Image number you want to load.

    Returns:
        np.array: 4D np array. Each row corresponds to an image. Each cell is a pixel number
    """

    img_list = os.listdir(path_to_data)
    img_pixel_list = []

    for i in range(len(num_list)) :
        img = Image.open(f'{path_to_data}/{img_list[i]}')
        img = img.resize((60, 76))
        img = np.array(img)
        img_pixel_list.append(img)

    img_pixel_list = np.array(img_pixel_list)
    img_pixel_list = img_pixel_list.astype('float32') / 255.0  # il faut normaliser pour + de puissance

    return img_pixel_list


# def img_id_attribute(attribute_list):
#     df = pd.read_csv("./CelebA/Anno/list_attr_celeba.txt")
#
#     for attr in attribute_list:
#         df = df.loc[df[attr] == 1]
#
#     return df

def give_list (lattributs, nb, path) :

    list_num = select_rand_pic.make_list(lattributs, nb)
    final_list = load_dataset(path, list_num)
    return final_list


if __name__ == "__main__":
    nb_img_to_load = 10000
    path = '/home/margaux/Documents/quatre_A/S2/dvp_logiciel/project/img_dataset'
    #img_pixel_list = load_dataset('./img_align_celeba/img_align_celeba',nb_img_to_load)

    attributos = (1, 'Bald', 'Big_Nose', 'Oval_Face', 'Brow_Hair', 'Mustache')
    listette = give_list(attributos, nb_img_to_load, path)
    print(len(listette))

    #path = f"./img_align_celeba/img_align_celeba/{nb_img_to_load}_img_pixel_list"

    #if not os.path.isfile(path):
        #np.save(path, img_pixel_list)

    #liste_attributs = ["Bangs", "Big_Lips", "Big_Nose"]
    # mon_df = img_id_attribute(liste_attributs)

    #df = pd.read_csv("./CelebA/Anno/list_attr_celeba.txt")

#attributos = (1, 'Bald', 'Big_Nose', 'Oval_Face', 'Brow_Hair', 'Mustache')
#print(give_list(attributos, 100))
