import get_data
import keras
from tensorflow.keras.layers import Dense, Dropout, Activation
import matplotlib.pyplot as plt
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model, load_model
from sklearn.model_selection import train_test_split
import numpy as np


def encodeur_decodeur():
    """
    Args:

    Returns:
        autoencoder, decoder, encoder compiled
    """

    input_shape = (76, 60, 3)  # taille des images de départ
    dropout_level = 0.1  # Dropout level, on verra si on utilise plus tard

    # Couches de l'encoder
    input_img = Input(shape=input_shape)
    x = Conv2D(64, (3, 3), activation='tanh', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)

    x = Conv2D(32, (3, 3), activation='tanh', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(16, (3, 3), activation='tanh', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)


    # Couches du décoder
    x = Conv2D(16, (3, 3), activation='tanh', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(32, (3, 3), activation='tanh', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(16, (3, 3), activation='sigmoid', padding='same')(x)
    decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    nb_decoded_layers = 6  # number of decoder layers

    # Création encoder, autoencoder
    autoencoder = Model(input_img, decoded)
    encoder = Model(input_img, encoded)

    # Récupération des couches pour le décoder
    input_encoded_img = keras.Input(shape=(encoded.shape[1:]))  # dimension de l'objet encodé
    y = autoencoder.layers[-nb_decoded_layers](input_encoded_img)

    for i in range(nb_decoded_layers - 1, 0, -1):  # 4 3 2 1
        y = autoencoder.layers[-i](y)

    # Decoder
    decoder = Model(input_encoded_img, y)

    # On compile uniquement l'auto encoder
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

    return autoencoder, encoder, decoder


def plot_loss(autoencoder):
    """
    Plot la loss de l'auto encodeur : si on a un bon modèele, val loss est proche de loss, et on veut une loss faible
    """

    history = autoencoder.history.history

    plt.plot(history['val_loss'], label="test")
    plt.plot(history['loss'], label="training")
    plt.xlabel("epochs")
    plt.ylabel("Loss")
    plt.legend()


def plot_image_reconstruction(autoencoder, X_test, n=10):
    """
    autoencoder: l'autoencoder qu'on souhaite tester
    n : combien de faces on display
    X_test : l'array des images tests"""

    decoded_imgs = autoencoder.predict(X_test)

    plt.figure(figsize=(20, 4))
    for i in range(n):
        # Display original
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(X_test[i].reshape(76, 60, 3))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Display reconstruction
        ax = plt.subplot(2, n, i + 1 + n)
        plt.imshow(decoded_imgs[i].reshape(76, 60, 3))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.show()

def save_encoded_img(img_pixel_list):
    encoded_img = encoder.predict(img_pixel_list)
    np.save(f"Data/{len(encoded_img)}_encoded_img", encoded_img)


if __name__ == "__main__":
    img_pixel_list = get_data.load_dataset('./CelebA/Img/img_align_celeba',100)

    X_train, X_test = train_test_split(img_pixel_list,
                                       test_size=0.2,
                                       random_state=0)
    print("Done train test split")

    autoencoder, encoder, decoder = encodeur_decodeur()

    print("Done autoencoder creation")

    autoencoder.fit(X_train, X_train,
                    epochs=2,
                    batch_size=50,
                    shuffle=True,
                    validation_data=(X_test, X_test))

    print("Done autoencoder training")

    encoder.save("./Model/encoder")
    decoder.save("./Model/decoder")
    autoencoder.save("./Model/autoencoder")

    print("Done model saving")

    plot_loss(autoencoder)
    plot_image_reconstruction(autoencoder, X_test)

    img_to_encode = get_data.load_dataset('./CelebA/Img/img_align_celeba',20)
    save_encoded_img(img_to_encode)