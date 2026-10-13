r"""
make_figs_part4.py —— 講義附錄 A 第 4 段（A.12–A.14，動畫 M12–M14）的 TikZ 圖

在 notes/ 或 notes/mit/ 裡執行：
    python mit/make_figs_part4.py
會先檢查 mit/part4.tex 寫到的每一個數字（check_numbers），再寫出 mit/figs_part4.tex
（mit/part4.tex 第一行 \input{mit/figs_part4}）。

數學資料一律由 codes/utils/counting.py 算出（第 6 節，格子 0 起算；講義顯示時 +1），
畫圖的基本圖元沿用 notes/make_catalan_figs.py（emit、node、picture、dyck_prims、pt ……）。
例子與數字和動畫場景 M12–M14 相同。顏色：
    第 1 列／U = cLeft（青）、第 2 列／D = cRight（紫紅）、第 3 列 = olive、
    鉤 = 黃、格子本身／漫步 = cTop（橘）、角落 = cC（綠）、
    列集合 A 與 c 上方的格子 = cLeft、行集合 B 與 c 左方的格子 = cRight、不合法 = cBad。
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent            # notes/mit
NOTES = HERE.parent                               # notes
sys.path.insert(0, str(NOTES.parent / "codes"))
sys.path.insert(0, str(NOTES))

from make_catalan_figs import dyck_prims, emit, node, picture, pt  # noqa: E402
from utils.counting import (  # noqa: E402
    catalan,
    conjugate,
    corner_prob_formula,
    corner_prob_product,
    corners,
    dyck_to_syt,
    dyck_words,
    hook_cells,
    hook_formula,
    hook_identity,
    hook_lemma_rhs,
    hook_length,
    hook_lengths,
    hook_product,
    hook_walk_probs,
    hook_walks,
    integer_partitions,
    is_dyck,
    is_lattice_rowword,
    remove_corner,
    rowword_counts,
    rowword_to_syt,
    syt,
    syt_bruteforce,
    syt_count,
    syt_to_dyck,
    syt_to_rowword,
    walk_rows_cols,
    young_cells,
)

OUT = HERE / "figs_part4.tex"

# ----------------------------------------------------------------- 例子（與場景相同）
EX_T = ((1, 2, 4), (3, 5, 6))            # M12：第 3 節的例子
EX_WORD = "UUDUDD"
GEN_LAM = (2, 2, 1)                      # M12：一般 λ 的 3 列小例子
GEN_T = ((1, 3), (2, 5), (4,))
BAD_T = ((1, 5), (2, 4), (3,))           # 5 在 4 上面：不是標準 Young 表
LAM = (4, 3, 1)                          # M13、M14 的主例，n = 8
HOOK_EX = (0, 1)                         # M13 示範鉤的格子（講義 (1,2)）
SMALL = (3, 2)
SQUARE = (3, 3)
C = (1, 2)                               # M14 的角落 c = (α, β)（講義 (2,3)）
WALK_R = ((0, 0), (0, 2), (1, 2))        # M14 示範漫步：先往右
WALK_D = ((0, 0), (1, 0), (1, 2))        # 投影相同：先往下

ROW_COL = ["cLeft", "cRight", "olive"]
ROW_FILL = ["cLeft!20", "cRight!18", "olive!22"]
HOOK_FILL = "yellow!55"
SELF_FILL = "cTop!45"
CORNER = "cC"
CORNER_FILL = "cC!30"
WALK = "cTop"


# =============================================================================
# 數字檢查：part4.tex 裡寫到的每一個數字
# =============================================================================
def walk_weight(lam, walk) -> Fraction:
    """∏ 1/(h(a_k)-1)（不含 1/n），並確認它是 hook_walks 列出的一條。"""
    w = Fraction(1)
    for c in walk[:-1]:
        w /= hook_length(lam, *c) - 1
    assert (tuple(walk), w) in hook_walks(lam, walk[0])
    return w


def check_numbers():
    # ------------------------------------------------ A.12
    assert syt_to_dyck(EX_T) == EX_WORD and is_dyck(EX_WORD) and dyck_to_syt(EX_WORD) == EX_T
    assert [(EX_T[0][j], EX_T[1][j]) for j in range(3)] == [(1, 3), (2, 5), (4, 6)]
    tabs = syt(SQUARE)
    assert set(tabs) == syt_bruteforce(SQUARE) and len(tabs) == 5 == catalan(3)
    assert [syt_to_dyck(T) for T in tabs] == ["UUUDDD", "UUDUDD", "UUDDUD", "UDUUDD", "UDUDUD"]
    assert tabs.index(EX_T) == 1
    for n in range(1, 7):                        # 一一對應：兩個方向都檢查
        assert sorted(syt_to_dyck(T) for T in syt((n, n))) == sorted(dyck_words(n))
        assert all(syt_to_dyck(dyck_to_syt(w)) == w for w in dyck_words(n))
    assert [syt_count((n, n)) for n in range(1, 7)] == [catalan(n) for n in range(1, 7)] == [1, 2, 5, 14, 42, 132]
    word = syt_to_rowword(GEN_T)
    assert GEN_T in syt(GEN_LAM) and word == (0, 1, 0, 2, 1) and is_lattice_rowword(word)
    assert rowword_counts(word, 3)[1:] == [(1, 0, 0), (1, 1, 0), (2, 1, 0), (2, 1, 1), (2, 2, 1)]
    bad = syt_to_rowword(BAD_T)
    assert BAD_T not in syt_bruteforce(GEN_LAM) and rowword_to_syt(bad) == BAD_T and not is_lattice_rowword(bad)
    bc = rowword_counts(bad, 3)
    assert bc[1:] == [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 2, 1), (2, 2, 1)]
    assert [t for t, x in enumerate(bc) if not (x[0] >= x[1] >= x[2])] == [4]
    for lam in [(2, 2, 1), (3, 2, 1), (3, 3), (4, 2), (2, 2, 2)]:     # 定理：SYT <-> 格子字
        assert set(syt(lam)) == syt_bruteforce(lam)
        assert all(is_lattice_rowword(syt_to_rowword(T)) for T in syt(lam))

    # ------------------------------------------------ A.13
    assert hook_lengths(LAM) == [(6, 4, 3, 1), (4, 2, 1), (1,)]
    i, j = HOOK_EX
    hk = hook_cells(LAM, i, j)
    arm = [(a, b) for a, b in hk if a == i and b > j]
    leg = [(a, b) for a, b in hk if b == j and a > i]
    assert arm == [(0, 2), (0, 3)] and leg == [(1, 1)] and hook_length(LAM, i, j) == 4
    assert len(arm) == LAM[i] - (j + 1) and len(leg) == conjugate(LAM)[j] - (i + 1)   # 1 起算：λ_i − j、λ'_j − i
    assert hook_product(LAM) == 576 and factorial(8) == 40320 and 40320 // 576 == 70
    assert hook_formula(LAM) == syt_count(LAM) == len(syt_bruteforce(LAM)) == 70
    assert hook_lengths(SMALL) == [(4, 3, 1), (2, 1)] and hook_product(SMALL) == 24
    assert factorial(5) == 120 and hook_formula(SMALL) == len(syt_bruteforce(SMALL)) == 5
    assert hook_lengths(SQUARE) == [(4, 3, 2), (3, 2, 1)] and hook_product(SQUARE) == 144
    assert factorial(6) == 720 and hook_formula(SQUARE) == 5 == catalan(3)
    for m in range(1, 10):
        hm = hook_lengths((m, m))
        assert list(hm[0]) == list(range(m + 1, 1, -1)) and list(hm[1]) == list(range(m, 0, -1))
        assert hook_product((m, m)) == factorial(m + 1) * factorial(m)
        assert hook_formula((m, m)) == syt_count((m, m)) == catalan(m)
    for n in range(1, 9):                        # 鉤長公式與角落遞迴互相驗證
        for lam in integer_partitions(n):
            assert hook_formula(lam) == syt_count(lam)
    for n in range(1, 7):
        for lam in integer_partitions(n):
            assert hook_formula(lam) == len(syt_bruteforce(lam))
    # 角落遞迴 (3,2)
    assert corners(SMALL) == [(0, 2), (1, 1)]
    assert [remove_corner(SMALL, c) for c in corners(SMALL)] == [(2, 2), (3, 1)]
    groups = [[T for T in syt(SMALL) if T[c[0]][c[1]] == 5] for c in corners(SMALL)]
    assert groups == [[((1, 2, 5), (3, 4)), ((1, 3, 5), (2, 4))],
                      [((1, 2, 3), (4, 5)), ((1, 2, 4), (3, 5)), ((1, 3, 4), (2, 5))]]
    assert [syt_count((2, 2)), syt_count((3, 1))] == [2, 3] and 2 + 3 == syt_count(SMALL)
    # 化約 (3,2)
    assert [hook_product((2, 2)), hook_product((3, 1))] == [12, 8]
    assert [corner_prob_formula(SMALL, c) for c in corners(SMALL)] == [Fraction(2, 5), Fraction(3, 5)]
    assert Fraction(24, 5 * 12) == Fraction(2, 5) and Fraction(24, 5 * 8) == Fraction(3, 5)

    # ------------------------------------------------ A.14
    n = sum(LAM)
    # (1) 示範漫步
    assert [hook_length(LAM, *c) for c in WALK_R] == [6, 3, 1]
    assert WALK_R[1] in hook_cells(LAM, *WALK_R[0]) and WALK_R[2] in hook_cells(LAM, *WALK_R[1])
    wr = walk_weight(LAM, WALK_R)
    assert wr == Fraction(1, 10) and wr / n == Fraction(1, 80)
    assert all(hook_length(LAM, *c) == 1 for c in corners(LAM))
    assert sorted(c for c in young_cells(LAM) if hook_length(LAM, *c) == 1) == sorted(corners(LAM))
    # (2) 主張：(4,3,1) 的三個角落
    assert corners(LAM) == [(0, 3), (1, 2), (2, 0)]
    subs = [remove_corner(LAM, c) for c in corners(LAM)]
    assert subs == [(3, 3, 1), (4, 2, 1), (4, 3)] and [hook_product(s) for s in subs] == [240, 144, 360]
    probs = hook_walk_probs(LAM)
    assert [probs[c] for c in corners(LAM)] == [Fraction(3, 10), Fraction(1, 2), Fraction(1, 5)]
    for c, s in zip(corners(LAM), subs):
        assert probs[c] == corner_prob_formula(LAM, c) == Fraction(576, 8 * hook_product(s))
    assert sum(probs.values()) == 1
    for m in range(1, 8):                        # 主張對所有小形狀都成立（列舉所有漫步）
        for lam in integer_partitions(m):
            pr = hook_walk_probs(lam)
            assert all(pr[c] == corner_prob_formula(lam, c) == corner_prob_product(lam, c) for c in corners(lam))
            assert sum(pr.values()) == 1
    # (3) 投影
    wd = walk_weight(LAM, WALK_D)
    assert [hook_length(LAM, *c) for c in WALK_D] == [6, 4, 1]
    assert wd == Fraction(1, 15) and wd / n == Fraction(1, 120)
    A, B = walk_rows_cols(WALK_R)
    assert (A, B) == walk_rows_cols(WALK_D) == ((0, 1), (0, 2))
    # (4) 關鍵恆等式
    assert hook_identity(LAM, (0, 0), C) == (5, 2, 3)
    assert len(hook_cells(LAM, 0, 0)) - 1 == 5 and len(hook_cells(LAM, 0, 2)) - 1 == 2
    assert len(hook_cells(LAM, 1, 0)) - 1 == 3
    for m in range(1, 9):                        # 恆等式對所有形狀、角落、左上方的格子都成立
        for lam in integer_partitions(m):
            for c in corners(lam):
                for (a, b) in young_cells(lam):
                    if a <= c[0] and b <= c[1]:
                        hook_identity(lam, (a, b), c)
    # (5) 引理：例子，以及所有 (A, B)
    rhs = hook_lemma_rhs(LAM, C, A, B)
    grp = [(p, w) for s in young_cells(LAM) for p, w in hook_walks(LAM, s)
           if p[-1] == C and walk_rows_cols(p) == (A, B)]
    assert sorted(p for p, _ in grp) == sorted([WALK_R, WALK_D])
    assert wr + wd == rhs == Fraction(1, 6) == Fraction(1, 2) * Fraction(1, 3)
    assert hook_length(LAM, 0, 2) - 1 == 2 and hook_length(LAM, 1, 0) - 1 == 3
    down_rest, right_rest = hook_lemma_rhs(LAM, C, A[1:], B), hook_lemma_rhs(LAM, C, A, B[1:])
    assert (down_rest, right_rest) == (Fraction(1, 3), Fraction(1, 2))
    assert down_rest == rhs * 2 and right_rest == rhs * 3
    assert Fraction(1, 5) * (down_rest + right_rest) == rhs
    for lam in [LAM, (3, 2), (4, 4, 2, 1), (3, 3, 3)]:
        for c in corners(lam):
            tot = {}
            for s in young_cells(lam):
                for p, w in hook_walks(lam, s):
                    if p[-1] == c:
                        key = walk_rows_cols(p)
                        tot[key] = tot.get(key, 0) + w
            al, be = c
            keys = {(tuple(sorted(set(a) | {al})), tuple(sorted(set(b) | {be})))
                    for ka in range(al + 1) for a in combinations(range(al), ka)
                    for kb in range(be + 1) for b in combinations(range(be), kb)}
            assert set(tot) == keys and len(keys) == 2 ** (al + be)
            assert all(v == hook_lemma_rhs(lam, c, *k) for k, v in tot.items())
    # (6)(7) 加總與結論：c = (2,3)
    al, be = C
    xs = [Fraction(1, hook_length(LAM, i, be) - 1) for i in range(al)]
    ys = [Fraction(1, hook_length(LAM, al, j) - 1) for j in range(be)]
    assert xs == [Fraction(1, 2)] and ys == [Fraction(1, 3), Fraction(1, 1)]
    assert [hook_length(LAM, 0, 2), hook_length(LAM, 1, 0), hook_length(LAM, 1, 1)] == [3, 4, 2]
    prod = Fraction(1, n) * Fraction(3, 2) * Fraction(4, 3) * Fraction(2, 1)
    assert prod == corner_prob_product(LAM, C) == probs[C] == Fraction(1, 2) and 2 ** (al + be) == 8
    assert xs[0] * ys[0] == Fraction(1, 6)
    sub = remove_corner(LAM, C)
    assert sub == (4, 2, 1) and hook_lengths(sub) == [(6, 4, 2, 1), (3, 1), (1,)]
    changed = sorted(c for c in young_cells(sub) if hook_length(sub, *c) != hook_length(LAM, *c))
    assert changed == [(0, 2), (1, 0), (1, 1)]
    assert all(hook_length(LAM, *c) - hook_length(sub, *c) == 1 for c in changed)
    assert Fraction(576, 144) == 4 == Fraction(3, 2) * Fraction(4, 3) * Fraction(2, 1)
    for m in range(1, 9):                        # 拿掉角落只改變同列左邊、同行上面的鉤長（各減 1）
        for lam in integer_partitions(m):
            for c in corners(lam):
                s = remove_corner(lam, c)
                ch = sorted(x for x in young_cells(s) if hook_length(s, *x) != hook_length(lam, *x))
                assert ch == sorted([(i, c[1]) for i in range(c[0])] + [(c[0], j) for j in range(c[1])])
                assert all(hook_length(lam, *x) - hook_length(s, *x) == 1 for x in ch)
    # (3,2) 的數值驗算
    assert sum(len(hook_walks(SMALL, s)) for s in young_cells(SMALL)) == 9
    assert hook_walk_probs(SMALL) == {(0, 2): Fraction(2, 5), (1, 1): Fraction(3, 5)}
    print("附錄 A 第 4 段（A.12–A.14）的數字檢查通過")


# =============================================================================
# Young 圖的圖元（左上角在 (x0, y0)，格子邊長 s；第 i 列第 j 行，0 起算）
# =============================================================================
def cell_box(i, j, s, x0=0.0, y0=0.0):
    xl, yt = x0 + j * s, y0 - i * s
    return [(xl, yt), (xl + s, yt), (xl + s, yt - s), (xl, yt - s)]


def cell_center(i, j, s, x0=0.0, y0=0.0):
    return x0 + (j + 0.5) * s, y0 - (i + 0.5) * s


def young_prims(lam, s, x0=0.0, y0=0.0, fills=None, entries=None, font=r"\small", entry_colors=None,
                line="gray!70!black,line width=0.5pt"):
    """Young 圖：fills = {格子: 填色}；entries = 每列的數字；entry_colors = {格子: 文字顏色}。"""
    prims = []
    for (i, j), col in (fills or {}).items():
        prims.append(("fill", col, cell_box(i, j, s, x0, y0)))
    for i, j in young_cells(lam):
        prims.append(("poly", line, cell_box(i, j, s, x0, y0)))
    if entries is not None:
        for i, row in enumerate(entries):
            for j, v in enumerate(row):
                col = (entry_colors or {}).get((i, j))
                opts = f"font={font},inner sep=0pt" + (f",text={col}" if col else "")
                prims.append(node(cell_center(i, j, s, x0, y0), f"${v}$", opts, (0.1, 0.1)))
    return prims


def outline(i, j, s, x0, y0, color, width=1.3, inset=0.07, extra=""):
    """格子內側的方框（起點、角落等標記）。"""
    xl, yt = x0 + j * s + inset, y0 - i * s - inset
    return rf"\draw[{color},line width={width}pt{extra}] {pt(xl, yt)} rectangle {pt(xl + s - 2 * inset, yt - s + 2 * inset)};"


def jump(p, q, s, x0, y0, color=WALK):
    """一跳：同列往右在格子上半部向上拱；同行往下在格子左半部向左拱（不壓到中間的數字）。"""
    (pi, pj), (qi, qj) = p, q
    a, b = cell_center(pi, pj, s, x0, y0), cell_center(qi, qj, s, x0, y0)
    if pi == qi:
        off, bend = (0.0, 0.28 * s), "bend left=45"
    else:
        off, bend = (-0.28 * s, 0.0), "bend right=45"
    a = (a[0] + off[0], a[1] + off[1])
    b = (b[0] + off[0], b[1] + off[1])
    return (rf"\draw[-{{Stealth[length=4.5pt,width=4pt]}},{color},line width=1.1pt,shorten <=1pt,shorten >=1pt] "
            rf"{pt(*a)} to[{bend}] {pt(*b)};")


def arrow(a, b, label=None, color="gray!60!black", above=True):
    side = "above" if above else "below"
    lab = rf" node[midway,{side},font=\footnotesize,text=black] {{{label}}}" if label else ""
    return rf"\draw[-{{Stealth[length=5pt]}},{color},line width=0.7pt] {pt(*a)} -- {pt(*b)}{lab};"


def ftex(x) -> str:
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else rf"\frac{{{x.numerator}}}{{{x.denominator}}}"


# =============================================================================
# A.12 標準 Young 表與 Dyck 路徑
# =============================================================================
def fig_m12_convert() -> str:
    """貫穿的例子：(3,3) 的表 [[1,2,4],[3,5,6]]，第一列 -> U、第二列 -> D，得到 UUDUDD。"""
    s = 0.62
    word = syt_to_dyck(EX_T)
    fills = {(i, j): ROW_FILL[i] for i, j in young_cells(SQUARE)}
    lines = emit(young_prims(SQUARE, s, 0.0, 0.0, fills=fills, entries=EX_T))
    for i, (txt, col) in enumerate([(r"\mathrm{U}", "cLeft"), (r"\mathrm{D}", "cRight")]):
        y = -(i + 0.5) * s
        lines += emit([node((3 * s + 0.12, y), rf"$\to{txt}$", f"anchor=west,font=\\small,text={col}", (0.3, 0.12))])
    lines.append(arrow((3.1, -0.62), (4.0, -0.62)))
    u, xb, yb = 0.46, 4.35, -0.9
    parts = ["left" if c == "U" else "right" for c in word]
    lines += emit(dyck_prims(word, u, parts, w=1.5), xb, yb)
    h = 0
    for k, c in enumerate(word):
        lines.append(rf"\fill[black] {pt(xb + k * u, yb + h * u)} circle (0.035);")
        h += 1 if c == "U" else -1
    lines.append(rf"\fill[black] {pt(xb + len(word) * u, yb)} circle (0.035);")
    for k, c in enumerate(word):
        x = xb + (k + 0.5) * u
        col = "cLeft" if c == "U" else "cRight"
        lines += emit([node((x, yb - 0.24), f"{k + 1}", "font=\\scriptsize,text=gray!70!black", (0.1, 0.1)),
                       node((x, yb - 0.56), rf"$\mathrm{{{c}}}$", f"font=\\small,text={col}", (0.1, 0.12))])
    lines += emit([node((xb - 0.3, yb - 0.24), "步", "anchor=east,font=\\scriptsize,text=gray!70!black", (0.2, 0.1))])
    return picture(lines)


def fig_m12_all() -> str:
    """(3,3) 的 5 個標準 Young 表與 5 條 Dyck 路徑（順序同動畫 M12），框出貫穿的例子。"""
    s, u, step = 0.34, 0.2, 2.25
    lines = []
    for k, T in enumerate(syt(SQUARE)):
        x = step * k
        x0 = x - 1.5 * s
        fills = {(i, j): ROW_FILL[i] for i, j in young_cells(SQUARE)}
        lines += emit(young_prims(SQUARE, s, x0, 0.0, fills=fills, entries=T, font=r"\scriptsize"))
        lines.append(rf"\node[font=\small,text=gray!60!black] at {pt(x, -0.98)} {{$\downarrow$}};")
        w = syt_to_dyck(T)
        parts = ["left" if c == "U" else "right" for c in w]
        lines += emit(dyck_prims(w, u, parts, w=1.2), x - 3 * u, -1.9)
        lines.append(rf"\node[font=\scriptsize] at {pt(x, -2.16)} {{$\mathrm{{{w}}}$}};")
        if T == EX_T:
            lines.append(rf"\draw[{WALK},dashed,line width=0.7pt,rounded corners=3pt] {pt(x - 0.85, 0.14)} "
                         rf"rectangle {pt(x + 0.85, -2.38)};")
    return picture(lines)


def fig_gen_tableau(T, bad=False) -> str:
    """一般形狀 (2,2,1) 的小表（行內用）；bad=True 時把 4、5 與它們那一行標紅。"""
    s = 0.36
    fills = {(i, j): ROW_FILL[i] for i, j in young_cells(GEN_LAM)}
    cols = {}
    if bad:
        cols = {(i, j): "cBad" for i, row in enumerate(T) for j, v in enumerate(row) if v in (4, 5)}
    lines = emit(young_prims(GEN_LAM, s, 0.0, 0.0, fills=fills, entries=T, font=r"\footnotesize", entry_colors=cols))
    if bad:
        lines.append(rf"\draw[cBad,line width=1pt] {pt(s, 0)} rectangle {pt(2 * s, -2 * s)};")
    lines.append(rf"\path {pt(-0.05, 0.14)} rectangle {pt(2 * s + 0.05, -3 * s - 0.14)};")   # 表格列的上下留白
    return picture(lines, f"baseline={{(0,{-1.5 * s - 0.09:.2f})}}")


# =============================================================================
# A.13 鉤長公式
# =============================================================================
def fig_m13_hook() -> str:
    """左：(4,3,1) 的格子 (1,2) 的鉤（自己＋臂＋腿）；右：每一格的鉤長。"""
    s = 0.62
    i, j = HOOK_EX
    hk = hook_cells(LAM, i, j)
    fills = {c: HOOK_FILL for c in hk[1:]}
    fills[hk[0]] = SELF_FILL
    lines = emit(young_prims(LAM, s, 0.0, 0.0, fills=fills))
    lines += emit([node(cell_center(i, j, s), "$c$", "font=\\small", (0.1, 0.1))])
    # 臂：上方的括線；腿：下方的標籤
    xa, xb, y = 2 * s + 0.06, 4 * s - 0.06, 0.1
    lines.append(rf"\draw[orange!70!black,line width=0.6pt] {pt(xa, y)} -- {pt(xa, y + 0.1)} -- {pt(xb, y + 0.1)} -- {pt(xb, y)};")
    lines += emit([node(((xa + xb) / 2, y + 0.33), "臂", "font=\\footnotesize,text=orange!70!black", (0.15, 0.12))])
    yl = -2 * s - 0.1
    lines.append(rf"\draw[orange!70!black,line width=0.6pt] {pt(s + 0.06, yl)} -- {pt(s + 0.06, yl - 0.1)} -- "
                 rf"{pt(2 * s - 0.06, yl - 0.1)} -- {pt(2 * s - 0.06, yl)};")
    lines += emit([node((1.5 * s, yl - 0.33), "腿", "font=\\footnotesize,text=orange!70!black", (0.15, 0.12))])
    lines += emit([node((2 * s, -3 * s - 0.55), r"$h(c)=2+1+1=4$", "font=\\small", (0.8, 0.12))])
    # 右：鉤長
    x0 = 4 * s + 1.7
    lines += emit(young_prims(LAM, s, x0, 0.0, entries=hook_lengths(LAM)))
    lines += emit([node((x0 + 2 * s, -3 * s - 0.55), r"$H(\lambda)=576$", "font=\\small", (0.8, 0.12))])
    return picture(lines)


def fig_hooks_inline(lam, row_colors=None) -> str:
    """行內的小 Young 圖，每格寫鉤長。"""
    s = 0.4
    tab = hook_lengths(lam)
    cols = {}
    if row_colors:
        cols = {(i, j): row_colors[i] for i, j in young_cells(lam)}
    lines = emit(young_prims(lam, s, 0.0, 0.0, entries=tab, font=r"\footnotesize", entry_colors=cols))
    return picture(lines, f"baseline={{(0,{-len(lam) * s / 2 - 0.08:.2f})}}")


def fig_m13_corner() -> str:
    """(3,2) 的 5 個表依 5 的位置分成兩組；拿掉 5 得到 (2,2) 與 (3,1) 的表。"""
    s = 0.36
    n = sum(SMALL)
    cs = corners(SMALL)
    lines = []
    # 左：λ 與它的兩個角落
    bx, by = 0.0, -0.37
    lines += emit(young_prims(SMALL, s, bx, by, fills={c: CORNER_FILL for c in cs}))
    lines += emit([node((bx + 1.5 * s, by - 2 * s - 0.27), r"$\lambda=(3,2)$", "font=\\footnotesize", (0.5, 0.1)),
                   node((bx + 1.5 * s, by + 0.22), "角落", f"font=\\scriptsize,text={CORNER}!80!black", (0.3, 0.1))])
    row_y = [0.3, -1.05]
    x_tab = 2.0
    for r, c in enumerate(cs):
        g = [T for T in syt(SMALL) if T[c[0]][c[1]] == n]
        y0 = row_y[r]
        for k, T in enumerate(g):
            x0 = x_tab + k * (3 * s + 0.3)
            lines += emit(young_prims(SMALL, s, x0, y0, fills={c: CORNER_FILL}, entries=T, font=r"\scriptsize"))
        ya = y0 - s
        xa = x_tab + 3 * (3 * s + 0.3) + 0.05
        lines.append(arrow((xa, ya), (xa + 1.05, ya), label=r"拿掉 $5$"))
        sub = remove_corner(SMALL, c)
        xs = xa + 1.3
        lines += emit(young_prims(sub, s, xs, y0))
        lines += emit([node((xs + sub[0] * s + 0.3, ya), rf"$f^{{({sub[0]},{sub[1]})}}={syt_count(sub)}$",
                            "anchor=west,font=\\small", (0.6, 0.12))])
    return picture(lines)


# =============================================================================
# A.14 鉤上漫步
# =============================================================================
def walk_panel(walk, x0, y0, s, show_proj=True, all_corners=False):
    """(4,3,1) 上的一條漫步：鉤長（灰）、起點（橘框）、終點角落（綠）、跳躍箭頭、列號與行號。"""
    ends = corners(LAM) if all_corners else [walk[-1]]
    fills = {c: CORNER_FILL for c in ends}
    gray = {c: "gray!55!black" for c in young_cells(LAM)}
    lines = emit(young_prims(LAM, s, x0, y0, fills=fills, entries=hook_lengths(LAM), font=r"\footnotesize",
                             entry_colors=gray))
    lines.append(outline(*walk[0], s, x0, y0, WALK, width=1.4))
    for p, q in zip(walk, walk[1:]):
        lines.append(jump(p, q, s, x0, y0))
    A, B = walk_rows_cols(walk)
    for i in range(len(LAM)):
        on = show_proj and i in A
        style = r"font=\scriptsize\bfseries,text=cLeft" if on else r"font=\scriptsize,text=gray!60!black"
        lines.append(rf"\node[{style}] at {pt(x0 - 0.32, y0 - (i + 0.5) * s)} {{{i + 1}}};")
    for j in range(LAM[0]):
        on = show_proj and j in B
        style = r"font=\scriptsize\bfseries,text=cRight" if on else r"font=\scriptsize,text=gray!60!black"
        lines.append(rf"\node[{style}] at {pt(x0 + (j + 0.5) * s, y0 + 0.2)} {{{j + 1}}};")
    return lines


def fig_m14_walks() -> str:
    """兩條投影相同的漫步：(1,1)->(1,3)->(2,3) 與 (1,1)->(2,1)->(2,3)。"""
    s, n = 0.62, sum(LAM)
    A, B = walk_rows_cols(WALK_R)
    lines = []
    for k, walk in enumerate((WALK_R, WALK_D)):
        x0 = 5.4 * k
        lines += walk_panel(walk, x0, 0.0, s)
        hs = [hook_length(LAM, *c) for c in walk[:-1]]
        w = walk_weight(LAM, walk)
        prob = rf"\frac{{1}}{{{n}}}" + "".join(rf"\cdot\frac{{1}}{{{h - 1}}}" for h in hs) + f"={ftex(w / n)}"
        cx = x0 + 2 * s
        lines.append(rf"\node[font=\small] at {pt(cx, -3 * s - 0.45)} {{${prob}$}};")
        a_tex = r"\textcolor{cLeft}{A=\{" + ",".join(str(i + 1) for i in A) + r"\}}"
        b_tex = r"\textcolor{cRight}{B=\{" + ",".join(str(j + 1) for j in B) + r"\}}"
        lines.append(rf"\node[font=\small] at {pt(cx, -3 * s - 1.0)} {{${a_tex},\ {b_tex}$}};")
    return picture(lines)


def fig_m14_identity() -> str:
    """關鍵恆等式 5 = 2 + 3：(1,1)、(1,3)、(2,1) 的鉤上「自己以外」的格子。"""
    s = 0.42
    al, be = C
    specs = [((0, 0), HOOK_FILL, r"h(a,b)-1"), ((0, be), "cLeft!35", r"h(a,\beta)-1"),
             ((al, 0), "cRight!30", r"h(\alpha,b)-1")]
    lines = []
    for k, (cell, col, lab) in enumerate(specs):
        x0 = 2.75 * k
        hk = hook_cells(LAM, *cell)
        lines += emit(young_prims(LAM, s, x0, 0.0, fills={c: col for c in hk[1:]}))
        lines.append(outline(*cell, s, x0, 0.0, WALK, width=1.3, inset=0.06))
        lines.append(outline(*C, s, x0, 0.0, CORNER, width=1.3, inset=0.06, extra=",densely dashed"))
        lines.append(rf"\node[font=\small] at {pt(x0 + 2 * s, 0.32)} {{${lab}$}};")
        lines.append(rf"\node[font=\normalsize] at {pt(x0 + 2 * s, -3 * s - 0.32)} {{${len(hk) - 1}$}};")
    for k, sign in enumerate(("=", "+")):
        lines.append(rf"\node[font=\large] at {pt(2.75 * k + 4 * s + (2.75 - 4 * s) / 2, -1.5 * s)} {{${sign}$}};")
    return picture(lines)


def fig_m14_remove() -> str:
    """拿掉角落 c = (2,3)：只有 c 上方（青）與左方（紫紅）的格子鉤長各減 1。"""
    s = 0.55
    al, be = C
    up = [(i, be) for i in range(al)]
    left = [(al, j) for j in range(be)]
    sub = remove_corner(LAM, C)
    fl = {**{c: "cLeft!30" for c in up}, **{c: "cRight!28" for c in left}, C: CORNER_FILL}
    fr = {**{c: "cLeft!30" for c in up}, **{c: "cRight!28" for c in left}}
    lines = emit(young_prims(LAM, s, 0.0, 0.0, fills=fl, entries=hook_lengths(LAM)))
    x1 = 4 * s + 2.0
    lines += emit(young_prims(sub, s, x1, 0.0, fills=fr, entries=hook_lengths(sub)))
    xl, yt = x1 + be * s, -al * s
    lines.append(rf"\draw[gray!60,densely dashed,line width=0.6pt] {pt(xl, yt)} rectangle {pt(xl + s, yt - s)};")
    lines.append(arrow((4 * s + 0.35, -1.5 * s), (x1 - 0.35, -1.5 * s), label=r"拿掉 $c$"))
    for x, lab, hval in ((0.0, r"\lambda=(4,3,1)", r"H(\lambda)=576"), (x1, r"\lambda-c=(4,2,1)", r"H(\lambda-c)=144")):
        lines.append(rf"\node[font=\small] at {pt(x + 2 * s, 0.3)} {{${lab}$}};")
        lines.append(rf"\node[font=\small] at {pt(x + 2 * s, -3 * s - 0.3)} {{${hval}$}};")
    return picture(lines)


FIGURES = [
    ("FigMXIIConvert", fig_m12_convert),
    ("FigMXIIAll", fig_m12_all),
    ("FigMXIIGenGood", lambda: fig_gen_tableau(GEN_T)),
    ("FigMXIIGenBad", lambda: fig_gen_tableau(BAD_T, bad=True)),
    ("FigMXIIIHook", fig_m13_hook),
    ("FigMXIIIHookSmall", lambda: fig_hooks_inline(SMALL)),
    ("FigMXIIIHookSquare", lambda: fig_hooks_inline(SQUARE, ["cLeft", "cRight"])),
    ("FigMXIIICorner", fig_m13_corner),
    ("FigMXIVWalks", fig_m14_walks),
    ("FigMXIVIdentity", fig_m14_identity),
    ("FigMXIVRemove", fig_m14_remove),
]


def main():
    check_numbers()
    parts = [
        "% figs_part4.tex —— 由 mit/make_figs_part4.py 產生，請勿手動修改。\n"
        "% 重新產生：python mit/make_figs_part4.py（附錄 A.12–A.14，動畫 M12–M14）\n"
    ]
    for name, func in FIGURES:
        body = func()
        assert "\n\n" not in body
        parts.append(f"\\newcommand{{\\{name}}}{{%\n{body}}}\n")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"已寫出 {OUT.name}：{len(FIGURES)} 張圖")


if __name__ == "__main__":
    main()
