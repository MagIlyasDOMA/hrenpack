from django.db import models
from .lookup import DirnameLookup


class FilePathField(models.CharField):
    def __init__(self, *args, db_collation=None, **kwargs):
        super().__init__(*args, db_collation=db_collation, **kwargs)
        self.register_lookup(DirnameLookup)
