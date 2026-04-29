"""校对辅助脚本：

用法：
  python toc-proofread.py list             # 列出所有 page=null 的条目（按章分组）
  python toc-proofread.py list 1           # 只列第 1 章的待校对项
  python toc-proofread.py set <id> <pg>    # 回填一条页码，例 set 1.7.6 75
  python toc-proofread.py set <id> null    # 还原为 null
  python toc-proofread.py title <id> <新标题>  # 改单条标题
  python toc-proofread.py apply            # 从 toc-proofread-checklist.txt 批量回灌
  python toc-proofread.py stats            # 统计还剩多少 null
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

DOC = Path(__file__).with_name("toc-discrete-math-8e.json")


def load() -> dict:
    return json.loads(DOC.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    DOC.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def items_missing(data: dict, ch: int | None = None):
    return [
        i for i in data["items"]
        if i["page"] is None
        and i["type"] not in ("frontmatter",)
        and (ch is None or i.get("chapter") == ch)
    ]


def cmd_list(argv):
    data = load()
    ch = int(argv[0]) if argv else None
    missing = items_missing(data, ch)
    if not missing:
        print(f"✅ 第 {ch} 章" if ch else "✅ 全书", "无待校对条目")
        return
    last_chap = None
    for it in missing:
        if it.get("chapter") != last_chap:
            last_chap = it.get("chapter")
            print()
            print(f"==== 第 {last_chap} 章 ====" if last_chap else "==== 附录 / 其他 ====")
        print(f"  [ ] {it['id']:<12} {it['title']}")
    print()
    print(f"共 {len(missing)} 处待校对")


def cmd_set(argv):
    if len(argv) < 2:
        print("usage: set <id> <page|null>")
        sys.exit(1)
    target_id, raw_page = argv[0], argv[1]
    page = None if raw_page.lower() == "null" else int(raw_page)

    data = load()
    for it in data["items"]:
        if it["id"] == target_id:
            old = it["page"]
            it["page"] = page
            save(data)
            print(f"✓ {target_id}  page: {old} → {page}  ({it['title']})")
            return
    print(f"✗ id 不存在: {target_id}")
    sys.exit(1)


def cmd_title(argv):
    if len(argv) < 2:
        print("usage: title <id> <新标题>")
        sys.exit(1)
    target_id, new_title = argv[0], " ".join(argv[1:])
    data = load()
    for it in data["items"]:
        if it["id"] == target_id:
            old = it["title"]
            it["title"] = new_title
            save(data)
            print(f"✓ {target_id}  title: {old!r} → {new_title!r}")
            return
    print(f"✗ id 不存在: {target_id}")
    sys.exit(1)


def cmd_stats(argv):
    data = load()
    total = len(data["items"])
    null_total = sum(1 for i in data["items"] if i["page"] is None)
    null_real = sum(
        1 for i in data["items"]
        if i["page"] is None and i["type"] not in ("frontmatter",)
    )
    print(f"total items     : {total}")
    print(f"null pages (all): {null_total}")
    print(f"null pages (须校对，剔除前置/封底等): {null_real}")


def cmd_apply(argv):
    """从 toc-proofread-checklist.txt 批量回灌页码。

    解析规则：每非空非注释行格式为 `<id> <page>`，page 可以是：
      - 数字（如 75）→ 写入 page
      - "?"           → 跳过（仍未确认）
      - "null"        → 强制写 null
    后面允许带 `# 注释` 任意尾巴。
    """
    src = Path(argv[0]) if argv else Path(__file__).with_name("toc-proofread-checklist.txt")
    if not src.exists():
        print(f"找不到清单文件：{src}")
        sys.exit(1)
    data = load()
    by_id = {i["id"]: i for i in data["items"]}
    updated = skipped = unknown = 0
    for ln, raw in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        target_id, raw_page = parts[0].strip(), parts[1].strip()
        if raw_page in ("?", ""):
            skipped += 1
            continue
        if target_id not in by_id:
            print(f"  ! L{ln}: 未知 id {target_id}")
            unknown += 1
            continue
        page = None if raw_page.lower() == "null" else int(raw_page)
        old = by_id[target_id]["page"]
        if old != page:
            by_id[target_id]["page"] = page
            updated += 1
            print(f"  ✓ {target_id:<22} {old} → {page}   {by_id[target_id]['title']}")
    if updated:
        save(data)
    print()
    print(f"updated={updated}  skipped(?)={skipped}  unknown={unknown}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd, argv = sys.argv[1], sys.argv[2:]
    {
        "list": cmd_list,
        "set": cmd_set,
        "title": cmd_title,
        "stats": cmd_stats,
        "apply": cmd_apply,
    }.get(cmd, lambda _: print(f"unknown cmd: {cmd}"))(argv)


if __name__ == "__main__":
    main()
