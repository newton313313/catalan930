"""
Scene F17 —— R-S-K：雙列陣列、矩陣與對稱定理（Fulton《Young Tableaux》§4.1，書 p.38–41）

    字典序的雙列陣列 ω = (u_1 … u_r / v_1 … v_r)：(1) u 弱遞增 (2) u_{k-1} = u_k ⇒ v_{k-1} ≤ v_k
    R-S-K：v_k 列插入 P，P 的新格子在 Q 的同一位置寫 u_k。書上的 CH4_ARRAY（Exercise 1）：
        (1 1 1 2 2 3 3 3 3 / 1 2 2 1 2 1 1 1 2) → P = ((1,1,1,1,1,2),(2,2,2))、Q = ((1,1,1,2,3,3),(2,3,3))
    Q 也是表：上列相同的一段，下列弱遞增 → 列擠壓引理：新格子一格比一格靠右，不會在同一行
    R-S-K 定理 (i)–(iii)；矩陣 A = CH4_MATRIX：列和 (3,2,4) = Q 的內容、行和 (5,4) = P 的內容
    對稱定理：陣列上下翻（＝轉置 A）↔ (Q, P)（Exercise 2）；推論 P(w⁻¹) = Q(w)（w = 3142）
    對稱矩陣 ↔ P = Q；S₄ 的 10 個對合 ↔ 4 格的 10 個標準表

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算；字幕裡的列號、欄號 1 起算）。

試渲染（在 C:\\mypython\\manim\\projects\\combkit）：
    python tools/render_check.py ../catalan930/codes/scenes/sceneF17_rsk_arrays.py SceneF17RSKArrays
           --config ../catalan930/codes/custom_config.yml
"""
import sys
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import TwoRowArray, assert_apart, assert_in_frame, labeled, tableau_mob
from utils.mit_draw import CELL_STROKE
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH4_ARRAY, CH4_MATRIX, CH4_P, CH4_Q, array_to_matrix, bump_steps, content, count_involutions, inverse_rsk,
    is_lex_array, is_standard, is_tableau, matrix_to_array, partitions, row_insert, rsk, rsk_matrix, rsk_steps,
    shape, standard_tableaux, transpose_matrix, young_boxes,
)

TOP, BOT = CH4_ARRAY
STEPS = rsk_steps(TOP, BOT)
NEW_BOXES = [(0, 0), (0, 1), (0, 2), (1, 0), (0, 3), (1, 1), (1, 2), (0, 4), (0, 5)]
A = CH4_MATRIX
AT = transpose_matrix(A)
FLIP = matrix_to_array(AT)                                   # 上下翻、再排回字典序
FLIP_ORDER = sorted(range(len(TOP)), key=lambda k: (BOT[k], TOP[k], k))   # 第 s 個位置放原來的第幾欄
W = (3, 1, 4, 2)
W_INV = tuple(W.index(k) + 1 for k in range(1, 5))
PW, QW = rsk(W)
INVOLUTIONS = [(lam, T, inverse_rsk(T, T)[1]) for lam in partitions(4) for T in standard_tableaux(lam)]

U_COLORS = {1: TEAL, 2: GOLD, 3: PINK}
NEW_COLOR = GREEN
FS = 36


def check_math():
    assert is_lex_array(TOP, BOT) and len(TOP) == 9
    assert [s[0] for s in STEPS] == list(TOP) and [s[1] for s in STEPS] == list(BOT)
    assert [s[4] for s in STEPS] == NEW_BOXES
    assert (STEPS[-1][2], STEPS[-1][3]) == rsk(TOP, BOT) == (CH4_P, CH4_Q)
    assert is_tableau(CH4_P) and is_tableau(CH4_Q) and shape(CH4_P) == shape(CH4_Q) == (6, 3)
    assert bump_steps(STEPS[2][2], 1) == [((0, 1), 1, 2), ((1, 0), 2, None)]       # 第 4 欄
    for u in set(TOP):                                        # Q 裡同一個數不在同一行
        cols = [j for i, j in young_boxes(shape(CH4_Q)) if CH4_Q[i][j] == u]
        assert len(cols) == len(set(cols)) == TOP.count(u)
    # 矩陣、列和、行和
    assert array_to_matrix(TOP, BOT) == A and matrix_to_array(A) == CH4_ARRAY
    assert tuple(map(sum, A)) == (3, 2, 4) == content(CH4_Q)
    assert tuple(map(sum, zip(*A))) == (5, 4) == content(CH4_P)
    assert rsk_matrix(A) == (CH4_P, CH4_Q)
    # 對稱定理（Exercise 2）
    assert tuple(BOT[k] for k in FLIP_ORDER) == FLIP[0] and tuple(TOP[k] for k in FLIP_ORDER) == FLIP[1]
    assert is_lex_array(*FLIP) and rsk(*FLIP) == (CH4_Q, CH4_P) == rsk_matrix(AT)
    # 推論：P(w⁻¹) = Q(w)
    assert W_INV == (2, 4, 1, 3) and rsk(W_INV) == (QW, PW) and PW != QW
    assert PW == ((1, 2), (3, 4)) and QW == ((1, 3), (2, 4)) and is_standard(PW) and is_standard(QW)
    # 對合 ↔ 標準表
    invs = [w for w in permutations(range(1, 5)) if all(w[w[i] - 1] == i + 1 for i in range(4))]
    assert len(invs) == count_involutions(4) == len(INVOLUTIONS) == 10
    assert [len(standard_tableaux(lam)) for lam in partitions(4)] == [1, 3, 2, 3, 1]
    for lam, T, w in INVOLUTIONS:
        assert w in invs and rsk(w) == (T, T) and shape(T) == lam
    assert sorted(w for _, _, w in INVOLUTIONS) == sorted(invs)


# =============================================================================
# 小工具
# =============================================================================
def number_matrix(M, font_size=40, dx=0.72, dy=0.62):
    """數字矩陣（左右圓括號）：.ent[(i, j)]、.lp、.rp。"""
    ent, ents = {}, VGroup()
    for i, row in enumerate(M):
        for j, a in enumerate(row):
            t = Tex(str(a), font_size=font_size).move_to(np.array([j * dx, -i * dy, 0.0]))
            ent[(i, j)] = t
            ents.add(t)
    mid = -(len(M) - 1) * dy / 2
    lp = Tex("(", font_size=font_size).stretch_to_fit_height((len(M) - 1) * dy + 0.7)
    rp = Tex(")", font_size=font_size).stretch_to_fit_height((len(M) - 1) * dy + 0.7)
    lp.move_to(np.array([-0.42, mid, 0.0]))
    rp.move_to(np.array([(len(M[0]) - 1) * dx + 0.42, mid, 0.0]))
    g = VGroup(lp, ents, rp)
    g.ent, g.lp, g.rp = ent, lp, rp
    return g


def empty_board(top_left, cs):
    return {"T": (), "cs": cs, "top_left": np.array(top_left, dtype=float), "cells": {}, "ents": {}}


def cell_point(st, i, j):
    return st["top_left"] + (j + 0.5) * st["cs"] * RIGHT + (i + 0.5) * st["cs"] * DOWN


def new_square(st, i, j):
    sq = Square(side_length=st["cs"], stroke_color=CELL_STROKE, stroke_width=3)
    return sq.set_fill(NEW_COLOR, opacity=0.4).move_to(cell_point(st, i, j))


def animate_insert(scene, st, x, mover, step_time=0.45):
    """列插入 st["T"] ← x：mover 飛到第 1 列上方，再一列一列擠下去（同 F06）。回傳新格子。"""
    steps = bump_steps(st["T"], x)
    T_new, _, new = row_insert(st["T"], x)
    cs = st["cs"]
    scene.play(mover.animate.move_to(cell_point(st, *steps[0][0]) + 0.85 * cs * UP).set_fill(YELLOW),
               run_time=step_time + 0.1)
    cur = mover
    for (r, c), v, b in steps:
        target = cell_point(st, r, c)
        if b is None:
            sq = new_square(st, r, c)
            st["cells"][(r, c)] = sq
            scene.play(FadeIn(sq), cur.animate.move_to(target).set_fill(WHITE), run_time=step_time)
            st["ents"][(r, c)] = cur
        else:
            old = st["ents"][(r, c)]
            assert old.tab_value == b
            scene.play(cur.animate.move_to(target).set_fill(WHITE),
                       old.animate.move_to(target + 0.5 * cs * (DOWN + RIGHT)).set_fill(YELLOW), run_time=step_time)
            st["ents"][(r, c)] = cur
            cur = old
    st["T"] = T_new
    assert all(st["ents"][(i, j)].tab_value == T_new[i][j] for i, j in young_boxes(shape(T_new)))
    return new


def bump_caption(k, u, v, T):
    steps = bump_steps(T, v)
    parts = [f"{x} 擠出 {b}" for _, x, b in steps if b is not None]
    (r, _), x, _ = steps[-1]
    return (f"第 {k + 1} 欄：" + "，".join(parts + [f"{x} 落在第 {r + 1} 列"]) + "；", "$Q$", f" 的同一格寫 {u}")


# =============================================================================
# 第 1 段：雙列陣列與字典序
# =============================================================================
def part_arrays(scene):
    gen = TwoRowArray(["u_1", "u_2", r"\cdots", "u_r"], ["v_1", "v_2", r"\cdots", "v_r"], font_size=40, buff=0.3)
    head = VGroup(Tex(r"\omega=", font_size=44), gen).arrange(RIGHT, buff=0.2).move_to(np.array([-3.7, 2.25, 0.0]))
    cond = VGroup(Tex(r"(1)\quad u_1\le u_2\le\cdots\le u_r", font_size=34),
                  Tex(r"(2)\quad u_{k-1}=u_k\ \Rightarrow\ v_{k-1}\le v_k", font_size=34))
    cond.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(np.array([2.9, 2.25, 0.0]))
    ex = TwoRowArray(TOP, BOT, font_size=48, buff=0.55, center=np.array([0.0, -0.05, 0.0]))
    marks = VGroup()
    for u in sorted(set(TOP)):
        ks = [k for k, t in enumerate(TOP) if t == u]
        y = ex.get_bottom()[1] - 0.2
        line = Line(np.array([ex.col(ks[0]).get_left()[0] - 0.1, y, 0.0]),
                    np.array([ex.col(ks[-1]).get_right()[0] + 0.1, y, 0.0]), stroke_color=U_COLORS[u], stroke_width=4)
        marks.add(VGroup(line, Tex(f"u={u}", font_size=30, fill_color=U_COLORS[u]).next_to(line, DOWN, buff=0.15)))
    note = mixed("字是特例：上列就是 ", "$1,2,\\ldots,r$", "，下列就是那個字", font_size=26, color=MUTED_COLOR)
    note.move_to(np.array([0.0, -2.4, 0.0]))
    assert_in_frame(head, cond, ex, marks, note)
    assert_apart(head, cond, gap=0.3)
    assert_apart(VGroup(head, cond), ex, gap=0.4)
    assert_apart(marks, note, gap=0.3)
    for m1, m2 in zip(marks, marks[1:]):
        assert_apart(m1, m2, gap=0.15)

    scene.say("把字推廣成雙列陣列：上下兩列，每一欄是一對數")
    scene.play(FadeIn(head, shift=0.2 * RIGHT), run_time=0.8)
    scene.wait(0.4)
    scene.say("要排成字典序：上列弱遞增；上列相同的地方，下列也弱遞增")
    scene.play(LaggedStart(*[FadeIn(c, shift=0.15 * LEFT) for c in cond], lag_ratio=0.4), run_time=1.0)
    scene.wait(1.0)
    scene.say("書上的例子：上列分成 1、2、3 三段，每一段的下列都不減")
    scene.play(FadeIn(ex), run_time=0.7)
    scene.play(*[ex.col(k).animate.set_fill(U_COLORS[t]) for k, t in enumerate(TOP)],
               LaggedStart(*[FadeIn(m, shift=0.1 * UP) for m in marks], lag_ratio=0.3), run_time=1.0)
    scene.wait(1.2)
    scene.say("字就是特例：上列剛好是 ", "$1,2,\\ldots,r$")
    scene.play(FadeIn(note, shift=0.15 * UP), run_time=0.6)
    scene.wait(1.0)


# =============================================================================
# 第 2 段：逐欄做 R-S-K（Exercise 1）
# =============================================================================
def part_insert(scene):
    arr = TwoRowArray(TOP, BOT, font_size=40, buff=0.42, center=np.array([-0.6, 2.35, 0.0]))
    tags = VGroup(mixed("上列 ", "$\\to Q$", font_size=22, color=MUTED_COLOR),
                  mixed("下列 ", "$\\to P$", font_size=22, color=MUTED_COLOR))
    for row, tag in enumerate(tags):
        tag.next_to(arr, RIGHT, buff=0.4)
        tag.set_y(arr.col(0)[row].get_y())
    cs = 0.64
    P, Q = empty_board((-5.2, 0.95, 0.0), cs), empty_board((1.4, 0.95, 0.0), cs)
    labs = VGroup(*[Tex(n, font_size=48).move_to(st["top_left"] + np.array([-0.5, -cs / 2, 0.0]))
                    for n, st in (("P", P), ("Q", Q))])
    areas = [Rectangle(width=6 * cs + 0.35, height=2 * cs + 0.35).move_to(st["top_left"], aligned_edge=UL)
             for st in (P, Q)]
    why = mixed("$u_{k-1}=u_k$", "：", "$v_{k-1}\\le v_k$", "$\\Rightarrow$", "新格子嚴格往右（列擠壓引理）",
                font_size=26)
    why.move_to(np.array([0.0, -2.25, 0.0]))
    note = zh("同色的格子任兩格不同行 → Q 的每一行嚴格遞增", font_size=24, color=MUTED_COLOR)
    note.move_to(np.array([3.3, -0.95, 0.0]))
    assert_in_frame(arr, tags, labs, *areas, why, note)
    assert_apart(VGroup(arr, tags), VGroup(labs, *areas), gap=0.2)
    assert_apart(areas[0], areas[1], gap=0.5)
    assert_apart(areas[1], note, gap=0.1)
    assert_apart(note, why, gap=0.3)

    scene.say("R-S-K：一欄一欄處理；下列的數列插入 ", "$P$", "，上列的數記在 ", "$Q$")
    scene.play(FadeIn(arr), FadeIn(tags), FadeIn(labs), run_time=0.8)
    scene.wait(0.3)
    hl = SurroundingRectangle(arr.col(0), buff=0.1, color=YELLOW, stroke_width=3)
    fresh = []
    for k, (u, v, Pk, Qk, new) in enumerate(STEPS):
        slow = k in (0, 3)                     # 第 1 欄與第一次擠壓放慢
        if k == 0:
            scene.say("第 1 欄：", f"${v}$", " 放進 ", "$P$", "；", "$P$", " 的新格子在哪，", "$Q$", " 就在同一格寫上列的數")
        elif k == 3:
            scene.say(*bump_caption(k, u, v, P["T"]))
        elif k == 4:
            scene.say("其餘幾欄照做")
        scene.play(ShowCreation(hl) if k == 0 else hl.animate.move_to(arr.col(k)),
                   *[m.animate.set_fill(opacity=0) for m in fresh], run_time=0.3 if slow else 0.2)
        mover = Tex(str(v), font_size=FS).move_to(arr.col(k)[1])
        mover.tab_value = v
        scene.add(mover)
        assert animate_insert(scene, P, v, mover, step_time=0.42 if slow else 0.26) == new and P["T"] == Pk
        q_sq = new_square(Q, *new)
        q_ent = Tex(str(u), font_size=FS).move_to(arr.col(k)[0])
        q_ent.tab_value = u
        scene.play(FadeIn(q_sq), q_ent.animate.move_to(cell_point(Q, *new)), arr.col(k).animate.set_fill(GREY_C),
                   run_time=0.45 if slow else 0.3)
        Q["cells"][new], Q["ents"][new], Q["T"] = q_sq, q_ent, Qk
        fresh = [P["cells"][new], q_sq]
        if k == 0:
            scene.wait(0.4)
    assert P["T"] == CH4_P and Q["T"] == CH4_Q
    ok = VGroup(*[SurroundingRectangle(VGroup(*st["cells"].values()), buff=0.08, color=OK_COLOR, stroke_width=3)
                  for st in (P, Q)])
    scene.play(FadeOut(hl), *[m.animate.set_fill(opacity=0) for m in fresh], run_time=0.3)
    scene.say("九欄做完：得到書上 Exercise 1 的答案 ", "$(P,Q)$")
    scene.play(ShowCreation(ok), run_time=0.6)
    scene.wait(0.8)

    # Q 為什麼是表
    scene.say("為什麼 ", "$Q$", " 也是表？把 ", "$Q$", " 的格子依上列的數上色")
    scene.play(FadeOut(ok), *[Q["cells"][b].animate.set_fill(U_COLORS[Q["T"][b[0]][b[1]]], opacity=0.45)
                              for b in Q["cells"]],
               *[arr.col(k)[0].animate.set_fill(U_COLORS[t]) for k, t in enumerate(TOP)], run_time=0.8)
    scene.play(FadeIn(note, shift=0.1 * UP), run_time=0.5)
    scene.wait(0.6)
    scene.say("上列相同的一段，下列弱遞增；由列擠壓引理，新格子一格比一格靠右")
    scene.play(FadeIn(why, shift=0.15 * UP), run_time=0.6)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：R-S-K 定理
# =============================================================================
def part_theorem(scene):
    title = zh("R-S-K 定理", font_size=36, color=YELLOW).move_to(2.65 * UP)
    left, right = Tex(r"\omega", font_size=60), Tex(r"(P,Q)", font_size=50)
    VGroup(left, right).arrange(RIGHT, buff=3.4).move_to(1.35 * UP)
    a1 = Arrow(left.get_right() + 0.25 * RIGHT + 0.14 * UP, right.get_left() + 0.25 * LEFT + 0.14 * UP,
               buff=0.0, thickness=3, fill_color=GREY_B)
    a2 = Arrow(right.get_left() + 0.25 * LEFT + 0.14 * DOWN, left.get_right() + 0.25 * RIGHT + 0.14 * DOWN,
               buff=0.0, thickness=3, fill_color=GREY_B)
    l1 = zh("列插入", font_size=22, color=MUTED_COLOR).next_to(a1, UP, buff=0.12)
    l2 = zh("反向擠出", font_size=22, color=MUTED_COLOR).next_to(a2, DOWN, buff=0.12)
    lines = VGroup(
        mixed("字典序的雙列陣列 ", "$\\omega$", "$\\longleftrightarrow$", "形狀相同的一對表 ", "$(P,Q)$",
              font_size=28),
        mixed("(i)  ", "$\\omega$", " 每列 ", "$r$", " 個數 ", "$\\Leftrightarrow$", " ", "$P,Q$", " 各 ", "$r$",
              " 格；", "$P$", " 的數＝下列，", "$Q$", " 的數＝上列", font_size=26),
        mixed("(ii)  ", "$\\omega$", " 是字 ", "$\\Leftrightarrow$", " ", "$Q$", " 是標準表", font_size=26),
        mixed("(iii)  ", "$\\omega$", " 是排列 ", "$\\Leftrightarrow$", " ", "$P$", "、", "$Q$", " 都是標準表", font_size=26),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(np.array([0.0, -1.2, 0.0]))
    box = SurroundingRectangle(lines, buff=0.22, color=YELLOW, stroke_width=2.5)
    assert_in_frame(title, left, right, a1, a2, l1, l2, box)
    assert_apart(title, VGroup(left, right, l1), gap=0.2)
    assert_apart(VGroup(left, right, a1, a2, l1, l2), box, gap=0.2)

    scene.say("反過來：每次取 ", "$Q$", " 最大的數（一樣大取最右邊）那格，對 ", "$P$", " 反向擠出")
    scene.play(FadeIn(title), FadeIn(left), FadeIn(right), GrowArrow(a1), FadeIn(l1), run_time=0.9)
    scene.play(GrowArrow(a2), FadeIn(l2), run_time=0.6)
    scene.wait(1.0)
    scene.say("兩個過程互逆：字典序陣列與同形狀的表對一一對應")
    scene.play(ShowCreation(box), LaggedStart(*[FadeIn(m, shift=0.1 * UP) for m in lines], lag_ratio=0.3),
               run_time=1.4)
    scene.wait(2.0)


# =============================================================================
# 第 4 段：矩陣
# =============================================================================
def part_matrix(scene):
    arr = TwoRowArray(TOP, BOT, font_size=36, buff=0.36, center=np.array([-2.9, 2.35, 0.0]))
    mat = number_matrix(A, font_size=42, dx=0.8, dy=0.68).move_to(np.array([-2.75, -0.35, 0.0]))
    rlab = VGroup(*[Tex(str(i + 1), font_size=26, fill_color=MUTED_COLOR)
                    .move_to(np.array([mat.lp.get_left()[0] - 0.3, mat.ent[(i, 0)].get_y(), 0.0])) for i in range(3)])
    clab = VGroup(*[Tex(str(j + 1), font_size=26, fill_color=MUTED_COLOR)
                    .move_to(np.array([mat.ent[(0, j)].get_x(), mat.get_top()[1] + 0.3, 0.0])) for j in range(2)])
    a_lab = Tex("A=", font_size=44).next_to(rlab, LEFT, buff=0.3)
    rsum = VGroup(*[Tex(str(s), font_size=40, fill_color=GOLD)
                    .move_to(np.array([mat.rp.get_right()[0] + 0.55, mat.ent[(i, 0)].get_y(), 0.0]))
                    for i, s in enumerate(map(sum, A))])
    csum = VGroup(*[Tex(str(s), font_size=40, fill_color=TEAL)
                    .move_to(np.array([mat.ent[(0, j)].get_x(), mat.get_bottom()[1] - 0.45, 0.0]))
                    for j, s in enumerate(map(sum, zip(*A)))])
    rhead = zh("列和", font_size=20, color=GOLD).next_to(rsum, UP, buff=0.2)
    chead = zh("行和", font_size=20, color=TEAL).next_to(csum, LEFT, buff=0.75)
    q_item = labeled("Q=", tableau_mob(CH4_Q, 0.55), font_size=40).move_to(np.array([3.6, 1.35, 0.0]))
    p_item = labeled("P=", tableau_mob(CH4_P, 0.55), font_size=40).move_to(np.array([3.6, -1.15, 0.0]))
    q_ct = mixed("內容 ", f"$({','.join(map(str, content(CH4_Q)))})$", font_size=24, color=GOLD).next_to(q_item, DOWN, buff=0.2)
    p_ct = mixed("內容 ", f"$({','.join(map(str, content(CH4_P)))})$", font_size=24, color=TEAL).next_to(p_item, DOWN, buff=0.2)
    left = VGroup(mat, rlab, clab, a_lab, rsum, csum, rhead, chead)
    assert_in_frame(arr, left, q_item, p_item, q_ct, p_ct)
    assert_apart(arr, left, gap=0.2)
    assert_apart(arr, q_item, gap=0.2)
    assert_apart(left, VGroup(q_item, p_item, q_ct, p_ct), gap=0.4)
    assert_apart(q_ct, p_item, gap=0.2)

    groups = {}
    for k, pair in enumerate(zip(TOP, BOT)):
        groups.setdefault(pair, []).append(k)
    assert all(ks == list(range(ks[0], ks[-1] + 1)) and len(ks) == A[u - 1][v - 1] for (u, v), ks in groups.items())
    scene.say("把陣列記成矩陣：", "$a(i,j)$", " ＝ 上 ", "$i$", " 下 ", "$j$", " 的欄出現幾次")
    scene.play(FadeIn(arr), FadeIn(a_lab), FadeIn(mat.lp), FadeIn(mat.rp), FadeIn(rlab), FadeIn(clab), run_time=0.7)
    rect = None
    for (u, v), ks in groups.items():
        r = SurroundingRectangle(VGroup(*[arr.col(k) for k in ks]), buff=0.08, color=YELLOW, stroke_width=3)
        e = mat.ent[(u - 1, v - 1)]
        scene.play(ShowCreation(r) if rect is None else Transform(rect, r), FadeIn(e, scale=1.4),
                   rlab[u - 1].animate.set_fill(YELLOW), clab[v - 1].animate.set_fill(YELLOW), run_time=0.35)
        scene.play(rlab[u - 1].animate.set_fill(MUTED_COLOR), clab[v - 1].animate.set_fill(MUTED_COLOR), run_time=0.12)
        rect = r if rect is None else rect
    scene.play(FadeOut(rect), run_time=0.3)
    scene.say("第 ", "$i$", " 列的和 ＝ ", "$i$", " 在上列出現幾次 ＝ ", "$Q$", " 裡有幾個 ", "$i$")
    scene.play(FadeIn(rsum), FadeIn(rhead), FadeIn(q_item), FadeIn(q_ct), run_time=0.9)
    scene.wait(1.0)
    scene.say("第 ", "$j$", " 行的和 ＝ ", "$j$", " 在下列出現幾次 ＝ ", "$P$", " 裡有幾個 ", "$j$")
    scene.play(FadeIn(csum), FadeIn(chead), FadeIn(p_item), FadeIn(p_ct), run_time=0.9)
    scene.wait(1.2)


# =============================================================================
# 第 5 段：對稱定理、推論、對合
# =============================================================================
def part_symmetry(scene):
    arr = TwoRowArray(TOP, BOT, font_size=40, buff=0.42, center=np.array([1.6, 2.3, 0.0]))
    mat = number_matrix(A, font_size=38, dx=0.7, dy=0.6)
    a_lab = Tex("A=", font_size=42)
    VGroup(a_lab, mat).arrange(RIGHT, buff=0.15).move_to(np.array([-4.9, 2.0, 0.0]))
    mat_t = number_matrix(AT, font_size=38, dx=0.7, dy=0.6).move_to(mat).align_to(mat, LEFT)
    at_lab = Tex("A^{T}=", font_size=42).next_to(mat_t, LEFT, buff=0.15)
    res = VGroup(labeled(r"P(A^{T})=", tableau_mob(CH4_Q, 0.5), font_size=36),
                 labeled(r"Q(A^{T})=", tableau_mob(CH4_P, 0.5), font_size=36)).arrange(RIGHT, buff=0.8)
    res.move_to(np.array([0.0, -0.3, 0.0]))
    concl = mixed("上下翻 ＝ 轉置：", "$(P,Q)\\ \\longmapsto\\ (Q,P)$", font_size=28, color=OK_COLOR)
    concl.move_to(np.array([0.0, -2.0, 0.0]))
    assert_in_frame(arr, mat, a_lab, mat_t, at_lab, res, concl)
    assert_apart(VGroup(a_lab, mat, at_lab, mat_t), arr, gap=0.3)
    assert_apart(VGroup(a_lab, mat, mat_t, arr), res, gap=0.3)
    assert_apart(res, concl, gap=0.3)

    xs = [c.get_x() for c in arr.cols]
    scene.say("對稱定理：把陣列上下翻過來，再排回字典序")
    scene.play(FadeIn(arr), FadeIn(a_lab), FadeIn(mat), run_time=0.7)
    scene.play(*[a for c in arr.cols for a in (c[0].animate(path_arc=-PI / 2).move_to(c[1]),
                                               c[1].animate(path_arc=-PI / 2).move_to(c[0]))], run_time=1.0)
    scene.play(*[arr.col(k).animate.set_x(xs[FLIP_ORDER.index(k)]) for k in range(len(TOP))], run_time=1.1)
    scene.wait(0.3)
    scene.say("在矩陣上，上下翻就是轉置：", "$a(i,j)$", " 搬到 ", "$(j,i)$")
    scene.play(*[ReplacementTransform(mat.ent[(i, j)], mat_t.ent[(j, i)]) for i, j in mat.ent],
               ReplacementTransform(mat.lp, mat_t.lp), ReplacementTransform(mat.rp, mat_t.rp),
               ReplacementTransform(a_lab, at_lab), run_time=1.2)
    scene.wait(0.4)
    scene.say("新的陣列做 R-S-K，得到的正好是 ", "$(Q,P)$", "（Exercise 2）")
    scene.play(LaggedStart(*[FadeIn(r, shift=0.15 * UP) for r in res], lag_ratio=0.4), run_time=1.0)
    scene.play(FadeIn(concl, shift=0.1 * UP), run_time=0.5)
    scene.wait(1.4)


def part_inverse(scene):
    blocks = []
    for name, w, (Pt, Qt), x in (("w", W, (PW, QW), -3.4), ("w^{-1}", W_INV, (QW, PW), 3.4)):
        arr = labeled(f"{name}=", TwoRowArray((1, 2, 3, 4), w, font_size=36), font_size=40)
        tabs = VGroup(labeled(f"P({name})=", tableau_mob(Pt, 0.5), font_size=32, buff=0.2),
                      labeled(f"Q({name})=", tableau_mob(Qt, 0.5), font_size=32, buff=0.2)).arrange(RIGHT, buff=0.4)
        blk = VGroup(arr, tabs).arrange(DOWN, buff=0.55).move_to(np.array([x, 0.9, 0.0]))
        blocks.append(blk)
    arrow = Arrow(blocks[0][0].get_right() + 0.3 * RIGHT, blocks[1][0].get_left() + 0.3 * LEFT, buff=0.0,
                  thickness=3, fill_color=GREY_B)
    alab = zh("上下翻、排序", font_size=22, color=MUTED_COLOR).next_to(arrow, UP, buff=0.12)
    marks = VGroup(*[SurroundingRectangle(blk[1][s][1], buff=0.08, color=col, stroke_width=3)
                     for blk, cols in zip(blocks, ((GOLD, TEAL), (TEAL, GOLD))) for s, col in enumerate(cols)])
    eq = Tex(r"P(w^{-1})=Q(w),\qquad Q(w^{-1})=P(w)", font_size=40, fill_color=OK_COLOR).move_to(-1.75 * UP)
    assert_in_frame(*blocks, arrow, alab, marks, eq)
    assert_apart(blocks[0], blocks[1], gap=0.4)
    assert_apart(VGroup(*blocks, marks), eq, gap=0.3)
    assert_apart(alab, VGroup(blocks[0][1], blocks[1][1]), gap=0.2)

    scene.say("推論：", "$w$", " 是排列時，陣列上下翻再排序，就是反排列 ", "$w^{-1}$")
    scene.play(FadeIn(blocks[0][0]), run_time=0.5)
    scene.play(GrowArrow(arrow), FadeIn(alab), FadeIn(blocks[1][0], shift=0.2 * RIGHT), run_time=0.8)
    scene.wait(0.4)
    scene.say("所以兩張表正好對調：", "$P(w^{-1})=Q(w)$", "、", "$Q(w^{-1})=P(w)$")
    scene.play(FadeIn(blocks[0][1]), FadeIn(blocks[1][1]), run_time=0.8)
    scene.play(ShowCreation(marks), FadeIn(eq, shift=0.1 * UP), run_time=0.7)
    scene.wait(1.4)


def part_involutions(scene):
    top = mixed("對稱矩陣 ", "$A=A^{T}$", "$\\Longleftrightarrow$", "$P=Q$", font_size=30)
    top.move_to(2.6 * UP)
    sub = mixed("排列矩陣對稱 ", "$\\Longleftrightarrow$", " ", "$w=w^{-1}$", "（對合）", font_size=26,
                color=MUTED_COLOR).move_to(1.95 * UP)
    tabs = VGroup(*[tableau_mob(T, 0.34) for _, T, _ in INVOLUTIONS])
    lams = [lam for lam, _, _ in INVOLUTIONS]
    for k in range(1, len(tabs)):
        gap = 0.32 if lams[k] == lams[k - 1] else 0.75
        tabs[k].next_to(tabs[k - 1], RIGHT, buff=gap, aligned_edge=UP)
    tabs.move_to(np.array([0.0, 0.75, 0.0])).align_to(np.array([0.0, 1.3, 0.0]), UP)
    words = VGroup(*[Tex("".join(map(str, w)), font_size=28, fill_color=YELLOW)
                     .move_to(np.array([t.get_x(), tabs.get_bottom()[1] - 0.4, 0.0])) for t, (_, _, w) in zip(tabs, INVOLUTIONS)])
    counts = VGroup()
    f_list = [len(standard_tableaux(lam)) for lam in partitions(4)]
    for lam, f in zip(partitions(4), f_list):
        members = VGroup(*[t for t, l in zip(tabs, lams) if l == lam])
        assert len(members) == f
        counts.add(Tex(str(f), font_size=34, fill_color=GOLD)
                   .move_to(np.array([members.get_x(), words.get_bottom()[1] - 0.45, 0.0])))
    total = mixed("$1+3+2+3+1=10$", " ＝ ", "$S_4$", " 的對合個數", font_size=30, color=OK_COLOR)
    total.move_to(np.array([0.0, -2.3, 0.0]))
    assert f_list == [1, 3, 2, 3, 1] and sum(f_list) == count_involutions(4) == 10
    assert_in_frame(top, sub, tabs, words, counts, total)
    assert_apart(top, sub, gap=0.15)
    assert_apart(sub, tabs, gap=0.25)
    assert_apart(tabs, words, gap=0.1)
    assert_apart(words, counts, gap=0.1)
    assert_apart(counts, total, gap=0.25)
    for a, b in zip(words, words[1:]):
        assert_apart(a, b, gap=0.1)

    scene.say("特別地，對稱矩陣對應到 ", "$P=Q$", " 的表對")
    scene.play(FadeIn(top), run_time=0.6)
    scene.wait(0.5)
    scene.say("排列矩陣對稱就是對合：每張標準表 ", "$T$", " 恰對應一個對合，", "$P(w)=Q(w)=T$")
    scene.play(FadeIn(sub), run_time=0.5)
    scene.play(LaggedStart(*[FadeIn(VGroup(t, w), shift=0.1 * DOWN) for t, w in zip(tabs, words)], lag_ratio=0.12),
               run_time=1.6)
    scene.wait(0.6)
    scene.say("$S_4$", " 有 10 個對合，正好是 4 格標準表的個數 ", "$1+3+2+3+1$")
    scene.play(FadeIn(counts), FadeIn(total, shift=0.1 * UP), run_time=0.8)
    scene.wait(1.8)


class SceneF17RSKArrays(ChuScene):
    def construct(self):
        self.show_header("R-S-K：雙列陣列與對稱定理")
        check_math()
        part_arrays(self)
        self.clear_stage()
        part_insert(self)
        self.clear_stage()
        part_theorem(self)
        self.clear_stage()
        part_matrix(self)
        self.clear_stage()
        part_symmetry(self)
        self.clear_stage()
        part_inverse(self)
        self.clear_stage()
        part_involutions(self)
        self.wait(1.0)
