from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler
from bot.views import *

from bot.models import Sections


def setup():
    Sections.objects.get_or_create(name="Welcome text", key='welcome')
    Sections.objects.get_or_create(name="Menu for user type", key='main')
    Sections.objects.get_or_create(name="Button for main buy and sell", key='mainbutton')
    Sections.objects.get_or_create(name="Please enter your phone number text", key='phone')
    Sections.objects.get_or_create(name="Send phone number button", key='phonebutton')
    Sections.objects.get_or_create(name="select language text", key='lang')
    Sections.objects.get_or_create(name="choose category text", key='categorytext')
    Sections.objects.get_or_create(name="select language button", key='langbutton')
    Sections.objects.get_or_create(name="Language changed text", key='lanchanged')
    Sections.objects.get_or_create(name="instagram username input", key='usernametxt')
    Sections.objects.get_or_create(name="username incorrect again input username", key='againusername')
    Sections.objects.get_or_create(name="Influencers- seller service txt", key='sellerservice')
    Sections.objects.get_or_create(name="give like section text", key='liketxt')
    Sections.objects.get_or_create(name="give comment section text", key='commenttxt')
    Sections.objects.get_or_create(name="confirm button", key='confirmbutton')
    Sections.objects.get_or_create(name="you are given 1 coin", key='commentexist')
    Sections.objects.get_or_create(name="please comment and check again", key='commentnotexist')


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        setup()
        request = Request(
            connect_timeout=None,
            read_timeout=None
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )

        updater = Updater(
            bot=bot,
            use_context=True
        )
        conv_hand = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text, start)
            ],
            states={
                'state_lang': [
                    CallbackQueryHandler(command_lang)
                ],
                'state_phone': [
                    MessageHandler(Filters.contact, command_phone)
                ],
                'state_main':[
                    CallbackQueryHandler(command_main)
                ],
                'state_username': [
                    MessageHandler(Filters.text, command_username)
                ],
                'state_category': [
                    CallbackQueryHandler(command_category)
                ],
                'state_service': [
                    CallbackQueryHandler(command_service)
                ],
                'state_check_service': [
                    CallbackQueryHandler(command_check_service)
                ]
            },
            fallbacks=[
                CommandHandler('start', start)
            ]

        )


        updater.dispatcher.add_handler(conv_hand)
        updater.dispatcher.add_handler(CommandHandler('language', set_language))
        updater.dispatcher.add_handler(CallbackQueryHandler(command_queries))
        updater.start_polling()
        updater.idle()