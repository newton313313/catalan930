"""
Scene F16 —— 記錄表 Q 與 Robinson–Schensted 對應（Fulton《Young Tableaux》§4.1，書 p.36–38、52、57）

    w = 5 4 8 2 3 4 1 7 5 3 1（CH4_WORD）：P_k = P_{k−1} ← x_k；Q_k = Q_{k−1} 在新格子寫 k（rsk_steps）
        P = ((1,1,3,5),(2,3),(4,4),(5,7),(8,))、Q = ((1,3,6,8),(2,5),(4,9),(7,10),(11,))，Q 是標準表
    倒推：Q 最大的數 k 那一格 → 對 P 反向擠出（reverse_bump），擠出第 1 列的就是 x_k
        k = 11：格子 (5,1)，擠出 1；k = 10：格子 (4,2)，擠出 3；其餘快轉 → 還原 w（inverse_rsk）
    Robinson–Schensted：長 r 的字 ↔ (P, Q)，同形狀、Q 標準
    排列 ↔ 兩個同形狀的標準表：S₃ 依形狀分組 1 + 2² + 1 = 6；4! = 1 + 9 + 4 + 9 + 1 = 24（n! = Σ (f^λ)²）
    習題 17：排列的升降（+/−）由 Q 決定：i+1 在 Q 裡比 i 低 ⇔ 第 i 個位置下降

數字全部由 utils/tableaux.py 算出並 assert（格子 0 起算；字幕裡的列號 1 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF16_rs_correspondence.py SceneF16RS
"""
import sys
from itertools import permutations
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import WordMob, assert_apart, assert_in_frame, tableau_mob, tuple_str, word_tex
from utils.mit_draw import CELL_STROKE
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH4_WORD,
    bump_steps,
    inverse_rsk,
    is_standard,
    partitions,
    reverse_bump,
    row_insert,
    rsk,
    rsk_steps,
    shape,
    standard_tableaux,
    young_boxes,
)

W = CH4_WORD                                       # 5 4 8 2 3 4 1 7 5 3 1（書 p.37）
P_FINAL = ((1, 1, 3, 5), (2, 3), (4, 4), (5, 7), (8,))
Q_FINAL = ((1, 3, 6, 8), (2, 5), (4, 9), (7, 10), (11,))
NEW_BOXES = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2), (3, 0), (0, 3), (2, 1), (3, 1), (4, 0)]
REV_SLOW = [(11, (4, 0), 1), (10, (3, 1), 3)]     # (Q 的數, 格子, 擠出的字母)
N_SLOW = 3

CS = 0.6
P_TL = np.array([-5.6, 1.45, 0.0])
Q_TL = np.array([-1.2, 1.45, 0.0])
ROUTE_COLOR = YELLOW
NEW_COLOR = GREEN
PANEL_X = 2.1


# =============================================================================
# 數學
# =============================================================================
def q_row(Q, k):
    return next(i for i, r in enumerate(Q) for v in r if v == k)


def updown(p):
    return ["+" if a < b else "-" for a, b in zip(p, p[1:])]


def q_updown(Q, n):
    return ["-" if q_row(Q, i + 1) > q_row(Q, i) else "+" for i in range(1, n)]


def perm_groups(n):
    """[(λ, f^λ, [[w(P_a, Q_b) for b] for a]) ...]，依 partitions(n) 的順序；w 由 inverse_rsk 算出。"""
    out = []
    for lam in partitions(n):
        tabs = standard_tableaux(lam)
        grid = [[inverse_rsk(Pa, Qb)[1] for Qb in tabs] for Pa in tabs]
        out.append((lam, len(tabs), grid))
    return out


def check_math():
    steps = rsk_steps(W)
    assert [s[0] for s in steps] == list(range(1, len(W) + 1)) and tuple(s[1] for s in steps) == W
    assert [s[4] for s in steps] == NEW_BOXES
    assert rsk(W) == (P_FINAL, Q_FINAL) and is_standard(Q_FINAL) and shape(P_FINAL) == shape(Q_FINAL)
    assert inverse_rsk(P_FINAL, Q_FINAL) == (tuple(range(1, len(W) + 1)), W)
    P, Q = (), []
    for k, x in enumerate(W, start=1):                 # 每一步的新格子與 Q 的數
        P, _, new = row_insert(P, x)
        assert new == NEW_BOXES[k - 1] and P == steps[k - 1][2]
    # 倒推：Q 最大的數那格反向擠出
    Pk = P_FINAL
    for k in range(len(W), 0, -1):
        box = NEW_BOXES[k - 1]
        assert Q_FINAL[box[0]][box[1]] == k
        Pk, x, _ = reverse_bump(Pk, box)
        assert x == W[k - 1] and Pk == (steps[k - 2][2] if k > 1 else ())
    for k, box, x in REV_SLOW:
        assert NEW_BOXES[k - 1] == box and W[k - 1] == x
    # 排列 ↔ 兩個標準表
    for n in (3, 4):
        groups = perm_groups(n)
        perms = [w for _, _, g in groups for row in g for w in row]
        assert sorted(perms) == sorted(permutations(range(1, n + 1)))
        assert sum(f * f for _, f, _ in groups) == factorial(n) == len(perms)
        for lam, f, g in groups:
            tabs = standard_tableaux(lam)
            for a, row in enumerate(g):
                for b, w in enumerate(row):
                    P_, Q_ = rsk(w)
                    assert (P_, Q_) == (tabs[a], tabs[b]) and is_standard(P_)
        for w in permutations(range(1, n + 1)):          # 習題 17
            assert updown(w) == q_updown(rsk(w)[1], n)
    assert [f for _, f, _ in perm_groups(3)] == [1, 2, 1]
    assert [f for _, f, _ in perm_groups(4)] == [1, 3, 2, 3, 1]


# =============================================================================
# 列插入／反向擠出的動畫（同 F06 的做法，P 從空表開始長）
# =============================================================================
def cell_point(st, i, j):
    return st["tl"] + (j + 0.5) * CS * RIGHT + (i + 0.5) * CS * DOWN


def new_square(st, i, j, color=NEW_COLOR, opacity=0.4):
    sq = Square(side_length=CS, stroke_color=CELL_STROKE, stroke_width=3).set_fill(color, opacity=opacity)
    return sq.move_to(cell_point(st, i, j))


def insert_anims(scene, st, x, mover, step_time, flight_time, extra=()):
    """列插入 st["T"] ← x：mover 飛到第 1 列上方，再一列一列擠下去。回傳新格子。"""
    steps = bump_steps(st["T"], x)
    T_new, _, new = row_insert(st["T"], x)
    above = cell_point(st, *steps[0][0]) + 0.85 * CS * UP
    scene.play(mover.animate.move_to(above).set_fill(ROUTE_COLOR), *extra, run_time=flight_time)
    cur = mover
    for (r, c), v, b in steps:
        assert cur.tab_value == v
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
                       old.animate.move_to(target + 0.5 * CS * (DOWN + RIGHT)).set_fill(ROUTE_COLOR),
                       run_time=step_time)
            st["ents"][(r, c)] = cur
            cur = old
    st["T"] = T_new
    check_state(st)
    return new


def reverse_anims(scene, st, box, dest, step_time, flight_time, extra=()):
    """反向擠出：從格子 box 的數往上擠，最後擠出第 1 列的數飛到 dest。回傳 (那個數的物件, 數)。"""
    T0, x, route = reverse_bump(st["T"], box)
    cur = st["ents"].pop(box)
    cell = st["cells"].pop(box)
    scene.play(cur.animate.set_fill(ROUTE_COLOR), FadeOut(cell), *extra, run_time=step_time)
    for r, c in reversed(route[:-1]):
        old = st["ents"][(r, c)]
        target = cell_point(st, r, c)
        scene.play(cur.animate.move_to(target).set_fill(WHITE),
                   old.animate.move_to(target + 0.5 * CS * (UP + LEFT)).set_fill(ROUTE_COLOR),
                   run_time=step_time)
        st["ents"][(r, c)] = cur
        cur = old
    assert cur.tab_value == x
    scene.play(cur.animate.move_to(dest), run_time=flight_time)
    st["T"] = T0
    check_state(st)
    return cur, x


def check_state(st):
    boxes = set(young_boxes(shape(st["T"]))) if st["T"] else set()
    assert set(st["ents"]) == boxes == set(st["cells"])
    assert all(st["ents"][(i, j)].tab_value == st["T"][i][j] for i, j in boxes)
    assert all(np.allclose(st["ents"][(i, j)].get_center(), cell_point(st, i, j)) for i, j in boxes)


def dim(tile):
    return [tile.square.animate.set_stroke(opacity=0.3).set_fill(opacity=0.04), tile.label.animate.set_fill(opacity=0.3)]


def relight(tile):
    return [tile.square.animate.set_stroke(opacity=1.0).set_fill(opacity=0.15), tile.label.animate.set_fill(opacity=1.0)]


def step_caption(k, x, steps):
    parts = [f"{v} 擠出 {b}" for _, v, b in steps if b is not None]
    (r, _), _, _ = steps[-1]
    return f"第 {k} 步插入 {x}：" + "，".join(parts + [f"新格子在第 {r + 1} 列"]) + f"；Q 那格寫 {k}"


# =============================================================================
# 第 1 段：P 與記錄表 Q
# =============================================================================
def part_record(scene):
    word = WordMob(W, size=0.55, center=np.array([0.0, 2.4, 0.0]))
    wlab = Tex("w=", font_size=40).next_to(word, LEFT, buff=0.25)
    idx = VGroup(*[Tex(str(k + 1), font_size=22, fill_color=MUTED_COLOR).next_to(t, UP, buff=0.1)
                   for k, t in enumerate(word.tiles)])
    final_p = tableau_mob(P_FINAL, cs=CS, top_left=P_TL)
    final_q = tableau_mob(Q_FINAL, cs=CS, top_left=Q_TL)
    plab = Tex("P", font_size=44).next_to(final_p.cell(0, 0), LEFT, buff=0.3)
    qlab = Tex("Q", font_size=44).next_to(final_q.cell(0, 0), LEFT, buff=0.3)
    r1 = Tex(r"P_k=P_{k-1}\leftarrow x_k", font_size=36)
    r2 = mixed("$Q_k$", "：新格子寫上 ", "$k$", font_size=26)
    r3 = mixed("$Q$", f" 是標準表：", f"$1,\\dots,{len(W)}$", " 各一次", font_size=26)
    panel = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    panel.move_to(np.array([PANEL_X, 0.55, 0.0]), aligned_edge=LEFT)
    bump_room = Rectangle(width=4 * CS + 0.5 * CS, height=5 * CS + 0.5 * CS).move_to(P_TL, aligned_edge=UL)
    assert_in_frame(word, wlab, idx, final_p, final_q, plab, qlab, panel, bump_room)
    assert_apart(VGroup(word, idx), VGroup(final_p, final_q, plab, qlab), gap=0.25)
    assert_apart(bump_room, VGroup(final_q, qlab), gap=0.15)
    assert_apart(final_q, panel, gap=0.4)

    scene.say("記錄表 ", "$Q$", "：把 ", "$w$", " 依序列插入得到 ", "$P$", "，同時記下每一步長出哪一格")
    scene.play(FadeIn(wlab), FadeIn(word), FadeIn(idx), FadeIn(plab), FadeIn(qlab), run_time=0.9)
    scene.play(FadeIn(r1), FadeIn(r2), run_time=0.6)
    scene.wait(0.8)

    sp = {"T": (), "tl": P_TL, "cells": {}, "ents": {}}
    sq = {"T": (), "tl": Q_TL, "cells": {}, "ents": {}}
    last_new = []
    for k, (u, x, P_k, Q_k, new) in enumerate(rsk_steps(W), start=1):
        slow = k <= N_SLOW
        steps = bump_steps(sp["T"], x)
        if slow:
            scene.say(step_caption(k, x, steps))
        elif k == N_SLOW + 1:
            scene.say("後面照做：", "$P$", " 照常列插入，", "$Q$", " 只記「第幾步長出哪一格」")
        tile = word.tiles[k - 1]
        mover = tile.label.copy().scale(CS / word.size)
        mover.tab_value = x
        scene.add(mover)
        fade_old = [m.animate.set_fill(opacity=0.0) for m in last_new]
        got = insert_anims(scene, sp, x, mover, step_time=0.45 if slow else 0.18, flight_time=0.6 if slow else 0.28,
                           extra=dim(tile) + [idx[k - 1].animate.set_fill(YELLOW)] + fade_old)
        assert got == new and sp["T"] == P_k
        qsq = new_square(sq, *new)
        num = idx[k - 1].copy()
        num.tab_value = k
        scene.add(num)
        scene.play(FadeIn(qsq), num.animate.scale(1.5).move_to(cell_point(sq, *new)).set_fill(WHITE),
                   idx[k - 1].animate.set_fill(MUTED_COLOR), run_time=0.5 if slow else 0.25)
        sq["cells"][new], sq["ents"][new] = qsq, num
        sq["T"] = Q_k
        check_state(sq)
        last_new = [sp["cells"][new], qsq]
        if slow:
            scene.wait(0.6)
    assert sp["T"] == P_FINAL and sq["T"] == Q_FINAL
    assert all(np.allclose(sp["ents"][b].get_center(), final_p.entry(*b).get_center()) for b in sp["ents"])
    assert all(np.allclose(sq["ents"][b].get_center(), final_q.entry(*b).get_center()) for b in sq["ents"])
    scene.say("$Q$", " 的數每列往右、每行往下都遞增，而且 ", f"$1,\\dots,{len(W)}$", " 各出現一次：標準表")
    scene.play(*[m.animate.set_fill(opacity=0.0) for m in last_new], FadeIn(r3, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)
    return word, idx, sp, sq


# =============================================================================
# 第 2 段：倒推
# =============================================================================
def part_inverse(scene, word, idx, sp, sq):
    r4 = mixed("倒推：", "$Q$", " 最大的數那一格", font_size=26, color=YELLOW)
    r5 = mixed("對 ", "$P$", " 反向擠出", "$\\Rightarrow x_k$", font_size=26, color=YELLOW)
    rev = VGroup(r4, r5).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    rev.move_to(np.array([PANEL_X, -1.55, 0.0]), aligned_edge=LEFT)
    assert_in_frame(rev)

    k0, box0, x0 = REV_SLOW[0]
    scene.say("反過來：", "$Q$", f" 最大的數 {k0} 在哪一格，就從 ", "$P$", " 的同一格反向擠出")
    scene.play(FadeIn(rev, shift=0.1 * UP), run_time=0.6)
    scene.wait(0.6)
    recovered = []
    for k in range(len(W), 0, -1):
        slow = k > len(W) - len(REV_SLOW)
        box = NEW_BOXES[k - 1]
        qcell, qnum = sq["cells"].pop(box), sq["ents"].pop(box)
        assert qnum.tab_value == k
        if slow:
            _, b, x = REV_SLOW[len(W) - k]
            assert b == box
            if k != k0:
                scene.say("接著 ", "$Q$", f" 最大的是 {k}，在第 {box[0] + 1} 列：同樣從 ", "$P$", " 的那一格反向擠出")
            scene.play(qcell.animate.set_fill(YELLOW, opacity=0.5), sp["cells"][box].animate.set_fill(YELLOW, opacity=0.35),
                       run_time=0.5)
        elif k == len(W) - len(REV_SLOW):
            scene.say("一步一步倒回去：擠出來的數，依序是 ", "$w$", " 從右邊數回來的字母")
        tile = word.tiles[k - 1]
        mob, x = reverse_anims(scene, sp, box, tile.get_center(), step_time=0.4 if slow else 0.12,
                               flight_time=0.6 if slow else 0.25, extra=[FadeOut(qcell), FadeOut(qnum)])
        assert x == W[k - 1]
        scene.play(FadeOut(mob), *relight(tile), idx[k - 1].animate.set_fill(YELLOW), run_time=0.35 if slow else 0.15)
        recovered.append(x)
        if slow:
            scene.say(f"從第 {box[0] + 1} 列一路往上擠，最後擠出第 1 列的 {x}：它就是 ", f"$x_{{{k}}}={x}$")
            scene.wait(1.4)
    assert tuple(reversed(recovered)) == W and sp["T"] == () and not sq["ents"]
    scene.say("$w$", " 完整還原：", "$(P,Q)$", " 記下了 ", "$w$", " 的全部資訊")
    scene.play(*[m.animate.set_fill(MUTED_COLOR) for m in idx], run_time=0.5)
    scene.wait(1.6)


# =============================================================================
# 第 3 段：Robinson–Schensted 對應
# =============================================================================
def part_statement(scene):
    big = Tex(r"w\ \longleftrightarrow\ (P,Q)", font_size=64)
    big.move_to(np.array([0.0, 1.5, 0.0]))
    l1 = mixed("$w$", "：長度 ", "$r$", " 的字", font_size=28)
    l2 = mixed("$P$", "：一個表；", "$Q$", "：同形狀的標準表（", "$1,\\dots,r$", " 各一次）", font_size=28)
    l3 = zh("任何這樣的一對都恰好來自一個字：標準表最大的數一定在外角，倒推永遠做得下去",
            font_size=22, color=MUTED_COLOR)
    lines = VGroup(l1, l2, l3).arrange(DOWN, buff=0.35).move_to(np.array([0.0, -0.75, 0.0]))
    box = SurroundingRectangle(big, buff=0.3, color=YELLOW, stroke_width=3)
    assert_in_frame(big, box, lines)
    assert_apart(box, lines, gap=0.3)

    scene.say("Robinson–Schensted 對應：字與「一對同形狀的表、", "$Q$", " 標準」一一對應")
    scene.play(Write(big), ShowCreation(box), run_time=1.2)
    scene.play(LaggedStart(*[FadeIn(m, shift=0.1 * UP) for m in lines[:2]], lag_ratio=0.4), run_time=1.0)
    scene.wait(1.2)
    scene.say("反方向也成立：任給這樣的一對，倒推都能做完，得到唯一的字")
    scene.play(FadeIn(l3, shift=0.1 * UP), run_time=0.6)
    scene.wait(2.0)


# =============================================================================
# 第 4 段：排列 ↔ 兩個標準表；n! = Σ (f^λ)²；習題 17
# =============================================================================
def perm_item(w, cs=0.42):
    P_, Q_ = rsk(w)
    word = word_tex(w, font_size=36)
    pair = VGroup(tableau_mob(P_, cs=cs), tableau_mob(Q_, cs=cs)).arrange(RIGHT, buff=0.22, aligned_edge=UP)
    item = VGroup(word, pair).arrange(DOWN, buff=0.18)
    signs = Tex(r"\,".join("{" + s + "}" for s in updown(w)), font_size=30)
    for g, s in zip(signs, updown(w)):
        g.set_fill(RED_B if s == "-" else TEAL_B)
    item.signs = signs                              # 排好版面之後再放到字的右邊
    return item


def part_permutations(scene):
    title = mixed("排列 ", "$w\\in S_3$", "：", "$P$", "、", "$Q$", " 都是標準表（每格下面左 ", "$P$", "、右 ",
                  "$Q$", "）", font_size=26)
    title.move_to(np.array([0.0, 2.8, 0.0]))
    groups = perm_groups(3)
    cols, labels, squares = VGroup(), VGroup(), VGroup()
    items = []
    for lam, f, grid in groups:
        rows = VGroup()
        for row in grid:
            its = [perm_item(w) for w in row]
            items += its
            rows.add(VGroup(*its).arrange(RIGHT, buff=0.7, aligned_edge=UP))
        rows.arrange(DOWN, buff=0.35)
        cols.add(rows)
    cols.arrange(RIGHT, buff=1.4).move_to(np.array([0.0, 0.3, 0.0]))
    for (lam, f, _), col in zip(groups, cols):
        labels.add(Tex(f"\\lambda={tuple_str(lam)}", font_size=32).move_to(np.array([col.get_x(), 2.2, 0.0])))
        squares.add(Tex(f"(f^\\lambda)^2={f}^2={f * f}", font_size=32).move_to(np.array([col.get_x(), -1.62, 0.0])))
    f3 = [f for _, f, _ in groups]
    f4 = [f for _, f, _ in perm_groups(4)]
    sum3 = Tex("3!=" + "+".join(f"{f}^2" for f in f3) + f"={factorial(3)}", font_size=40)
    sum4 = Tex("4!=" + "+".join(f"{f}^2" for f in f4) + f"={factorial(4)}", font_size=40)
    VGroup(sum3, sum4).arrange(RIGHT, buff=1.2).move_to(np.array([0.0, -2.45, 0.0]))
    for it in items:
        it.signs.next_to(it[0], RIGHT, buff=0.25)
    signs = VGroup(*[it.signs for it in items])
    assert sum(f * f for f in f3) == factorial(3) and sum(f * f for f in f4) == factorial(4)
    assert_in_frame(title, cols, labels, squares, sum3, sum4, signs)
    assert_apart(title, labels, gap=0.15)
    assert_apart(labels, cols, gap=0.1)
    assert_apart(cols, squares, gap=0.15)
    assert_apart(squares, VGroup(sum3, sum4), gap=0.2)
    for a, b in zip(cols[:-1], cols[1:]):
        assert_apart(a, b, gap=0.5)
    for it in items:
        for other in items:
            if other is not it:
                assert_apart(it.signs, other, gap=0.08)

    scene.say("$w$", " 是排列時（1 到 ", "$n$", " 各一次），", "$P$", " 也是標準表：", "$S_3$", f" 的 {len(items)} 個排列")
    scene.play(FadeIn(title), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(it, shift=0.1 * DOWN) for it in items], lag_ratio=0.15), run_time=1.6)
    scene.wait(0.6)
    scene.say("依形狀分組：形狀 ", "$\\lambda$", " 的標準表有 ", "$f^\\lambda$", " 個，所以有 ", "$(f^\\lambda)^2$",
              " 對")
    scene.play(FadeIn(labels), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(s, shift=0.1 * UP) for s in squares], lag_ratio=0.3), run_time=1.0)
    scene.wait(1.0)
    scene.say("$n!=\\sum_\\lambda (f^\\lambda)^2$", "：", "$n=3$", f" 是 {factorial(3)}，", "$n=4$",
              f" 是 {factorial(4)}")
    scene.play(Write(sum3), run_time=0.9)
    scene.play(Write(sum4), run_time=1.1)
    scene.wait(1.4)
    scene.say("習題 17：排列的升降（", "$+$", "、", "$-$", "）只看 ", "$Q$", "：", "$i+1$", " 在 ", "$i$",
              " 的下面一列以下就是 ", "$-$")
    scene.play(LaggedStart(*[FadeIn(s, shift=0.1 * LEFT) for s in signs], lag_ratio=0.1), run_time=1.2)
    scene.wait(2.4)


class SceneF16RS(ChuScene):
    def construct(self):
        self.show_header("記錄表 Q 與 Robinson–Schensted 對應")
        check_math()
        word, idx, sp, sq = part_record(self)
        part_inverse(self, word, idx, sp, sq)
        self.clear_stage()
        part_statement(self)
        self.clear_stage()
        part_permutations(self)
        self.wait(1.0)
