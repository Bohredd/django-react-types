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
    models.AutoField: "number", # id 
    models.PositiveIntegerField: "number",
    models.PositiveSmallIntegerField: "number",
    models.EmailField: "string",
    models.PositiveBigIntegerField: "number",
    models.BinaryField: "string",
    models.BigAutoField: "number",
    models.BigIntegerField: "number",
    models.DurationField: "string",
    models.GenericIPAddressField: "string",
    models.IPAddressField: "string",
    models.SmallIntegerField: "number",
    models.SlugField: "string",
    models.TimeField: "string",
    models.URLField: "string",
    models.UUIDField: "string",
    models.FileField: "string",
    models.ImageField: "string",
    models.FilePathField: "string",
    models.JSONField: "string",
    models.NullBooleanField: "boolean",
    models.SmallAutoField: "number",
    models.SmallIntegerField: "number",
    models.TimeField: "string",
}
