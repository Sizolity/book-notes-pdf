# A Philosophy of Software Design（第 2 版）

Ousterhout《A Philosophy of Software Design, 2nd Edition》（Yaknyam Press）。

与前两本书不同：**这本是 EPUB，自带原生目录**，不存在"扫描 PDF 无大纲"的问题，所以本目录没有书签注入流程。

---

## 目录

```
apsod-2e/
├── README.md
├── source/APSOD-2e.epub   # 源文件（未入库）
├── en/                    # 逐章英文转换：33 md + assets/19
├── zh/                    # 中文译文：33 md + assets/19
└── extracts/              # 6 个早期按 part 切的纯文本，内容与 en/ 重叠
```

`en/` 与 `zh/` 文件名一一对应（`NN-<slug>.md`，NN 是 spine 顺序号），可直接并排对照。入口是各自的 `00-目录.md`。

`en/` 每个文件头部有 `<!-- source: partNNNN.xhtml -->`，可反查回 EPUB。
`zh/` 少一个 `03-copyright.md`（版权页未译）。

---

## 结构统计

曾按 `discrete-math-8e` / `linear-algebra-6e` 的 schema 生成过一份 `toc-apsod-2e.json`（156 条目），后因本目录不需要注入流程而删除。这里保留统计，需要时可从 EPUB 的 `toc.ncx` 重新生成。

| 段位 | 条目数 |
|---|---:|
| 章 | 22 |
| 节 | 124 |
| 前置 frontmatter | 5 |
| 后置 endmatter | 5 |
| **合计** | **156** |

生成时的两个要点：

- `toc.ncx` 本身**不带锚点**，156 条 src 全部只指向文件。节级锚点要从正文取：每章 XHTML 里小节标题是带 `id` 的段落元素，按 `id` 加文本前缀 `N.M` 配对，当时 124 个小节全部解析成功。
- 定位字段用 `href` + `spine` + `fragment`，替代前两本书的 `page` / `pdf_page` / `note` 三件套。EPUB 没有书页码与物理页的偏移问题，因此不存在 OFFSET 系数。

---

## 源文件指针

| 项 | 值 |
|---|---|
| 本机原始路径 | `C:\Users\huchao\Downloads\A Philosophy of Software Design (John K. Ousterhout) (z-library.sk, 1lib.sk, z-lib.sk).epub` |
| 大小 | 2736155 字节 |
| sha256 | `9f587b71073a53a7813f4048669ee80ec3183eedd8eeb43736add7601d6b3d21` |
| OPF | `content.opf`（根目录） |
| 章节文件 | `OEBPS/partNNNN.xhtml`，共 31 个 |

校验命令：

```bash
sha256sum /mnt/c/Users/huchao/Downloads/A\ Philosophy\ of\ Software\ Design*.epub
```

---

## 入库范围（已定）

根目录 `.gitignore` 已忽略 `*/en/`、`*/zh/`、`*/source/`、`*/extracts/` 以及 `*.epub` / `*.pdf` 等源文件格式。**本目录入库的只有本 README。**

理由：`en/`、`zh/`、`extracts/` 是整本书的正文与中文译文，`source/` 是整本 EPUB，都不适合推到远端；与 `discrete-math-8e`、`linear-algebra-6e` 的既有做法一致——那两个目录也只提交了脚本与 TOC JSON，从未提交源 PDF 或正文。

---

## 已知瑕疵

- `extracts/` 与 `en/` 内容重叠，可删。
- 曾考虑给 `cleancode-2e` 与本目录统一形状（分语言 `en/`、`zh/`），`cleancode-2e` 只有英文版，故只有 `en/`。
