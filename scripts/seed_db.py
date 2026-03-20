"""
Populate MongoDB with D&D seed data from JSON files.

Usage:
    python -m scripts.seed_db           # seed both editions
    python -m scripts.seed_db --edition 5e
    python -m scripts.seed_db --edition 5.5e
    python -m scripts.seed_db --drop    # drop collections first
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Type

from beanie import Document

from app.config import settings
from app.database import init_db, close_db, ALL_MODELS
from app.models.race import Race
from app.models.character_class import CharacterClass
from app.models.spell import Spell
from app.models.background import Background
from app.models.feat import Feat
from app.models.equipment import Equipment

SEED_DIR = Path(__file__).resolve().parent.parent / "seed"

EDITION_MAP: dict[str, str] = {
    "5e": "5e",
    "5.5e": "5_5e",
}

FILE_MODEL_MAP: dict[str, Type[Document]] = {
    "races.json": Race,
    "classes.json": CharacterClass,
    "spells.json": Spell,
    "backgrounds.json": Background,
    "feats.json": Feat,
    "equipment.json": Equipment,
}


async def seed_edition(edition: str, drop: bool = False) -> None:
    folder_name = EDITION_MAP[edition]
    seed_path = SEED_DIR / folder_name

    if not seed_path.exists():
        print(f"  [SKIP] Seed folder not found: {seed_path}")
        return

    print(f"\n{'='*50}")
    print(f"  Seeding edition: {edition} (from {seed_path})")
    print(f"{'='*50}")

    for filename, model_cls in FILE_MODEL_MAP.items():
        filepath = seed_path / filename
        if not filepath.exists():
            print(f"  [SKIP] {filename} not found")
            continue

        raw = json.loads(filepath.read_text(encoding="utf-8"))
        print(f"  {filename}: {len(raw)} entries ... ", end="", flush=True)

        if drop:
            deleted = await model_cls.find({"edition": edition}).delete()
            count = deleted.deleted_count if deleted else 0
            print(f"(dropped {count}) ", end="", flush=True)

        upserted = 0
        for entry in raw:
            entry["edition"] = edition
            existing = await model_cls.find_one(
                {"name": entry["name"], "edition": edition}
            )
            if existing:
                await existing.set(entry)
            else:
                await model_cls(**entry).insert()
            upserted += 1

        print(f"OK ({upserted} upserted)")


async def main(editions: list[str], drop: bool) -> None:
    print(f"Connecting to {settings.MONGO_URI} / {settings.MONGO_DB_NAME}")
    await init_db()

    for edition in editions:
        await seed_edition(edition, drop=drop)

    await close_db()
    print("\nDone!")


def cli() -> None:
    parser = argparse.ArgumentParser(description="Seed D&D data into MongoDB")
    parser.add_argument(
        "--edition",
        choices=["5e", "5.5e"],
        help="Seed only this edition (default: both)",
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop existing data for the edition(s) before seeding",
    )
    args = parser.parse_args()

    editions = [args.edition] if args.edition else ["5e", "5.5e"]
    asyncio.run(main(editions, args.drop))


if __name__ == "__main__":
    cli()
