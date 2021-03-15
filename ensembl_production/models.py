# -*- coding: utf-8 -*-
"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import jsonfield
from django.contrib.auth.models import Group
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ValidationError
from django.db import models
from django.db.utils import ConnectionHandler, ConnectionRouter
from django.utils.safestring import mark_safe
from fernet_fields import EncryptedCharField

from ensembl.production.djcore.models import BaseTimestampedModel

connections = ConnectionHandler()
router = ConnectionRouter()
NOT_PROVIDED = object()


class ProductionFlaskApp(BaseTimestampedModel):
    class Meta:
        db_table = 'flask_app'
        app_label = 'ensembl_production'
        verbose_name = 'Production App'
        verbose_name_plural = 'Production Apps'

    def __str__(self):
        return self.app_name

    color_theme = (
        ('336', 'Ensembl'),
        ('707080', 'Bacteria'),
        ('714486', 'Protists'),
        ('407253', 'Plants'),
        ('725A40', 'Fungi'),
        ('015365', 'Metazoa'),
        ('800066', 'Datachecks')
    )

    # TODO add menu organisation
    app_id = models.AutoField(primary_key=True)
    app_name = models.CharField("App display name", max_length=255, null=False)
    app_is_framed = models.BooleanField('Display app in iframe', default=True, null=True, help_text='Need an url then')
    app_url = models.URLField("App flask url", max_length=255, null=True, blank=True)
    app_theme = models.CharField(max_length=6, default='FFFFFF', choices=color_theme)
    app_groups = models.ManyToManyField(Group, blank=True)
    app_prod_url = models.CharField('App Url', max_length=200, null=False, unique=True)
    app_config_params = jsonfield.JSONField('Configuration parameters', null=True, blank=True)

    @property
    def img(self):
        if finders.find('img/' + self.app_prod_url.split('-')[0] + ".png"):
            return u'img/' + self.app_prod_url.split('-')[0] + ".png"
        else:
            return u'img/logo_industry.png'

    @property
    def img_admin_tag(self):
        return mark_safe(u"<img class='admin_app_logo' src='" + static(self.img) + "'/>")

    def clean(self):
        super().clean()
        if self.app_is_framed and not self.app_url:
            raise ValidationError('You must set url if app is iframed')


class Credentials(models.Model):
    class Meta:
        app_label = 'ensembl_production'
        verbose_name = 'Credential'
        verbose_name_plural = 'Credentials'

    cred_id = models.AutoField(primary_key=True)
    cred_name = models.CharField("Name", unique=True, max_length=150)
    cred_url = models.CharField("Access Url", max_length=255)
    user = models.CharField("User Name", max_length=100)
    credentials = EncryptedCharField("Password", max_length=255)

    def __str__(self):
        return self.cred_name


