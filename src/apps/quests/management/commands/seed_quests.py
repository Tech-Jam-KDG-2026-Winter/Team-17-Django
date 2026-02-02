# src/apps/quests/management/commands/seed_quests.py
from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.quests.management.seed_quests import upsert_quests


class Command(BaseCommand):
    help = "Seed quests into DB (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--inactive",
            action="store_true",
            help="Seed as inactive (is_active=False)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        is_active = not bool(options.get("inactive", False))
        result = upsert_quests(is_active=is_active)

        self.stdout.write(self.style.SUCCESS(
            f"seed_quests done: created={result['created']} updated={result['updated']} total={result['total']}"
        ))
