#!/usr/bin/env python3
"""Inspect actual LoRA checkpoint artifacts; never infer weights from config files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ADAPTER_DIR_NAMES = (
    "qwen_adapter", "qwen_3b_sql",
    "sarvam_adapter", "sarvam_transliteration",
)
WEIGHT_NAMES = ("adapter_model.safetensors", "adapter_model.bin")


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_adapter_folder(folder: Path) -> dict:
    config = folder / "adapter_config.json"
    weights = [folder / name for name in WEIGHT_NAMES if (folder / name).is_file()]
    output = {
        "path": str(folder),
        "adapter_config_present": config.is_file(),
        "weights_present": bool(weights),
        "weights": [{"filename": p.name, "bytes": p.stat().st_size, "sha256": digest_file(p)} for p in weights],
        "checkpoint_verified_by_inference": False,
        "status": "weights_on_disk_unverified" if weights else "missing_adapter_weights",
    }
    if config.is_file():
        config_payload = json.loads(config.read_text(encoding="utf-8"))
        output["base_model_name_or_path"] = config_payload.get("base_model_name_or_path")
        output["config_sha256"] = digest_file(config)
    return output


def audit_root(root: Path) -> dict:
    items = [audit_adapter_folder(root / name) for name in ADAPTER_DIR_NAMES]
    return {
        "artifact_type": "IndicSQL LoRA packaging audit",
        "all_requested_adapters_have_weights": all(x["weights_present"] for x in items),
        "adapters": items,
        "note": "Artifact presence and SHA-256 do not verify training or performance; run inference to certify a checkpoint.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights-root", type=Path, default=Path("models/lora_weights"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit_root(args.weights_root)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
