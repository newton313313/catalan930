r"""
make_figs_part3.py —— 附錄 A 第 3 段（A.9 堆疊與佇列排序、A.10 模式迴避、A.11 整數分割與 Young 表）的 TikZ 圖

在 notes/ 或任何地方執行：
    python mit/make_figs_part3.py
會先檢查 mit/part3.tex 寫到的每一個數字（check_numbers），再寫出 mit/figs_part3.tex
（part3.tex 第一行 \input{mit/figs_part3} 讀進來）。

數學資料一律由 codes/utils/counting.py 算（與動畫 M09–M11 同一份），
TikZ 圖元的小工具從 notes/make_catalan_figs.py 匯入（不複製）。
顏色：一般的卡塔蘭物件 cA（藍）、根／左／右 cTop／cLeft／cRight、不合法 cBad（紅）。
"""
from __future__ import annotations

import re
import sys
from itertools import combinations, permutations
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent            # notes/mit
NOTES = HERE.parent                               # notes
sys.path.insert(0, str(NOTES.parent / "codes"))
sys.path.insert(0, str(NOTES))

from utils.counting import (  # noqa: E402
    PATTERNS_3,
    avoiders,
    catalan,
    closed_form,
    contains_pattern,
    dyck_to_matching,
    dyck_words,
    integer_compositions,
    integer_partitions,
    is_noncrossing,
    partition_count,
    queue_bypass_sort,
    sort_states,
    stack_sort,
    standardize,
    syt,
    syt_bruteforce,
    syt_count,
    young_cells,
)
from make_catalan_figs import circle_point, emit, node, picture, pt  # noqa: E402

OUT = HERE / "figs_part3.tex"
MAIN_TEX = NOTES / "chu1987_導讀.tex"                # 只讀，用來核對警告框裡引用的主文圖與節次

# 與動畫 M09–M11 相同的例子
STACK_OK, STACK_BAD = "4213", "231"          # M09
QUEUE_OK, QUEUE_BAD = "231", "321"           # M09
W, AV, PAT = (4, 1, 5, 3, 2), (5, 2, 1, 4, 3), (2, 3, 1)   # M10
YOUNG_EX, SHAPE = (5, 3, 3, 2, 1), (3, 2)    # M11
GOOD_T = ((1, 2, 4), (3, 5))                 # 貫穿例子的 SYT (3,3) 拿掉 6
BAD_T = ((1, 4, 5), (2, 3))                  # 每列遞增，但第 2 行 4 在 3 上面
SET_BLOCKS = [(0, 1, 4), (2, 3)]             # Chu 的集合分割 {1,2,5},{3,4}（0 起算）
RUNNING_SYT = ((1, 2, 4), (3, 5, 6))         # mit_plan.md 第 3 節
RUNNING_DYCK = "UUDUDD"


# =============================================================================
# 小工具
# =============================================================================
def word(p) -> str:
    return "".join(str(x) for x in p)


def op_word(ops) -> str:
    """推入 -> U、彈出 -> D。"""
    return "".join("U" if op == "push" else "D" for op, _ in ops)


def reverse(p):
    return tuple(reversed(p))


def complement(p):
    return tuple(len(p) + 1 - x for x in p)


def stack_any(perm) -> bool:
    """獨立檢查：允許任何推入／彈出的順序（彈出只能輸出下一個要的數），看有沒有一種能排好。"""
    perm = tuple(perm)
    n, seen = len(perm), set()

    def rec(i, stack, need):
        if need > n:
            return True
        key = (i, stack)
        if key in seen:
            return False
        seen.add(key)
        if stack and stack[-1] == need and rec(i, stack[:-1], need + 1):
            return True
        return i < n and rec(i + 1, stack + (perm[i],), need)

    return rec(0, (), 1)


def queue_any(perm) -> bool:
    """獨立檢查：佇列＋插隊線，允許任何合法的順序（排入、插隊、出列），看有沒有一種能排好。"""
    perm = tuple(perm)
    n, seen = len(perm), set()

    def rec(i, queue, need):
        if need > n:
            return True
        key = (i, queue)
        if key in seen:
            return False
        seen.add(key)
        if queue and queue[0] == need and rec(i, queue[1:], need + 1):
            return True
        if i < n and perm[i] == need and rec(i + 1, queue, need + 1):
            return True
        return i < n and rec(i + 1, queue + (perm[i],), need)

    return rec(0, (), 1)


def push_pop_matching(perm, ops):
    """同一個數的推入與彈出配成一對（0 起算的步數）。"""
    where = {}
    for k, (op, x) in enumerate(ops):
        where.setdefault(x, []).append(k)
    return sorted(tuple(v) for v in where.values())


def split_at_max(w):
    k = w.index(max(w))
    return w[:k], w[k + 1:]


# =============================================================================
# part3.tex 寫到的數字
# =============================================================================
def check_numbers():
    # ---------------------------------------------------------------- A.9 堆疊排序 4213（正文的例子）
    ok, ops = stack_sort(STACK_OK)
    assert ok and op_word(ops) == "UUUDDUDD"
    names = {"push": "推入", "pop": "彈出", "bypass": "插隊"}
    assert [(names[o], x) for o, x in ops] == [("推入", 4), ("推入", 2), ("推入", 1), ("彈出", 1),
                                               ("彈出", 2), ("推入", 3), ("彈出", 3), ("彈出", 4)]
    assert sort_states(STACK_OK, ops) == [
        ((4, 2, 1, 3), (), ()), ((2, 1, 3), (4,), ()), ((1, 3), (4, 2), ()), ((3,), (4, 2, 1), ()),
        ((3,), (4, 2), (1,)), ((3,), (4,), (1, 2)), ((), (4, 3), (1, 2)), ((), (4,), (1, 2, 3)),
        ((), (), (1, 2, 3, 4))]
    # 佇列＋插隊線排 231（正文的例子）
    ok, ops = queue_bypass_sort(QUEUE_OK)
    q_names = {"push": "排入", "pop": "出列", "bypass": "插隊"}
    assert ok and [(q_names[o], x) for o, x in ops] == [("排入", 2), ("排入", 3), ("插隊", 1),
                                                        ("出列", 2), ("出列", 3)]
    assert sort_states(QUEUE_OK, ops) == [
        ((2, 3, 1), (), ()), ((3, 1), (2,), ()), ((1,), (2, 3), ()), ((), (2, 3), (1,)),
        ((), (3,), (1, 2)), ((), (), (1, 2, 3))]
    # 卡住的狀態（圖 fig:m09-stuck）：堆疊排 231 -> 堆疊 2,3（底到頂）、輸出 1；佇列排 321 -> 佇列 3,2、輸出 1
    ok, ops = stack_sort(STACK_BAD)
    assert not ok and sort_states(STACK_BAD, ops)[-1] == ((), (2, 3), (1,))
    ok, ops = queue_bypass_sort(QUEUE_BAD)
    assert not ok and sort_states(QUEUE_BAD, ops)[-1] == ((), (3, 2), (1,))
    # n = 3：堆疊只排不了 231，佇列＋插隊線只排不了 321
    p3 = list(permutations((1, 2, 3)))
    assert [p for p in p3 if not stack_sort(p)[0]] == [(2, 3, 1)]
    assert [p for p in p3 if not queue_bypass_sort(p)[0]] == [(3, 2, 1)]
    # 規則沒有錯過任何排法；可排序 <=> 避開 231／321；個數 C_n（n <= 8）
    for n in range(1, 9):
        perms = list(permutations(range(1, n + 1)))
        ss = {p for p in perms if stack_sort(p)[0]}
        qs = {p for p in perms if queue_bypass_sort(p)[0]}
        assert ss == set(avoiders(n, PAT)) and qs == set(avoiders(n, (3, 2, 1)))
        assert len(ss) == len(qs) == catalan(n)
        if n <= 6:
            assert ss == {p for p in perms if stack_any(p)} and qs == {p for p in perms if queue_any(p)}
    assert (catalan(3), catalan(4)) == (5, 14)
    # 推入 = U、彈出 = D：堆疊可排序的排列 <-> Dyck 路徑（一一對應）；同一個數的推入、彈出 = 不交叉配對
    for n in range(0, 8):
        words = {}
        for p in permutations(range(1, n + 1)):
            ok, ops = stack_sort(p)
            if ok:
                wd = op_word(ops)
                assert wd not in words
                words[wd] = p
                assert push_pop_matching(p, ops) == dyck_to_matching(wd)
        assert sorted(words) == sorted(dyck_words(n))
    assert op_word(stack_sort("312")[1]) == RUNNING_DYCK
    assert dyck_to_matching(RUNNING_DYCK) == [(0, 5), (1, 2), (3, 4)]          # 配對 (1,6),(2,3),(4,5)

    # ---------------------------------------------------------------- A.10 模式迴避
    occ = contains_pattern(W, PAT)
    assert occ == (0, 2, 3) and tuple(W[i] for i in occ) == (4, 5, 3) and standardize((4, 5, 3)) == PAT
    triples = list(combinations(range(5), 3))
    assert len(triples) == comb(5, 3) == 10
    pats = {standardize([AV[i] for i in t]) for t in triples}
    assert pats == {(3, 2, 1), (3, 1, 2), (2, 1, 3), (1, 3, 2)} and contains_pattern(AV, PAT) is None
    assert stack_sort(AV)[0]
    # n = 3：6 個中 5 個避開 231（只有 231 自己含有）；n = 4：24 個中 14 個
    assert factorial(3) == 6 and len(avoiders(3, PAT)) == 5
    assert [p for p in p3 if contains_pattern(p, PAT) is not None] == [PAT]
    assert factorial(4) == 24 and len(avoiders(4, PAT)) == 14
    # 定理框裡的表：6 個長度 3 的模式，n = 1..6
    assert [catalan(n) for n in range(1, 7)] == [1, 2, 5, 14, 42, 132]
    for p in PATTERNS_3:
        assert [len(avoiders(n, p)) for n in range(1, 7)] == [1, 2, 5, 14, 42, 132]
    # 以最大的數 n 切開：w = L n R；避開 231 <=> L 全部小於 R，且 L、R 都避開 231
    for n in range(1, 8):
        for w in permutations(range(1, n + 1)):
            L, R = split_at_max(w)
            good = (all(a < b for a in L for b in R) and contains_pattern(L, PAT) is None
                    and contains_pattern(R, PAT) is None)
            assert good == (contains_pattern(w, PAT) is None)
        assert len(avoiders(n, PAT)) == sum(catalan(k) * catalan(n - 1 - k) for k in range(n))
    assert split_at_max((2, 1, 5, 3, 4)) == ((2, 1), (3, 4)) and contains_pattern((2, 1, 5, 3, 4), PAT) is None
    assert split_at_max(W) == ((4, 1), (3, 2)) and 4 > 3
    assert split_at_max(AV) == ((), (2, 1, 4, 3))
    # 反轉、補：231 -> 132、213、312；123 <-> 321
    assert reverse(PAT) == (1, 3, 2) and complement(PAT) == (2, 1, 3) and reverse(complement(PAT)) == (3, 1, 2)
    assert reverse((1, 2, 3)) == complement((1, 2, 3)) == (3, 2, 1)
    for n in range(1, 7):
        for p in PATTERNS_3:
            assert len(avoiders(n, reverse(p))) == len(avoiders(n, complement(p))) == len(avoiders(n, p))

    # ---------------------------------------------------------------- A.11 整數分割與 Young 表
    parts = integer_partitions(5)
    assert parts == [(5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1)]
    assert len(parts) == 7 == partition_count(5)
    comps = integer_compositions(5)
    assert len(comps) == 16 == 2 ** 4
    assert sorted(c for c in comps if all(c[k] >= c[k + 1] for k in range(len(c) - 1))) == sorted(parts)
    assert (3, 2) in parts and (2, 3) in comps and (2, 3) not in parts
    assert sum(YOUNG_EX) == 14 and YOUNG_EX in integer_partitions(14) and len(young_cells(YOUNG_EX)) == 14
    tabs = syt(SHAPE)
    assert tabs == [((1, 2, 3), (4, 5)), ((1, 2, 4), (3, 5)), ((1, 2, 5), (3, 4)),
                    ((1, 3, 4), (2, 5)), ((1, 3, 5), (2, 4))]
    assert set(tabs) == syt_bruteforce(SHAPE) and syt_count(SHAPE) == 5
    assert GOOD_T in tabs and GOOD_T == (RUNNING_SYT[0], RUNNING_SYT[1][:-1])
    assert BAD_T not in syt_bruteforce(SHAPE) and BAD_T[0][1] == 4 and BAD_T[1][1] == 3
    assert all(r[j] < r[j + 1] for r in BAD_T for j in range(len(r) - 1))
    assert syt_count((3, 3)) == 5 == catalan(3) and RUNNING_SYT in syt((3, 3))
    assert all(syt_count((k, k)) == catalan(k) for k in range(1, 8))
    # Chu：集合分割 {1,2,5},{3,4} 不交叉；原文例子 n=(1,1), v=(2,3) 的區塊大小由大到小 = (3,2) ⊢ 5
    assert is_noncrossing(SET_BLOCKS)
    n_vec, v_vec = (1, 1), (2, 3)
    sizes = tuple(sorted((v for v, m in zip(v_vec, n_vec) for _ in range(m)), reverse=True))
    assert sizes == (3, 2) and sum(sizes) == 5 and closed_form(n_vec, v_vec) == 5
    assert tuple(sorted(map(len, SET_BLOCKS), reverse=True)) == sizes
    # 警告框引用主文：「圖 fig:paper 的第 5 個」= {1,2,5},{3,4}；「第 2 節」講群組；「第 3 節原文例子」n=(1,1), v=(2,3)
    text = MAIN_TEX.read_text(encoding="utf-8")
    end = text.index(r"\label{fig:paper}")
    cfgs = re.findall(r"\\PaperCfg\{(\d)\}\{(\d)\}\{(\d)\}\{(\d)\}\{(\d)\}", text[text.rindex(r"\begin{figure}", 0, end):end])
    assert len(cfgs) == 5
    chord, tri = {int(c) for c in cfgs[4][:2]}, {int(c) for c in cfgs[4][2:]}
    assert (tri, chord) == ({b + 1 for b in SET_BLOCKS[0]}, {b + 1 for b in SET_BLOCKS[1]}) == ({1, 2, 5}, {3, 4})

    def section_no(pos):
        """pos 所在的節次 = pos 之前（含 pos 開頭）出現過幾個 \\section{。"""
        return len(re.findall(r"\\section\{", text[:pos + len(r"\section{")]))

    assert section_no(text.index(r"\section{從「兩點一組」到「$v$ 點一組」}")) == 2
    assert section_no(text.index(r"\subsection{原文的例子：$\vn=(1,1)$，$\vv=(2,3)$}")) == 3
    assert section_no(end) == 3
    print("附錄 A 第 3 段的數字檢查通過")


# =============================================================================
# 圖元
# =============================================================================
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def box_prims(c, half, text, style="plain"):
    """一個數字方塊；style = plain / out / bad / want / empty。"""
    x, y = c
    pts = rect(x - half, y - half, x + half, y + half)
    styles = {
        "plain": ("gray!8", "gray!70!black,line width=0.6pt"),
        "out": ("cA!14", "cA,line width=0.8pt"),
        "bad": ("cBad!22", "cBad,line width=1.1pt"),
        "want": ("cB!18", "cB,line width=1.1pt"),
        "empty": (None, "gray!55,dashed,line width=0.5pt"),
    }
    fill, draw = styles[style]
    prims = []
    if fill:
        prims.append(("fill", fill, pts))
    prims.append(("poly", draw, pts))
    if text:
        prims.append(node((x, y), f"${text}$", "font=\\small", (half, half)))
    return prims


def young_prims(lam, u, entries=None, fill="cA!14", cell_fill=None, font="\\small", lw=0.6):
    """英式 Young 圖，左上角在 (0, 0)。cell_fill = {(i, j): 顏色} 覆蓋個別格子的底色。"""
    prims = []
    for i, r in enumerate(lam):
        for j in range(r):
            x0, y0 = j * u, -i * u
            pts = rect(x0, y0 - u, x0 + u, y0)
            f = (cell_fill or {}).get((i, j), fill)
            if f:
                prims.append(("fill", f, pts))
            prims.append(("poly", f"gray!60!black,line width={lw}pt", pts))
            if entries:
                prims.append(node((x0 + u / 2, y0 - u / 2), f"${entries[i][j]}$", f"font={font}", (u / 2, u / 2)))
    return prims


def perm_plot_prims(w, u, occ=(), base="cA", dot_r=0.075, label_font="\\small"):
    """排列的點圖：第 i 個數 w_i 畫在 (i, w_i)；occ（0 起算的位置）塗成 cTop 並連線，下面寫出 w。"""
    n = len(w)
    lo, hi = 0.45 * u, (n + 0.55) * u
    prims = [("poly", "gray!45,line width=0.4pt", rect(lo, lo, hi, hi))]
    for k in range(1, n + 1):
        prims.append(("line", "gray!18,line width=0.3pt", (k * u, lo), (k * u, hi)))
        prims.append(("line", "gray!18,line width=0.3pt", (lo, k * u), (hi, k * u)))
    occ_pts = [((i + 1) * u, w[i] * u) for i in occ]
    for a, b in zip(occ_pts[:-1], occ_pts[1:]):
        prims.append(("line", "cTop,line width=0.9pt", a, b))
    for i, v in enumerate(w):
        color = "cTop" if i in occ else (base if not occ else "gray!55")
        prims.append(("dot", color, ((i + 1) * u, v * u), dot_r * (1.25 if i in occ else 1.0)))
        tc = "cTop" if i in occ else "black"
        prims.append(node(((i + 1) * u, lo - 0.22), f"${v}$", f"font={label_font},text={tc}", (0.08, 0.13)))
    return prims


# =============================================================================
# 圖
# =============================================================================
def fig_m09_stuck() -> str:
    """堆疊排 231、佇列＋插隊線排 321：卡住的那一刻。"""
    h, pitch = 0.25, 0.6
    lines = []
    lab = "font=\\small,text=gray!40!black"
    arrow = "-{Stealth[length=2.2mm]},gray!60!black,line width=0.7pt"

    # ---------------- (a) 堆疊，231：輸出 1；堆疊（底到頂）2, 3；輸入用完
    y = 1.5
    prims = []
    for k in range(3):
        prims += box_prims((k * pitch, y), h, "1" if k == 0 else "", "out" if k == 0 else "empty")
    sx, bottom, top, half_w = 2.55, -0.45, 1.05, 0.36
    prims += box_prims((sx, bottom + 0.05 + h), h, "2", "want")
    prims += box_prims((sx, bottom + 0.05 + h + pitch), h, "3", "bad")
    for k in range(3):
        prims += box_prims((3.95 + k * pitch, y), h, "", "empty")
    prims += [node((0.6, y + 0.52), "輸出", lab, (0.4, 0.15)),
              node((4.55, y + 0.52), "輸入（已用完）", lab, (0.8, 0.15)),
              node((sx, bottom - 0.3), "堆疊", lab, (0.3, 0.15))]
    lines += emit(prims)
    lines.append(rf"\draw[gray!60!black,line width=1.2pt] {pt(sx - half_w, top)} -- {pt(sx - half_w, bottom)}"
                 rf" -- {pt(sx + half_w, bottom)} -- {pt(sx + half_w, top)};")
    lines.append(rf"\draw[{arrow}] {pt(3.6, y)} -- {pt(sx + 0.15, top + 0.12)};")
    lines.append(rf"\draw[{arrow}] {pt(sx - 0.15, top + 0.12)} -- {pt(1.55, y)};")
    lines.append(rf"\node[font=\footnotesize,text=gray!40!black] at {pt(3.35, 1.0)} {{推入}};")
    lines.append(rf"\node[font=\footnotesize,text=gray!40!black] at {pt(1.75, 1.0)} {{彈出}};")
    lines.append(rf"\node[font=\small] at {pt(2.55, -1.25)} {{(a) 堆疊排 $231$}};")

    # ---------------- (b) 佇列＋插隊線，321：輸出 1（走插隊線）；佇列（頭到尾）3, 2；輸入用完
    ox, y = 7.1, 0.35
    prims = []
    for k in range(3):
        prims += box_prims((ox + k * pitch, y), h, "1" if k == 0 else "", "out" if k == 0 else "empty")
    q0, q1, qh = ox + 1.95, ox + 3.5, 0.36
    prims += box_prims((q0 + 0.42, y), h, "3", "bad")
    prims += box_prims((q0 + 0.42 + pitch, y), h, "2", "want")
    for k in range(3):
        prims += box_prims((ox + 4.25 + k * pitch, y), h, "", "empty")
    # 三個標籤都放在下面一排，上方只留插隊線（避免虛線穿過「輸入」字樣）
    prims += [node((ox + 0.6, y - 0.62), "輸出", lab, (0.4, 0.15)),
              node((ox + 4.85, y - 0.62), "輸入（已用完）", lab, (0.8, 0.15)),
              node(((q0 + q1) / 2, y - 0.62), "佇列", lab, (0.3, 0.15)),
              node((q0 + 0.25, y + 0.55), "頭", "font=\\footnotesize,text=gray!40!black", (0.15, 0.15)),
              node((q1 - 0.25, y + 0.55), "尾", "font=\\footnotesize,text=gray!40!black", (0.15, 0.15))]
    lines += emit(prims)
    lines.append(rf"\draw[gray!60!black,line width=1.2pt] {pt(q0, y + qh)} -- {pt(q1, y + qh)};")
    lines.append(rf"\draw[gray!60!black,line width=1.2pt] {pt(q0, y - qh)} -- {pt(q1, y - qh)};")
    lines.append(rf"\draw[{arrow}] {pt(ox + 3.95, y)} -- {pt(q1 + 0.05, y)};")
    lines.append(rf"\draw[{arrow}] {pt(q0 - 0.05, y)} -- {pt(ox + 1.55, y)};")
    by = y + 1.15
    # 插隊線：從輸入的第一格上方出發，越過佇列，落到輸出格上方
    lines.append(rf"\draw[cB,dashed,line width=0.9pt,-{{Stealth[length=2.2mm]}}] {pt(ox + 4.25, y + 0.33)} -- "
                 rf"{pt(ox + 4.25, by)} -- {pt(ox + 1.2, by)} -- {pt(ox + 1.2, y + 0.33)};")
    lines.append(rf"\node[font=\small,text=cB!80!black] at {pt((q0 + q1) / 2, by + 0.25)} {{插隊線}};")
    lines.append(rf"\node[font=\small] at {pt(ox + 2.75, -1.25)} {{(b) 佇列＋插隊線排 $321$}};")
    return picture(lines)


def fig_m10_plots() -> str:
    """排列的點圖：模式 231、41532 含有 231（4,5,3）、52143 避開 231。"""
    u = 0.36
    lines = []
    panels = [
        (PAT, (0, 1, 2), 0.0, r"模式 $\pi=231$"),
        (W, contains_pattern(W, PAT), 2.95, r"$w=41532$：含有 $231$"),
        (AV, (), 6.8, r"$w=52143$：避開 $231$"),
    ]
    for w, occ, x0, cap in panels:
        lines += emit(perm_plot_prims(w, u, occ), x0, 0.0)
        cx = x0 + (len(w) + 1) / 2 * u
        lines.append(rf"\node[font=\small] at {pt(cx, -0.55)} {{{cap}}};")
    return picture(lines)


def fig_m10_grid() -> str:
    """n = 3 與 n = 4 的全部排列（字典序）：藍底 = 避開 231；灰字 = 含有 231，紅字是找到的第一個 231。"""
    dx, x0 = 1.3, 1.7
    lines = []

    def item(p, x, y):
        occ = contains_pattern(p, PAT)
        if occ is None:
            lines.append(rf"\fill[cA!12,rounded corners=2pt] {pt(x - 0.48, y - 0.19)} rectangle {pt(x + 0.48, y + 0.19)};")
            body = rf"{{\color{{cA}}\mathbf{{{word(p)}}}}}"
        else:
            body = "".join(rf"{{\color{{{'cBad' if i in occ else 'gray'}}}{d}}}" for i, d in enumerate(p))
        lines.append(rf"\node[font=\small] at {pt(x, y)} {{${body}$}};")

    p3, p4 = list(permutations((1, 2, 3))), list(permutations((1, 2, 3, 4)))
    for k, p in enumerate(p3):
        item(p, x0 + k * dx, 0.0)
    ys4 = [-0.68, -1.18, -1.68, -2.18]
    for k, p in enumerate(p4):
        item(p, x0 + (k % 6) * dx, ys4[k // 6])
    right = x0 + 5 * dx + 0.65
    lines.append(rf"\draw[gray!40,line width=0.4pt] {pt(0, -0.34)} -- {pt(right + 1.55, -0.34)};")
    lines.append(rf"\node[font=\small,anchor=west] at {pt(0, 0)} {{$n=3$}};")
    lines.append(rf"\node[font=\small,anchor=west] at {pt(0, sum(ys4) / 4)} {{$n=4$}};")
    lines.append(rf"\node[font=\small,anchor=west,text=cA] at {pt(right, 0)} "
                 rf"{{{len(avoiders(3, PAT))} 個避開}};")
    lines.append(rf"\node[font=\small,anchor=west,text=cA] at {pt(right, sum(ys4) / 4)} "
                 rf"{{{len(avoiders(4, PAT))} 個避開}};")
    return picture(lines)


def fig_m11_young_syt() -> str:
    """
    兩排、左右兩欄對齊（中間一條分隔線）：
      上排：λ = (5,3,3,2,1) 的 Young 圖 | 5 的 7 個整數分割
      下排：一個 SYT 與一個反例      | 形狀 (3,2) 的全部 5 個 SYT
    """
    lines = []
    u, s, su, ss = 0.36, 0.30, 0.5, 0.42          # 大 Young 圖、小 Young 圖、SYT 例子、5 個 SYT 的格子邊長
    left_w = 6 * su + 0.8                          # 下排左欄：兩個 (3,2) 表
    sep = left_w + 0.45
    x_right = sep + 0.5

    # ---- 上排
    y1_lab = -5 * u - 0.35
    bx = (left_w - 5 * u) / 2
    lines += emit(young_prims(YOUNG_EX, u), bx, 0.0)
    for i, r in enumerate(YOUNG_EX):
        lines.append(rf"\node[font=\footnotesize,text=gray!40!black] at {pt(bx + r * u + 0.2, -i * u - u / 2)} {{{r}}};")
    lines.append(rf"\node[font=\small] at {pt(left_w / 2, y1_lab)} {{$\lambda=(5,3,3,2,1)\vdash 14$}};")
    items, x = [], 0.0
    for p in integer_partitions(5):
        lab = "(" + ",".join(map(str, p)) + ")"
        lab_w = 0.19 * sum(c.isdigit() for c in lab) + 0.1 * lab.count(",") + 0.3     # \small 的約略寬度
        w = max(p[0] * s, lab_w)
        items.append((p, lab, x, w))
        x += w + 0.42
    row1_w = x - 0.42
    syt_w = 5 * 3 * ss + 4 * 0.5
    right_w = max(row1_w, syt_w)
    off = x_right + (right_w - row1_w) / 2
    for p, lab, x, w in items:
        lines += emit(young_prims(p, s, lw=0.5), off + x + (w - p[0] * s) / 2, 0.0)
        lines.append(rf"\node[font=\small] at {pt(off + x + w / 2, y1_lab)} {{${lab}$}};")

    # ---- 下排
    top2 = y1_lab - 0.55
    y2_lab = top2 - 2 * su - 0.33
    lines += emit(young_prims(SHAPE, su, entries=GOOD_T, fill="cA!10"), 0.0, top2)
    lines.append(rf"\node[font=\small,text=cA] at {pt(1.5 * su, y2_lab)} {{是 SYT}};")
    bx = 3 * su + 0.8
    red = {(0, 1): "cBad!25", (1, 1): "cBad!25"}
    lines += emit(young_prims(SHAPE, su, entries=BAD_T, fill="gray!6", cell_fill=red), bx, top2)
    lines.append(rf"\node[font=\small,text=cBad] at {pt(bx + 1.5 * su, y2_lab)} {{第 2 行 $4>3$}};")
    x = x_right + (right_w - syt_w) / 2
    for T in syt(SHAPE):
        lines += emit(young_prims(SHAPE, ss, entries=T, fill="cA!14" if T == GOOD_T else "cA!5"), x, top2)
        x += 3 * ss + 0.5
    lines.append(rf"\node[font=\small] at {pt(x_right + right_w / 2, y2_lab)} "
                 rf"{{形狀 $(3,2)$ 的全部 SYT：$f^{{(3,2)}}=5$}};")
    lines.append(rf"\draw[gray!35,line width=0.4pt] {pt(sep, 0.1)} -- {pt(sep, y2_lab - 0.15)};")
    return picture(lines)


def fig_m11_warn() -> str:
    """整數分割 5 = 3 + 2 對照 Chu 的集合分割 {1,2,5},{3,4}。"""
    lines = []
    u = 0.36
    lines += emit(young_prims(SHAPE, u), 0.0, 0.36)
    lines.append(rf"\node[font=\small] at {pt(1.5 * u, -1.05)} {{$5=3+2$}};")
    lines.append(rf"\node[font=\Large,text=cBad] at {pt(1.75, 0.0)} {{$\neq$}};")
    cx, r = 3.05, 0.55
    lines.append(rf"\node[font=\small] at {pt(cx, -1.05)} {{$\{{1,2,5\}},\{{3,4\}}$}};")
    P = [circle_point(i, 5, r) for i in range(5)]
    tri = [P[i] for i in SET_BLOCKS[0]]
    a, b = (P[i] for i in SET_BLOCKS[1])
    lines.append(rf"\draw[gray!65,line width=0.5pt] {pt(cx, 0)} circle ({r});")
    lines.append(r"\draw[tri] " + " -- ".join(pt(x + cx, y) for x, y in tri) + " -- cycle;")
    lines.append(rf"\draw[chord] {pt(a[0] + cx, a[1])} -- {pt(b[0] + cx, b[1])};")
    for i, (x, y) in enumerate(P):
        lines.append(rf"\fill {pt(x + cx, y)} circle (0.04);")
        lx, ly = circle_point(i, 5, r + 0.24)
        lines.append(rf"\node[font=\scriptsize] at {pt(lx + cx, ly)} {{{i + 1}}};")
    return picture(lines)


FIGURES = [
    ("FigMnineStuck", fig_m09_stuck),
    ("FigMtenPlots", fig_m10_plots),
    ("FigMtenGrid", fig_m10_grid),
    ("FigMelevenYoungSYT", fig_m11_young_syt),
    ("FigMelevenWarn", fig_m11_warn),
]


def main():
    check_numbers()
    parts = [
        "% figs_part3.tex —— 由 mit/make_figs_part3.py 產生，請勿手動修改。\n"
        "% 重新產生：python mit/make_figs_part3.py\n"
    ]
    for name, func in FIGURES:
        body = func()
        assert "\n\n" not in body
        parts.append(f"\\newcommand{{\\{name}}}{{%\n{body}}}\n")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"已寫出 {OUT.name}：{len(FIGURES)} 張圖")


if __name__ == "__main__":
    main()
