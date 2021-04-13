# See the NOTICE file distributed with this work for additional information
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
from django import forms

from ensembl.production.webhelp.models import DIVISION_CHOICES, HelpLink

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
