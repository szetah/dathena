from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Confidentiality(models.Model):
    """
    A table store document confidentiality

    @Ryan, 29.10.2018
    """
    name = models.CharField(_('Name'), max_length=255)
    short_name = models.CharField(_('Short Name'), unique=True, max_length=255)
    authority_level = models.PositiveSmallIntegerField(_("Authority"), default=1)
    total_docs = models.IntegerField(_("Total Docs"), default=0)

    class Meta:
        verbose_name = _("Confidentiality")
        verbose_name_plural = _("Confidentiality")

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    A table store languages

    @Ryan, 29.10.2018
    """
    name = models.CharField(_('Name'), max_length=255)
    short_name = models.CharField(_('Short Name'), unique=True, max_length=255)
    total_docs = models.IntegerField(_("Total Docs"), default=0)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return self.name


class DocumentType(models.Model):
    """
    A table store document type

    @Ryan, 29.10.2018
    """
    name = models.CharField(_('Name'), max_length=255)
    short_name = models.CharField(_('Short Name'), unique=True, max_length=255)
    total_docs = models.IntegerField(_("Total Docs"), default=0)

    class Meta:
        verbose_name = _("Document Type")
        verbose_name_plural = _("Document Types")

    def __str__(self):
        return self.name


class Document(TimeStampedModel):
    """
    A table store uploaded document with descriptions such as confidentiality, langauges and document type.

    @Ryan, 29.10.2018
    """
    confidentiality = models.ForeignKey(Confidentiality, related_name='doc_condifentuality', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='doc_langauge', on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, related_name='doc_documenttype', on_delete=models.CASCADE)
    file = models.FileField(
        verbose_name=_("Document"),
        upload_to='uploads/',
        max_length=255
    )
    user = models.ForeignKey(
        User,
        related_name='doc_user',
        on_delete=models.CASCADE
    )
    tags = ArrayField(models.CharField(max_length=100), blank=True)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    @property
    def filename(self):
        return self.get_file_name()

    def get_file_name(self):
        try:
            return self.document.name.split('/')[-1]
        except Exception:
            return self.document.name

    def save(self, *args, **kwargs):
        """
        Override save() to set confidentiality, document_type and language into tags

        Ryan, 30.10.2018
        """
        for short_name_tag in [
            self.confidentiality.short_name,
            self.language.short_name,
            self.document_type.short_name,
        ]:
            if short_name_tag not in self.tags:
                self.tags.append(short_name_tag)
        super().save(*args, **kwargs)
