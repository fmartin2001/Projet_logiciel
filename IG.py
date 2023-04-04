import sys
import os
from typing import Union, Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIntValidator, QFont, QIcon
from PyQt5.QtWidgets import QLabel, QApplication, QLineEdit, QWidget, QMessageBox, QFormLayout, QPushButton, \
    QGridLayout, QComboBox
from PyQt5.QtWidgets import QTextEdit, QMainWindow, QVBoxLayout
from numpy import ndarray
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import numpy as np
import algo_genetic as algo
import get_data as get
from PIL import Image
import matplotlib.image as mat_im
from tensorflow.keras.models import load_model
from datetime import datetime

# variables globales : compteur pour l'algo gen et les images choisies
cnt = 1

decoder = load_model("./Model/decoder_smallset_512_100_8864/",compile=False)  # decoder
banque_img = np.load('./Data/50000_encoded_img.npy')  # Banque d'image encodées
banque_filtre = []  # Images encodées correspondant aux caracteristiques choisie en fen2
index_derniere_img_utilisee = 6  # Pour ne pas rechoisir les mêmes images plusieurs fois


class customButton(QPushButton):
    """
        Redéfinie le widget QPushButton pour sélectionner des visages
    Attributes:
        Aucun attribut en plus mais définition d'une taille fixe et d'une couleur de fond

    Methods :
         on_click(self) : Redefinition de l'évênement clic qui change la couleur et le logo du bouton
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setText("Choisir")
        self.setFixedSize(30, 30)
        self.setStyleSheet("background-color: #D3D3D3")
        self.setCheckable(True)
        self.clicked.connect(self.on_click)

    def on_click(self):
        if self.isChecked():
            # self.setText("Choisi")
            check = QIcon('check.png')
            self.setIcon(check)
            self.setStyleSheet("background-color: #008000")
        else:
            # self.setText("Choisir")
            self.setIcon(QIcon())
            self.setStyleSheet("background-color: white")


class FEN0(QWidget):
    """
        Fenêtre de présentation du logiciel
    Attributes:
        Label (QLabel) : Phrase d'introduction
        image_label (QLabel) : Le logo du logiciel
        nextfen (QWidget) : La fenêtre suivante
     """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Portrait robot')
        # Créer les widgets pour l'interface graphique
        self.label = QLabel(
            "Bienvenue dans un générateur de portrait robot ! \nNous vous prions de répondre le plus honnêtement possible afin de faire un portrait robot \nde votre agresseur des plus representatifs. \nLors du choix des visages, nous vous conseillons également de choisir le minimum de propositions. \nVeuillez appuyer sur démarrer quand vous serez prêt.")
        self.image_label = QLabel()
        self.image_pixmap = QPixmap("logo.png")
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
        self.setWindowIcon(QIcon('logo.png'))

    def nextwindow2(self):
        """
        Ferme la fenêtre et ouvre la suivante
        """
        self.nextfen.show()
        self.close()


class FEN1(QWidget):
    """
        Fenêtre pour rentrer et sauvegarder les informations de l'utilisateur.
        Elle contient trois champs à remplir.
        Si un champ est vide au moment de la validation, un message d'erreur apparait
    Attributes:
        e1 (QLineEdit) : champs pour rentrer le nom
        e2 (QLineEdit) : champs pour rentrer le prénom
        e3 (QLineEdit) : champs pour rentrer la date de naissance
        btn (QPushButton) : bouton "soumettre" pour passer à la fenêtre suivante
        nextfen (QWidget) : la fenêtre suivante
    Warning:
        Pour la date de naissance il est nécessaire de placer le curseur à gauche du champ et seuls les chiffres sont supportés.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.e1 = QLineEdit()
        self.e2 = QLineEdit()
        self.e3 = QLineEdit()
        self.btn = QPushButton()
        self.initUI()

    def initUI(self):
        """
        Place les widgets dans la fenêtre.
        """

        # permet de rentrer le nom
        self.e1.setMaxLength(20)
        self.e1.setAlignment(Qt.AlignRight)
        self.e1.setFont(QFont("Helvetica", 10))

        # permet de rentrer le prénom
        self.e2.setMaxLength(20)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont(QFont("Helevetica", 10))

        # permet de rentrer la date de naissance
        self.e3.setValidator(QIntValidator())
        self.e3.setInputMask("99/99/9999")

        self.nextfen = FEN2(self.e1, self.e2, self.e3)  # sa fenetre suivante est la fenetre 2

        # bouton "soumettre" pour passer à la fenêtre suivante et sauvegarder les données entrées
        self.btn.setText("Soumettre")

        # Grille de mise en page
        flo = QFormLayout()
        flo.addRow("Nom", self.e1)
        flo.addRow("Prénom", self.e2)
        flo.addRow("Date de naissance", self.e3)
        flo.addWidget(self.btn)

        self.resize(500, 220)  # taille de la fenêtre
        self.move(100, 100)  # position de la fenêtre
        self.setLayout(flo)  # affichage de la grille
        self.setWindowTitle("Coordonnées utilisateur")
        self.setWindowIcon(QIcon('logo.png'))

        # rattachement du bouton "soumettre à l'évenement "changer de fenêtre" (après avoir vérifié si les champs n'étaient pas vides)
        self.btn.clicked.connect(self.rempli)

    def rempli(self):
        """
        Renvoie vers la fonction nextwindow() si tout est renseigné.
        Renvoie un message d'erreur si un des champs est vide.
        """
        if (self.e1.text() != "" and self.e2.text() != "" and self.e3.text() != "//"):
            self.nextwindow()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez remplir tous les champs")
            msg.exec_()

    def nextwindow(self):
        """
        Ferme la fenêtre 1 puis ouvre la fenêtre 2 (la suivante).
        """
        # changement de fenetre
        self.nextfen.show()
        self.close()  # or close


class FEN2(QWidget):
    """
            Fenêtre pour rentrer les caractéristiques de l'agresseur.
        Attributes:
            label1 (QLabel) : "Sexe"
            label2 (QLabel) : "Couleur des cheveux"
            label3 (QLabel) : "Pilosité faciale"
            label4 (QLabel) : "Avait-il/elle des lunettes?"
            label5 (QLabel) : "Avait-il/elle un gros nez?"
            Combo boxes (nose,hair_combo,sexe_combo,lunettes) : Respectivement les choix pour chaque label
            bouton_retour (QPushButton) : Bouton "retour" pour revenir à la fenêtre précédente
            nextfen (QWidget) : La fenêtre suivante
            firstwindow (QWidget) : La fenêtre précédente
        Methods:
             nextwindow2(self) : Passe à la fenêtre suivante (nextfen)
             backwindow(self) : Revient à la fenêtre précédente
             submit(self) : Sauvegarde les caractéristiques choisies par l'utilisateur
        """

    def __init__(self, nom, prenom, date, parent=None):
        super().__init__(parent)
        self.nom = nom
        self.prenom = prenom
        self.date = date
        self.initUI()

    def initUI(self):
        """
        Place les widgets dans la fenêtre.
        """
        self.setWindowTitle('Caractéristiques')
        self.setGeometry(320, 320, 320, 320)

        # Labels
        label1 = QLabel('Sexe:', self)
        label2 = QLabel('Couleur de cheveux:', self)
        label3 = QLabel('Pilosité faciale:', self)
        label4 = QLabel('Avait-il/elle des lunettes?', self)
        label5 = QLabel('Avait-il/elle un gros nez?', self)

        # Combo boxes
        nose = ['Oui', 'Non', 'Je ne sais pas']
        hair_colors = ['Brun', 'Gris', 'Blond', 'Noir', 'Chauve', 'Je ne sais pas']
        pilosite = ['Barbe', 'Moustache', 'Ni barbe,ni moustache', 'Je ne sais pas']
        sex = ['Homme', 'Femme']
        lunettes = ['Oui', 'Non', 'Je ne sais pas']

        self.sex_combo = QComboBox(self)
        self.sex_combo.addItems(sex)
        # self.eye_combo.move(140, 20)
        self.hair_combo = QComboBox(self)
        self.hair_combo.addItems(hair_colors)
        # self.hair_combo.move(140, 60)
        self.pilo_combo = QComboBox(self)
        self.pilo_combo.addItems(pilosite)
        # self.sex_combo.move(140, 100)
        self.lunettes = QComboBox(self)
        self.lunettes.addItems(lunettes)
        # self.skin_combo.move(140, 140)
        self.nose = QComboBox(self)
        self.nose.addItems(nose)

        # Button
        button = QPushButton('Soumettre', self)
        # button.move(100, 180)
        button.clicked.connect(self.submit)

        # Bouton pour retourner en arrière sur la fenêtre des coordonnées utilisateur
        self.bouton_retour = QPushButton('Retour')
        self.bouton_retour.clicked.connect(self.backwindow)

        layout = QGridLayout()
        # Qt.AlignVCenter
        layout.addWidget(label1, 1, 1)
        layout.addWidget(label2, 2, 1)
        layout.addWidget(label3, 3, 1)
        layout.addWidget(label4, 4, 1)
        layout.addWidget(label5, 5, 1)
        layout.addWidget(self.sex_combo, 1, 2)
        layout.addWidget(self.hair_combo, 2, 2)
        layout.addWidget(self.pilo_combo, 3, 2)
        layout.addWidget(self.lunettes, 4, 2)
        layout.addWidget(self.nose, 5, 2)
        layout.addWidget(button, 6, 2)
        layout.addWidget(self.bouton_retour, 7, 2)
        self.setLayout(layout)
        self.setWindowIcon(QIcon('logo.png'))

    def submit(self):
        """
        Fonction appelée lorsque l'utilisateur clique sur le bouton "button" pour soumettre.
        Si au moins une caractéristique est choisie, la fonction nextwindow2 est appelée.
        Sinon, un message d'erreur apparaît.
        Permet aussi d'établir une sous base d'images encodées qui correspondent aux caractéristiques sélectionnées.

        Utilise les variables globales banque_img et banque_filtre.
        """
        nose = self.nose.currentText()
        hair_color = self.hair_combo.currentText()
        sex = self.sex_combo.currentText()
        lunettes = self.lunettes.currentText()
        pilo = self.pilo_combo.currentText()
        if nose != 'Je ne sais pas' or hair_color != 'Je ne sais pas' or lunettes != 'Je ne sais pas' or pilo != 'Je ne sais pas':

            nb_lignes = 1000  # le nombre d'images maximal à prendre en compte = nb d'images encodées dans le fichier
            usecols = [i for i in range(1, 41)]
            mat = np.loadtxt('./Data/list_attr_celeba.txt', skiprows=1, max_rows=nb_lignes,
                             usecols=usecols)  # matrice contenant les attributs de chaque visage

            # Créer une liste filtrée en fonction des caractéristiques
            liste_filtree = get.filtre(get.create_dict(nose, hair_color, sex, lunettes, pilo), mat)
            # Créer une liste filtrée en fonction du sexe choisi
            liste_sex = get.filtre(get.create_sex_dict(sex), mat)
            # Renvoie une liste des indices des images à prendre dans la liste d'images encodées Attention : ne
            # correspond pas à l'identifiant de l'image mais à la position dans la liste qui commence à 0. Si on veut
            # retrouver l'identifiant, il faut faire +1 à tous les indices
            liste_img_filtre = get.data_img_filtrees(liste_filtree, liste_sex, 100)  # 100 images dans la liste

            global banque_img
            global banque_filtre
            for i in range(100):
                banque_filtre.append(banque_img[liste_img_filtre[i]])
            banque_filtre = np.array(banque_filtre)
            banque_img=[]
            self.nextwindow2()
        else:
            msg_err = QMessageBox()
            msg_err.setWindowTitle("Erreur")
            msg_err.setText("Veuillez choisir au moins une caractéristique.")
            msg_err.exec_()

    def nextwindow2(self):
        """
        Ouvre la fenêtre suivante (Fenêtre 3) et ferme la fenêtre courante.
        Utilise la variable globale banque_filtre
        """
        self.nextfen = FEN3(self.nom, self.prenom, self.date, banque_filtre)
        self.nextfen.show()
        self.close()

    def backwindow(self):
        """
        Ferme la fenêtre courante et ouvre la précédente (Fenêtre 1)
        """
        self.close()
        self.first_window = FEN1()
        self.first_window.show()


class FEN3(QWidget):
    """
        Fenêtre pour choisir récursivement l'image la plus ressemblante à l'agresseur
    Warning:
        img_encod doit comporter au moins 6 images pour pouvoir afficher une première fois la fenêtre.
    Attributes:
        img_encod (ndarray) : Liste d'images encodées
        pour i de 1 à 6 :
        img{i} (QPixmap) : L'image décodée d'un visage
        label{i} (QLabel) : Le label comportant l'image
        btn_selection{i} (CustomButton) : Bouton pour sélectionner l'image
        btn1 (QPushButton) : Bouton "continuer" pour relancer la fenêtre avec de nouvelles images
        btn2 (QPushButton) : Bouton "valider" pour valider le visage sélectionné passer à la fenêtre suivante
        fen (QGridLayout) : Grille pour disposer tous les éléments
        nextfen (QWidget) : La fenêtre suivante
        nom (String) : Le nom de l'utilisateur
        prénom (String) : Le prénom de l'utilisateur
        date (String) : La date de naissance
    Methods:
        __init__ (self,img) : Constructeur qui prend une liste d'images encodées en argument.

    """

    def __init__(self, nom, prenom, date, img):
        super().__init__()
        self.img_encod = img
        self.nom = nom
        self.prenom = prenom
        self.date = date
        self.initUI()

    def initUI(self):

        self.gen_premieres_img()
        # Une à une on prend les images et on les place dans un label
        self.img1 = QPixmap('Img/img1.png')
        self.label1 = QLabel()
        self.label1.setPixmap(self.img1)
        self.img2 = QPixmap('Img/img2.png')
        self.label2 = QLabel()
        self.label2.setPixmap(self.img2)
        self.img3 = QPixmap('Img/img3.png')
        self.label3 = QLabel()
        self.label3.setPixmap(self.img3)
        self.img4 = QPixmap('Img/img4.png')
        self.label4 = QLabel()
        self.label4.setPixmap(self.img4)
        self.img5 = QPixmap('Img/img5.png')
        self.label5 = QLabel()
        self.label5.setPixmap(self.img5)
        self.img6 = QPixmap('Img/img6.png')
        self.label6 = QLabel()
        self.label6.setPixmap(self.img6)

        # Ajout des deux boutons de validation
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

        self.fen.addWidget(QLabel("Sélectionnez le ou les deux visages qui ressemble(nt) le plus à votre agresseur(e)"),
                           6,
                           2, alignment=Qt.AlignCenter)
        self.fen.addWidget(self.bt1, 6, 3, alignment=Qt.AlignRight)
        self.fen.addWidget(self.bt2, 6, 1, alignment=Qt.AlignLeft)

        # Attribution aux boutons de validation les évenements correspondants
        self.bt1.clicked.connect(self.selection1vs5)
        self.bt2.clicked.connect(self.selection1_final)

        self.resize(900, 600)  # taille
        self.move(100, 100)  # position
        self.setLayout(self.fen)
        self.setWindowTitle("Choix du portrait")
        self.setWindowIcon(QIcon('logo.png'))

    def gen_premieres_img(self):
        """
        Décode les images encodées de l'attribut img_encod grâce au décodeur.
        Sauvegarde ces images au format .png dans le dossier Img
        """

        global decoder

        img_list = decoder.predict(self.img_encod)

        mat_im.imsave("Img/img1.png", img_list[0])
        mat_im.imsave("Img/img2.png", img_list[1])
        mat_im.imsave("Img/img3.png", img_list[2])
        mat_im.imsave("Img/img4.png", img_list[3])
        mat_im.imsave("Img/img5.png", img_list[4])
        mat_im.imsave("Img/img6.png", img_list[5])

    def nextimg(self):
        """Gère le renouvellement des images de la fenêtre et appelle l'algo génétique si besoin.

        La fonction compte le nombre d'itération de l'algo_gen.

        Si le nombre d'itération est supérieur à 25,
        un message d'erreur apparait et l'algo génétique s'arrête.

        Sinon appelle l'algo génétique.

        Utilise la variable globale cnt qui est incrémenté de 1 à chaque passage.

        See also:
            algo_gen()
        """
        global cnt

        list = [self.btn_selection1, self.btn_selection2, self.btn_selection3, self.btn_selection4, self.btn_selection5,
                self.btn_selection6]
        img_choisie = []
        # On regarde combien de boutons sont sélectionnés
        for i in range(len(list)):
            if list[i].isChecked():
                img_choisie.append(self.img_encod[i])

        if cnt < 25:
            cnt = cnt + 1
            self.algo_gen()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Il est temps de faire un choix, veuillez sélectionner 1 visage et cliquer sur soumettre")
            msg.exec_()

    def algo_gen(self):
        """Algo génétique

        Reste sur la même fenêtre en changeant les images
        Envoie sous forme de liste les images sélectionnées par l'utilisateur à l'algorithme génétique
        Actualise img1.jpg, img2.jpg, img3.jpg, img4.jpg
        Relance la fenêtre

        Le coût de l'algorithme est remplacé par le choix de l'utilisateur
        On procède à des mutations sur les images choisies
        On recrée une population avec les images choisies, les images modifiées et d'autres images "random"
        """
        list = [self.btn_selection1, self.btn_selection2, self.btn_selection3, self.btn_selection4, self.btn_selection5,
                self.btn_selection6]
        img_choisie = []
        len_img=len(img_choisie)
        # on prend celles qui ont le coût le plus faible soit celles choisies
        for i in range(len(list)):

            if list[i].isChecked():
                img_choisie.append(self.img_encod[i])
        # si une seule selectionnée pour augmenter diversité des choix on introduit un autre visage random
        # (on peut modifier mais ca simplifie le code de la suite)
        global banque_filtre
        global index_derniere_img_utilisee
        if len(img_choisie) == 4:
            rang = index_derniere_img_utilisee
            img_choisie.append(banque_filtre[rang])
            index_derniere_img_utilisee = index_derniere_img_utilisee + 1
            print(index_derniere_img_utilisee)
        while len(img_choisie) < 4:
            rang = index_derniere_img_utilisee
            img_choisie.append(banque_filtre[rang])
            index_derniere_img_utilisee = index_derniere_img_utilisee + 1
        img_choisie = np.asarray(img_choisie)
        #   procéde aux mutations et crossing over
        if (cnt < 10):
            new_img = algo.new_img_generator_debut(img_choisie,len_img)
            new_img = np.asarray(new_img)
        else:
            new_img = algo.new_img_generator_fin(img_choisie,len_img)
            new_img = np.asarray(new_img)
        #   ouverture de la nouvelle fenêtre == nouveau calcul du cout
        self.newfen = FEN3(self.nom, self.prenom, self.date, new_img)
        self.newfen.show()

        #   fermeture de l'ancienne
        self.close()

    def selection1vs5(self):
        """Vérification du nombre d'images sélectionnées :
        Il doit être égal entre 1 et 5 inclus
        Si nombre réglementaire, renvoie à la fonction nextimg
        Sinon affiche un message d'erreur
        """
        list = [self.btn_selection1, self.btn_selection2, self.btn_selection3, self.btn_selection4, self.btn_selection5,
                self.btn_selection6]
        cnt = 0
        for btn in list:
            if btn.isChecked():
                cnt = cnt + 1
        if cnt != 0 and cnt != 6:
            if cnt < 4:
                self.nextimg()
            else:
                buttonReply = QMessageBox.question(self, 'Avertissement',
                                                   "Voulez-vous continuer avec autant d'images? \nEn choisissant un grand nombre d'image la recherche sera moins efficace.",
                                                   QMessageBox.Yes | QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    self.nextimg()
                if buttonReply == QMessageBox.No:
                    print('No clicked.')

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez sélectionner au moins un visage et au plus cinq")
            msg.exec_()

    def selection1_final(self):
        """Verification du nombre d'images sélectionnées pour la validation finale
        Il doit être egal à 1 pour valider
        Si nombre réglementaire, renvoie à la fonction nextwindow
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
                btn_selected = int(np.where(list == btn)[0] + 1)  # numéro d'image correspondant à l'image choisie
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
        """ Renvoie sur la fenêtre suivante (Fenêtre 4) et ferme la fenêtre courante

        Parameters:
            img (QPixmap): Image finale choisie par l'utilisateur
        """

        self.fen = FEN4(self.nom, self.prenom, self.date, img)  # prend en paramètres l'image choisie
        self.fen.show()
        self.close()


class FEN4(QMainWindow):
    """
            Fenêtre pour valider son choix et générer un pdf
        Attributes:
            label (QLabel) : Décrit le role de la fenêtre
            label2 (QLabel) : Décrit comment remplir le champs text_edit
            text_edit (QTextEdit) : Vérification des noms et prénoms
            image_pixmap (DArray) : L'image sélectionnée
            button (QPushButton) : Bouton pour fermer le logiciel et générer un pdf en sortie
            nom (String) : Le nom de l'utilisateur
            prenom (String) : Le prénom de l'utilisateur
            date (String) : La date de naissance
        Methods:
            __init__ (self,image) : Constructeur qui prend l'image choisie dans la page precedente en argument
             save_to_pdf (self) : Génère un pdf de 2 pages qui permettent d'enregistrer le portrait robot avec et sans l'identité de la victime
            vérification (self) : Vérifie les nom et prénom entrés
        """

    def __init__(self, nom, prenom, date, image):
        super().__init__()

        self.nom = nom
        self.prenom = prenom
        self.date = date

        # Créer les widgets pour l'interface graphique
        self.label = QLabel("Vous confirmez que ce portrait robot correspond le mieux à votre agresseur :")
        self.image_label = QLabel()
        self.image_pixmap = image
        self.image_label.setPixmap(self.image_pixmap.scaledToWidth(400))
        self.label2 = QLabel("Merci de réindiquer votre nom puis prénom afin de vérifier votre identité.")

        self.text_edit = QTextEdit()
        self.text_edit.setMaximumSize(150, 25)
        self.button = QPushButton("Sauvegarder")

        # Créer un layout vertical pour contenir les widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label2, alignment=Qt.AlignCenter)
        layout.addWidget(self.text_edit, alignment=Qt.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # Créer un widget pour contenir le layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Associer un signal à l'événement "clicked" du bouton
        self.button.clicked.connect(self.save_to_pdf)

        self.setWindowTitle("Validation du portrait robot")
        self.setWindowIcon(QIcon('logo.png'))

    def save_to_pdf(self):
        """
        Appelle la fonction verification qui renvoie un boolean: elle vérifie que le nom et le prénom renseignés à la fenêtre 1 correspondent à ceux renseignés dans le QTextEdit "text_edit".
        Si True: Sauvegarde l'image choisie, le nom, le prénom, la date de naissance de la victime et la date du jour dans un fichier PDF au format nom_prenom.pdf dans le dossier User.
        Si False: Ne fait rien
        """
        # Obtenir le contenu du QTextEdit
        verif = self.text_edit.toPlainText()
        text_to_verify = self.nom.text() + " " + self.prenom.text()

        # Boolean pour savoir si la contenu du QtextEdit correspond aux noms et prénoms de la fenêtre 1
        correct = self.verification(verif, text_to_verify)

        if correct == True:

            # Données à mettre dans le pdf
            text = self.prenom.text() + " " + self.nom.text() + " né(e) le " + self.date.text()

            # date
            now = datetime.now()
            today = now.strftime("%d/%m/%Y %H:%M:%S")

            # Créer un objet canvas pour générer le PDF
            c = canvas.Canvas(f"User/{self.prenom.text()}_{self.nom.text()}.pdf", pagesize=letter)

            # Dessiner le titre
            c.setFontSize(20)
            c.drawString(1 * inch, 10 * inch, "Fiche récapitulative de la victime")

            # Dessiner le texte
            c.setFontSize(12)
            textobject = c.beginText(1 * inch, 7.5 * inch)
            for line in text.split('\n'):
                textobject.textLine(line)
            c.drawText(textobject)

            # Dessiner la date
            c.drawString(1 * inch, 8 * inch, today)

            # Sauter une page
            c.showPage()

            # Titre de la seconde page
            c.setFontSize(20)
            c.drawString(1 * inch, 10 * inch, "Portrait robot de l'agresseur")

            # Convertit l'image QPixmap en PIL Image
            qimage = self.image_pixmap.toImage()
            # Sauvegarde de l'image dans le directory
            qimage.save("./img_choisie.png", "PNG", -1)
            # Dessine l'image dans le pdf
            c.drawInlineImage("./img_choisie.png", 244, 400, height=128, width=128)
            # Enregistrer le PDF et fermer le canvas
            c.save()

            # Supprime l'image du directory
            os.remove("./img_choisie.png")

            msg = QMessageBox()
            msg.setWindowTitle("Terminé")
            msg.setText("Informations enregistrées dans le dossier User. Vous allez quitter le logiciel.")
            msg.exec_()

            self.close()

    def verification(self, verif_, text_):
        """
            Compare le contenu de deux chaînes de caractères.Si le contenu est le même, renvoie True. Sinon, un message d'erreur apparaît et la fonction renvoie False.
        Parameters:
            verif_ (str) : Les coordonnées rentrées en Fenêtre 4
            text_ (str) : Les coordonnées rentrées en Fenêtre 1
        Return:
            return (bool):
        """
        if verif_ != text_:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Les informations ne correspondent pas. Veuillez réessayer.")
            msg.exec_()
            return False
        else:
            return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = FEN0()
    main_window.show()
    sys.exit(app.exec_())
