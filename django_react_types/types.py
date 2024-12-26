from django.db import models

FIELD_TYPE_MAPPING = {
    models.CharField: "string",
    models.IntegerField: "number",
    models.BooleanField: "boolean",
    models.DateTimeField: "string",
    models.DateField: "string",
    models.TextField: "string",
    models.FloatField: "number",
    models.DecimalField: "number",
    models.ForeignKey: "string",  # You may want to handle relationships differently
    models.ManyToManyField: "string[]",  # Similar handling for many-to-many relationships
    # Add other mappings here
}
