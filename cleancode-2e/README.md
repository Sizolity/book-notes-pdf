# Clean Code: A Handbook of Agile Software Craftsmanship（第 2 版）

Robert C. Martin，2025 年第二版。

版次判定依据：37 章（第一版为 17 章），含 ch17 *AIs, LLMs, and God Knows What*、ch25 *Architectural Boundaries*、ch27 *The Clean Architecture*；EPUB 内 `dc:title` 为 "…Second Edition"，`dc:date` 2025。

---

## 目录

```
cleancode-2e/
├── README.md
├── en/                      # 逐章转换文本（未入库）
│   ├── 51 个 NN-<slug>.md
│   └── 36 个同名图片目录 / 120 张 jpg
└── source/                  # 源 EPUB（未入库）
    └── CleanCode-2e.epub
```

入口是 `en/` 下按编号排序的文件；`00-cover.md` 起，`50-bibliography.md` 止。

---

## 图片引用方式

正文用 HTML `<img src="章目录/文件名.jpg">` 引用书页图片，**不是** markdown 的 `![]()` 语法。全库共 121 处引用（120 个 `<img>` + 1 个 markdown 图片），全部可解析，无断链。

因此 `en/` 下的 md 与其同名图片目录**必须一起移动**，单独挪 md 会全部断链。

---

## 源文件指针

`source/` 与 `en/` 都不进版本库（见根目录 `.gitignore`），这里留校验信息以便换机器时确认是否同一份：

| 项 | 值 |
|---|---|
| 本机原始路径 | `C:\Users\huchao\Downloads\Clean Code A Handbook of Agile Software Craftsmanship - Second Edition (Robert C. Martin) (z-library.sk, 1lib.sk, z-lib.sk).epub` |
| 大小 | 17605338 字节 |
| sha256 | `0c8dffd9585c89704a1d111d0f37b2cab2614a33f6ccaa7eeb6847fe234635a6` |
| 内部结构 | 37 个 `OEBPS/chNN.html` + 120 张图，OPF 为 `OEBPS/9780135398586.opf` |

校验命令：

```bash
sha256sum /mnt/c/Users/huchao/Downloads/Clean\ Code*Second\ Edition*.epub
```

注：Downloads 里另有一个 `Clean Code.epub`，与上面这份 **md5 相同**，是同一文件的副本；还有一个 4.2 MB 的 `dc:date` 2008 版本，那是**第一版**，不要混用。

---

## 已知瑕疵

51 个文件的章标题里残留 HTML：形如 `## <span class="ash">Chapter 5</span>. Comments`。Typora 会正常渲染，但大纲面板的条目文字会带上标签内容。清理是一条 sed 的事，尚未执行。

---

## 与仓库其他条目的差异

`discrete-math-8e` 与 `linear-algebra-6e` 处理的是**无内嵌大纲的扫描 PDF**，所以配了 TOC JSON 与书签注入脚本。这本是 EPUB，自带原生目录，不需要注入流程，因此本目录没有脚本与 JSON，只有说明与（本地）转换文本。
