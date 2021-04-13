#   See the NOTICE file distributed with this work for additional information
#   regarding copyright ownership.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import json

from django.contrib import admin
from django.utils.safestring import mark_safe

from ensembl.production.djcore.admin import ProductionUserAdminMixin

from ensembl.production.webhelp.forms import WebSiteRecordForm, LookupItemForm, MovieForm, FaqForm, ViewForm
from ensembl.production.webhelp.models import *


class HelpLinkInline(admin.TabularInline):
    model = HelpLink


class HelpLinkModelAdmin(admin.ModelAdmin):
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff


class HelpRecordModelAdmin(ProductionUserAdminMixin):
    list_per_page = 50
    readonly_fields = (
        'help_record_id', 'created_by', 'created_at', 'modified_by', 'modified_at')
    ordering = ('-modified_at', '-created_at')
    list_filter = ['created_by', 'modified_by']

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff


@admin.register(HelpLink)
class HelpLinkItemAdmin(HelpLinkModelAdmin):
    form = WebSiteRecordForm
    list_display = ('page_url',)
    fields = ('page_url',)
    search_fields = ('page_url',)


@admin.register(MovieRecord)
class MovieItemAdmin(HelpRecordModelAdmin):
    form = MovieForm
    list_display = ('title', 'movie_id', 'youtube_id', 'youku_id', 'keyword', 'status')
    fields = ('title', 'help_record_id', 'youtube_id', 'youku_id', 'list_position', 'length', 'keyword', 'status',
              ('created_by', 'created_at'),
              ('modified_by', 'modified_at'))
    search_fields = ('data', 'keyword', 'status', 'help_record_id')

    def get_queryset(self, request):
        q = MovieRecord.objects.filter(type='movie')
        ordering = self.get_ordering(request)
        if ordering:
            q = q.order_by(*ordering)
        return q

    def title(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return raw_data.get('title')

    def youtube_id(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return raw_data.get('youtube_id')

    def youku_id(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return raw_data.get('youku_id')

    def save_model(self, request, obj, form, change):
        extra_field = {field: form.cleaned_data[field].replace('\n', '').replace('\r', '').replace('\t', '') for field
                       in form.fields if
                       field in ('title', 'list_position', 'youtube_id', 'youku_id', 'length')}
        obj.data = json.dumps(extra_field)
        super().save_model(request, obj, form, change)

    def movie_id(self, obj):
        return obj.help_record_id

    movie_id.short_description = 'Movie ID'
    movie_id.admin_order_field = 'help_record_id'


@admin.register(FaqRecord)
class FaqItemAdmin(HelpRecordModelAdmin):
    form = FaqForm
    list_display = ('question', 'category', 'keyword', 'status')
    fields = ('category', 'question', 'answer', 'keyword', 'status', 'division',
              ('created_by', 'created_at'),
              ('modified_by', 'modified_at'))
    search_fields = ('data', 'keyword', 'status')

    def get_queryset(self, request):
        q = FaqRecord.objects.filter(type='faq')
        ordering = self.get_ordering(request)
        if ordering:
            q = q.order_by(*ordering)
        return q

    def category(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return raw_data.get('category')

    def question(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return mark_safe(raw_data.get('question'))

    def save_model(self, request, obj, form, change):
        extra_field = {field: form.cleaned_data[field].replace('\n', '').replace('\r', '').replace('\t', '') for field
                       in form.fields if
                       field in ('category', 'question', 'answer')}
        extra_field.update({'division': form.cleaned_data['division']})
        obj.data = json.dumps(extra_field)
        super().save_model(request, obj, form, change)


@admin.register(ViewRecord)
class ViewItemAdmin(HelpRecordModelAdmin):
    form = ViewForm
    list_display = ('page_url', 'keyword', 'status')
    fields = ('help_link', 'content', 'keyword', 'status',
              ('ensembl_action', 'ensembl_object'),
              ('created_by', 'created_at'),
              ('modified_by', 'modified_at'))
    search_fields = ('data', 'keyword', 'status', 'helplink__page_url')

    def get_queryset(self, request):
        q = ViewRecord.objects.filter(type='view')
        ordering = self.get_ordering(request)
        if ordering:
            q = q.order_by(*ordering)
        return q

    def ensembl_action(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return raw_data.get('ensembl_action', "")

    def ensembl_object(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return raw_data.get('ensembl_object', "")

    def page_url(self, obj):
        if obj:
            q = HelpLink.objects.filter(help_record_id=obj.help_record_id).first()
            if q:
                return q.page_url

    def save_model(self, request, obj, form, change):
        extra_field = {field: form.cleaned_data[field].replace('\n', '').replace('\r', '').replace('\t', '') for field
                       in form.fields if field in ('content', 'ensembl_action', 'ensembl_object') if
                       form.cleaned_data.get(field, False)}
        obj.data = json.dumps(extra_field)
        super().save_model(request, obj, form, change)
        q = HelpLink.objects.filter(help_record_id=obj.pk).first()
        if not q:
            HelpLink.objects.create(page_url=form.cleaned_data['help_link'], help_record_id=obj.pk)

    page_url.admin_order_field = 'helplink__page_url'
    page_url.short_description = 'Help Links'


@admin.register(LookupRecord)
class LookupItemAdmin(HelpRecordModelAdmin):
    form = LookupItemForm
    list_display = ('word', 'meaning', 'keyword', 'status')
    fields = ('word', 'expanded', 'meaning', 'keyword', 'status',
              ('created_by', 'created_at'),
              ('modified_by', 'modified_at'))
    search_fields = ('data', 'keyword', 'status')

    def get_queryset(self, request):
        q = LookupRecord.objects.filter(type='lookup')
        ordering = self.get_ordering(request)
        if ordering:
            q = q.order_by(*ordering)
        return q

    def word(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return raw_data.get('word')

    def meaning(self, obj):
        if obj:
            raw_data = json.loads(obj.data)
            return mark_safe(raw_data.get('meaning'))

    def save_model(self, request, obj, form, change):
        extra_field = {field: form.cleaned_data[field].replace('\n', '').replace('\r', '').replace('\t', '') for field
                       in form.fields if
                       field in ('word', 'expanded', 'meaning')}
        obj.data = json.dumps(extra_field)
        super().save_model(request, obj, form, change)
