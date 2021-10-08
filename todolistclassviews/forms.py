from django import forms
from django.forms import ModelForm
from .models import ItemModel, ToDoGroupsModel
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

#--------------------------------------------------------------------------------
#Registration/Login/Profile

#form Registrierung
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='')
    password1 = forms.CharField(label='', widget=forms.PasswordInput)
    password2 = forms.CharField(label='', widget=forms.PasswordInput)
    username = forms.CharField(label='')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

#++++++++++++++++++
#form Login
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id':''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':''}))

#++++++++++++++++++
#form Profiel Daten ändern
class ChangeProfilForm(forms.ModelForm):
    username = forms.CharField(label='')
    first_name = forms.CharField(label='')
    last_name = forms.CharField(label='')
    email = forms.EmailField(label='')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]

#--------------------------------------------------------------------------------
#ToDoGroups

#form ToDoGruppen
class ToDoGroupsForm(ModelForm):
    name = forms.CharField(max_length=200, label='Neue ToDo-Liste')
    class Meta:
        model = ToDoGroupsModel
        fields = [
            'name'
        ]

#form bearbeiten der Gruppen
class EditGroupsForm(ModelForm):
    name = forms.CharField(label='Neuer Titel')
    class Meta:
        model = ToDoGroupsModel
        fields = [
            "name"
        ]

#--------------------------------------------------------------------------------
#ToDoItems

#form ToDoItems
class ItemForm(ModelForm):
    title = forms.CharField(label='Titel')
    description = forms.CharField(label='Beschreibung')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ItemForm,self).__init__(*args, **kwargs)
        self.fields['group'].queryset = ToDoGroupsModel.objects.filter(user=user)

    class Meta:
        model = ItemModel
        fields = [
            "title",
            "description",
            "group",
            "visibility",
            "is_shared"
        ]

