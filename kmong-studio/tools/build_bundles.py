"""Build single-file bundles from the kmong-studio docs.

- chrome/크몽_입점_작업지시서.md : Claude in Chrome runbook + profile/service copy appendices
- claude-project/뚝딱컷_운영본부_전체.md : every operating doc in one file for claude.ai project knowledge

Run after editing any source doc:  python3 kmong-studio/tools/build_bundles.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADER = "<!-- 자동 생성 파일입니다. 직접 고치지 말고 원본 문서를 고친 뒤 tools/build_bundles.py를 다시 실행하세요. -->\n\n"


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8").strip() + "\n"


def build_runbook():
    parts = [
        HEADER,
        read("chrome/_지시서_본문.md"),
        "\n# [부록 A] 프로필 원문 (02_프로필_세팅.md)\n\n",
        read("02_프로필_세팅.md"),
        "\n---\n\n# [부록 B] 서비스 등록 원문 (03_서비스_등록.md)\n\n",
        read("03_서비스_등록.md"),
        "\n---\n\n# [부록 C] 크몽 텍스트 원고 — 서비스 설명·가격 정보 (10_크몽_텍스트_원고.md)\n\n",
        read("10_크몽_텍스트_원고.md"),
    ]
    out = ROOT / "chrome/크몽_입점_작업지시서.md"
    out.write_text("".join(parts), encoding="utf-8")
    return out


def build_project_bundle():
    docs = sorted(ROOT.glob("[0-9][0-9]_*.md")) + sorted((ROOT / "portfolio").glob("*.md"))
    parts = [HEADER, "# 뚝딱컷 크몽 운영본부 — 전체 문서 합본\n\n", "## 목차\n"]
    parts += [f"- {d.relative_to(ROOT)}\n" for d in docs]
    for d in docs:
        parts += [f"\n\n---\n\n<!-- 원본: {d.relative_to(ROOT)} -->\n\n", d.read_text(encoding="utf-8").strip(), "\n"]
    out = ROOT / "claude-project/뚝딱컷_운영본부_전체.md"
    out.write_text("".join(parts), encoding="utf-8")
    return out


if __name__ == "__main__":
    for path in (build_runbook(), build_project_bundle()):
        print(f"built {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)")
