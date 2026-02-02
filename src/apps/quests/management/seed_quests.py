# src/apps/quests/management/seed_quests.py
# クエスト項目のリスト(後回しでもいいけど、あれば良い)
# 難易度 / クエスト名 / カテゴリ / ポイント

# src/apps/quests/management/seed_quests.py
# クエスト項目のリスト(後回しでもいいけど、あれば良い)
# 難易度 / クエスト名 / カテゴリ / ポイント

from __future__ import annotations

from typing import Iterable

from apps.quests.models import Quest, QuestCategory, QuestDifficulty


# NOTE:
# - 難易度ラベルは「Easy / Normal / Hard」
# - モデル側の DB 値は QuestDifficulty の定義に従う
#   (例: EASY="easy", NORMAL="normal", HARD="hard")
QUESTS: list[tuple[str, str, str, int]] = [
    # -------------------------
    # Easy（各10pt）
    # -------------------------
    (QuestDifficulty.EASY, "ラジオ体操（第1のみ） 1回", QuestCategory.STRETCH, 10),
    (QuestDifficulty.EASY, "かかと上げ下げ 30回", QuestCategory.MUSCLE, 10),
    (QuestDifficulty.EASY, "座る寸前スクワット 15回", QuestCategory.MUSCLE, 10),
    (QuestDifficulty.EASY, "壁腕立て 20回", QuestCategory.MUSCLE, 10),
    (QuestDifficulty.EASY, "お腹ペタンコキープ 1分", QuestCategory.MUSCLE, 10),
    (QuestDifficulty.EASY, "肩甲骨はがし回し（前後各20回）", QuestCategory.STRETCH, 10),
    (QuestDifficulty.EASY, "寝ながら足パカ 30回", QuestCategory.MUSCLE, 10),
    (QuestDifficulty.EASY, "足指グーパー 50回", QuestCategory.STRETCH, 10),
    (QuestDifficulty.EASY, "ウエストねじり 30回", QuestCategory.STRETCH, 10),
    (QuestDifficulty.EASY, "肩すくめリラックス 20回", QuestCategory.STRETCH, 10),
    # -------------------------
    # Normal（各40pt）
    # -------------------------
    (QuestDifficulty.NORMAL, "スクワット 30回", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "ひざつき腕立て 20回", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "プランク 1分", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "へそ見腹筋 30回", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "爆速もも上げ 1分", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "プランク左右ゆらし 1分", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "クロス腹筋 30回", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "ツイスト・マウンテン 1分", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "リバース・プランク 1分", QuestCategory.MUSCLE, 40),
    (QuestDifficulty.NORMAL, "クロスタッチ・クランチ 30回", QuestCategory.MUSCLE, 40),
    # -------------------------
    # Hard（各100pt）
    # -------------------------
    (QuestDifficulty.HARD, "腕立て伏せ 30回", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "V字バランス腹筋 25回", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "ジャンピングランジ 30回", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "スローワイドスクワット 20回", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "タックジャンプ 20回", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "プッシュアップ・サイド 30回", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "ジャンピングスクワット 30回", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "スタージャンプ 30回", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "シャドボクシング 3分", QuestCategory.MUSCLE, 100),
    (QuestDifficulty.HARD, "バービージャンプ 20回", QuestCategory.MUSCLE, 100),
]


def upsert_quests(*, is_active: bool = True) -> dict[str, int]:
    """
    クエスト定義をDBに投入（idempotent）。
    - 同名 + 同difficulty をキーに update_or_create する
    - points/category/is_active を同期する
    """
    created = 0
    updated = 0

    for difficulty, name, category, points in QUESTS:
        obj, was_created = Quest.objects.update_or_create(
            name=name,
            difficulty=difficulty,
            defaults={
                "category": category,
                "points": points,
                "is_active": is_active,
                # description などが必須ならここで埋める
                "description": "",
            },
        )
        if was_created:
            created += 1
        else:
            updated += 1

    return {"created": created, "updated": updated, "total": len(QUESTS)}
