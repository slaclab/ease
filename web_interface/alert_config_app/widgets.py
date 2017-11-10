""" widgets.py is used for customizing the input elements rendered in forms

A number of django's default input widgets do not offer the flexibility 
required by ease. Additionally, these widgets often have peculiar interactions
with Bootstrap causing form elements to often look deformed, misplaced or
missing entirely. The primary means of determining the widget's appearence is
drawn from the template file used to render the widget. As a result many of the
new widget classes introduced in this file will have no function other than to
link a preexisting widget to new template in a subclass. Most of these new
templates are heavily based upon the default django templates with only slight
modifications. 
Note 
----
    Modifications to the inherited values such as template_name must be made in
    init and call super. init takes one named argument: attrs

Note
----
    Widgets are being placed in the alert_config_app because the engine
    responsible for rendering widgets does not interact with the TEMPLATES
    setting in the master settings file,
    web_interface/web_interface/settings.py, like the normal page rendering
    engine. For more info, see this stackexchange thread:
    https://stackoverflow.com/questions/45844032/django-templatedoesnotexist-in-case-of-a-custom-widget

"""

from django import forms

class HorizontalCheckbox(forms.CheckboxInput):
    """Provides a horizontal-form-style bootstrap compatible checkbox.

    The default django checkbox.html simiply inherits from the input wideget so
    the horizontal_checkbox.html is based upon django's generic input.html
    instead of the more specific checkbox.html
    """
    def __init__(self, attrs=None,*args,**kwargs):
        """Edit the configuration of the HorizontalCheckbox

        Args
        ----
            attrs : dict
                specify the attributes of the html <input>. It is strongly
                recommended that the dict contain:
                    "class":"form-check-input position-static",
                    "type":"checkbox"
        """
        self.template_name = "horizontal_checkbox.html"
        super().__init__(attrs,*args,**kwargs)
        

