__version__ = "0.9.9.1"
__author__ = "mahrtayyab"

from modules.tweety.src.tweety.bot import BotMethods
from modules.tweety.src.tweety.updates import UpdateMethods
from modules.tweety.src.tweety.auth import AuthMethods
from modules.tweety.src.tweety.user import UserMethods


class Twitter(
    UserMethods, BotMethods, UpdateMethods, AuthMethods
):
    pass



