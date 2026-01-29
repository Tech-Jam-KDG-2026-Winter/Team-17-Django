# src/config/settings/prod.py
from .base import *  # noqa

# 本番想定だが、ローカルでこの設定を読んでも即死しないように最低限の保険を入れる
DEBUG = False

# ローカルでの確認時に DisallowedHost を避けるためのフォールバック
# 本番では環境変数 DJANGO_ALLOWED_HOSTS を必ず設定する運用にする（後日でOK）
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
