r"""
make_catalan_figs.py —— 產生講義第 1 節（經典卡塔蘭數）用的 TikZ 圖

在 notes/ 資料夾內執行：
    python make_catalan_figs.py
會先檢查第 1 節用到的數字，再寫出 catalan_figs.tex（講義在導言區用 \input 讀進來）。

所有物件都由 codes/utils/counting.py 的「樹」產生（不需要 manim），排列順序與上色規則
都和 manim 動畫的卡塔蘭模組（場景 00a–00m）相同，所以講義與動畫裡「第 k 個」物件彼此對應：
    根 = cTop（橘）、左邊的子問題 = cLeft（青）、右邊 = cRight（紫紅）、
    一般的卡塔蘭物件 = cA（藍）、不合法 = cBad（紅）。顏色定義在講義的導言區。
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "codes"))

from utils.counting import (  # noqa: E402
    ballot_more_than_k_times,
    bertrand_strict_count,
    binary_trees,
    catalan,
    dyck_parts,
    dyck_to_ballot,
    dyck_to_brackets,
    dyck_to_lattice,
    dyck_to_matching,
    first_bad_step,
    lattice_ok,
    lattice_points,
    lattice_words,
    matching_parts,
    reflect_tail,
    tree_size,
    tree_to_dyck,
    tree_to_paren_tokens,
    tree_to_triangulation,
    triangulations,
)

OUT = HERE / "catalan_figs.tex"
COLOR = {"root": "cTop", "left": "cLeft", "right": "cRight", None: "cA"}
FILL = {"root": "cTop!38", "left": "cLeft!22", "right": "cRight!20"}


# =============================================================================
# 第 1 節用到的數字
# =============================================================================
def check_numbers():
    """講義第 1 節寫到的每一個數字；任何一項不對就停下來，不產生圖。"""
    # 1.1 數列與兩種公式
    assert [catalan(n) for n in range(11)] == [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796]
    for n in range(1, 30):
        assert comb(2 * n, n) - comb(2 * n, n - 1) == catalan(n)
    # 1.1 明安圖的級數：sin 2x = 2 sin x - sum_{k>=1} C_{k-1} / 4^{k-1} * sin^{2k+1} x
    for x in (0.1, 0.4, 0.7, 1.0):
        s = math.sin(x)
        series = 2 * s - sum(catalan(k - 1) / 4 ** (k - 1) * s ** (2 * k + 1) for k in range(1, 200))
        assert abs(series - math.sin(2 * x)) < 1e-12, (x, series)
    # 1.2–1.3 三角剖分與遞迴：T_3..T_6 = 1, 2, 5, 14；六邊形依第三個頂點分組 5 + 2 + 2 + 5
    assert [len(triangulations(m)) for m in (3, 4, 5, 6)] == [1, 2, 5, 14]
    groups = [sum(1 for t in binary_trees(4) if tree_size(t[0]) + 1 == k) for k in (1, 2, 3, 4)]
    assert groups == [5, 2, 2, 5]
    # 1.6 格子路徑：n = 3 共 20 條、合法 5 條、不合法 15 條 = C(6, 2)
    words = lattice_words(3)
    assert len(words) == 20 and sum(map(lattice_ok, words)) == 5 == catalan(3)
    assert 20 - 5 == comb(6, 2)
    assert first_bad_step("RUURRU") == 3 and reflect_tail("RUURRU") == "RUUUUR"
    assert lattice_points("RUUUUR")[-1] == (2, 4)
    # 1.7 格子路徑 RURRUU 對應 Dyck 路徑 UDUUDD
    assert dyck_to_lattice("UDUUDD") == "RURRUU"
    # 1.8 括號字串
    assert dyck_to_brackets("UUDUDD") == "(()())"
    # 1.9 投票：一般 Bertrand、k 倍推廣、卡塔蘭特例
    for a in range(1, 9):
        for b in range(a):
            assert Fraction(bertrand_strict_count(a, b), comb(a + b, a)) == Fraction(a - b, a + b)
    for a, b, k in [(5, 1, 2), (7, 2, 2), (7, 2, 3), (9, 2, 3), (10, 3, 3)]:
        assert Fraction(ballot_more_than_k_times(a, b, k), comb(a + b, a)) == Fraction(a - k * b, a + b)
    for n in range(1, 8):
        assert bertrand_strict_count(n + 1, n) == catalan(n) == Fraction(comb(2 * n + 1, n), 2 * n + 1)
    # 1.12 生成函數：C^2 與 1 + x C^2 的前幾項；sqrt(1 - 4x) = 1 - 2 sum C_n x^{n+1}
    c = [catalan(n) for n in range(12)]
    square = [sum(c[k] * c[m - k] for k in range(m + 1)) for m in range(11)]
    assert square[:4] == [1, 2, 5, 14]
    assert [1] + square[:10] == c[:11]
    for m in range(1, 12):
        # binom(1/2, m) * (-4)^m = -2 C_{m-1}
        b = Fraction(1)
        for i in range(m):
            b *= Fraction(1, 2) - i
        b /= math.factorial(m)
        assert b * (-4) ** m == -2 * catalan(m - 1)
    print("講義第 1 節的數字檢查通過")


# =============================================================================
# 幾何：先在原點附近建立圖元，再整體平移
# =============================================================================
def f(x: float) -> str:
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pt(x: float, y: float) -> str:
    return f"({f(x)},{f(y)})"


def bbox(prims):
    xs, ys = [], []
    for pr in prims:
        kind = pr[0]
        if kind in ("fill", "poly"):
            pts = pr[2]
        elif kind == "line":
            pts = [pr[2], pr[3]]
        elif kind in ("dot", "square", "circle"):
            (x, y), r = pr[2], pr[3]
            pts = [(x - r, y - r), (x + r, y + r)]
        elif kind == "node":
            (x, y), (w, h) = pr[2], pr[4]
            pts = [(x - w, y - h), (x + w, y + h)]
        else:
            raise ValueError(kind)
        xs += [p[0] for p in pts]
        ys += [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def emit(prims, dx: float = 0.0, dy: float = 0.0) -> list:
    def P(p):
        return pt(p[0] + dx, p[1] + dy)

    out = []
    for pr in prims:
        kind = pr[0]
        if kind == "fill":
            out.append(rf"\fill[{pr[1]}] " + " -- ".join(P(p) for p in pr[2]) + " -- cycle;")
        elif kind == "poly":
            out.append(rf"\draw[{pr[1]}] " + " -- ".join(P(p) for p in pr[2]) + " -- cycle;")
        elif kind == "line":
            out.append(rf"\draw[{pr[1]}] {P(pr[2])} -- {P(pr[3])};")
        elif kind == "dot":
            out.append(rf"\fill[{pr[1]}] {P(pr[2])} circle ({f(pr[3])});")
        elif kind == "square":
            (x, y), s = pr[2], pr[3]
            out.append(rf"\fill[{pr[1]}] {pt(x - s + dx, y - s + dy)} rectangle {pt(x + s + dx, y + s + dy)};")
        elif kind == "circle":
            out.append(rf"\draw[{pr[1]}] {P(pr[2])} circle ({f(pr[3])});")
        elif kind == "node":
            out.append(rf"\node[{pr[1]}] at {P(pr[2])} {{{pr[3]}}};")
    return out


def place(prims, cx: float, cy: float) -> list:
    """把圖元的外框中心移到 (cx, cy)。"""
    x0, y0, x1, y1 = bbox(prims)
    return emit(prims, cx - (x0 + x1) / 2, cy - (y0 + y1) / 2)


def node(p, text, opts="", size=(0.12, 0.12)):
    return ("node", opts, p, text, size)


def colored_math(chars, parts, wrap=lambda c: c) -> str:
    """把連續屬於同一部分的字元包成一組上色（數學模式）。"""
    out, i = [], 0
    while i < len(chars):
        j = i
        while j < len(chars) and parts[j] == parts[i]:
            j += 1
        seg = "".join(wrap(c) for c in chars[i:j])
        out.append(rf"{{\color{{{COLOR[parts[i]]}}}{seg}}}")
        i = j
    return "".join(out)


# =============================================================================
# 物件（與 codes/utils/catalan_draw.py 的畫法相同）
# =============================================================================
def polygon_vertices(m: int, r: float):
    """底邊（第 0 與第 m-1 點）水平放在最下面；第 0 點在左下，順時針到右下的第 m-1 點。"""
    out = []
    for k in range(m):
        a = -math.pi / 2 - math.pi / m - 2 * math.pi * k / m
        out.append((r * math.cos(a), r * math.sin(a)))
    return out


def tri_prims(m: int, diags, r: float, tree=None, diag_w=1.1, dot_r=0.03):
    """凸 m 邊形的三角剖分；給 tree 時把根三角形、左右子多邊形上色。"""
    v = polygon_vertices(m, r)
    prims, colors = [], {}
    if tree is not None:
        k = tree_size(tree[0]) + 1
        left, right = list(range(0, k + 1)), list(range(k, m))
        prims.append(("fill", FILL["root"], [v[0], v[k], v[m - 1]]))
        if len(left) >= 3:
            prims.append(("fill", FILL["left"], [v[i] for i in left]))
        if len(right) >= 3:
            prims.append(("fill", FILL["right"], [v[i] for i in right]))
        for a, b in diags:
            if (a, b) in ((0, k), (k, m - 1)):
                colors[(a, b)] = "cTop"
            elif b <= k:
                colors[(a, b)] = "cLeft"
            else:
                colors[(a, b)] = "cRight"
    prims.append(("poly", "gray!70,line width=0.6pt,line join=round", v))
    for a, b in diags:
        prims.append(("line", f"{colors.get((a, b), 'cA')},line width={diag_w}pt,line cap=round", v[a], v[b]))
    for p in v:
        prims.append(("dot", "black", p, dot_r))
    return prims


def tree_prims(tree, gap: float, level: float, colored=True, labels=None,
               node_r=0.05, leaf_s=0.04, edge_w=0.8):
    """
    滿二元樹，樹根在 (0, 0)。葉子依中序等距排列，內部節點放在它所有葉子的正中間
    （與 catalan_draw.BinaryTreeMob 相同）。labels 給字母時，葉子畫成字母。
    """
    leaves, nodes = [], []

    def rec(t, depth, part):
        if t is None:
            leaves.append({"x": len(leaves), "d": depth, "part": part})
            return ("leaf", len(leaves) - 1)
        left = rec(t[0], depth + 1, part)
        i = len(nodes)
        nodes.append({"d": depth, "part": part, "ch": None})
        right = rec(t[1], depth + 1, part)
        nodes[i]["ch"] = (left, right)
        return ("node", i)

    if tree is None:
        leaves.append({"x": 0, "d": 0, "part": "root"})
    else:
        lref = rec(tree[0], 1, "left")
        nodes.append({"d": 0, "part": "root", "ch": None})
        root = len(nodes) - 1
        rref = rec(tree[1], 1, "right")
        nodes[root]["ch"] = (lref, rref)

    def span(ref):
        kind, i = ref
        if kind == "leaf":
            return leaves[i]["x"], leaves[i]["x"]
        return span(nodes[i]["ch"][0])[0], span(nodes[i]["ch"][1])[1]

    x0 = (len(leaves) - 1) / 2

    def pos(ref):
        kind, i = ref
        if kind == "leaf":
            return (leaves[i]["x"] - x0) * gap, -leaves[i]["d"] * level
        lo, hi = span(ref)
        return ((lo + hi) / 2 - x0) * gap, -nodes[i]["d"] * level

    def col(part, default):
        return COLOR[part] if colored else default

    prims = []
    for i, nd in enumerate(nodes):
        start = pos(("node", i))
        for ref in nd["ch"]:
            end = pos(ref)
            if ref[0] == "leaf" and labels:
                dx, dy = end[0] - start[0], end[1] - start[1]
                length = math.hypot(dx, dy)
                end = (end[0] - 0.17 * dx / length, end[1] - 0.17 * dy / length)
            part = "root" if nd["part"] == "root" else nd["part"]
            prims.append(("line", f"{col(part, 'gray!70')},line width={edge_w}pt,line cap=round", start, end))
    for i, nd in enumerate(nodes):
        prims.append(("dot", col(nd["part"], "cA"), pos(("node", i)), node_r))
    for i, lf in enumerate(leaves):
        p = pos(("leaf", i))
        if labels:
            prims.append(node((p[0], p[1] - 0.03), f"${labels[i]}$",
                              f"font=\\small,inner sep=0pt,text={col(lf['part'], 'black')}", (0.1, 0.13)))
        else:
            prims.append(("square", col(lf["part"], "gray!60"), p, leaf_s))
    return prims


def dyck_prims(word: str, unit: float, parts=None, w=1.1, base=True):
    pts = [(0.0, 0.0)]
    for c in word:
        pts.append((pts[-1][0] + unit, pts[-1][1] + (unit if c == "U" else -unit)))
    prims = []
    if base:
        prims.append(("line", "gray!55,line width=0.4pt", (0.0, 0.0), (unit * max(len(word), 1), 0.0)))
    for j in range(len(word)):
        color = COLOR[parts[j]] if parts else "cA"
        prims.append(("line", f"{color},line width={w}pt,line cap=round", pts[j], pts[j + 1]))
    if not word:
        prims.append(("dot", "cA", (0.0, 0.0), 0.05))
    return prims


def lattice_prims(word: str, n: int, unit: float, color="cA", colors=None, w=1.1, ny=None):
    ny = n if ny is None else ny
    prims = []
    for i in range(n + 1):
        prims.append(("line", "gray!30,line width=0.3pt", (i * unit, 0.0), (i * unit, ny * unit)))
    for j in range(ny + 1):
        prims.append(("line", "gray!30,line width=0.3pt", (0.0, j * unit), (n * unit, j * unit)))
    prims.append(("line", "gray!60,dashed,line width=0.4pt", (0.0, 0.0), (n * unit, n * unit)))
    pts = [(x * unit, y * unit) for x, y in lattice_points(word)]
    for j in range(len(word)):
        c = colors[j] if colors else color
        prims.append(("line", f"{c},line width={w}pt,line cap=round", pts[j], pts[j + 1]))
    return prims


def circle_point(i: int, npts: int, r: float):
    a = math.radians(90 - 360 * i / npts)
    return r * math.cos(a), r * math.sin(a)


def matching_prims(pairs, npts: int, r: float, parts=None, root=False, w=1.1, labels=False):
    """圓周 npts 點（第 0 點在正上方、順時針）的配對；root=True 時第 0 點畫成橘色。"""
    prims = [("circle", "gray!65,line width=0.5pt", (0.0, 0.0), r)]
    for j, (a, b) in enumerate(pairs):
        color = COLOR[parts[j]] if parts else "cA"
        prims.append(("line", f"{color},line width={w}pt,line cap=round",
                      circle_point(a, npts, r), circle_point(b, npts, r)))
    for i in range(npts):
        prims.append(("dot", "black", circle_point(i, npts, r), 0.035))
    if root:
        prims.append(("dot", "cTop", circle_point(0, npts, r), 0.065))
    if labels:
        for i in range(npts):
            prims.append(node(circle_point(i, npts, r + 0.24), f"{i + 1}", "font=\\scriptsize"))
    return prims


def paren_math(tree, factors="abcd", colored=True) -> str:
    tokens, parts = tree_to_paren_tokens(tree, factors)
    if not colored:
        return "".join(r"\cdot " if t == "·" else t for t in tokens)
    out, i = [], 0
    while i < len(tokens):
        if parts[i] == "root":                      # 最後一次乘法：保留二元運算的間距
            out.append(r"\mathbin{\color{cTop}\cdot}")
            i += 1
            continue
        j = i
        while j < len(tokens) and parts[j] == parts[i]:
            j += 1
        seg = "".join(r"\cdot " if t == "·" else t for t in tokens[i:j])
        out.append(rf"{{\color{{{COLOR[parts[i]]}}}{seg}}}")
        i = j
    return "".join(out)


def word_math(word: str, parts, kind: str) -> str:
    """Dyck 字轉成括號字串或開票順序，逐字依根／左／右上色。"""
    text = dyck_to_brackets(word) if kind == "brackets" else dyck_to_ballot(word)
    wrap = (lambda c: c) if kind == "brackets" else (lambda c: rf"\mathrm{{{c}}}")
    return colored_math(text, parts, wrap)


# =============================================================================
# 圖
# =============================================================================
def picture(lines, opts="") -> str:
    head = r"\begin{tikzpicture}" + (f"[{opts}]" if opts else "")
    return head + "\n" + "\n".join(lines) + "\n" + r"\end{tikzpicture}"


def fig_tri_small() -> str:
    """凸三、四、五邊形的所有三角剖分（不上色）。"""
    lines, x = [], 0.0
    for m, label in [(3, r"$T_3=1=C_1$"), (4, r"$T_4=2=C_2$"), (5, r"$T_5=5=C_3$")]:
        xs = []
        for diags in triangulations(m):
            lines += place(tri_prims(m, diags, 0.6), x, 0.0)
            xs.append(x)
            x += 1.45
        lines += emit([node((sum(xs) / len(xs), -0.95), label, "font=\\small")])
        x += 0.75
    return picture(lines)


def fig_tri_split() -> str:
    """凸六邊形、第三個頂點 k = 2：根三角形把它切成左邊的三角形與右邊的四邊形。"""
    m, k, r = 6, 2, 1.35
    v = polygon_vertices(m, r)
    lines = [
        rf"\fill[{FILL['left']}] " + " -- ".join(pt(*v[i]) for i in range(0, k + 1)) + " -- cycle;",
        rf"\fill[{FILL['right']}] " + " -- ".join(pt(*v[i]) for i in range(k, m)) + " -- cycle;",
        rf"\fill[{FILL['root']}] {pt(*v[0])} -- {pt(*v[k])} -- {pt(*v[m - 1])} -- cycle;",
        r"\draw[gray!70,line width=0.7pt,line join=round] " + " -- ".join(pt(*p) for p in v) + " -- cycle;",
        rf"\draw[cTop,line width=1.3pt,line cap=round] {pt(*v[0])} -- {pt(*v[k])} -- {pt(*v[m - 1])};",
        rf"\draw[cTop,line width=2.2pt,line cap=round] {pt(*v[0])} -- {pt(*v[m - 1])};",
    ]
    for i, p in enumerate(v):
        lines.append(rf"\fill {pt(*p)} circle (0.045);")
        lab = polygon_vertices(m, r + 0.3)[i]
        lines.append(rf"\node[font=\small] at {pt(*lab)} {{${i}$}};")

    def centroid(idx):
        return (sum(v[i][0] for i in idx) / len(idx), sum(v[i][1] for i in idx) / len(idx))

    lines += [
        rf"\node[font=\small,text=cTop!80!black] at {pt(*centroid([0, k, m - 1]))} {{根}};",
        rf"\node[font=\small,text=cLeft!80!black,align=center] at {pt(*centroid([0, 1, 2]))} {{左\\$C_1$}};",
        rf"\node[font=\small,text=cRight!85!black,align=center] at {pt(*centroid([2, 3, 4, 5]))} {{右\\$C_2$}};",
        rf"\node[font=\small,text=cTop!80!black] at {pt(0.0, v[0][1] - 0.32)} {{底邊}};",
    ]
    return picture(lines)


def fig_tri_groups() -> str:
    """凸六邊形的 14 種三角剖分，依底邊三角形的第三個頂點 k 分組（5 | 2 | 2 | 5），上色。"""
    trees = binary_trees(4)
    by_k = {k: [t for t in trees if tree_size(t[0]) + 1 == k] for k in (1, 2, 3, 4)}
    step, gap, r = 1.28, 0.95, 0.52
    lines = []
    for row, ks in enumerate([(1, 2), (3, 4)]):
        widths = [len(by_k[k]) * step for k in ks]
        x = -(sum(widths) + gap) / 2 + step / 2
        y = -2.05 * row
        for k in ks:
            xs = []
            for t in by_k[k]:
                lines += place(tri_prims(6, tree_to_triangulation(t, 0, 5), r, tree=t), x, y)
                xs.append(x)
                x += step
            a, b = k - 1, 4 - k
            label = (rf"$k={k}$：$\textcolor{{cLeft}}{{C_{a}}}\textcolor{{cRight}}{{C_{b}}}"
                     rf"={catalan(a)}\cdot{catalan(b)}={catalan(a) * catalan(b)}$")
            lines += emit([node((sum(xs) / len(xs), y - 0.82), label, "font=\\footnotesize")])
            x += gap
    return picture(lines)


def fig_paren_trees() -> str:
    """4 個因子的五種完全括號化（上）與對應的滿二元樹（下），依根／左／右上色。"""
    lines = []
    for j, t in enumerate(binary_trees(3)):
        x = 3.05 * j
        lines += emit([node((x, 0.0), f"${paren_math(t)}$", "font=\\small")])
        lines += emit(tree_prims(t, gap=0.55, level=0.45, labels="abcd"), x, -0.6)
    return picture(lines)


def fig_lattice_all() -> str:
    """(0,0) 到 (3,3) 的 20 條路徑：合法（不越過 y = x）的藍色並打勾，其餘紅色。"""
    lines = []
    for idx, w in enumerate(lattice_words(3)):
        row, colm = divmod(idx, 10)
        ok = lattice_ok(w)
        x, y = 0.95 * colm, -1.15 * row
        lines += emit(lattice_prims(w, 3, 0.2, color="cA" if ok else "cBad", w=1.0), x, y)
        if ok:
            lines += emit([node((x + 0.3, y - 0.25), r"\checkmark", "font=\\scriptsize,text=green!50!black")])
    return picture(lines)


def fig_reflection() -> str:
    """反射原理：RUU|RRU 在 (1,2) 第一次碰到 y = x + 1，之後的部分翻成 UUR，終點變成 (2,4)。"""
    u = 0.62
    bad = "RUURRU"
    j = first_bad_step(bad)
    new = reflect_tail(bad)
    p_bad = [(x * u, y * u) for x, y in lattice_points(bad)]
    p_new = [(x * u, y * u) for x, y in lattice_points(new)]
    lines = []
    for i in range(4):
        lines.append(rf"\draw[gray!30,line width=0.3pt] {pt(i * u, 0)} -- {pt(i * u, 4 * u)};")
    for i in range(5):
        lines.append(rf"\draw[gray!30,line width=0.3pt] {pt(0, i * u)} -- {pt(3 * u, i * u)};")
    lines += [
        rf"\draw[gray!60,dashed,line width=0.5pt] {pt(0, 0)} -- {pt(3.45 * u, 3.45 * u)} node[right,font=\scriptsize,text=gray!70!black] {{$y=x$}};",
        rf"\draw[cBad!80,dashed,line width=0.5pt] {pt(0, u)} -- {pt(3 * u, 4 * u)} node[right,font=\scriptsize,text=cBad] {{$y=x+1$}};",
    ]
    for i in range(len(bad)):
        lines.append(rf"\draw[cBad,line width=1.3pt,line cap=round] {pt(*p_bad[i])} -- {pt(*p_bad[i + 1])};")
    for i in range(j, len(new)):
        lines.append(rf"\draw[cTop,line width=1.3pt,line cap=round,dashed] {pt(*p_new[i])} -- {pt(*p_new[i + 1])};")
    lines += [
        rf"\fill[cBad] {pt(*p_bad[j])} circle (0.07);",
        rf"\node[left,font=\scriptsize] at {pt(*p_bad[j])} {{$P$}};",
        rf"\fill {pt(*p_bad[-1])} circle (0.05);",
        rf"\node[below right,font=\scriptsize] at {pt(*p_bad[-1])} {{$(3,3)$}};",
        rf"\fill[cTop] {pt(*p_new[-1])} circle (0.05);",
        rf"\node[above,font=\scriptsize] at {pt(*p_new[-1])} {{$(2,4)$}};",
        rf"\node[below left,font=\scriptsize] at {pt(0, 0)} {{$(0,0)$}};",
    ]
    return picture(lines)


def fig_lattice_to_dyck() -> str:
    """格子路徑 RURRUU（左）對應 Dyck 路徑 UDUUDD（右）：R -> 上坡、U -> 下坡。"""
    lat, dyck = "RURRUU", "UDUUDD"
    assert dyck_to_lattice(dyck) == lat
    lines = emit(lattice_prims(lat, 3, 0.55, w=1.4))
    for i, c in enumerate(lat):
        lines.append(rf"\node[font=\scriptsize] at {pt(0.2 + 0.32 * i, -0.4)} {{{c}}};")
    lines.append(r"\draw[-{Stealth[length=5pt]},line width=0.7pt,gray!60!black] (2.3,0.8) -- (3.6,0.8)"
                 r" node[midway,above,font=\scriptsize] {$\mathrm{R}\mapsto\nearrow$}"
                 r" node[midway,below,font=\scriptsize] {$\mathrm{U}\mapsto\searrow$};")
    lines += emit(dyck_prims(dyck, 0.45, w=1.4), 4.0, 0.25)
    for i, c in enumerate(dyck):
        lines.append(rf"\node[font=\scriptsize] at {pt(4.0 + 0.45 * i + 0.225, -0.4)} {{{c}}};")
    return picture(lines)


def fig_dyck_table() -> str:
    """半長 n = 0, 1, 2, 3 的所有 Dyck 路徑，依根／左／右上色。"""
    u, x_start, step = 0.22, 1.35, 1.75
    lines = []
    y = 0.0
    for n in range(4):
        trees = binary_trees(n)
        lines.append(rf"\node[anchor=west,font=\small] at {pt(0, y + 0.05)} {{$n={n}$}};")
        for i, t in enumerate(trees):
            word = tree_to_dyck(t)
            parts = dyck_parts(t)
            lines += emit(dyck_prims(word, u, parts, w=1.2), x_start + step * i, y)
            if not word:
                lines.append(rf"\node[anchor=west,font=\scriptsize] at {pt(x_start + 0.35, y + 0.02)} {{（空路徑）}};")
        lines.append(rf"\node[anchor=west,font=\small] at {pt(10.3, y + 0.05)} {{{len(trees)} 種}};")
        y -= 0.55 + u * (n + 1) + 0.2
    return picture(lines)


def fig_dyck_words() -> str:
    """半長 3 的五條 Dyck 路徑，下面是對應的括號字串與開票順序（逐字上色）。"""
    u, x0, step = 0.24, 2.7, 2.45
    lines = [
        r"\node[anchor=west,font=\small] at (0,0.3) {Dyck 路徑};",
        r"\node[anchor=west,font=\small] at (0,-0.45) {括號字串};",
        r"\node[anchor=west,font=\small] at (0,-0.98) {開票順序};",
    ]
    for i, t in enumerate(binary_trees(3)):
        word, parts = tree_to_dyck(t), dyck_parts(t)
        x = x0 + step * i
        lines += emit(dyck_prims(word, u, parts, w=1.2), x, 0.0)
        cx = x + 3 * u
        lines.append(rf"\node[font=\small] at {pt(cx, -0.45)} {{${word_math(word, parts, 'brackets')}$}};")
        lines.append(rf"\node[font=\small] at {pt(cx, -0.98)} {{${word_math(word, parts, 'ballot')}$}};")
    return picture(lines)


def fig_ballot() -> str:
    """開票順序 AABABB：A 領先的票數 0, 1, 2, 1, 2, 1, 0 連成一條 Dyck 路徑。"""
    votes = "AABABB"
    ux, uy = 0.8, 0.6
    h = [0]
    for c in votes:
        h.append(h[-1] + (1 if c == "A" else -1))
    lines = []
    for y in (1, 2):
        lines.append(rf"\draw[gray!25,line width=0.3pt] {pt(0, y * uy)} -- {pt(6 * ux, y * uy)};")
    lines += [
        rf"\draw[-{{Stealth[length=4pt]}},gray!70!black,line width=0.5pt] (0,0) -- {pt(6 * ux + 0.4, 0)}"
        r" node[right,font=\scriptsize] {已開的票數};",
        rf"\draw[-{{Stealth[length=4pt]}},gray!70!black,line width=0.5pt] (0,0) -- {pt(0, 2 * uy + 0.45)}"
        r" node[above,font=\scriptsize] {A 領先的票數};",
    ]
    for i in range(7):
        lines.append(rf"\node[below,font=\scriptsize] at {pt(i * ux, 0)} {{{i}}};")
    for y in range(3):
        lines.append(rf"\node[left,font=\scriptsize] at {pt(0, y * uy)} {{{y}}};")
    for i, c in enumerate(votes):
        a, b = (i * ux, h[i] * uy), ((i + 1) * ux, h[i + 1] * uy)
        lines.append(rf"\draw[cA,line width=1.4pt,line cap=round] {pt(*a)} -- {pt(*b)};")
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        side = "above left" if c == "A" else "above right"
        lines.append(rf"\node[{side},font=\scriptsize,inner sep=1.5pt] at {pt(*mid)} {{{c}}};")
    for i in range(7):
        lines.append(rf"\fill[cA] {pt(i * ux, h[i] * uy)} circle (0.045);")
    assert h == [0, 1, 2, 1, 2, 1, 0]
    return picture(lines)


def fig_match_regions() -> str:
    """圓周 6 點：點 1 與點 2、4、6 配對時，弦把其餘的點分成兩側（各自獨立配對）。"""
    r = 1.0
    lines = []
    label_pos = {   # q（0 起算的配對點）-> (內側標籤位置, 外側標籤位置)：(角度, 半徑)
        1: ((60, 1.48), (-120, 0.32)),
        3: ((0, 0.5), (180, 0.5)),
        5: ((-60, 0.32), (120, 1.48)),
    }
    for col, q in enumerate((1, 3, 5)):
        cx = 3.75 * col
        a_q = 90 - 60 * q
        inner, outer = (q - 1) // 2, (5 - q) // 2
        p0 = (cx, r)
        pq = (cx + r * math.cos(math.radians(a_q)), r * math.sin(math.radians(a_q)))
        lines += [
            rf"\fill[{FILL['left']}] {pt(*p0)} arc[start angle=90,end angle={a_q},radius={r}] -- cycle;",
            rf"\fill[{FILL['right']}] {pt(*pq)} arc[start angle={a_q},end angle=-270,radius={r}] -- cycle;",
            rf"\draw[gray!65,line width=0.5pt] {pt(cx, 0)} circle ({r});",
            rf"\draw[cTop,line width=1.5pt,line cap=round] {pt(*p0)} -- {pt(*pq)};",
        ]
        for i in range(6):
            p = circle_point(i, 6, r)
            lines.append(rf"\fill {pt(cx + p[0], p[1])} circle (0.04);")
            lp = circle_point(i, 6, r + 0.22)
            lines.append(rf"\node[font=\scriptsize] at {pt(cx + lp[0], lp[1])} {{{i + 1}}};")
        lines.append(rf"\fill[cTop] {pt(*p0)} circle (0.07);")
        (ai, ri), (ao, ro) = label_pos[q]
        for (ang, rad), size, color in (((ai, ri), inner, "cLeft"), ((ao, ro), outer, "cRight")):
            x = cx + rad * math.cos(math.radians(ang))
            y = rad * math.sin(math.radians(ang))
            lines.append(rf"\node[font=\footnotesize,text={color}!85!black] at {pt(x, y)} {{$C_{size}$}};")
        value = catalan(inner) * catalan(outer)
        lines.append(rf"\node[font=\footnotesize] at {pt(cx, -1.55)} {{點 1 配點 {q + 1}："
                     rf"$\textcolor{{cLeft}}{{C_{inner}}}\textcolor{{cRight}}{{C_{outer}}}={value}$}};")
    return picture(lines)


def fig_one_number() -> str:
    """同一個 C_3 = 5：每一欄是同一棵樹，畫成八種物件。"""
    trees = binary_trees(3)
    rows = [
        ("tri", "凸五邊形的三角剖分", 1.4),
        ("paren", "4 個因子的完全括號化", 0.62),
        ("tree", "3 個內部節點的滿二元樹", 1.4),
        ("lattice", r"不越過 $y=x$ 的格子路徑", 1.15),
        ("dyck", "半長 3 的 Dyck 路徑", 0.85),
        ("brackets", "3 對括號的平衡字串", 0.58),
        ("ballot", "兩人各 3 票的開票順序", 0.58),
        ("match", "圓周 6 點的不交叉配對", 1.35),
    ]
    xs = [5.0 + 2.4 * j for j in range(5)]
    lines = []
    for j, t in enumerate(trees):         # 欄首：左、右子樹的大小
        a, b = tree_size(t[0]), tree_size(t[1])
        lines.append(rf"\node[font=\footnotesize] at {pt(xs[j], 0.35)} "
                     rf"{{$\textcolor{{cLeft}}{{C_{a}}}\textcolor{{cRight}}{{C_{b}}}$}};")
    y = 0.0
    lines.append(rf"\draw[gray!35,line width=0.4pt] {pt(0, 0.08)} -- {pt(xs[-1] + 1.2, 0.08)};")
    for fam, label, height in rows:
        cy = y - height / 2
        lines.append(rf"\node[anchor=west,font=\small] at {pt(0, cy)} {{{label}}};")
        for x, t in zip(xs, trees):
            word, parts = tree_to_dyck(t), dyck_parts(t)
            if fam == "tri":
                lines += place(tri_prims(5, tree_to_triangulation(t, 0, 4), 0.58, tree=t), x, cy)
            elif fam == "paren":
                lines.append(rf"\node[font=\small] at {pt(x, cy)} {{${paren_math(t)}$}};")
            elif fam == "tree":
                lines += place(tree_prims(t, gap=0.36, level=0.36), x, cy)
            elif fam == "lattice":
                colors = [COLOR[p] for p in parts]
                lines += place(lattice_prims(dyck_to_lattice(word), 3, 0.3, colors=colors, w=1.2), x, cy)
            elif fam == "dyck":
                lines += place(dyck_prims(word, 0.2, parts, w=1.2), x, cy)
            elif fam in ("brackets", "ballot"):
                lines.append(rf"\node[font=\small] at {pt(x, cy)} {{${word_math(word, parts, fam)}$}};")
            elif fam == "match":
                pairs = dyck_to_matching(word)
                lines += place(matching_prims(pairs, 6, 0.52, parts=matching_parts(t), root=True), x, cy)
        y -= height
        lines.append(rf"\draw[gray!25,line width=0.3pt] {pt(0, y)} -- {pt(xs[-1] + 1.2, y)};")
    return picture(lines)


FIGURES = [
    ("FigTriSmall", fig_tri_small),
    ("FigTriSplit", fig_tri_split),
    ("FigTriGroups", fig_tri_groups),
    ("FigParenTrees", fig_paren_trees),
    ("FigLatticeAll", fig_lattice_all),
    ("FigReflection", fig_reflection),
    ("FigLatticeToDyck", fig_lattice_to_dyck),
    ("FigDyckTable", fig_dyck_table),
    ("FigDyckWords", fig_dyck_words),
    ("FigBallot", fig_ballot),
    ("FigMatchRegions", fig_match_regions),
    ("FigOneNumber", fig_one_number),
]


def main():
    check_numbers()
    parts = [
        "% catalan_figs.tex —— 由 make_catalan_figs.py 產生，請勿手動修改。\n"
        "% 重新產生：在 notes/ 裡執行 python make_catalan_figs.py\n"
    ]
    for name, func in FIGURES:
        parts.append(f"\\newcommand{{\\{name}}}{{%\n{func()}}}\n")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"已寫出 {OUT.name}：{len(FIGURES)} 張圖")


if __name__ == "__main__":
    main()
