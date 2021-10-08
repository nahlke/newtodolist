from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from todolistclassviews import models
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from todolistclassviews import forms

User = get_user_model()

#--------------------------------------------------------------------------------
#Links/Path

#++++++++++++++++++
#Path
class HomereginPathClass(generic.TemplateView):
    template_name = 'registration/homeregin.html'

class HomeToDoPathClass(generic.TemplateView):
    template_name = 'todolist/show/hometodo.html'

#--------------------------------------------------------------------------------
#Registrierung/PW/Profile

#++++++++++++++++++
#Registration
class RegistrationClass(SuccessMessageMixin, generic.CreateView):
    template_name = "registration/registration.html"
    form_class = forms.RegistrationForm
    success_url = "/login"
    success_message = "User wurde erfolgreich Registriert"

#++++++++++++++++++
#ChangePW
class ChangePWClass(SuccessMessageMixin, PasswordChangeView):
    template_name = 'todolist/edit/changepw.html'
    form_class = PasswordChangeForm
    success_url = 'hometodo'
    success_message = "Passwort erfolgreich geändert"

#++++++++++++++++++
#ChangeProfile
class ChangeProfileClass(SuccessMessageMixin, generic.UpdateView):
    template_name = 'todolist/edit/changeprofile.html'
    model = User
    form_class = forms.ChangeProfilForm
    success_url = '../hometodo'
    success_message = "Profiel erfolgreich geändert"

#--------------------------------------------------------------------------------
#Alle Todos anzeigen

#++++++++++++++++++
#Alle Todos
class AllTodosClass(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView, generic.ListView):
    template_name = 'todolist/show/alltodos.html'
    model = models.ItemModel
    form_class = forms.ItemForm
    context_object_name = 'items'
    success_url = 'alltodos'
    success_message = "ToDo wurde erstellt"

    def get_form_kwargs(self):
        kwargs = super(AllTodosClass,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save
        form.instance.user = self.request.user
        return super().form_valid(form)

#--------------------------------------------------------------------------------
#ToDoGroup erstellen/bearbeiten

#++++++++++++++++++
#GroupList
class ToDoGroupsClass(SuccessMessageMixin, generic.CreateView, generic.ListView, LoginRequiredMixin):
    template_name = 'todolist/show/todos.html'
    model = models.ToDoGroupsModel
    form_class = forms.ToDoGroupsForm
    context_object_name = 'todos'
    success_url = 'grouplist'
    success_message = "Gruppe wurde erstellt"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#++++++++++++++++++
#GroupDelete + ToDosDelete
class GroupDeleteAllClass(SuccessMessageMixin, generic.DeleteView):
    template_name = 'todolist/edit/groupdeleteall.html'
    model = models.ToDoGroupsModel
    success_url = '../grouplist'

    def form_valid(self, form):
        messages.error(self.request, 'Gruppe und dazugehörige ToDos wurden gelöscht')
        return super().form_valid(form)

#++++++++++++++++++
#GroupDelete
class GroupDeleteClass(SuccessMessageMixin, generic.DeleteView):
    template_name = 'todolist/edit/groupdelete.html'

    def get_object(self):
        group_pk = self.kwargs['pk']
        group = get_object_or_404(models.ToDoGroupsModel, pk=group_pk)
        item_manager = models.ItemModel.objects.filter(group=group.pk)
        for obj in item_manager:
            obj.group = None
            obj.save()
        return group

    model = models.ToDoGroupsModel
    success_url = '../grouplist'

    def form_valid(self, form):
        messages.error(self.request, 'Gruppe wurde gelöscht')
        return super().form_valid(form)

#++++++++++++++++++
#GroupUpdate
class GroupUpdateClass(SuccessMessageMixin, generic.UpdateView):
    template_name = 'todolist/edit/update.html'
    model = models.ToDoGroupsModel
    form_class = forms.EditGroupsForm
    success_url = '../grouplist'
    success_message = "Gruppe wurde bearbeitet"

#--------------------------------------------------------------------------------
#ToDoItems erstellen/bearbeiten

#++++++++++++++++++
#ItemList
class ItemListClass(generic.ListView):
    template_name = 'todolist/show/items.html'
    def get_queryset(self):
        group_pk = self.kwargs['pk']
        group = get_object_or_404(models.ToDoGroupsModel, pk=group_pk)
        item_manager = models.ItemModel.objects.filter(group=group.pk)
        return item_manager
    context_object_name = 'items'

#++++++++++++++++++
#ItemDelete
class ItemDeleteClass(SuccessMessageMixin, generic.DeleteView):
    template_name = 'todolist/edit/delete.html'
    model = models.ItemModel
    success_url = '../alltodos'

    def form_valid(self, form):
        messages.error(self.request, 'ToDo wurde gelöscht')
        return super().form_valid(form)

#++++++++++++++++++
#ItemUpdate
class ItemUpdateClass(SuccessMessageMixin, generic.UpdateView):
    template_name = 'todolist/edit/update.html'
    model = models.ItemModel
    form_class = forms.ItemForm
    success_url = '../alltodos'
    success_message = "ToDo wurde bearbeitet"

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateClass,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object.user = self.request.user
        self.object.save
        return super().form_valid(form)

#++++++++++++++++++
#ItemComplete
class ItemCompleteClass(SuccessMessageMixin, generic.UpdateView):
    template_name = 'todolist/edit/complete.html'
    model = models.ItemModel
    fields = ['status']
    success_url = '../alltodos'
    success_message = "Status wurde bearbeitet"

#--------------------------------------------------------------------------------
#Globale Todos

#++++++++++++++++++
#GlobalItemList
class GlobalItemClass(generic.ListView):
    template_name = 'todolist/show/global.html'
    model = models.ItemModel
    context_object_name = 'items'

#--------------------------------------------------------------------------------
#Share Todos

#++++++++++++++++++
#ToDos Sharen
class ShareToDoClass(generic.ListView):
    template_name = 'todolist/show/shared.html'
    def get_queryset(self):
        item_token = self.kwargs['token']
        item = get_object_or_404(models.ItemModel, token=item_token)
        return item
    context_object_name = 'item'

#++++++++++++++++++
#Share Link
class ShareLinkClass(generic.DetailView):
    template_name = 'todolist/edit/getsharelink.html'
    def get_queryset(self):
        item_pk = self.kwargs['pk']
        item = get_object_or_404(models.ItemModel, pk=item_pk)
        item_manager = models.ItemModel.objects.filter(token=item.token)
        return item_manager
    context_object_name = 'item'
