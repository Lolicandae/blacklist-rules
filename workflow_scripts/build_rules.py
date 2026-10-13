#!/usr/bin/env python3
"""Build YAML, MRS, Surge and JSON rule files from neutral .rules sources."""

from __future__ import annotations

import argparse
import json
import ipaddress
import os
import re
import shutil
import subprocess
import tempfile
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
BUILD_CONFIG_PATH = ROOT / "rule_sources" / "rules.build.json"


class BuildError(RuntimeError):
    """Raised when source files or build config are invalid."""


@dataclass(frozen=True)
class Marker:
    kind: str
    text: str


@dataclass(frozen=True)
class Rule:
    raw: str
    enabled: bool = True
    note: str = ""


Item = Marker | Rule


def load_config(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise BuildError(f"Failed to read build config: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BuildError(f"Build config is not valid JSON: {path}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("outputs"), list):
        raise BuildError("Build config must contain an `outputs` array")
    return data


def split_note(text: str) -> tuple[str, str]:
    if " # " not in text:
        return text.strip(), ""
    raw, note = text.split(" # ", 1)
    return raw.strip(), note.strip()


def parse_source(path: Path) -> list[Item]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise BuildError(f"Failed to read source file: {path}") from exc

    items: list[Item] = []
    for number, line in enumerate(lines, 1):
        text = line.strip()
        if not text:
            continue
        if text.startswith("### "):
            items.append(Marker("group", text[4:].strip()))
            continue
        if text.startswith("## "):
            items.append(Marker("category", text[3:].strip()))
            continue

        enabled = True
        if text.startswith("! "):
            enabled = False
            text = text[2:].strip()

        raw, note = split_note(text)
        if not raw:
            raise BuildError(f"Empty rule in {path} at line {number}")
        items.append(Rule(raw=raw, enabled=enabled, note=note))

    return items


def load_sources(paths: Iterable[str]) -> list[Item]:
    items: list[Item] = []
    for source in paths:
        items.extend(parse_source(ROOT / source))
    return items


def source_sort_key(value: str | None) -> str:
    return "" if value is None else value.casefold()


def merge_sort_categories_groups(items: list[Item]) -> list[Item]:
    categories: "OrderedDict[str | None, OrderedDict[str | None, list[Rule]]]" = OrderedDict()
    current_category: str | None = None
    current_group: str | None = None

    for item in items:
        if isinstance(item, Marker) and item.kind == "category":
            current_category = item.text
            current_group = None
            categories.setdefault(current_category, OrderedDict())
            continue
        if isinstance(item, Marker) and item.kind == "group":
            current_group = item.text
            categories.setdefault(current_category, OrderedDict()).setdefault(current_group, [])
            continue
        if isinstance(item, Rule):
            categories.setdefault(current_category, OrderedDict()).setdefault(current_group, []).append(item)

    merged: list[Item] = []
    for category in sorted(categories, key=source_sort_key):
        if category is not None:
            merged.append(Marker("category", category))
        groups = categories[category]
        if None in groups:
            merged.extend(groups[None])
        for group in sorted((name for name in groups if name is not None), key=source_sort_key):
            merged.append(Marker("group", group))
            merged.extend(groups[group])
    return merged


def to_surge_rule(raw: str) -> str:
    if raw.startswith("+."):
        return raw[1:]
    return raw


def render_items(items: list[Item], fmt: str, include_categories: bool = True) -> list[str]:
    if fmt not in {"clash", "surge"}:
        raise BuildError(f"Unsupported output format: {fmt}")

    lines: list[str] = []
    if fmt == "clash":
        lines.append("payload:")

    for item in items:
        if isinstance(item, Marker):
            if item.kind == "category" and not include_categories:
                continue
            if item.kind == "category":
                comment = f"/*{item.text}*/"
            elif item.kind == "group":
                comment = item.text
            else:
                raise BuildError(f"Unsupported marker kind: {item.kind}")
            lines.append(f"  # {comment}" if fmt == "clash" else f"# {comment}")
            continue

        raw = item.raw if fmt == "clash" else to_surge_rule(item.raw)
        if fmt == "clash" and raw.startswith("*"):
            raw = json.dumps(raw, ensure_ascii=False)
        note = f" # {item.note}" if fmt == "clash" and item.note else ""
        if fmt == "clash":
            prefix = "  - " if item.enabled else "  # - "
            lines.append(f"{prefix}{raw}{note}")
        else:
            prefix = "" if item.enabled else "# "
            lines.append(f"{prefix}{raw}")

    return lines


def detect_line_ending(path: Path) -> str:
    if not path.exists():
        return "\n"
    content = path.read_bytes()
    return "\r\n" if b"\r\n" in content else "\n"


def render_json_rules(items: list[Item]) -> str:
    fields: dict[str, list[str]] = {}
    seen: dict[str, set[str]] = {}

    def add(field: str, value: str) -> None:
        values = fields.setdefault(field, [])
        unique = seen.setdefault(field, set())
        if value not in unique:
            unique.add(value)
            values.append(value)

    for item in items:
        if not isinstance(item, Rule) or not item.enabled:
            continue
        if item.raw.startswith("PROCESS-NAME,"):
            name = item.raw.partition(",")[2]
            if not name or any(char in name for char in ",/\\\r\n"):
                raise BuildError(f"Invalid process name rule: {item.raw}")
            add("process_name", name)
            continue
        raw = item.raw.lower()
        try:
            network = ipaddress.ip_network(raw, strict=False)
        except ValueError:
            network = None
        if network is not None:
            add("ip_cidr", str(network))
            continue
        plus, dot = raw.startswith("+."), raw.startswith(".")
        name = raw[2:] if plus else raw[1:] if dot else raw
        if not name or not all(label == "*" or re.fullmatch(r"[a-z0-9_-]+", label) for label in name.split(".")):
            raise BuildError(f"Unsupported JSON domain rule: {item.raw}")
        if "*" not in name:
            if not dot:
                add("domain", name)
            if plus or dot:
                add("domain_suffix", "." + name)
        else:
            labels = r"\.".join(r"[^.]+" if label == "*" else re.escape(label) for label in name.split("."))
            prefix = r"(?:[^.]+\.)*" if plus else r"(?:[^.]+\.)+" if dot else ""
            add("domain_regex", "^" + prefix + labels + "$")
    domains = {key: values for key, values in fields.items() if key.startswith("domain")}
    rules = [domains] if domains else []
    rules.extend({key: fields[key]} for key in ("ip_cidr", "process_name") if key in fields)
    return json.dumps({"version": 3, "rules": rules}, ensure_ascii=False, indent=2)


def self_check() -> None:
    groups = json.loads(render_json_rules([Rule("exact.test"), Rule("+.suffix.test"), Rule(".child.test"), Rule("*.one.test"), Rule("+.stun.*.*"), Rule("disabled.test", enabled=False), Rule("192.0.2.1/24"), Rule("PROCESS-NAME,App.exe")]))["rules"]
    rules = groups[0]

    def matches(name: str) -> bool:
        return name in rules.get("domain", []) or any(name.endswith(suffix) for suffix in rules.get("domain_suffix", [])) or any(re.fullmatch(pattern, name) for pattern in rules.get("domain_regex", []))

    assert matches("exact.test") and not matches("a.exact.test")
    assert matches("suffix.test") and matches("a.b.suffix.test") and not matches("bad-suffix.test")
    assert matches("a.child.test") and not matches("child.test")
    assert matches("a.one.test") and not matches("a.b.one.test") and not matches("one.test")
    assert matches("stun.foo.bar") and matches("a.stun.foo.bar") and not matches("stun.bar")
    assert not matches("disabled.test")
    assert groups[1:] == [{"ip_cidr": ["192.0.2.0/24"]}, {"process_name": ["App.exe"]}]
    assert json.loads(render_json_rules([Rule("disabled.test", enabled=False)]))["rules"] == []
    for raw in ["PROCESS-NAME,", "PROCESS-NAME,/app.exe", "DOMAIN,app.test", "+.bad..test", "192.0.2.0/33"]:
        try:
            render_json_rules([Rule(raw)])
        except BuildError:
            continue
        raise AssertionError(f"Invalid JSON rule accepted: {raw}")
    print("JSON rule self-check passed.")


def render_mrs(items: list[Item], behavior: str) -> bytes:
    if not isinstance(behavior, str) or behavior not in {"domain", "ipcidr"}:
        raise BuildError("MRS behavior must be domain or ipcidr")
    groups = json.loads(render_json_rules(items))["rules"]
    allowed = {"domain", "domain_suffix", "domain_regex"} if behavior == "domain" else {"ip_cidr"}
    if not groups or any(set(group) - allowed for group in groups):
        raise BuildError(f"MRS {behavior} requires nonempty rules of the matching type")
    payload = groups[0]["ip_cidr"] if behavior == "ipcidr" else [
        item.raw for item in items if isinstance(item, Rule) and item.enabled
    ]
    executable = os.environ.get("MIHOMO_BIN") or shutil.which("mihomo")
    if not executable:
        raise BuildError("MRS conversion requires Mihomo; set MIHOMO_BIN to its executable path")
    with tempfile.TemporaryDirectory(prefix="ai-agent-custom-mrs-") as temporary:
        source = Path(temporary) / "ai-agent-input.yaml"
        target = Path(temporary) / "ai-agent-output.mrs"
        source.write_text("payload:\n" + "\n".join(f"  - {json.dumps(value, ensure_ascii=False)}" for value in payload) + "\n", encoding="utf-8")
        try:
            result = subprocess.run(
                [executable, "convert-ruleset", behavior, "yaml", str(source), str(target)],
                capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise BuildError(f"MRS conversion failed: {exc}") from exc
        if result.returncode or not target.is_file():
            raise BuildError(f"MRS conversion failed: {result.stderr.strip()}")
        content = target.read_bytes()
        if not content:
            raise BuildError("Mihomo returned an empty MRS file")
        return content


def self_check_mrs() -> None:
    for behavior, rules in (("domain", [Rule("exact.test"), Rule("+.suffix.test"), Rule(".child.test"), Rule("*.one.test"), Rule("+.stun.*.*"), Rule("null"), Rule("true"), Rule("0123"), Rule("disabled.test", enabled=False)]), ("ipcidr", [Rule("192.0.2.1/24"), Rule("2001:db8:abcd::1/32"), Rule("198.51.100.1"), Rule("2001:db9::1"), Rule("203.0.113.1", enabled=False)])):
        content = render_mrs(rules, behavior)
        assert content == render_mrs([item for item in rules if item.enabled], behavior)
        with tempfile.TemporaryDirectory(prefix="ai-agent-mrs-self-check-") as temporary:
            source = Path(temporary) / "ai-agent-input.mrs"
            target = Path(temporary) / "ai-agent-output.txt"
            source.write_bytes(content)
            result = subprocess.run(
                [os.environ.get("MIHOMO_BIN") or shutil.which("mihomo"), "convert-ruleset", behavior, "mrs", str(source), str(target)],
                capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            assert result.returncode == 0, result.stderr
            expected = {str(ipaddress.ip_network(item.raw, strict=False)) if behavior == "ipcidr" else item.raw for item in rules if item.enabled}
            assert set(target.read_text(encoding="utf-8").splitlines()) == expected
    for behavior, rules in (("classical", [Rule("PROCESS-NAME,App.exe")]), ("domain", [Rule("PROCESS-NAME,App.exe")]), ("domain", [Rule("192.0.2.0/24")]), ("ipcidr", [Rule("example.test")]), ("domain", [Rule("disabled.test", enabled=False)])):
        try:
            render_mrs(rules, behavior)
        except BuildError:
            continue
        raise AssertionError(f"Invalid {behavior} MRS input accepted")
    with tempfile.TemporaryDirectory(prefix="ai-agent-mrs-build-check-") as temporary:
        root = Path(temporary)
        (root / "ai-agent-source.rules").write_text("example.test\n", encoding="utf-8")
        original = root / "ai-agent-first.yaml"
        original.write_bytes(b"Unchanged original output\n")
        config = root / "ai-agent-config.json"
        config.write_text(json.dumps({"outputs": [
            {"path": "ai-agent-first.yaml", "format": "clash", "sources": ["ai-agent-source.rules"]},
            {"path": "ai-agent-second.yaml", "format": "clash", "mrs": "classical", "sources": ["ai-agent-source.rules"]},
        ]}), encoding="utf-8")
        with patch.dict(globals(), {"ROOT": root, "BUILD_CONFIG_PATH": config}):
            try:
                build_targets(check_mode=False)
            except BuildError:
                pass
            else:
                raise AssertionError("Invalid MRS output did not stop the build")
        assert original.read_bytes() == b"Unchanged original output\n"
        assert not (root / "ai-agent-second.yaml").exists()
        config.write_text(json.dumps({"outputs": [
            {"path": "ai-agent-first.yaml", "format": "clash", "mrs": "domain", "sources": ["ai-agent-source.rules"]},
        ]}), encoding="utf-8")
        with patch.dict(globals(), {"ROOT": root, "BUILD_CONFIG_PATH": config}):
            assert build_targets(check_mode=False, validate_mode=True) == 0
        assert original.read_bytes() == b"Unchanged original output\n"
        assert not original.with_suffix(".mrs").exists()
    print("MRS domain/IP conversion, disabled rules and unsupported input checks passed.")


def build_output(output: dict[str, Any]) -> list[tuple[Path, bytes]]:
    path = ROOT / str(output.get("path", ""))
    fmt = str(output.get("format", "")).lower()
    sources = output.get("sources")
    if not path.name or not isinstance(sources, list):
        raise BuildError("Each output must define `path`, `format`, and `sources`")

    items = load_sources(str(source) for source in sources)
    if output.get("merge") == "sort_categories_groups":
        items = merge_sort_categories_groups(items)

    line_ending = detect_line_ending(path)
    include_categories = not bool(output.get("omit_categories", False))
    content = render_json_rules(items).replace("\n", line_ending) + line_ending if fmt == "json" else line_ending.join(render_items(items, fmt, include_categories)) + line_ending
    targets = [(path, content.encode("utf-8"))]
    if "mrs" in output:
        if fmt != "clash" or path.suffix != ".yaml":
            raise BuildError("MRS companions require a Clash YAML output")
        targets.append((path.with_suffix(".mrs"), render_mrs(items, output["mrs"])))
    return targets


def build_targets(check_mode: bool, validate_mode: bool = False) -> int:
    config = load_config(BUILD_CONFIG_PATH)
    failures = 0
    targets = []
    for output in config["outputs"]:
        if not isinstance(output, dict):
            raise BuildError("Output entries must be objects")
        targets.extend(build_output(output))

    if validate_mode:
        return 0

    for target_path, content in targets:
        if check_mode:
            try:
                expected = target_path.read_bytes()
            except OSError as exc:
                raise BuildError(f"Failed to read target file: {target_path}") from exc
            if expected != content:
                print(f"[DIFF] {target_path.relative_to(ROOT)}")
                failures += 1
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(content)
        print(f"[OK] {target_path.relative_to(ROOT)}")

    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description="Build rule outputs from .rules sources")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Check generated files without writing")
    mode.add_argument("--validate", action="store_true", help="Validate source-generated candidates without writing or comparing published files")
    mode.add_argument("--self-test", action="store_true", help="Check JSON matching and MRS conversion without publishing")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_check()
            self_check_mrs()
            return
        failures = build_targets(check_mode=args.check, validate_mode=args.validate)
    except BuildError as exc:
        print(f"[ERROR] {exc}")
        raise SystemExit(1)

    if args.check and failures:
        print(f"Build check failed, mismatch count: {failures}")
        raise SystemExit(1)
    if args.validate:
        print("Build candidate validation passed.")
    elif args.check:
        print("Build check passed.")
    else:
        print("Build completed.")


if __name__ == "__main__":
    main()
