from django.db import models
from common.models.base_model import BaseModel

class Gender(BaseModel):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name