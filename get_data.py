import os
import numpy as np
from PIL import Image
import pandas as pd


def load_dataset(path_to_data, nb_im):
    """
     Args:
        path_to_data (str): Path to the dataset
        nb_im (str): Image number you want to load.

    Returns:
        np.array: 4D np array. Each row corresponds to an image. Each cell is a pixel number
    """

    img_list = os.listdir(path_to_data)
    img_pixel_list = []

    for i in range(nb_im):
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


if __name__ == "__main__":
    nb_img_to_load = 4
    img_pixel_list = load_dataset('./img_align_celeba/img_align_celeba',nb_img_to_load)

    path = f"./img_align_celeba/img_align_celeba/{nb_img_to_load}_img_pixel_list"

    if not os.path.isfile(path):
        np.save(path, img_pixel_list)

    liste_attributs = ["Bangs", "Big_Lips", "Big_Nose"]
    # mon_df = img_id_attribute(liste_attributs)

    #df = pd.read_csv("./CelebA/Anno/list_attr_celeba.txt")
