from django.forms.widgets import Widget

class PlusMinusInput(Widget):
    template_name = 'widgets/plusminus.html'
    class Media:
        css = {
            'all': ('css/plusminus.css')
        }
        js = ('js/plusminus.js')
