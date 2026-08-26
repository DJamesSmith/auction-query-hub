from django import forms
from .models import User


class UserForm(forms.ModelForm):                                            # Creates a Django ModelForm class based on the User model.
    # Defines password as a form field. CharField determines what type of data the form accepts.
    # It means "create a character form field and use a password input widget to display it."
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={                                  # Specifies how the password field should be displayed in HTML. PasswordInput hides the entered characters.
                "class": "form-control",                                    # Adds HTML attributes to the password input, such as Bootstrap styling and placeholder text.
                "placeholder": "Enter password",
            }))

    class Meta:                                                             # Contains configuration for the ModelForm, such as the model, fields, and widgets.
        model: User = User
        fields: list[str] = ["username", "email", "password", "role"]
        widgets: dict = {                                                   # Defines widgets for the model fields. This dictionary expects widget instances, not form fields.
            "username": forms.TextInput(attrs={                             # TextInput is a widget that controls how the username field is displayed in HTML.
                    "class": "form-control",
                    "placeholder": "Enter username",
                }),
            "email": forms.EmailInput(attrs={                               # EmailInput is a widget that displays the email field as an HTML email input.
                "class": "form-control",
                "placeholder": "Enter email"
                }),
            "role": forms.Select(attrs = { "class": "form-select" }),       # Select is a widget that displays the role field as a dropdown.
        }

    # Django clean_<field>() validation — server-side validation that your AJAX request receives as JSON.

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Username is required.")
        if len(username) < 3:
            raise forms.ValidationError("Username must contain at least 3 characters.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email address is required.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password is required.")
        if len(password) < 6:
            raise forms.ValidationError("Password must contain at least 6 characters.")
        return password

    def clean_role(self):
        role = self.cleaned_data.get("role")
        if not role:
            raise forms.ValidationError("Please select a role.")
        if role not in User.Role.values:
            raise forms.ValidationError("Invalid user role.")
        return role



# Hashing the password before saving
# from django.contrib.auth.hashers import make_password
# user.password = make_password(form.cleaned_data["password"])
# Did not perform hash password due to insertion of bulk queries for testing JOIN queries.