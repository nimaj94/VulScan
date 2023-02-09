import re
import uuid

from django.db import models
from rest_framework.exceptions import ValidationError


def full_domain_validator(hostname):
    HOSTNAME_LABEL_PATTERN = re.compile("(?!-)[A-Z\d-]+(?<!-)$", re.IGNORECASE)
    if not hostname:
        return
    if len(hostname) > 255:
        raise ValidationError("The domain name cannot be composed of more than 255 characters.")
    if hostname[-1:] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    for label in hostname.split("."):
        if len(label) > 63:
            raise ValidationError(f"The label '{label}' is too long (maximum is 63 characters).")
        if not HOSTNAME_LABEL_PATTERN.match(label):
            raise ValidationError(f"Unallowed characters in label '{label}'.")


class Website(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain = models.CharField('domain', max_length=255, validators=[full_domain_validator], unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    FINISHED = 1
    ONGOING = 2
    ERROR = 3
    STATUS_CHOICES = (
        (FINISHED, 'finished'),
        (ONGOING, 'ongoing'),
        (ERROR, 'error'),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ONGOING)


class Subdomain(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    subdomain_name = models.CharField('subdomain_name', max_length=255)
    result = models.TextField('result')
    ip_address = models. GenericIPAddressField(null=True)
