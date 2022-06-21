from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from .models import *


def main_button(lang):
    categories = UserTypeCategory.objects.all()
    button = []
    for i in categories:
        if lang == 'eng':
            name = i.name_eng
        else:
            name = i.name_ar
        button.append([InlineKeyboardButton(name, callback_data=f'usertype_{i.id}')])
    return InlineKeyboardMarkup(button)


def phone_button(lang):
    message = Messages.objects.filter(section__key='phonebutton').last()
    if lang == 'eng':
        mes = message.text_eng
    else:
        mes = message.text_ar
    button = [
        [KeyboardButton(mes, request_contact=True)]
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


def choose_language_button():
    message = Messages.objects.filter(section__key='langbutton').last()
    button = [
        [InlineKeyboardButton(message.text_eng, callback_data='eng')],
        [InlineKeyboardButton(message.text_ar, callback_data='ar')]
    ]
    return InlineKeyboardMarkup(button)


def choose_category_button(lang):
    categories = Category.objects.all()
    button = []
    for i in categories:
        if lang == 'eng':
            button.append([InlineKeyboardButton(i.name_eng, callback_data=f"category_{i.id}")])
        else:
            button.append([InlineKeyboardButton(i.name_ar, callback_data=f"category_{i.id}")])
    return InlineKeyboardMarkup(button)


def choose_service_button(lang):
    categories = ServiceCategory.objects.all()
    button = []
    for i in categories:
        if lang == 'eng':
            button.append([InlineKeyboardButton(i.name_eng, callback_data=f"service_{i.id}")])
        else:
            button.append([InlineKeyboardButton(i.name_ar, callback_data=f"service_{i.id}")])
    return InlineKeyboardMarkup(button)


def confirm_services_button(lang, url):
    button = []
    message = Messages.objects.filter(section__key='confirmbutton').last()
    if lang == 'eng':
        button.append([InlineKeyboardButton(message.text_eng, callback_data='confirm')])
    else:
        button.append([InlineKeyboardButton(message.text_ar, callback_data='confirm')])
    button.append([InlineKeyboardButton("Post", url=url)])
    return InlineKeyboardMarkup(button)
