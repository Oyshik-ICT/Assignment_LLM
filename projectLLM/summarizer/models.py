# summarizer/models.py

from django.db import models

class PropertySummary(models.Model):
    property_id = models.IntegerField(primary_key=True)
    summary = models.TextField()

    def __str__(self):
        return f"Summary for Property {self.property_id}"

