"""Print the discrete-math TOC tree from toc-discrete-math-8e.json.

Demo for downstream automation: load JSON, build child index, walk by parent_id.
"""

import json
import sys
from pathlib import Path

DOC = Path(__file__).with_name("toc-discrete-math-8e.json")


def load():
    return json.loads(DOC.read_text(encoding="utf-8"))


def label(it):
    if it["type"] == "chapter":
        prefix = f"第{it['chapter']}章"
    elif it["type"] == "appendix":
        prefix = f"附录{it['id']}"
    elif it["type"] == "frontmatter":
        prefix = ""
    else:
        prefix = it["id"]
    page = f" ... {it['page']}" if it["page"] is not None else ""
    return f"{prefix} {it['title']}{page}".strip()


def main(include_aux: bool = False):
    data = load()
    items = data["items"]
    by_id = {i["id"]: i for i in items}
    children: dict = {}
    for it in items:
        children.setdefault(it["parent_id"], []).append(it["id"])

    def walk(pid, depth):
        for cid in children.get(pid, []):
            it = by_id[cid]
            if not include_aux and it["type"] in ("exercises", "endmatter"):
                continue
            if it["type"] == "chapter":
                print()
            print(
                ("    " * depth)
                + ("" if depth == 0 else "|-- ")
                + label(it)
            )
            walk(cid, depth + 1)

    walk(None, 0)


if __name__ == "__main__":
    main(include_aux="--all" in sys.argv)
