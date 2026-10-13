"""
Scene F07 —— jeu de taquin：內角、外角、滑動、反向滑動、rectification（Fulton §1.2，p.12–15）

    斜表 S（p.12）：形狀 (5,5,4,3,2)/(4,4,1)，內角 2 個、外角 4 個
    滑動：洞的右鄰、下鄰取較小的滑進洞（一樣大取下面），洞挖到外角就拿掉
        從第 3 列的內角滑：2 上移 → 3 左移 → 5 上移 → 拿掉第 5 列第 2 格（p.13）
    局部圖（p.14）：x ≤ y 時 x 往上、x > y 時 y 往左，列與行的大小關係都保持
    反向滑動：洞往上或往左，取較大的（一樣大取上面），洞成為內角時停
    rectification：一直滑到沒有內角；Claim 2：與內角的挑法無關（p.15）

數字全部由 utils/tableaux.py 算出並 assert。格子 (i, j) 0 起算，第 0 列在最上面。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF07_jeu_de_taquin.py SceneF07JeuDeTaquin
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh
from utils.tableaux import (
    FULTON_SKEW,
    forward_slide,
    inside_corners,
    is_skew_tableau,
    is_tableau,
    jdt_steps,
    outside_corners,
    rectify,
    reverse_slide,
    skew_cells,
    skew_shape,
    standard_tableaux,
)

N_ = None
BOOK_SKEW = ((N_, N_, N_, N_, 2),              # 書 p.12 的斜表
             (N_, N_, N_, N_, 6),
             (N_, 2, 4, 4),
             (2, 3, 6),
             (5, 5))
BOOK_AFTER = ((N_, N_, N_, N_, 2),             # 書 p.13：從第 3 列的內角滑一次之後
              (N_, N_, N_, N_, 6),
              (2, 2, 4, 4),
              (3, 5, 6),
              (5,))
FIRST_CORNER = (2, 0)                          # 書上的「第 3 列第 1 格」
RECT = ((2, 2, 2, 4, 6), (3, 4, 6), (5, 5))

MU_FILL, MU_OPACITY = GREY_C, 0.45
IN_COLOR = GREEN                               # 內角
OUT_COLOR = ORANGE                             # 外角
HOLE_COLOR = YELLOW                            # 洞
A_COLOR = TEAL                                 # 右鄰（反向：左鄰）
B_COLOR = PINK                                 # 下鄰（反向：上鄰）
CELL_STROKE = GREY_A

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2
PANEL_X = -1.8                                 # 右側說明欄的左邊界


def pick_bottom(cs):
    return cs[-1]


def pick_top(cs):
    return cs[0]


def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊（至少一個方向分開 gap）。"""
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a, b)


def as_point(xy):
    return np.array([xy[0], xy[1], 0.0])


def part_str(p):
    return "(" + ",".join(str(v) for v in p) + ")"


def all_rectifications(S):
    """把每一種挑內角的順序都走一遍：回傳 (順序的個數, 得到的表的集合)。"""
    cs = inside_corners(S)
    if not cs:
        return 1, {S}
    total, results = 0, set()
    for c in cs:
        k, res = all_rectifications(forward_slide(S, c)[0])
        total += k
        results |= res
    return total, results


# =============================================================================
# 滑動的每一步（自己照規則算一遍，再和 tableaux.py 對照）
# =============================================================================
def slide_steps(S, corner):
    """[(洞, 右鄰的數, 下鄰的數, 滑進洞的格子 或 None)]，最後一筆是洞到了外角。"""
    cells = skew_cells(S)
    hole, steps = corner, []
    while True:
        i, j = hole
        right, below = cells.get((i, j + 1)), cells.get((i + 1, j))
        if right is None and below is None:
            steps.append((hole, right, below, None))
            break
        nxt = (i + 1, j) if right is None or (below is not None and below <= right) else (i, j + 1)
        steps.append((hole, right, below, nxt))
        cells[hole] = cells.pop(nxt)
        hole = nxt
    S2, path = forward_slide(S, corner)
    assert [s[0] for s in steps] == path
    return steps, S2


def reverse_steps(S, box):
    """反向滑動：[(洞, 上鄰的數, 左鄰的數, 滑進洞的格子 或 None)]。"""
    cells = skew_cells(S)
    hole, steps = box, []
    while True:
        i, j = hole
        up, left = cells.get((i - 1, j)), cells.get((i, j - 1))
        if up is None and left is None:
            steps.append((hole, up, left, None))
            break
        nxt = (i - 1, j) if left is None or (up is not None and up >= left) else (i, j - 1)
        steps.append((hole, up, left, nxt))
        cells[hole] = cells.pop(nxt)
        hole = nxt
    S0, path = reverse_slide(S, box)
    assert [s[0] for s in steps] == path
    return steps, S0


# =============================================================================
# 畫斜表：用 dict 記住每一格（方便滑動時更新）
# =============================================================================
def cell_pos(board, i, j):
    cs = board["cs"]
    return board["origin"] + (j + 0.5) * cs * RIGHT + (i + 0.5) * cs * DOWN


def new_cell(board, i, j, in_mu):
    sq = Square(side_length=board["cs"], stroke_color=CELL_STROKE, stroke_width=3)
    sq.set_fill(MU_FILL if in_mu else BLACK, opacity=MU_OPACITY if in_mu else 0.0)
    sq.move_to(cell_pos(board, i, j))
    return sq


def make_board(S, cs, top_left, font_size):
    board = {"cs": cs, "origin": as_point(top_left), "fs": font_size,
             "cells": {}, "nums": {}, "vals": {}, "mu": set(), "hole": None, "hole_at": None}
    for i, row in enumerate(S):
        for j, v in enumerate(row):
            board["cells"][(i, j)] = new_cell(board, i, j, v is None)
            if v is None:
                board["mu"].add((i, j))
            else:
                t = Tex(str(v), font_size=font_size).move_to(cell_pos(board, i, j))
                t.set_z_index(2)
                board["nums"][(i, j)] = t
                board["vals"][(i, j)] = v
    return board


def board_group(board):
    return VGroup(*board["cells"].values(), *board["nums"].values())


def board_as_skew(board):
    """把畫面上的格子讀回斜表，和 tableaux.py 的結果比對。"""
    rows = sorted({i for i, _ in board["cells"]})
    out = []
    for i in rows:
        length = max(j for a, j in board["cells"] if a == i) + 1
        assert all((i, j) in board["cells"] for j in range(length))
        out.append(tuple(None if (i, j) in board["mu"] else board["vals"][(i, j)] for j in range(length)))
    return tuple(out)


def hole_marker(board):
    sq = Square(side_length=board["cs"] * 0.86, stroke_color=HOLE_COLOR, stroke_width=5)
    sq.set_fill(HOLE_COLOR, opacity=0.22)
    sq.set_z_index(1)
    return sq


def anims_open_hole(board, corner):
    """內角變成洞：灰色拿掉、放上洞的記號。"""
    assert corner in board["mu"]
    board["mu"].discard(corner)
    hole = hole_marker(board).move_to(cell_pos(board, *corner))
    board["hole"], board["hole_at"] = hole, corner
    return [board["cells"][corner].animate.set_fill(BLACK, opacity=0.0), FadeIn(hole, scale=0.5)]


def anims_move(board, src):
    """src 上的數滑進洞，洞移到 src。"""
    dst = board["hole_at"]
    num = board["nums"].pop(src)
    board["nums"][dst] = num
    board["vals"][dst] = board["vals"].pop(src)
    board["hole_at"] = src
    return [num.animate.move_to(cell_pos(board, *dst)), board["hole"].animate.move_to(cell_pos(board, *src))]


def anims_drop_cell(board):
    """洞到了外角：這一格整個拿掉。"""
    h = board["hole_at"]
    cell = board["cells"].pop(h)
    hole = board["hole"]
    board["hole"], board["hole_at"] = None, None
    return [FadeOut(cell, scale=0.4), FadeOut(hole, scale=0.4)]


def anims_open_reverse(board, box):
    """反向滑動：把拿掉的格子放回來當洞。"""
    cell = new_cell(board, *box, in_mu=False)
    board["cells"][box] = cell
    hole = hole_marker(board).move_to(cell_pos(board, *box))
    board["hole"], board["hole_at"] = hole, box
    return [FadeIn(cell), FadeIn(hole, scale=0.5)]


def anims_close_reverse(board):
    """反向滑動結束：洞成了內角，併回 μ（灰色）。"""
    h = board["hole_at"]
    board["mu"].add(h)
    hole = board["hole"]
    board["hole"], board["hole_at"] = None, None
    return [board["cells"][h].animate.set_fill(MU_FILL, opacity=MU_OPACITY), FadeOut(hole)]


def frame_at(board, box, color):
    sq = Square(side_length=board["cs"] * 0.8, stroke_color=color, stroke_width=6)
    sq.set_fill(opacity=0.0)
    sq.move_to(cell_pos(board, *box))
    sq.set_z_index(3)
    return sq


def word(text, color=WHITE, fs=26):
    return zh(text, font_size=fs, color=color)


def compare_line(first, second, forward=True, fs=26):
    """一步的比較說明。forward：first = 右鄰、second = 下鄰；反向：first = 左鄰、second = 上鄰。"""
    fa, fb = ("右", "下") if forward else ("左", "上")
    A = word(fa, A_COLOR, fs)
    B = word(fb, B_COLOR, fs)
    if first is None and second is None:
        if forward:
            return mixed("右、下都沒有數：洞到了外角，拿掉這一格", font_size=fs)
        return mixed("上、左都沒有數：洞成了內角，停下", font_size=fs)
    if first is None:
        return mixed(B, f"${second}$", f"，{fa}邊沒有：取{fb}面", font_size=fs)
    if second is None:
        return mixed(A, f"${first}$", f"，{fb}面沒有：取{fa}邊", font_size=fs)
    if first == second:
        return mixed(A, f"${first}$", "，", B, f"${second}$", f"：一樣大，取{fb}面", font_size=fs)
    if forward:
        if second < first:
            return mixed(A, f"${first}$", "，", B, f"${second}$", "：下面較小，取下面", font_size=fs)
        return mixed(A, f"${first}$", "，", B, f"${second}$", "：右邊較小，取右邊", font_size=fs)
    if second > first:
        return mixed(A, f"${first}$", "，", B, f"${second}$", "：上面較大，取上面", font_size=fs)
    return mixed(A, f"${first}$", "，", B, f"${second}$", "：左邊較大，取左邊", font_size=fs)


def swatch(color, opacity=0.6, side=0.34):
    sq = Square(side_length=side, stroke_color=color, stroke_width=4)
    sq.set_fill(color, opacity=opacity)
    return sq


def check_math():
    S = FULTON_SKEW
    assert S == BOOK_SKEW and is_skew_tableau(S)
    assert skew_shape(S) == ((5, 5, 4, 3, 2), (4, 4, 1))
    assert inside_corners(S) == [(1, 3), (2, 0)]               # 書：第 2 列第 4 格、第 3 列第 1 格
    assert outside_corners(S) == [(1, 4), (2, 3), (3, 2), (4, 1)]  # 書：第 2、3、4、5 列的最後一格
    S2, path = forward_slide(S, FIRST_CORNER)
    assert S2 == BOOK_AFTER and path == [(2, 0), (3, 0), (3, 1), (4, 1)]
    assert is_skew_tableau(S2) and skew_shape(S2) == ((5, 5, 4, 3, 1), (4, 4))
    assert reverse_slide(S2, (4, 1)) == (S, [(4, 1), (3, 1), (3, 0), (2, 0)])
    assert rectify(S) == RECT == rectify(S, pick_top) and is_tableau(RECT)
    n_orders, results = all_rectifications(S)
    assert results == {RECT}
    mu = skew_shape(S)[1]
    assert n_orders == 84 == len(standard_tableaux(mu))         # 挑法的個數 = μ 的標準表個數
    assert len(jdt_steps(S)) == len(jdt_steps(S, pick_top)) == sum(mu) == 9
    return S, n_orders


# =============================================================================
def part_corners(scene, S):
    board = make_board(S, 0.7, (-6.3, 2.75), 36)
    lam, mu = skew_shape(S)
    shape_line = mixed("斜形狀 ", f"$\\lambda/\\mu={part_str(lam)}/{part_str(mu)}$", font_size=28)
    mu_line = VGroup(swatch(MU_FILL, MU_OPACITY), mixed("灰色：挖掉的小圖 ", "$\\mu$", font_size=26))
    in_line = VGroup(swatch(IN_COLOR, 0.0), mixed("內角：", "$\\mu$", " 的角（右、下都不在 ", "$\\mu$", " 裡）",
                                                  font_size=26))
    out_line = VGroup(swatch(OUT_COLOR, 0.0), mixed("外角：", "$\\lambda$", " 的角（右、下都沒有格子）",
                                                    font_size=26))
    for ln in (mu_line, in_line, out_line):
        ln.arrange(RIGHT, buff=0.22)
    panel = VGroup(shape_line, mu_line, in_line, out_line).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
    panel.move_to(np.array([PANEL_X, 1.5, 0.0]), aligned_edge=LEFT)

    ins = inside_corners(S)
    outs = outside_corners(S)
    in_frames = VGroup(*[frame_at(board, b, IN_COLOR) for b in ins])
    out_frames = VGroup(*[frame_at(board, b, OUT_COLOR) for b in outs])
    cells = VGroup(*board["cells"].values())
    nums = VGroup(*board["nums"].values())
    assert_in_frame(cells, panel)
    assert_apart(cells, panel, gap=0.3)

    scene.say("斜表：從大圖 ", "$\\lambda$", " 挖掉左上角的小圖 ", "$\\mu$", "，剩下的格子照表的規則填數")
    scene.play(ShowCreation(cells), FadeIn(shape_line), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(t, scale=1.3) for t in nums], lag_ratio=0.08), FadeIn(mu_line), run_time=1.2)
    scene.wait(0.5)
    scene.say("內角：灰色區域的角——它的右邊和下面都不是灰色")
    scene.play(ShowCreation(in_frames), FadeIn(in_line), run_time=0.8)
    scene.wait(1.2)
    scene.say("外角：整個圖形的角——它的右邊和下面都沒有格子")
    scene.play(ShowCreation(out_frames), FadeIn(out_line), run_time=0.8)
    scene.wait(1.3)
    scene.play(FadeOut(panel), FadeOut(out_frames),
               *[FadeOut(f) for b, f in zip(ins, in_frames) if b != FIRST_CORNER], run_time=0.6)
    keep = in_frames[ins.index(FIRST_CORNER)]
    return board, keep


def part_slide(scene, S, board, keep_frame):
    title = zh("滑動（挖洞）", font_size=30, color=YELLOW)
    rules = VGroup(
        mixed("1. 選一個內角當洞（空格）", font_size=25),
        zh("2. 洞的右鄰、下鄰比大小，較小的滑進洞", font_size=25, t2c={"右鄰": A_COLOR, "下鄰": B_COLOR}),
        mixed("3. 一樣大取下面；只有一個鄰居就取它", font_size=25),
        mixed("4. 兩邊都沒有（到了外角）：拿掉這一格", font_size=25),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    panel = VGroup(title, rules).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    panel.move_to(np.array([PANEL_X, 1.55, 0.0]), aligned_edge=LEFT)
    step_y = -0.65
    cells = VGroup(*board["cells"].values())
    assert_in_frame(panel)
    assert_apart(cells, panel, gap=0.3)

    scene.say("滑動：在內角挖一個洞，讓旁邊的數一格一格滑進洞裡")
    scene.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=0.15 * UP) for r in rules], lag_ratio=0.3),
               run_time=1.6)
    scene.wait(0.6)

    steps, S2 = slide_steps(S, FIRST_CORNER)
    scene.say("從第 3 列的內角開始挖洞")
    scene.play(*anims_open_hole(board, FIRST_CORNER), FadeOut(keep_frame), run_time=0.7)

    prev = VGroup()
    for hole, right, below, nxt in steps:
        i, j = hole
        frames = VGroup()
        if right is not None:
            frames.add(frame_at(board, (i, j + 1), A_COLOR))
        if below is not None:
            frames.add(frame_at(board, (i + 1, j), B_COLOR))
        line = compare_line(right, below, forward=True)
        line.move_to(np.array([PANEL_X, step_y, 0.0]), aligned_edge=LEFT)
        assert_in_frame(line, frames)
        assert_apart(line, cells, gap=0.3)
        assert_apart(line, panel, gap=0.3)
        scene.play(FadeOut(prev), FadeIn(line, shift=0.15 * UP), ShowCreation(frames), run_time=0.6)
        scene.wait(0.6)
        if nxt is not None:
            scene.play(*anims_move(board, nxt), FadeOut(frames), run_time=0.7)
            prev = line
        else:
            scene.play(*anims_drop_cell(board), run_time=0.7)
            prev = line
    assert board_as_skew(board) == S2 == BOOK_AFTER

    lam2, mu2 = skew_shape(S2)
    result = VGroup(
        mixed("新形狀 ", f"$\\lambda/\\mu={part_str(lam2)}/{part_str(mu2)}$", font_size=26),
        mixed("內角那格加進來、外角那格拿掉：仍是斜表", font_size=26, color=OK_COLOR),
    ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    result.move_to(np.array([PANEL_X, -1.85, 0.0]), aligned_edge=LEFT)
    assert_in_frame(result)
    assert_apart(result, prev, gap=0.2)
    assert_apart(result, VGroup(*board["cells"].values()), gap=0.3)
    scene.say("洞挖到外角就把那一格拿掉：得到一個新的斜表")
    scene.play(FadeIn(result, shift=0.15 * UP), run_time=0.8)
    scene.wait(1.6)
    return S2


def patch(labels, cs, center, moved=None):
    """3×3 的局部圖：labels[(r, c)] 是字母或 'hole'。"""
    g = VGroup()
    origin = as_point(center) + 1.5 * cs * (LEFT + UP)
    for (r, c), lab in labels.items():
        pos = origin + (c + 0.5) * cs * RIGHT + (r + 0.5) * cs * DOWN
        sq = Square(side_length=cs, stroke_color=CELL_STROKE, stroke_width=3).move_to(pos)
        g.add(sq)
        if lab == "hole":
            h = Square(side_length=cs * 0.86, stroke_color=HOLE_COLOR, stroke_width=5)
            h.set_fill(HOLE_COLOR, opacity=0.22).move_to(pos)
            g.add(h)
        else:
            g.add(Tex(lab, font_size=40, fill_color=YELLOW if lab == moved else WHITE).move_to(pos))
    return g


def part_local_rule(scene):
    cs = 0.6
    top = patch({(0, 1): "b", (0, 2): "v", (1, 0): "a", (1, 1): "hole", (1, 2): "y", (2, 0): "u", (2, 1): "x"},
                cs, (0.0, 1.9))
    left = patch({(0, 1): "b", (0, 2): "v", (1, 0): "a", (1, 1): "x", (1, 2): "y", (2, 0): "u", (2, 1): "hole"},
                 cs, (-3.7, -0.35), moved="x")
    right = patch({(0, 1): "b", (0, 2): "v", (1, 0): "a", (1, 1): "y", (1, 2): "hole", (2, 0): "u", (2, 1): "x"},
                  cs, (3.7, -0.35), moved="y")
    arr_l = Arrow(top.get_left() + 0.3 * DOWN + 0.1 * LEFT, left.get_top() + 0.15 * UP + 0.4 * RIGHT, buff=0.1,
                  stroke_width=4)
    arr_r = Arrow(top.get_right() + 0.3 * DOWN + 0.1 * RIGHT, right.get_top() + 0.15 * UP + 0.4 * LEFT, buff=0.1,
                  stroke_width=4)
    lab_l = Tex(r"x\le y", font_size=36, fill_color=YELLOW).next_to(arr_l.get_center(), UL, buff=0.12)
    lab_r = Tex(r"x>y", font_size=36, fill_color=YELLOW).next_to(arr_r.get_center(), UR, buff=0.12)
    note_l = VGroup(
        mixed("$x$", " 往上；這一列要 ", "$a\\le x\\le y$", font_size=24),
        mixed("原本就有 ", "$a<u\\le x$", font_size=24),
    ).arrange(DOWN, buff=0.22).next_to(left, DOWN, buff=0.35)
    note_r = VGroup(
        mixed("$y$", " 往左；這一行要 ", "$b<y<x$", font_size=24),
        mixed("原本就有 ", "$b\\le v<y$", font_size=24),
    ).arrange(DOWN, buff=0.22).next_to(right, DOWN, buff=0.35)
    note_top = mixed("字母代表數字", font_size=24, color=MUTED_COLOR)
    note_top.next_to(top, RIGHT, buff=0.5).align_to(top, UP)
    assert_in_frame(top, left, right, arr_l, arr_r, lab_l, lab_r, note_l, note_r, note_top)
    assert_apart(note_l, note_r, gap=0.3)
    assert_apart(lab_l, top)
    assert_apart(lab_r, top)
    assert_apart(lab_l, left)
    assert_apart(lab_r, right)
    assert_apart(note_top, top)
    assert_apart(note_top, lab_r)

    scene.say("為什麼滑完還是表？只要看洞附近的幾格（有些格子可以不存在）")
    scene.play(FadeIn(top), FadeIn(note_top), run_time=0.8)
    scene.wait(1.0)
    scene.say("$x\\le y$", "：下面的 ", "$x$", " 往上。因為 ", "$a<u\\le x$", "，這一列仍是 ", "$a\\le x\\le y$")
    scene.play(GrowArrow(arr_l), FadeIn(lab_l), FadeIn(left), run_time=0.9)
    scene.play(FadeIn(note_l, shift=0.15 * UP), run_time=0.6)
    scene.wait(1.8)
    scene.say("$x>y$", "：右邊的 ", "$y$", " 往左。因為 ", "$b\\le v<y$", "，這一行仍是 ", "$b<y<x$")
    scene.play(GrowArrow(arr_r), FadeIn(lab_r), FadeIn(right), run_time=0.9)
    scene.play(FadeIn(note_r, shift=0.15 * UP), run_time=0.6)
    scene.wait(1.8)
    scene.say("規則挑「較小的」滑進洞，正好讓每列、每行的大小關係都保持住")
    scene.wait(1.6)


def part_reverse(scene, S, S2):
    board = make_board(S2, 0.7, (-6.3, 2.75), 36)
    removed = (4, 1)
    ghost = DashedVMobject(Square(side_length=board["cs"]), num_dashes=16).set_stroke(OUT_COLOR, width=3)
    ghost.move_to(cell_pos(board, *removed))
    title = zh("反向滑動", font_size=30, color=YELLOW)
    rules = VGroup(
        mixed("1. 把拿掉的那一格放回來當洞", font_size=25),
        zh("2. 洞的上鄰、左鄰比大小，較大的滑進洞", font_size=25, t2c={"上鄰": B_COLOR, "左鄰": A_COLOR}),
        mixed("3. 一樣大取上面", font_size=25),
        mixed("4. 洞變成內角時停下，併回 ", "$\\mu$", font_size=25),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    panel = VGroup(title, rules).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    panel.move_to(np.array([PANEL_X, 1.55, 0.0]), aligned_edge=LEFT)
    cells = VGroup(*board["cells"].values())
    assert_in_frame(panel, cells, ghost)
    assert_apart(cells, panel, gap=0.3)

    scene.say("滑動可以倒回去：只要記得最後拿掉的是哪一格")
    scene.play(FadeIn(board_group(board)), ShowCreation(ghost), run_time=0.9)
    scene.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=0.15 * UP) for r in rules], lag_ratio=0.3),
               run_time=1.4)
    scene.wait(0.5)

    steps, S0 = reverse_steps(S2, removed)
    assert S0 == S
    scene.play(*anims_open_reverse(board, removed), FadeOut(ghost), run_time=0.6)
    prev = VGroup()
    for hole, up, left, nxt in steps:
        i, j = hole
        frames = VGroup()
        if left is not None:
            frames.add(frame_at(board, (i, j - 1), A_COLOR))
        if up is not None:
            frames.add(frame_at(board, (i - 1, j), B_COLOR))
        line = compare_line(left, up, forward=False)
        line.move_to(np.array([PANEL_X, -0.65, 0.0]), aligned_edge=LEFT)
        assert_in_frame(line, frames)
        assert_apart(line, cells, gap=0.3)
        assert_apart(line, panel, gap=0.3)
        scene.play(FadeOut(prev), FadeIn(line, shift=0.15 * UP), ShowCreation(frames), run_time=0.5)
        scene.wait(0.5)
        if nxt is not None:
            scene.play(*anims_move(board, nxt), FadeOut(frames), run_time=0.6)
        else:
            scene.play(*anims_close_reverse(board), run_time=0.6)
        prev = line
    assert board_as_skew(board) == S

    back = mixed("又回到原來的斜表，內角也回來了", font_size=26, color=OK_COLOR)
    back.move_to(np.array([PANEL_X, -1.5, 0.0]), aligned_edge=LEFT)
    assert_in_frame(back)
    assert_apart(back, prev, gap=0.2)
    scene.say("一步一步倒回去，回到原來的斜表")
    scene.play(FadeIn(back, shift=0.15 * UP), run_time=0.6)
    scene.wait(1.6)


def part_rectify(scene, S, n_orders):
    cs, fs = 0.66, 32
    A = make_board(S, cs, (-6.5, 2.3), fs)
    B = make_board(S, cs, (-2.3, 2.3), fs)
    gA, gB = board_group(A), board_group(B)
    labA = zh("每次挑最下面的內角", font_size=24, color=A_COLOR).next_to(gA, UP, buff=0.25)
    labB = zh("每次挑最上面的內角", font_size=24, color=B_COLOR).next_to(gB, UP, buff=0.25)
    stepsA = jdt_steps(S, pick_bottom)
    stepsB = jdt_steps(S, pick_top)
    n = len(stepsA)
    assert n == len(stepsB) == 9

    def counter(k):
        return mixed("第 ", f"${k}$", " 次滑動（共 ", f"${n}$", " 次）", font_size=26)

    cnt = counter(0)
    rule = VGroup(
        mixed("jeu de taquin：", font_size=26, color=YELLOW),
        mixed("一直挑內角來滑動，", font_size=26),
        mixed("直到沒有內角為止", font_size=26),
    ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    rule.move_to(np.array([1.75, 2.55, 0.0]), aligned_edge=LEFT)
    rule.shift((rule.get_top()[1] - 2.85) * DOWN)
    cnt.next_to(rule, DOWN, buff=0.35, aligned_edge=LEFT)
    assert_in_frame(gA, gB, labA, labB, cnt, rule)
    assert_apart(gA, gB, gap=0.5)
    assert_apart(gB, rule, gap=0.3)
    assert_apart(gB, cnt, gap=0.3)
    assert_apart(labA, labB, gap=0.3)

    scene.say("jeu de taquin：一直挑內角來滑動，直到沒有內角為止")
    scene.play(FadeIn(gA), FadeIn(gB), FadeIn(labA), FadeIn(labB), FadeIn(rule), FadeIn(cnt), run_time=1.0)
    scene.say("左右兩邊用不同的方式挑內角，同時進行")
    scene.wait(0.3)

    SA, SB = S, S
    for k in range(n):
        cA, pathA, SA_next = stepsA[k]
        cB, pathB, SB_next = stepsB[k]
        mvA, SA2 = slide_steps(SA, cA)
        mvB, SB2 = slide_steps(SB, cB)
        assert SA2 == SA_next and SB2 == SB_next
        new_cnt = counter(k + 1).move_to(cnt, aligned_edge=LEFT)
        scene.play(*anims_open_hole(A, cA), *anims_open_hole(B, cB), FadeOut(cnt), FadeIn(new_cnt), run_time=0.3)
        cnt = new_cnt
        srcA = [s[3] for s in mvA if s[3] is not None]
        srcB = [s[3] for s in mvB if s[3] is not None]
        for t in range(max(len(srcA), len(srcB))):
            anims = []
            if t < len(srcA):
                anims += anims_move(A, srcA[t])
            if t < len(srcB):
                anims += anims_move(B, srcB[t])
            scene.play(*anims, run_time=0.26)
        scene.play(*anims_drop_cell(A), *anims_drop_cell(B), run_time=0.3)
        assert board_as_skew(A) == SA_next and board_as_skew(B) == SB_next
        SA, SB = SA_next, SB_next
    assert SA == SB == RECT
    assert not inside_corners(SA)

    cellsA = VGroup(*A["cells"].values())
    cellsB = VGroup(*B["cells"].values())
    eq = Tex("=", font_size=50, fill_color=YELLOW)
    eq.move_to(np.array([(cellsA.get_right()[0] + cellsB.get_left()[0]) / 2, cellsA.get_center()[1], 0.0]))
    boxA = SurroundingRectangle(cellsA, buff=0.08, color=OK_COLOR, stroke_width=4)
    boxB = SurroundingRectangle(cellsB, buff=0.08, color=OK_COLOR, stroke_width=4)
    rect_lab = Tex(r"\mathrm{Rect}(S)", font_size=40, fill_color=OK_COLOR)
    rect_lab.next_to(VGroup(boxA, boxB), DOWN, buff=0.35)
    assert_apart(eq, boxA, gap=0.15)
    assert_apart(eq, boxB, gap=0.15)

    claim_title = mixed("Claim 2", font_size=30, color=YELLOW)
    claim = VGroup(
        claim_title,
        mixed("不管內角怎麼挑，", font_size=26),
        mixed("最後得到的表都一樣", font_size=26),
        mixed("挑法共 ", f"${n_orders}$", " 種，全部算過：", font_size=26),
        mixed("結果都是同一個表", font_size=26),
    ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    claim.move_to(np.array([1.75, -0.75, 0.0]), aligned_edge=LEFT)
    claim_box = SurroundingRectangle(claim, buff=0.22, color=YELLOW, stroke_width=3)
    assert_in_frame(eq, boxA, boxB, rect_lab, claim_box)
    assert_apart(claim_box, cnt, gap=0.15)
    assert_apart(claim_box, VGroup(boxB, rect_lab), gap=0.15)
    assert_apart(rect_lab, VGroup(cellsA, cellsB), gap=0.1)

    scene.say("兩種挑法，最後得到同一個表")
    scene.play(FadeIn(eq, scale=1.4), ShowCreation(boxA), ShowCreation(boxB), run_time=0.8)
    scene.wait(1.0)
    scene.say("這個表叫做 ", "$S$", " 的 rectification，記作 ", "$\\mathrm{Rect}(S)$")
    scene.play(FadeIn(rect_lab, shift=0.15 * UP), run_time=0.7)
    scene.wait(1.4)
    scene.say("Claim 2：結果與內角的挑法無關（證明在後面的章節）")
    scene.play(ShowCreation(claim_box), LaggedStart(*[FadeIn(c, shift=0.1 * UP) for c in claim], lag_ratio=0.2),
               run_time=1.6)
    scene.wait(2.6)


class SceneF07JeuDeTaquin(ChuScene):
    def construct(self):
        self.show_header("jeu de taquin：滑動與 rectification")
        S, n_orders = check_math()
        board, keep = part_corners(self, S)
        S2 = part_slide(self, S, board, keep)
        self.clear_stage()
        part_local_rule(self)
        self.clear_stage()
        part_reverse(self, S, S2)
        self.clear_stage()
        part_rectify(self, S, n_orders)
        self.wait(1.0)
