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

from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.utils.safestring import mark_safe

from ensembl.production.djcore.admin import ProductionUserAdminMixin
from ensembl.production.webhelp.models import *


class HelpLinkInline(admin.TabularInline):
    model = HelpLink


class WebSiteRecordForm(forms.ModelForm):
    class Meta:
        exclude = ('type', 'data')


class LookupItemForm(WebSiteRecordForm):
    word = forms.CharField(label='Word')
    keyword = forms.CharField(widget=forms.Textarea({'rows': 3}))
    expanded = forms.CharField(label='Expanded', required=False, widget=forms.Textarea({'rows': 3}))
    meaning = forms.CharField(label='Meaning', widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        # Populate the form with fields from the data object.
        # Only for update
        if 'instance' in kwargs and kwargs['instance'] is not None:
            if 'initial' not in kwargs:
                kwargs['initial'] = {}
                data = json.loads(kwargs['instance'].data)
                kwargs['initial'].update(
                    {'word': data.get('word', ""), 'meaning': data.get('meaning', ""),
                     'expanded': data.get('expanded', "")})
        super(LookupItemForm, self).__init__(*args, **kwargs)


class MovieForm(WebSiteRecordForm):
    title = forms.CharField(label="Title")
    list_position = forms.CharField(label="List Position", required=False)
    youtube_id = forms.CharField(label="Youtube ID")
    youku_id = forms.CharField(label="Youku ID", required=False)
    length = forms.CharField(label="Length", required=False)
    keyword = forms.CharField(widget=forms.Textarea({'rows': 3}))

    def __init__(self, *args, **kwargs):
        # Populate the form with fields from the data object.
        # Only for update
        if 'instance' in kwargs and kwargs['instance'] is not None:
            if 'initial' not in kwargs:
                kwargs['initial'] = {}
                data = json.loads(kwargs['instance'].data)
                initial = {'title': data.get('title', ""), 'list_position': data.get('list_position', ""),
                           'youtube_id': data.get('youtube_id', ""), 'youku_id': data.get('youku_id', ""),
                           'length': data.get('length', "")}
                kwargs['initial'].update(initial)
        super(MovieForm, self).__init__(*args, **kwargs)


FAQ_CATEGORY = (
    ('archives', 'Archives'),
    ('genes', 'Genes'),
    ('assemblies', 'Genome assemblies'),
    ('comparative', 'Comparative genomics'),
    ('regulation', 'Regulation'),
    ('variation', 'Variation'),
    ('data', 'Export, uploads and downloads'),
    ('z_data', 'Other data'),
    ('core_api', 'Core API'),
    ('compara_api', 'Compara API'),
    ('compara', 'Compara'),
    ('variation_api', 'Variation API'),
    ('regulation_api', 'Regulation API'),
    ('web', 'Website'),
)


class FaqForm(WebSiteRecordForm):
    category = forms.CharField(label="Category", widget=forms.Select(choices=FAQ_CATEGORY))
    question = forms.CharField(label="Question", widget=CKEditorWidget())
    answer = forms.CharField(label="Answer", widget=CKEditorWidget())
    keyword = forms.CharField(widget=forms.Textarea({'rows': 3}))
    division = forms.MultipleChoiceField(label='Division specific', required=False,
                                         widget=forms.CheckboxSelectMultiple(), choices=DIVISION_CHOICES)

    def __init__(self, *args, **kwargs):
        # Populate the form with fields from the data object.
        # Only for update
        if 'instance' in kwargs and kwargs['instance'] is not None:
            if 'initial' not in kwargs:
                kwargs['initial'] = {}
                data = json.loads(kwargs['instance'].data)
                kwargs['initial'].update(
                    {'category': data.get('category', ""), 'question': data.get('question', ""),
                     'answer': data.get('answer', ""), 'division': data.get('division', "")})
        super(FaqForm, self).__init__(*args, **kwargs)


class ViewForm(WebSiteRecordForm):
    content = forms.CharField(label="Content", widget=CKEditorWidget())
    help_link = forms.CharField(label="Linked URLs")
    ensembl_action = forms.CharField(label="Ensembl Action", required=False)
    ensembl_object = forms.CharField(label="Ensembl Object", required=False)
    keyword = forms.CharField(widget=forms.Textarea({'rows': 3}))

    def __init__(self, *args, **kwargs):
        # Populate the form with fields from the data object.
        # Only for update
        if 'instance' in kwargs and kwargs['instance'] is not None:
            if 'initial' not in kwargs:
                kwargs['initial'] = {}
                help_link = HelpLink.objects.filter(help_record_id=kwargs['instance'].pk).first()
                data = json.loads(kwargs['instance'].data)
                kwargs['initial'].update(
                    {'content': data.get('content', ""), 'ensembl_action': data.get('ensembl_action', ""),
                     'ensembl_object': data.get('ensembl_object', ""), 'help_link': help_link.page_url})
                super(ViewForm, self).__init__(*args, **kwargs)
                self.fields['help_link'].widget.attrs['readonly'] = True
            else:
                super(ViewForm, self).__init__(*args, **kwargs)
        else:
            super(ViewForm, self).__init__(*args, **kwargs)


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
