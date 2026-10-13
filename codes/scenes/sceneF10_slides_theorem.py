"""
Scene F10 —— 滑動保持 Knuth 等價、主定理、兩個推論、plactic monoid（Fulton《Young Tableaux》§2.1，書 p.20–24）

    (1) 滑動的每一步都保持字的 Knuth 等價類（書 p.20–22）。從 S = [[·,1,4],[2,3,5]] 的內角滑一次：
          1 往左（水平，字不變）→ CH2_SLIDE_BEFORE = u ∘ y / v x z（u,v,x,y,z = 1..5）
          3 往上（垂直）→ CH2_SLIDE_AFTER，字 v x z u y = 23514 → v z u x y = 25134，
            用 CH2_SLIDE_CHAIN 的四步基本變換（書上的規則 K''⁻¹、K'、K''、K''，由 knuth_moves 查證）
          5 往左（水平，字不變），洞到外角拿掉
        一般情形：u, v, y, z 換成整段的列，對列長歸納（每步用一次命題 1）→ 命題 2
    (2) 主定理：每個字恰與一個表的字 Knuth 等價。存在：P(w) = (…(x₁←x₂)…)←x_r，
        例 CH3_WORD → CH3_TABLEAU（快速播放），w(P(w)) = CH3_WORD2；唯一性第 3 章證
    (3) 推論 1：Rect(S) = 唯一與 w(S) 等價的表（FULTON_SKEW：rectify 與 insert_word(w(S)) 相同）
    (4) 推論 2：T·U 的三種做法（列插入、Rect(T∗U)、P(w(T)w(U))）相同（FULTON_INSERT_T、FULTON_PRODUCT_U）
    (5) Plactic monoid：字的連接 ↔ 表的乘積；表環 R[m] → ℤ[x₁,…,x_m]，T ↦ x^T

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算）。

執行（在 codes/ 資料夾內；要平行渲染請用 combkit/tools/render_check.py）：
    manimgl scenes/sceneF10_slides_theorem.py SceneF10SlidesTheorem
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import (
    HOLE_COLOR,
    MU_COLOR,
    RULE_COLORS,
    RULE_TEX,
    SkewMob,
    WordMob,
    assert_apart,
    assert_in_frame,
    tableau_mob,
    word_tex,
)
from utils.mit_draw import CELL_STROKE
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH2_SLIDE_AFTER,
    CH2_SLIDE_BEFORE,
    CH2_SLIDE_CHAIN,
    CH3_TABLEAU,
    CH3_WORD,
    CH3_WORD2,
    FULTON_INSERT_T,
    FULTON_PRODUCT_U,
    FULTON_SKEW,
    content,
    forward_slide,
    insert_word,
    insert_word_steps,
    is_tableau,
    knuth_moves,
    knuth_path,
    product,
    rectify,
    star,
    tableau_word,
)

S_START = ((None, 1, 4), (2, 3, 5))       # 從內角 (0,0) 滑一次，途中正好經過 CH2_SLIDE_BEFORE、AFTER
CORNER = (0, 0)
SLIDE_END = ((1, 3, 4), (2, 5))
LETTER = {1: "u", 2: "v", 3: "x", 4: "y", 5: "z"}                    # 書 p.20：u < v < x < y < z
BOOK_MOVES = ((2, "K''⁻¹"), (0, "K'"), (2, "K''"), (1, "K''"))       # 書 p.20 的四步
T0, U0 = FULTON_INSERT_T, FULTON_PRODUCT_U
TU = ((1, 1, 2, 2, 3), (2, 2, 3, 5), (3, 4, 5), (4, 6, 6), (5,))
RECT_S = ((2, 2, 2, 4, 6), (3, 4, 6), (5, 5))
M = 6                                                                 # 字母表 [m]，m = 6


def cells_to_rows(cells):
    rows = sorted({i for i, _ in cells})
    return tuple(tuple(cells[(i, j)] for j in range(max(j for a, j in cells if a == i) + 1)) for i in rows)


def slide_states(S, corner):
    """一次滑動：[(狀態, 洞)]（洞與 μ 都是 None）、每步 (src, dst)、結果。"""
    out, path = forward_slide(S, corner)
    cells = {(i, j): v for i, row in enumerate(S) for j, v in enumerate(row)}
    states, moves = [(S, path[0])], []
    for dst, src in zip(path, path[1:]):
        cells[dst], cells[src] = cells[src], None
        moves.append((src, dst))
        states.append((cells_to_rows(cells), src))
    del cells[path[-1]]
    assert cells_to_rows(cells) == out
    return states, moves, out


def letters(w):
    return "".join(LETTER[a] for a in w)


def ltex(w):
    """字母版的字（Tex）。"""
    return r"\,".join(letters(w))


def rule_condition(rule, triple):
    """基本變換成立的條件（書 p.19），回傳 (左, 關係, 中, 關係, 右)。"""
    a, b, c = triple
    if rule == "K'":                          # y z x：x < y ≤ z
        return c, "<", a, r"\le", b
    if rule == "K'⁻¹":                        # y x z
        return b, "<", a, r"\le", c
    if rule == "K''":                         # x z y：x ≤ y < z
        return a, r"\le", c, "<", b
    return b, r"\le", c, "<", a               # K''⁻¹：z x y


def insertion_tex(w):
    """((T ← w1) ← w2) ← …"""
    s = "T"
    for k, x in enumerate(w):
        s = (s if k == 0 else "(" + s + ")") + r"\leftarrow " + str(x)
    return s


def monomial(c):
    return "".join(f"x_{i}" + (f"^{{{e}}}" if e > 1 else "") for i, e in enumerate(c, 1) if e)


def check_math():
    states, moves, out = slide_states(S_START, CORNER)
    assert out == SLIDE_END and is_tableau(SLIDE_END) and len(moves) == 3
    assert states[1][0] == CH2_SLIDE_BEFORE and states[2][0] == CH2_SLIDE_AFTER
    assert [s[0] == d[0] for s, d in moves] == [True, False, True]             # 水平、垂直、水平
    words = [tableau_word(st) for st, _ in states]
    assert words[0] == words[1] == CH2_SLIDE_CHAIN[0] and words[2] == words[3] == CH2_SLIDE_CHAIN[-1]
    assert letters(CH2_SLIDE_CHAIN[0]) == "vxzuy" and letters(CH2_SLIDE_CHAIN[-1]) == "vzuxy"
    hi, hj = states[1][1]
    right, below = CH2_SLIDE_BEFORE[hi][hj + 1], CH2_SLIDE_BEFORE[hi + 1][hj]
    assert below < right and moves[1] == ((hi + 1, hj), (hi, hj))
    for (i, rule), a, b in zip(BOOK_MOVES, CH2_SLIDE_CHAIN, CH2_SLIDE_CHAIN[1:]):
        assert (i, rule, b) in knuth_moves(a)
        l, o1, m, o2, r = rule_condition(rule, a[i:i + 3])
        assert (l < m if o1 == "<" else l <= m) and (m < r if o2 == "<" else m <= r)
    assert len(knuth_path(CH2_SLIDE_CHAIN[0], CH2_SLIDE_CHAIN[-1])) == len(BOOK_MOVES)
    # 主定理的例子
    steps = insert_word_steps(CH3_WORD)
    assert len(steps) == len(CH3_WORD) == 12 and steps[-1][1] == CH3_TABLEAU == insert_word(CH3_WORD)
    assert tableau_word(CH3_TABLEAU) == CH3_WORD2 != CH3_WORD
    # 推論 1、2
    assert rectify(FULTON_SKEW) == RECT_S == insert_word(tableau_word(FULTON_SKEW)) and is_tableau(RECT_S)
    assert product(T0, U0) == TU == rectify(star(T0, U0)) == insert_word(tableau_word(T0) + tableau_word(U0))
    assert insertion_tex(tableau_word(U0)) == r"((T\leftarrow 2)\leftarrow 1)\leftarrow 3"
    # 表環：x^{T·U} = x^T x^U；乘積不交換
    assert content(TU, M) == tuple(a + b for a, b in zip(content(T0, M), content(U0, M)))
    assert max(max(r) for r in TU) == M
    assert product(((1,),), ((2,),)) != product(((2,),), ((1,),))


# =============================================================================
# 第 1 段：滑動保持 Knuth 等價
# =============================================================================
def cell_pos(board, i, j):
    cs = board["cs"]
    return board["origin"] + (j + 0.5) * cs * RIGHT + (i + 0.5) * cs * DOWN


def make_board(S, cs, top_left, fs):
    """有洞的斜表（μ 灰格）；每個數的右下角標上書裡的字母。"""
    board = {"cs": cs, "origin": np.array(top_left, dtype=float), "cells": {}, "nums": {}, "vals": {},
             "hole": None}
    for i, row in enumerate(S):
        for j, v in enumerate(row):
            sq = Square(side_length=cs, stroke_color=CELL_STROKE, stroke_width=3)
            sq.set_fill(MU_COLOR, opacity=0.35 if v is None else 0.0)
            board["cells"][(i, j)] = sq.move_to(cell_pos(board, i, j))
            if v is not None:
                num = Tex(str(v), font_size=fs).move_to(cell_pos(board, i, j))
                tag = Tex(LETTER[v], font_size=fs * 0.55, fill_color=MUTED_COLOR)
                tag.move_to(cell_pos(board, i, j) + 0.3 * cs * (RIGHT + DOWN))
                board["nums"][(i, j)] = VGroup(num, tag).set_z_index(2)
                board["vals"][(i, j)] = v
    return board


def board_group(board):
    return VGroup(*board["cells"].values(), *board["nums"].values())


def board_state(board):
    return cells_to_rows({b: board["vals"].get(b) for b in board["cells"]})


def open_hole(board, corner):
    hole = Square(side_length=board["cs"] * 0.86, stroke_color=HOLE_COLOR, stroke_width=5)
    hole.set_fill(HOLE_COLOR, opacity=0.2).move_to(cell_pos(board, *corner)).set_z_index(1)
    board["hole"] = hole
    return [board["cells"][corner].animate.set_fill(opacity=0.0), FadeIn(hole, scale=0.5)]


def slide_move(board, src, dst):
    num = board["nums"].pop(src)
    board["nums"][dst] = num
    board["vals"][dst] = board["vals"].pop(src)
    return [num.animate.shift(cell_pos(board, *dst) - cell_pos(board, *src)),
            board["hole"].animate.move_to(cell_pos(board, *src))]


def drop_hole(board, at):
    cell, hole = board["cells"].pop(at), board["hole"]
    board["hole"] = None
    return [FadeOut(cell, scale=0.4), FadeOut(hole, scale=0.4)]


def part_slides(scene):
    states, moves, out = slide_states(S_START, CORNER)
    board = make_board(S_START, 0.9, (-6.2, 2.35, 0.0), fs=44)
    bg = board_group(board)
    wm = WordMob(CH2_SLIDE_CHAIN[0], size=0.6, center=np.array([2.6, 2.3, 0.0]))
    w_lab = Tex("w=", font_size=40).next_to(wm, LEFT, buff=0.25)
    probe = wm.bracket(0, 3, RULE_TEX["K''⁻¹"])
    log = VGroup()
    for k, w in enumerate(CH2_SLIDE_CHAIN):
        y = 0.95 - 0.55 * k
        item = VGroup(Tex(ltex(w), font_size=34).move_to(np.array([0.9, y, 0.0]), aligned_edge=LEFT))
        if k:
            i, rule = BOOK_MOVES[k - 1]
            l, o1, m, o2, r = rule_condition(rule, CH2_SLIDE_CHAIN[k - 1][i:i + 3])
            cond = Tex(f"{RULE_TEX[rule]}:\\ {LETTER[l]} {o1} {LETTER[m]} {o2} {LETTER[r]}", font_size=30,
                       fill_color=RULE_COLORS[rule])
            item.add(Tex(r"\equiv", font_size=34).next_to(item[0], LEFT, buff=0.2),
                     cond.move_to(np.array([3.0, y, 0.0]), aligned_edge=LEFT))
        log.add(item)
    notes = VGroup()
    for k, (src, dst) in enumerate(moves):
        val = states[k][0][src[0]][src[1]]
        flat = src[0] == dst[0]
        same = tableau_word(states[k][0]) == tableau_word(states[k + 1][0])
        txt = f"{val} {'往左：水平' if flat else '往上：垂直'}滑動，字{'不變' if same else '改變'}"
        notes.add(zh(txt, font_size=24, color=OK_COLOR if same else YELLOW))
    notes.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(np.array([-6.2, -0.45, 0.0]), aligned_edge=LEFT)
    prop2 = mixed("命題 2：用一連串滑動互相得到的斜表，它們的字 Knuth 等價", font_size=26)
    prop2_box = SurroundingRectangle(prop2, buff=0.18, color=YELLOW, stroke_width=3)
    prop2_g = VGroup(prop2, prop2_box).move_to(np.array([0.0, -2.3, 0.0]))
    assert_in_frame(bg, wm, w_lab, probe, log, notes, prop2_g)
    assert_apart(bg, notes, gap=0.3)
    assert_apart(VGroup(bg, notes), VGroup(w_lab, log), gap=0.4)
    assert_apart(VGroup(wm, probe), log, gap=0.15)
    assert_apart(VGroup(log, notes), prop2_g, gap=0.2)
    hi, hj = states[1][1]
    right, below = CH2_SLIDE_BEFORE[hi][hj + 1], CH2_SLIDE_BEFORE[hi + 1][hj]

    scene.say("滑動時會出現「有洞」的表；字照樣讀：由下往上、由左往右，跳過洞")
    scene.play(FadeIn(bg), FadeIn(w_lab), FadeIn(wm), run_time=0.8)
    scene.wait(1.4)
    (src, dst) = moves[0]
    scene.say(f"從內角開一個洞：{board['vals'][src]} 往左滑進洞。水平移動，字完全沒變")
    scene.play(*open_hole(board, CORNER), run_time=0.5)
    scene.play(*slide_move(board, src, dst), run_time=0.6)
    assert board_state(board) == states[1][0] == CH2_SLIDE_BEFORE
    scene.play(FadeIn(notes[0]), Indicate(wm, scale_factor=1.05), run_time=0.8)
    scene.wait(0.8)
    (src, dst) = moves[1]
    scene.say(f"洞的右邊是 {right}、下面是 {below}：較小的 {below} 往上滑，這是垂直移動")
    scene.play(*slide_move(board, src, dst), run_time=0.7)
    assert board_state(board) == states[2][0] == CH2_SLIDE_AFTER
    scene.play(FadeIn(notes[1]), run_time=0.4)
    scene.wait(0.6)
    scene.say("字從 ", "$" + ltex(CH2_SLIDE_CHAIN[0]) + "$", " 變成 ", "$" + ltex(CH2_SLIDE_CHAIN[-1]) + "$",
              f"：用 {len(BOOK_MOVES)} 次基本變換就到得了")
    scene.play(FadeIn(log[0]), run_time=0.5)
    for k, (i, rule) in enumerate(BOOK_MOVES):
        assert wm.apply_move(scene, i, rule, run_time=0.5, hold=0.1) == CH2_SLIDE_CHAIN[k + 1]
        scene.play(FadeIn(log[k + 1], shift=0.1 * LEFT), run_time=0.35)
    scene.wait(1.0)
    (src, dst) = moves[2]
    scene.say(f"最後 {board['vals'][src]} 往左滑（水平），洞到了外角就拿掉；字又沒變")
    scene.play(*slide_move(board, src, dst), run_time=0.6)
    scene.play(*drop_hole(board, src), FadeIn(notes[2]), run_time=0.5)
    assert board_state(board) == out
    scene.wait(0.8)
    scene.say("一般情形把 ", "$u,v,y,z$", " 換成整段的列，對列長歸納，每一步用一次命題 1")
    scene.play(FadeIn(prop2_g, shift=0.1 * UP), run_time=0.7)
    scene.wait(2.0)


# =============================================================================
# 第 2 段：主定理（存在性）
# =============================================================================
def part_theorem(scene):
    thm = mixed("定理：每個字都恰好與一個表的字 Knuth 等價", font_size=30)
    thm_box = SurroundingRectangle(thm, buff=0.18, color=YELLOW, stroke_width=3)
    thm_g = VGroup(thm, thm_box).move_to(np.array([0.0, 2.55, 0.0]))
    pdef = Tex(r"P(w)=(\cdots((x_1\leftarrow x_2)\leftarrow x_3)\leftarrow\cdots)\leftarrow x_r", font_size=34)
    pdef.move_to(np.array([0.0, 1.6, 0.0]))
    wt = word_tex(CH3_WORD, font_size=40)
    wrow = VGroup(Tex("w=", font_size=40), wt).arrange(RIGHT, buff=0.2).move_to(np.array([0.0, 0.75, 0.0]))
    steps = insert_word_steps(CH3_WORD)
    tl = np.array([-1.5, 0.2, 0.0])
    stages = [tableau_mob(Tk, cs=0.5, top_left=tl) for _, Tk, _, _ in steps]
    final = stages[-1]
    p_lab = Tex("P(w)=", font_size=38).next_to(final, LEFT, buff=0.3)
    wp = VGroup(Tex("w(P(w))=", font_size=36), word_tex(CH3_WORD2, font_size=36), Tex(r"\equiv w", font_size=36))
    wp.arrange(RIGHT, buff=0.2).move_to(np.array([0.0, -2.0, 0.0]))
    assert_in_frame(thm_g, pdef, wrow, final, p_lab, wp)
    for a, b in [(thm_g, pdef), (pdef, wrow), (wrow, final), (final, wp), (p_lab, final), (p_lab, wp)]:
        assert_apart(a, b, gap=0.15)

    scene.say("主定理：每個字都恰好和一個表的字 Knuth 等價")
    scene.play(FadeIn(thm_g), run_time=0.7)
    scene.wait(1.2)
    scene.say("存在：從 ", "$x_1$", " 開始逐一列插入；由命題 1，每插一個數等價類都不變")
    scene.play(Write(pdef), run_time=1.0)
    scene.play(FadeIn(wrow), run_time=0.5)
    scene.wait(0.6)
    cur = None
    for k, (x, Tk, route, new) in enumerate(steps):
        nxt = stages[k]
        nxt.cell(*new).set_fill(GREEN, opacity=0.45)
        anims = [wt[k].animate.set_fill(YELLOW), FadeIn(nxt)]
        if cur is not None:
            anims += [wt[k - 1].animate.set_fill(GREY_B), FadeOut(cur)]
        scene.play(*anims, run_time=0.36)
        cur = nxt
    scene.play(FadeIn(p_lab), wt[-1].animate.set_fill(GREY_B), final.cell(*steps[-1][3]).animate.set_fill(opacity=0.0),
               run_time=0.5)
    scene.say(f"例：{len(CH3_WORD)} 個數插完得到 ", "$P(w)$", "；它的字和 ", "$w$", " 不同，但彼此等價")
    scene.play(FadeIn(wp, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.8)
    scene.say("唯一性（不可能和兩個不同的表都等價）要用新的想法，第 3 章再證")
    scene.wait(2.2)


# =============================================================================
# 第 3、4 段：兩個推論
# =============================================================================
def part_cor1(scene):
    stmt = mixed("推論 1：", "$\\mathrm{Rect}(S)$", " 是唯一一個字與 ", "$w(S)$", " 等價的表", font_size=28)
    stmt.move_to(np.array([0.0, 2.75, 0.0]))
    sk = SkewMob(FULTON_SKEW, cs=0.46, top_left=np.array([-5.6, 2.2, 0.0]))
    s_lab = Tex("S=", font_size=40).next_to(sk, LEFT, buff=0.2)
    ws = VGroup(Tex("w(S)=", font_size=36), word_tex(tableau_word(FULTON_SKEW), font_size=34))
    ws.arrange(RIGHT, buff=0.2).move_to(np.array([-6.3, -1.35, 0.0]), aligned_edge=LEFT)
    res = tableau_mob(RECT_S, cs=0.55, center=np.array([3.9, 0.45, 0.0]))
    res_lab = Tex(r"\mathrm{Rect}(S)=P(w(S))", font_size=32, fill_color=OK_COLOR).next_to(res, DOWN, buff=0.3)
    x0 = res.get_left()[0] - 0.2
    arr1 = Arrow(np.array([sk.get_right()[0] + 0.25, 1.05, 0.0]), np.array([x0, 0.75, 0.0]), buff=0.0,
                 thickness=2.5, fill_color=GREY_B)
    arr2 = Arrow(np.array([ws.get_right()[0] + 0.25, -1.35, 0.0]), np.array([x0, 0.15, 0.0]), buff=0.0,
                 thickness=2.5, fill_color=GREY_B)
    lab1 = zh("滑動（命題 2）", font_size=22, color=MUTED_COLOR).next_to(arr1, UP, buff=0.1)
    lab2 = zh("列插入（命題 1）", font_size=22, color=MUTED_COLOR).next_to(arr2, DOWN, buff=0.1)
    iff = Tex(r"\mathrm{Rect}(S)=\mathrm{Rect}(S')\iff w(S)\equiv w(S')", font_size=34, fill_color=YELLOW)
    iff.move_to(np.array([0.0, -2.45, 0.0]))
    assert_in_frame(stmt, sk, s_lab, ws, res, res_lab, arr1, arr2, lab1, lab2, iff)
    for a, b in [(stmt, sk), (sk, ws), (sk, lab1), (ws, lab2), (lab1, res), (res, res_lab), (ws, iff),
                 (lab2, iff), (res_lab, iff), (arr1, arr2), (lab1, lab2), (s_lab, ws)]:
        assert_apart(a, b, gap=0.1)

    scene.say("推論 1：把斜表滑成表，和把它的字逐一插入，結果一定相同")
    scene.play(FadeIn(stmt), FadeIn(sk), FadeIn(s_lab), run_time=0.7)
    scene.play(FadeIn(ws), run_time=0.5)
    scene.wait(0.8)
    scene.say("兩條路都不改變字的等價類，而與 ", "$w(S)$", " 等價的表只有一個")
    scene.play(GrowArrow(arr1), FadeIn(lab1), run_time=0.6)
    scene.play(GrowArrow(arr2), FadeIn(lab2), run_time=0.6)
    scene.play(FadeIn(res), FadeIn(res_lab), run_time=0.6)
    scene.wait(1.4)
    scene.say("所以兩個斜表滑出同一個表，恰好是它們的字 Knuth 等價的時候")
    scene.play(FadeIn(iff, shift=0.1 * UP), run_time=0.6)
    scene.wait(2.0)


def arrow_label(arrow, text, side=1, buff=0.24):
    """沿著箭頭方向擺的小標籤（side = 1 在上方，-1 在下方）。"""
    s, e = arrow.get_start(), arrow.get_end()
    ang = np.arctan2(e[1] - s[1], e[0] - s[0])
    normal = np.array([-np.sin(ang), np.cos(ang), 0.0])
    lab = zh(text, font_size=20, color=MUTED_COLOR).rotate(ang)
    return lab.move_to((s + e) / 2 + side * buff * normal)


def part_cor2(scene):
    stmt = mixed("推論 2：乘積 ", "$T\\cdot U$", " 的三種做法，結果都一樣", font_size=28)
    stmt.move_to(np.array([0.0, 2.75, 0.0]))
    wtu = tableau_word(T0) + tableau_word(U0)
    a = mixed("列插入：", "$" + insertion_tex(tableau_word(U0)) + "$", font_size=26)
    sk = SkewMob(star(T0, U0), cs=0.32, fs=19)
    b = VGroup(Tex(r"\mathrm{Rect}", font_size=34), sk).arrange(RIGHT, buff=0.2)
    c = VGroup(Tex("P(", font_size=34), word_tex(wtu, font_size=28), Tex(")", font_size=34)).arrange(RIGHT, buff=0.08)
    for mob, y in [(a, 1.75), (b, 0.05), (c, -1.75)]:
        mob.move_to(np.array([-6.3, y, 0.0]), aligned_edge=LEFT)
    res = tableau_mob(TU, cs=0.48, center=np.array([4.4, 0.0, 0.0]))
    res_lab = Tex(r"T\cdot U", font_size=36, fill_color=OK_COLOR).next_to(res, UP, buff=0.2)
    x0 = res.get_left()[0] - 0.2
    arrows = VGroup(*[Arrow(np.array([m.get_right()[0] + 0.25, m.get_center()[1], 0.0]), np.array([x0, y, 0.0]),
                            buff=0.0, thickness=2.5, fill_color=GREY_B)
                      for m, y in [(a, 0.6), (b, 0.0), (c, -0.6)]])
    labs = VGroup(*[arrow_label(ar, txt, side) for ar, txt, side in
                    zip(arrows, ["命題 1 的推論", "命題 2", "主定理（定義）"], [1, 1, -1])])
    assert_in_frame(stmt, a, b, c, res, res_lab, arrows, labs)
    for p, q in [(stmt, a), (a, b), (b, c), (stmt, res_lab), (res_lab, res), (labs[0], labs[1]),
                 (labs[1], labs[2]), (labs[0], res_lab)]:
        assert_apart(p, q, gap=0.2)
    for p in (a, b, c):
        assert_apart(p, VGroup(res, res_lab), gap=0.5)
        for lab in labs:
            assert_apart(p, lab, gap=0.15)

    scene.say("推論 2：", "$T\\cdot U$", " 用列插入、用滑動 ", "$\\mathrm{Rect}(T*U)$", "、或用 ", "$P(w(T)\\,w(U))$",
              "，都一樣")
    scene.play(FadeIn(stmt), run_time=0.5)
    scene.play(LaggedStart(FadeIn(a), FadeIn(b), FadeIn(c), lag_ratio=0.3), run_time=1.2)
    scene.wait(1.0)
    scene.say("三種做法都讓字保持等價：", "$w(T\\cdot U)\\equiv w(T)\\,w(U)$", "；這樣的表只有一個")
    scene.play(LaggedStart(*[GrowArrow(ar) for ar in arrows], lag_ratio=0.3), run_time=1.0)
    scene.play(FadeIn(res), FadeIn(res_lab), run_time=0.6)
    scene.wait(1.6)
    scene.say("列插入靠命題 1 的推論，滑動靠命題 2；第三種就是用主定理來定義")
    scene.play(LaggedStart(*[FadeIn(lab) for lab in labs], lag_ratio=0.3), run_time=0.9)
    scene.wait(2.0)


# =============================================================================
# 第 5 段：plactic monoid 與表環
# =============================================================================
def part_plactic(scene):
    l1 = mixed("字的乘法＝接起來：", "$w\\equiv w',\\ v\\equiv v'\\ \\Rightarrow\\ w\\,v\\equiv w'\\,v'$", font_size=28)
    l2 = mixed("等價類組成 plactic monoid ", "$\\mathcal{M}$", "；它和「表＋乘積」一模一樣", font_size=28)
    l3 = mixed("表環 ", "$R[m]$", "：以表為基底，乘法用 ", "$T\\cdot U$", "（有結合律、不交換）", font_size=28)
    l4 = Tex(r"R[m]\to\mathbb{Z}[x_1,\dots,x_m],\quad T\mapsto x^T", font_size=38, fill_color=YELLOW)
    l5 = Tex("x^T=" + monomial(content(T0, M)) + r",\qquad x^U=" + monomial(content(U0, M)), font_size=36)
    l6 = Tex("x^{T\\cdot U}=" + monomial(content(TU, M)) + "=x^T\\,x^U", font_size=36)
    lines = VGroup(l1, l2, l3, l4, l5, l6).arrange(DOWN, buff=0.36).move_to(np.array([0.0, 0.2, 0.0]))
    assert_in_frame(lines)
    for p, q in zip(lines[:-1], lines[1:]):
        assert_apart(p, q, gap=0.15)

    scene.say("把字接起來當乘法：等價的字接起來還是等價，所以等價類也能相乘")
    scene.play(FadeIn(l1, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)
    scene.say("等價類的么半群叫 plactic monoid；由主定理，它就是表和表的乘積")
    scene.play(FadeIn(l2, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)
    scene.say("表環 ", "$R[m]$", "：每個表換成單項式 ", "$x^T$", "，就到了多項式環")
    scene.play(FadeIn(l3, shift=0.1 * UP), run_time=0.6)
    scene.play(FadeIn(l4, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)
    scene.say("例：", "$x^{T\\cdot U}=x^T\\,x^U$", "，因為乘積裡的數正好是兩個表的數合起來")
    scene.play(FadeIn(l5, shift=0.1 * UP), run_time=0.6)
    scene.wait(0.8)
    scene.play(FadeIn(l6, shift=0.1 * UP), run_time=0.6)
    scene.wait(2.4)


class SceneF10SlidesTheorem(ChuScene):
    def construct(self):
        self.show_header("滑動、主定理與 plactic monoid")
        check_math()
        part_slides(self)
        self.clear_stage()
        part_theorem(self)
        self.clear_stage()
        part_cor1(self)
        self.clear_stage()
        part_cor2(self)
        self.clear_stage()
        part_plactic(self)
        self.wait(1.0)
