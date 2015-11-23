from django.forms.widgets import DateInput, FileInput
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.encoding import force_text


class DataPickerWidget(DateInput):
    """
    A DataInput Widget
    """

    class Media:
        css = {
            'all': (
                staticfiles_storage.url('css/jquery-ui.min.css'),
                staticfiles_storage.url('css/jquery-ui.theme.min.css'),
            )
        }
        js = (
            staticfiles_storage.url('js/jquery-1.11.3.min.js'),
            staticfiles_storage.url('js/jquery-ui.min.js'),
        )

    def __init__(self, params='', attrs=None):
        self.params = params
        super(DataPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(DataPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
                                    $('#id_%s').datepicker({%s});
                                    </script>''' % (name, self.params,))


class UploadImageWidget(FileInput):
    """
    An ImageField Widget
    """

    class Media:
        js = (
            staticfiles_storage.url('js/bootstrap-filestyle.min.js'),
        )

    def __init__(self, attrs=None):
        super(UploadImageWidget, self).__init__(attrs=attrs)

    template_with_initial = '%(initial)s%(input)s'

    url_markup_template = '<a href="{0}" class="thumbnail">\
                           <img src="{0}" alt="Person\'s photo" \
                           width="200" height="200"></a>'

    def render(self, name, value, attrs=None):
        substitutions = {}
        template = '%(input)s'
        attrs = {'multiple': '', 'accept': 'image/*,image/jpeg'}
        substitutions['input'] = super(UploadImageWidget, self).render(name,
                                                                       value,
                                                                       attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = format_html(self.url_markup_template,
                                                   value.url,
                                                   force_text(value))

        return mark_safe(template % substitutions) + mark_safe(
            u'''<script type="text/javascript">
            $(":file").filestyle({icon: false, placeholder: "No file"});
            </script>'''
        )
