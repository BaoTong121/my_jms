from django.db import models
from django.db import models


class User(models.Model):
    class Meta:
        db_table = 'user'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, null=False)
    email = models.EmailField(max_length=40, null=False, unique=True)
    password = models.CharField(max_length=128, null=False)

    def __repr__(self):
        return "{}{}".format(self.id, self.name)
    __str__ = __repr__