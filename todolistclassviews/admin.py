from django.contrib import admin
from .models import ItemModel, ToDoGroupsModel

admin.site.register(ToDoGroupsModel)
admin.site.register(ItemModel)
