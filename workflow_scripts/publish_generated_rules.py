#!/usr/bin/env python3
"""Publish regenerated rules from the latest main branch; locally, run --self-test."""

from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path, PurePosixPath
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MAX_ATTEMPTS = 3
DIRECTORIES = {"build": ("artifact",), "sync": ("third_party/clash", "third_party/surge", "third_party/sing-box")}
SCOPES = {
    "build": ("artifact",),
    "sync": (
        "third_party/clash", "third_party/surge", "third_party/sing-box",
        "third_party/sources.json", "third_party/README.md", "third_party/README.zh-cn.md",
        "client_conf/mihomo_configuration/mihomo_configuration.yaml",
        "client_conf/mihomo_override/mihomo_override.js",
        "client_conf/surge_configuration/surge_configuration.conf",
    ),
}
SCRIPTS = {"build": "build_rules.py", "sync": "sync_third_party_rules.py"}
MESSAGES = {"build": "chore: build rules", "sync": "chore: sync third-party rules"}


class PublishError(RuntimeError):
    """Generation, validation or safe publication could not complete."""


def command_environment() -> dict[str, str]:
    environment = os.environ.copy()
    # Explicit -C paths must not be redirected by inherited Git repository settings.
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
                 "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE"):
        environment.pop(name, None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["GIT_TERMINAL_PROMPT"] = "0"
    return environment


def git(root: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=command_environment(), timeout=180,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PublishError(f"Git {arguments[0]} could not complete.") from exc
    if check and result.returncode:
        # Remote diagnostics may contain authenticated URLs; never echo them.
        raise PublishError(f"Git {arguments[0]} failed (exit {result.returncode}).")
    return result


def text_git(root: Path, *arguments: str) -> str:
    return git(root, *arguments).stdout.decode("utf-8").strip()


def allowed_path(worktree: Path, mode: str, relative: str) -> Path:
    path = PurePosixPath(relative)
    if (not relative or "\\" in relative or path.is_absolute()
            or any(part in {"", ".", ".."} for part in relative.split("/"))
            or ":" in relative
            or not (relative in SCOPES[mode]
                    or any(relative.startswith(scope + "/") for scope in DIRECTORIES[mode]))):
        raise PublishError("Generated output is outside the permitted paths.")
    target = worktree / path
    current = target
    while current != worktree:
        if current.is_symlink():
            raise PublishError("Generated outputs cannot use symbolic links.")
        current = current.parent
    if not target.resolve().is_relative_to(worktree.resolve()):
        raise PublishError("Generated output resolves outside the worktree.")
    return target


def changed_paths(worktree: Path, mode: str) -> list[str]:
    tracked = git(worktree, "diff", "--no-renames", "--name-only", "-z", "HEAD", "--").stdout
    # Include ignored files too: a new ignored file is still an unexpected output.
    untracked = git(worktree, "ls-files", "--others", "-z").stdout
    paths = sorted({path.decode("utf-8") for path in (tracked + untracked).split(b"\0") if path})
    for relative in paths:
        allowed_path(worktree, mode, relative)
    return paths


def validate_inputs(worktree: Path, mode: str) -> None:
    for scope in SCOPES[mode]:
        allowed_path(worktree, mode, scope)
    entries = git(worktree, "ls-files", "--stage", "-z", "--", *SCOPES[mode]).stdout
    if any(entry.startswith((b"120000 ", b"160000 ")) for entry in entries.split(b"\0")):
        raise PublishError("Generated output paths cannot contain links or submodules.")
    if mode == "build":
        try:
            configuration = json.loads((worktree / "rule_sources/rules.build.json").read_text(encoding="utf-8"))
            outputs = configuration["outputs"]
            if not isinstance(outputs, list):
                raise ValueError("outputs must be an array")
            for output in outputs:
                target = allowed_path(worktree, mode, output["path"])
                if "mrs" in output:
                    allowed_path(worktree, mode, target.with_suffix(".mrs").relative_to(worktree).as_posix())
        except (OSError, ValueError, TypeError, KeyError) as exc:
            raise PublishError("Build output configuration is invalid.") from exc


def generate(worktree: Path, mode: str, base: str) -> None:
    validate_inputs(worktree, mode)
    script = worktree / "workflow_scripts" / SCRIPTS[mode]
    if (not script.is_file() or script.is_symlink() or script.parent.is_symlink()
            or not script.resolve().is_relative_to(worktree.resolve())):
        raise PublishError("The latest branch has no regular generation script.")
    # Run the fetched version's tests and CLI; do not import the root checkout's code.
    for arguments, label in ((["--self-test"], "self-test"), ([], "generation"), (["--check"], "check")):
        try:
            result = subprocess.run(
                [sys.executable, str(script), *arguments], cwd=worktree,
                env=command_environment(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        except OSError as exc:
            raise PublishError(f"{mode} {label} could not run.") from exc
        if result.returncode:
            raise PublishError(f"{mode} {label} failed (exit {result.returncode}).")
        if label == "generation":
            sys.stdout.write(result.stdout.decode("utf-8", errors="replace"))
        if text_git(worktree, "rev-parse", "HEAD") != base:
            raise PublishError("Generation unexpectedly changed the worktree commit.")
        changed_paths(worktree, mode)


def fetch_tip(root: Path, branch: str) -> str:
    git(root, "fetch", "--no-tags", "origin", f"refs/heads/{branch}")
    return text_git(root, "rev-parse", "FETCH_HEAD^{commit}")


def advanced(root: Path, base: str, latest: str) -> bool:
    if latest == base:
        return False
    result = git(root, "merge-base", "--is-ancestor", base, latest, check=False)
    if result.returncode:
        raise PublishError("The target branch was rewritten; refusing to retry.")
    return True


def publish(root: Path, mode: str, branch: str, before_push=None) -> str:
    """Internal seam for local bare-repository tests; the CLI enforces CI authorization."""
    root = root.resolve()
    if mode not in SCOPES or branch != "main":
        raise PublishError("Publication only supports build/sync on main.")
    if Path(text_git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise PublishError("Publication requires the repository root.")
    if git(root, "config", "--get-all", "remote.origin.pushurl", check=False).returncode != 1:
        raise PublishError("An alternate origin push target is unsupported.")

    with tempfile.TemporaryDirectory(prefix="ai-agent-rules-publish-") as temporary:
        owned = Path(temporary).resolve()
        for attempt in range(1, MAX_ATTEMPTS + 1):
            base = fetch_tip(root, branch)
            worktree = owned / f"ai-agent-worktree-{attempt}"
            added = False
            try:
                git(root, "worktree", "add", "--detach", str(worktree), base)
                added = True
                generate(worktree, mode, base)
                paths = changed_paths(worktree, mode)
                if not paths:
                    if not advanced(root, base, fetch_tip(root, branch)):
                        print(f"{mode}: generated rules are already up to date.")
                        return "unchanged"
                else:
                    git(worktree, "add", "--all", "--", *paths)
                    git(worktree, "-c", "user.name=github-actions[bot]", "-c",
                        "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                        "commit", "--no-gpg-sign", "-m", MESSAGES[mode])
                    if before_push is not None:
                        before_push(attempt)
                    result = git(worktree, "push", "origin", f"HEAD:refs/heads/{branch}", check=False)
                    if result.returncode == 0:
                        print(f"{mode}: published generated rules (attempt {attempt}).")
                        return "published"
                    latest = fetch_tip(root, branch)
                    if not advanced(root, base, latest):
                        raise PublishError(f"Git push failed without branch advancement (exit {result.returncode}).")
                if attempt == MAX_ATTEMPTS:
                    raise PublishError(f"The target branch kept advancing; exhausted {MAX_ATTEMPTS} attempts.")
                print(f"{mode}: branch advanced; regenerating from the latest source.")
            finally:
                if added:
                    # Remove only the exact worktree created inside this invocation's directory.
                    if worktree.parent.resolve() != owned or worktree.resolve().parent != owned:
                        raise PublishError("Unsafe temporary worktree cleanup path.")
                    git(root, "worktree", "remove", "--force", str(worktree))
    raise PublishError("Publication did not complete.")


def require_ci() -> str:
    if (os.environ.get("GITHUB_ACTIONS") != "true"
            or os.environ.get("GITHUB_EVENT_NAME") not in {"push", "schedule", "workflow_dispatch"}
            or os.environ.get("GITHUB_REF") != "refs/heads/main"
            or os.environ.get("GITHUB_HEAD_REF") or os.environ.get("GITHUB_BASE_REF")):
        raise PublishError("Publishing requires a trusted non-PR GitHub Actions main-branch run; use --self-test locally.")
    return "main"


def self_test() -> None:
    """Exercise real Git publication exclusively against temporary local bare remotes."""
    fixture_script = textwrap.dedent('''\
        import json
        import subprocess
        import sys
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        if "--self-test" in sys.argv:
            result = subprocess.run(["git", "config", "--get", "aiagent.checkout-v6-compatible"], capture_output=True)
            assert result.stdout.strip() == b"true", "checkout v6 worktree credential include did not match"
            print("ai-agent-self-test-only")
            raise SystemExit(0)
        data = json.loads((root / "rule_sources/ai-agent-source.json").read_text())
        mode = "build" if Path(__file__).name == "build_rules.py" else "sync"
        target = root / ("artifact/ai-agent-build.txt" if mode == "build" else "third_party/clash/ai-agent-sync.txt")
        content = "VERSION:" + data[mode]
        if "--check" in sys.argv:
            print("ai-agent-check-only")
            raise SystemExit(1 if data.get("invalid") or target.read_text() != content else 0)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        if mode == "sync":
            print("::warning::ai-agent retained-source test")
        if data.get("stray"):
            (root / data["stray"]).write_text("unexpected", encoding="utf-8")
        ''')

    with tempfile.TemporaryDirectory(prefix="ai-agent-rules-publish-test-") as temporary, patch.dict(
        os.environ, {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
    ):
        owned = Path(temporary).resolve()

        def fixture(name: str) -> tuple[Path, Path, Path]:
            folder = owned / ("ai-agent-" + name)
            folder.mkdir()
            remote, actor, root = (folder / part for part in ("ai-agent-remote.git", "ai-agent-actor", "ai-agent-root"))
            git(folder, "init", "--bare", "--initial-branch=main", str(remote))
            git(folder, "init", "--initial-branch=main", str(actor))
            git(actor, "config", "user.name", "ai-agent-test")
            git(actor, "config", "user.email", "ai-agent@example.invalid")
            for relative, content in {
                "workflow_scripts/build_rules.py": fixture_script,
                "workflow_scripts/sync_third_party_rules.py": fixture_script,
                "rule_sources/rules.build.json": json.dumps({"outputs": [{"path": "artifact/ai-agent-build.txt"}]}),
                "rule_sources/ai-agent-source.json": json.dumps({"build": "one", "sync": "one"}),
                "artifact/ai-agent-build.txt": "old-build",
                "third_party/clash/ai-agent-sync.txt": "old-sync",
                "README.md": "original",
                ".gitignore": "ai-agent-ignored.txt\n",
            }.items():
                path = actor / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            git(actor, "add", "--all")
            git(actor, "commit", "--no-gpg-sign", "-m", "fixture")
            git(actor, "remote", "add", "origin", str(remote))
            git(actor, "push", "origin", "main")
            git(folder, "clone", str(remote), str(root))
            credentials = folder / "ai-agent-credentials.config"
            credentials.write_text("[aiagent]\ncheckout-v6-compatible = true\n", encoding="utf-8")
            # Same includeIf patterns as checkout v6, with a harmless marker instead of credentials.
            git(root, "config", f"includeIf.gitdir:{root.as_posix()}/.git.path", str(credentials))
            git(root, "config", f"includeIf.gitdir:{root.as_posix()}/.git/worktrees/*.path", str(credentials))
            (root / "README.md").write_text("staged user edit", encoding="utf-8")
            git(root, "add", "README.md")
            (root / "README.md").write_text("unstaged user edit", encoding="utf-8")
            (root / "ai-agent-user.txt").write_text("untracked user edit", encoding="utf-8")
            return root, actor, remote

        def update(actor: Path, **values) -> None:
            git(actor, "pull", "--ff-only", "origin", "main")
            source = actor / "rule_sources/ai-agent-source.json"
            data = json.loads(source.read_text())
            data.update(values)
            source.write_text(json.dumps(data), encoding="utf-8")
            git(actor, "add", "--all")
            git(actor, "commit", "--no-gpg-sign", "-m", "manual update")
            git(actor, "push", "origin", "main")

        def snapshot(root: Path) -> tuple:
            return (
                text_git(root, "rev-parse", "HEAD"), text_git(root, "symbolic-ref", "HEAD"),
                git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout,
                git(root, "diff", "--binary", "HEAD").stdout,
                git(root, "diff", "--cached", "--binary").stdout,
                (root / "ai-agent-user.txt").read_bytes(),
            )

        def preserved(root: Path, original: tuple) -> None:
            assert snapshot(root) == original, "root checkout changed"
            assert text_git(root, "worktree", "list", "--porcelain").count("worktree ") == 1

        def rejected(action, message: str) -> None:
            try:
                action()
            except PublishError as exc:
                assert message in str(exc), str(exc)
                assert "ai-agent-secret" not in str(exc)
            else:
                raise AssertionError("expected publication to fail")

        root, actor, remote = fixture("both-modes")
        original = snapshot(root)
        assert publish(root, "build", "main") == "published"
        with patch("sys.stdout", new_callable=io.StringIO) as captured:
            assert publish(root, "sync", "main") == "published"
        assert "::warning::ai-agent retained-source test" in captured.getvalue()
        assert "ai-agent-self-test-only" not in captured.getvalue() and "ai-agent-check-only" not in captured.getvalue()
        assert text_git(remote, "show", "main:artifact/ai-agent-build.txt") == "VERSION:one"
        assert text_git(remote, "show", "main:third_party/clash/ai-agent-sync.txt") == "VERSION:one"
        count = text_git(remote, "rev-list", "--count", "main")
        assert publish(root, "build", "main") == "unchanged"
        assert text_git(remote, "rev-list", "--count", "main") == count
        preserved(root, original)

        root, actor, remote = fixture("unchanged-race")
        assert publish(root, "build", "main") == "published"
        original = snapshot(root)
        real_generate = generate
        generated = 0

        def source_changed(worktree: Path, mode: str, base: str) -> None:
            nonlocal generated
            real_generate(worktree, mode, base)
            generated += 1
            if generated == 1:
                update(actor, build="after-unchanged")

        with patch(__name__ + ".generate", side_effect=source_changed):
            assert publish(root, "build", "main") == "published"
        assert generated == 2
        assert text_git(remote, "show", "main:artifact/ai-agent-build.txt") == "VERSION:after-unchanged"
        preserved(root, original)

        root, actor, remote = fixture("manual-race")
        original = snapshot(root)

        def race(attempt: int) -> None:
            if attempt == 1:
                script = actor / "workflow_scripts/build_rules.py"
                script.write_text(fixture_script.replace("VERSION:", "LATEST:"), encoding="utf-8")
                update(actor, build="two")

        assert publish(root, "build", "main", race) == "published"
        assert text_git(remote, "show", "main:artifact/ai-agent-build.txt") == "LATEST:two"
        assert text_git(remote, "show", "main:rule_sources/ai-agent-source.json") == json.dumps({"build": "two", "sync": "one"})
        preserved(root, original)

        root, actor, remote = fixture("continued-race")
        original = snapshot(root)
        rejected(lambda: publish(root, "build", "main", lambda attempt: update(actor, build=str(attempt))), "exhausted 3")
        assert text_git(remote, "rev-list", "--count", "main") == "4"
        assert text_git(remote, "show", "main:artifact/ai-agent-build.txt") == "old-build"
        preserved(root, original)

        root, actor, remote = fixture("push-permission")
        original = snapshot(root)
        (remote / "hooks/pre-receive").write_text("#!/bin/sh\necho ai-agent-secret >&2\nexit 1\n", encoding="utf-8")
        (remote / "hooks/pre-receive").chmod(0o755)
        rejected(lambda: publish(root, "build", "main"), "push failed without branch advancement")
        assert text_git(remote, "rev-list", "--count", "main") == "1"
        preserved(root, original)

        root, actor, remote = fixture("push-network")
        original = snapshot(root)
        run = subprocess.run

        def interrupted(command, **kwargs):
            if "push" in command:
                raise subprocess.TimeoutExpired(command, 180, stderr=b"ai-agent-secret")
            return run(command, **kwargs)

        with patch(__name__ + ".subprocess.run", side_effect=interrupted):
            rejected(lambda: publish(root, "build", "main"), "Git push could not complete")
        assert text_git(remote, "rev-list", "--count", "main") == "1"
        preserved(root, original)

        for name, values, message in (
            ("invalid-result", {"invalid": True}, "build check failed"),
            ("tracked-stray", {"stray": "README.md"}, "outside the permitted"),
            ("untracked-stray", {"stray": "ai-agent-new.txt"}, "outside the permitted"),
            ("ignored-stray", {"stray": "ai-agent-ignored.txt"}, "outside the permitted"),
        ):
            root, actor, remote = fixture(name)
            update(actor, **values)
            original = snapshot(root)
            rejected(lambda: publish(root, "build", "main"), message)
            assert text_git(remote, "rev-list", "--count", "main") == "2"
            preserved(root, original)

        root, actor, remote = fixture("retry-invalid")
        original = snapshot(root)
        rejected(lambda: publish(root, "build", "main", lambda attempt: update(actor, invalid=True)), "build check failed")
        assert text_git(remote, "rev-list", "--count", "main") == "2"
        preserved(root, original)

        root, actor, remote = fixture("escaping-output")
        configuration = actor / "rule_sources/rules.build.json"
        configuration.write_text(json.dumps({"outputs": [{"path": "../ai-agent-escape.txt"}]}), encoding="utf-8")
        update(actor, build="escape")
        original = snapshot(root)
        rejected(lambda: publish(root, "build", "main"), "outside the permitted")
        assert not list(owned.rglob("ai-agent-escape.txt"))
        preserved(root, original)

        for environment in (
            {}, {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request", "GITHUB_REF": "refs/pull/1/merge"},
            {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request_target", "GITHUB_REF": "refs/heads/main"},
            {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "push", "GITHUB_REF": "refs/heads/feature"},
            {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "push", "GITHUB_REF": "refs/heads/main", "GITHUB_HEAD_REF": "feature"},
        ):
            with patch.dict(os.environ, environment, clear=True):
                rejected(require_ci, "trusted non-PR")
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "push", "GITHUB_REF": "refs/heads/main"}, clear=True):
            assert require_ci() == "main"
    print("Publish self-test passed: both modes, latest-source races, bounded failures, output boundaries and root preservation.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=SCOPES, nargs="?")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test and arguments.mode:
        parser.error("--self-test cannot be combined with a publication mode")
    if not arguments.self_test and not arguments.mode:
        parser.error("choose build/sync in CI, or --self-test locally")
    try:
        if arguments.self_test:
            self_test()
        else:
            publish(ROOT, arguments.mode, require_ci())
    except (PublishError, OSError, ValueError, UnicodeError) as exc:
        parser.exit(1, f"[ERROR] {exc}\n")


if __name__ == "__main__":
    main()
