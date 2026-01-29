# src/apps/quests/views.py
"""
Quests Views（MVP）

このファイルは「画面制御のみ」を担当する。
- DB操作・ビジネスルールは services.py に集約されている
- views は Service を呼び、結果をテンプレートに渡す or リダイレクトするだけ

絶対ルール:
- Quest / DailyQuestSet / DailyQuestItem / QuestCompletion を views で直接操作しない
- 更新系は必ず QuestService を利用する

最低限のガード（views がやること）:
- 未所属ユーザーは teams の entry（join/create）へ誘導する
- quests はチーム前提のため、未所属は来ないのが理想だが保険で守る
- 破壊的操作（達成）は POST のみ（@require_POST）
"""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

# TODO:
# - from .services import QuestService
# - service = QuestService()

# TODO:
# templates:
# - templates/quests/today.html
# - templates/quests/progress.html
# - templates/quests/mvp.html


# -----------------------------
# Helpers（teams と同じ思想）
# -----------------------------
def _get_my_team_id_or_none(user) -> int | None:
    """
    自分の所属チームIDを返す（未所属なら None）

    NOTE:
    - TeamMember.user = OneToOne のため、user.team_membership が基本導線
    - 参照のみ（更新しない）
    """
    membership = getattr(user, "team_membership", None)
    return membership.team_id if membership else None


def _redirect_to_team_entry(request, reason: str | None = None):
    """
    未所属ユーザーを「作成 or 参加」導線へ誘導する。
    quests はチーム前提なので、未所属が来たら teams:join に戻す。
    """
    if reason:
        messages.info(request, reason)
    return redirect("teams:join")


# -----------------------------
# Views
# -----------------------------
@login_required
def today_view(request):
    """
    今日のクエスト表示（チーム単位 / 4件）。

    仕様（MVP）:
    - GET:
        1) request.user の所属チームを取得（未所属なら teams:join へ）
        2) QuestService.get_or_create_today_set(team=..., user=request.user)
           - 「日付が変わればリセット」= DailyQuestSet(date=今日) が無ければ作る
           - 「4つ全部達成OK」= 1日1回制限はかけない（Completion は item×user の重複防止のみ）
        3) templates/quests/today.html に渡して表示

    UI要件（あなたの追加機能）:
    - クエストをタップ → Completed? Yes/No モーダル
      - Yes → POST /quests/complete/<daily_item_id>/
      - 成功したら flash message "Quest Clear!!"
    - 達成済みの見た目（任意だが発表映え）
      - 「達成済み判定」は service 側で返しても良いし、
        MVPなら complete を叩いたらメッセージが出るだけでも成立する

    TODO（共同開発者向け）:
    - Team を取得する（TeamModel は services 側に寄せてもOK）
    - service.get_or_create_today_set(...) を呼ぶ
    - context: team / daily_set / items / difficulty / generated_by などを渡す
    - ValidationError は messages.error → teams:detail へ戻す
    """
    my_team_id = _get_my_team_id_or_none(request.user)
    if my_team_id is None:
        return _redirect_to_team_entry(request, "クエストを見るには、まずチームに参加してください。")

    try:
        # TODO:
        # - team を取得（Team.objects.get(id=my_team_id)）
        # - result = service.get_or_create_today_set(team=team, user=request.user)
        # - return render(request, "quests/today.html", context)

        pass

    except ValidationError:
        messages.error(request, "クエストを表示できませんでした。")
        return redirect("teams:detail", team_id=my_team_id)
    except Exception:
        # デモで落とさない（詳細はログに出す想定）
        messages.error(request, "予期しないエラーが発生しました。")
        return redirect("teams:detail", team_id=my_team_id)


@login_required
@require_POST
def complete_view(request, daily_item_id: int):
    """
    クエスト達成（モーダルの Yes → POST）。

    仕様（MVP）:
    - POST:
        1) 未所属なら teams:join へ
        2) QuestService.complete(user=request.user, daily_item_id=...)
        - 4つ全部達成OK
        - 既に達成済みなら「達成済み」として扱う（例外にしない/しても良いが一貫性が大事）
        - ポイント加算は Team 側に保持（累計が保持される）
        - Notification 連携（member_completed / team_rank_up 等）は service 側で行う
        3) 成功:
        - messages.success("Quest Clear!!")（発表映え）
        - quests:today へ戻す

    失敗時:
    - ValidationError（所属外アクセス/存在しない/日付違い等）
    → messages.error → quests:today へ

    TODO（共同開発者向け）:
    - service.complete(...) の返り値設計に合わせて
    - gained_points を見て success/info を出し分けても良い
    """
    my_team_id = _get_my_team_id_or_none(request.user)
    if my_team_id is None:
        return _redirect_to_team_entry(request, "達成するには、まずチームに参加してください。")

    try:
        # TODO:
        # - result = service.complete(user=request.user, daily_item_id=daily_item_id)
        # - messages.success(request, "Quest Clear!!")
        # - return redirect("quests:today")

        pass

    except ValidationError:
        messages.error(request, "達成できませんでした。")
        return redirect("quests:today")
    except Exception:
        messages.error(request, "予期しないエラーが発生しました。")
        return redirect("quests:today")


@login_required
def progress_view(request):
    """
    チーム進捗（達成人数を星表示など）。

    仕様（MVP）:
    - GET:
        1) 未所属なら teams:join へ
        2) QuestService.get_today_progress(team=..., user=request.user)
        - 今日の DailyQuestSet を前提に、各 DailyQuestItem の達成人数を集計
        3) templates/quests/progress.html に渡して表示

    表示要件:
    - 達成人数を星にして表示（例: 5人中3人なら ★★★☆☆）
    - 4件それぞれに表示できると発表映え

    TODO（共同開発者向け）:
    - service.get_today_progress(...) を作る（items + completed_count + member_count）
    - context に渡してテンプレ側で星表示
    """
    my_team_id = _get_my_team_id_or_none(request.user)
    if my_team_id is None:
        return _redirect_to_team_entry(request, "進捗を見るには、まずチームに参加してください。")

    try:
        # TODO:
        # - team を取得
        # - progress = service.get_today_progress(team=team, user=request.user)
        # - return render(request, "quests/progress.html", context)

        pass

    except ValidationError:
        messages.error(request, "進捗を表示できませんでした。")
        return redirect("teams:detail", team_id=my_team_id)
    except Exception:
        messages.error(request, "予期しないエラーが発生しました。")
        return redirect("teams:detail", team_id=my_team_id)


@login_required
def mvp_view(request):
    """
    MVP表示（最もポイントを稼いだ人 / 同値は最速達成）。

    MVPの集計期間（おすすめ）:
    - 「今日（DailyQuestSet.date=今日）」の合計ポイント
    → 発表で説明しやすく、ユーザーも納得しやすい

    仕様（MVP）:
    - GET:
        1) 未所属なら teams:join へ
        2) QuestService.get_today_mvp(team=..., user=request.user)
        - 今日の達成ログを集計
        - 合計ポイントが最大のユーザー
        - 同値の場合は最も早く達成したユーザー
        3) templates/quests/mvp.html に渡して表示

    TODO（共同開発者向け）:
    - service.get_today_mvp(...) を作る
    - 戻り値は dict でも dataclass でも良いが、テンプレが扱いやすい形にする
    """
    my_team_id = _get_my_team_id_or_none(request.user)
    if my_team_id is None:
        return _redirect_to_team_entry(request, "MVPを見るには、まずチームに参加してください。")

    try:
        # TODO:
        # - team を取得
        # - mvp = service.get_today_mvp(team=team, user=request.user)
        # - return render(request, "quests/mvp.html", {"mvp": mvp})

        pass

    except ValidationError:
        messages.error(request, "MVPを表示できませんでした。")
        return redirect("teams:detail", team_id=my_team_id)
    except Exception:
        messages.error(request, "予期しないエラーが発生しました。")
        return redirect("teams:detail", team_id=my_team_id)
