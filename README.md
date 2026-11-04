# book-notes-pdf — 书籍导航工具集与目录结构数据

为**没有内嵌大纲的扫描版 PDF**构建层级书签，以及为**自带目录的 EPUB**记录结构数据。

本仓库只包含脚本、目录结构数据（JSON）和文档。**不包含任何书籍正文，不包含任何书籍原件。**

---

## 四本书

| 目录 | 书名 | 版次与出版信息 | 源文件形态 | 入库内容 |
|---|---|---|---|---|
| `discrete-math-8e/` | 离散数学及其应用 | Rosen 8E 中文版，机械工业出版社，徐六通 等译，2019.10 | 扫描 PDF，无文本层、无大纲 | README + 3 脚本 + TOC JSON（611 条目 → 注入 610 条书签，1 条标记跳过） |
| `linear-algebra-6e/` | Introduction to Linear Algebra | Strang 6E，Wellesley-Cambridge Press 2023（978-1-7331466-7-8）；清华大学出版社影印（978-7-302-66807-7，2024.7） | 扫描 PDF，无大纲 | README + 4 脚本 + TOC JSON（110 条目） |
| `apsod-2e/` | A Philosophy of Software Design | 2nd Edition，Yaknyam Press，2021-07-25 | EPUB，自带原生目录 | README |
| `cleancode-2e/` | Clean Code: A Handbook of Agile Software Craftsmanship | 2nd Edition，Pearson，2025，ISBN 9780135398586 | EPUB，自带原生目录 | README |

前两本走"注入书签"流程（`add-bookmarks.py` + OFFSET 定位），后两本不需要，只记录结构与校验信息。

---

## 源文件说明

四本书的原件（两个扫描 PDF、两个 EPUB）**都不在本仓库内**，由根目录 `.gitignore` 排除：

```
*/en/  */zh/  */source/  */extracts/
*.epub  *.pdf  *.mobi  *.azw3  *.7z
```

它们是维护者留在本机用于阅读与学习的副本，存放于 `C:\Users\huchao\Downloads\`。本仓库不存储、不镜像、不传播这些文件，也不提供获取它们的下载点。

登记校验值只为一个目的：**换机器或文件被改动后，能确认是不是同一份**。

| 书 | 大小 | sha256 |
|---|---:|---|
| 离散数学及其应用 8E（PDF） | 448940605 | `f8f4b3fe9a4f0a728412d91f17352e1d688db3cd5140b6188940c0efc8eb07ea` |
| Introduction to Linear Algebra 6E（PDF） | 201475187 | `f5927a1af6c0ed0b25a7984899a7cd96e02e05e7c93decf24e58a59fccb2c664` |
| A Philosophy of Software Design 2E（EPUB） | 2736155 | `9f587b71073a53a7813f4048669ee80ec3183eedd8eeb43736add7601d6b3d21` |
| Clean Code 2E（EPUB） | 17605338 | `0c8dffd9585c89704a1d111d0f37b2cab2614a33f6ccaa7eeb6847fe234635a6` |

两个 PDF 的体积（428.1 MiB 与 192.1 MiB）本身也超过 GitHub 的 100 MB 单文件限制，无法直接提交；两个 EPUB（2.6 MiB 与 16.8 MiB）不超限，不入库是出于版权而非容量。

---

## 版权与许可

- **书籍著作权归原作者与出版社所有。** 本仓库对书籍内容不主张任何权利。
- 本仓库的 **MIT 许可证只覆盖仓库内的脚本、JSON 数据与文档**，不构成对任何书籍正文、图片或原件的使用授权。
- 各目录 README 中记录的书名、作者、出版社、版次、ISBN、章节标题，属于书目元数据，用于标识对象本身。
- 若权利人认为本仓库中的元数据条目需要调整或移除，提 issue 说明即可处理；这些条目不涉及书籍正文，删除不影响工具部分。

---

## 各目录入口

- `discrete-math-8e/README.md` — 数据格式、OFFSET=31 的推导、Docker 旁路注入、610 条书签的构成
- `linear-algebra-6e/README.md` — OFFSET=11、442 页分段对照、注入命令
- `apsod-2e/README.md` — 156 条结构统计、节级锚点的取法、源 EPUB 校验
- `cleancode-2e/README.md` — 版次判定依据、121 处图片引用机制、已知 `<span>` 残留

---

## 环境依赖

- Python 3.12（脚本无第三方依赖，除 `add-bookmarks.py` 需要 `pymupdf`）
- `pymupdf` 若本机装不上，走 Docker：见各目录 README 的 `docker run` 段
- 注入结果（`*-bookmarked.pdf`）同样不入库
