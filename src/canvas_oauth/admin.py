from django.contrib import admin

from canvas_oauth.models import CanvasOAuth2Token


@admin.register(CanvasOAuth2Token)
class CanvasOAuth2TokenAdmin(admin.ModelAdmin):
    list_display = ["user", "created_on", "updated_on", "expires"]
    search_fields = ["user__username", "user__email"]
    # Tokens only come from the OAuth flow; the admin is for viewing and deleting
    exclude = ["access_token", "refresh_token"]
    readonly_fields = ["user", "expires", "created_on", "updated_on"]

    def has_add_permission(self, request):
        return False
