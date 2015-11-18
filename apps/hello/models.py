from django.db import models


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

    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.last_name, self.email)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
