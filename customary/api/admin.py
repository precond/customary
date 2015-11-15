from django.contrib import admin

from customary.api.models import ApiUser, ApiToken


admin.site.register(ApiUser)
admin.site.register(ApiToken)
