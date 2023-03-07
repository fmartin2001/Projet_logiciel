import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIntValidator, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QLineEdit, QWidget, QMessageBox, QFormLayout, QPushButton, \
    QGridLayout, QComboBox

class customLabel(QPushButton):
    # bouton personnaliser pour selectionner et deselectionner les visages
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("sélectionner")
        self.selected=False
    def mouseReleaseEvent(self, e):
        #redefinition de l'evenement "relacher la souris"
        if self.selected==False :
            self.setText("déselectionner")
            self.selected=True
        else :
            self.setText("sélectionner")
            self.selected = False
class FEN1(QWidget):
    #creation de la fenetre 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nextfen = FEN2()# sa fenetre suivante est la fenetre 2
        self.e1 = QLineEdit()# premiere entrée de texte
        self.e1.setMaxLength(20)
        self.e1.setAlignment(Qt.AlignRight)
        self.e1.setFont(QFont("Helvetica", 10))

        self.e2 = QLineEdit()# deuxieme entrée de texte
        self.e2.setMaxLength(20)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont(QFont("Arial", 10))

        self.e3 = QLineEdit()# troisieme pour la date de naissance
        self.e3.setValidator(QIntValidator())
        self.e3.setInputMask("99/99/9999")

        self.btn = QPushButton()# bouton valider pour passer à la fenetre suivante
        self.btn.setText("valider")

        flo = QFormLayout()# on met tout dans une grille pour que ca s'adapte à la largeur de la page
        # Qt.AlignVCenter
        flo.addRow("nom", self.e1)
        flo.addRow("prenom", self.e2)
        flo.addRow("date de naissance", self.e3)
        flo.addWidget(self.btn)

        self.resize(500, 220)#taille de la fenetre
        self.move(100, 100)# position de la fenetre
        self.setLayout(flo)# affichage de la grille
        self.setWindowTitle("Coordonnees utilisateur")
        # set icon
        # self.setWindowIcon(QtGui.QIcon('icon.png'))


        self.btn.clicked.connect(self.rempli)#action assignée au bouton valider (appelle la fct rempli)
        # btn.setToolTip("Close the widget")

    def rempli(self):# si tous les champs sont rempli appelle la fonction page suivante, sinon affiche un message d'erreur
        if (self.e1.text() != "" and self.e2.text() != "" and self.e3.text() != "//"):
            self.nextwindow()
        else:
            msg = QMessageBox(win)
            msg.setWindowTitle("erreur")
            msg.setText("Veuillez remplir tous les champs")

            x = msg.exec_()

    def textchanged(self, text): # a ma connaissance je ne l'utilise plus
        print("Changed: " + text)

    def nextwindow(self):# enregistre les infos (nom, prenom, date) dans un fichier et ferme la fen 1 pour ouvrir la fen 2
        # ecriture des infos de l'utilisateur
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
        self.close()


class FEN2(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Caracteristiques')
        self.setGeometry(320, 320, 320, 320)

        # Labels
        label1 = QLabel('Couleur des yeux:', self)
        # label1.move(20, 20)
        label2 = QLabel('Couleur des cheveux:', self)
        # label2.move(20, 60)
        label3 = QLabel('Taille:', self)
        # label3.move(20, 100)
        label4 = QLabel('Couleur de la peau:', self)
        # label4.move(20, 140)

        # Combo boxes
        eye_colors = ['Bleu', 'Marron', 'Vert', 'Noir']
        hair_colors = ['Noir', 'Brun', 'Blond', 'Roux']
        sex = ['Homme', 'Femme', 'Je ne sais pas']
        skin_colors = ['blanc', 'noir', 'métisse']
        self.eye_combo = QComboBox(self)
        self.eye_combo.addItems(eye_colors)
        # self.eye_combo.move(140, 20)
        self.hair_combo = QComboBox(self)
        self.hair_combo.addItems(hair_colors)
        # self.hair_combo.move(140, 60)
        self.sex_combo = QComboBox(self)
        self.sex_combo.addItems(sex)
        # self.sex_combo.move(140, 100)
        self.skin_combo = QComboBox(self)
        self.skin_combo.addItems(skin_colors)
        # self.skin_combo.move(140, 140)

        # Button
        button = QPushButton('Soumettre', self)
        # button.move(100, 180)
        button.clicked.connect(self.submit)

        layout = QGridLayout()
        # Qt.AlignVCenter
        layout.addWidget(label1, 1, 1)
        layout.addWidget(label2, 2, 1)
        layout.addWidget(label3, 3, 1)
        layout.addWidget(label4, 4, 1)
        layout.addWidget(self.eye_combo, 1, 2)
        layout.addWidget(self.hair_combo, 2, 2)
        layout.addWidget(self.sex_combo, 3, 2)
        layout.addWidget(self.skin_combo, 4, 2)
        layout.addWidget(button, 5, 2)
        self.setLayout(layout)

    def submit(self):
        eye_color = self.eye_combo.currentText()
        hair_color = self.hair_combo.currentText()
        sex = self.sex_combo.currentText()
        skin_colors = self.skin_combo.currentText()
        print(
            f'Couleur des yeux : {eye_color}, Couleur des cheveux : {hair_color}, Sexe : {sex}, Couleur de la peau : {skin_colors}')


class FEN3(QWidget):#creation de la fenetre 3
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        #appelle la fonction qui prend les images générées par fannie et natacha il faut voir si c'est la même la premiere fois et les fois suivante?
        self.gener_new_img()

#une à une on prend les image les met dans un label puis une grille
        self.img1 = QPixmap('img1.jpg')
        self.label1 = QLabel()
        self.label1.setPixmap(self.img1)
        self.img2 = QPixmap('img2.jpg')
        self.label2 = QLabel()
        self.label2.setPixmap(self.img2)
        self.img3 = QPixmap('img3.jpg')
        self.label3 = QLabel()
        self.label3.setPixmap(self.img3)
        self.img4 = QPixmap('img4.jpg')
        self.label4 = QLabel()
        self.label4.setPixmap(self.img4)

        self.bt1 = QPushButton("continuer la recherche")
        self.bt2 = QPushButton("valider le visage final")

        self.fen = QGridLayout()
        # Qt.AlignVCenter

#creation des boutons puour selectionner les images
        self.btn_selection1 = customLabel()
        self.btn_selection2 = customLabel()
        self.btn_selection3 = customLabel()
        self.btn_selection4 = customLabel()

# on met tout dans une grille
        self.fen.addWidget(self.label1, 1, 1)
        self.fen.addWidget(self.btn_selection1,2,1)
        self.fen.addWidget(self.label2, 1, 2)
        self.fen.addWidget(self.btn_selection2, 2, 2)
        self.fen.addWidget(self.label3, 3, 1)
        self.fen.addWidget(self.btn_selection3, 4, 1)
        self.fen.addWidget(self.label4, 3, 2)
        self.fen.addWidget(self.btn_selection4, 4, 2)

        self.fen.addWidget(self.bt1, 5, 1)
        self.fen.addWidget(self.bt2, 5, 2)

        self.bt1.clicked.connect(self.nextimg) #on assigne une action au bouton continuer
        self.bt2.clicked.connect(self.nextwindow)#on assigne une action au bouton valider

        self.resize(600, 600)
        self.move(100, 100)
        self.setLayout(self.fen)
        self.setWindowTitle("choix du portrait")
        # set icon
        # self.setWindowIcon(QtGui.QIcon('icon.png'))



    def gener_new_img(self):
        print("ouiiii je genere des nouvelles images blablabla")
        #   génération des 4 images
        #   ouverture de la nouvelle fenetre
        #   fermeture de l'ancienne



    def nextimg(self):
        self.selection1ou2()
        self.gener_new_img()
        #   appel algo génétique (tab image choisies)

    def selection1ou2(self):
        cnt = 0
        #for i in range (4):


    def nextwindow(self): #sauvegarde le choix final et envoie sur la page suivante (code pas fini sur cette fonction, pour l'instant renvoie juste sur la page suivante)
        self.fen = FEN4()
        self.fen.show()
        self.close()


class FEN4(QWidget):
    def __init__(self):
        super().__init__()

        # Création d'un widget QLabel pour afficher l'image
        image = QLabel(self)
        pixmap = QPixmap('img4.jpg')  # Chemin vers votre image
        image.setPixmap(pixmap)
        self.fen = QGridLayout()
        # Qt.AlignVCenter
        self.fen.addWidget(image, 1, 1)
        # image.setGeometry(10, 10, 200, 200)

        # Création d'un widget QLabel pour afficher le texte
        texte = QLabel(self)
        texte.setText("Bim est le coupable")
        # texte.setGeometry(50, 260, 300, 40)

        self.fen.addWidget(texte, 2, 1)
        self.setLayout(self.fen)
        # Configuration de la fenêtre principale
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Robotte les fesses')
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FEN1()
    window = FEN3()
    win.show()
    window.show()

    # main_window = FEN4()
    # main_window.show()
    sys.exit(app.exec_())
