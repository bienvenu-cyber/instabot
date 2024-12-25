from instabot import Bot
import os
import time
import random
import logging
from dotenv import load_dotenv

# Chargement des variables d'environnement
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

# Initialisation du bot
bot = Bot(debug=True)

try:
    # Connexion au compte Instagram
    bot.login(username=USERNAME, password=PASSWORD)
    logging.info("Connexion réussie au compte Instagram.")
except Exception as e:
    logging.error(f"Erreur de connexion : {e}")
    exit()

# Fonction pour suivre les utilisateurs d'un hashtag spécifique
def follow_users_by_hashtag(hashtag, max_follows=10):
    try:
        users = bot.get_hashtag_users(hashtag)
        count = 0
        for user in users:
            if count >= max_follows:
                break
            bot.follow(user)
            logging.info(f"Suivi de l'utilisateur {user}")
            count += 1
            time.sleep(random.randint(30, 90))  # Pause aléatoire pour imiter un comportement humain
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
                bot.like(post)
                logging.info(f"Like sur le post {post}")
                count += 1
                time.sleep(random.randint(10, 30))  # Pause aléatoire
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
                bot.comment(post, comment_text)
                logging.info(f"Commentaire sur le post {post}: {comment_text}")
                count += 1
                time.sleep(random.randint(20, 60))  # Pause aléatoire
    except Exception as e:
        logging.error(f"Erreur lors des commentaires : {e}")

# Exemple d'utilisation
hashtags = ["coding", "programming", "developer", "technology", "python", "innovation", "love", "entrepreneur", "motivation", "startup", "digitalmarketing", "singlelife", "webdevelopment", "gaming", "ai", "machinelearning", "dataanalysis", "iphone", "appdevelopment", "codingcommunity"]

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