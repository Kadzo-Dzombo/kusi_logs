from django import forms

from .models import Yard, Reference, Container, Invoice, InvoiceItem, Inquiry

from django.forms import ModelForm, TextInput, Select, DateInput, NumberInput, Textarea
from django.forms.models import inlineformset_factory

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# =========================================================
# LOGIN FORM
# =========================================================

class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autocomplete': 'username'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'autocomplete': 'current-password'
            }
        )
    )


# =========================================================
# REGISTER FORM
# =========================================================

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

        widgets = {

            'username': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username',
                    'autocomplete': 'username'
                }
            ),

            'email': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address',
                    'autocomplete': 'email'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        })


# =========================================================
# YARD FORM
# =========================================================

class YardForm(ModelForm):

    class Meta:
        model = Yard
        fields = ['name', 'location']

        widgets = {

            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter yard name')
                }
            ),

            'location': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter yard location')
                }
            ),
        }


# =========================================================
# REFERENCE FORM
# =========================================================

class ReferenceForm(ModelForm):

    class Meta:
        model = Reference
        fields = ['reference_no', 'yard']

        widgets = {

            'reference_no': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter reference no')
                }
            ),

            'yard': Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }


# =========================================================
# CONTAINER FORM
# =========================================================

class ContainerForm(ModelForm):

    class Meta:
        model = Container

        fields = [
            'reference',
            'container_no',
            'size',
            'status',
            'client_name',
            'phone_number',
            'date'
        ]

        widgets = {

            'reference': Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'container_no': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter container no')
                }
            ),

            'size': Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'status': Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'client_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter client name')
                }
            ),

            'phone_number': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter phone number')
                }
            ),

            'date': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter date')
                }
            )
        }



class InvoiceForm(ModelForm):

    class Meta:

        model = Invoice

        fields = [
            'invoice_no',
            'date',
            'company_name',
            'address',
            'phone_no',
            'email_address',
            'attention',
            'amount_in_words',
            'bill_of_sale',
            'delivery',
            'authorised_signature',
            'buyer_acknowledgement',
            'buyer_signature',
        ]

        widgets = {

            'invoice_no': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter invoice number'
                }
            ),

            'date': DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'company_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter company name'
                }
            ),

            'address': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter address'
                }
            ),

            'phone_no': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),

            'email_address': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),

            'attention': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Attention'
                }
            ),

            'amount_in_words': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Amount in words'
                }
            ),

            'bill_of_sale': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Bill of sale'
                }
            ),

            'delivery': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Delivery details'
                }
            ),

            'authorised_signature': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Authorised signature'
                }
            ),

            'buyer_acknowledgement': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Buyer acknowledgement'
                }
            ),

            'buyer_signature': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Buyer signature'
                }
            ),
        }


# =========================================================
# INVOICE ITEM FORM
# =========================================================

class InvoiceItemForm(ModelForm):

    class Meta:

        model = InvoiceItem

        fields = [
            'ser_no',
            'quantity',
            'unit_price',
        ]

        widgets = {

            'ser_no': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Serial No.'
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Quantity',
                    'step': '0.01',
                    'min': '0'
                }
            ),

            'unit_price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Unit Price',
                    'step': '0.01',
                    'min': '0'
                }
            ),
        }


# =========================================================
# INVOICE ITEM FORMSET
# =========================================================

InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True
)


class InquiryForm(forms.ModelForm):
    """Used by the public homepage contact form."""

    class Meta:
        model = Inquiry
        fields = ['full_name', 'email', 'container_type', 'delivery_location', 'notes']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'john@company.com'}),
            'delivery_location': forms.TextInput(
                attrs={'placeholder': 'e.g. Port of Mombasa / 80100'}
            ),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Mention required quantity, offloading constraints, '
                               'or special modifications...',
            }),
        }

