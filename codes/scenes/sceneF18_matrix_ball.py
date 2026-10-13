"""
Scene F18 —— 矩陣球構造（Fulton《Young Tableaux》§4.2，書 p.42–47）

    A = CH4_MATRIX = ((1,2),(1,1),(3,1))：(i,j) 放 a(i,j) 顆球（同一格由西北往東南斜排）
    編號：每顆球 = 比西北方（列 ≤、行 ≤）所有球的號碼都大的最小整數（ball_numbering）
        (1,1):1  (1,2):2,3  (2,1):2  (2,2):4  (3,1):3,4,5  (3,2):6
    P 的第 1 列 = 各號碼最左的行 (1,1,1,1,1,2)；Q 的第 1 列 = 各號碼最上的列 (1,1,1,2,3,3)
    導出矩陣 A♭：同號的球由西南排到東北，每顆球（最後一顆除外）往右、下一顆往下，交會處放新球
        號碼 2：(2,1),(1,2) → (2,2)；號碼 3：(3,1),(1,2) → (3,2)；號碼 4：(3,1),(2,2) → (3,2)
        A♭ = ((0,0),(0,1),(0,2))，再編號 → 第 2 列 (2,2,2)、(2,3,3)；A♭ 沒有同號的球 → 停
    → (P, Q) = (CH4_P, CH4_Q)，與 F17 的列插入相同；構造對列、行對稱 → 對稱定理
    Exercise 4：對稱矩陣 S = ((2,1),(1,1)) → P = Q = ((1,1,1,2),(2))：tr S + tr S♭ = 3 + 1 = 4 = P 第一列長，
        tr S = 3 = P 裡奇數長的行數；排列矩陣時就是 Viennot 的影子線（一句）

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算；畫面與字幕的列號、行號 1 起算）。

試渲染（在 C:\\mypython\\manim\\projects\\combkit）：
    python tools/render_check.py ../catalan930/codes/scenes/sceneF18_matrix_ball.py SceneF18MatrixBall
           --config ../catalan930/codes/custom_config.yml
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import BallMatrixMob, assert_apart, assert_in_frame, labeled, tableau_mob
from utils.mit_draw import CELL_STROKE
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH4_MATRIX, CH4_P, CH4_Q, ball_numbering, conjugate, derived_matrix, matrix_ball, rsk_matrix, shape,
    transpose_matrix,
)

A = CH4_MATRIX
P_ALL, Q_ALL, STAGES = matrix_ball(A)
NUM, A_FLAT, NUM_FLAT = STAGES[0]["balls"], STAGES[1]["A"], STAGES[1]["balls"]
AT = transpose_matrix(A)
S = ((2, 1), (1, 1))
S_P, S_Q, S_STAGES = matrix_ball(S)
S_FLAT = S_STAGES[1]["A"]
CELL, FS, BALL = 1.25, 30, BLUE_C


def trace(M):
    return sum(M[i][i] for i in range(min(len(M), len(M[0]))))


def balls_of(numbering, k):
    """號碼 k 的球：[(i, j, t)]（t = 那一格裡的第幾顆）。"""
    return [(i, j, xs.index(k)) for (i, j), xs in numbering.items() if k in xs]


def derived_moves(numbering):
    """同號的球由西南到東北排好，相鄰兩顆 → 新球在（前一顆的列, 後一顆的行）。回傳 [(號碼, 前, 後, 新球的格子)]。"""
    by = {}
    for pos, xs in numbering.items():
        for x in xs:
            by.setdefault(x, []).append(pos)
    out = []
    for k in sorted(by):
        balls = sorted(by[k], key=lambda b: b[1])
        out += [(k, b1, b2, (b1[0], b2[1])) for b1, b2 in zip(balls, balls[1:])]
    return out


def check_math():
    assert (P_ALL, Q_ALL) == (CH4_P, CH4_Q) == rsk_matrix(A) and len(STAGES) == 2
    assert NUM == ball_numbering(A) == {(0, 0): [1], (0, 1): [2, 3], (1, 0): [2], (1, 1): [4], (2, 0): [3, 4, 5],
                                        (2, 1): [6]}
    for (i, j), xs in NUM.items():                       # 西北方最大 + 1，同一格連號
        top = max([x for (r, c), ys in NUM.items() if r <= i and c <= j and (r, c) != (i, j) for x in ys], default=0)
        assert xs == list(range(top + 1, top + 1 + A[i][j]))
    assert STAGES[0]["P_row"] == (1, 1, 1, 1, 1, 2) and STAGES[0]["Q_row"] == (1, 1, 1, 2, 3, 3)
    moves = derived_moves(NUM)
    assert moves == [(2, (1, 0), (0, 1), (1, 1)), (3, (2, 0), (0, 1), (2, 1)), (4, (2, 0), (1, 1), (2, 1))]
    B = [[0, 0] for _ in A]
    for *_, (i, j) in moves:
        B[i][j] += 1
    assert tuple(map(tuple, B)) == A_FLAT == derived_matrix(A) == ((0, 0), (0, 1), (0, 2))
    assert NUM_FLAT == ball_numbering(A_FLAT) == {(1, 1): [1], (2, 1): [2, 3]}
    assert STAGES[1]["P_row"] == (2, 2, 2) and STAGES[1]["Q_row"] == (2, 3, 3)
    assert derived_moves(NUM_FLAT) == [] and not any(map(any, derived_matrix(A_FLAT)))
    # 對稱：轉置後號碼跟著轉置，(P, Q) 對調
    assert ball_numbering(AT) == {(j, i): xs for (i, j), xs in NUM.items()}
    assert matrix_ball(AT)[:2] == (CH4_Q, CH4_P) == rsk_matrix(AT)
    # Exercise 4
    assert S == transpose_matrix(S) and S_P == S_Q == ((1, 1, 1, 2), (2,)) and rsk_matrix(S) == (S_P, S_Q)
    assert ball_numbering(S) == {(0, 0): [1, 2], (0, 1): [3], (1, 0): [3], (1, 1): [4]}
    assert S_FLAT == ((0, 0), (0, 1)) and len(S_STAGES) == 2
    assert trace(S) == 3 and trace(S_FLAT) == 1 and trace(S) + trace(S_FLAT) == len(S_P[0]) == 4
    assert sum(1 for h in conjugate(shape(S_P)) if h % 2) == trace(S)


# =============================================================================
# 小工具
# =============================================================================
def ball_matrix(M, numbering, cell, center, name):
    bm = BallMatrixMob(M, numbering, cell=cell, ball_radius=0.2 if cell > 1 else 0.16, center=center,
                       font_size=24 if cell > 1 else 21)
    bm.name = Tex(name, font_size=40).move_to(np.array([bm.grid.get_left()[0] - 0.45, bm.labels[bm.m].get_y(), 0.0]))
    return bm


def show_grid(bm):
    return [FadeIn(bm.grid), FadeIn(bm.labels), FadeIn(bm.name)]


def nw_region(bm, i, j):
    ul, dr = bm.cell_square(0, 0).get_corner(UL), bm.cell_square(i, j).get_corner(DR)
    r = Rectangle(width=dr[0] - ul[0], height=ul[1] - dr[1]).move_to((ul + dr) / 2)
    return r.set_fill(YELLOW, opacity=0.12).set_stroke(YELLOW, width=2.5)


def pq_boards():
    """右邊的 P、Q：每一列一排空格子（之後逐格寫入）。"""
    cs, boards = 0.5, {}
    for name, y, note, col in (("P", 1.35, "各號碼最左的行", TEAL), ("Q", -0.55, "各號碼最上的列", GOLD)):
        tl = np.array([1.45, y, 0.0])
        rows = [VGroup(*[Square(side_length=cs, stroke_color=CELL_STROKE, stroke_width=2.5)
                         .move_to(tl + (j + 0.5) * cs * RIGHT + (r + 0.5) * cs * DOWN) for j in range(n)])
                for r, n in enumerate(shape(P_ALL))]
        boards[name] = {"rows": rows, "lab": Tex(name, font_size=44).move_to(tl + np.array([-0.45, -cs / 2, 0.0])),
                        "note": zh(note, font_size=20, color=col).next_to(rows[0], RIGHT, buff=0.25)}
    return boards


def read_row(scene, bm, numbering, p_cells, q_cells, p_expect, q_expect, slow=True):
    """號碼 k = 1, 2, …：亮出號碼 k 的球，最左的行號寫進 P、最上的列號寫進 Q。"""
    top = max(x for xs in numbering.values() for x in xs)
    assert len(p_cells) == len(q_cells) == top == len(p_expect)
    prev_balls, prev_labs = [], []
    for k in range(1, top + 1):
        where = balls_of(numbering, k)
        c, r = min(j for _, j, _ in where), min(i for i, _, _ in where)
        assert (c + 1, r + 1) == (p_expect[k - 1], q_expect[k - 1])
        balls = [bm.ball(i, j, t)[0] for i, j, t in where]
        labs = {bm.labels[bm.m + c]: TEAL, bm.labels[r]: GOLD}
        scene.play(*[b.animate.set_fill(BALL) for b in prev_balls if b not in balls],
                   *[lb.animate.set_fill(MUTED_COLOR) for lb in prev_labs if lb not in labs],
                   *[b.animate.set_fill(YELLOW) for b in balls], *[lb.animate.set_fill(col) for lb, col in labs.items()],
                   run_time=0.3)
        pv = Tex(str(c + 1), font_size=FS).move_to(p_cells[k - 1])
        qv = Tex(str(r + 1), font_size=FS).move_to(q_cells[k - 1])
        scene.play(TransformFromCopy(bm.labels[bm.m + c], pv), TransformFromCopy(bm.labels[r], qv),
                   run_time=0.6 if slow else 0.45)
        prev_balls, prev_labs = balls, list(labs)
    scene.play(*[b.animate.set_fill(BALL) for b in prev_balls], *[lb.animate.set_fill(MUTED_COLOR) for lb in prev_labs],
               run_time=0.3)


# =============================================================================
# 第 1 段：放球、編號
# =============================================================================
def part_numbering(scene):
    bm = ball_matrix(A, NUM, CELL, np.array([-5.05, 0.0, 0.0]), "A")
    rule = VGroup(mixed("號碼 ＝ 比西北方每一顆球的號碼都大的最小整數", font_size=26),
                  mixed("西北方：列號 ≤、行號 ≤（同一格裡排在前面的也算）", font_size=22, color=MUTED_COLOR))
    rule.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(np.array([2.1, 2.6, 0.0]))
    assert_in_frame(bm, bm.name, rule)
    assert_apart(VGroup(bm, bm.name), rule, gap=0.3)

    scene.say("矩陣球：", "$a(i,j)$", " 是幾，第 ", "$i$", " 列第 ", "$j$", " 行就放幾顆球")
    scene.play(*show_grid(bm), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(b[0], scale=0.5) for b in bm.balls], lag_ratio=0.12), run_time=1.0)
    scene.wait(0.8)
    scene.say("同一格的球由西北往東南斜排；接著替每顆球編號：")
    scene.play(FadeIn(rule, shift=0.1 * DOWN), run_time=0.7)
    scene.wait(1.6)
    region = None
    for i, j in [(i, j) for i in range(len(A)) for j in range(len(A[0])) if A[i][j]]:
        nums = NUM[(i, j)]
        top = nums[0] - 1
        if top == 0:
            scene.say(f"$({i + 1},{j + 1})$", "：西北方沒有球，編 1")
        else:
            scene.say(f"$({i + 1},{j + 1})$", f"：西北方最大的號碼是 {top}，這一格編 {'、'.join(map(str, nums))}")
        reg = nw_region(bm, i, j)
        scene.play(FadeIn(reg) if region is None else Transform(region, reg), run_time=0.45)
        region = reg if region is None else region
        scene.play(LaggedStart(*[FadeIn(bm.ball(i, j, t)[1], scale=1.6) for t in range(len(nums))], lag_ratio=0.35),
                   run_time=0.55)
        scene.wait(1.0)
    scene.play(FadeOut(region), run_time=0.3)
    return bm, rule


# =============================================================================
# 第 2 段：讀出第 1 列
# =============================================================================
def part_first_rows(scene, bm, rule):
    boards = pq_boards()
    stuff = VGroup(*[VGroup(b["lab"], *b["rows"], b["note"]) for b in boards.values()])
    assert_in_frame(stuff)
    assert_apart(stuff, rule, gap=0.2)
    assert_apart(stuff, bm, gap=0.4)
    assert_apart(stuff[0], stuff[1], gap=0.3)

    scene.say("讀出第 1 列：", "$P$", " 記每個號碼最左在第幾行，", "$Q$", " 記最上在第幾列")
    scene.play(*[FadeIn(VGroup(b["lab"], b["rows"][0], b["note"])) for b in boards.values()], run_time=0.6)
    read_row(scene, bm, NUM, boards["P"]["rows"][0], boards["Q"]["rows"][0], STAGES[0]["P_row"],
             STAGES[0]["Q_row"])
    scene.wait(1.0)
    return boards


# =============================================================================
# 第 3 段：導出矩陣
# =============================================================================
def part_derived(scene, bm, rule, boards):
    bf = ball_matrix(A_FLAT, NUM_FLAT, CELL, np.array([-1.25, 0.0, 0.0]), r"A^{\flat}")
    y = bm.grid.get_y()
    arrow = Arrow(np.array([bm.grid.get_right()[0] + 0.12, y, 0.0]), np.array([bf.get_left()[0] - 0.1, y, 0.0]),
                  buff=0.0, thickness=3, fill_color=GREY_B)
    stop = Tex(r"A^{\flat\flat}=0", font_size=36, fill_color=MUTED_COLOR).next_to(bf, DOWN, buff=0.35)
    stuff = VGroup(*[VGroup(b["lab"], *b["rows"], b["note"]) for b in boards.values()])
    assert_in_frame(bf, bf.name, arrow, stop)
    assert_apart(bf, bm, gap=0.5)
    assert_apart(VGroup(bf, stop), stuff, gap=0.4)
    assert_apart(bf.name, VGroup(bm, bm.name), gap=0.3)

    scene.say("導出矩陣 ", "$A^{\\flat}$", "：號碼相同的球，由西南到東北排成一串")
    scene.play(FadeOut(rule), *show_grid(bf), GrowArrow(arrow), run_time=0.8)
    scene.wait(0.8)
    used = {}
    for n, (k, b1, b2, (r, c)) in enumerate(derived_moves(NUM)):
        if n == 0:
            scene.say("每顆球往右、下一顆往下，交會的那一格放一顆新球（號碼 ", f"${k}$", "）")
        else:
            scene.say("號碼 ", f"${k}$", "：新球放在第 ", f"${r + 1}$", " 列第 ", f"${c + 1}$", " 行")
        ball1, ball2 = bm.ball(*b1, NUM[b1].index(k)), bm.ball(*b2, NUM[b2].index(k))
        tc = bm.cell_center(r, c)
        h = Arrow(ball1.get_center(), np.array([tc[0], ball1.get_y(), 0.0]), buff=0.2, thickness=2.5, fill_color=YELLOW)
        v = Arrow(ball2.get_center(), np.array([ball2.get_x(), tc[1], 0.0]), buff=0.2, thickness=2.5, fill_color=YELLOW)
        same = [bm.ball(i, j, t)[0] for i, j, t in balls_of(NUM, k)]
        tsq = bm.cell_square(r, c).copy().set_fill(YELLOW, opacity=0.25)
        fsq = bf.cell_square(r, c).copy().set_fill(YELLOW, opacity=0.25)
        t = used.get((r, c), 0)
        used[(r, c)] = t + 1
        scene.play(*[b.animate.set_fill(YELLOW) for b in same], run_time=0.35)
        scene.play(GrowArrow(h), GrowArrow(v), run_time=0.6)
        scene.play(FadeIn(tsq), FadeIn(fsq), run_time=0.3)
        scene.play(TransformFromCopy(tsq, bf.ball(r, c, t)[0]), run_time=0.6)
        scene.wait(0.7 if n == 0 else 0.5)
        scene.play(FadeOut(h), FadeOut(v), FadeOut(tsq), FadeOut(fsq), *[b.animate.set_fill(BALL) for b in same],
                   run_time=0.35)
    assert used == {(i, j): a for i, row in enumerate(A_FLAT) for j, a in enumerate(row) if a}

    scene.say("$A^{\\flat}$", " 用同樣的規則編號，讀出 ", "$P$", "、", "$Q$", " 的第 2 列")
    scene.play(*[FadeIn(bf.ball(i, j, t)[1], scale=1.6) for (i, j), xs in NUM_FLAT.items() for t in range(len(xs))],
               *[FadeIn(b["rows"][1]) for b in boards.values()], run_time=0.6)
    read_row(scene, bf, NUM_FLAT, boards["P"]["rows"][1], boards["Q"]["rows"][1], STAGES[1]["P_row"],
             STAGES[1]["Q_row"])
    scene.wait(0.6)
    scene.say("$A^{\\flat}$", " 裡沒有同號的球，再導出就是空的：停")
    scene.play(FadeIn(stop, shift=0.1 * UP), run_time=0.5)
    scene.wait(1.2)
    ok = VGroup(*[SurroundingRectangle(VGroup(*b["rows"]), buff=0.08, color=OK_COLOR, stroke_width=3)
                  for b in boards.values()])
    scene.say("得到的 ", "$(P,Q)$", " 和用列插入算的完全一樣（Exercise 1）")
    scene.play(ShowCreation(ok), run_time=0.6)
    scene.wait(1.8)


# =============================================================================
# 第 4 段：對稱定理一目了然
# =============================================================================
def part_symmetry(scene):
    NT = ball_numbering(AT)
    bm = ball_matrix(A, NUM, 0.85, np.array([-4.1, 1.15, 0.0]), "A")
    bt = ball_matrix(AT, NT, 0.85, np.array([3.0, 1.45, 0.0]), "A^{T}")
    arrow = Arrow(np.array([bm.get_right()[0] + 0.3, 1.15, 0.0]), np.array([bt.name.get_left()[0] - 0.3, 1.15, 0.0]),
                  buff=0.0, thickness=3, fill_color=GREY_B)
    alab = zh("轉置", font_size=24, color=MUTED_COLOR).next_to(arrow, UP, buff=0.12)

    def pair(names, tabs, x):
        g = VGroup(*[labeled(nm, tableau_mob(T, 0.42), font_size=30, buff=0.2) for nm, T in zip(names, tabs)])
        return g.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(np.array([x, -1.8, 0.0]))

    left = pair(("P(A)=", "Q(A)="), (CH4_P, CH4_Q), -4.1)
    right = pair((r"P(A^{T})=", r"Q(A^{T})="), (CH4_Q, CH4_P), 3.0)
    marks = VGroup(*[SurroundingRectangle(g[s][1], buff=0.06, color=col, stroke_width=3)
                     for g, cols in ((left, (TEAL, GOLD)), (right, (GOLD, TEAL))) for s, col in enumerate(cols)])
    assert_in_frame(bm, bm.name, bt, bt.name, arrow, alab, left, right)
    assert_apart(VGroup(bm, bm.name), left, gap=0.25)
    assert_apart(VGroup(bt, bt.name), right, gap=0.25)
    assert_apart(left, right, gap=0.5)
    assert_apart(alab, VGroup(bt, bt.name), gap=0.1)

    scene.say("編號規則對列、行一視同仁：把 ", "$A$", " 轉置，每顆球連同號碼一起轉置")
    scene.play(*show_grid(bm), FadeIn(bm.balls), FadeIn(left), run_time=0.8)
    scene.wait(0.4)
    scene.play(GrowArrow(arrow), FadeIn(alab), *show_grid(bt), run_time=0.6)
    for (i, j), xs in NUM.items():
        assert NT[(j, i)] == xs
    scene.play(*[TransformFromCopy(bm.ball(i, j, t), bt.ball(j, i, t)) for (i, j), xs in NUM.items()
                 for t in range(len(xs))], run_time=1.2)
    scene.wait(0.5)
    scene.say("「最左的行」與「最上的列」互換：", "$A^{T}$", " 給出 ", "$(Q,P)$", "，對稱定理一目了然")
    scene.play(FadeIn(right, shift=0.15 * UP), run_time=0.8)
    scene.play(ShowCreation(marks), run_time=0.6)
    scene.wait(1.8)


# =============================================================================
# 第 5 段：Exercise 4（對稱矩陣的跡）
# =============================================================================
def part_trace(scene):
    bs = ball_matrix(S, ball_numbering(S), 1.0, np.array([-4.6, 1.0, 0.0]), "S")
    bsf = ball_matrix(S_FLAT, S_STAGES[1]["balls"], 1.0, np.array([-1.1, 1.0, 0.0]), r"S^{\flat}")
    y = bs.grid.get_y()
    arrow = Arrow(np.array([bs.grid.get_right()[0] + 0.12, y, 0.0]), np.array([bsf.get_left()[0] - 0.1, y, 0.0]),
                  buff=0.0, thickness=3, fill_color=GREY_B)
    tab = tableau_mob(S_P, 0.6)
    item = labeled("P=Q=", tab, font_size=40).move_to(np.array([3.9, 1.1, 0.0]))
    diag = VGroup(*[b.cell_square(i, i).copy().set_fill(GOLD, opacity=0.3).set_stroke(width=0)
                    for b in (bs, bsf) for i in range(2)])
    first = SurroundingRectangle(VGroup(*[tab.cell(0, j) for j in range(len(S_P[0]))]), buff=0.05, color=GOLD,
                                 stroke_width=3)
    heights = conjugate(shape(S_P))
    odd = VGroup(*[SurroundingRectangle(VGroup(*[tab.cell(i, j) for i in range(h)]), buff=0.05, color=TEAL,
                                        stroke_width=3) for j, h in enumerate(heights) if h % 2])
    t1, t2, n1 = trace(S), trace(S_FLAT), len(S_P[0])
    lines = VGroup(mixed(f"$\\mathrm{{tr}}\\,S+\\mathrm{{tr}}\\,S^{{\\flat}}={t1}+{t2}={t1 + t2}$", "＝", "$P$",
                         " 第一列的長度", font_size=28),
                   mixed(f"$\\mathrm{{tr}}\\,S={t1}$", "＝", "$P$", " 裡長度為奇數的行數", font_size=28))
    lines.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(np.array([0.0, -1.65, 0.0]))
    assert t1 + t2 == n1 and len(odd) == t1
    assert_in_frame(bs, bs.name, bsf, bsf.name, arrow, item, lines)
    assert_apart(VGroup(bs, bsf, bs.name, bsf.name, item), lines, gap=0.3)
    assert_apart(bsf, item, gap=0.4)
    assert_apart(bs, VGroup(bsf, bsf.name), gap=0.4)

    scene.say("Exercise 4：對稱矩陣 ", "$S$", " 對應到 ", "$(P,P)$", "；看一個小例子和它的 ", "$S^{\\flat}$")
    scene.play(*show_grid(bs), FadeIn(bs.balls), run_time=0.8)
    scene.play(GrowArrow(arrow), *show_grid(bsf), FadeIn(bsf.balls), run_time=0.8)
    scene.play(FadeIn(item), run_time=0.6)
    scene.wait(1.0)
    scene.say("對角線上的球數：", "$\\mathrm{tr}\\,S+\\mathrm{tr}\\,S^{\\flat}$", " 等於 ", "$P$", " 第一列的長度")
    scene.play(FadeIn(diag), ShowCreation(first), run_time=0.7)
    scene.play(FadeIn(lines[0], shift=0.1 * UP), run_time=0.6)
    scene.wait(1.8)
    scene.say("推得 ", "$\\mathrm{tr}\\,S$", " ＝ ", "$P$", " 裡奇數長的行數；對合的不動點個數也這樣數")
    scene.play(FadeOut(first), ShowCreation(odd), run_time=0.7)
    scene.play(FadeIn(lines[1], shift=0.1 * UP), run_time=0.6)
    scene.wait(2.0)
    scene.say("當 ", "$A$", " 是排列矩陣時，矩陣球構造就是 Viennot 的「影子線」構造")
    scene.wait(2.2)


class SceneF18MatrixBall(ChuScene):
    def construct(self):
        self.show_header("矩陣球構造")
        check_math()
        bm, rule = part_numbering(self)
        boards = part_first_rows(self, bm, rule)
        part_derived(self, bm, rule, boards)
        self.clear_stage()
        part_symmetry(self)
        self.clear_stage()
        part_trace(self)
        self.wait(1.0)
