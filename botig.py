from instabot import Bot
import os
import time
import random
import logging
from dotenv import load_dotenv

# Chargement des variables d'environnement
print("Chargement des variables d'environnement...")
load_dotenv()

# Configuration des identifiants depuis les variables d'environnement
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

# Configuration de la journalisation (logs)
logging.basicConfig(
    filename="bot.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialisation du bot sans option de proxy
print("Initialisation du bot...")
bot = Bot()
logging.info("Aucun proxy utilisé.")

# Vérification des identifiants
if not USERNAME or not PASSWORD:
    logging.error("Les identifiants Instagram ne sont pas définis.")
    exit()

# Connexion au compte Instagram
print("Connexion au compte Instagram...")
try:
    bot.login(username=USERNAME, password=PASSWORD)
    logging.info("Connexion réussie au compte Instagram.")
except Exception as e:
    logging.error(f"Erreur de connexion : {e}")
    print(f"Erreur de connexion : {e}")
    exit()

# Fonction pour suivre les utilisateurs d'un hashtag spécifique
def follow_users_by_hashtag(hashtag, max_follows=10):
    try:
        users = bot.get_hashtag_users(hashtag)
        count = 0
        for user in users:
            if count >= max_follows:
                break
            if bot.follow(user):
                logging.info(f"Suivi de l'utilisateur {user}")
                count += 1
            else:
                logging.warning(f"Échec du suivi de l'utilisateur {user}")
            time.sleep(random.randint(90, 120))  # Pause aléatoire pour imiter un comportement humain
    except Exception as e:
        logging.error(f"Erreur lors du suivi des utilisateurs pour le hashtag {hashtag} : {e}")

# Fonction pour liker les posts récents des utilisateurs suivis
def like_recent_posts_of_followed_users(max_likes=10):
    try:
        followed_users = bot.following
        for user in followed_users:
            posts = bot.get_user_medias(user, filtration=False)
            count = 0
            for post in posts[:5]:  # Liker les 5 premiers posts
                if count >= max_likes:
                    break
                if bot.like(post):
                    logging.info(f"Like sur le post {post}")
                    count += 1
                else:
                    logging.warning(f"Échec du like sur le post {post}")
                time.sleep(random.randint(30, 60))  # Pause aléatoire
    except Exception as e:
        logging.error(f"Erreur lors du like des posts : {e}")

# Fonction pour commenter les posts récents des utilisateurs suivis
def comment_on_recent_posts(max_comments=5, comment_text="Super post !"):
    try:
        followed_users = bot.following
        for user in followed_users:
            posts = bot.get_user_medias(user, filtration=False)
            count = 0
            for post in posts[:3]:  # Commenter les 3 premiers posts
                if count >= max_comments:
                    break
                if bot.comment(post, comment_text):
                    logging.info(f"Commentaire sur le post {post}: {comment_text}")
                    count += 1
                else:
                    logging.warning(f"Échec du commentaire sur le post {post}")
                time.sleep(random.randint(90, 120))  # Pause aléatoire
    except Exception as e:
        logging.error(f"Erreur lors des commentaires : {e}")

# Fonction pour envoyer des alertes en cas d'erreurs critiques
def send_alert(message):
    # Implémentez une méthode pour envoyer des alertes, par exemple par email
    logging.info(f"Envoi d'une alerte : {message}")

# Exemple d'utilisation
hashtags = ["holiday", "christmass"]

for hashtag in hashtags:
    follow_users_by_hashtag(hashtag, max_follows=10)  # Suivre jusqu'à 10 utilisateurs par hashtag
    like_recent_posts_of_followed_users(max_likes=10)  # Liker jusqu'à 10 posts
    comment_on_recent_posts(max_comments=5, comment_text="Super post !")  # Ajouter des commentaires

# Déconnexion
try:
    bot.logout()
    logging.info("Déconnexion réussie.")
except Exception as e:
    logging.error(f"Erreur lors de la déconnexion : {e}")

# Rappel pour tester régulièrement le bot et respecter les conditions d'utilisation d'Instagram
# Assurez-vous de tester régulièrement le bot et de respecter les conditions d'utilisation d'Instagram.