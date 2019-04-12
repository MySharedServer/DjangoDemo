from django.db import models

# Create your models here.


class FunctionInfo(models.Model):
    """
    This table is used to save function information
    """

    fileName = models.CharField(max_length=1000, blank=False, null=True)
    name = models.CharField(max_length=1000, blank=False, null=False)
    params = models.CharField(max_length=4000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    line = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        verbose_name = 'Function detail'
        verbose_name_plural = verbose_name
        ordering = ['fileName']
