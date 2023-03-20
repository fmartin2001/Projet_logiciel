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
import algo_genetic as algo
import get_data as get
from PIL import Image
import matplotlib.image as mat_im
from tensorflow.keras.models import load_model

# variables globales : compteur pour l'algo gen et les images choisies
cnt = 1
img_recurrente = []
autoencoder = load_model("./Model/autoencoder")
banque_img = np.load('./Data/20_encoded_img.npy')


class customButton(QPushButton):
    """
    Redefinie le widget QPushButton
    Ajoute les attributs suivants :
        le logo 'check' ou rien
        une taille et une couleur
    redefinition de l'evenement clic :
        change la couleur et le logo

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
    Fenetre de presentation du logiciel
    Attributes:
        Label (QLabel) : phrase d'introduction
        image_label (QLabel) : le logo du logiciel
        nextfen (QWidget) : la fenetre suivante

    Methods :
         nextwindow2(self) : passe à la fenetre suivante (nextfen)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Projet')
        # Créer les widgets pour l'interface graphique
        self.label = QLabel(
            "Bienvenue dans un générateur de portrait robot ! Nous vous prions de répondre le plus honnêtement possible afin de faire un protrait robot de votre agresseur le plus représentatif possible")
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
    """
    Fenetre pour rentrer et sauvegarder les informations de l'utilisateur
    Elle contient trois champs à remplir
    Si un champs est vide au moment de la validation, un message d'erreur apparait

    Attributes:
        e1 (QLineEdit) : champs pour rentrer le nom
        e2 (QLineEdit) : champs pour rentrer le prenom
        e3 (QLineEdit) : champs pour rentrer la date de naissance
        btn (QPushButton) : bouton "soumettre" pour passer à la fenetre suivante
        nextfen (QWidget) : la fenetre suivante

    Methods :
         nextwindow(self) : passe à la fenetre suivante (nextfen)
         rempli(self) : vérifie que l'utilisateur est renseigné le nom prenom et la date demandés

    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.e1 = QLineEdit()
        self.e2 = QLineEdit()
        self.e3 = QLineEdit()
        self.btn = QPushButton()
        self.initUI()

    def initUI(self):

        # permet de rentrer le nom
        self.e1.setMaxLength(20)
        self.e1.setAlignment(Qt.AlignRight)
        self.e1.setFont(QFont("Helvetica", 10))

        # permet de rentrer le prenom
        self.e2.setMaxLength(20)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont(QFont("Helevetica", 10))

        # permet de rentrer la date de naissance
        self.e3.setValidator(QIntValidator())
        self.e3.setInputMask("99/99/9999")

        self.nextfen = FEN2(self.e1, self.e2, self.e3)  # sa fenetre suivante est la fenetre 2

        # bouton "soumettre" pour passer à la fenetre suivante et sauvegarder les données entrées
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
        """
        Renvoie vers la fonction nextwindow si tout est renseigné
        Renvoie un message d'erreur si un des champs est vide
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
        Ferme la fenetre 1 puis ouvre la fenetre 2
        """
        # changement de fenetre
        self.nextfen.show()
        self.close()  # or close


class FEN2(QWidget):
    """
        Fenetre pour rentrer les caractéristiques de l'agresseur

        Attributes:
            label1 (QLabel) : "Avait-il/elle un gros nez?"
            label2 (QLabel) : "Couleur des cheveux"
            label3 (QLabel) : "Sexe"
            label4 (QLabel) : "Avait-il/elle des lunettes?"
            Combo boxes (nose,hair_combo,sexe_combo,lunettes) respectivement les choix pour chaque label
            bouton_retour (QPushButton) : bouton "retour" pour revenir à la fenetre precedente
            nextfen (QWidget) : la fenetre suivante
            firstwindow (QWidget) : la fenetre precedente

        Methods :
             nextwindow2(self) : passe à la fenetre suivante (nextfen)
             backwindow(self) : revient à la fenetre precedente
             submit(self) : sauvegarde les caractéristiques choisies par l'utilisateur

        """

    def __init__(self, nom, prenom, date, parent=None):
        super().__init__(parent)
        self.nom = nom
        self.prenom = prenom
        self.date = date
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Caracteristiques')
        self.setGeometry(320, 320, 320, 320)

        # Labels
        label1 = QLabel('Avait-il/elle un gros nez?:', self)
        label2 = QLabel('Couleur des cheveux:', self)
        label3 = QLabel('Sexe:', self)
        label4 = QLabel('Avait-il/elle des lunettes ?', self)

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
        self.setWindowIcon(QIcon('logo.jpg'))

    def submit(self):
        nose = self.nose.currentText()
        hair_color = self.hair_combo.currentText()
        sex = self.sex_combo.currentText()
        lunettes = self.lunettes.currentText()
        print(
            f'Taille du nez : {nose}, Couleur des cheveux : {hair_color}, Sexe : {sex}, Avait-il des lunettes ? : {lunettes}')

    def nextwindow2(self):
        global banque_img
        self.nextfen = FEN3(self.nom,self.prenom,self.date,banque_img)
        self.nextfen.show()
        self.close()

    def backwindow(self):
        self.close()
        # ça marche (je sais pas pourquoi mais faut les mettre en attributs)

        self.first_window = FEN1()
        self.first_window.show()


class FEN3(QWidget):
    """
            Fenetre pour choisir récursivement l'image la plus ressemblante à l'agresseur

            Attributes:
                img_encod (ndarray) : liste d'image encodées

                pour i de 1 à 6 :
                img{i} (QPixmap) : l'image décodée d'un visage
                label{i} (QLabel) : le label comportant l'image
                btn_selection{i} (CustomButton) : bouton pour sélectionner l'image

                btn1 (QPushButton) : bouton "continuer" pour relancer la fenetre avec de nouvelles images
                btn2 (QPushButton) : bouton "valider" pour valider le visage sélectionné passer à la fenetre suivante
                fen (QGridLayout) : grille pour disposer tous les éléments

                nextfen (QWidget) : la fenetre suivante


            Methods :
                __init__ (self,img) : constructeur qui prend une liste d'images encodées en argument
                 gen_premieres_img (self) : decode des images et les enregistre
                 selection1_final (self) : verifie qu'une seule image soit choisie
                 selection_1vs5 (self) : vérifie qu'il un nombre d'images sélectionnées entre 1 et 5 inclu
                 nextimg (self) : renouvelle les images en passant par algo_gen si le nombre d'itération n'excède pas 10
                 algo_gen (self) : renouvelle les images
                 next_window (self) : passe à la fenetre suivante

            See Also :
                algo_gen.py
            """

    def __init__(self,nom,prenom,date, img):
        super().__init__()
        self.img_encod = img
        self.initUI()
        self.nom=nom
        self.prenom=prenom
        self.date=date

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
        else:
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
        # si une seule selectionnée pour augmenter diversité des choix on introduit un autre visage random
        # (on peut modifier mais ca simplifie le code de la suite)
        if len(img_choisie) == 1:
            rand = int(np.random.random() * 20)
            global banque_img
            img_choisie.append(banque_img[rand])

        img_choisie = np.asarray(img_choisie)
        print(len(img_choisie))
        #   procede aux mutations et crossing over
        new_img = algo.new_img_generator(img_choisie)
        new_img = np.asarray(new_img)
        print("hey")
        #   ouverture de la nouvelle fenetre == nouveau calcul du cout
        self.newfen = FEN3(self.nom,self.prenom,self.date,new_img)
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

        self.fen = FEN4(self.nom,self.prenom,self.date,img)  # prend en paramètres l'image choisie
        self.fen.show()
        self.close()


class FEN4(QMainWindow):
    """
        Fenetre pour valider son choix et générer un pdf

        Attributes:
            label (QLabel) : décrit le role de la fenetre
            image_label (QLabel) : contient l'image choisie

            button (QPushButton) : bouton pour fermer le logiciel et générer un pdf en sortie

            A FINIR


        Methods :
            __init__ (self,image) : constructeur qui prend l'image choisie dans la page precedente en argument
             save_to_pdf (self) : genere un pdf de 2 pages qui permettent d'enregistrer le portrait robot avec et sans l'identité de la victime

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

    def save_to_pdf(self):
        # Obtenir le contenu du QTextEdit
        verif = self.text_edit.toPlainText()
        text_to_verify = self.nom.text() + " " + self.prenom.text()

        # Boolean pour savoir si c'est bon
        correct = self.verification(verif, text_to_verify)

        if correct == True:

            # Données à mettre dans le pdf
            text = self.prenom.text() + " " + self.nom.text() + " né(e) le " + self.date.text()

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
            c.drawInlineImage("./img_choisie.png", 80, 250, height=270, width=480)
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
    # win = FEN1()
    # ndow = FEN3()
    # win.show()
    # window.show()
    # liste_img_encoded = np.load("Data/20_encoded_img.npy")
    main_window = FEN0()
    main_window.show()
    sys.exit(app.exec_())
