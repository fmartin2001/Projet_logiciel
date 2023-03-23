VAR=$(realpath $0)
CHEMIN=$(echo "${VAR%/*}")

# Créer un environnement virtuel Python (qu'une seule fois)
#python3 -m venv env_robot
#pip3 install PyQt5 reportlab numpy matplotlib datetime Pillow pandas scikit-learn keras tensorflow

echo "[Desktop Entry]
Version= 1.0
Icon=$CHEMIN/logo.png
Name=Portrait robot
Exec=$CHEMIN/lancer.sh
Terminal=false
Type=Application" > $CHEMIN/appli.desktop

chmod u+x $CHEMIN/appli.desktop
