from django.shortcuts import render
from telegram import Update
from telegram.ext import CallbackContext
from .Button import *
from instagrapi import Client
from django.conf import settings

import environ

env = environ.Env()
environ.Env.read_env()

def check_comment(username, post_url):
    cl = Client()
    cl.login(env('instagram_username'), env('instagram_password'))

    media_id = cl.media_id(cl.media_pk_from_url(post_url))

    comment = cl.media_comments(media_id, 1000000)

    for i in comment:
        if i.dict()['user']['username'] == username:
            return True
    return False

def start(update: Update, context: CallbackContext):
    user, status = Users.objects.get_or_create(telegram_id=update.effective_user.id)
    user.first_name = update.effective_user.first_name
    user.last_name = update.effective_user.last_name
    user.save()
    message = Messages.objects.filter(section__key='welcome').last()
    mes = message.text_eng + '\n' + message.text_ar
    update.message.reply_html(mes, reply_markup=ReplyKeyboardRemove())
    if user.lang:
        if user.phone_number:
            mes = Messages.objects.filter(section__key='main').last()
            if user.lang == 'eng':
                mes = mes.text_eng
            elif user.lang == 'ar':
                mes = mes.text_ar
            update.message.reply_html(mes, reply_markup=main_button(user.lang))
            return 'state_main'
        else:
            mes = Messages.objects.filter(section__key='phone').last()
            if user.lang == 'eng':
                mes = mes.text_eng
            elif user.lang == 'ar':
                mes = mes.text_ar
            update.message.reply_html(mes, reply_markup=phone_button(user.lang))
            return 'state_phone'
    else:
        message = Messages.objects.filter(section__key='lang').last()
        mes = message.text_eng + '\n' + message.text_ar
        update.message.reply_text(mes, reply_markup=choose_language_button())
        return 'state_lang'


def command_lang(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user = Users.objects.get(telegram_id=update.effective_user.id)
    if data == 'eng':
        user.lang = 'eng'
    elif data == 'ar':
        user.lang = 'ar'
    user.save()
    if user.lang:
        query.message.delete()
        mes = Messages.objects.filter(section__key='phone').last()
        if user.lang == 'eng':
            mes = mes.text_eng
        elif user.lang == 'ar':
            mes = mes.text_ar
        query.message.reply_html(mes, reply_markup=phone_button(user.lang))
        return 'state_phone'


def command_phone(update: Update, context: CallbackContext):
    phone = update.message.contact.phone_number
    user = Users.objects.get(telegram_id=update.effective_user.id)
    user.phone_number = phone
    user.save()
    mes = Messages.objects.filter(section__key='main').last()
    if user.lang == 'eng':
        mes = mes.text_eng
    elif user.lang == 'ar':
        mes = mes.text_ar
    update.message.reply_html(mes, reply_markup=main_button(user.lang))
    return 'state_main'


def set_language(update: Update, context: CallbackContext):
    message = Messages.objects.filter(section__key='lang').last()
    mes = message.text_eng + '\n' + message.text_ar
    update.message.reply_text(mes, reply_markup=choose_language_button())


def command_queries(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user = Users.objects.get(telegram_id=update.effective_user.id)
    message = Messages.objects.filter(section__key='lanchanged').last()
    if data == 'eng':
        user.lang = 'eng'
    elif data == 'ar':
        user.lang = 'ar'
    user.save()
    if user.lang and (data == 'eng' or data == 'ar'):
        if user.lang == 'eng':
            text = message.text_eng
        else:
            text = message.text_ar
        query.message.edit_text(text, parse_mode='HTML')


def command_main(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user = Users.objects.get(telegram_id=update.effective_user.id)
    data, id = data.split('_')
    if data == 'usertype':
        try:
            usertype = UserTypeCategory.objects.get(id=int(id))
            if 'influe' in usertype.name_eng:
                if user.instagram_username:
                    message = Messages.objects.filter(section__key='categorytext').last()
                    if user.lang == 'eng':
                        text = message.text_eng
                    else:
                        text = message.text_ar
                    query.message.edit_text(text, reply_markup=choose_category_button(user.lang), parse_mode='HTML')
                    return 'state_category'
                else:
                    message = Messages.objects.filter(section__key='usernametxt').last()
                    if user.lang == 'eng':
                        text = message.text_eng
                    else:
                        text = message.text_ar
                    query.message.edit_text(text)
                    return 'state_username'
        except Exception as e:
            print(e)


def check_user_exist(username):
    import requests

    url = "https://instagram47.p.rapidapi.com/get_user_id"

    querystring = {"username": f"{username}"}

    headers = {
        "X-RapidAPI-Key": "5d21dc8f4bmsh18656fa8c84a19ep107680jsnae6a8e19c697",
        "X-RapidAPI-Host": "instagram47.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.json())
    if response.json()['status'] == 'Success':
        return True
    else:
        return False


def command_username(update: Update, context: CallbackContext):
    username = update.message.text
    user = Users.objects.get(telegram_id=update.effective_user.id)
    if " " not in username and check_user_exist(username):
        message = Messages.objects.filter(section__key='categorytext').last()
        user.instagram_username = username
        user.save()
        if user.lang == 'eng':
            text = message.text_eng
        else:
            text = message.text_ar
        update.message.reply_html(text, reply_markup=choose_category_button(user.lang))
        return 'state_category'
    else:
        message = Messages.objects.filter(section__key='againusername').last()
        if user.lang == 'eng':
            text = message.text_eng
        else:
            text = message.text_ar
        update.message.reply_text(text)
        return 'state_username'


def command_category(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    data, id = data.split('_')
    user = Users.objects.get(telegram_id=update.effective_user.id)
    if data == 'category':
        try:

            category = Category.objects.get(id=int(id))
            context.user_data['category'] = category
            message = Messages.objects.filter(section__key='sellerservice').last()
            if user.lang == 'eng':
                text = message.text_eng
            else:
                text = message.text_ar
            query.message.edit_text(text, reply_markup=choose_service_button(user.lang), parse_mode='HTML')
            return 'state_service'
        except Exception as e:
            print(e)

    else:
        query.message.delete()
        message = Messages.objects.filter(section__key='categorytext').last()
        if user.lang == 'eng':
            text = message.text_eng
        else:
            text = message.text_ar
        query.message.reply_html(text, reply_markup=choose_category_button(user.lang))
        return 'state_category'


def command_service(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    data, id = data.split('_')
    user = Users.objects.get(telegram_id=update.effective_user.id)
    if data == 'service':
        try:
            service = ServiceCategory.objects.get(id=int(id))
            context.user_data['service'] = service
            if 'like' in service.name_eng:
                context.user_data['service'] = 'like'
                message = Messages.objects.filter(section__key='liketxt').last()
                if user.lang == 'eng':
                    text = message.text_eng
                else:
                    text = message.text_ar
            else:
                context.user_data['service'] = 'comment'
                message = Messages.objects.filter(section__key='commenttxt').last()
                if user.lang == 'eng':
                    text = message.text_eng
                else:
                    text = message.text_ar
            services = Services.objects.filter(servicecategory=service, status='progress').first()
            text += f"\n{services.instagram_url}\n" \
                    f"your username: {user.instagram_username}"
            context.user_data['post'] = services.id
            context.user_data['url'] = services.instagram_url
            query.message.edit_text(text, reply_markup=confirm_services_button(user.lang, services.instagram_url),
                                    parse_mode='HTML')
            return 'state_check_service'


        except Exception as e:
            print(e)

    else:
        query.message.delete()
        message = Messages.objects.filter(section__key='sellerservice').last()
        if user.lang == 'eng':
            text = message.text_eng
        else:
            text = message.text_ar
        query.message.reply_html(text, reply_markup=choose_service_button(user.lang))
        return 'state_service'


def command_check_service(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user = Users.objects.get(telegram_id=update.effective_user.id)
    if data == 'confirm':
        if context.user_data['service'] == 'comment':
            post = context.user_data['post']
            username = user.instagram_username
            if check_comment(username, context.user_data['url']):
                message = Messages.objects.filter(section__key='commentexist').last()
                if user.lang == 'eng':
                    text = message.text_eng
                else:
                    text = message.text_ar
                user.coin+=1
                user.save()
                query.message.edit_text(text, reply_markup=main_button(user.lang), parse_mode='HTML')
                return 'state_main'
            else:
                query.message.delete()
                message = Messages.objects.filter(section__key='commentnotexist').last()
                if user.lang == 'eng':
                    text = message.text_eng
                else:
                    text = message.text_ar
                text += f"\n{context.user_data['url']}\n" \
                        f"your username: {user.instagram_username}"
                query.message.reply_html(text, reply_markup=confirm_services_button(user.lang, context.user_data['url']))

                return 'state_check_service'

