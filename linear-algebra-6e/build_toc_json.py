"""Generate toc-linear-algebra-6e.json (run once: python3 build_toc_json.py)."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).with_name("toc-linear-algebra-6e.json")

# (id, type, level, title, page, parent_id, chapter, pdf_page|None)
# page is printed book page; pdf_page is 1-based physical page when there is no arabic number.
ROWS: list[tuple] = [
    ("frontmatter.cover", "frontmatter", 1, "Cover", None, None, None, 1),
    ("frontmatter.title", "frontmatter", 1, "Title Page", None, None, None, 2),
    ("frontmatter.copyright", "frontmatter", 1, "Copyright", None, None, None, 3),
    ("frontmatter.preface", "frontmatter", 1, "Preface", None, None, None, 4),
    ("frontmatter.contents", "frontmatter", 1, "Contents", None, None, None, 10),
    ("1", "chapter", 1, "Vectors and Matrices", 1, None, 1, None),
    ("1.1", "section", 2, "Vectors and Linear Combinations", 2, "1", 1, None),
    ("1.1.exercises", "exercises", 3, "Problem Set 1.1", 6, "1.1", 1, None),
    ("1.2", "section", 2, "Lengths and Angles from Dot Products", 9, "1", 1, None),
    ("1.2.exercises", "exercises", 3, "Problem Set 1.2", 15, "1.2", 1, None),
    ("1.3", "section", 2, "Matrices and Their Column Spaces", 18, "1", 1, None),
    ("1.3.exercises", "exercises", 3, "Problem Set 1.3", 24, "1.3", 1, None),
    ("1.4", "section", 2, "Matrix Multiplication AB and CR", 27, "1", 1, None),
    ("1.4.exercises", "exercises", 3, "Problem Set 1.4", 35, "1.4", 1, None),
    ("2", "chapter", 1, "Solving Linear Equations Ax = b", 39, None, 2, None),
    ("2.1", "section", 2, "Elimination and Back Substitution", 40, "2", 2, None),
    ("2.1.exercises", "exercises", 3, "Problem Set 2.1", 46, "2.1", 2, None),
    ("2.2", "section", 2, "Elimination Matrices and Inverse Matrices", 49, "2", 2, None),
    ("2.2.exercises", "exercises", 3, "Problem Set 2.2", 53, "2.2", 2, None),
    ("2.3", "section", 2, "Matrix Computations and A = LU", 57, "2", 2, None),
    ("2.3.exercises", "exercises", 3, "Problem Set 2.3", 61, "2.3", 2, None),
    ("2.4", "section", 2, "Permutations and Transposes", 64, "2", 2, None),
    ("2.4.exercises", "exercises", 3, "Problem Set 2.4", 71, "2.4", 2, None),
    ("2.5", "section", 2, "Derivatives and Finite Difference Matrices", 74, "2", 2, None),
    ("2.5.exercises", "exercises", 3, "Problem Set 2.5", 81, "2.5", 2, None),
    ("3", "chapter", 1, "The Four Fundamental Subspaces", 84, None, 3, None),
    ("3.1", "section", 2, "Vector Spaces and Subspaces", 85, "3", 3, None),
    ("3.1.exercises", "exercises", 3, "Problem Set 3.1", 89, "3.1", 3, None),
    ("3.2", "section", 2, "Computing the Nullspace by Elimination: A = CR", 93, "3", 3, None),
    ("3.2.exercises", "exercises", 3, "Problem Set 3.2", 100, "3.2", 3, None),
    ("3.3", "section", 2, "The Complete Solution to Ax = b", 104, "3", 3, None),
    ("3.3.exercises", "exercises", 3, "Problem Set 3.3", 111, "3.3", 3, None),
    ("3.4", "section", 2, "Independence, Basis, and Dimension", 115, "3", 3, None),
    ("3.4.exercises", "exercises", 3, "Problem Set 3.4", 124, "3.4", 3, None),
    ("3.5", "section", 2, "Dimensions of the Four Subspaces", 129, "3", 3, None),
    ("3.5.exercises", "exercises", 3, "Problem Set 3.5", 137, "3.5", 3, None),
    ("4", "chapter", 1, "Orthogonality", 143, None, 4, None),
    ("4.1", "section", 2, "Orthogonality of Vectors and Subspaces", 144, "4", 4, None),
    ("4.1.exercises", "exercises", 3, "Problem Set 4.1", 148, "4.1", 4, None),
    ("4.2", "section", 2, "Projections onto Lines and Subspaces", 151, "4", 4, None),
    ("4.2.exercises", "exercises", 3, "Problem Set 4.2", 159, "4.2", 4, None),
    ("4.3", "section", 2, "Least Squares Approximations", 163, "4", 4, None),
    ("4.3.exercises", "exercises", 3, "Problem Set 4.3", 172, "4.3", 4, None),
    ("4.4", "section", 2, "Orthonormal Bases and Gram-Schmidt", 176, "4", 4, None),
    ("4.4.exercises", "exercises", 3, "Problem Set 4.4", 186, "4.4", 4, None),
    ("4.5", "section", 2, "The Pseudoinverse of a Matrix", 190, "4", 4, None),
    ("4.5.exercises", "exercises", 3, "Problem Set 4.5", 196, "4.5", 4, None),
    ("5", "chapter", 1, "Determinants", 198, None, 5, None),
    ("5.1", "section", 2, "3 by 3 Determinants and Cofactors", 199, "5", 5, None),
    ("5.1.exercises", "exercises", 3, "Problem Set 5.1", 203, "5.1", 5, None),
    ("5.2", "section", 2, "Computing and Using Determinants", 205, "5", 5, None),
    ("5.2.exercises", "exercises", 3, "Problem Set 5.2", 209, "5.2", 5, None),
    ("5.3", "section", 2, "Areas and Volumes by Determinants", 211, "5", 5, None),
    ("5.3.exercises", "exercises", 3, "Problem Set 5.3", 214, "5.3", 5, None),
    ("6", "chapter", 1, "Eigenvalues and Eigenvectors", 216, None, 6, None),
    ("6.1", "section", 2, "Introduction to Eigenvalues: Ax = λx", 217, "6", 6, None),
    ("6.1.exercises", "exercises", 3, "Problem Set 6.1", 226, "6.1", 6, None),
    ("6.2", "section", 2, "Diagonalizing a Matrix", 232, "6", 6, None),
    ("6.2.exercises", "exercises", 3, "Problem Set 6.2", 242, "6.2", 6, None),
    ("6.3", "section", 2, "Symmetric Positive Definite Matrices", 246, "6", 6, None),
    ("6.3.exercises", "exercises", 3, "Problem Set 6.3", 257, "6.3", 6, None),
    ("6.4", "section", 2, "Complex Numbers and Vectors and Matrices", 262, "6", 6, None),
    ("6.4.exercises", "exercises", 3, "Problem Set 6.4", 269, "6.4", 6, None),
    ("6.5", "section", 2, "Solving Linear Differential Equations", 270, "6", 6, None),
    ("6.5.exercises", "exercises", 3, "Problem Set 6.5", 280, "6.5", 6, None),
    ("7", "chapter", 1, "The Singular Value Decomposition (SVD)", 286, None, 7, None),
    ("7.1", "section", 2, "Singular Values and Singular Vectors", 287, "7", 7, None),
    ("7.1.exercises", "exercises", 3, "Problem Set 7.1", 295, "7.1", 7, None),
    ("7.2", "section", 2, "Image Processing by Linear Algebra", 297, "7", 7, None),
    ("7.2.exercises", "exercises", 3, "Problem Set 7.2", 301, "7.2", 7, None),
    ("7.3", "section", 2, "Principal Component Analysis (PCA by the SVD)", 302, "7", 7, None),
    ("7.3.exercises", "exercises", 3, "Problem Set 7.3", 307, "7.3", 7, None),
    ("8", "chapter", 1, "Linear Transformations", 308, None, 8, None),
    ("8.1", "section", 2, "The Idea of a Linear Transformation", 309, "8", 8, None),
    ("8.1.exercises", "exercises", 3, "Problem Set 8.1", 315, "8.1", 8, None),
    ("8.2", "section", 2, "The Matrix of a Linear Transformation", 318, "8", 8, None),
    ("8.2.exercises", "exercises", 3, "Problem Set 8.2", 324, "8.2", 8, None),
    ("8.3", "section", 2, "The Search for a Good Basis", 327, "8", 8, None),
    ("8.3.exercises", "exercises", 3, "Problem Set 8.3", 334, "8.3", 8, None),
    ("9", "chapter", 1, "Linear Algebra in Optimization", 335, None, 9, None),
    ("9.1", "section", 2, "Minimizing a Multivariable Function", 336, "9", 9, None),
    ("9.1.exercises", "exercises", 3, "Problem Set 9.1", 345, "9.1", 9, None),
    ("9.2", "section", 2, "Backpropagation and Stochastic Gradient Descent", 346, "9", 9, None),
    ("9.2.exercises", "exercises", 3, "Problem Set 9.2", 353, "9.2", 9, None),
    ("9.3", "section", 2, "Constraints, Lagrange Multipliers, Minimum Norms", 355, "9", 9, None),
    ("9.3.exercises", "exercises", 3, "Problem Set 9.3", 363, "9.3", 9, None),
    ("9.4", "section", 2, "Linear Programming, Game Theory, and Duality", 364, "9", 9, None),
    ("9.4.exercises", "exercises", 3, "Problem Set 9.4", 369, "9.4", 9, None),
    ("10", "chapter", 1, "Learning from Data", 370, None, 10, None),
    ("10.1", "section", 2, "Piecewise Linear Learning Functions", 372, "10", 10, None),
    ("10.1.exercises", "exercises", 3, "Problem Set 10.1", 380, "10.1", 10, None),
    ("10.2", "section", 2, "Creating and Experimenting", 381, "10", 10, None),
    ("10.2.exercises", "exercises", 3, "Problem Set 10.2", 385, "10.2", 10, None),
    ("10.3", "section", 2, "Mean, Variance, and Covariance", 386, "10", 10, None),
    ("10.3.exercises", "exercises", 3, "Problem Set 10.3", 398, "10.3", 10, None),
    ("A1", "appendix", 1, "The Ranks of AB and A + B", 400, None, None, None),
    ("A2", "appendix", 1, "Matrix Factorizations", 401, None, None, None),
    ("A3", "appendix", 1, "Counting Parameters in the Basic Factorizations", 403, None, None, None),
    ("A4", "appendix", 1, "Codes and Algorithms for Numerical Linear Algebra", 404, None, None, None),
    ("A5", "appendix", 1, "The Jordan Form of a Square Matrix", 405, None, None, None),
    ("A6", "appendix", 1, "Tensors", 406, None, None, None),
    ("A7", "appendix", 1, "The Condition Number of a Matrix Problem", 407, None, None, None),
    ("A8", "appendix", 1, "Markov Matrices and Perron-Frobenius", 408, None, None, None),
    ("A9", "appendix", 1, "Elimination and Factorization", 410, None, None, None),
    ("A10", "appendix", 1, "Computer Graphics", 414, None, None, None),
    ("backmatter.eqindex", "frontmatter", 1, "Index of Equations", 419, None, None, None),
    ("backmatter.notations", "frontmatter", 1, "Index of Notations", 422, None, None, None),
    ("backmatter.index", "frontmatter", 1, "Index", 423, None, None, None),
    ("backmatter.theorems", "frontmatter", 1, "Six Great Theorems of Linear Algebra", 430, None, None, None),
    ("backmatter.cover", "frontmatter", 1, "Back Cover", None, None, None, 442),
]


def main() -> None:
    items = []
    for id_, typ, level, title, page, parent_id, chapter, pdf_page in ROWS:
        it = {
            "id": id_,
            "type": typ,
            "level": level,
            "title": title,
            "page": page,
            "parent_id": parent_id,
            "chapter": chapter,
        }
        if pdf_page is not None:
            it["pdf_page"] = pdf_page
        items.append(it)

    ids = [it["id"] for it in items]
    if len(ids) != len(set(ids)):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        raise SystemExit(f"duplicate ids: {dup}")

    doc = {
        "metadata": {
            "title_zh": "线性代数（第6版）",
            "title_en": "Introduction to Linear Algebra",
            "edition": "6E",
            "publisher": "Tsinghua University Press / Wellesley-Cambridge Press",
            "isbn_zh": "978-7-302-66807-7",
            "isbn_en": "978-1-7331466-7-8",
            "extracted_at": "2026-08-19",
            "source": "书内 Contents（PDF p.10–11 / 书页 vii–viii）+ Problem Set 页码对照",
            "schema": {
                "id": "层级编号，例 '1' / '1.1' / '1.1.exercises' / 'frontmatter.preface'",
                "type": "chapter | section | exercises | appendix | frontmatter",
                "level": "1=章/附录/前置, 2=节, 3=Problem Set",
                "title": "英文标题（影印正文为英文）",
                "page": "起始书页码（int 或 null）",
                "parent_id": "父节点 id；章/前置/附录 = null",
                "chapter": "归属章号（int 或 null）",
            },
            "notes": [
                "清华影印扫描版 PDF 共 442 页，无文本层、无内置大纲。",
                "OFFSET=11：PDF 第 12 页 = 书第 1 页（前 3 页封面/书名/版权 + 前言 i–vi + 目录 vii–viii）。",
                "page 为阿拉伯数字书页码；封面/版权/前言/目录/封底用 pdf_page。",
                "Appendix 10 以本书目录与正文为准（书页 414），MIT outline / 另一电子版书签里的 413 是 A9 末页。",
                "Problem Set 页码来自同版英文 PDF 文本层检索，并去掉正文里对习题集的提及。",
            ],
        },
        "items": items,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(items)} items → {OUT}")


if __name__ == "__main__":
    main()
