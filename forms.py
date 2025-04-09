from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Note, User  # Import our custom User model

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address'
    }))

    class Meta:
        model = User  # Using our custom User model
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):  # Fixed __init__
        super().__init__(*args, **kwargs)
        # Add placeholders and class attributes
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'form-control'
    }))

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Note title',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your note here...',
                'class': 'form-control',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):  # Fixed __init__
        super().__init__(*args, **kwargs)

# Separate YourNoteForm class (outside of NoteForm class)
class YourNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Note title',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your note here...',
                'class': 'form-control',
                'rows': 5
            }),
        }
 
        # You can add additional initialization here if needed