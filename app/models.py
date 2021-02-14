import uuid as uuid
from django.db import models

# Create your models here.
def get_uuid():
    return uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()))