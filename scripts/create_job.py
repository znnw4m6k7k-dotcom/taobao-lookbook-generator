#!/usr/bin/env python3
"""Create a non-destructive Taobao lookbook job skeleton and fixed shot manifest."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SHOTS = [
    ("ST-FRONT-01", "studio", "full_body_front"),
    ("ST-FRONT-02", "studio", "full_body_front"),
    ("ST-SIDE-L45", "studio", "left_45_degree"),
    ("ST-SIDE-R45", "studio", "right_45_degree"),
    ("ST-BACK-01", "studio", "full_body_back"),
    ("ST-BACK-02", "studio", "back_three_quarter"),
    ("ST-HALF-01", "studio", "half_body"),
    ("ST-HALF-02", "studio", "half_body"),
    ("ST-DETAIL-01", "studio", "product_detail"),
    ("ST-DETAIL-02", "studio", "product_detail"),
    ("ST-DETAIL-03", "studio", "product_detail"),
    ("ST-DETAIL-04", "studio", "product_detail"),
    ("STREET-01", "city_street", "full_body_front_motion"),
    ("STREET-02", "city_street", "side_three_quarter"),
    ("STREET-03", "city_street", "back_three_quarter"),
    ("STREET-04", "city_street", "full_or_half_editorial"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-dir", required=True, type=Path)
    parser.add_argument("--sku", required=True)
    parser.add_argument("--color", required=True)
    parser.add_argument(
        "--product-type",
        required=True,
        choices=("dress", "top", "bottom", "set", "outerwear"),
    )
    parser.add_argument("--primary-product", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = args.job_dir / "job-manifest.json"
    if manifest_path.exists():
        raise SystemExit(f"Refusing to overwrite existing manifest: {manifest_path}")

    directories = [
        "source/model",
        "source/product",
        "source/product-detail",
        "source/styling",
        "candidates",
        "reviews",
        "final",
        "human-review",
    ]
    for relative in directories:
        (args.job_dir / relative).mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sku": args.sku,
        "color": args.color,
        "product_type": args.product_type,
        "primary_product": args.primary_product,
        "model_authorized_for_ai_and_commercial_use": None,
        "output": {
            "count": 16,
            "format": "jpg",
            "quality": "highest",
            "width": 1536,
            "height": 2048,
            "aspect_ratio": "3:4",
        },
        "sources": {
            "model": [],
            "product": [],
            "product_detail": [],
            "styling": [],
        },
        "locks": {
            "identity_lock": {},
            "product_lock": {},
            "styling_lock": {},
            "unknowns": [],
        },
        "shots": [
            {
                "shot_id": shot_id,
                "environment": environment,
                "coverage": coverage,
                "status": "pending",
                "attempts": [],
            }
            for shot_id, environment, coverage in SHOTS
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    review_path = args.job_dir / "reviews" / "review-state.json"
    review_path.write_text(
        json.dumps({"schema_version": 1, "reviews": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(manifest_path)
    print(review_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

