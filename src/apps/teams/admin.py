# src/apps/teams/admin.py
from django.contrib import admin

from .models import Team, TeamInvite, TeamMember

# @admin.registerはadminのみが管理者画面に入れるという意味。

# teamの新規登録
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "member_count", "max_members", "rank", "total_points", "created_at")
    search_fields = ("name",)
    list_filter = ("rank",)
    raw_id_fields = ("owner",)

# teamへの招待
@admin.register(TeamInvite)
class TeamInviteAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "code", "is_active", "expires_at", "created_at")
    search_fields = ("code",)
    list_filter = ("is_active",)
    raw_id_fields = ("team",)

# team memberの登録
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "user", "joined_at")
    raw_id_fields = ("team", "user")
