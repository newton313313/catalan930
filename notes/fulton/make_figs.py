r"""
make_figs.py —— 講義附錄 B（Fulton《Young Tableaux》第 2–4 章，動畫 F09–F19）的圖與表

在 notes/ 或 notes/fulton/ 裡執行：
    python fulton/make_figs.py
會先檢查 fulton/part1.tex、part2.tex 寫到的每一個數字（check_numbers），再寫出 fulton/figs.tex
（part1.tex 第一行 \input{fulton/figs}）。Young 表用 ytableau 套件畫，矩陣球用 TikZ。

數學資料一律由 codes/utils/tableaux.py 算出（第 7 節；格子 0 起算，講義顯示時 +1）。例子與動畫 F09–F19 相同。
顏色：被換的三個字母 = cB（橘）、K′ 規則 = cLeft、K″ 規則 = cRight、擠壓路徑 = yellow、新格子 = cC（綠）。
"""
from __future__ import annotations

import sys
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent            # notes/fulton
sys.path.insert(0, str(HERE.parent.parent / "codes"))

from utils.counting import hook_product, syt_count  # noqa: E402
from utils.tableaux import (  # noqa: E402
    CH2_SLIDE_AFTER, CH2_SLIDE_BEFORE, CH2_SLIDE_CHAIN, CH2_WORD, CH3_TABLEAU, CH3_WORD, CH3_WORD2, CH4_ARRAY,
    CH4_HOOK_SHAPE, CH4_MATRIX, CH4_P, CH4_Q, CH4_WORD, FULTON_INSERT_T, FULTON_PRODUCT_U, FULTON_SKEW,
    array_to_matrix, ball_numbering, bump_steps, column_word, complete_h, conjugate, count_involutions,
    derived_matrix, dominates, elementary_e, insert_word, insertion_knuth_chain, inverse_rsk, knuth_class,
    knuth_moves, kostka, kostka_matrix, lex_greater, matrix_ball, matrix_to_array, max_increasing,
    partitions, pieri_shapes, poly_mul, poly_sum, product, rectify, remove_largest, row_insert, rsk, rsk_matrix,
    rsk_steps, schur_poly, shape, skew_from_word, ssyt, standard_tableaux, star, tableau_from_greene,
    tableau_word, transpose_matrix, word_runs, word_to_tableau, hook_content_count, young_boxes,
)

OUT = HERE / "figs.tex"
T0, U0 = FULTON_INSERT_T, FULTON_PRODUCT_U
TU = ((1, 1, 2, 2, 3), (2, 2, 3, 5), (3, 4, 5), (4, 6, 6), (5,))
T_INS = ((1, 2, 2, 2), (2, 3, 3, 5), (4, 4, 5), (5, 6, 6))
RECT_S = ((2, 2, 2, 4, 6), (3, 4, 6), (5, 5))
ES_WORD = (4, 9, 2, 10, 6, 1, 8, 3, 7, 5)
ES_P = ((1, 3, 5), (2, 6, 7), (4, 8, 10), (9,))
INV_W, INV_WI = (3, 1, 4, 2), (2, 4, 1, 3)
SYM = ((2, 1), (1, 1))
SEQ_COLORS = ["cLeft", "cB", "cRight"]


# =============================================================================
# 數字檢查（講義裡寫到的每一個數）
# =============================================================================
def check_numbers():
    # B.1 回顧
    T1, route, new = row_insert(T0, 2)
    assert T1 == T_INS and new == (3, 2) and [b for _, _, b in bump_steps(T0, 2)] == [3, 5, 6, None]
    assert tableau_word(T0) == CH2_WORD and product(T0, U0) == TU == rectify(star(T0, U0))
    # B.2 字與 Knuth 變換
    assert word_runs(CH2_WORD) == [(5, 6), (4, 4, 6), (2, 3, 5, 5), (1, 2, 2, 3)] and word_to_tableau(CH2_WORD) == T0
    assert word_to_tableau((3, 4, 1, 4)) is None
    chain = insertion_knuth_chain(T0, 2)
    assert [r for _, r, _ in chain] == ["K''"] * 3 + ["K'"] + ["K''"] * 4
    assert chain[-1][2] == tableau_word(T_INS)
    assert knuth_class((1, 3, 2)) == {(1, 3, 2), (3, 1, 2)} and len(standard_tableaux((2, 1))) == 2
    for lam in [(2, 2), (3, 1), (2, 1, 1)]:
        T = standard_tableaux(lam)[0]
        assert len(knuth_class(tableau_word(T))) == len(standard_tableaux(lam))
    # B.3 滑動與主定理
    assert CH2_SLIDE_CHAIN[0] == (2, 3, 5, 1, 4) and CH2_SLIDE_CHAIN[-1] == (2, 5, 1, 3, 4) and len(CH2_SLIDE_CHAIN) == 5
    assert tableau_word(CH2_SLIDE_BEFORE) == CH2_SLIDE_CHAIN[0] and tableau_word(CH2_SLIDE_AFTER) == CH2_SLIDE_CHAIN[-1]
    assert insert_word(CH3_WORD) == CH3_TABLEAU and tableau_word(CH3_TABLEAU) == CH3_WORD2
    assert rectify(FULTON_SKEW) == RECT_S == insert_word(tableau_word(FULTON_SKEW))
    assert tableau_word(FULTON_SKEW) == (5, 5, 2, 3, 6, 2, 4, 4, 6, 2)
    assert insert_word(tableau_word(T0) + tableau_word(U0)) == TU
    # B.4 Pieri
    assert pieri_shapes((2, 1), 2) == [(4, 1), (3, 2), (3, 1, 1), (2, 2, 1)]
    assert pieri_shapes((2, 1), 2, vertical=True) == [(3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1)]
    e = (2, 2, 1)
    lhs_h = poly_mul(schur_poly((2, 1), 3), complete_h(2, 3))
    lhs_e = poly_mul(schur_poly((2, 1), 3), elementary_e(2, 3))
    assert lhs_h[e] == 6 and [schur_poly(mu, 3).get(e, 0) for mu in pieri_shapes((2, 1), 2)] == [2, 2, 1, 1]
    assert lhs_e[e] == 4 and [schur_poly(mu, 3).get(e, 0) for mu in pieri_shapes((2, 1), 2, True)] == [2, 1, 1, 0]
    assert len(ssyt((2, 1), 3)) == 8 and len(ssyt((2,), 3)) == 6
    assert [len(ssyt(mu, 3)) for mu in pieri_shapes((2, 1), 2)] == [24, 15, 6, 3] and 8 * 6 == 48 == 24 + 15 + 6 + 3
    # B.5 Kostka
    assert ssyt((3, 2), content=(2, 2, 1)) == [((1, 1, 2), (2, 3)), ((1, 1, 3), (2, 2))] and kostka((3, 2), (2, 2, 1)) == 2
    h = poly_mul(poly_mul(complete_h(2, 4), complete_h(1, 4)), complete_h(1, 4))
    assert [kostka(lam, (2, 1, 1)) for lam in partitions(4)] == [1, 2, 1, 1, 0]
    assert h == poly_sum(f for lam in partitions(4) for f in [schur_poly(lam, 4)] * kostka(lam, (2, 1, 1)))
    parts, K = kostka_matrix(4)
    assert parts == [(1, 1, 1, 1), (2, 1, 1), (2, 2), (3, 1), (4,)]
    assert K == [[1, 0, 0, 0, 0], [3, 1, 0, 0, 0], [2, 1, 1, 0, 0], [3, 2, 1, 1, 0], [1, 1, 1, 1, 1]]
    assert dominates((3, 1), (2, 2)) and lex_greater((4, 1, 1), (3, 3)) and not dominates((4, 1, 1), (3, 3))
    assert kostka((4, 1, 1), (3, 3)) == 0 and not dominates((2, 2, 2), (3, 1, 1, 1)) and not dominates((3, 1, 1, 1), (2, 2, 2))
    assert kostka((3, 2), (2, 2, 1)) == kostka((3, 2), (1, 2, 2)) == kostka((3, 2), (2, 1, 2)) == 2
    # B.6 行字
    assert column_word(T0) == (5, 4, 2, 1, 6, 4, 3, 2, 6, 5, 2, 5, 3) and insert_word(column_word(T0)) == T0
    left, right = cut(T0, 2)
    assert left == ((1, 2), (2, 3), (4, 4), (5, 6)) and right == ((2, 3), (5, 5), (6,))
    assert insert_word(tableau_word(left) + tableau_word(right)) == T0 == rectify(star(left, right))
    # B.7 遞增子序列
    assert [max_increasing(CH3_WORD, k)[0] for k in (1, 2, 3, 4)] == [6, 9, 12, 12]
    assert [max_increasing(CH3_WORD2, k)[0] for k in (1, 2, 3)] == [6, 9, 12] and shape(CH3_TABLEAU) == (6, 3, 3)
    assert not three_six_three_three()
    # B.8 唯一性
    assert remove_largest((1, 3, 4, 2, 3, 1, 3), 3) == (1, 3, 2, 1) and tableau_from_greene(CH3_WORD) == CH3_TABLEAU
    assert insert_word(ES_WORD) == ES_P and max_increasing(ES_WORD)[0] == 3 and max_increasing(ES_WORD, decreasing=True)[0] == 4
    # B.9 Robinson–Schensted
    P, Q = rsk(CH4_WORD)
    assert P == ((1, 1, 3, 5), (2, 3), (4, 4), (5, 7), (8,)) and Q == ((1, 3, 6, 8), (2, 5), (4, 9), (7, 10), (11,))
    assert inverse_rsk(P, Q) == (tuple(range(1, 12)), CH4_WORD)
    assert [len(standard_tableaux(l)) ** 2 for l in partitions(3)] == [1, 4, 1]
    assert [len(standard_tableaux(l)) ** 2 for l in partitions(4)] == [1, 9, 4, 9, 1] and factorial(4) == 24
    # B.10 R-S-K
    assert matrix_to_array(CH4_MATRIX) == CH4_ARRAY and rsk(*CH4_ARRAY) == (CH4_P, CH4_Q)
    assert [sum(r) for r in CH4_MATRIX] == [3, 2, 4] and [sum(c) for c in zip(*CH4_MATRIX)] == [5, 4]
    assert rsk_matrix(transpose_matrix(CH4_MATRIX)) == (CH4_Q, CH4_P)
    assert rsk(INV_W) == (((1, 2), (3, 4)), ((1, 3), (2, 4))) and rsk(INV_WI) == (((1, 3), (2, 4)), ((1, 2), (3, 4)))
    assert count_involutions(4) == 10 == sum(len(standard_tableaux(l)) for l in partitions(4))
    # B.11 矩陣球
    Pb, Qb, st = matrix_ball(CH4_MATRIX)
    assert st[0]["balls"] == {(0, 0): [1], (0, 1): [2, 3], (1, 0): [2], (1, 1): [4], (2, 0): [3, 4, 5], (2, 1): [6]}
    assert st[1]["A"] == ((0, 0), (0, 1), (0, 2)) and st[1]["balls"] == {(1, 1): [1], (2, 1): [2, 3]}
    assert rsk_matrix(SYM) == (((1, 1, 1, 2), (2,)),) * 2 and derived_matrix(SYM) == ((0, 0), (0, 1))
    # B.12 應用
    assert kostka((6, 2), (5, 3)) == kostka((6, 2), (3, 5)) == 1
    assert sum(len(ssyt(l, 2)) ** 2 for l in partitions(3)) == 20 == comb(6, 3)
    assert [len(ssyt(l, 2)) ** 2 for l in partitions(3)] == [16, 4, 0]
    assert sum(len(ssyt(l, 2)) * len(standard_tableaux(l)) for l in partitions(3)) == 8 == 2 ** 3
    assert hook_content_count(CH4_HOOK_SHAPE, 5) == 3360 == len(ssyt(CH4_HOOK_SHAPE, 5))
    assert factorial(19) // hook_product(CH4_HOOK_SHAPE) == 6651216 == syt_count(CH4_HOOK_SHAPE)
    from itertools import permutations
    twos = sorted("".join(map(str, w)) for w in permutations(range(1, 5))
                  if max_increasing(w)[0] == 2 and max_increasing(w, decreasing=True)[0] == 2)
    assert twos == ["2143", "2413", "3142", "3412"] and len(standard_tableaux((2, 2))) ** 2 == 4


def cut(T, c):
    return tuple(r[:c] for r in T if r[:c]), tuple(r[c:] for r in T if r[c:])


def three_six_three_three():
    """是否有三條不相交的遞增子序列，長度 6、3、3（書上說沒有）。暴力：先取一條長 6 的，剩下的要 L(·,2) = 6 且分成 3+3。"""
    from itertools import combinations
    w = CH3_WORD
    for six in combinations(range(12), 6):
        if all(w[a] <= w[b] for a, b in zip(six, six[1:])):
            rest = [i for i in range(12) if i not in six]
            for three in combinations(rest, 3):
                other = [i for i in rest if i not in three]
                if all(w[a] <= w[b] for a, b in zip(three, three[1:])) and \
                        all(w[a] <= w[b] for a, b in zip(other, other[1:])):
                    return True
    return False


# =============================================================================
# 畫圖小工具
# =============================================================================
def yt(T, fills=None, colors=None) -> str:
    """ytableau：T 的每列可以有 None（\\none，空白不畫）或 ""（空格子）。fills／colors = {(i,j): 顏色}。"""
    rows = []
    for i, row in enumerate(T):
        cells = []
        for j, v in enumerate(row):
            if v is None:
                cells.append(r"\none")
                continue
            s = str(v) if v != "" else "{}"                 # 空格子要寫成 {}，否則整列會消失
            if colors and (i, j) in colors:
                s = rf"\textcolor{{{colors[(i, j)]}}}{{{s}}}"
            if fills and (i, j) in fills:
                s = rf"*({fills[(i, j)]}) {s}"
            cells.append(s)
        rows.append(" & ".join(cells))
    return r"\begin{ytableau}" + r" \\ ".join(rows) + r"\end{ytableau}"


def blank(lam, fills=None) -> str:
    return yt(tuple(("",) * r for r in lam), fills)


def wtex(w, colors=None, sep=r"\,") -> str:
    out = []
    for k, a in enumerate(w):
        s = str(a)
        if colors and k in colors:
            s = rf"\textcolor{{{colors[k]}}}{{\mathbf{{{s}}}}}"
        out.append(s)
    return sep.join(out)


def tstr(lam) -> str:
    return "(" + ",".join(map(str, lam)) + ")"


# =============================================================================
# 各圖
# =============================================================================
def fig_recap() -> str:
    T1, route, new = row_insert(T0, 2)
    before = yt(T0, {b: "yellow!45" for b in route[:-1]})
    after = yt(T1, {**{b: "yellow!45" for b in route[:-1]}, new: "cC!35"})
    return (rf"$T={before}\quad\xrightarrow{{\ \leftarrow 2\ }}\quad T\leftarrow 2={after}$"
            rf"\qquad $U={yt(U0)}$\qquad $T\cdot U={yt(TU)}$")


def fig_runs() -> str:
    S = skew_from_word(CH3_WORD)
    return r"{\ytableausetup{smalltableaux}" + rf"${yt(S)}$" + "}"


def fig_knuth_rules() -> str:
    a = rf"{yt((('y', 'z'),))}\leftarrow x\ =\ {yt((('x', 'z'), ('y',)))}"
    b = rf"{yt((('x', 'z'),))}\leftarrow y\ =\ {yt((('x', 'y'), ('z',)))}"
    return (r"\begin{tabular}{@{}c@{\qquad\qquad}c@{}}"
            rf"$\textcolor{{cLeft}}{{K'}}:\ y\,z\,x\mapsto y\,x\,z\quad(x<y\le z)$ & "
            rf"$\textcolor{{cRight}}{{K''}}:\ x\,z\,y\mapsto z\,x\,y\quad(x\le y<z)$\\[6pt]"
            rf"${a}$ & ${b}$\\[4pt]"
            r"字：$y\,z\,x\ \to\ y\,x\,z$ & 字：$x\,z\,y\ \to\ z\,x\,y$"
            r"\end{tabular}")


def fig_chain() -> str:
    chain = insertion_knuth_chain(T0, 2)
    rows = [rf"0 & ${wtex(tableau_word(T0) + (2,), {13: 'cB'})}$ & $w(T)\cdot 2$\\"]
    for k, (i, rule, w) in enumerate(chain, 1):
        col = "cLeft" if rule == "K'" else "cRight"
        name = "K'" if rule == "K'" else "K''"
        rows.append(rf"{k} & ${wtex(w, {i: 'cB', i + 1: 'cB', i + 2: 'cB'})}$ & $\textcolor{{{col}}}{{{name}}}$\\")
    return (r"\begin{tabular}{@{}rll@{}}\toprule 步 & 字 & 規則\\\midrule" + "\n".join(rows)
            + r"\bottomrule\end{tabular}")


def fig_slide() -> str:
    before = yt(tuple(tuple("" if v is None else v for v in r) for r in CH2_SLIDE_BEFORE), {(0, 1): "yellow!40"})
    after = yt(tuple(tuple("" if v is None else v for v in r) for r in CH2_SLIDE_AFTER), {(1, 1): "yellow!40"})
    steps = []
    for a, b in zip(CH2_SLIDE_CHAIN, CH2_SLIDE_CHAIN[1:]):
        i = next(i for i, _, v in knuth_moves(a) if v == b)
        steps.append(wtex(b, {i: "cB", i + 1: "cB", i + 2: "cB"}))
    chain = r"\equiv ".join([wtex(CH2_SLIDE_CHAIN[0])] + steps)
    return rf"${before}\ \longrightarrow\ {after}$\qquad ${chain}$"


def fig_pieri() -> str:
    lam = (2, 1)
    old = set(young_boxes(lam))
    hs = [blank(mu, {b: "cLeft!40" for b in young_boxes(mu) if b not in old}) for mu in pieri_shapes(lam, 2)]
    vs = [blank(mu, {b: "cRight!35" for b in young_boxes(mu) if b not in old}) for mu in pieri_shapes(lam, 2, True)]
    return (r"\begin{tabular}{@{}r@{\ }l@{}}"
            rf"$S_{{(2,1)}}\cdot S_{{(2)}}=$ & ${'+'.join(hs)}$\\[10pt]"
            rf"$S_{{(2,1)}}\cdot S_{{(1,1)}}=$ & ${'+'.join(vs)}$"
            r"\end{tabular}")


VALUE_COLORS = {1: "cLeft!35", 2: "cB!40", 3: "cRight!30"}


def fig_kostka_tabs() -> str:
    out = []
    for T in ssyt((3, 2), content=(2, 2, 1)):
        fills = {(i, j): VALUE_COLORS[v] for i, r in enumerate(T) for j, v in enumerate(r)}
        chain = []
        for k in (1, 2, 3):
            sub = tuple(tuple(v for v in r if v <= k) for r in T)
            sub = tuple(r for r in sub if r)
            chain.append(tstr(shape(sub)))
        out.append(rf"${yt(T, fills)}$\ \ {{\small $\varnothing\subset " + r"\subset ".join(chain) + "$}")
    return r"\qquad\qquad ".join(out)


def fig_kostka_matrix() -> str:
    parts, K = kostka_matrix(4)
    head = " & ".join(f"${tstr(m)}$" for m in parts)
    rows = []
    for lam, row in zip(parts, K):
        cells = [(rf"\textbf{{{v}}}" if a == b else (str(v) if v else r"\textcolor{gray}{0}"))
                 for b, v in enumerate(row) for a in [parts.index(lam)]]
        rows.append(rf"${tstr(lam)}$ & " + " & ".join(cells) + r"\\")
    return (r"\begin{tabular}{@{}l|ccccc@{}}$\lambda\backslash\mu$ & " + head + r"\\\hline" + "\n".join(rows)
            + r"\end{tabular}")


def fig_cut() -> str:
    left, right = cut(T0, 2)
    lw, rw = len(left[0]), len(right)
    S = star(left, right)
    show = tuple(tuple("" if v is None else v for v in r) for r in S)
    mu = {(i, j): "gray!25" for i, r in enumerate(S) for j, v in enumerate(r) if v is None}
    fills_t = {(i, j): ("cLeft!30" if j < 2 else "cRight!25") for i, r in enumerate(T0) for j in range(len(r))}
    return (rf"$T={yt(T0, fills_t)}$\qquad $T'={yt(left)}$\quad $T''={yt(right)}$\qquad"
            rf"$T'*T''={yt(show, mu)}$")


def fig_increasing() -> str:
    lines = []
    for k in (1, 2, 3):
        L, seqs = max_increasing(CH3_WORD, k)
        cols = {p: SEQ_COLORS[t] for t, s in enumerate(seqs) for p in s}
        lens = "+".join(str(len(s)) for s in seqs)
        word = wtex(CH3_WORD, cols, sep=r"\ ")
        lines.append(rf"$k={k}$: & ${word}$ & $L(w,{k})={L}" + (f"={lens}$" if k > 1 else "$") + r"\\")
    fills = {(i, j): SEQ_COLORS[i].replace("cB", "cB") + "!30" for i, r in enumerate(CH3_TABLEAU) for j in range(len(r))}
    return (r"\begin{tabular}{@{}lll@{}}" + "\n".join(lines) + r"\end{tabular}\qquad"
            rf"$P(w)={yt(CH3_TABLEAU, fills)}$")


def fig_rebuild() -> str:
    w = CH3_WORD
    rows = []
    for p in range(12):
        wp, wq = remove_largest(w, p), remove_largest(w, p + 1)
        lam, lam1 = shape(insert_word(wp)), shape(insert_word(wq))
        i = next(i for i in range(len(lam)) if i >= len(lam1) or lam[i] > lam1[i])
        L = [max_increasing(wp, k)[0] for k in (1, 2, 3)]
        gone = set(range(12)) - set(keep_positions(w, p))
        shown = wtex(w, {g: "gray!45" for g in gone}, sep=r"\,")
        rows.append(rf"{p} & ${shown}$ & {L[0]}, {L[1]}, {L[2]} & ${tstr(lam)}$ & ${max(wp)}\to$ 第 {i + 1} 列\\")
    return (r"{\small\begin{tabular}{@{}rlccl@{}}\toprule $p$ & $w_p$（灰色是已去掉的） & $L(w_p,1..3)$ & 形狀 & 最大字母放哪"
            r"\\\midrule" + "\n".join(rows) + r"\bottomrule\end{tabular}}")


def keep_positions(w, p):
    order = sorted(range(len(w)), key=lambda i: (w[i], i))
    drop = set(order[len(w) - p:]) if p else set()
    return [i for i in range(len(w)) if i not in drop]


def fig_rs() -> str:
    steps = rsk_steps(CH4_WORD)
    items = []
    for k in (1, 2, 3, 4):
        _, v, P, Q, _ = steps[k - 1]
        items.append(rf"$k={k}$：$x_{k}={v}$\ \ ${yt(P)}\ \ {yt(Q)}$")
    P, Q = steps[-1][2], steps[-1][3]
    return (r"{\ytableausetup{smalltableaux}" + r"\quad ".join(items) + r"}\\[8pt]"
            + rf"$P={yt(P)}\qquad Q={yt(Q)}$")


def fig_array() -> str:
    top, bot = CH4_ARRAY
    arr = (r"\begin{pmatrix}" + " & ".join(map(str, top)) + r"\\" + " & ".join(map(str, bot)) + r"\end{pmatrix}")
    mat = r"\begin{pmatrix}" + r"\\".join(" & ".join(map(str, r)) for r in CH4_MATRIX) + r"\end{pmatrix}"
    return rf"$\omega={arr}\qquad A={mat}\qquad P={yt(CH4_P)}\quad Q={yt(CH4_Q)}$"


def balls_tikz(A, numbering, s=1.0) -> list:
    m, n = len(A), len(A[0])
    lines = []
    for i in range(m + 1):
        lines.append(rf"\draw[gray!60] (0,{-i * s:.2f}) -- ({n * s:.2f},{-i * s:.2f});")
    for j in range(n + 1):
        lines.append(rf"\draw[gray!60] ({j * s:.2f},0) -- ({j * s:.2f},{-m * s:.2f});")
    for i in range(m):
        lines.append(rf"\node[font=\scriptsize,gray] at ({-0.25:.2f},{-(i + 0.5) * s:.2f}) {{{i + 1}}};")
    for j in range(n):
        lines.append(rf"\node[font=\scriptsize,gray] at ({(j + 0.5) * s:.2f},{0.22:.2f}) {{{j + 1}}};")
    for (i, j), nums in numbering.items():
        a = len(nums)
        for t, x in enumerate(nums):
            off = (t - (a - 1) / 2) * 0.25
            cx, cy = (j + 0.5) * s + off, -(i + 0.5) * s - off
            lines.append(rf"\node[circle,draw=cA,fill=cA!15,inner sep=0pt,minimum size=9pt,font=\tiny] "
                         rf"at ({cx:.2f},{cy:.2f}) {{{x}}};")
    return lines


def fig_balls() -> str:
    _, _, st = matrix_ball(CH4_MATRIX)
    pics = []
    for k, stage in enumerate(st):
        name = "A" if k == 0 else r"A^\flat"
        body = "\n".join(balls_tikz(stage["A"], stage["balls"]))
        pics.append(rf"${name}$:\ \begin{{tikzpicture}}[baseline=(current bounding box.center)]" + "\n" + body
                    + r"\end{tikzpicture}\ \ {\small\begin{tabular}{@{}l@{}}"
                    + rf"$P$ 第 {k + 1} 列：${wtex(stage['P_row'], sep=',')}$\\$Q$ 第 {k + 1} 列：${wtex(stage['Q_row'], sep=',')}$"
                    + r"\end{tabular}}")
    return r"\qquad ".join(pics)


def fig_hook() -> str:
    lam = CH4_HOOK_SHAPE
    lt = conjugate(lam)
    hooks = tuple(tuple((lam[i] - j) + (lt[j] - i) - 1 for j in range(lam[i])) for i in range(len(lam)))
    cont = tuple(tuple(5 + j - i for j in range(lam[i])) for i in range(len(lam)))
    diag = {(i, i): "cB!35" for i in range(min(len(lam), lam[0]))}
    return rf"$h(i,j)={yt(hooks)}\qquad 5+j-i={yt(cont, diag)}$"


# =============================================================================
# 第 5–6 章（part3.tex、part4.tex）
# =============================================================================
V1, V2 = ((1, 2, 3), (4, 5), (6,)), ((1, 1, 2), (2, 3), (3,))
U0_LR = ((1, 1), (2,))
W_RL = (1, 1, 2, 3, 1, 2, 1)


def check_numbers_ch56():
    from utils.tableaux import (alternant, character_table, e_lambda, h_lambda, is_reverse_lattice, jacobi_trudi,
                                lattice_tableau, lr_tableaux, monomial_sym, omega, p_lambda, poly_scale,
                                principal_specialization, rectifying_skews, remmel_whitney, schur_expand,
                                skew_decomposition, skew_tableaux, z_lambda, CH5_DECOMP, CH5_LAM, CH5_NU,
                                CH5_RL_BAD, CH5_RL_GOOD, CH5_S21_SQUARED, CH5_ZERO, factorizations, lr_coefficient,
                                lr_product)
    # 5.1–5.2
    assert factorizations(V1, (2, 1), (2, 1)) == [(((1, 4), (6,)), ((2, 3), (5,))), (((1, 6), (4,)), ((2, 3), (5,)))]
    assert len(factorizations(V2, (2, 1), (2, 1))) == 2 and len(rectifying_skews((3, 2, 1), (2, 1), U0_LR)) == 2
    cands = [S for S in skew_tableaux((3, 2, 1), (2, 1), 2) if sorted(v for r in S for v in r if v) == [1, 1, 2]]
    assert len(cands) == 3 and sorted(shape(rectify(S)) for S in cands) == [(2, 1), (2, 1), (3,)]
    assert lr_coefficient((2, 1), (3, 1), (4, 2, 1)) == lr_coefficient((3, 1), (2, 1), (4, 2, 1)) == 2
    assert lr_coefficient((2, 1), (2, 1, 1), (3, 2, 1, 1)) == 2 and lr_coefficient(*CH5_ZERO) == 0
    # 5.3–5.4
    assert is_reverse_lattice(CH5_RL_GOOD) and not is_reverse_lattice(CH5_RL_BAD)
    assert not is_reverse_lattice(CH5_RL_BAD[1:]) and is_reverse_lattice(CH5_RL_BAD[2:])   # 最後 6 個字母出問題
    assert skew_decomposition(CH5_NU, CH5_LAM) == CH5_DECOMP and len(lr_tableaux(CH5_NU, CH5_LAM)) == 15
    assert lr_product((2, 1), (2, 1)) == CH5_S21_SQUARED
    assert lr_coefficient((3, 1), (2, 2, 1), (5, 3, 1)) == 1
    assert all(rectify(S) == lattice_tableau(mu) for mu in CH5_DECOMP for S in lr_tableaux(CH5_NU, CH5_LAM, mu))
    # 5.5
    assert is_reverse_lattice(W_RL) and u_of_word(W_RL) == ((1, 3, 6, 7), (2, 5), (4,))
    counts = [(len(standard_tableaux(mu)), len(remmel_whitney(CH5_NU, CH5_LAM, mu))) for mu in CH5_DECOMP]
    assert sum(a for a, _ in counts) == 189 and sum(b for _, b in counts) == 15
    assert [b for _, b in counts] == list(CH5_DECOMP.values())
    from itertools import permutations
    cat = [len({w for w in permutations((1,) * n + (2,) * n) if is_reverse_lattice(w)}) for n in range(1, 6)]
    assert cat == [1, 2, 5, 14, 42]
    # 6.1
    m = 3
    h21 = h_lambda((2, 1), m)
    assert h21 == poly_sum([monomial_sym((3,), m), poly_scale(monomial_sym((2, 1), m), 2), poly_scale(monomial_sym((1, 1, 1), m), 3)])
    assert schur_expand(h21, m) == {(3,): 1, (2, 1): 1}
    assert h21 == poly_sum([e_lambda((1, 1, 1), m), poly_scale(e_lambda((2, 1), m), -1)])
    assert poly_scale(h21, 2) == poly_sum([p_lambda((1, 1, 1), m), p_lambda((2, 1), m)])
    assert poly_scale(complete_h(3, m), 6) == poly_sum([p_lambda((1, 1, 1), m), poly_scale(p_lambda((2, 1), m), 3),
                                                        poly_scale(p_lambda((3,), m), 2)])
    assert [z_lambda(l) for l in [(1, 1, 1), (2, 1), (3,)]] == [6, 2, 3] and [6 // z_lambda(l) for l in [(1, 1, 1), (2, 1), (3,)]] == [1, 3, 2]
    # 6.2
    assert jacobi_trudi((2, 1), m) == poly_sum([poly_mul(complete_h(2, m), complete_h(1, m)), poly_scale(complete_h(3, m), -1)]) == schur_poly((2, 1), m)
    assert jacobi_trudi((3,), m, dual=True) == complete_h(3, m)
    assert poly_mul(schur_poly((2, 1), 2), alternant((1, 0), 2)) == alternant((3, 1), 2)
    assert schur_poly((2, 1), 2) == {(2, 1): 1, (1, 2): 1}
    assert principal_specialization((2, 1), 3) == {1: 1, 2: 2, 3: 2, 4: 2, 5: 1} and len(ssyt((2, 1), 3)) == 8
    # 6.3
    parts3, X3 = character_table(3)
    assert X3 == [[1, 1, 1], [-1, 0, 2], [1, -1, 1]]
    assert omega(p_lambda((2, 1), 4), 4) == poly_scale(p_lambda((2, 1), 4), -1)
    assert omega(complete_h(3, 3), 3) == elementary_e(3, 3)
    parts4, X4 = character_table(4)
    assert [row[-1] for row in X4] == [len(standard_tableaux(l)) for l in parts4] == [1, 3, 2, 3, 1]
    from itertools import permutations as _perms
    from math import prod as _prod
    P3 = [(3,), (2, 1), (1, 1, 1)]
    M = [[p_lambda(l, 3).get(tuple(mu) + (0,) * (3 - len(mu)), 0) for mu in P3] for l in P3]   # p_λ 在 m_μ 的係數
    det = sum((1 if sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3)) % 2 == 0 else -1)
              * _prod(M[i][p[i]] for i in range(3)) for p in _perms(range(3)))
    assert abs(det) == 6
    e1, e2, e3 = (elementary_e(k, 3) for k in (1, 2, 3))
    assert poly_sum([poly_mul(poly_mul(e1, e1), e1), poly_scale(poly_mul(e1, e2), -2), e3]) == complete_h(3, 3)


def u_of_word(w):
    """反格字 w → 標準表 U(w)：從右邊數第 p 個字母是 x，就把 p 放進第 x 列（書 p.68）。"""
    rows = []
    for p, x in enumerate(reversed(w), 1):
        while len(rows) < x:
            rows.append([])
        rows[x - 1].append(p)
    return tuple(map(tuple, rows))


def skew_show(S, value_colors=True):
    """斜表 → ytableau：λ 的格子灰色、數字依值上色。"""
    show = tuple(tuple("" if v is None else v for v in r) for r in S)
    fills = {(i, j): "gray!30" for i, r in enumerate(S) for j, v in enumerate(r) if v is None}
    if value_colors:
        fills.update({(i, j): VALUE_COLORS.get(v, "cC!30") for i, r in enumerate(S) for j, v in enumerate(r)
                      if v is not None})
    return yt(show, fills)


def fig_factor() -> str:
    from utils.tableaux import factorizations, skew_tableaux
    pairs_ = factorizations(V1, (2, 1), (2, 1))
    fp = [rf"${yt(T)}\cdot{yt(U)}$" for T, U in pairs_]
    cands = [S for S in skew_tableaux((3, 2, 1), (2, 1), 2) if sorted(v for r in S for v in r if v) == [1, 1, 2]]
    cs = [rf"${skew_show(S, False)}\ \to\ {yt(rectify(S))}$" + (r"\ \textcolor{cC}{\checkmark}" if rectify(S) == U0_LR
                                                                  else r"\ \textcolor{cBad}{$\times$}")
          for S in cands]
    return (r"\begin{tabular}{@{}l@{\qquad}l@{}}"
            rf"$V={yt(V1)}=$ & " + r"\quad 或\quad ".join(fp) + r"\\[10pt]"
            rf"$U_0={yt(U0_LR)}$ & " + r"\qquad ".join(cs)
            + r"\end{tabular}")


def fig_lr_all() -> str:
    from utils.tableaux import CH5_DECOMP, CH5_LAM, CH5_NU, lr_tableaux
    rows = []
    for c in (1, 2, 3):
        cells = []
        for mu, cc in CH5_DECOMP.items():
            if cc != c:
                continue
            tabs = r"\,".join(f"${skew_show(S)}$" for S in lr_tableaux(CH5_NU, CH5_LAM, mu))
            cells.append(rf"\begin{{tabular}}{{c}}{tabs}\\[-1pt]{{\scriptsize ${tstr(mu)}$}}\end{{tabular}}")
        step = 2 if c == 2 else 4                              # c=2 的 8 個表分兩行，才放得下
        for k in range(0, len(cells), step):
            rows.append((rf"$c={c}$" if k == 0 else "") + " & " + r"\ \ ".join(cells[k:k + step]) + r"\\[4pt]")
    return (r"{\ytableausetup{smalltableaux}\begin{tabular}{@{}r@{\quad}l@{}}" + "\n".join(rows)
            + r"\end{tabular}}")


def fig_rw() -> str:
    from utils.tableaux import CH5_LAM, CH5_NU, reverse_numbering
    num = reverse_numbering(CH5_NU, CH5_LAM)
    lam = CH5_LAM + (0,) * (len(CH5_NU) - len(CH5_LAM))
    show = tuple(tuple(num[(i, j)] if j >= lam[i] else "" for j in range(r)) for i, r in enumerate(CH5_NU))
    fills = {(i, j): "gray!30" for i, r in enumerate(CH5_NU) for j in range(lam[i])}
    return (rf"反向編號：${yt(show, fills)}$\qquad\qquad"
            rf"$w=1\,1\,2\,3\,1\,2\,1\ \longmapsto\ U(w)={yt(u_of_word(W_RL))}$")


def fig_rw_table() -> str:
    from utils.tableaux import CH5_DECOMP, CH5_LAM, CH5_NU, remmel_whitney
    head = " & ".join(f"${tstr(mu)}$" for mu in CH5_DECOMP)
    f = " & ".join(str(len(standard_tableaux(mu))) for mu in CH5_DECOMP)
    ok = " & ".join(str(len(remmel_whitney(CH5_NU, CH5_LAM, mu))) for mu in CH5_DECOMP)
    n = len(CH5_DECOMP)
    return (rf"{{\footnotesize\setlength{{\tabcolsep}}{{4pt}}\begin{{tabular}}{{@{{}}l|{'c' * n}|c@{{}}}}$\mu$ & {head} & 合計\\\hline"
            rf"$\mu$ 上的標準表 & {f} & 189\\ 符合 (i)(ii) 的 & {ok} & 15\end{{tabular}}}}")


def fig_char4() -> str:
    from utils.tableaux import character_table, z_lambda
    parts, X = character_table(4)
    head = " & ".join(f"${tstr(m)}$" for m in parts)
    rows = [rf"$\chi^{{{tstr(l)}}}$ & " + " & ".join(str(v) for v in X[a]) + r"\\" for a, l in enumerate(parts)]
    zrow = r"\midrule $z(\mu)$ & " + " & ".join(str(z_lambda(m)) for m in parts) + r"\\"
    return (r"\begin{tabular}{@{}l|ccccc@{}}$\lambda\backslash\mu$ & " + head + r"\\\hline" + "\n".join(rows) + zrow
            + r"\end{tabular}")


FIGURES = [
    ("FulFactor", fig_factor),
    ("FulLRAll", fig_lr_all),
    ("FulRW", fig_rw),
    ("FulRWTable", fig_rw_table),
    ("FulCharFour", fig_char4),
    ("FulRecap", fig_recap),
    ("FulRuns", fig_runs),
    ("FulKnuthRules", fig_knuth_rules),
    ("FulChain", fig_chain),
    ("FulSlide", fig_slide),
    ("FulPieri", fig_pieri),
    ("FulKostkaTabs", fig_kostka_tabs),
    ("FulKostkaMatrix", fig_kostka_matrix),
    ("FulCut", fig_cut),
    ("FulIncreasing", fig_increasing),
    ("FulRebuild", fig_rebuild),
    ("FulRS", fig_rs),
    ("FulArray", fig_array),
    ("FulBalls", fig_balls),
    ("FulHook", fig_hook),
]


def check_numbers_ch7():
    """part5.tex（第 7 章）內文的每一個數字。資料在 codes/data/fulton7_math.json，由 utils/rep_data.py 重算。"""
    from collections import Counter

    from utils import rep_data as R
    from utils.tableaux import character_table, kostka, lr_coefficient
    assert R.check()
    multi = lambda lam: factorial(sum(lam)) // __import__("math").prod(factorial(x) for x in lam)
    assert multi((2, 1)) == 3 and multi((3, 2)) == 10 and multi((2, 2, 1)) == 30
    assert len(R.row_group(((1, 2, 3), (4, 5)))) == 12 and len(R.col_group(((1, 2, 3), (4, 5)))) == 4
    # v_T 與 (12)、(23)、(123) 的矩陣、特徵標
    vA = R.polytabloid(R.T_A)
    assert vA == {((1, 2), (3,)): 1, ((2, 3), (1,)): -1}
    assert R.rep_matrix21((2, 1, 3)) == [[1, 0], [-1, -1]] and R.rep_matrix21((1, 3, 2)) == [[0, 1], [1, 0]]
    assert R.rep_matrix21((2, 3, 1)) == [[0, 1], [-1, -1]]                    # (123)：1→2→3→1
    tr = lambda M: M[0][0] + M[1][1]
    assert [tr(R.rep_matrix21(p)) for p in ((1, 2, 3), (2, 1, 3), (2, 3, 1))] == [2, 0, -1]
    _, X = character_table(3)
    assert [list(reversed(r)) for r in X] == [[1, 1, 1], [2, 0, -1], [1, -1, 1]]
    assert sum(r[-1] ** 2 for r in X) == 6
    # Young's rule：M^(2,2,1)
    yr = {(5,): 1, (4, 1): 2, (3, 2): 2, (3, 1, 1): 1, (2, 2, 1): 1}
    assert all(kostka(l, (2, 2, 1)) == k for l, k in yr.items())
    assert sum(k * len(standard_tableaux(l)) for l, k in yr.items()) == 30
    # 兩變數多項式（dict：(a,b) → 係數）
    def pmul(*fs):
        out = Counter({(0, 0): 1})
        for f in fs:
            new = Counter()
            for (a, b), c in out.items():
                for (d, e), g in f.items():
                    new[(a + d, b + e)] += c * g
            out = new
        return out
    p = lambda r: {(r, 0): 1, (0, r): 1}
    assert pmul(p(2), p(2), p(1))[(3, 2)] == 2                                 # Lemma 4：M^(3,2) 在 (2,2,1) 上
    vd = {(1, 0): 1, (0, 1): -1}
    assert [pmul(vd, *map(p, mu))[(3, 1)] for mu in ((1, 1, 1), (2, 1), (3,))] == [2, 0, -1]   # Frobenius
    assert lr_coefficient((2, 1), (2, 1), (3, 2, 1)) == 2
    assert [len(standard_tableaux(l)) for l in ((3, 1), (2, 2), (2, 1, 1))] == [3, 2, 3]
    # straightening：v_T 寫成標準 v 的組合
    vec = lambda T: R.polytabloid(T)
    def lin(*terms):
        out = Counter()
        for c, T in terms:
            for k, v in vec(T).items():
                out[k] += c * v
        return {k: v for k, v in out.items() if v}
    assert vec(((2, 1), (3,))) == lin((1, R.T_A), (-1, R.T_B))
    assert vec(((1, 2, 5), (4, 3))) == lin((1, ((1, 2, 5), (3, 4))), (-1, ((1, 3, 5), (2, 4))))
    # Young 對稱化子：c_T^2 = 3 c_T，3 = 鉤長乘積 = 3!/f
    a, b, c = R.symmetrizers(R.T_A)
    assert R.gr_mul(c, c) == {k: 3 * v for k, v in c.items()} and len(c) == 4 and hook_product((2, 1)) == 3
    # 模 3：S 有平凡直線 v_a+v_b，S~ 沒有
    inv = lambda M, x: all((sum(M[i][j] * x[j] for j in range(2)) - x[i]) % 3 == 0 for i in range(2))
    assert all(inv(R.rep_matrix21(q), (1, 1)) for q in ((2, 1, 3), (1, 3, 2)))
    St = [[[1, -1], [0, -1]], [[0, 1], [1, 0]]]
    assert not any(all(inv(M, (x, y)) for M in St) for x in range(3) for y in range(3) if (x, y) != (0, 0))
    al, be = [[2, -1], [-1, 2]], [[2, 1], [1, 2]]
    assert [[sum(al[i][k] * be[k][j] for k in range(2)) for j in range(2)] for i in range(2)] == [[3, 0], [0, 3]]
    m12 = R.rep_matrix21((2, 1, 3))
    img = lambda x: [m12[0][0] * x[0] + m12[0][1] * x[1], m12[1][0] * x[0] + m12[1][1] * x[1]]
    assert img([2, -1]) == [2, -1] and img([0, 1]) == [0, -1]                  # 限制到 S_2 的特徵向量
    assert c == {(1, 2, 3): 1, (2, 1, 3): 1, (3, 2, 1): -1, (2, 3, 1): -1}
    from utils.tableaux import ssyt
    assert len(ssyt((2, 1), 3)) == 8                                             # 預告第 8 章：dim E^(2,1)，m = 3
    assert sorted(ssyt((3, 2), content=(2, 2, 1))) == [((1, 1, 2), (2, 3)), ((1, 1, 3), (2, 2))]   # 表 Young 規則
    print("第 7 章（part5.tex）的數字全部正確")


def check_numbers_ch8():
    """part6.tex（第 8 章）內文的每一個數字（與動畫 F42–F45 相同的例子）。"""
    from collections import Counter

    import sympy as sp
    from utils.tableaux import content, hook_content_count, schur_poly, ssyt
    d = hook_content_count
    # 基底 = 半標準表；d_(2,1)(m) = m(m^2-1)/3
    assert ssyt((2, 1), 2) == [((1, 1), (2,)), ((1, 2), (2,))]
    assert all(d((2, 1), m) == m * (m * m - 1) // 3 for m in range(1, 7)) and d((2, 1), 3) == 8
    assert d((3,), 3) == 10 and d((1, 1, 1), 3) == 1 and d((1, 1, 1), 2) == 0 and d((3,), 2) == 4
    # 權重：7 堆，(1,1,1) 那堆 2 個；Char = s_(2,1)
    w = Counter(content(T, 3) for T in ssyt((2, 1), 3))
    assert len(w) == 7 and w[(1, 1, 1)] == 2 and dict(w) == schur_poly((2, 1), 3)
    assert max(w) == (2, 1, 0)                                                   # 最高權重 = λ（字典序）
    # Schur–Weyl：m^n = Σ d_λ(m) f^λ
    f = lambda lam: len(standard_tableaux(lam))
    for m in (2, 3):
        assert sum(d(l, m) * f(l) for l in ((3,), (2, 1), (1, 1, 1))) == m ** 3
    assert [d(l, 2) * f(l) for l in ((3,), (2, 1), (1, 1, 1))] == [4, 4, 0]
    assert [d(l, 3) * f(l) for l in ((3,), (2, 1), (1, 1, 1))] == [10, 16, 1]
    # Pieri：Sym^2 E ⊗ E = E^(3) ⊕ E^(2,1)（m = 3：18 = 10 + 8）；Cor 3：Sym^2(E ⊕ E) = 21 = 6·3 + 3·1
    assert 6 * 3 == d((3,), 3) + d((2, 1), 3) == 18
    assert comb(6 + 1, 2) == d((2,), 3) * d((2,), 2) + d((1, 1), 3) * d((1, 1), 2) == 21
    # 行列式模型：D_12·z_3 = D_32·z_1 + D_13·z_2（z_i = z_{i1}，D_ij = 前兩行的 2×2 子式）
    Z = sp.Matrix(3, 2, sp.symbols("z11 z12 z21 z22 z31 z32"))
    D = lambda i, j: Z[i - 1, 0] * Z[j - 1, 1] - Z[j - 1, 0] * Z[i - 1, 1]
    z = lambda i: Z[i - 1, 0]
    assert sp.expand(D(1, 2) * z(3) - D(3, 2) * z(1) - D(1, 3) * z(2)) == 0
    # Plücker：A 的 2×2 子式
    A = [[1, 2, 0, 1], [0, 1, 3, 2]]
    p = lambda i, j: A[0][i - 1] * A[1][j - 1] - A[0][j - 1] * A[1][i - 1]
    assert [p(1, 2), p(1, 3), p(1, 4), p(2, 3), p(2, 4), p(3, 4)] == [1, 3, 2, 6, 3, -3]
    assert (p(1, 2) * p(3, 4), p(1, 3) * p(2, 4), p(1, 4) * p(2, 3)) == (-3, 9, 12)
    # Grassmannian G(2,4) 的座標環：第 k 次 = E^(k,k)（m = 4）；6、21 − 1 = 20
    assert d((1, 1), 4) == 6 and d((2, 2), 4) == comb(6 + 1, 2) - 1 == 20
    print("第 8 章（part6.tex）的數字全部正確")


# =============================================================================
# 第 9–10 章（part7.tex、part8.tex；動畫 F46–F55）：數字檢查與圖表
# =============================================================================
def rev_echelon(rows):
    """Fulton §9.4 的列梯形：每列最後一個非零數是 1（樞紐），樞紐所在的行其他列都是 0，樞紐由左到右遞增。"""
    from fractions import Fraction
    M = [[Fraction(x) for x in r[::-1]] for r in rows]          # 把行倒過來做一般的 RREF
    piv, r = [], 0
    for c in range(len(M[0])):
        k = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if k is None:
            continue
        M[r], M[k] = M[k], M[r]
        M[r] = [x / M[r][c] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                M[i] = [a - M[i][c] * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    out = [row[::-1] for row in M[:r]][::-1]
    return out, [len(rows[0]) - c for c in piv][::-1]


def check_numbers_ch910():
    """part7.tex（第 9 章）與 part8.tex（第 10 章）寫到的每一個數字。"""
    from fractions import Fraction as Fr
    from itertools import combinations

    from utils.schubert import (act_right, box_product, bruhat_chain, bruhat_covers, bruhat_leq, bruhat_leq_tableau,
                                bruhat_levels, count_flags_F2, count_subspaces_F2, descents, divided_difference,
                                flag_cell_pattern, flag_ring_dim, gaussian_binomial, grass_cell_pattern,
                                grassmannian_partition, inversions, length, perms, pipe_dreams, pipe_weight, plucker,
                                plucker_from_coords, q_factorial, rank_matrix, rectangle_count, schubert_path,
                                schubert_poly, swap_vars)
    from utils.tableaux import schur_expand
    X = lambda *e: {tuple(e): 1}
    dd = divided_difference
    # 射影空間的點數
    assert [count_subspaces_F2(n + 1, 1) for n in (1, 2, 3)] == [3, 7, 15] == [2 ** (n + 1) - 1 for n in (1, 2, 3)]
    # Plücker
    A = [[1, 2, 0, 1], [0, 1, 3, 2]]
    pA = plucker(A)
    assert [pA[I] for I in sorted(pA)] == [1, 3, 2, 6, 3, -3]
    gA = [[1, 3, 3, 3], [0, 2, 6, 4]]
    assert [[sum(g * a for g, a in zip(gr, col)) for col in zip(*A)] for gr in ([1, 1], [0, 2])] == gA
    assert [plucker(gA)[I] for I in sorted(pA)] == [2, 6, 4, 12, 6, -6]
    rel = lambda x: x[(1, 2)] * x[(3, 4)] - x[(1, 3)] * x[(2, 4)] + x[(1, 4)] * x[(2, 3)]
    assert rel(pA) == 1 * (-3) - 3 * 3 + 2 * 6 == 0
    assert rel({(1, 2): 1, (1, 3): 0, (1, 4): 0, (2, 3): 0, (2, 4): 0, (3, 4): 1}) == 1
    p3 = plucker([[1, 0, 1], [0, 1, 2]])
    assert (p3[(1, 2)], p3[(1, 3)], p3[(2, 3)]) == (1, 2, -1)
    u, v = (1, 0, 1), (0, 1, 2)
    cross = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    assert cross == (-1, -2, 1) == (p3[(2, 3)], -p3[(1, 3)], p3[(1, 2)])
    from utils.schubert import _det
    for a, b in ([[1, 2, 0, 1], [0, 1, 3, 2]], [[2, -1, 5, 3], [4, 0, 1, 7]]):           # Laplace：2×(關係)
        M = [a, b, a, b]
        x = plucker([a, b])
        lap = sum((-1) ** (3 + sum(I)) * x[I] * x[tuple(sorted(set(range(1, 5)) - set(I)))] for I in combinations(range(1, 5), 2))
        assert lap == 2 * rel(x) and _det(M) == 0
    ex2 = {(1, 2): 1, (1, 3): 2, (1, 4): 1, (2, 3): 1, (2, 4): 2, (3, 4): 3}
    assert rel(ex2) == 3 - 4 + 1 == 0 and plucker_from_coords(ex2, 2, 4) == [[1, 0, -1, -2], [0, 1, 2, 1]]
    pe = plucker([[1, 1, 0, 0], [0, 0, 1, 1]])
    assert [pe[I] for I in sorted(pe)] == [0, 1, 1, 1, 1, 0] and rel(pe) == 0
    # 旗：點在線上
    y = plucker([[1, 2, 3], [0, 1, 1]])
    inc = lambda x: x[0] * y[(2, 3)] - x[1] * y[(1, 3)] + x[2] * y[(1, 2)]
    assert (y[(1, 2)], y[(1, 3)], y[(2, 3)]) == (1, 1, -1) and inc((1, 2, 3)) == 0 and inc((0, 1, 1)) == 0
    assert inc((1, 0, 0)) == -1
    assert [flag_ring_dim(*ab) for ab in ((1, 0), (0, 1), (2, 0), (1, 1), (2, 1), (1, 2), (2, 2))] == [3, 3, 6, 8, 15, 15, 27]
    assert 3 * 3 - 1 == 8 and 6 * 3 - 3 * 1 == 15 and 6 * 6 - 3 * 3 == 27
    # 列梯形的例子（Fulton §9.4 的寫法：r = 2、n = 2，樞紐在第 n+i−λ_i 行）
    lam = lambda piv: tuple(2 + i + 1 - p for i, p in enumerate(piv))
    E1, P1 = rev_echelon([[1, 2, 0, 1], [0, 1, 3, 2]])
    assert E1 == [[Fr(-2, 3), -1, 1, 0], [1, 2, 0, 1]] and lam(P1) == (0, 0)
    assert lam(rev_echelon([[3, 1, 0, 0], [1, 0, 2, 1]])[1]) == (1, 0)
    assert lam(rev_echelon([[1, 0, 0, 0], [0, 1, 1, 1]])[1]) == (2, 0)
    assert lam(rev_echelon([[1, 0, 1, 0], [0, 1, 0, 0]])[1]) == (1, 1)
    assert lam(rev_echelon([[1, 0, 0, 0], [0, 1, 0, 0]])[1]) == (2, 2)
    assert lam(rev_echelon([[0, 1, 0, 0], [0, 0, 0, 1]])[1]) == (1, 0)                   # 練習：⟨e2, e4⟩
    assert gaussian_binomial(4, 2) == [1, 1, 2, 1, 1] and count_subspaces_F2(4, 2) == 35 == 15 * 14 // (3 * 2)
    assert gaussian_binomial(3, 1) == [1, 1, 1] and gaussian_binomial(5, 2) == [1, 1, 2, 2, 2, 1, 1]
    assert count_subspaces_F2(5, 2) == 155 == 31 * 30 // (3 * 2) and count_subspaces_F2(4, 3) == 15
    # Schubert 計算（Gr(2,4)）
    bp = lambda a, b: box_product(a, b, 2, 2)
    assert bp((1,), (1,)) == {(2,): 1, (1, 1): 1} and bp((1,), (2,)) == bp((1,), (1, 1)) == {(2, 1): 1}
    assert bp((1,), (2, 1)) == {(2, 2): 1} and bp((2,), (2,)) == bp((1, 1), (1, 1)) == {(2, 2): 1}
    assert bp((2,), (1, 1)) == {} and bp((2, 1), (1,)) == {(2, 2): 1}
    s = {(): 1}
    for _ in range(4):
        s = poly_sum([{nu: c * k for nu, k in bp(l, (1,)).items()} for l, c in s.items()])
    assert s == {(2, 2): 2}
    assert rectangle_count(2, 5) == 5 == factorial(6) * 1 // (factorial(4) * factorial(3)) and rectangle_count(3, 6) == 42
    assert box_product((2, 1), (2, 1), 3, 3) == {(3, 3): 1, (3, 2, 1): 2, (2, 2, 2): 1}
    # 第 10 章：旗流形
    assert len(perms(2)) == 2 and len(perms(3)) == 6
    assert inversions((2, 3, 1)) == [(1, 3), (2, 3)] and length((2, 3, 1)) == 2
    w = (4, 2, 6, 1, 3, 5)
    assert length(w) == 7 and [r.count("*") for r in flag_cell_pattern(w)] == [3, 1, 3, 0, 0, 0]
    assert q_factorial(3) == [1, 2, 2, 1] and count_flags_F2(3) == 21 == 7 * 3
    assert q_factorial(4) == [1, 3, 5, 6, 5, 3, 1] and count_flags_F2(4) == 315 == 15 * 7 * 3
    # 上同調環 R(3) 的化簡：x1^3 = e1x1^2 − e2x1 + e3、h2(x1,x2) = e1(x1+x2) − e2（都是多項式恆等式）
    e1 = poly_sum([X(1, 0, 0), X(0, 1, 0), X(0, 0, 1)])
    e2 = poly_sum([X(1, 1, 0), X(1, 0, 1), X(0, 1, 1)])
    e3 = X(1, 1, 1)
    neg = lambda f: {k: -c for k, c in f.items()}
    assert poly_sum([poly_mul(e1, X(2, 0, 0)), neg(poly_mul(e2, X(1, 0, 0))), e3]) == X(3, 0, 0)
    assert poly_sum([poly_mul(e1, poly_sum([X(1, 0, 0), X(0, 1, 0)])), neg(e2)]) == poly_sum([X(2, 0, 0), X(1, 1, 0), X(0, 2, 0)])
    # 差商
    assert dd(X(2, 0, 0), 1) == poly_sum([X(1, 0, 0), X(0, 1, 0)]) and dd(X(1, 1, 0), 1) == {}
    assert dd(X(0, 1, 0), 1) == {(0, 0, 0): -1} and dd(X(1, 0, 0), 1) == {(0, 0, 0): 1}
    assert dd(X(3, 0, 0), 1) == poly_sum([X(2, 0, 0), X(1, 1, 0), X(0, 2, 0)])
    assert dd(X(2, 1, 0), 1) == X(1, 1, 0) and dd(X(2, 1, 0), 2) == X(2, 0, 0) and dd(X(0, 1, 1), 2) == {}
    assert dd(X(2, 0, 1), 1) == poly_sum([X(1, 0, 1), X(0, 1, 1)]) and dd(X(0, 2, 1), 2) == X(0, 1, 1)
    f = X(2, 1, 0)
    assert dd(dd(dd(f, 1), 2), 1) == dd(dd(dd(f, 2), 1), 2) == {(0, 0, 0): 1}
    assert dd(poly_mul(X(1, 0, 0), X(1, 0, 0)), 1) == poly_sum([X(1, 0, 0), X(0, 1, 0)])
    assert swap_vars(X(2, 1, 0), 1) == X(1, 2, 0)
    # Schubert 多項式
    S = lambda *w: schubert_poly(w)
    assert S(1, 3, 2) == poly_sum([X(1, 0, 0), X(0, 1, 0)]) and S(3, 2, 1) == X(2, 1, 0)
    path = schubert_path(5, [1, 4, 3, 2, 3])
    assert [len(p) for _, p in path] == [1, 1, 1, 2, 5, 3]
    s21543 = S(2, 1, 5, 4, 3)
    assert len(s21543) == 13 and sum(s21543.values()) == 14 == len(pipe_dreams((2, 1, 5, 4, 3))) and s21543[(2, 1, 1, 0, 0)] == 2
    assert S(1, 2, 4, 3) == poly_sum([X(1, 0, 0, 0), X(0, 1, 0, 0), X(0, 0, 1, 0)])
    assert S(3, 1, 2, 4) == X(2, 0, 0, 0) and S(4, 2, 1, 3) == X(3, 1, 0, 0)                 # 練習 6：支配型
    assert schubert_poly((1, 3, 2, 4, 5)) == {k + (0,): c for k, c in S(1, 3, 2, 4).items()}   # 穩定
    # Monk：x1·x1 = 𝔖_312；(x1+x2)^2 = 𝔖_2314 + 𝔖_1423
    assert poly_mul(X(1, 0, 0), X(1, 0, 0)) == S(3, 1, 2)
    s1324 = S(1, 3, 2, 4)
    assert poly_mul(s1324, s1324) == poly_sum([S(2, 3, 1, 4), S(1, 4, 2, 3)])
    # pipe dream
    assert len(pipe_dreams((1, 3, 2))) == 2 and len(pipe_dreams((3, 2, 1))) == 1
    assert sum(pipe_weight(D, 5) == (2, 1, 1, 0, 0) for D in pipe_dreams((2, 1, 5, 4, 3))) == 2
    # Bruhat
    assert rank_matrix((1, 3, 2)) == [[1, 1, 1], [1, 1, 2], [1, 2, 3]] and rank_matrix((3, 1, 2)) == [[0, 0, 1], [1, 1, 2], [1, 2, 3]]
    assert bruhat_leq((1, 3, 2), (3, 1, 2)) and bruhat_leq_tableau((2, 1, 4, 3), (4, 2, 3, 1))
    assert not bruhat_leq((1, 4, 2, 3), (3, 1, 2, 4)) and not bruhat_leq((3, 1, 2, 4), (1, 4, 2, 3))
    assert bruhat_leq((2, 4, 1, 3), (3, 4, 1, 2)) and not bruhat_leq((2, 3, 1), (3, 1, 2))
    assert len(bruhat_covers(3)) == 8 and [len(l) for l in bruhat_levels(4)] == [1, 3, 5, 6, 5, 3, 1]
    ch = bruhat_chain((4, 2, 8, 3, 6, 1, 7, 9, 5), (6, 7, 9, 2, 5, 1, 8, 3, 4))
    assert len(ch) == 9 and length(ch[0]) == 22 and length(ch[-1]) == 14
    # Grassmann 置換（r = 2、m = 4 的六個）
    G = {(1, 2, 3, 4): (0, 0), (1, 3, 2, 4): (1, 0), (1, 4, 2, 3): (2, 0), (2, 3, 1, 4): (1, 1), (2, 4, 1, 3): (2, 1),
         (3, 4, 1, 2): (2, 2)}
    for w, l in G.items():
        if w != (1, 2, 3, 4):
            assert grassmannian_partition(w) == (l, 2)
    assert grassmannian_partition((1, 3, 4, 2)) == ((1, 1, 0), 3) and S(3, 4, 1, 2) == X(2, 2, 0, 0)
    s1 = schur_poly((1,), 2)
    p4 = poly_mul(poly_mul(s1, s1), poly_mul(s1, s1))
    assert schur_expand(p4, 2) == {(4,): 1, (3, 1): 3, (2, 2): 2}
    # 補充：part7 的 s21^2 完整展開；part8 的例子與練習
    from utils.tableaux import lr_coefficient
    full = {nu: lr_coefficient((2, 1), (2, 1), nu) for nu in partitions(6)}
    assert {nu: c for nu, c in full.items() if c} == {(4, 2): 1, (4, 1, 1): 1, (3, 3): 1, (3, 2, 1): 2, (3, 1, 1, 1): 1,
                                                      (2, 2, 2): 1, (2, 2, 1, 1): 1}
    assert S(3, 2, 1, 4) == X(2, 1, 0, 0) and S(2, 1, 4, 3) == poly_mul(X(1, 0, 0, 0), S(1, 2, 4, 3))
    assert length((3, 1, 4, 2)) == 3 == sum(r.count("*") for r in flag_cell_pattern((3, 1, 4, 2)))
    assert sum(c * 3 ** k for k, c in enumerate(q_factorial(3))) == 52 == (1 + 3) * (1 + 3 + 9)
    assert bruhat_leq_tableau((2, 4, 1, 3), (3, 4, 1, 2)) and not bruhat_leq((2, 3, 1), (3, 1, 2))
    for w, l in G.items():
        sl = schur_poly(tuple(x for x in l if x), 2) if any(l) else {(0, 0): 1}
        assert S(*w) == {e + (0, 0): c for e, c in sl.items()}
    print("第 9–10 章（part7.tex、part8.tex）的數字全部正確")


def _mat_tex(pattern, star=r"\textcolor{cA}{\ast}", one=r"\mathbf{1}", small=False):
    body = r"\\".join("&".join({"*": star, "1": one}.get(s, "0") for s in row) for row in pattern)
    if small:
        return r"\left(\begin{smallmatrix}" + body + r"\end{smallmatrix}\right)"
    return r"\begin{pmatrix}" + body + r"\end{pmatrix}"


def _ydiag(lam):
    lam = [x for x in lam if x]
    return r"$\varnothing$" if not lam else r"{\ytableausetup{smalltableaux}\ydiagram{" + ",".join(map(str, lam)) + "}}"


def fig_grass_cells() -> str:
    from utils.schubert import grass_cell_pattern
    box = [(0, 0), (1, 0), (2, 0), (1, 1), (2, 1), (2, 2)]
    cols = []
    for lam in box:
        pat = grass_cell_pattern(lam, 2, 2)
        k = sum(r.count("*") for r in pat)
        cols.append((lam, pat, k))
    head = " & ".join(_ydiag(l) for l, _, _ in cols)
    mats = " & ".join("$" + _mat_tex(p, small=True) + "$" for _, p, _ in cols)
    dims = " & ".join(f"${k}$" for _, _, k in cols)
    qs = " & ".join(f"$q^{{{k}}}$" if k > 1 else ("$q$" if k == 1 else "$1$") for _, _, k in cols)
    return ("\\begin{tabular}{@{}l" + "c" * 6 + "@{}}\n\\toprule\n$\\lambda$ & " + head + "\\\\\n\\midrule\n"
            "列梯形矩陣 & " + mats + "\\\\[4pt]\n星號數＝維數 & " + dims + "\\\\\n$\\mathbb F_q$ 上的點數 & " + qs
            + "\\\\\n\\bottomrule\n\\end{tabular}\n")


def fig_flag_cells() -> str:
    from utils.schubert import flag_cell_pattern, length, perm_str
    ws = [(1, 2, 3), (2, 1, 3), (1, 3, 2), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
    head = " & ".join(f"${perm_str(w)}$" for w in ws)
    mats = " & ".join("$" + _mat_tex(flag_cell_pattern(w)) + "$" for w in ws)
    lens = " & ".join(f"${length(w)}$" for w in ws)
    return ("\\begin{tabular}{@{}l" + "c" * 6 + "@{}}\n\\toprule\n$w$ & " + head + "\\\\\n\\midrule\n"
            "胞腔 $X^\\circ_w$ & " + mats + "\\\\[4pt]\n$\\ell(w)$＝星號數 & " + lens + "\\\\\n\\bottomrule\n\\end{tabular}\n")


def fig_schubert_s4() -> str:
    from utils.schubert import length, perm_str, perms, poly_str, schubert_poly
    ws = sorted(perms(4), key=lambda w: (length(w), w))
    assert all(e[3] == 0 for w in ws for e in schubert_poly(w))
    cells = [f"${perm_str(w)}$ & ${length(w)}$ & ${poly_str({e[:3]: c for e, c in schubert_poly(w).items()})}$" for w in ws]
    half = len(cells) // 2
    rows = [cells[i] + " & " + cells[i + half] for i in range(half)]
    return ("{\\small\\begin{tabular}{@{}ccl@{\\qquad}ccl@{}}\n"
            + "\\toprule\n$w$ & $\\ell$ & $\\mathfrak S_w$ & $w$ & $\\ell$ & $\\mathfrak S_w$\\\\\n\\midrule\n"
            + "\\\\\n".join(rows) + "\\\\\n\\bottomrule\n\\end{tabular}}\n")


def fig_hasse_s3() -> str:
    from utils.schubert import bruhat_covers, perm_str, poly_str, schubert_poly
    pos = {(3, 2, 1): (0, 3), (2, 3, 1): (-1.6, 2), (3, 1, 2): (1.6, 2), (2, 1, 3): (-1.6, 1), (1, 3, 2): (1.6, 1),
           (1, 2, 3): (0, 0)}
    out = ["\\begin{tikzpicture}[xscale=1.5,yscale=1.75]"]
    for w, (x, y) in pos.items():
        out.append(f"\\node[align=center,inner sep=1pt] ({perm_str(w)}) at ({x},{y}) "
                   f"{{\\footnotesize ${perm_str(w)}$\\\\ $\\scriptstyle {poly_str(schubert_poly(w))}$}};")
    for u, v in bruhat_covers(3):
        out.append(f"\\draw[gray,shorten <=2pt,shorten >=2pt] ({perm_str(u)}.north) -- ({perm_str(v)}.south);")
    out.append("\\end{tikzpicture}")
    return "\n".join(out) + "\n"


def _pipe_tikz(D, m, s=0.42):
    from utils.schubert import pipe_exits
    D = set(D)
    w = pipe_exits(D, m)
    winv = {c: i + 1 for i, c in enumerate(w)}
    out = [f"\\begin{{tikzpicture}}[scale={s},line width=0.9pt]"]
    for i in range(1, m + 1):
        for j in range(1, m + 2 - i):
            x0, y0 = j - 1, -(i - 1)
            out.append(f"\\draw[gray!40,line width=0.3pt] ({x0},{y0}) rectangle ({x0 + 1},{y0 - 1});")
            if (i, j) in D and i + j <= m:
                out.append(f"\\draw[cB] ({x0},{y0 - 0.5}) -- ({x0 + 1},{y0 - 0.5}); \\draw[cB] ({x0 + 0.5},{y0}) -- ({x0 + 0.5},{y0 - 1});")
            else:
                out.append(f"\\draw[cA] ({x0},{y0 - 0.5}) arc[start angle=-90,end angle=0,radius=0.5];")
                if i + j <= m:
                    out.append(f"\\draw[cA] ({x0 + 1},{y0 - 0.5}) arc[start angle=90,end angle=180,radius=0.5];")
        out.append(f"\\node[left] at (0,{-(i - 1) - 0.5}) {{\\tiny {i}}};")
    for c in range(1, m + 1):
        out.append(f"\\node[above] at ({c - 0.5},0) {{\\tiny {winv[c]}}};")
    out.append("\\end{tikzpicture}")
    return "\n".join(out)


def fig_pipes_132() -> str:
    from utils.schubert import pipe_dreams
    return "\\quad ".join(_pipe_tikz(D, 3, 0.55) for D in sorted(pipe_dreams((1, 3, 2)))) + "\n"


def fig_pipes_21543() -> str:
    from utils.schubert import pipe_dreams, pipe_weight
    two = [D for D in pipe_dreams((2, 1, 5, 4, 3)) if pipe_weight(D, 5) == (2, 1, 1, 0, 0)]
    assert len(two) == 2
    return "\\qquad ".join(_pipe_tikz(D, 5, 0.42) for D in two) + "\n"


# =============================================================================
# 附錄 A–B（part9.tex、part10.tex；動畫 F56–F65）
# =============================================================================
def check_numbers_appAB():
    """part9.tex（附錄 A）與 part10.tex（附錄 B）寫到的每一個數字。"""
    from utils import fulton_appendix as FA
    from utils.schubert import gaussian_binomial, q_factorial
    from utils.tableaux import insert_word, transpose
    assert FA.check()
    # §A.1
    assert FA.dual_word((3, 1, 2, 1), 3) == (3, 2, 3, 1)
    assert insert_word((3, 1, 2, 1)) == ((1, 1), (2,), (3,)) and insert_word((3, 2, 3, 1)) == ((1, 3), (2,), (3,))
    assert FA.evacuation(((1, 1), (2,), (3,)), 3) == ((1, 3), (2,), (3,))
    st = FA.evacuation_steps(((1, 2), (3,)), 3)
    assert [s[1] for s in st] == [(0, 1), (1, 0), (0, 0)] and [s[2] for s in st] == [3, 2, 1]
    assert FA.evacuation(((1, 2), (3,)), 3) == ((1, 3), (2,)) and FA.evacuation(((1, 3), (2,)), 3) == ((1, 2), (3,))
    assert FA.evacuation(((1, 1, 2), (2, 3)), 3) == ((1, 2, 3), (2, 3))
    T = ((1, 2, 2, 3), (2, 3, 5, 5), (4, 4, 6), (5, 6))
    assert FA.evacuation_steps(T, 6)[0][0] == ((2, 2, 2, 3), (3, 4, 5, 5), (4, 6, 6), (5,))
    assert FA.evacuation(T, 6) == ((1, 1, 2, 3), (2, 2, 3, 5), (4, 4, 5), (5, 6))
    # §A.2
    assert FA.column_insert(((1, 3), (2,)), 1)[0] == ((1, 1, 3), (2,)) and FA.column_insert(((1, 3), (2,)), 2)[0] == ((1, 2, 3), (2,))
    assert FA.column_insert(((1, 2), (3,)), 2)[0] == ((1, 2), (2, 3))
    assert insert_word((2, 4, 1, 3, 5)) == FA.column_insert_word((5, 3, 1, 4, 2)) == ((1, 3, 5), (2, 4))
    assert insert_word((5, 3, 1, 4, 2)) == ((1, 2), (3, 4), (5,)) == transpose(((1, 3, 5), (2, 4)))
    # §A.4.1–4.2
    A = [[1, 2, 0], [0, 1, 1], [1, 1, 1]]
    assert FA.antilex_sort(*zip(*FA.matrix_to_pairs(A))) == ((3, 3, 3, 2, 2, 1, 1, 1), (1, 2, 3, 2, 3, 1, 2, 2))
    P, Q = FA.rsk_array(*zip(*FA.matrix_to_pairs(A)))
    R, S = FA.burge(A)
    assert (P, Q) == (((1, 1, 2, 2, 2, 3), (2, 3)), ((1, 1, 1, 2, 2, 3), (3, 3)))
    assert (R, S) == (((1, 1, 2, 2, 2), (2, 3), (3,)), ((1, 1, 1, 3, 3), (2, 2), (3,)))
    c = FA.corners(A)
    assert c["se"] == (P, ((1, 1, 1, 3, 3, 3), (2, 2))) and FA.evacuation(P, 3) == P
    assert c["sw"] == (R, ((1, 1, 1, 2, 3), (2, 3), (3,))) and c["ne"] == (((1, 1, 2, 2, 3), (2, 2), (3,)), S)
    # §A.4.3
    assert FA.dual_rsk([[0, 1, 1], [1, 0, 1], [1, 0, 1]]) == (((1, 1, 2), (3, 3, 3)), ((1, 1), (2, 2), (3, 3)))
    assert len(FA.zero_one_matrices((3, 2, 1), (2, 2, 2))) == 3 and FA.zero_one_matrices((3, 3), (3, 1, 1, 1)) == []
    assert len(FA.zero_one_matrices((2, 2), (2, 2))) == 1 and len(FA.zero_one_matrices((3, 1), (2, 1, 1))) == 1
    assert FA.gale_ryser((3, 2, 1), (2, 2, 2)) and not FA.gale_ryser((3, 3), (3, 1, 1, 1))
    assert conjugate((3, 3)) == (2, 2, 2) and conjugate((3, 2, 1)) == (3, 2, 1)
    assert sum(kostka(conjugate(nu), (3, 2, 1)) * kostka(nu, (2, 2, 2)) for nu in partitions(6)) == 3
    # §A.5
    T5 = ((1, 1, 2, 2), (2, 3, 3), (4,))
    assert FA.frank_tableau(T5, [2, 3, 2, 1]) == ((1, 2), (1, 3, 4), (2, 3), (2,))
    assert FA.keys(T5) == (((1, 1, 1, 1), (2, 2, 2), (4,)), ((2, 2, 2, 2), (3, 3, 3), (4,)))
    assert FA.keys(((1, 2), (3,))) == (((1, 1), (3,)), ((2, 2), (3,)))
    # 附錄 A 的練習
    assert FA.dual_word((4, 1, 3, 2), 4) == (3, 2, 4, 1)
    assert FA.column_insert(((1, 2), (3,)), 3)[0] == ((1, 2), (3, 3))
    assert FA.gale_ryser((2, 2, 1), (3, 1, 1)) and conjugate((2, 2, 1)) == (3, 2)
    assert [[1, 1, 0], [1, 0, 1], [1, 0, 0]] in FA.zero_one_matrices((2, 2, 1), (3, 1, 1))
    # 附錄 B
    assert FA.betti_from_cells([1, 1, 1]) == ([1, 0, 1, 0, 1], 3)
    assert FA.betti_from_cells(gaussian_binomial(4, 2)) == ([1, 0, 1, 0, 2, 0, 1, 0, 1], 6)
    assert FA.betti_from_cells(q_factorial(3))[1] == 6 and FA.betti_from_cells([1, 1])[1] == 2
    assert FA.chern_projective(1) == [1, 2] and FA.chern_projective(2) == [1, 3, 3] and FA.chern_projective(3) == [1, 4, 6, 4]
    assert FA.plucker_degree(2, 4) == 2 and FA.plucker_degree(2, 5) == 5 and FA.plucker_degree(3, 6) == 42
    assert 1 * 2 == 2 and 2 * 2 == 4                                               # 直線∩圓錐、兩條圓錐
    # Segre：(h1+h2)^2 = 2 h1 h2（h1^2 = h2^2 = 0）
    sq = poly_mul({(1, 0): 1, (0, 1): 1}, {(1, 0): 1, (0, 1): 1})
    assert {e: c for e, c in sq.items() if max(e) <= 1} == {(1, 1): 2}
    cu = poly_mul(sq, {(1, 0): 1, (0, 1): 1})                                        # P^1 × P^2：h1^2 = 0、h2^3 = 0
    assert {e: c for e, c in cu.items() if e[0] <= 1 and e[1] <= 2} == {(1, 2): 3}
    assert FA.betti_from_cells(gaussian_binomial(5, 2)) == ([1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 1, 0, 1], 10)
    assert FA.betti_from_cells(q_factorial(4))[1] == 24 and 3 * 3 == 9
    print("附錄 A–B（part9.tex、part10.tex）的數字全部正確")


def _ytab(T):
    return r"{\ytableausetup{smalltableaux}\ytableaushort{" + ",".join("".join(map(str, r)) for r in T) + "}}"


def fig_evac_small() -> str:
    """T = 12/3（N = 3）的 evacuation：每步的 ΔT 與逐漸填滿的 T*。"""
    from utils.fulton_appendix import evacuation_steps
    T = ((1, 2), (3,))
    lam = (2, 1)
    star = {}
    cols_top, cols_bot = [_ytab(T)], [r"{\ytableausetup{smalltableaux}\ytableaushort{{}{},{}}}"]
    for nxt, b, val in evacuation_steps(T, 3):
        star[b] = val
        cols_top.append(_ytab(nxt) if nxt else r"$\varnothing$")
        rows = []
        for i in range(len(lam)):
            rows.append("".join(str(star[(i, j)]) if (i, j) in star else "{}" for j in range(lam[i])))
        cols_bot.append(r"{\ytableausetup{smalltableaux}\ytableaushort{" + ",".join(rows) + "}}")
    n = len(cols_top)
    return ("\\begin{tabular}{@{}l" + "c" * n + "@{}}\n剩下的表 & " + " & ".join(cols_top) + "\\\\[4pt]\n"
            "$T^*$（填進去的 $x^*=4-x$） & " + " & ".join(cols_bot) + "\\\\\n\\end{tabular}\n")


def fig_gale_ryser() -> str:
    from utils.fulton_appendix import zero_one_matrices
    mats = zero_one_matrices((3, 2, 1), (2, 2, 2))
    return "\\quad ".join("$" + r"\begin{pmatrix}" + r"\\".join("&".join(map(str, r)) for r in M) + r"\end{pmatrix}$"
                          for M in mats) + "\n"


FIGURES += [
    ("FulEvacSmall", fig_evac_small),
    ("FulGaleRyser", fig_gale_ryser),
]

FIGURES += [
    ("FulGrassCells", fig_grass_cells),
    ("FulFlagCells", fig_flag_cells),
    ("FulSchubertSfour", fig_schubert_s4),
    ("FulHasseSthree", fig_hasse_s3),
    ("FulPipesOTT", fig_pipes_132),
    ("FulPipesTOFFT", fig_pipes_21543),
]


def main():
    check_numbers()
    check_numbers_ch56()
    check_numbers_ch7()
    check_numbers_ch8()
    check_numbers_ch910()
    check_numbers_appAB()
    parts = ["% figs.tex —— 由 fulton/make_figs.py 產生，請勿手動修改。\n"
             "% 重新產生：python fulton/make_figs.py（附錄 B，動畫 F09–F19）\n"]
    for name, func in FIGURES:
        body = func()
        assert "\n\n" not in body
        parts.append(f"\\newcommand{{\\{name}}}{{%\n{body}}}\n")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"已寫出 {OUT.name}：{len(FIGURES)} 張圖")


if __name__ == "__main__":
    main()
