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
import re
from django.views.generic import DetailView

from ensembl.production.webhelp.models import HelpRecord


# Create your views here.
class HelpRecordPreview(DetailView):
    queryset = HelpRecord.objects.all()
    http_method_names = ['get']
    template_name_suffix = "_preview"
    # template_name = "admin/ensembl_website/help_preview.html"
    pk_url_kwarg = 'object_id'
    content_field = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_popup'] = True
        context['json_data'] = json.loads(self.object.data)
        replaced = re.sub(r'(\[\[IMAGE::([a-zA-Z0-9._-]+)( width=\\?"([0-9]+)\\?" height=\\?"([0-9]+)\\?")?\]\])',
                          r"<img src='https://raw.githubusercontent.com/Ensembl/ensembl-webcode/main/htdocs/img/help/\2' width='\4' height='\5'/>",
                          self.object.data)
        context['json_data'] = json.loads(replaced)
        context['displayed'] = context['json_data'][self.content_field]
        return context


class FaqItemPreview(HelpRecordPreview):
    content_field = "answer"


class MovieItemPreview(HelpRecordPreview):
    content_field = "title"


class ViewItemPreview(HelpRecordPreview):
    content_field = "content"


class LookupItemPreview(HelpRecordPreview):
    content_field = "meaning"
