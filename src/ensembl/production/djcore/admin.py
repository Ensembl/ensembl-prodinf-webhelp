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
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class ProductionUserAdminMixin(admin.ModelAdmin):
    """
    Mixin class to associated request user to integer ID in another database host
    Allow cross linking within multiple database
    Warning: Do not check for foreign key integrity across databases
    """
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at')

    class Media:
        css = {
            'all': ('css/production_admin.css',)
        }

    def save_model(self, request, obj, form, change):
        if change:
            if form.changed_data:
                obj.modified_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class SuperUserAdmin:
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return request.user.is_superuser


class CustomUserAdmin(UserAdmin, SuperUserAdmin):
    actions = ['deactivate_users', ]

    def has_delete_permission(self, request, obj=None):
        return False

    def deactivate_users(self, request, queryset):
        cnt = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(request, 'Deactivated {} users.'.format(cnt))

    deactivate_users.short_description = 'Deactivate Users'
