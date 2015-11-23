# -*- coding: utf-8 -*-
import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from PIL import Image as Img


class Person(models.Model):
    first_name = models.CharField("name", max_length=30)
    last_name = models.CharField("last name", max_length=30)
    date_of_birthday = models.DateField(
        "date of birth",
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    bio = models.TextField("bio", max_length=255, blank=True)
    email = models.EmailField("email")
    jabber = models.CharField("jabber",
                              max_length=30, blank=True)
    skype = models.CharField("skype",
                             max_length=30, blank=True)
    other_contacts = models.TextField("other contacts",
                                      max_length=255, blank=True)

    person_pic = models.ImageField("photo",
                                   upload_to='pic_folder/',
                                   default='pic_folder/None/no-img.jpg')

    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.last_name, self.email)

    def save(self, *args, **kwargs):
        image_width = 200
        image_height = 200
        image_size = (image_width, image_height)
        image_isSame = False

        if self.person_pic:
            try:
                this = Person.objects.get(id=self.id)
                if this.person_pic == self.person_pic:
                    image_isSame = True
            except:
                pass

            image = Img.open(StringIO.StringIO(self.person_pic.read()))

            if image.mode not in ("L", "RGB"):
                image = image.convert("RGB")

            (imw, imh) = image.size
            if (imw > image_width) or (imh > image_height):
                image.thumbnail(image_size, Img.ANTIALIAS)

            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.person_pic = InMemoryUploadedFile(
                output,
                'ImageField',
                "%s.jpg" % self.person_pic.name.split('.')[0],
                'image/jpeg', output.len, None
            )

        try:
            this = Person.objects.get(id=self.id)
            if this.person_pic == self.person_pic or image_isSame:
                self.person_pic = this.person_pic
            else:
                this.person_pic.delete(save=False)
        except:
            pass

        super(Person, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


class Requests(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=1000)
    method = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=1000, blank=True, null=True)
    remote_addr = models.IPAddressField()
    is_secure = models.BooleanField()
    is_ajax = models.BooleanField()

    def __unicode__(self):
        return "%s %s %s" % (self.time, self.path, self.remote_addr)

    class Meta:
        verbose_name = 'Requests'
        verbose_name_plural = 'Requests'
