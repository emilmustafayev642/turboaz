from django import forms

from .models import (
    Listing,
    Brand,
    CarModel,
    Year,
    Profile,
    EmailVerification,
    CarModelBodyType,
    CarGeneration,
)

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)


class MultipleImageField(forms.ImageField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            if not data:
                return super().clean(None, initial)
            cleaned_images = []
            for image in data:
                cleaned_images.append(super().clean(image, initial))
            return cleaned_images
        return [super().clean(data, initial)]


class ListingForm(forms.ModelForm):
    photos = MultipleImageField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model_id = self.data.get('car_model') if self.is_bound else None
        if not model_id and self.instance and self.instance.pk:
            model_id = self.instance.car_model_id

        body_type_choices = [('', 'Əvvəlcə model seçin')]
        if model_id:
            body_type_choices.extend(
                (option.body_type, option.get_body_type_display())
                for option in CarModelBodyType.objects.filter(
                    car_model_id=model_id
                ).order_by('body_type')
            )
        self.fields['body_type'].choices = body_type_choices

    def clean_description(self):
        desc = self.cleaned_data.get('description', '')
        sentences = [s for s in desc.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        if len(sentences) < 2 and len(desc.split()) < 10:
            raise forms.ValidationError("Avtomobil haqqında ən azı 2 cümlə məlumat yazmalısınız!")
        return desc

    class Meta:
        model = Listing
        fields = [
            'car_model',
            'year',
            'condition',
            'body_type',
            'fuel_type',
            'price',
            'mileage',
            'city',
            'description',
            'phone_number',
            'generation',
            'is_damaged',
            'is_repainted'
        ]

        labels = {
            'mileage': 'Yürüş',
            'condition': 'Vəziyyəti',
            'body_type': 'Ban növü',
            'price': 'Qiymət',
            'city': 'Şəhər',
            'description': 'Təsvir',
            'phone_number': 'Elaqe Nomresi',
            'fuel_type': 'Yanacaq növü',
            'generation': 'Nesil',
        }

        widgets = {
            'car_model': forms.HiddenInput(),
            'year': forms.HiddenInput(),
            'condition': forms.Select(attrs={'class': 'listing-control'}),
            'body_type': forms.Select(attrs={'class': 'listing-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'listing-control',
                'placeholder': 'Qiymət',
            }),

            'description': forms.Textarea(attrs={
                'class': 'listing-control listing-description',
                'rows': 4,
                'placeholder': 'Elan haqqında məlumat yazın',
            }),

            'phone_number': forms.TextInput(attrs={
             'class': 'listing-control',
             'placeholder': '+994 (__) ___-__-__',
             'type': 'tel',
            }),

            'fuel_type': forms.Select(attrs={'class': 'listing-control'}),
            'generation': forms.Select(attrs={'class': 'listing-control'})
        }

    def clean_year(self):
        year = self.cleaned_data['year']
        if not Year.objects.filter(year=year).exists():
            raise forms.ValidationError('Choose a year from the available list.')
        return year

    def clean_photos(self):
        photos = self.cleaned_data['photos']
        if len(photos) < 3:
            raise forms.ValidationError('Upload at least 3 photos.')
        return photos


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=30)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['username'].widget.attrs['autocomplete'] = 'username'
        self.fields['email'].widget.attrs['autocomplete'] = 'email'
        self.fields['phone'].widget.attrs['autocomplete'] = 'tel'
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        user_model = get_user_model()

        if user_model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email

        
# this part was hart bro it required some rearching


