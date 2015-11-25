from django.core.urlresolvers import reverse
from django import template


register = template.Library()


@register.simple_tag
def edit_link(obj):
    return reverse("admin:%s_%s_change" %
                   (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
