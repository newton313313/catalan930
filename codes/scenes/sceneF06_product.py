"""
Scene F06 —— 表的字與乘積 T·U（Fulton《Young Tableaux》§1.1，書 p.11–12）

    表的字 w(T)：從最下面一列讀到最上面一列，每列由左往右
        U = [[1,3],[2]]               -> w(U) = 2 1 3
        T = [[1,2,2,3],[2,3,5,5],[4,4,6],[5,6]] -> w(T) = 5 6 | 4 4 6 | 2 3 5 5 | 1 2 2 3
    乘積 T·U：把 w(U) 的數依序列插入 T
        T ← 2 = [[1,2,2,2],[2,3,3,5],[4,4,5],[5,6,6]]
          ← 1 = [[1,1,2,2],[2,2,3,5],[3,4,5],[4,6,6],[5]]
          ← 3 = [[1,1,2,2,3],[2,2,3,5],[3,4,5],[4,6,6],[5]] = T·U
    Claim 1：乘積有結合律、空表是單位元（用小例子驗算兩種括法；證明在書的後面章節）

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算；字幕裡的「第 k 列」1 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF06_product.py SceneF06Product
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.mit_draw import CELL_STROKE, YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh
from utils.tableaux import (
    FULTON_INSERT_T,
    FULTON_PRODUCT_U,
    bump_steps,
    content,
    insert_word,
    insert_word_steps,
    is_tableau,
    num_boxes,
    product,
    row_insert,
    shape,
    tableau_word,
    young_boxes,
)

T0 = FULTON_INSERT_T                       # 書 p.12 的 T（同 F04）
U0 = FULTON_PRODUCT_U                      # 書 p.12 的 U
W_U = (2, 1, 3)
W_T = (5, 6, 4, 4, 6, 2, 3, 5, 5, 1, 2, 2, 3)
STAGES = (                                 # T←2、再 ←1、再 ←3
    ((1, 2, 2, 2), (2, 3, 3, 5), (4, 4, 5), (5, 6, 6)),
    ((1, 1, 2, 2), (2, 2, 3, 5), (3, 4, 5), (4, 6, 6), (5,)),
    ((1, 1, 2, 2, 3), (2, 2, 3, 5), (3, 4, 5), (4, 6, 6), (5,)),
)
NEW_BOXES = ((3, 2), (4, 0), (0, 4))       # 0 起算
SHAPES = ((4, 4, 3, 3), (4, 4, 3, 3, 1), (5, 4, 3, 3, 1))

# Claim 1 的小例子
A_T = ((2, 3),)
A_U = ((1, 2),)
A_V = ((1,),)
A_TU = ((1, 2), (2, 3))
A_UV = ((1, 1), (2,))
A_RES = ((1, 1), (2, 2), (3,))
UNIT_STAGES = (((2,),), ((1,), (2,)), ((1, 3), (2,)))   # 空表依序插入 w(U) = 2 1 3

ROW_COLORS = [TEAL, GOLD, PINK, BLUE_B]    # 第 1、2、3、4 個被讀到的列（由下往上）
ROUTE_COLOR = YELLOW
NEW_COLOR = GREEN

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊（至少一個方向分開 gap）。"""
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a.get_corner(UL).round(2), a.get_corner(DR).round(2),
                                b.get_corner(UL).round(2), b.get_corner(DR).round(2))


def check_math():
    assert is_tableau(T0) and is_tableau(U0)
    assert tableau_word(U0) == W_U and tableau_word(T0) == W_T
    assert len(W_T) == num_boxes(T0) == 13 and num_boxes(U0) == 3 and len(T0) == 4
    steps = insert_word_steps(W_U, T0)
    assert tuple(s[0] for s in steps) == W_U
    assert tuple(s[1] for s in steps) == STAGES
    assert tuple(s[3] for s in steps) == NEW_BOXES
    assert shape(T0) == (4, 4, 3, 2) and tuple(shape(s[1]) for s in steps) == SHAPES
    assert STAGES[-1] == product(T0, U0)
    assert num_boxes(STAGES[-1]) == 16 == 13 + 3
    assert content(STAGES[-1], 6) == tuple(a + b for a, b in zip(content(T0, 6), content(U0, 6)))
    # 字幕裡的擠壓過程
    assert bump_steps(T0, 2) == [((0, 3), 2, 3), ((1, 2), 3, 5), ((2, 2), 5, 6), ((3, 2), 6, None)]
    assert bump_steps(STAGES[0], 1) == [((0, 1), 1, 2), ((1, 1), 2, 3), ((2, 0), 3, 4), ((3, 0), 4, 5),
                                        ((4, 0), 5, None)]
    assert bump_steps(STAGES[1], 3) == [((0, 4), 3, None)]
    # Claim 1：兩種括法
    assert product(A_T, A_U) == A_TU and product(A_U, A_V) == A_UV
    assert product(A_TU, A_V) == A_RES == product(A_T, A_UV)
    left_seq = tableau_word(A_U) + tableau_word(A_V)
    right_seq = tableau_word(A_UV)
    assert left_seq == (1, 2, 1) and right_seq == (2, 1, 1) and left_seq != right_seq
    assert tableau_word(A_V) == (1,)
    assert insert_word(left_seq, A_T) == insert_word(right_seq, A_T) == A_RES
    # 單位元
    assert tuple(s[1] for s in insert_word_steps(W_U, ())) == UNIT_STAGES and UNIT_STAGES[-1] == U0
    assert product((), U0) == U0 == product(U0, ()) and tableau_word(()) == ()
    assert product((), T0) == T0 == product(T0, ())


def tuple_str(lam):
    return "(" + ",".join(str(p) for p in lam) + ")"


def bump_caption(x, steps, n_rows):
    """由 bump_steps 的結果組出字幕（列號 1 起算）。"""
    parts = [f"{v} 擠出 {b}" for _, v, b in steps if b is not None]
    (r, _), v, _ = steps[-1]
    if r == n_rows:
        end = f"{v} 在最下面自成新的第 {r + 1} 列"
    elif len(steps) == 1:
        end = f"第 1 列沒有比 {v} 大的數，{v} 直接接在列尾"
    else:
        end = f"{v} 接在第 {r + 1} 列的尾端"
    return f"插入 {x}：" + "，".join(parts + [end])


def diagram(T, cs, fs, top_left=None):
    """填好數字的 Young 圖；每個數字物件記下 .tab_value。"""
    kw = {} if top_left is None else {"top_left": np.array(top_left, dtype=float)}
    d = YoungDiagramMob(shape(T), cell_size=cs, entries=T, font_size=fs, **kw)
    for i, j in young_boxes(shape(T)):
        d.entry(i, j).tab_value = T[i][j]
    return d


def word_line(name, T, font_size=40):
    """VGroup(「w(name)=」, 各列的數字群組)；群組依讀的順序（最下列在前），顏色 ROW_COLORS。"""
    groups = VGroup()
    for k, row in enumerate(reversed(T)):
        g = VGroup(*[Tex(str(v), font_size=font_size, fill_color=ROW_COLORS[k]) for v in row])
        g.arrange(RIGHT, buff=0.16)
        groups.add(g)
    groups.arrange(RIGHT, buff=0.42)
    lab = Tex(f"w({name})=", font_size=font_size)
    groups.next_to(lab, RIGHT, buff=0.25)
    groups.align_to(lab[0], DOWN)                # 數字的底線對齊 w 的底線
    assert tuple(int(v) for row in reversed(T) for v in row) == tableau_word(T)
    return VGroup(lab, groups)


def eq_item(tex, T, cs=0.5, fs=30, font_size=38):
    """「tex」+ 小表，左右排好。"""
    lab = Tex(tex, font_size=font_size)
    d = diagram(T, cs, fs)
    return VGroup(lab, d).arrange(RIGHT, buff=0.3)


# =============================================================================
# 第 1 段：表的字
# =============================================================================
def read_rows(scene, diag, T, line, run_time=0.75):
    """由下往上一列一列塗色，數字飛到字裡；回傳左邊的順序標籤。"""
    tags = VGroup()
    n = len(T)
    scene.play(FadeIn(line[0]), run_time=0.4)
    for k in range(n):
        i = n - 1 - k
        col = ROW_COLORS[k]
        row_cells = VGroup(*[diag.cell(i, j) for j in range(len(T[i]))])
        src = VGroup(*[diag.entry(i, j) for j in range(len(T[i]))])
        tag = Tex(str(k + 1), font_size=28, fill_color=col).next_to(row_cells, LEFT, buff=0.22)
        tags.add(tag)
        scene.play(row_cells.animate.set_fill(col, opacity=0.3), FadeIn(tag),
                   TransformFromCopy(src, line[1][k]), run_time=run_time)
    return tags


def part_word(scene):
    u = diagram(U0, 0.75, 40, top_left=(-5.0, 1.9, 0))
    t = diagram(T0, 0.62, 34, top_left=(0.9, 2.2, 0))
    u_name = Tex("U", font_size=44).next_to(u, UP, buff=0.25)
    t_name = Tex("T", font_size=44).next_to(t, UP, buff=0.25)
    wu = word_line("U", U0)
    wt = word_line("T", T0)
    wu.move_to(np.array([u.get_center()[0], -1.05, 0.0]))
    wt.move_to(np.array([t.get_center()[0], -1.05, 0.0]))
    if wt.get_right()[0] > X_MAX - 0.3:
        wt.shift((X_MAX - 0.3 - wt.get_right()[0]) * RIGHT)
    rule = mixed("列與列之間：由下往上；同一列裡：由左往右", font_size=24, color=MUTED_COLOR)
    rule.move_to(np.array([0.0, -2.2, 0.0]))
    tag_space_u = Rectangle(width=0.5, height=u.get_height()).next_to(u, LEFT, buff=0.0)
    tag_space_t = Rectangle(width=0.5, height=t.get_height()).next_to(t, LEFT, buff=0.0)
    assert_in_frame(u, t, u_name, t_name, wu, wt, rule, tag_space_u, tag_space_t)
    assert_apart(wu, wt, gap=0.4)
    assert_apart(VGroup(u, tag_space_u), VGroup(t, tag_space_t), gap=0.5)
    assert_apart(u, wu, gap=0.3)
    assert_apart(t, wt, gap=0.3)
    assert_apart(VGroup(wu, wt), rule, gap=0.3)

    scene.say("表的「字」：把表攤平成一串數——從最下面一列讀起，每列由左往右")
    scene.play(FadeIn(u), FadeIn(u_name), run_time=0.8)
    read_rows(scene, u, U0, wu, run_time=0.8)
    scene.say("$U$", " 先讀最下列的 2，再讀上一列的 1、3，得到 ", "$w(U)=2\\enspace 1\\enspace 3$")
    scene.wait(1.2)

    scene.say("$T$", " 也一樣：四列由下往上接起來，一共 13 個數")
    scene.play(FadeIn(t), FadeIn(t_name), run_time=0.8)
    read_rows(scene, t, T0, wt, run_time=0.7)
    scene.play(FadeIn(rule, shift=0.15 * UP), run_time=0.6)
    scene.wait(1.6)


# =============================================================================
# 第 2 段：乘積 T·U
# =============================================================================
def cell_point(st, i, j):
    return st["top_left"] + (j + 0.5) * st["cs"] * RIGHT + (i + 0.5) * st["cs"] * DOWN


def new_square(st, i, j):
    sq = Square(side_length=st["cs"], stroke_color=CELL_STROKE, stroke_width=3)
    sq.set_fill(NEW_COLOR, opacity=0.4)
    sq.move_to(cell_point(st, i, j))
    return sq


def animate_insert(scene, st, x, mover, flight_anims=(), step_time=0.5):
    """列插入 st["T"] ← x 的動畫：mover 飛到第 1 列上方，再一列一列擠下去。"""
    steps = bump_steps(st["T"], x)
    T_new, route, new = row_insert(st["T"], x)
    cs = st["cs"]
    assert mover.tab_value == x == steps[0][1]
    above = cell_point(st, *steps[0][0]) + 0.9 * cs * UP
    scene.play(mover.animate.move_to(above).set_fill(ROUTE_COLOR), *flight_anims, run_time=0.7)
    cur = mover
    for (r, c), v, b in steps:
        assert cur.tab_value == v
        target = cell_point(st, r, c)
        if b is None:                       # 停在列尾或新的一列：長出新格子
            sq = new_square(st, r, c)
            st["cells"][(r, c)] = sq
            scene.play(FadeIn(sq), cur.animate.move_to(target).set_fill(WHITE), run_time=step_time)
            st["ents"][(r, c)] = cur
        else:                               # 擠出原來的數，它往下一列走
            old = st["ents"][(r, c)]
            assert old.tab_value == b
            scene.play(cur.animate.move_to(target).set_fill(WHITE),
                       old.animate.move_to(target + 0.5 * cs * (DOWN + RIGHT)).set_fill(ROUTE_COLOR),
                       st["cells"][(r, c)].animate.set_fill(ROUTE_COLOR, opacity=0.35),
                       run_time=step_time)
            st["ents"][(r, c)] = cur
            cur = old
    st["T"] = T_new
    assert set(st["ents"]) == set(young_boxes(shape(T_new))) == set(st["cells"])
    assert all(st["ents"][(i, j)].tab_value == T_new[i][j] for i, j in young_boxes(shape(T_new)))
    assert all(np.allclose(st["ents"][(i, j)].get_center(), cell_point(st, i, j))
               for i, j in young_boxes(shape(T_new)))
    return route, new


def part_product(scene):
    cs = 0.62
    w_top_left = np.array([-6.3, 2.1, 0.0])
    w = diagram(T0, cs, 34, top_left=w_top_left)
    st = {"T": T0, "cs": cs, "top_left": w_top_left,
          "cells": {(i, j): w.cell(i, j) for i, j in young_boxes(shape(T0))},
          "ents": {(i, j): w.entry(i, j) for i, j in young_boxes(shape(T0))}}
    t_mid_y = w.get_center()[1]
    dot = Tex(r"\cdot", font_size=72).move_to(np.array([-2.55, t_mid_y, 0.0]))
    u = diagram(U0, cs, 34)
    u.move_to(np.array([-1.45, t_mid_y, 0.0]))
    for e in list(w.entries) + list(u.entries):     # 被擠出、跨在格線上時仍看得清楚
        e.set_backstroke(BLACK, 4)
    wu = word_line("U", U0, font_size=36)
    wu.next_to(u, DOWN, buff=0.45)
    formula = Tex(r"T\cdot U=((T\leftarrow 2)\leftarrow 1)\leftarrow 3", font_size=40)
    formula.move_to(np.array([3.55, 2.55, 0.0]))
    final_box = Rectangle(width=5 * cs, height=5 * cs).move_to(w_top_left, aligned_edge=UL)   # T·U 的外框
    assert_in_frame(w, dot, u, wu, formula, final_box)
    assert_apart(final_box, dot, gap=0.2)
    assert_apart(final_box, wu, gap=0.2)
    assert_apart(VGroup(u, wu), formula, gap=0.2)

    scene.say("乘積 ", "$T\\cdot U$", "：把 ", "$w(U)$", " 的數，一個接一個列插入 ", "$T$")
    scene.play(FadeIn(w), FadeIn(dot), FadeIn(u), FadeIn(wu), run_time=1.0)
    scene.play(Write(formula), run_time=1.2)
    scene.wait(0.8)

    # U 的格子依 w(U) 的順序（最下列先）
    order = [(i, j) for i in reversed(range(len(U0))) for j in range(len(U0[i]))]
    digits = [d for g in wu[1] for d in g]
    assert tuple(U0[i][j] for i, j in order) == W_U and len(digits) == len(W_U)

    logs = VGroup()
    new_marks = []
    for k, ((i, j), x) in enumerate(zip(order, W_U)):
        n_rows = len(st["T"])
        steps = bump_steps(st["T"], x)
        scene.say(bump_caption(x, steps, n_rows))
        src = u.entry(i, j)
        mover = src.copy()
        mover.tab_value = x
        src.set_opacity(0)
        scene.add(mover)
        route, new = animate_insert(scene, st, x, mover, flight_anims=[
            u.cell(i, j).animate.set_stroke(opacity=0.0),
            digits[k].animate.set_fill(ROUTE_COLOR),
        ])
        assert new == NEW_BOXES[k] and st["T"] == STAGES[k]
        assert not set(route[:-1]) & set(new_marks)            # 綠色的新格子不會被路徑蓋掉
        new_marks.append(new)
        log = mixed(f"$\\leftarrow {x}$", f"：新格子在第 {new[0] + 1} 列，形狀變成 ",
                    f"${tuple_str(shape(st['T']))}$", font_size=24)
        assert shape(st["T"]) == SHAPES[k]
        log.move_to(np.array([0.5, 1.6 - 0.72 * k, 0.0]), aligned_edge=LEFT)
        assert_in_frame(log)
        assert_apart(log, formula, gap=0.2)
        assert_apart(log, VGroup(u, wu), gap=0.2)
        if logs:
            assert_apart(log, logs[-1], gap=0.15)
        logs.add(log)
        scene.play(*[st["cells"][b].animate.set_fill(opacity=0.0) for b in route[:-1]],
                   digits[k].animate.set_fill(GREY_D), FadeIn(log, shift=0.15 * LEFT), run_time=0.6)
        scene.wait(0.9 if k < 2 else 0.6)

    # ---------------------------------------------------- 結果
    assert st["T"] == product(T0, U0)
    final_cells = VGroup(*[st["cells"][b] for b in young_boxes(shape(st["T"]))])
    label = Tex(r"T\cdot U", font_size=44).next_to(final_cells, DOWN, buff=0.3)
    summary = VGroup(
        mixed("格子數：", "$13+3=16$", font_size=26),
        mixed("裡面的數：", "$T$", " 的數和 ", "$U$", " 的數合在一起", font_size=26),
        zh("綠色：每插入一個數，就新長出一格", font_size=24, color=NEW_COLOR),
    ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    summary.move_to(np.array([0.5, -1.3, 0.0]), aligned_edge=LEFT)
    assert_in_frame(label, summary, final_cells)
    assert_apart(summary, logs, gap=0.2)
    assert_apart(label, final_cells, gap=0.1)
    assert_apart(VGroup(final_cells, label), summary, gap=0.3)
    scene.say("$T\\cdot U$", " 有 ", "$13+3=16$", " 格；三個綠格子就是三次插入新長出來的")
    scene.play(FadeOut(dot), FadeOut(u), FadeOut(wu), FadeIn(label, shift=0.15 * UP), run_time=0.7)
    scene.play(LaggedStart(*[FadeIn(s, shift=0.15 * UP) for s in summary], lag_ratio=0.35), run_time=1.3)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：Claim 1（結合律、單位元）
# =============================================================================
def part_assoc(scene):
    stmt = mixed("Claim 1（結合律）：", "$(T\\cdot U)\\cdot V=T\\cdot(U\\cdot V)$", font_size=28)
    stmt.move_to(2.7 * UP)
    factors = VGroup(eq_item("T=", A_T), eq_item("U=", A_U), eq_item("V=", A_V)).arrange(RIGHT, buff=1.1)
    factors.move_to(1.75 * UP)

    lx, rx = -3.6, 3.6
    l1 = eq_item(r"T\cdot U=", A_TU).move_to(np.array([lx, 0.55, 0.0]))
    r1 = eq_item(r"U\cdot V=", A_UV).move_to(np.array([rx, 0.55, 0.0]))
    l2 = mixed("再把 ", "$w(V)=1$", " 插入", font_size=24, color=MUTED_COLOR).move_to(np.array([lx, -0.45, 0.0]))
    r2 = mixed("把 ", "$w(U\\cdot V)=2\\enspace 1\\enspace 1$", " 插入 ", "$T$", font_size=24,
               color=MUTED_COLOR)
    r2.move_to(np.array([rx, -0.45, 0.0]))
    l3 = eq_item(r"(T\cdot U)\cdot V=", A_RES).move_to(np.array([lx, -1.75, 0.0]))
    r3 = eq_item(r"T\cdot(U\cdot V)=", A_RES).move_to(np.array([rx, -1.75, 0.0]))
    eq = Tex("=", font_size=80, fill_color=YELLOW).move_to(np.array([0.0, -1.75, 0.0]))
    boxes = VGroup(SurroundingRectangle(l3[1], buff=0.08, color=OK_COLOR, stroke_width=3),
                   SurroundingRectangle(r3[1], buff=0.08, color=OK_COLOR, stroke_width=3))
    assert_in_frame(stmt, factors, l1, r1, l2, r2, l3, r3, eq, boxes)
    for a, b in [(stmt, factors), (factors, l1), (factors, r1), (l1, l2), (r1, r2), (l2, l3), (r2, r3),
                 (l3, eq), (r3, eq), (VGroup(l1, l2, l3), VGroup(r1, r2, r3)), (boxes[0], eq),
                 (boxes[1], eq), (boxes[0], l3[0]), (boxes[1], r3[0])]:
        assert_apart(a, b, gap=0.15)
    for a, b in zip(factors[:-1], factors[1:]):
        assert_apart(a, b, gap=0.5)

    scene.say("乘積有結合律：先算 ", "$T\\cdot U$", " 再乘 ", "$V$", "，或先算 ", "$U\\cdot V$",
              " 再讓 ", "$T$", " 去乘，結果相同")
    scene.play(FadeIn(stmt), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(f, shift=0.15 * DOWN) for f in factors], lag_ratio=0.25), run_time=1.0)
    scene.play(FadeIn(l1), FadeIn(r1), run_time=0.8)
    scene.play(FadeIn(l2), FadeIn(r2), run_time=0.6)
    scene.play(FadeIn(l3, shift=0.15 * DOWN), FadeIn(r3, shift=0.15 * DOWN), run_time=0.9)
    scene.play(FadeIn(eq, scale=1.4), ShowCreation(boxes), run_time=0.6)
    scene.say("左邊等於把 1、2、1 依序插入 ", "$T$", "，右邊插入的是 2、1、1：順序不同，結果卻一樣")
    scene.wait(2.6)


def part_unit(scene):
    stmt = mixed("單位元：", "$\\varnothing\\cdot U=U\\cdot\\varnothing=U$", font_size=28)
    stmt.move_to(2.7 * UP)
    empty = Tex(r"\varnothing", font_size=60)
    items = [empty] + [diagram(S, 0.6, 34) for S in UNIT_STAGES]
    chain = VGroup(*items).arrange(RIGHT, buff=1.7)
    chain.move_to(np.array([-0.5, 1.15, 0.0]))
    arrows, arrow_labels = VGroup(), VGroup()
    y = chain.get_center()[1]
    for a, b, x in zip(items[:-1], items[1:], W_U):
        arr = Arrow(np.array([a.get_right()[0] + 0.15, y, 0.0]), np.array([b.get_left()[0] - 0.15, y, 0.0]),
                    buff=0.0, thickness=2.5, fill_color=GREY_B)
        lab = zh(f"插入 {x}", font_size=22, color=YELLOW).next_to(arr, UP, buff=0.12)
        arrows.add(arr)
        arrow_labels.add(lab)
    eq_u = Tex("=U", font_size=48, fill_color=OK_COLOR).next_to(items[-1], RIGHT, buff=0.3)
    right_unit = mixed("$U\\cdot\\varnothing$", "：", "$\\varnothing$", " 的字是空的，一個數也不用插入，仍是 ",
                       "$U$", font_size=26)
    right_unit.move_to(np.array([0.0, -0.45, 0.0]))
    block = VGroup(
        mixed("表的乘積有結合律，空表 ", "$\\varnothing$", " 是單位元", font_size=30),
        zh("（換句話說：所有的表在這個乘積之下構成一個么半群）", font_size=22, color=MUTED_COLOR),
    ).arrange(DOWN, buff=0.22)
    box = SurroundingRectangle(block, buff=0.22, color=YELLOW, stroke_width=3)
    VGroup(block, box).move_to(np.array([0.0, -1.95, 0.0]))
    assert_in_frame(stmt, chain, arrows, arrow_labels, eq_u, right_unit, box)
    assert_apart(stmt, VGroup(chain, arrow_labels), gap=0.2)
    assert_apart(VGroup(chain, arrow_labels, eq_u), right_unit, gap=0.3)
    assert_apart(right_unit, box, gap=0.2)
    for lab, d in zip(arrow_labels, items):
        assert_apart(lab, d, gap=0.1)
    for lab, d in zip(arrow_labels, items[1:]):
        assert_apart(lab, d, gap=0.1)

    scene.say("空表是單位元：從空表開始依序插入 ", "$w(U)=2\\enspace 1\\enspace 3$", "，又長回原來的 ", "$U$")
    scene.play(FadeIn(stmt), FadeIn(empty), run_time=0.7)
    for k in range(len(W_U)):
        scene.play(GrowArrow(arrows[k]), FadeIn(arrow_labels[k]), FadeIn(items[k + 1], shift=0.2 * RIGHT),
                   run_time=0.7)
    scene.play(FadeIn(eq_u, scale=1.3), run_time=0.5)
    scene.wait(0.6)
    scene.say("另一邊 ", "$U\\cdot\\varnothing$", " 什麼都不用插入，當然還是 ", "$U$")
    scene.play(FadeIn(right_unit, shift=0.15 * UP), run_time=0.7)
    scene.wait(0.8)
    scene.say("結合律從定義上一點也看不出來：這裡只用例子驗算，書到後面的章節才證明")
    scene.play(FadeIn(block), ShowCreation(box), run_time=0.9)
    scene.wait(2.6)


class SceneF06Product(ChuScene):
    def construct(self):
        self.show_header("表的字與乘積 T·U")
        check_math()
        part_word(self)
        self.clear_stage()
        part_product(self)
        self.clear_stage()
        part_assoc(self)
        self.clear_stage()
        part_unit(self)
        self.wait(1.0)
