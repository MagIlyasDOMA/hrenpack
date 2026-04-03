from django.db import models
from .lookup import DirnameLookup


class FilePathField(models.CharField):
    pass


FilePathField.register_lookup(DirnameLookup)
