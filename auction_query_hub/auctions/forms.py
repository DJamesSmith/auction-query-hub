from django import forms
from .models import AuctionItem
from users.models import User

class AuctionForm(forms.ModelForm):
    class Meta:
        model: AuctionItem = AuctionItem
        fields = ["title", "description", "base_price", "current_price", "start_time", "end_time", "seller"]

        widgets = {
            "title": forms.TextInput(attrs={
                    "class": "form-control",
                    "placeholder": "Enter auction title",
                }),
            "description": forms.Textarea(attrs={
                    "class": "form-control",
                    "placeholder": "Enter auction description",
                    "rows": 4,
                }),
            "base_price": forms.NumberInput(attrs={
                    "class": "form-control",
                    "placeholder": "Enter base price",
                    "step": "0.01",
                    "min": "0",
                }),
            "current_price": forms.NumberInput(attrs={
                    "class": "form-control",
                    "placeholder": "Enter current price",
                    "step": "0.01",
                    "min": "0",
                }),
            "start_time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "class": "form-control time-input",
                    "placeholder": "HH:MM",
                    "autocomplete": "off",                      # switches off the "autocomplete" suggestion
                    "maxlength": "5",
                    "inputmode": "numeric",
                }
            ),
            "end_time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "class": "form-control time-input",
                    "placeholder": "HH:MM",
                    "autocomplete": "off",
                    "maxlength": "5",
                    "inputmode": "numeric",
                }),
            "seller": forms.Select(attrs={
                    "class": "form-select",
                }),
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["seller"].queryset = User.objects.filter(role=User.Role.SELLER)
        self.fields["start_time"].input_formats = ["%H:%M"]
        self.fields["end_time"].input_formats = ["%H:%M"]

        # Line below ensures that only users whose role is SELLER are displayed in the seller dropdown.
        # L59: self.fields["seller"].queryset = User.objects.filter(role=User.Role.SELLER)
        # It filters the User records and prevents buyers or other types of users from being selected as the seller of an auction.

    def clean(self):
        cleaned_data = super().clean()
        base_price = cleaned_data.get("base_price")
        current_price = cleaned_data.get("current_price")
        if (base_price is not None and current_price is not None and current_price < base_price):
            raise forms.ValidationError("Current price cannot be lower than base price.")
        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("Auction title is required.")
        if len(title) < 3:
            raise forms.ValidationError("Auction title must contain at least 3 characters.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description:
            raise forms.ValidationError("Auction description is required.")
        return description

    def clean_base_price(self):
        base_price = self.cleaned_data.get("base_price")
        if base_price is None:
            raise forms.ValidationError("Base price is required.")
        if base_price <= 0:
            raise forms.ValidationError("Base price must be greater than zero.")
        return base_price

    def clean_current_price(self):
        current_price = self.cleaned_data.get("current_price")
        if current_price is None:
            raise forms.ValidationError("Current price is required.")
        if current_price <= 0:
            raise forms.ValidationError("Current price must be greater than zero.")
        return current_price

    def clean_start_time(self):
        start_time = self.cleaned_data.get("start_time")
        if not start_time:
            raise forms.ValidationError("Start time is required.")
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get("end_time")
        if not end_time:
            raise forms.ValidationError("End time is required.")
        start_time = self.cleaned_data.get("start_time")
        if start_time and end_time <= start_time:
            raise forms.ValidationError("End time must be later than start time.")
        return end_time

    def clean_seller(self):
        seller = self.cleaned_data.get("seller")
        if not seller:
            raise forms.ValidationError("Please select a seller.")
        if seller.role != User.Role.SELLER:
            raise forms.ValidationError("Selected user is not a seller.")
        return seller