# Chargement de l'image tar
docker load -i bento_image.tar

# Lancer l'image docker
docker run --rm -p 3000:3000 doucet_admission:latest

# Lancer les tests
python3 -m pytest service_test.py
