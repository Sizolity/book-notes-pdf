"""把 toc-linear-algebra-6e.json 注入为 PDF outline（书签），并就地覆盖原 PDF。

输入（环境变量）：
  PDF_SRC            必填，原 PDF 在容器内的绝对路径；脚本会就地覆盖该文件
  PDF_COPY           带书签副本的输出路径（容器内）
  TOC_OFFSET         book_page → pdf_page 偏移；默认 11（PDF p.12 = 书 p.1）

说明：
  - JSON 与脚本同目录，使用 __file__ 自定位
  - 普通条目按 (page + OFFSET) 计算 PDF 物理页；frontmatter / 封底优先用 pdf_page
  - 含 note 字段的条目被跳过

容器运行模板（在本目录里，Windows PowerShell）：

  docker run --rm `
    -v "$env:USERPROFILE\\Downloads:/work/downloads" `
    -v "${PWD}:/work/lrmp" `
    -e TOC_OFFSET=11 `
    python:3.12-slim bash -lc `
      "pip install -q pymupdf && python /work/lrmp/add-bookmarks.py"
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import fitz  # PyMuPDF

JSON_DOC = Path(__file__).with_name("toc-linear-algebra-6e.json")

src_env = os.environ.get("PDF_SRC")
if not src_env:
    raise SystemExit("PDF_SRC must be set: absolute path of the source PDF inside the container")
PDF_SRC = Path(src_env)
PDF_COPY = Path(os.environ.get(
    "PDF_COPY",
    "/work/downloads/Introduction-to-Linear-Algebra-6e-bookmarked.pdf",
))
OFFSET = int(os.environ.get("TOC_OFFSET", "11"))


def label(it: dict) -> str:
    """生成书签显示名。"""
    typ = it["type"]
    if typ == "chapter":
        return f"{it['chapter']} {it['title']}"
    if typ == "appendix":
        n = it["id"][1:] if str(it["id"]).startswith("A") else it["id"]
        return f"Appendix {n} {it['title']}"
    if typ in ("section", "subsection"):
        return f"{it['id']} {it['title']}"
    if typ == "exercises":
        return f"Problem Set {it['parent_id']}"
    return it["title"]  # frontmatter / endmatter


def level_of(it: dict) -> int | None:
    """映射到 PyMuPDF 期望的层级（1=最浅）。"""
    typ = it["type"]
    if typ in ("chapter", "appendix", "frontmatter"):
        return 1
    if typ in ("section", "endmatter"):
        return 2
    if typ in ("subsection", "exercises"):
        return 3
    return None


def pdf_page_of(it: dict) -> int | None:
    """优先 pdf_page（直接 PDF 物理页），否则 book page + offset。"""
    if it.get("pdf_page") is not None:
        return int(it["pdf_page"])
    if it.get("page") is not None:
        return int(it["page"]) + OFFSET
    return None


def main() -> None:
    data = json.loads(JSON_DOC.read_text(encoding="utf-8"))
    items = data["items"]

    doc = fitz.open(PDF_SRC)
    n_pages = len(doc)
    print(f"PDF: {PDF_SRC.name}  ({n_pages} 页)")

    toc: list[list] = []
    skipped_no_page = skipped_with_note = skipped_out_of_range = 0
    for it in items:
        if it.get("note"):
            print(f"  - 跳过（note）: {it['id']}  {it['title']}")
            skipped_with_note += 1
            continue
        lvl = level_of(it)
        if lvl is None:
            skipped_no_page += 1
            continue
        pdf_p = pdf_page_of(it)
        if pdf_p is None:
            skipped_no_page += 1
            continue
        if pdf_p < 1 or pdf_p > n_pages:
            print(f"  ! 跳过越界: {it['id']}  →  PDF p.{pdf_p}")
            skipped_out_of_range += 1
            continue
        toc.append([lvl, label(it), pdf_p])

    print(
        f"将写入 {len(toc)} 条书签 "
        f"（跳过：无页码 {skipped_no_page}，note {skipped_with_note}，越界 {skipped_out_of_range}）"
    )

    prev_lvl = 0
    for i, (lvl, t, p) in enumerate(toc):
        if lvl > prev_lvl + 1:
            raise RuntimeError(
                f"层级跳跃 @ idx={i}: {prev_lvl} → {lvl}  "
                f"({t!r} p.{p})。前一条目: {toc[i-1] if i else None}"
            )
        prev_lvl = lvl

    doc.set_toc(toc)

    PDF_COPY.parent.mkdir(parents=True, exist_ok=True)
    print(f"输出副本 → {PDF_COPY}")
    doc.save(PDF_COPY, garbage=0, deflate=False, clean=False, pretty=False)
    doc.close()
    print(f"  副本 {PDF_COPY.stat().st_size:,} 字节")

    print(f"用副本覆盖原 PDF → {PDF_SRC}")
    overwritten = True
    try:
        shutil.copy2(PDF_COPY, PDF_SRC)
        print(f"  原 PDF 现在 {PDF_SRC.stat().st_size:,} 字节")
    except PermissionError:
        overwritten = False
        print("  ! 原 PDF 被占用，无法覆盖。请关闭阅读器后把副本复制回去，或直接用副本。")

    print("\n=== 验证 ===")
    paths = [PDF_COPY] if not overwritten else (PDF_SRC, PDF_COPY)
    for path in paths:
        d = fitz.open(path)
        outline = d.get_toc()
        print(f"  {path.name}  outline={len(outline)}  pages={len(d)}")
        if path == PDF_COPY:
            print("  前 8 条:")
            for row in outline[:8]:
                print(f"    {row}")
            print("  后 6 条:")
            for row in outline[-6:]:
                print(f"    {row}")
        d.close()


if __name__ == "__main__":
    main()
