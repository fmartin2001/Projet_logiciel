import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIntValidator, QFont
from PyQt5.QtWidgets import QLabel, QTextEdit, QApplication, QLineEdit, QWidget, QMessageBox, QFormLayout, QPushButton, QGridLayout, QComboBox, QMainWindow, QVBoxLayout
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


class FEN1(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.nextfen = FEN2()
        self.e1 = QLineEdit()
        self.e1.setMaxLength(20)
        self.e1.setAlignment(Qt.AlignRight)
        self.e1.setFont(QFont("Helvetica", 10))

        self.e2 = QLineEdit()
        self.e2.setMaxLength(20)
        self.e2.setAlignment(Qt.AlignRight)
        self.e2.setFont(QFont("Arial", 10))

        self.e3 = QLineEdit()
        self.e3.setValidator(QIntValidator())
        self.e3.setInputMask("99/99/9999")

        self.btn = QPushButton()
        self.btn.setText("valider")

        flo = QFormLayout()
        # Qt.AlignVCenter
        flo.addRow("nom", self.e1)
        flo.addRow("prenom", self.e2)
        flo.addRow("date de naissance", self.e3)
        flo.addWidget(self.btn)

        self.resize(500, 220)
        self.move(100, 100)
        self.setLayout(flo)
        self.setWindowTitle("Coordonnees utilisateur")
        # set icon
        # self.setWindowIcon(QtGui.QIcon('icon.png'))
        # self.nom = str(e1.text())
        # print(self.nom)
        # self.pren = str(e2.text())
        # self.date = str(e3.text())

        self.btn.clicked.connect(self.rempli)
        # btn.setToolTip("Close the widget")

    def rempli(self):
        if (self.e1.text() != "" and self.e2.text() != "" and self.e3.text() != "//"):
            self.nextwindow()
        else:
            msg = QMessageBox(win)
            msg.setWindowTitle("erreur")
            msg.setText("Veuillez remplir tous les champs")

            x = msg.exec_()

    def textchanged(self, text):
        print("Changed: " + text)

    def nextwindow(self):
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
        self.nextfen = FEN3()
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
        button.clicked.connect(self.nextwindow2)

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
        print(f'Couleur des yeux : {eye_color}, Couleur des cheveux : {hair_color}, Sexe : {sex}, Couleur de la peau : {skin_colors}')


    def nextwindow2(self):
        self.nextfen.show()
        self.close()

class FEN3(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.gener_new_img()

        self.choisi1 = False
        self.choisi2 = False
        self.choisi3 = False
        self.choisi4 = False

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



        # self.label2.installEventFilter()
        # self.label4.mouseDoubleClickEvent

        self.bt1 = QPushButton("continuer")
        self.bt2 = QPushButton("valider")

        self.fen = QGridLayout()
        # Qt.AlignVCenter
        self.btn3=QPushButton("choisir")
        self.fen.addWidget(self.label1, 1, 1)
        self.fen.addWidget(self.btn3,1,1)
        self.fen.addWidget(self.label2, 1, 2)
        self.fen.addWidget(self.label3, 2, 1)
        self.fen.addWidget(self.label4, 2, 2)

        self.fen.addWidget(self.bt1, 3, 1)
        self.fen.addWidget(self.bt2, 3, 2)

        self.bt1.clicked.connect(self.nextimg)
        self.bt2.clicked.connect(self.nextwindow)

        self.resize(600, 600)
        self.move(100, 100)
        self.setLayout(self.fen)
        self.setWindowTitle("choix du portrait")
        # set icon
        # self.setWindowIcon(QtGui.QIcon('icon.png'))

    # def eventFilter(self, object, event):
    #
    #     if object == self.label2 and event.type() == QEvent.MouseButtonDblClick:
    #         print("allelujah")


        # return False
    def changechoisi2(self):
        if self.choisi2 != True:
            self.choisi2=True
        else:
            self.choisi2=False

    def gener_new_img(self):
        print("ouiiii je genere des nouvelles images blablabla")


    def mouseReleaseEvent(self, event):
        super().mouseDoubleClickEvent(event)
        print(event.button())
        cache = QLabel("Image choisie")
        cache.setFont(QFont("Helvetica", 30))
        # sender=self.sender
        # print(sender.text())
        #self.fen.addWidget(cache, i % 2, i // 2)

    def nextimg(self):
        self.gener_new_img()

    def nextwindow(self):
        self.fen = FEN4()
        self.fen.show()
        self.close()


class FEN4(QMainWindow):
    def __init__(self):
        super().__init__()

        # Créer les widgets pour l'interface graphique
        self.label = QLabel("Vous confirmez que ce portrait robot correspond le mieux à votre agresseur :")
        self.image_label = QLabel()
        self.image_pixmap = QPixmap("/home/cbuton/Documents/INSA/4BIM/S2/ProjetDevLogi/gui/img1.jpg")
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

        # Dessiner l'image
        c.drawInlineImage("/home/cbuton/Documents/INSA/4BIM/S2/ProjetDevLogi/gui/img1.jpg", 80, 250, height=270, width=480)

        # Dessiner le texte
        c.setFontSize(12)
        textobject = c.beginText(1 * inch, 7.5 * inch)
        for line in text.split('\n'):
            textobject.textLine(line)
        c.drawText(textobject)

        # Enregistrer le PDF et fermer le canvas
        c.save()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #win = FEN1()
    #window = FEN3()
    #win.show()
    #window.show()

    main_window = FEN4()
    main_window.show()
    sys.exit(app.exec_())
