import get_data
import keras
from tensorflow.keras.layers import Dense, Dropout, Activation
import matplotlib.pyplot as plt
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model, load_model
from sklearn.model_selection import train_test_split
import numpy as np


class Autoencoder(Model):
    def __init__(self, input_shape=(76, 60, 3)):
        super(Autoencoder, self).__init__()

        self.encoder = keras.Sequential([
            Input(shape=input_shape),
            Conv2D(32, (3, 3), activation='tanh', padding='same'),
            MaxPooling2D((2, 2), padding='same'),
            Conv2D(16, (3, 3), activation='tanh', padding='same'),
            MaxPooling2D((2, 2), padding='same', name="encoded"),
        ])
        self.decoder = keras.Sequential([
            Conv2D(16, (3, 3), activation='tanh', padding='same'),
            UpSampling2D((2, 2)),
            Conv2D(32, (3, 3), activation='tanh', padding='same'),
            UpSampling2D((2, 2)),
            Conv2D(16, (3, 3), activation='sigmoid', padding='same'),
            Conv2D(3, (3, 3), activation='sigmoid', padding='same', name="decod")
        ])
        # On compile uniquement l'auto encoder
        self.compile(optimizer='adam', loss='binary_crossentropy')

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded





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
    from PIL import Image
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
    encoded_img = autoencoder.encoder.predict(img_pixel_list)
    np.save(f"Data/{len(encoded_img)}_encoded_img", encoded_img)


if __name__ == "__main__":
     img_pixel_list = get_data.load_dataset('./img_align_celeba/img_align_celeba',1000)

     X_train, X_test = train_test_split(img_pixel_list,
                                        test_size=0.2,
                                        random_state=0)
     print("Done train test split")

     autoencoder = Autoencoder()

     print("Done autoencoder creation")

     autoencoder.fit(X_train, X_train,
                     epochs=10,
                     batch_size=50,
                     shuffle=True,
                     validation_data=(X_test, X_test))

     print("Done autoencoder training")

     autoencoder.save("./Model/autoencoder")

     print("Done model saving")
     plot_loss(autoencoder)
     plot_image_reconstruction(autoencoder, X_test)

     img_to_encode = get_data.load_dataset('./img_align_celeba/img_align_celeba',20)
     save_encoded_img(img_to_encode)

     print("Done image encoded saving")