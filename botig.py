from instabot import Bot
import time
import random

# Initialisation du bot
bot = Bot()

# Connexion au compte Instagram
bot.login(username="votre_nom_utilisateur", password="votre_mot_de_passe")

# Fonction pour suivre les utilisateurs d'un hashtag spécifique
def follow_users_by_hashtag(hashtag):
    users = bot.get_hashtag_users(hashtag)
    for user in users:
        bot.follow(user)
        time.sleep(random.randint(30, 90))  # Attendre entre 30 et 90 secondes entre les suivis pour imiter un comportement humain

# Fonction pour liker les posts récents des utilisateurs suivis
def like_recent_posts_of_followed_users():
    followed_users = bot.following
    for user in followed_users:
        posts = bot.get_user_medias(user, filtration=False)
        for post in posts[:5]:  # Liker les 5 premiers posts
            bot.like(post)
            time.sleep(random.randint(10, 30))  # Attendre entre 10 et 30 secondes entre les likes

# Fonction pour commenter les posts récents des utilisateurs suivis
def comment_on_recent_posts():
    followed_users = bot.following
    for user in followed_users:
        posts = bot.get_user_medias(user, filtration=False)
        for post in posts[:3]:  # Commenter les 3 premiers posts
            bot.comment(post, "Super post !")
            time.sleep(random.randint(20, 60))  # Attendre entre 20 et 60 secondes entre les commentaires

# Exemple d'utilisation
hashtags = ["coding", "programming", "developer"]

for hashtag in hashtags:
    follow_users_by_hashtag(hashtag)
    like_recent_posts_of_followed_users()
    comment_on_recent_posts()

# Se déconnecter
bot.logout()
