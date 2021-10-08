from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import User

#--------------------------------------------------------------------------------
#Models für die Gruppen und die Items

#models/tabellenfelder für die ToDoGruppen
class ToDoGroupsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

#++++++++++++++++++

#function für random zeichenkette
def get_rendom_str():
    uniqe_id = get_random_string(length=32)
    return uniqe_id

#models/tabellenfelder für die Itemliste
class ItemModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ToDoGroupsModel, on_delete=models.CASCADE, max_length=15, null=True, blank=True, verbose_name='Gruppe')
    title = models.CharField(max_length=32, null=True)
    description = models.CharField(max_length=256, null=True)
    USER_CHOICE = (
        ('privat','privat'),
        ('global','global')
    )
    visibility = models.CharField(max_length=6, null=True, choices=USER_CHOICE, verbose_name='Status', default='privat')
    status = models.BooleanField(False, null=True)
    token = models.CharField(max_length=32, default=get_rendom_str)
    is_shared = models.BooleanField(verbose_name='Teilen', default=False)



