from django.db import models


class Sections(models.Model):
    name = models.CharField(max_length=225, null=True, blank=True)
    key = models.CharField(max_length=35, null=True, blank=True)

    def __str__(self):
        return self.name


class Messages(models.Model):
    section = models.OneToOneField(Sections, on_delete=models.CASCADE)
    text_eng = models.TextField()
    text_ar = models.TextField()

    def __str__(self):
        return f"{self.text_eng}"


class UserTypeCategory(models.Model):
    name_eng = models.CharField(max_length=255, null=True)
    name_ar = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name_eng


class Users(models.Model):
    choices = (("eng", "English"), ('ar', "Arabic"))
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    lang = models.CharField(max_length=55, null=True, blank=True, choices=choices)
    instagram_username = models.CharField(max_length=255, null=True, blank=True)
    coin = models.IntegerField(default=0)
    def __str__(self):
        mes = ''
        if self.phone_number:
            mes += self.phone_number
        if self.first_name:
            mes += self.first_name

        return mes


class Category(models.Model):
    name_eng = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name_eng}"
class ServiceCategory(models.Model):
    name_eng = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name_eng}"
class Services(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    servicecategory = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    instagram_url = models.CharField(max_length=125)
    quantity = models.IntegerField(default=5)
    lefquantity = models.IntegerField(default=0)
    status = models.CharField(max_length=125, choices=(('progress', "Progress"),('done', 'Finished')), default='progress')

    def __str__(self):
        return f"{self.user.first_name}  {self.status}"



