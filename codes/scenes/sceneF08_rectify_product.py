"""
Scene F08 —— 用滑動算乘積：Rect(T∗U) = T·U（Fulton《Young Tableaux》§1.2，p.15–16）

    T∗U：中間挖一塊「T 的行數 × U 的列數」的空白矩形，T 接在矩形下面、U 接在矩形右邊
    書上的練習 1：T = [[1,2,2,3],[2,3,5,5],[4,4,6],[5,6]]、U = [[1,3],[2]]
        → 矩形 2 列 × 4 行 = 8 格 → 滑 8 次（每次挑最上面的內角）
        洞的起點 → 終點（列, 行，1 起算）：(2,4)→(2,5)、(1,4)→(1,6)、(2,3)→(4,4)、(1,3)→(3,4)、
                                          (2,2)→(6,2)、(1,2)→(5,3)、(2,1)→(6,1)、(1,1)→(5,2)
    結果 [[1,1,2,2,3],[2,2,3,5],[3,4,5],[4,6,6],[5]] = 列插入算出的 T·U（Claim 3）；
    改成每次挑最下面的內角，結果相同（Claim 2）
    結尾：Claim 1–3，書在第 2、3 章證明

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF08_rectify_product.py SceneF08RectifyProduct
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh
from utils.tableaux import (
    FULTON_INSERT_T,
    FULTON_PRODUCT_U,
    inside_corners,
    is_skew_tableau,
    is_tableau,
    jdt_steps,
    product,
    rectify,
    shape,
    skew_cells,
    skew_shape,
    star,
    tableau_word,
    young_boxes,
)

T_TAB = FULTON_INSERT_T                       # p.15 練習 1 的 T（= p.7、p.12 的 T）
U_TAB = FULTON_PRODUCT_U                      # p.15 練習 1 的 U
BOOK_SKEW = ((None, None, None, None, 1, 3),  # p.16 印出來的 T∗U
             (None, None, None, None, 2),
             (1, 2, 2, 3),
             (2, 3, 5, 5),
             (4, 4, 6),
             (5, 6))
TU = ((1, 1, 2, 2, 3), (2, 2, 3, 5), (3, 4, 5), (4, 6, 6), (5,))   # p.12 用列插入算出的 T·U
HOLE_PATHS_BOOK = [((2, 4), (2, 5)), ((1, 4), (1, 6)), ((2, 3), (4, 4)), ((1, 3), (3, 4)),
                   ((2, 2), (6, 2)), ((1, 2), (5, 3)), ((2, 1), (6, 1)), ((1, 1), (5, 2))]
N_EXPLAIN = 3                                 # 前 3 次滑動逐步說明（第 3 次有「一樣大取下面」）

CS = 0.66                                     # 主圖的格子大小
GRID_TL = np.array([-6.0, 2.75, 0.0])         # 主圖 (0,0) 格的左上角
ENTRY_FONT = 32
SRC_CS, SRC_FONT = 0.5, 24
T_COLOR = TEAL_B
U_COLOR = PINK
HOLE_COLOR = YELLOW
CAND_COLOR = ORANGE
MU_FILL, MU_OPACITY = GREY_D, 0.85
LOG_X = (-0.7, 2.9)
LOG_Y0, LOG_DY = -0.62, 0.5
SHIFT_RESULT = 1.0                            # 比對時把結果往右移，與 T·U 左右對稱

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


def top_corner(cs):
    """每次挑最上面的內角（書上練習 1 的順序：一行一行從右邊清掉矩形）。"""
    return cs[0]


def book(box):
    """0 起算的 (i, j) -> 書上 1 起算的 (列, 行)。"""
    return box[0] + 1, box[1] + 1


def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊（至少一個方向分開 gap）。"""
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a, b)


def check_math():
    S = star(T_TAB, U_TAB)
    assert S == BOOK_SKEW and is_skew_tableau(S)
    assert is_tableau(T_TAB) and is_tableau(U_TAB)
    assert len(T_TAB[0]) == 4 and len(U_TAB) == 2                     # 矩形 2 列 × 4 行
    assert skew_shape(S) == ((6, 5, 4, 4, 3, 2), (4, 4))
    steps = jdt_steps(S, choose=top_corner)
    assert len(steps) == 8 == len(T_TAB[0]) * len(U_TAB)
    assert [(book(c), book(p[-1])) for c, p, _ in steps] == HOLE_PATHS_BOOK
    assert [len(p) - 1 for _, p, _ in steps] == [1, 2, 3, 3, 4, 5, 4, 5]
    R = steps[-1][2]
    assert R == TU == product(T_TAB, U_TAB) and is_tableau(R) and shape(R) == (5, 4, 3, 3, 1)
    bottom = jdt_steps(S)                                               # 預設：每次挑最下面的內角
    assert [c for c, _, _ in bottom] != [c for c, _, _ in steps]
    assert bottom[-1][2] == R == rectify(S)                            # Claim 2 在這個例子
    assert tableau_word(U_TAB) == (2, 1, 3)
    V = ((2, 4), (3,))                                                  # 練習 2 的想法（畫面上沒有數字）
    assert rectify(star(T_TAB, U_TAB, V)) == product(product(T_TAB, U_TAB), V) == product(T_TAB, product(U_TAB, V))
    return S, steps


# =============================================================================
# 主圖的格子與數字
# =============================================================================
def cell_center(i, j):
    return GRID_TL + (j + 0.5) * CS * RIGHT + (i + 0.5) * CS * DOWN


def shown_cells(st):
    """畫面上每格的數字 {(i, j): 數字}（由數字物件身上的 tab_value 讀出）。"""
    return {pos: mob.tab_value for pos, mob in st["entries"].items()}


def check_state(st, S):
    """畫面上的格子、灰格（μ）與數字都和 tableaux.py 算出的斜表一致。"""
    lam, mu = skew_shape(S)
    assert set(st["cells"]) == set(young_boxes(lam))
    assert st["empty"] == set(young_boxes(mu))
    assert shown_cells(st) == skew_cells(S)
    for pos, mob in st["entries"].items():
        assert np.allclose(mob.get_center(), cell_center(*pos), atol=1e-3), pos


def outline(pos, color, size=0.82, width=5.0):
    sq = Square(side_length=CS * size, stroke_color=color, stroke_width=width)
    sq.set_fill(color, opacity=0.0)
    sq.move_to(cell_center(*pos))
    return sq


# =============================================================================
# 第 1 段：排出 T∗U
# =============================================================================
def part_build(scene, S):
    src_T = YoungDiagramMob(shape(T_TAB), cell_size=SRC_CS, top_left=np.array([0.75, 2.75, 0.0]),
                            entries=T_TAB, font_size=SRC_FONT, entry_color=T_COLOR)
    src_U = YoungDiagramMob(shape(U_TAB), cell_size=SRC_CS, top_left=np.array([4.45, 2.75, 0.0]),
                            entries=U_TAB, font_size=SRC_FONT, entry_color=U_COLOR)
    lab_T = Tex("T=", font_size=40, fill_color=T_COLOR).next_to(src_T, LEFT, buff=0.2)
    lab_U = Tex("U=", font_size=40, fill_color=U_COLOR).next_to(src_U, LEFT, buff=0.2)

    rows_u, cols_t = len(U_TAB), len(T_TAB[0])
    rect = YoungDiagramMob((cols_t,) * rows_u, cell_size=CS, top_left=GRID_TL, stroke_color=GREY_B,
                           fill_color=MU_FILL, fill_opacity=MU_OPACITY)
    t_mob = YoungDiagramMob(shape(T_TAB), cell_size=CS, top_left=GRID_TL + rows_u * CS * DOWN,
                            entries=T_TAB, font_size=ENTRY_FONT, entry_color=T_COLOR)
    u_mob = YoungDiagramMob(shape(U_TAB), cell_size=CS, top_left=GRID_TL + cols_t * CS * RIGHT,
                            entries=U_TAB, font_size=ENTRY_FONT, entry_color=U_COLOR)

    # 主圖拆成「每格一個方塊、每個數字一個物件」，滑動時逐一移動
    cells, entries, empty = {}, {}, set()
    for i in range(rows_u):
        for j in range(cols_t):
            cells[(i, j)] = rect.cell(i, j)
            empty.add((i, j))
    for mob, tab, di, dj in ((t_mob, T_TAB, rows_u, 0), (u_mob, U_TAB, 0, cols_t)):
        for i, row in enumerate(tab):
            for j, v in enumerate(row):
                cells[(i + di, j + dj)] = mob.cell(i, j)
                e = mob.entry(i, j)
                e.tab_value = v
                entries[(i + di, j + dj)] = e
    st = {"cells": cells, "entries": entries, "empty": empty}
    check_state(st, S)

    n_rows, n_cols = len(S), len(S[0])
    col_labs = VGroup(*[Tex(str(j + 1), font_size=20, fill_color=GREY_B).move_to(
        cell_center(0, j) + (CS / 2 + 0.17) * UP) for j in range(n_cols)])
    row_labs = VGroup(*[Tex(str(i + 1), font_size=20, fill_color=GREY_B).move_to(
        cell_center(i, 0) + (CS / 2 + 0.2) * LEFT) for i in range(n_rows)])
    idx = VGroup(col_labs, row_labs)
    grid_lab = Tex(r"T\ast U", font_size=40).move_to(cell_center(n_rows - 1, 2.5) + (CS / 2 + 0.4) * DOWN)

    lam, mu = skew_shape(S)
    e1 = mixed("矩形的行數 ", "$=$", " ", "$T$", " 的行數 ", "$=$", " ", f"${cols_t}$", font_size=24)
    e2 = mixed("矩形的列數 ", "$=$", " ", "$U$", " 的列數 ", "$=$", " ", f"${rows_u}$", font_size=24)
    e3 = mixed("$T$", " 接在矩形下面，", "$U$", " 接在矩形右邊", font_size=24)
    e4 = mixed("形狀 ", "$" + str(lam).replace(" ", "") + "/" + str(mu).replace(" ", "") + "$", font_size=24)
    expl = VGroup(e1, e2, e3, e4).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    expl.move_to(np.array([-0.4, 0.15, 0.0]), aligned_edge=UL)
    whole = VGroup(*cells.values(), *entries.values())
    assert_in_frame(src_T, src_U, lab_T, lab_U, whole, idx, grid_lab, expl)
    assert_apart(VGroup(whole, idx, grid_lab), VGroup(lab_T, src_T, expl), gap=0.3)
    assert_apart(src_T, expl, gap=0.2)
    assert_apart(src_T, lab_U, gap=0.2)

    scene.say("前面用列插入算過 ", "$T\\cdot U$", "；現在改用滑動，再算一次")
    scene.play(FadeIn(lab_T), FadeIn(src_T), FadeIn(lab_U), FadeIn(src_U), run_time=0.9)
    scene.wait(0.8)
    scene.say("先排出斜表 ", "$T\\ast U$", "：左上角是一塊空白矩形")
    scene.play(FadeIn(idx), LaggedStart(*[FadeIn(c, scale=0.7) for c in rect.cells], lag_ratio=0.08),
               run_time=1.2)
    scene.play(FadeIn(e1, shift=0.15 * UP), FadeIn(e2, shift=0.15 * UP), run_time=0.7)
    scene.wait(1.0)
    scene.say("$T$", " 接在矩形下面，", "$U$", " 接在矩形右邊")
    scene.play(TransformFromCopy(src_T, t_mob), TransformFromCopy(src_U, u_mob), FadeIn(e3, shift=0.15 * UP),
               run_time=1.5)
    scene.wait(0.6)
    scene.say("這就是斜表 ", "$T\\ast U$", "：內部的空白形狀 ", "$(4,4)$", " 正是那塊矩形")
    scene.play(FadeIn(grid_lab), FadeIn(e4, shift=0.15 * UP), run_time=0.7)
    scene.wait(1.2)

    # 拆開三個 YoungDiagramMob：之後每格、每個數字各自動
    scene.remove(rect, t_mob, u_mob)
    scene.add(*cells.values())
    scene.add(*entries.values())
    st.update(idx=idx, grid_lab=grid_lab, intro=VGroup(src_T, src_U, lab_T, lab_U, expl))
    return st


# =============================================================================
# 第 2 段：8 次滑動
# =============================================================================
def step_caption(right, below):
    if right is not None and below is not None:
        if right == below:
            return ("右邊、下面都是 ", f"${right}$", "：一樣大，取下面的")
        small = min(right, below)
        return ("右邊 ", f"${right}$", "、下面 ", f"${below}$", "：較小的 ", f"${small}$", " 滑進洞")
    if right is not None:
        return ("下面沒有數，右邊的 ", f"${right}$", " 滑進洞")
    return ("右邊沒有數，下面的 ", f"${below}$", " 滑進洞")


def log_line(k, corner, end):
    r0, c0 = book(corner)
    r1, c1 = book(end)
    head = VGroup(Tex(f"{k + 1}.", font_size=28, fill_color=GREY_B), Tex(f"({r0},{c0})", font_size=30))
    head.arrange(RIGHT, buff=0.15)
    tail = VGroup(Tex(r"\to", font_size=30), Tex(f"({r1},{c1})", font_size=30))
    tail.arrange(RIGHT, buff=0.12)
    line = VGroup(head, tail).arrange(RIGHT, buff=0.12)
    col, row = divmod(k, 4)
    line.move_to(np.array([LOG_X[col], LOG_Y0 - row * LOG_DY, 0.0]), aligned_edge=LEFT)
    return line


def run_slide(scene, k, S_before, corner, path, S_after, st, explain):
    cells, entries, empty = st["cells"], st["entries"], st["empty"]
    corners = inside_corners(S_before)
    assert corner == top_corner(corners)
    line = log_line(k, corner, path[-1])
    st["log"].add(line)

    hole = Square(side_length=CS * 0.9, stroke_color=HOLE_COLOR, stroke_width=5)
    hole.set_fill(HOLE_COLOR, opacity=0.28)
    hole.move_to(cell_center(*corner))
    if explain:
        r, c = book(corner)
        if len(corners) == 1:
            scene.say("只有一個內角（第 ", f"${r}$", " 列第 ", f"${c}$", " 行）：從這裡挖洞")
        else:
            scene.say("現在有 ", f"${len(corners)}$", " 個內角，這裡挑最上面的那個")
        others = VGroup(*[outline(b, HOLE_COLOR, size=0.9, width=3) for b in corners if b != corner])
        if len(others):
            scene.play(ShowCreation(others), run_time=0.5)
    empty.discard(corner)
    scene.play(FadeIn(hole, scale=0.6), cells[corner].animate.set_fill(opacity=0.0).set_stroke(GREY_A),
               FadeIn(line[0]), *([FadeOut(others)] if explain and len(others) else []),
               run_time=0.6 if explain else 0.35)
    if explain:
        scene.wait(0.3)

    vals = dict(skew_cells(S_before))
    for h, nxt in zip(path[:-1], path[1:]):
        right, below = vals.get((h[0], h[1] + 1)), vals.get((h[0] + 1, h[1]))
        rule = (h[0] + 1, h[1]) if right is None or (below is not None and below <= right) else (h[0], h[1] + 1)
        assert rule == nxt
        cands = VGroup()
        if explain:
            cands = VGroup(*[outline(b, CAND_COLOR) for b, v in (((h[0], h[1] + 1), right), ((h[0] + 1, h[1]), below))
                             if v is not None])
            scene.say(*step_caption(right, below))
            scene.play(ShowCreation(cands), run_time=0.4)
            scene.wait(0.35)
        mob = entries.pop(nxt)
        assert mob.tab_value == vals[nxt]
        entries[h] = mob
        vals[h] = vals.pop(nxt)
        scene.play(mob.animate.move_to(cell_center(*h)), hole.animate.move_to(cell_center(*nxt)),
                   *([FadeOut(cands)] if explain else []), run_time=0.6 if explain else 0.3)

    end = path[-1]
    assert vals.get((end[0], end[1] + 1)) is None and vals.get((end[0] + 1, end[1])) is None
    if explain:
        scene.say("右邊、下面都沒有數了：把這一格拿掉")
    sq = cells.pop(end)
    scene.play(FadeOut(sq, scale=0.4), FadeOut(hole, scale=0.4), FadeIn(line[1], shift=0.1 * RIGHT),
               run_time=0.6 if explain else 0.35)
    check_state(st, S_after)
    if explain:
        scene.wait(0.3)


def part_slides(scene, S, steps, st):
    rule_title = zh("滑動規則", font_size=26, color=HOLE_COLOR)
    rules = VGroup(
        zh("從一個內角挖洞（黃色）", font_size=23),
        zh("洞的右邊、下面：較小的數滑進洞", font_size=23),
        zh("一樣大：取下面的", font_size=23),
        zh("右邊、下面都沒有數：拿掉這一格", font_size=23),
    ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    rule_block = VGroup(rule_title, rules).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    rule_block.move_to(np.array([-0.45, 2.9, 0.0]), aligned_edge=UL)
    rule_box = SurroundingRectangle(rule_block, buff=0.2, color=GREY_B, stroke_width=2)
    log_head = mixed("洞的起點 ", "$\\to$", " 終點（列, 行）", font_size=23, color=MUTED_COLOR)
    log_head.move_to(np.array([LOG_X[0], LOG_Y0 + 0.58, 0.0]), aligned_edge=LEFT)
    st["log"] = VGroup()

    whole = VGroup(*st["cells"].values(), *st["entries"].values(), st["idx"], st["grid_lab"])
    lines = VGroup(*[log_line(k, c, p[-1]) for k, (c, p, _) in enumerate(steps)])
    assert_in_frame(rule_box, log_head, lines)
    assert_apart(whole, VGroup(rule_box, log_head, lines), gap=0.3)
    assert_apart(rule_box, log_head, gap=0.15)
    assert_apart(log_head, lines, gap=0.1)
    assert_apart(lines[:4], lines[4:], gap=0.3)

    scene.play(FadeOut(st["intro"]), run_time=0.6)
    scene.say("矩形有 ", "$8$", " 格，就要滑 ", "$8$", " 次：每次從一個內角挖洞")
    scene.play(ShowCreation(rule_box), FadeIn(rule_block), FadeIn(log_head), run_time=0.9)
    scene.wait(1.0)

    cur = S
    for k, (corner, path, after) in enumerate(steps):
        if k == N_EXPLAIN:
            scene.say("其餘 ", f"${len(steps) - N_EXPLAIN}$", " 次照同樣的規則，每次都挑最上面的內角")
        run_slide(scene, k, cur, corner, path, after, st, explain=k < N_EXPLAIN)
        cur = after
    assert cur == TU and not st["empty"]
    st["rules"] = VGroup(rule_box, rule_block, log_head, st["log"])

    rect_lab = Tex(r"\mathrm{Rect}(T\ast U)", font_size=40).move_to(st["grid_lab"])
    scene.say("矩形的 ", "$8$", " 格都滑出去了，沒有內角：得到一個 Young 表")
    scene.play(ReplacementTransform(st["grid_lab"], rect_lab), run_time=0.8)
    st["grid_lab"] = rect_lab
    scene.wait(1.2)
    return cur


# =============================================================================
# 第 3 段：和列插入的 T·U 比對
# =============================================================================
def part_compare(scene, R, st):
    left = VGroup(*st["cells"].values(), *st["entries"].values())
    n = len(R)
    right_x = -(GRID_TL[0] + SHIFT_RESULT) - len(R[0]) * CS            # 與左邊的結果左右對稱
    right_tl = np.array([right_x, GRID_TL[1], 0.0])
    tu_mob = YoungDiagramMob(shape(TU), cell_size=CS, top_left=right_tl, entries=TU, font_size=ENTRY_FONT)
    mid_y = cell_center((n - 1) / 2, 0)[1]
    eq = Tex("=", font_size=72).move_to(np.array([0.0, mid_y, 0.0]))
    lab_y = cell_center(n - 1, 0)[1] - CS / 2 - 0.4
    left_lab = mixed("$\\mathrm{Rect}(T\\ast U)$", "：滑動得到", font_size=24)
    right_lab = mixed("$T\\cdot U$", "：把 ", "$w(U)=2\\ 1\\ 3$", " 依序插入 ", "$T$", font_size=24)
    claim3 = mixed("Claim 3：", "$\\mathrm{Rect}(T\\ast U)=T\\cdot U$", font_size=28)
    claim3_box = SurroundingRectangle(claim3, buff=0.18, color=YELLOW, stroke_width=3)
    claim2 = mixed("改成每次挑最下面的內角，滑完也是同一個表（Claim 2）", font_size=22, color=MUTED_COLOR)

    # 位置（先算好、assert，再動畫）
    left_after = left.copy().shift(SHIFT_RESULT * RIGHT)
    left_lab.move_to(np.array([left_after.get_center()[0], lab_y, 0.0]))
    right_lab.move_to(np.array([tu_mob.get_center()[0], lab_y, 0.0]))
    VGroup(claim3, claim3_box).move_to(np.array([0.0, lab_y - 0.85, 0.0]))
    claim2.next_to(claim3_box, DOWN, buff=0.3)
    assert abs(left_after.get_center()[0] + tu_mob.get_center()[0]) < 1e-6        # 左右對稱
    assert shown_cells(st) == skew_cells(R) == skew_cells(TU)
    assert_in_frame(left_after, tu_mob, eq, left_lab, right_lab, claim3_box, claim2)
    assert_apart(left_after, eq, gap=0.3)
    assert_apart(tu_mob, eq, gap=0.3)
    assert_apart(left_lab, right_lab, gap=0.3)
    assert_apart(VGroup(left_after, tu_mob), VGroup(left_lab, right_lab), gap=0.15)
    assert_apart(VGroup(left_lab, right_lab), claim3_box, gap=0.15)
    assert_apart(claim3_box, claim2, gap=0.1)
    assert claim2.get_width() < 13.0

    scene.play(FadeOut(st["rules"]), FadeOut(st["idx"]), FadeOut(st["grid_lab"]), run_time=0.6)
    scene.say("和列插入算出的 ", "$T\\cdot U$", " 放在一起比對")
    scene.play(*[m.animate.set_fill(WHITE) for m in st["entries"].values()], run_time=0.4)
    scene.play(left.animate.shift(SHIFT_RESULT * RIGHT), run_time=0.8)
    scene.play(FadeIn(left_lab), FadeIn(tu_mob, shift=0.2 * LEFT), FadeIn(right_lab), FadeIn(eq), run_time=0.9)
    scene.wait(0.5)

    checks = VGroup()
    for i, row in enumerate(R):
        lrow = VGroup(*[st["cells"][(i, j)] for j in range(len(row))])
        rrow = VGroup(*[tu_mob.cell(i, j) for j in range(len(row))])
        checks.add(SurroundingRectangle(lrow, buff=0.04, color=OK_COLOR, stroke_width=4),
                   SurroundingRectangle(rrow, buff=0.04, color=OK_COLOR, stroke_width=4))
    scene.say("逐列比對：", "$5$", " 列的數字完全相同")
    scene.play(LaggedStart(*[ShowCreation(c) for c in checks], lag_ratio=0.15), run_time=1.6)
    scene.wait(0.5)
    scene.say("這就是 Claim 3：用滑動算出的乘積，等於用列插入算出的乘積")
    scene.play(FadeOut(checks), FadeIn(claim3), ShowCreation(claim3_box), run_time=0.8)
    scene.wait(1.3)
    scene.say("內角的挑法不影響結果：換成每次挑最下面的，也得到同一個表")
    scene.play(FadeIn(claim2, shift=0.15 * UP), run_time=0.6)
    scene.wait(1.6)


# =============================================================================
# 第 4 段：三個 Claim
# =============================================================================
def part_claims(scene):
    title = zh("第 1 章留下的三個 Claim", font_size=34, color=YELLOW)
    title.move_to(2.45 * UP)
    tags = [zh(f"Claim {k}", font_size=26, color=YELLOW) for k in (1, 2, 3)]
    bodies = [
        mixed("乘積有結合律 ", "$(T\\cdot U)\\cdot V=T\\cdot(U\\cdot V)$", "，空表是單位元", font_size=26),
        mixed("$\\mathrm{Rect}(S)$", " 與內角的挑法無關", font_size=26),
        mixed("$\\mathrm{Rect}(T\\ast U)=T\\cdot U$", "：滑動與列插入給出同一個乘積", font_size=26),
    ]
    rows = VGroup()
    for tag, body in zip(tags, bodies):
        rows.add(VGroup(tag, body).arrange(RIGHT, buff=0.45))
    rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
    rows.next_to(title, DOWN, buff=0.55)
    note = zh("書上第 1 章先承認這三件事，證明放在第 2、3 章", font_size=24, color=MUTED_COLOR)
    note2 = mixed("練習 2：把三個表排成 ", "$T\\ast U\\ast V$", "，由 Claim 2、3 就能推出 Claim 1",
                  font_size=24, color=MUTED_COLOR)
    notes = VGroup(note, note2).arrange(DOWN, buff=0.25)
    notes.next_to(rows, DOWN, buff=0.55)
    frame_box = SurroundingRectangle(VGroup(title, rows, notes), buff=0.3, color=GREY_B, stroke_width=2)
    assert_in_frame(frame_box)
    assert_apart(title, rows, gap=0.2)
    assert_apart(rows, notes, gap=0.2)

    scene.say("第 1 章到這裡，留下三個還沒證明的 Claim")
    scene.play(ShowCreation(frame_box), FadeIn(title), run_time=0.8)
    for r in rows:
        scene.play(FadeIn(r, shift=0.2 * RIGHT), run_time=0.7)
        scene.wait(0.7)
    scene.say("書上先承認它們，第 2、3 章再補上證明")
    scene.play(FadeIn(note), run_time=0.6)
    scene.wait(1.0)
    scene.say("而且 Claim 1 不必另外證：排成 ", "$T\\ast U\\ast V$", " 再用 Claim 2、3 就推得出來")
    scene.play(FadeIn(note2), run_time=0.6)
    scene.wait(2.0)


class SceneF08RectifyProduct(ChuScene):
    def construct(self):
        self.show_header("用滑動算乘積：Rect(T*U) = T·U")
        S, steps = check_math()
        st = part_build(self, S)
        R = part_slides(self, S, steps, st)
        part_compare(self, R, st)
        self.clear_stage()
        part_claims(self)
        self.wait(1.0)
