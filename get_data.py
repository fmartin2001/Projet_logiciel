import os
import numpy as np
from PIL import Image
import pandas as pd


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
        img = img.resize((60, 76))
        img = np.array(img)
        img_pixel_list.append(img)

    img_pixel_list = np.array(img_pixel_list)
    img_pixel_list = img_pixel_list.astype('float32') / 255.0  # il faut normaliser pour + de puissance

    return img_pixel_list


if __name__ == "__main__":
    nb_img_a_charger = 4
    img_pixel_list = charger_dataset('./img_align_celeba/img_align_celeba',nb_img_to_load)

    chemin = f"./img_align_celeba/img_align_celeba/{nb_img_a_charger}_img_pixel_list"

    if not os.path.isfile(chemin):
        np.save(chemin, img_pixel_list)