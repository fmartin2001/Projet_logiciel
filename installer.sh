VAR=$(realpath $0)
CHEMIN=$(echo "${VAR%/*}")

# Créer un environnement virtuel Python (qu'une seule fois)
cd $CHEMIN
python3 -m venv env_robot
source ./env_robot/bin/activate

pip3 install --upgrade pip
pip3 install PyQt5 reportlab numpy matplotlib datetime Pillow pandas scikit-learn keras tensorflow --no-cache-dir

echo "[Desktop Entry]
Version= 1.0
Icon=$CHEMIN/logo.png
Name=Portrait robot
Exec=$CHEMIN/lancer.sh
Terminal=false
Type=Application" > $CHEMIN/appli.desktop

chmod u+x $CHEMIN/appli.desktop
