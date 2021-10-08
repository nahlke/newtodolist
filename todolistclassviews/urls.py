from django.urls import path, re_path
from todolistclassviews import views
from django.contrib.auth import views as view
from todolistclassviews import forms

urlpatterns = [
    #homeseiten
    path('', views.HomereginPathClass.as_view(), name='homeregin'),
    path('hometodo', views.HomeToDoPathClass.as_view(), name='hometodo'),

    #registrierung/change pw
    path('registration', views.RegistrationClass.as_view(), name='registration'),
    path('login', view.LoginView.as_view(template_name="login.html", authentication_form=forms.UserLoginForm), name='login'),
    path('changepw', views.ChangePWClass.as_view(), name='changepw'),
    path('changeprofile/<int:pk>', views.ChangeProfileClass.as_view(), name='changeprofile'),

    #todogruppen/items
    path('alltodos', views.AllTodosClass.as_view(), name='alltodos'),
    path('grouplist', views.ToDoGroupsClass.as_view(), name='grouplist'),
    re_path(r'^todo/(?P<pk>\d+)$', views.ItemListClass.as_view(), name='itemlist'),

    #gruppen/items bearbeiten
    path('deletegroupall/<int:pk>', views.GroupDeleteAllClass.as_view(), name='deletegroupall'),
    path('deletegroup/<int:pk>', views.GroupDeleteClass.as_view(), name='deletegroup'),
    path('deleteitem/<int:pk>', views.ItemDeleteClass.as_view(), name='deleteitem'),
    path('update/<int:pk>', views.ItemUpdateClass.as_view(), name='update'),
    path('complete/<int:pk>', views.ItemCompleteClass.as_view(), name='complete'),
    path('updategroup/<int:pk>', views.GroupUpdateClass.as_view(), name='updategroup'),

    #globale todos
    path('global', views.GlobalItemClass.as_view(), name='global'),

    #share link
    path('share/<str:token>', views.ShareToDoClass.as_view(), name='share'),
    path('shareitem/<int:pk>', views.ShareLinkClass.as_view(), name='shareitem'),


]