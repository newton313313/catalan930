"""
Scene F04 —— 列插入（row bumping）（Fulton《Young Tableaux》§1.1，書 p.7–9）

    T ← x：x 進第 1 列；該列沒有比 x 大的數就接在列尾，否則 x 換掉「最左邊、嚴格大於 x」的數，
           被擠出的數再插入下一列，依此類推（擠到最底下就自成新的一列）
    書上的例子：T = [[1,2,2,3],[2,3,5,5],[4,4,6],[5,6]] ← 2
           2 擠出 3、3 擠出 5、5 擠出 6、6 接在第 4 列 → [[1,2,2,2],[2,3,3,5],[4,4,5],[5,6,6]]
           擠壓路徑每列一格，最後一格 = 新格子（第 4 列第 3 行）
    為什麼仍是表：被擠出的 z 正下方的數 > z，所以 z 落在同一行或更左邊；落點上方 ≤ y < z
    反向擠出：知道新格子，從外角往上倒推，找「最右邊、嚴格小於」的數，最後擠出 x = 2、還原 T

數字一律由 utils/tableaux.py 算出並 assert（格子 0 起算；畫面上的「第幾列／行」是 1 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF04_row_insertion.py SceneF04RowInsertion
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import mixed, zh
from utils.tableaux import (
    FULTON_INSERT_T,
    bump_steps,
    corners,
    is_tableau,
    reverse_bump,
    row_insert,
    shape,
)

T0 = FULTON_INSERT_T
X = 2
BOOK_T = ((1, 2, 2, 3), (2, 3, 5, 5), (4, 4, 6), (5, 6))          # 書 p.7
BOOK_RESULT = ((1, 2, 2, 2), (2, 3, 3, 5), (4, 4, 5), (5, 6, 6))   # 書 p.8

# ------------------------------------------------------------------ 版面
CS = 0.9                                  # 格子邊長
TL = np.array([-6.2, 2.35, 0.0])           # 格子 (0,0) 的左上角
IN_X = -1.3                               # 等著進入某一列的數（「← x」的 x）
ARROW_X = -2.0
LOG_X = -0.4                             # 右邊紀錄欄的左緣
ENTRY_FONT = 42
LABEL_POS = np.array([TL[0] + 2 * CS, 2.8, 0.0])

ROUTE_COLOR = ORANGE
NEW_COLOR = GREEN
TRAVEL_COLOR = YELLOW
DIM_COLOR = GREY_D

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


def row_y(i):
    return TL[1] - (i + 0.5) * CS


def col_x(j):
    return TL[0] + (j + 0.5) * CS


def cell_pt(i, j):
    return np.array([col_x(j), row_y(i), 0.0])


def lane_y(i):
    """第 i 列上方的格線（第 i 列下方是 lane_y(i + 1)）；移動中的數沿格線走，不會壓到別的數。"""
    return TL[1] - i * CS


def slot(i):
    return np.array([IN_X, row_y(i), 0.0])


def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a, b)


def num_tex(v, color=WHITE):
    t = Tex(str(v), font_size=ENTRY_FONT, fill_color=color)
    t.set_z_index(2)
    return t


def glide(mob, points, start_color=WHITE, end_color=None, **kwargs):
    """沿折線等速移動（可同時改顏色）。"""
    pts = [np.array(p, dtype=float) for p in points]
    seg = [float(np.linalg.norm(q - p)) for p, q in zip(pts[:-1], pts[1:])]
    total = sum(seg)

    def pos(a):
        s = a * total
        for p, q, length in zip(pts[:-1], pts[1:], seg):
            if length > 0 and s <= length:
                return p + (q - p) * (s / length)
            s -= length
        return pts[-1]

    def update(m, a):
        m.move_to(pos(a))
        if end_color is not None:
            m.set_fill(interpolate_color(start_color, end_color, a))

    return UpdateFromAlphaFunc(mob, update, **kwargs)


def reverse_steps(T, box):
    """反向擠出的每一步（由下往上）：[(格子, 換上去的數, 被往上擠的數)]，以及最後擠出的數與還原的列。"""
    rows = [list(r) for r in T]
    r, _ = box
    y = rows[r].pop()
    out = []
    for rr in range(r - 1, -1, -1):
        row = rows[rr]
        k = max(j for j, v in enumerate(row) if v < y)          # 最右邊、嚴格小於 y
        out.append(((rr, k), y, row[k]))
        row[k], y = y, row[k]
    return out, y, tuple(tuple(row) for row in rows if row)


def check_math():
    assert T0 == BOOK_T and is_tableau(T0) and shape(T0) == (4, 4, 3, 2)
    steps = bump_steps(T0, X)
    assert steps == [((0, 3), 2, 3), ((1, 2), 3, 5), ((2, 2), 5, 6), ((3, 2), 6, None)]
    # 每一步都是「最左邊、嚴格大於」：左邊的數都不大於放進去的數
    cur = [list(r) for r in T0]
    for (r, c), placed, bumped in steps:
        assert all(v <= placed for v in cur[r][:c])
        if bumped is None:
            assert c == len(cur[r])
            cur[r].append(placed)
        else:
            assert cur[r][c] == bumped > placed
            cur[r][c] = placed
    T1, route, new = row_insert(T0, X)
    assert tuple(tuple(r) for r in cur) == T1 == BOOK_RESULT and is_tableau(T1)
    assert route == [b for b, _, _ in steps] and new == (3, 2)        # 新格子 = 書上的 (4,3)
    assert shape(T1) == (4, 4, 3, 3)
    # 為什麼仍是表：第 2 列 3 坐進 (1,2)，左邊 3 ≤ 3、右邊 5 > 3
    assert T1[1][1] == 3 <= 3 and T1[1][3] == 5 > 3 and T1[1][2] == 3
    # 2 擠出 (0,3) 的 3；3 原本正下方 T0[1][3] = 5 > 3；3 落在 (1,2)（更左邊一行）；落點上方 T1[0][2] = 2 ≤ 2 < 3
    assert T0[0][3] == 3 and T0[1][3] == 5 > 3 and steps[1][0] == (1, 2) and 2 < 3
    assert T1[0][2] == 2 <= T1[0][3] == 2 < 3
    # 反向擠出
    T_back, x_back, r_route = reverse_bump(T1, new)
    assert T_back == T0 and x_back == X and r_route == route
    rsteps, x_out, rows_back = reverse_steps(T1, new)
    assert rsteps == [((2, 2), 6, 5), ((1, 2), 5, 3), ((0, 3), 3, 2)] and x_out == X and rows_back == T0
    assert [b for b, _, _ in rsteps] == list(reversed(route[:-1]))
    assert corners(shape(T1)) == [(1, 3), (3, 2)]
    return dict(steps=steps, T1=T1, new=new, route=route, rsteps=rsteps)


# =============================================================================
def build_board(scene):
    d = YoungDiagramMob(shape(T0), cell_size=CS, top_left=TL)
    ents = {}
    for i, row in enumerate(T0):
        for j, v in enumerate(row):
            ents[(i, j)] = num_tex(v).move_to(cell_pt(i, j))
    label = Tex("T", font_size=46).move_to(LABEL_POS)
    assert_in_frame(d, label)
    assert_apart(label, d)
    return dict(d=d, ents=ents, label=label, extra=VGroup())


def part_intro(scene, b):
    d, ents = b["d"], b["ents"]
    scene.say("列插入：把一個數 ", "$x$", " 放進表 ", "$T$", "，得到多一格的新表 ", "$T\\leftarrow x$")
    scene.play(ShowCreation(d.cells), FadeIn(b["label"]), run_time=0.9)
    scene.play(LaggedStart(*[FadeIn(ents[k], scale=0.6) for k in sorted(ents)], lag_ratio=0.05), run_time=1.0)

    rules = VGroup(
        mixed("① 在這一列找最左邊、嚴格大於 ", "$x$", " 的數", font_size=24),
        mixed("② 找到了：", "$x$", " 換進那一格，原來的數被擠到下一列，換它做 ①", font_size=24),
        mixed("③ 找不到：", "$x$", " 接在這一列尾端（沒有下一列就自成一列），結束", font_size=24),
    ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    rules.move_to(np.array([0.0, -2.25, 0.0])).set_x(TL[0], direction=LEFT)
    assert_in_frame(rules)
    assert_apart(rules, d, gap=0.3)
    b["rules"] = rules
    scene.say("規則：從第 1 列開始，找最左邊、嚴格大於 ", "$x$", " 的數，把它擠到下一列")
    scene.play(LaggedStart(*[FadeIn(r, shift=0.15 * UP) for r in rules], lag_ratio=0.45), run_time=1.8)
    scene.wait(1.6)


def part_forward(scene, b, data):
    d, ents = b["d"], b["ents"]
    steps = data["steps"]
    cur = [list(r) for r in T0]
    trav = num_tex(X, TRAVEL_COLOR).move_to(slot(0))
    arrow = Tex(r"\leftarrow", font_size=40).move_to(np.array([ARROW_X, row_y(0), 0.0]))
    log = VGroup()
    b["log"] = log

    scene.say("例：把 ", "$x=2$", " 插入 ", "$T$", "，從第 1 列的右邊送進去")
    scene.play(FadeIn(trav, shift=0.4 * LEFT), FadeIn(arrow, shift=0.4 * LEFT), run_time=0.7)

    for k, ((r, c), placed, bumped) in enumerate(steps):
        skipped = [ents[(r, j)] for j in range(c)]
        assert all(cur[r][j] <= placed for j in range(c))
        if bumped is not None:
            assert cur[r][c] == bumped and bumped > placed
            if k == 0:
                small = ",".join(str(v) for v in cur[r][:c])
                scene.say("第 1 列：", f"${small}$", " 都不大於 ", f"${placed}$", "，最左邊比 ", f"${placed}$",
                          " 大的是 ", f"${bumped}$")
            else:
                scene.say(f"第 {r + 1} 列：最左邊、比 ", f"${placed}$", " 大的是 ", f"${bumped}$", "，於是 ",
                          f"${placed}$", " 換進去、", f"${bumped}$", " 往下一列")
            scene.play(*[m.animate.set_fill(DIM_COLOR) for m in skipped],
                       d.cell(r, c).animate.set_fill(ROUTE_COLOR, opacity=0.4), run_time=0.6)
            if k == 0:
                scene.wait(0.6)
                scene.say("$2$", " 換進 ", "$3$", " 的位置；被擠出來的 ", "$3$", " 去第 2 列重複同樣的事")
            old = ents[(r, c)]
            new_arrow = Tex(r"\leftarrow", font_size=40).move_to(np.array([ARROW_X, row_y(r + 1), 0.0]))
            line = mixed(f"${placed}$", " 擠出 ", f"${bumped}$", font_size=26)
            line.move_to(np.array([LOG_X, row_y(r), 0.0]), aligned_edge=LEFT)
            log.add(line)
            scene.play(
                glide(trav, [slot(r), (IN_X, lane_y(r), 0), (col_x(c), lane_y(r), 0), cell_pt(r, c)],
                      start_color=TRAVEL_COLOR, end_color=WHITE),
                glide(old, [cell_pt(r, c), (col_x(c), lane_y(r + 1), 0), (IN_X, lane_y(r + 1), 0), slot(r + 1)],
                      start_color=WHITE, end_color=TRAVEL_COLOR),
                FadeOut(arrow), FadeIn(new_arrow), FadeIn(line, shift=0.2 * LEFT),
                *[m.animate.set_fill(WHITE) for m in skipped],
                run_time=1.4,
            )
            ents[(r, c)] = trav
            trav, arrow = old, new_arrow
            cur[r][c] = placed
            scene.wait(1.0 if k == 0 else 0.4)
        else:
            assert c == len(cur[r]) and r == len(cur) - 1
            row_vals = ",".join(str(v) for v in cur[r])
            scene.say(f"第 {r + 1} 列是 ", f"${row_vals}$", "，沒有比 ", f"${placed}$", " 大的數：", f"${placed}$",
                      " 直接接在列尾")
            new_cell = Square(side_length=CS, stroke_color=NEW_COLOR, stroke_width=6)
            new_cell.set_fill(ROUTE_COLOR, opacity=0.4).move_to(cell_pt(r, c))
            line = mixed(f"${placed}$", " 接在列尾", font_size=26)
            line.move_to(np.array([LOG_X, row_y(r), 0.0]), aligned_edge=LEFT)
            log.add(line)
            scene.play(*[m.animate.set_fill(DIM_COLOR) for m in skipped], run_time=0.5)
            scene.play(FadeIn(new_cell, scale=0.5), FadeOut(arrow),
                       glide(trav, [slot(r), cell_pt(r, c)], start_color=TRAVEL_COLOR, end_color=WHITE),
                       FadeIn(line, shift=0.2 * LEFT), run_time=1.1)
            scene.play(*[m.animate.set_fill(WHITE) for m in skipped], run_time=0.4)
            ents[(r, c)] = trav
            cur[r].append(placed)
            b["new_cell"] = new_cell
    assert tuple(tuple(r) for r in cur) == data["T1"]
    assert_in_frame(log)
    for line in log:
        assert_apart(line, VGroup(d, b["new_cell"]), gap=0.3)
    scene.wait(0.6)


def part_result(scene, b, data):
    d = b["d"]
    T1, new = data["T1"], data["new"]
    label2 = Tex(r"T\leftarrow 2", font_size=46).move_to(LABEL_POS)
    sw_route = Square(side_length=0.32, stroke_width=0).set_fill(ROUTE_COLOR, opacity=0.6)
    sw_new = Square(side_length=0.32, stroke_color=NEW_COLOR, stroke_width=5).set_fill(ROUTE_COLOR, opacity=0.6)
    leg1 = VGroup(sw_route, zh("擠壓路徑：每列一格，由上往下", font_size=24)).arrange(RIGHT, buff=0.2)
    leg2 = VGroup(sw_new, mixed("新格子：路徑的最後一格（第 ", "$4$", " 列第 ", "$3$", " 行）", font_size=24)
                  ).arrange(RIGHT, buff=0.2)
    assert (new[0] + 1, new[1] + 1) == (4, 3)
    legend = VGroup(leg1, leg2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    legend.move_to(np.array([0.0, -2.05, 0.0])).set_x(TL[0], direction=LEFT)
    assert_in_frame(label2, legend)
    assert_apart(legend, VGroup(d, b["new_cell"]), gap=0.3)
    b["legend"] = legend
    assert [[b["ents"][(i, j)].get_tex() for j in range(len(row))] for i, row in enumerate(T1)] == \
        [[str(v) for v in row] for row in T1]

    scene.say("完成：得到新表 ", "$T\\leftarrow 2$", "，比 ", "$T$", " 多了一格")
    scene.play(FadeOut(b["rules"]), TransformMatchingTex(b["label"], label2), run_time=0.9)
    b["label"] = label2
    scene.say("被擠動的格子連成「擠壓路徑」，路徑的最後一格就是新格子")
    scene.play(FadeIn(legend, shift=0.15 * UP), run_time=0.8)
    scene.play(Indicate(b["new_cell"], color=NEW_COLOR, scale_factor=1.15), run_time=0.9)
    scene.wait(1.6)


def part_why(scene, b, data):
    d = b["d"]
    title = mixed("為什麼 ", "$T\\leftarrow x$", " 一定還是表？", font_size=28, color=YELLOW)
    lines = VGroup(
        mixed("列：", "$x$", " 左邊的數 ", "$\\le x$", "，右邊的數 ", "$>x$", font_size=26),
        mixed("行：", "$y$", " 擠出 ", "$z$", " 時，", "$z$", " 正下方的數 ", "$>z$", font_size=26),
        mixed("$\\Rightarrow$", " ", "$z$", " 落在同一行或更左邊", font_size=26),
        mixed("$\\Rightarrow$", " 落點上方的數 ", "$\\le y<z$", font_size=26),
    ).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
    panel = VGroup(title, lines).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
    panel.move_to(np.array([0.0, 0.7, 0.0])).set_x(LOG_X, direction=LEFT)
    assert_in_frame(panel)
    assert_apart(panel, VGroup(d, b["new_cell"], b["label"]), gap=0.4)

    scene.say("為什麼結果一定還是表？先看每一列")
    scene.play(FadeOut(b["log"]), run_time=0.5)
    scene.play(FadeIn(title), run_time=0.6)

    # ---- 列：第 2 列的 3 坐進 (1,2)
    row_box = SurroundingRectangle(VGroup(*[d.cell(1, j) for j in range(1, 4)]), buff=0.04,
                                   color=YELLOW, stroke_width=4)
    scene.say("$x$", " 坐進最左邊比它大的位置：左邊 ", "$\\le x$", "，右邊 ", "$>x$", "（例：", "$3\\le 3<5$", "）")
    scene.play(FadeIn(lines[0], shift=0.15 * UP), ShowCreation(row_box), run_time=0.8)
    scene.wait(1.6)

    # ---- 行：2 擠出 (0,3) 的 3，3 落在 (1,2)
    below = SurroundingRectangle(d.cell(1, 3), buff=-0.04, color=TEAL, stroke_width=5)
    hop = Arrow(cell_pt(0, 3), cell_pt(1, 2), buff=0.36, stroke_width=0, thickness=4, fill_color=YELLOW)
    hop.set_color(YELLOW)
    above = SurroundingRectangle(d.cell(0, 2), buff=-0.04, color=PINK, stroke_width=5)
    lines[1][-1].set_fill(TEAL)
    lines[3][-1].set_fill(PINK)
    scene.say("例：", "$2$", " 擠出 ", "$3$", "。原本 ", "$3$", " 正下方是 ", "$5>3$", "，所以 ", "$3$", " 不會落到更右邊")
    scene.play(FadeOut(row_box), FadeIn(lines[1], shift=0.15 * UP), ShowCreation(below), run_time=0.8)
    scene.play(GrowArrow(hop), FadeIn(lines[2], shift=0.15 * UP), run_time=0.8)
    scene.wait(1.4)
    scene.say("$3$", " 的落點上方是 ", "$2$", "，而 ", "$2\\le 2<3$", "：每一行仍由上往下嚴格遞增")
    scene.play(ShowCreation(above), FadeIn(lines[3], shift=0.15 * UP), run_time=0.8)
    scene.wait(2.0)
    scene.play(FadeOut(VGroup(panel, below, above, hop, b["legend"])), run_time=0.7)


def part_reverse(scene, b, data):
    d, ents = b["d"], b["ents"]
    T1, new, rsteps, route = data["T1"], data["new"], data["rsteps"], data["route"]
    new_cell = b["new_cell"]
    cur = [list(r) for r in T1]

    # ---- 先把路徑的底色拿掉，只留新格子的綠框
    scene.say("反過來：只要知道新格子在哪裡，整個過程可以倒著做回去")
    scene.play(*[d.cell(i, j).animate.set_fill(opacity=0) for i, j in route[:-1]],
               new_cell.animate.set_fill(opacity=0), run_time=0.7)
    corner_marks = VGroup(*[Square(side_length=CS * 0.78, stroke_color=NEW_COLOR, stroke_width=4).move_to(
        cell_pt(i, j)) for i, j in corners(shape(T1))])
    scene.say("倒推要從「外角」出發：正下方和右邊都沒有格子。這個表有 ", "$2$", " 個外角")
    scene.play(ShowCreation(corner_marks), run_time=0.8)
    scene.wait(1.0)
    scene.play(FadeOut(corner_marks), run_time=0.5)

    rule = mixed("倒推：往上一列找最右邊、嚴格小於它的數，換上去，把那個數再往上擠", font_size=24)
    rule.move_to(np.array([0.0, -1.85, 0.0])).set_x(TL[0], direction=LEFT)
    assert_in_frame(rule)
    assert_apart(rule, VGroup(d, new_cell), gap=0.3)
    log = VGroup()
    r0, c0 = new
    trav = ents.pop(new)
    scene.say("從新格子（第 ", "$4$", " 列第 ", "$3$", " 行）的 ", f"${cur[r0][c0]}$", " 出發，把它往上一列送")
    cur[r0].pop()
    scene.play(FadeIn(rule, shift=0.15 * UP),
               glide(trav, [cell_pt(r0, c0), (col_x(c0), lane_y(r0), 0), (IN_X, lane_y(r0), 0), slot(r0 - 1)],
                     start_color=WHITE, end_color=TRAVEL_COLOR),
               FadeOut(new_cell), run_time=1.3)

    for (r, k), placed, pushed in rsteps:
        assert cur[r][k] == pushed < placed and all(v >= placed for v in cur[r][k + 1:])
        right = [ents[(r, j)] for j in range(k + 1, len(cur[r]))]
        scene.say(f"第 {r + 1} 列：最右邊、比 ", f"${placed}$", " 小的是 ", f"${pushed}$", "，於是 ", f"${placed}$",
                  " 換上去、", f"${pushed}$", " 往上")
        scene.play(*[m.animate.set_fill(DIM_COLOR) for m in right],
                   d.cell(r, k).animate.set_fill(ROUTE_COLOR, opacity=0.4), run_time=0.5)
        old = ents[(r, k)]
        line = mixed(f"${placed}$", " 往上擠出 ", f"${pushed}$", font_size=26)
        line.move_to(np.array([LOG_X, row_y(r), 0.0]), aligned_edge=LEFT)
        log.add(line)
        scene.play(
            glide(trav, [slot(r), (IN_X, lane_y(r + 1), 0), (col_x(k), lane_y(r + 1), 0), cell_pt(r, k)],
                  start_color=TRAVEL_COLOR, end_color=WHITE),
            glide(old, [cell_pt(r, k), (col_x(k), lane_y(r), 0), (IN_X, lane_y(r), 0), slot(r - 1)],
                  start_color=WHITE, end_color=TRAVEL_COLOR),
            FadeIn(line, shift=0.2 * LEFT),
            *[m.animate.set_fill(WHITE) for m in right],
            run_time=1.3,
        )
        ents[(r, k)] = trav
        cur[r][k] = placed
        trav = old
        scene.wait(0.2)
    assert tuple(tuple(r) for r in cur if r) == T0
    x_val = int(trav.get_tex())
    assert x_val == X
    x_lab = Tex("x=", font_size=40, fill_color=TRAVEL_COLOR).next_to(trav, LEFT, buff=0.12)
    label0 = Tex("T", font_size=46).move_to(LABEL_POS)
    assert_in_frame(log, x_lab, trav)
    for line in log:
        assert_apart(line, d, gap=0.3)
    assert_apart(x_lab, b["label"], gap=0.3)
    scene.say("最後從第 1 列被擠出來的 ", "$2$", " 就是 ", "$x$", "，表也變回原來的 ", "$T$")
    scene.play(FadeIn(x_lab), TransformMatchingTex(b["label"], label0),
               *[d.cell(i, j).animate.set_fill(opacity=0) for i, j in route[:-1]], run_time=0.9)
    b["label"] = label0
    assert [[ents[(i, j)].get_tex() for j in range(len(row))] for i, row in enumerate(T0)] == \
        [[str(v) for v in row] for row in T0]
    scene.wait(1.4)
    b["rev"] = VGroup(log, rule, x_lab, trav)


def part_summary(scene, b):
    d = b["d"]
    left = Tex(r"(T,\ x)", font_size=40)
    right = mixed("$(T\\leftarrow x,$", " 新格子", "$)$", font_size=30, buff=0.1)
    gap = 2.6
    left.move_to(ORIGIN, aligned_edge=RIGHT)
    right.move_to(gap * RIGHT, aligned_edge=LEFT)
    a_fwd = Arrow(0.3 * RIGHT + 0.22 * UP, (gap - 0.3) * RIGHT + 0.22 * UP, buff=0, stroke_width=0,
                  thickness=3.5, fill_color=NEW_COLOR).set_color(NEW_COLOR)
    a_bwd = Arrow((gap - 0.3) * RIGHT + 0.22 * DOWN, 0.3 * RIGHT + 0.22 * DOWN, buff=0, stroke_width=0,
                  thickness=3.5, fill_color=ROUTE_COLOR).set_color(ROUTE_COLOR)
    tag_f = zh("列插入", font_size=22, color=NEW_COLOR).next_to(a_fwd, UP, buff=0.12)
    tag_b = zh("反向擠出", font_size=22, color=ROUTE_COLOR).next_to(a_bwd, DOWN, buff=0.12)
    g = VGroup(left, a_fwd, tag_f, a_bwd, tag_b, right)
    assert_apart(left, VGroup(a_fwd, a_bwd), gap=0.25)
    assert_apart(right, VGroup(a_fwd, a_bwd), gap=0.25)
    assert_apart(tag_f, tag_b)
    box = SurroundingRectangle(g, buff=0.3, color=YELLOW, stroke_width=3)
    summary = VGroup(box, g)
    summary.move_to(np.array([(LOG_X + X_MAX) / 2, 0.5, 0.0]))
    assert_in_frame(summary)
    assert_apart(summary, VGroup(d, b["rev"][2], b["rev"][3]), gap=0.3)
    scene.play(FadeOut(b["rev"][0]), FadeOut(b["rev"][1]), run_time=0.6)
    scene.say("所以列插入不會遺失資訊：記下新格子，就能完整還原 ", "$T$", " 和 ", "$x$")
    scene.play(ShowCreation(box), FadeIn(g, shift=0.15 * UP), run_time=1.0)
    scene.wait(2.4)


class SceneF04RowInsertion(ChuScene):
    def construct(self):
        self.show_header("列插入（row bumping）")
        data = check_math()
        b = build_board(self)
        part_intro(self, b)
        part_forward(self, b, data)
        part_result(self, b, data)
        part_why(self, b, data)
        part_reverse(self, b, data)
        part_summary(self, b)
        self.wait(1.0)
