# Clean Code: A Handbook of Agile Software Craftsmanship（第 2 版）

Robert C. Martin，第二版。

版次判定依据：37 章（第一版为 17 章），含 ch17 *AIs, LLMs, and God Knows What*、ch25 *Architectural Boundaries*、ch27 *The Clean Architecture*；EPUB 内 `dc:title` 含 "Second Edition"，`dc:date` 为 2025。

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

## 已知瑕疵

51 个文件的章标题里残留 HTML：形如 `## <span class="ash">Chapter 5</span>. Comments`。Typora 会正常渲染，但大纲面板的条目文字会带上标签内容。清理是一条 sed 的事，尚未执行。

---

## 与仓库其他条目的差异

`discrete-math-8e` 与 `linear-algebra-6e` 处理的是**无内嵌大纲的扫描 PDF**，所以配了 TOC JSON 与书签注入脚本。这本是 EPUB，自带原生目录，不需要注入流程，因此本目录没有脚本与 JSON，只有说明与（本地）转换文本。
