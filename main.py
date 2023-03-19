import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QIcon
from PyQt5.QtWidgets import QLabel, QApplication, QLineEdit, QWidget, QMessageBox, QFormLayout, QPushButton, \
    QGridLayout, QComboBox
from PyQt5.QtWidgets import QTextEdit, QMainWindow, QVBoxLayout
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import numpy as np
import algo_gen as algo
import get_data as get
from PIL import Image
import matplotlib.image as mat_im
from tensorflow.keras.models import load_model

# variables globales : compteur pour l'algo gen et les images choisies
cnt = 1
img_recurrente = []
autoencoder = load_model("./Model/autoencoder")


class customButton(QPushButton):
    """Redefinie le widget QPushButton
        ajoute les attributs suivants :
        le texte 'sélectionner' ou 'désélectionner'
        selected -- boolean qui indique si le bouton est sélectionner (= on a cliqué un nombre impair de fois dessus)

        redefinition de l'evenement mouseRelease :
        change les deux attributs
        """

    # bouton personnaliser pour selectionner et deselectionner les visages
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setText("Choisir")
        self.setFixedSize(30, 30)
        self.setStyleSheet("background-color: #D3D3D3")
        self.setCheckable(True)
        self.clicked.connect(self.on_click)

    def on_click(self):
        if self.isChecked():
            #self.setText("Choisi")
            check = QIcon('check.png')
            self.setIcon(check)
            self.setStyleSheet("background-color: #008000")
        else:
            # self.setText("Choisir")
            self.setIcon(QIcon())
            self.setStyleSheet("background-color: white")


class FEN0(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Projet')
        # Créer les widgets pour l'interface graphique
        self.label = QLabel("Bienvenue dans un générateur de portrait robot ! Nous vous prions de répondre le plus honnêtement possible afin de faire un protrait robot de votre agresseur le plus représentatif possible")
        self.image_label = QLabel()
        self.image_pixmap = QPixmap("logo.jpg")
        self.image_label.setPixmap(self.image_pixmap.scaledToWidth(400))
        button = QPushButton("Démarrer", self)
        self.nextfen = FEN1()
        button.clicked.connect(self.nextwindow2)

        # Créer un layout vertical pour contenir les widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.move(80, 80)  # position de la fenetre
        self.setWindowIcon(QIcon('logo.jpg'))

    def nextwindow2(self):
        self.nextfen.show()
        self.close()


class FEN1(QWidget):
    """Création de la fenetre 1
            Cette fenetre sert à rentrer et sauvegarder les informations de l'utilisateur
            Elle contient trois champs à remplir
            Si un champs est vide au moment de la validation, un message d'erreur apparait
            """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nextfen = FEN2()  # sa fenetre suivante est la fenetre 2

        # permet de rentrer le nom
        self.e1 = QLineEdit()  #
        self.e1.setMaxLength(20)
        self.e1.setAlignment(Qt.AlignRight)
        self.e1.setFont(QFont("Helvetica", 10))

        # permet de rentrer le prenom
        self.e2 = QLineEdit()
        self.e2.setMaxLength(20)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont(QFont("Helevetica", 10))

        # permet de rentrer la date de naissance
        self.e3 = QLineEdit()
        self.e3.setValidator(QIntValidator())
        self.e3.setInputMask("99/99/9999")

        # bouton "soumettre" pour passer à la fenetre suivante et sauvegarder les données entrées
        self.btn = QPushButton()
        self.btn.setText("Soumettre")

        # Grille de mise en page
        flo = QFormLayout()
        flo.addRow("Nom", self.e1)
        flo.addRow("Prénom", self.e2)
        flo.addRow("Date de naissance", self.e3)
        flo.addWidget(self.btn)

        self.resize(500, 220)  # taille de la fenetre
        self.move(100, 100)  # position de la fenetre
        self.setLayout(flo)  # affichage de la grille
        self.setWindowTitle("Coordonnees utilisateur")
        self.setWindowIcon(QIcon('logo.jpg'))

        # rattachement du bouton "soumettre à l'évenement "changer de fenetre" (apres avoir vérifier si les champs n'étaient pas vides)
        self.btn.clicked.connect(self.rempli)

    def rempli(self):
        """renvoie vers la fonction nextwindow ou un message d'erreur
            prend seulement les attributs en paramètres

        """
        if (self.e1.text() != "" and self.e2.text() != "" and self.e3.text() != "//"):
            self.nextwindow()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez remplir tous les champs")
            msg.exec_()

    def nextwindow(self):
        """enregistre les infos (nom, prenom, date) dans un fichier
        ferme la fenetre 1 puis ouvre la fenetre 2

        """
        fichier = open("user.txt", "a")
        fichier.write(self.e1.text())
        fichier.write("\n")
        fichier.write(self.e2.text())
        fichier.write("\n")
        fichier.write(self.e3.text())
        fichier.write("\n")
        fichier.close()

        # changement de fenetre
        self.nextfen.show()
        self.close() #or close


class FEN2(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Caracteristiques')
        self.setGeometry(320, 320, 320, 320)

        # Labels
        label1 = QLabel('Avait-il/elle un gros nez?:', self)
        # label1.move(20, 20)
        label2 = QLabel('Couleur des cheveux:', self)
        # label2.move(20, 60)
        label3 = QLabel('Sexe:', self)
        # label3.move(20, 100)
        label4 = QLabel('Avait-il/elle des lunettes ?', self)
        # label4.move(20, 140)

        # Combo boxes
        nose = ['Oui', 'Non']
        hair_colors = ['Brun', 'Gris', 'Blond', 'Noir']
        sex = ['Homme', 'Femme', 'Je ne sais pas']
        lunettes = ['Oui', 'Non']
        self.nose = QComboBox(self)
        self.nose.addItems(nose)
        # self.eye_combo.move(140, 20)
        self.hair_combo = QComboBox(self)
        self.hair_combo.addItems(hair_colors)
        # self.hair_combo.move(140, 60)
        self.sex_combo = QComboBox(self)
        self.sex_combo.addItems(sex)
        # self.sex_combo.move(140, 100)
        self.lunettes = QComboBox(self)
        self.lunettes.addItems(lunettes)
        # self.skin_combo.move(140, 140)

        # Button
        button = QPushButton('Soumettre', self)
        # button.move(100, 180)
        button.clicked.connect(self.nextwindow2)

        # Bouton pour retourner en arrière sur la fenêtre des coordonnées utilisateur
        self.bouton_retour = QPushButton('Retour')
        self.bouton_retour.clicked.connect(self.backwindow)

        layout = QGridLayout()
        # Qt.AlignVCenter
        layout.addWidget(label1, 4, 1)
        layout.addWidget(label2, 2, 1)
        layout.addWidget(label3, 3, 1)
        layout.addWidget(label4, 1, 1)
        layout.addWidget(self.nose, 1, 2)
        layout.addWidget(self.hair_combo, 2, 2)
        layout.addWidget(self.sex_combo, 3, 2)
        layout.addWidget(self.lunettes, 4, 2)
        layout.addWidget(button, 5, 2)
        layout.addWidget(self.bouton_retour, 6, 2)
        self.setLayout(layout)

    def submit(self):
        nose = self.nose.currentText()
        hair_color = self.hair_combo.currentText()
        sex = self.sex_combo.currentText()
        lunettes = self.lunettes.currentText()
        print(f'Taille du nez : {nose}, Couleur des cheveux : {hair_color}, Sexe : {sex}, Avait-il des lunettes ? : {lunettes}')


    def nextwindow2(self):
        img = np.load('./Data/20_encoded_img.npy')
        self.nextfen = FEN3(img)
        self.nextfen.show()
        self.close()

    def backwindow(self):
        self.close()
        first_window = FEN1() #ça marche pas
        first_window.show()
        print("je passe par back window")



class FEN3(QWidget):
    """Creation de la fenetre 3
    composée de 4 images
    4 boutons de sélection
    1 label explicatif
    2 boutons pour valider et terminer ou valider et continuer la recherche
    """

    def __init__(self, img):
        super().__init__()
        self.img_encod = img
        self.initUI()

    def initUI(self):

        self.gen_premieres_img()

        # Une à une on prend les image et on les place dans un label
        self.img1 = QPixmap('img1.png')
        self.label1 = QLabel()
        self.label1.setPixmap(self.img1)
        self.img2 = QPixmap('img2.png')
        self.label2 = QLabel()
        self.label2.setPixmap(self.img2)
        self.img3 = QPixmap('img3.png')
        self.label3 = QLabel()
        self.label3.setPixmap(self.img3)
        self.img4 = QPixmap('img4.png')
        self.label4 = QLabel()
        self.label4.setPixmap(self.img4)
        self.img5 = QPixmap('img5.png')
        self.label5 = QLabel()
        self.label5.setPixmap(self.img5)
        self.img6 = QPixmap('img6.png')
        self.label6 = QLabel()
        self.label6.setPixmap(self.img6)

        # Ajout des deux boutons de validations
        self.bt1 = QPushButton("Continuer la recherche")
        self.bt1.setFixedSize(200, 30)
        self.bt2 = QPushButton("Soumettre le visage final")
        self.bt2.setFixedSize(200, 30)

        # Création de grille pour la mise en page
        self.fen = QGridLayout()
        # Qt.AlignVCenter

        # Creation des boutons de selection des images
        self.btn_selection1 = customButton()
        self.btn_selection2 = customButton()
        self.btn_selection3 = customButton()
        self.btn_selection4 = customButton()
        self.btn_selection5 = customButton()
        self.btn_selection6 = customButton()

        # Placement des widgets dans la grille
        self.fen.addWidget(self.label1, 1, 1, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.btn_selection1, 2, 1, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.label2, 1, 2, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.btn_selection2, 2, 2, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.label3, 1, 3, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.btn_selection3, 2, 3, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.label4, 3, 1, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.btn_selection4, 4, 1, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.label5, 3, 2, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.btn_selection5, 4, 2, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.label6, 3, 3, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.btn_selection6, 4, 3, alignment=Qt.AlignCenter)

        self.fen.addWidget(QLabel("Sélectionnez le ou les deux visages qui ressemble(nt) le plus à votre agresseur"), 6,
                           2, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.bt1, 6, 3, alignment=Qt.AlignRight)
        self.fen.addWidget(self.bt2, 6, 1, alignment=Qt.AlignLeft)

        # Attribution au boutons de validation les evenements correspondants
        self.bt1.clicked.connect(self.selection1vs5)
        self.bt2.clicked.connect(self.selection1_final)

        self.resize(900, 600)  # taille
        self.move(100, 100)  # position
        self.setLayout(self.fen)
        self.setWindowTitle("choix du portrait")
        self.setWindowIcon(QIcon('logo.jpg'))

    def gen_premieres_img(self):
        # img_encoded_list = np.load('./Data/20_encoded_img.npy')

        global autoencoder
        img_list = autoencoder.decoder.predict(self.img_encod)

        mat_im.imsave("img1.png", img_list[0])
        mat_im.imsave("img2.png", img_list[1])
        mat_im.imsave("img3.png", img_list[2])
        mat_im.imsave("img4.png", img_list[3])
        mat_im.imsave("img5.png", img_list[4])
        mat_im.imsave("img6.png", img_list[5])

    def nextimg(self):
        global cnt
        global img_recurrente

        list = [self.btn_selection1, self.btn_selection2, self.btn_selection3, self.btn_selection4, self.btn_selection5,
                self.btn_selection6]
        # img_choisie = []
        # for i in range(len(list)):
        #     if list[i].isChecked():
        #         img_choisie.append(self.img_encod[i])
        #
        # for i in range(len(img_choisie)):
        #     if np.array_equal(img_recurrente[0], img_choisie[i]) or len(img_recurrente) == 0:
        #         img_recurrente.append(img_choisie[i])
        #
        if cnt < 10 and len(img_recurrente) < 5:
            cnt = cnt + 1
            self.algo_gen()
        elif len(img_recurrente) >= 5:
            self.nextwindow(img_recurrente[4])
        else :
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Il est temps de faire un choix, veuillez sélectionner 1 visage et cliquer sur valider")
            msg.exec_()

    def algo_gen(self):
        """Algo genetique
        Reste sur la meme fenetre en changeant les images
        Envoie sous forme de liste les images selectionnees par l'utilisateur à l'algorithme genetique
        Actualise img1.jpg, img2.jpg, img3.jpg, img4.jpg
        Relance la fenetre
        """
        list = [self.btn_selection1, self.btn_selection2, self.btn_selection3, self.btn_selection4, self.btn_selection5,
                self.btn_selection6]
        img_choisie = []
        # on prend celles qui ont le cout le plus faible soit celles choisies
        for i in range(len(list)):

            if list[i].isChecked():
                img_choisie.append(self.img_encod[i])
                print("ça passe par là")
        img_choisie = np.asarray(img_choisie)
        #   procede aux mutations et crossing over
        new_img = algo.new_img_generator(img_choisie)
        new_img = np.asarray(new_img)
        print("hey")
        #   ouverture de la nouvelle fenetre == nouveau calcul du cout
        self.newfen = FEN3(new_img)
        self.newfen.show()

        #   fermeture de l'ancienne
        self.close()

    def selection1vs5(self):
        """Verification du nombre d'images selectionnees
        Il doit etre egal entre 1 et 5 inclu
        Si nombre reglementaire, renvoie à la fonction nextimg
        Sinon affiche un message d'erreur
        """
        list = [self.btn_selection1, self.btn_selection2, self.btn_selection3, self.btn_selection4, self.btn_selection5,
                self.btn_selection6]
        cnt = 0
        for btn in list:
            if btn.isChecked():
                cnt = cnt + 1
        if cnt != 0 and cnt != 6:
            self.nextimg()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez sélectionner au moins un visage et au plus cinq")
            msg.exec_()

    def selection1_final(self):
        """Verification du nombre d'images selectionnees
        Il doit etre egal à 1 pour valider
        Si nombre reglementaire, renvoie à la fonction nextwindow
        Sinon affiche un message d'erreur
        """
        list = [self.btn_selection1, self.btn_selection2, self.btn_selection3, self.btn_selection4, self.btn_selection5,
                self.btn_selection6]
        list = np.array(list)
        cnt = 0
        btn_selected = 0
        for btn in list:
            if btn.isChecked():
                cnt = cnt + 1
                btn_selected = int(np.where(list == btn)[0] + 1)  # quel numéro d'image c'était ?
                name = "img" + str(btn_selected)
                img_selected = getattr(self, name)  # image correspondant a la photo choisie

        if cnt == 1:
            self.nextwindow(img_selected)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez sélectionner un seul visage pour valider")
            msg.exec_()

    def nextwindow(self, img):
        """Renvoie sur la fenetre suivante
        Sauvegarde le choix final
        """
        # msg = QMessageBox(main_window)
        # msg.setWindowTitle("Etes vous sur(e) de votre choix?")
        # msg.setText("Souhaitez vous valider votre choix?")
        # msg.exec_()

        self.fen = FEN4(img)  # prend en paramètres l'image choisie
        self.fen.show()
        self.close()


class FEN4(QMainWindow):
    def __init__(self, image):
        super().__init__()

        # Créer les widgets pour l'interface graphique
        self.label = QLabel("Vous confirmez que ce portrait robot correspond le mieux à votre agresseur :")
        self.image_label = QLabel()
        self.image_pixmap = image
        self.image_label.setPixmap(self.image_pixmap.scaledToWidth(400))
        self.label2 = QLabel("Merci de réindiquer votre nom et prénom afin de vérifier votre identité.")
        self.text_edit = QTextEdit()
        self.button = QPushButton("Sauvegarder")

        # Créer un layout vertical pour contenir les widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label2, alignment=Qt.AlignCenter)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # Créer un widget pour contenir le layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Recapitulatif de la requete")
        self.setWindowIcon(QIcon('logo.jpg'))

        # Associer un signal à l'événement "clicked" du bouton
        self.button.clicked.connect(self.save_to_pdf)

    def save_to_pdf(self):
        # Obtenir le contenu du QTextEdit
        text = self.text_edit.toPlainText()

        # Créer un objet canvas pour générer le PDF
        c = canvas.Canvas("mon_document.pdf", pagesize=letter)

        # Dessiner le titre
        c.setFontSize(20)
        c.drawString(1 * inch, 10 * inch, "Fiche récapitulative")

        # Convertit l'image QPixmap en PIL Image
        qimage = self.image_pixmap.toImage()
        # Sauvegarde de l'image dans le directory
        qimage.save("./img_choisie.png", "PNG", -1)
        # Dessiner l'image
        c.drawInlineImage("img1.jpg", 80, 250, height=270, width=480)

        # Dessiner le texte
        c.setFontSize(12)
        textobject = c.beginText(1 * inch, 7.5 * inch)
        for line in text.split('\n'):
            textobject.textLine(line)
        c.drawText(textobject)

        # Sauter une page
        c.showPage()

        # Titre de la seconde page
        c.setFontSize(20)
        c.drawString(1 * inch, 10 * inch, "Portrait robot de l'agresseur")

        # Dessine l'image dans le pdf
        c.drawInlineImage("./img_choisie.png", 80, 250, height=270, width=480)
        # Enregistrer le PDF et fermer le canvas
        c.save()

        # Supprime l'image du directory
        os.remove("./img_choisie.png")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # win = FEN1()
    # ndow = FEN3()
    # win.show()
    # window.show()
    # liste_img_encoded = np.load("Data/20_encoded_img.npy")
    main_window = FEN2()
    main_window.show()
    sys.exit(app.exec_())
