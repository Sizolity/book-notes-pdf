# Introduction to Linear Algebra（第 6 版，清华影印）— PDF 书签工具集

把扫描版 PDF（无文本层、无内置大纲）改造成带层级书签的可导航文档。

源书：Gilbert Strang《Introduction to Linear Algebra, Sixth Edition》（Wellesley-Cambridge Press, 2023）；清华大学出版社影印（ISBN 978-7-302-66807-7，2024.7）。正文为英文。

---

## 目录

```
linear-algebra-6e/
├── README.md
├── toc-linear-algebra-6e.json   # 目录数据
├── build_toc_json.py            # 生成 JSON（改条目时先改这里）
├── print-tree.py                # 树状打印目录
├── proofread.py                 # 校对辅助
└── add-bookmarks.py             # 把 JSON 注入为 PDF outline
```

---

## 数据格式

与 `discrete-math-8e` 相同：扁平数组 `items[]`，用 `parent_id` 重建层级。

- `page` / `pdf_page` / `note` 三者优先级：含 `note` → 跳过；否则有 `pdf_page` → 直接用；否则 `page + OFFSET`
- 封面 / 书名页 / 版权 / 前言 / 目录 / 封底使用 `pdf_page`
- `type=exercises` 对应各节 **Problem Set**

---

## 偏移系数

```
PDF_page = book_page + OFFSET   (OFFSET = 11)
```

- 扫描 PDF 共 **442** 页
- PDF 1–3：彩色封面 / 书名页 / 版权
- PDF 4–9：Preface i–vi
- PDF 10–11：Contents vii–viii
- PDF 12 = 书第 1 页（第 1 章）
- PDF 442：封底

校验：第 1 章（书 1 / PDF 12）、第 2 章（39 / 50）、第 7 章（286 / 297）、Appendix 1（400 / 411）、Index（423 / 434）。

Appendix 10 正文从书页 **414** 开始（413 仍是 A9）。

---

## 注入书签

依赖 `pymupdf`。本机环境若有问题，用 Docker：

```powershell
$env:PDF_SRC  = "$env:USERPROFILE\Downloads\线性代数 (第6版).pdf"
$env:PDF_COPY = "$env:USERPROFILE\Downloads\Introduction-to-Linear-Algebra-6e-bookmarked.pdf"
$env:TOC_OFFSET = "11"

docker run --rm `
  -v "$env:USERPROFILE\Downloads:/work/downloads" `
  -v "${PWD}:/work/lrmp" `
  -e TOC_OFFSET=11 `
  python:3.12-slim bash -lc `
    "pip install -q pymupdf && python /work/lrmp/add-bookmarks.py"
```

脚本会先写完整副本到 `PDF_COPY`，再用副本覆盖 `PDF_SRC`。若原 PDF 被 Edge / Acrobat / WPS 占用，第 3 步会 `PermissionError`：先关掉占用进程再重跑（副本已写好）。

---

## 打印目录树

```powershell
python print-tree.py          # 章 / 节 / 附录 / 索引
python print-tree.py --all    # 加上 Problem Set
```
