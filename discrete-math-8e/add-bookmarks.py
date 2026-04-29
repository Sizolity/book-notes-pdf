"""把 toc-discrete-math-8e.json 注入为 PDF outline（书签），并就地覆盖原 PDF。

输入（环境变量；不设置时取默认值，对应"中文 8 版扫描 PDF + Windows Downloads 目录"）：
  PDF_SRC            原 PDF 绝对路径（容器内）。默认：
                     /work/downloads/Chi San Shu Xue Ji Qi Ying Yong (Yuan Shu Di 8Ban )...rosen).pdf
  PDF_COPY           带书签副本的输出路径（容器内）。默认：
                     /work/downloads/Chi-San-Shu-Xue-bookmarked.pdf
  TOC_OFFSET         book_page → pdf_page 偏移；默认 31

说明：
  - JSON 与脚本同目录，使用 __file__ 自定位
  - 普通条目按 (page + OFFSET) 计算 PDF 物理页；frontmatter / backmatter 优先用 pdf_page 字段
  - 含 note 字段的条目被跳过（用于扫描版未收录的目录条目，如本书的"奇数编号练习答案"）

容器运行模板（在工具目录里）：

  docker run --rm \\
    -v "C:\\Users\\huchao\\Downloads:/work/downloads" \\
    -v "%CD%:/work/lrmp" \\
    python:3.12-slim bash -lc \\
      "pip install -q pymupdf && python /work/lrmp/add-bookmarks.py"
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import fitz  # PyMuPDF

JSON_DOC = Path(__file__).with_name("toc-discrete-math-8e.json")

PDF_SRC = Path(os.environ.get(
    "PDF_SRC",
    "/work/downloads/Chi San Shu Xue Ji Qi Ying Yong (Yuan Shu Di 8Ban ) - Ken Ni Si  H.Luo Sen  (kenneth H.rosen).pdf",
))
PDF_COPY = Path(os.environ.get(
    "PDF_COPY",
    "/work/downloads/Chi-San-Shu-Xue-bookmarked.pdf",
))
OFFSET = int(os.environ.get("TOC_OFFSET", "31"))


def label(it: dict) -> str:
    """生成书签显示名。"""
    typ = it["type"]
    if typ == "chapter":
        return f"第 {it['chapter']} 章 {it['title']}"
    if typ == "appendix":
        return f"附录 {it['id']} {it['title']}"
    if typ in ("section", "subsection"):
        return f"{it['id']} {it['title']}"
    if typ == "exercises":
        return f"{it['parent_id']} 练习"
    return it["title"]  # endmatter / frontmatter


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

    # PyMuPDF 强制要求：第一条 level=1，且 level 不能跨级跳（+1 以上）
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
    shutil.copy2(PDF_COPY, PDF_SRC)
    print(f"  原 PDF 现在 {PDF_SRC.stat().st_size:,} 字节")

    print("\n=== 验证 ===")
    for path in (PDF_SRC, PDF_COPY):
        d = fitz.open(path)
        outline = d.get_toc()
        print(f"  {path.name}  outline={len(outline)}  pages={len(d)}")
        d.close()


if __name__ == "__main__":
    main()
