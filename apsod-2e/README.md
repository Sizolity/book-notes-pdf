# A Philosophy of Software Design（第 2 版）

Ousterhout《A Philosophy of Software Design, 2nd Edition》（Yaknyam Press）。

与前两本书不同：**这本是 EPUB，自带原生目录**，不存在"扫描 PDF 无大纲"的问题，所以本目录没有书签注入流程，只有结构数据 + 转换文本。

---

## 目录

```
apsod-2e/
├── README.md
├── toc-apsod-2e.json      # 目录结构数据（156 条目）
├── source/APSOD-2e.epub   # 源文件副本（2.7M）
├── en/                    # 逐章英文转换：33 md + assets/19
├── zh/                    # 中文译文：33 md + assets/19
└── extracts/              # 6 个早期按 part 切的纯文本
```

`en/` 与 `zh/` 文件名一一对应（`NN-<slug>.md`，NN 是 spine 顺序号），可直接并排对照。入口是各自的 `00-目录.md`。

`en/` 每个文件头部有 `<!-- source: partNNNN.xhtml -->`，可反查回 EPUB。
`zh/` 少一个 `03-copyright.md`（版权页未译）。

---

## 数据格式：`toc-apsod-2e.json`

与 `discrete-math-8e` / `linear-algebra-6e` 同为扁平数组 `items[]` + `parent_id` 重建层级，但定位字段不同：

| 字段 | 含义 |
|---|---|
| `id` | 层级编号：`4` / `4.3` / `frontmatter.preface` |
| `type` | `chapter` / `section` / `frontmatter` / `endmatter` |
| `level` | 1 = 章、前置、后置；2 = 节 |
| `title` | 英文原标题 |
| `parent_id` | 父节点；章、前置、后置为 null |
| `chapter` | 归属章号 |
| `href` | EPUB 内部文件，例 `OEBPS/part0008.xhtml` |
| `spine` | OPF spine 序号，定位所在文件 |
| `fragment` | 章内锚点，仅 section 携带 |

替代了前两本书的 `page` / `pdf_page` / `note` 三件套——EPUB 没有书页码与物理页的偏移问题，也就没有 OFFSET 系数。

`toc.ncx` 本身不带锚点（156 条 src 全部只指向文件），所以 `fragment` 是解析正文得到的：每章 XHTML 里小节标题是带 `id` 的段落元素，按 `id` 加文本前缀 `N.M` 配对。当前 **124 个小节全部解析成功**，`href` 加 `fragment` 可直接深链到节。

条目分布：章 22 / 节 124 / 前置 5 / 后置 5，合计 156。

---

## 为什么没有 add-bookmarks.py 和 proofread.py

EPUB 阅读器直接消费内嵌 NCX，无需外部注入；也没有需要人工回填的页码。JSON 是一次性生成的静态数据，改条目时直接改 JSON。

---

## 提交前请注意

本目录含**整本书的转换文本与中文译文**（8.8M）。仓库远端是 `git@github.com:Sizolity/book-notes-pdf.git`，而另外两本书只提交了脚本与结构数据，没有提交书本文字。

若不想把这些内容推到远端，二选一：

- 加 `.gitignore` 忽略 `en/`、`zh/`、`source/`、`extracts/`，只提交 `README.md` 与 `toc-apsod-2e.json`；
- 或整个 `apsod-2e/` 不提交。

---

## 已知边界

- `spine` 为 null 表示该条目未出现在 spine 中（封面之类），不是数据缺失。
- `fragment` 只在 `type=section` 上有值；章条目为 null，因为章与节同文件，章级定位靠 `href` 即可。
- JSON 由 EPUB 的 `toc.ncx` 加正文 id 生成一次，没有配套脚本；EPUB 换版本需重新生成。
- `extracts/` 是早期按 EPUB part 切的纯文本，内容与 `en/` 重叠，可删。
