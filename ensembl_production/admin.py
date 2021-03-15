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
from django import forms
from django.contrib import admin
# Unregister the provided model admin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from fernet_fields import EncryptedCharField

from ensembl.production.djcore.admin import ProductionUserAdminMixin, SuperUserAdmin
from .models import ProductionFlaskApp, Credentials


@admin.register(ProductionFlaskApp)
class FlaskAppAdmin(ProductionUserAdminMixin, SuperUserAdmin):
    list_display = ('app_name', 'app_url', 'app_url_link', 'app_is_framed', 'img_url', 'app_theme_color')
    readonly_fields = ('img_url',
                       'app_theme_color', 'app_url_link', 'created_by', 'created_at', 'modified_at',
                       'modified_by')
    fields = ('app_name', 'app_prod_url', 'app_url_link',
              'app_is_framed', 'app_url',
              'app_config_params',
              'app_theme',
              ('created_by', 'created_at'),
              ('modified_by', 'modified_at'))

    formfield_overrides = {
        jsonfield.JSONField: {'widget': jsonfield.fields.JSONWidget(attrs={'rows': 20, 'cols': 70,
                                                                            'class': 'vLargeTextField'})},
    }

    def app_theme_color(self, obj):
        return mark_safe(u"<div class='admin_app_theme_color' style='background:#" + obj.app_theme + "'/>")

    def app_url_link(self, obj):
        if obj.app_prod_url:
            url_view = reverse('production_app_view', kwargs={'app_prod_url': obj.app_prod_url})
            return mark_safe(u"<a href='" + url_view + "' target='_blank'>" + obj.app_prod_url + "</a>")
        else:
            return "N/A"

    def img_url(self, obj):
        return obj.img_admin_tag

    img_url.short_description = 'App Logo'
    img_url.allow_tags = True


admin.site.unregister(User)


@admin.register(Credentials)
class CredentialsAdmin(admin.ModelAdmin, SuperUserAdmin):
    formfield_overrides = {
        EncryptedCharField: {'widget': forms.widgets.PasswordInput},
    }