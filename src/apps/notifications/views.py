# src/apps/notifications/views.py
from __future__ import annotations

from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .services import NotificationService


# -----------------------------
# Service accessor（quests と統一）
# -----------------------------
def _service() -> NotificationService:
    return NotificationService()


# -----------------------------
# Helpers（共通ガード）
# -----------------------------
def _get_my_team_id_or_none(user) -> Optional[int]:
    membership = getattr(user, "team_membership", None)
    return membership.team_id if membership else None


def _redirect_to_team_entry(request, reason: Optional[str] = None):
    if reason:
        messages.info(request, reason)
    return redirect("teams:join")


def _guard_team_mismatch(request, team_id: int) -> int:
    """
    - 未所属 → ValidationError ではなく redirect させたいので、ここでは例外にしない。
      呼び出し元で「未所属チェック」をしてから使う。
    - 所属不一致 → ValidationError
    """
    my_team_id = _get_my_team_id_or_none(request.user)
    if my_team_id is None:
        # 呼び出し元で先に弾く前提なので、ここに来たら想定外
        raise ValidationError({"team": "チームに所属していません"})

    if my_team_id != team_id:
        raise ValidationError({"permission": "あなたはこのチームの通知を閲覧できません。"})

    return my_team_id


# -----------------------------
# Views
# -----------------------------
@login_required
def notifications_index_view(request):
    """
    /notifications/ を開いた時に、自分のチームの通知一覧へ誘導する（footer用）
    """
    team_id = _get_my_team_id_or_none(request.user)
    if team_id is None:
        messages.info(request, "通知を見るには、まずチームに参加してください。")
        return redirect("teams:join")
    return redirect("notifications:list", team_id=team_id)


@login_required
def notification_list_view(request, team_id: int):
    my_team_id = _get_my_team_id_or_none(request.user)
    if my_team_id is None:
        return _redirect_to_team_entry(request, "通知を見るには、まずチームに参加してください。")

    try:
        _guard_team_mismatch(request, team_id)

        feed = _service().list_feed(team_id=team_id, user=request.user)
        return render(
            request,
            "notifications/list.html",
            {"feed": feed, "team_id": team_id},
        )

    except ValidationError:
        messages.error(request, "このページは閲覧できません。")
        return redirect("notifications:list", team_id=my_team_id)


@login_required
@require_POST
def notification_read_view(request, notification_id: int):
    my_team_id = _get_my_team_id_or_none(request.user)
    if my_team_id is None:
        return _redirect_to_team_entry(request, "通知を見るには、まずチームに参加してください。")

    try:
        _service().mark_read(notification_id=notification_id, user=request.user)
        return redirect("notifications:list", team_id=my_team_id)
    except ValidationError:
        messages.error(request, "既読化に失敗しました。")
        return redirect("notifications:list", team_id=my_team_id)


@login_required
@require_POST
def notification_read_all_view(request, team_id: int):
    my_team_id = _get_my_team_id_or_none(request.user)
    if my_team_id is None:
        return _redirect_to_team_entry(request, "通知を見るには、まずチームに参加してください。")

    try:
        _guard_team_mismatch(request, team_id)

        count = _service().mark_all_read(team_id=team_id, user=request.user)
        messages.success(request, f"{count}件を既読にしました")
        return redirect("notifications:list", team_id=team_id)

    except ValidationError:
        messages.error(request, "この操作は実行できません。")
        return redirect("notifications:list", team_id=my_team_id)
