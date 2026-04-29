# 离散数学及其应用（原书第 8 版）— PDF 书签工具集

把扫描版 PDF（无文本层、无内置大纲）改造成带 **610 条层级书签** 的可导航文档。

源书：Kenneth H. Rosen《Discrete Mathematics and Its Applications, 8E》中文版（机械工业出版社，徐六通 等 译，2019.10）。

---

## 目录

```
discrete-math-8e/
├── README.md                       # 本文件
├── toc-discrete-math-8e.json       # 目录数据（611 条目）
├── print-tree.py                   # 树状打印目录
├── proofread.py                    # 校对辅助：填页码 / 改标题 / 批量回灌
└── add-bookmarks.py                # 把 JSON 注入为 PDF outline
```

---

## 数据格式：`toc-discrete-math-8e.json`

扁平数组 `items[]`，便于自动化遍历；通过 `parent_id` 重建层级。

```jsonc
{
  "id": "1.4.10",
  "type": "subsection",        // chapter | section | subsection | exercises | endmatter | appendix | frontmatter
  "level": 3,                  // 1=章, 2=节, 3=小节
  "title": "语句到逻辑表达式的翻译",
  "page": 42,                  // 书页码（可能为 null：前置 / 扫描版未收录）
  "parent_id": "1.4",
  "chapter": 1,
  "pdf_page": null,            // 可选；若给出则直接作为 PDF 物理页（1-based），优先于 page+offset
  "note": null                 // 可选；非空表示扫描版未收录该条目，注入书签时跳过
}
```

字段约定：

- `page` / `pdf_page` / `note` 三者优先级：含 `note` → 跳过；否则有 `pdf_page` → 直接用；否则 `page + OFFSET`（OFFSET 默认 31，即 PDF 第 32 页 = 书第 1 页）
- 前置 7 项（出版者的话 / 译者序 / 前言 / 在线资源 / 致学生 / 作者简介 / 符号表）和后置（推荐读物 / 参考文献）使用 `pdf_page`，因为它们没有阿拉伯数字书页码
- `奇数编号练习答案` 在中文 8 版扫描 PDF 中未收录（附录 C 后直接进入推荐读物），因此被打上 `note` 跳过

---

## 工具一：树状打印 — `print-tree.py`

```powershell
# 仅章/节/小节
python print-tree.py

# 包含练习与章末附属（关键术语、复习题、补充练习、计算机课题、写作课题）
python print-tree.py --all
```

输出形如：

```
第1章 基础：逻辑和证明 ... 1
    |-- 1.1 命题逻辑 ... 1
        |-- 1.1.1 引言 ... 1
        |-- 1.1.2 命题 ... 1
        ...
```

---

## 工具二：校对 — `proofread.py`

```powershell
# 列出所有待校对的 page=null 条目（按章分组）
python proofread.py list
python proofread.py list 1                  # 只看第 1 章

# 单条修改
python proofread.py set 1.7.6 75            # 回填页码
python proofread.py set 1.7.6 null          # 还原为 null
python proofread.py title 12.4.4 "新标题"   # 改标题（处理 OCR 噪音 / em-dash 等）

# 批量回灌（从同目录下的 toc-proofread-checklist.txt）
python proofread.py apply
python proofread.py apply path\to\my-list.txt

# 统计
python proofread.py stats
```

`apply` 解析的清单文件格式（每行）：

```
1.7.6 75            # 数字 → 写入 page
2.3.4 ?             # ? → 跳过（仍未确认）
backmatter.refs null # null → 强制写 null
# 以 # 起始的行视为注释
```

---

## 工具三：注入书签 — `add-bookmarks.py`

依赖 `pymupdf`，本机环境若有问题，**推荐 Docker 旁路**（参见下方）。

### 直接运行（本机有 pymupdf 时）

```powershell
$env:PDF_SRC  = "C:\path\to\source.pdf"
$env:PDF_COPY = "C:\path\to\source-bookmarked.pdf"
$env:TOC_OFFSET = "31"      # 默认 31，即 PDF p.32 = book p.1
python add-bookmarks.py
```

### Docker 运行（推荐）

在工具目录（即本目录）执行：

```powershell
# 把 Downloads 挂到 /work/downloads，把当前工具目录挂到 /work/lrmp
docker run --rm `
  -v "C:\Users\huchao\Downloads:/work/downloads" `
  -v "${PWD}:/work/lrmp" `
  python:3.12-slim bash -lc `
    "pip install -q pymupdf && python /work/lrmp/add-bookmarks.py"
```

脚本默认读：

- `PDF_SRC`  = `/work/downloads/Chi San Shu Xue Ji Qi Ying Yong (Yuan Shu Di 8Ban ) - Ken Ni Si  H.Luo Sen  (kenneth H.rosen).pdf`
- `PDF_COPY` = `/work/downloads/Chi-San-Shu-Xue-bookmarked.pdf`

要换书或改路径，在 `docker run` 里加 `-e PDF_SRC=... -e PDF_COPY=... -e TOC_OFFSET=...`。

### 行为

1. 读 JSON，按 `note / pdf_page / page+OFFSET` 计算每条 PDF 物理页
2. 写完整副本到 `PDF_COPY`（约 449 MB）
3. 用副本 `shutil.copy2` 覆盖 `PDF_SRC`（实现"原地加书签"）
4. 重新打开两份 PDF 校验 outline 条目数与总页数

如果 `PDF_SRC` 被某 GUI 占用（Edge / Acrobat / WPS / SumatraPDF 等），第 3 步会 `PermissionError`。**先关掉占用进程**再重跑即可（副本已写入，不需要重算）。

---

## 偏移系数与定位约定

```
PDF_page = book_page + OFFSET   (OFFSET = 31)
```

- 中文 8 版扫描 PDF 共 854 页
- 前 31 页为：封面 / 版权 / 出版者的话 / 译者序 / 前言 / 在线资源 / 致学生 / 作者简介 / 符号表 / 目录 ⇒ 这部分使用 `pdf_page` 字段（绝对页号）
- 第 32 页起 = 第 1 章正文（书页码 1）⇒ 使用 `page + OFFSET`

OFFSET=31 的验证页：第 1 章首页（book 1）、第 7 章 `7.2.3`（book 403）、第 10 章 `10.7.exercises`（book 638）、第 12 章 `12.3.exercises`（book 729）等。

---

## 为别的书复用这套流程

1. 复制本目录为同级新目录（如 `_common/book-toc/<your-book>/`）
2. 改 `toc-<your-book>.json` 内容；脚本里 JSON 文件名是用 `Path(__file__).with_name(...)` 自定位的，**只需保持与脚本同目录**
3. `print-tree.py` / `proofread.py` 内部硬编码了 `toc-discrete-math-8e.json`，复用时一并改
4. `add-bookmarks.py` 走 `__file__.with_name("toc-discrete-math-8e.json")`，改成对应 JSON 文件名
5. 通过环境变量 `PDF_SRC` / `PDF_COPY` / `TOC_OFFSET` 指向新书

---

## 历史与来源

- 数据来源：原始 9 张目录扫描图 → OCR 提取 → 渲染 PDF p.23–31 高清图视觉重读 → 批量修正 78 处页码 / 5 处标题 / 1 处漏条目（`12.3.exercises`）
- 已知特殊处理：
  - `12.4.4` 标题里的 `EM DASH —` 改回 `HYPHEN-MINUS -`（OCR 噪音）
  - `4.1.5` 标题修正为「模 m 算术」（保留 m，原 OCR 漏识）
  - `9.1.4` 修正为「关系的性质」（原 OCR 与 9.1.3 重复成「关系的组合」）
  - `backmatter.answers`（奇数编号练习答案）：扫描版未收录，注入时跳过

最终注入：**610 条书签 / 854 页 PDF**。

| 段位 | 条目数 | 例 |
|---|---:|---|
| 前置 frontmatter | 7 | 出版者的话 → 符号表 |
| 章 / 节 / 小节 / 练习 / 章末附属 | 599 | 第 1 章 → 第 13 章 + endmatter |
| 附录 | 3 | A 实数和正整数的公理 / B 指数与对数函数 / C 伪代码 |
| 后置 backmatter | 2 | 推荐读物 / 参考文献 |
| **合计** | **610** | (`奇数编号练习答案` 跳过) |
