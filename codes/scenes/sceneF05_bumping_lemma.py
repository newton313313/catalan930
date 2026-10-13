"""
Scene F05 —— 擠壓路徑與列擠壓引理（Fulton《Young Tableaux》§1.1，p.9–11）

    擠壓路徑 R：列插入 T ← x 時「有數被擠出的格子」加上「最後落腳的格子」；新格子 B = R 的最後一格
        例（p.9）：T = [[1,2,2,3],[2,3,5,5],[4,4,6],[5,6]] ← 2，R = (1,4),(2,3),(3,3),(4,3)（1 起算），B = (4,3)
    Row Bumping Lemma：先插 x 再插 x′，路徑 R、R′，新格子 B、B′
        (1) x ≤ x′：R 嚴格在 R′ 左邊；B 嚴格在 B′ 左邊、不比 B′ 低        例：T ← 1 ← 2
        (2) x > x′：R′ 弱在 R 左邊；B′ 嚴格在 B 下面、不在 B 右邊          例：T ← 2 ← 1
    命題（p.11）：插入弱遞增的 1 ≤ 3 ≤ 3 → 新格子在不同行、由左到右（水平條）；
                  插入嚴格遞減的 5 > 3 > 1 → 新格子在不同列、由上到下（垂直條）；反向擠壓可唯一還原

數學資料全部由 utils/tableaux.py 計算並 assert。格子 (i, j) 0 起算；畫面上的「第 k 列／行」是 1 起算。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF05_bumping_lemma.py SceneF05BumpingLemma
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.mit_draw import LEFT_COLOR, RIGHT_COLOR, ROOT_COLOR, YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, YELLOW, mixed
from utils.tableaux import (
    FULTON_INSERT_T,
    bump_steps,
    corners,
    insert_word_steps,
    is_horizontal_strip,
    is_tableau,
    is_vertical_strip,
    reverse_bump,
    row_insert,
    shape,
    skew_boxes,
    young_boxes,
)

T0 = FULTON_INSERT_T                 # 書 p.7–9 的表
X_DEMO = 2                           # p.9：T ← 2 的擠壓路徑
CASE1 = (1, 2)                       # x ≤ x′
CASE2 = (2, 1)                       # x > x′
INC = (1, 3, 3)                      # 弱遞增 -> 水平條
DEC = (5, 3, 1)                      # 嚴格遞減 -> 垂直條

R_COLOR = LEFT_COLOR                 # 第一條路徑 R（青）
R2_COLOR = RIGHT_COLOR               # 第二條路徑 R′（粉紅）
DEMO_COLOR = ROOT_COLOR              # p.9 的單一路徑（橘）
NEW_COLOR = OK_COLOR                 # 命題裡的新格子（綠）
ZONE1_COLOR = BLUE_C
ZONE2_COLOR = PURPLE_B
FILL_OP = 0.5

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


# =============================================================================
# 檢查用
# =============================================================================
def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊（至少一個方向分開 gap）。"""
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a, b)


def strictly_left(R, R2):
    """R 嚴格在 R2 左邊：R2 有格子的每一列，R 在那一列也有格子而且更靠左（路徑每列一格、由第 0 列連續往下）。"""
    return all(r < len(R) and R[r][0] == r and R[r][1] < c for r, c in R2)


def weakly_left(R, R2):
    return all(r < len(R) and R[r][0] == r and R[r][1] <= c for r, c in R2)


def is_route(R):
    return [r for r, _ in R] == list(range(len(R)))


def check_math():
    assert T0 == ((1, 2, 2, 3), (2, 3, 5, 5), (4, 4, 6), (5, 6)) and is_tableau(T0)

    # ---- p.9 的例子
    T1, R, B = row_insert(T0, X_DEMO)
    assert T1 == ((1, 2, 2, 2), (2, 3, 3, 5), (4, 4, 5), (5, 6, 6))
    assert R == [(0, 3), (1, 2), (2, 2), (3, 2)] and B == (3, 2) and is_route(R)
    assert young_boxes(shape(T1)) == sorted(young_boxes(shape(T0)) + [B])
    assert [s[2] for s in bump_steps(T0, X_DEMO)] == [3, 5, 6, None]

    # ---- 引理的兩種情況
    cases = []
    for (x, x2) in (CASE1, CASE2):
        Ta, Ra, Ba = row_insert(T0, x)
        Tb, Rb, Bb = row_insert(Ta, x2)
        assert is_route(Ra) and is_route(Rb) and is_tableau(Tb)
        assert not set(Ra) & set(Rb)                 # 兩條路徑沒有共用格子（上色才不會互相蓋掉）
        cases.append((x, x2, Ta, Ra, Ba, Tb, Rb, Bb))
    (x, x2, Ta, Ra, Ba, Tb, Rb, Bb) = cases[0]
    assert x <= x2
    assert Ra == [(0, 1), (1, 1), (2, 0), (3, 0), (4, 0)] and Ba == (4, 0)
    assert Rb == [(0, 3), (1, 2), (2, 2), (3, 2)] and Bb == (3, 2)
    assert strictly_left(Ra, Rb)
    assert Ba[1] < Bb[1] and Ba[0] >= Bb[0]          # B 嚴格在 B′ 左邊、弱在下面
    assert Tb == ((1, 1, 2, 2), (2, 2, 3, 5), (3, 4, 5), (4, 6, 6), (5,))
    (x, x2, Ta, Ra, Ba, Tb, Rb, Bb) = cases[1]
    assert x > x2
    assert Ra == [(0, 3), (1, 2), (2, 2), (3, 2)] and Ba == (3, 2)
    assert Rb == [(0, 1), (1, 1), (2, 0), (3, 0), (4, 0)] and Bb == (4, 0)
    assert weakly_left(Rb, Ra) and len(Rb) > len(Ra)  # R′ 弱在 R 左邊，而且多走至少一列
    assert Bb[1] <= Ba[1] and Bb[0] > Ba[0]          # B′ 弱在 B 左邊、嚴格在下面
    assert Tb == ((1, 1, 2, 2), (2, 2, 3, 5), (3, 4, 5), (4, 6, 6), (5,))
    for c in cases:
        assert shape(c[5]) == (4, 4, 3, 3, 1)

    # ---- 命題
    lam = shape(T0)
    props = []
    for seq in (INC, DEC):
        steps = insert_word_steps(seq, T0)
        news = [s[3] for s in steps]
        U = steps[-1][1]
        mu = shape(U)
        assert sorted(news) == sorted(skew_boxes(mu, lam))
        props.append((seq, steps, news, U, mu))
    seq, steps, news, U, mu = props[0]
    assert all(a <= b for a, b in zip(seq, seq[1:]))
    assert news == [(4, 0), (0, 4), (0, 5)] and mu == (6, 4, 3, 2, 1)
    cols = [c for _, c in news]
    assert cols == sorted(set(cols)) and [c + 1 for c in cols] == [1, 5, 6]
    assert is_horizontal_strip(mu, lam) and not is_vertical_strip(mu, lam)
    # 反過來：由最右邊的新格子往左做反向擠壓，唯一還原 T 與 x1 ≤ x2 ≤ x3
    W, back = U, []
    for box in sorted(news, key=lambda b: -b[1]):
        assert box in corners(shape(W))
        W, y, _ = reverse_bump(W, box)
        back.append(y)
    assert W == T0 and tuple(reversed(back)) == seq

    seq, steps, news, U, mu = props[1]
    assert all(a > b for a, b in zip(seq, seq[1:]))
    assert news == [(0, 4), (1, 4), (4, 0)] and mu == (5, 5, 3, 2, 1)
    rows = [r for r, _ in news]
    assert rows == sorted(set(rows)) and [r + 1 for r in rows] == [1, 2, 5]
    assert is_vertical_strip(mu, lam) and not is_horizontal_strip(mu, lam)
    W, back = U, []
    for box in sorted(news, key=lambda b: -b[0]):          # 由最下面的新格子往上
        assert box in corners(shape(W))
        W, y, _ = reverse_bump(W, box)
        back.append(y)
    assert W == T0 and tuple(reversed(back)) == seq
    return cases, props


# =============================================================================
# 可以長大的表：YoungDiagramMob 用「最後的形狀」建好，只把目前形狀的格子放上畫面
# =============================================================================
def make_board(T, final_shape, cs, top_left, font_size=None):
    top_left = np.array([top_left[0], top_left[1], 0.0], dtype=float)
    diag =YoungDiagramMob(final_shape, cell_size=cs, top_left=top_left, stroke_width=3)
    fs = font_size or 46 * cs
    ent, val = {}, {}
    for i, row in enumerate(T):
        for j, v in enumerate(row):
            t = Tex(str(v), font_size=fs)
            t.move_to(diag.cell_center(i, j))
            t.set_z_index(2)
            ent[(i, j)] = t
            val[(i, j)] = v
    return {"diag": diag, "ent": ent, "val": val, "T": tuple(tuple(r) for r in T), "cs": cs, "tl": top_left,
            "fs": fs}


def board_group(board):
    """目前畫面上的格子與數字。"""
    diag = board["diag"]
    cells = VGroup(*[diag.cell(i, j) for i, j in young_boxes(shape(board["T"]))])
    return VGroup(cells, VGroup(*board["ent"].values()))


def final_group(board):
    """最後形狀的所有格子（排版檢查用）。"""
    return board["diag"].cells


def slot_point(board, r):
    """第 r 列左邊、等著進入那一列的數的位置。"""
    cs = board["cs"]
    return board["tl"] + np.array([-0.62 * cs, -(r + 0.5) * cs, 0.0])


def insert_anim(scene, board, x, color, step_time=0.45, mover_color=None):
    """逐步列插入 board ← x：移動中的數用 mover_color，經過的格子填 color。回傳 (新表, 路徑, 新格子)。"""
    mover_color = mover_color or color
    T = board["T"]
    steps = bump_steps(T, x)
    T2, route, new = row_insert(T, x)
    assert [b for b, _, _ in steps] == route
    diag, ent, val = board["diag"], board["ent"], board["val"]
    mover = Tex(str(x), font_size=board["fs"], fill_color=mover_color)
    mover.move_to(slot_point(board, 0))
    mover.set_z_index(3)
    mover_val = x
    scene.play(FadeIn(mover, shift=0.3 * RIGHT), run_time=0.35)
    for (r, c), placed, bumped in steps:
        assert placed == mover_val
        cell = diag.cell(r, c)
        anims = [mover.animate.move_to(diag.cell_center(r, c)).set_fill(WHITE)]
        if bumped is None:
            assert (r, c) == new and (r, c) not in ent
            cell.set_fill(color, opacity=FILL_OP)
            anims.append(FadeIn(cell))
            nxt = None
        else:
            old = ent[(r, c)]
            assert val[(r, c)] == bumped
            anims.append(old.animate.move_to(slot_point(board, r + 1)).set_fill(mover_color))
            anims.append(cell.animate.set_fill(color, opacity=FILL_OP))
            nxt = old
        scene.play(*anims, run_time=step_time)
        mover.set_z_index(2)
        ent[(r, c)] = mover
        val[(r, c)] = placed
        mover, mover_val = nxt, bumped
        if mover is not None:
            mover.set_z_index(3)
    board["T"] = T2
    assert val == {(i, j): v for i, row in enumerate(T2) for j, v in enumerate(row)}
    return T2, route, new


def side_label(board, box, mob, buff=0.1, sh=None):
    """把 mob 放在格子 box 的右邊（在形狀 sh 裡右邊是空的時候），否則放在上面。sh 預設為目前的形狀。"""
    diag = board["diag"]
    i, j = box
    sh = sh or shape(board["T"])
    if j + 1 >= sh[i]:
        mob.next_to(diag.cell(i, j), RIGHT, buff=buff)
    else:
        assert i == 0 or sh[i - 1] <= j, "上面也有格子"
        mob.next_to(diag.cell(i, j), UP, buff=buff)
    return mob


def colored_mixed(parts, colors, font_size=24):
    """mixed(...) 之後把第 k 段上色：colors = {k: 顏色}。"""
    m = mixed(*parts, font_size=font_size)
    for k, col in colors.items():
        m[k].set_fill(col)
    return m


def order_tag(k, color=YELLOW):
    c = Circle(radius=0.15, stroke_color=color, stroke_width=2.5)
    t = Tex(str(k), font_size=20, fill_color=color).move_to(c)
    return VGroup(c, t)


# =============================================================================
def part_route(scene):
    cs = 0.72
    T1, R, B = row_insert(T0, X_DEMO)
    board = make_board(T0, shape(T1), cs, (-5.9, 1.75))
    title = Tex(r"T\leftarrow 2", font_size=44)
    title.next_to(final_group(board), UP, buff=0.35)
    title0 = Tex("T", font_size=44).move_to(title)        # 插入完成前畫面上還是 T（與 F04 一致）

    defs = VGroup(
        mixed("擠壓路徑 ", "$R$", "：被擠出數字的格子，", font_size=28),
        mixed("再加上最後落腳的那一格", font_size=28),
        mixed("新格子 ", "$B$", "：形狀多出來的那一格", font_size=28),
        mixed("（也就是 ", "$R$", " 的最後一格）", font_size=28),
        mixed("路徑從第 1 列出發，每列至多一格", font_size=28),
    ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
    defs[1].shift(0.68 * RIGHT)
    defs[3].shift(0.68 * RIGHT)
    defs[0][1].set_fill(DEMO_COLOR)
    defs[2][1].set_fill(YELLOW)
    defs.move_to(np.array([-2.3, 2.75, 0.0]), aligned_edge=UL)

    cmp_ = VGroup(
        mixed("比較兩條路徑 ", "$R$", "、", "$R'$", "：", font_size=28),
        mixed("嚴格在左：", "$R'$", " 經過的每一列，", "$R$", " 的格子都更靠左", font_size=26),
        mixed("弱在左：同上，但允許落在同一格", font_size=26),
    ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    cmp_[1].shift(0.3 * RIGHT)
    cmp_[2].shift(0.3 * RIGHT)
    cmp_[0][1].set_fill(R_COLOR)
    cmp_[0][3].set_fill(R2_COLOR)
    cmp_[1][1].set_fill(R2_COLOR)
    cmp_[1][3].set_fill(R_COLOR)
    cmp_.next_to(defs, DOWN, buff=0.45, aligned_edge=LEFT)
    cmp_box = SurroundingRectangle(cmp_, buff=0.15, color=MUTED_COLOR, stroke_width=2)

    b_lab = Tex("B", font_size=40, fill_color=YELLOW)
    b_outline = Square(side_length=cs, stroke_color=YELLOW, stroke_width=6).move_to(board["diag"].cell_center(*B))
    b_outline.set_z_index(1)

    scene.say("回顧：把 ", "$2$", " 插入 ", "$T$", "，數字一列一列往下擠")
    scene.play(FadeIn(board_group(board)), FadeIn(title0), run_time=0.8)
    T_after, route, new = insert_anim(scene, board, X_DEMO, DEMO_COLOR, step_time=0.5, mover_color=YELLOW)
    assert (T_after, route, new) == (T1, R, B)
    scene.play(ReplacementTransform(title0, title), run_time=0.5)
    side_label(board, B, b_lab)
    assert_in_frame(final_group(board), title, defs, cmp_box, b_lab, VGroup(*[Dot(slot_point(board, r))
                                                                                for r in range(5)]))
    assert_apart(VGroup(final_group(board), b_lab), defs, gap=0.4)
    assert_apart(VGroup(final_group(board), b_lab), cmp_box, gap=0.4)
    assert_apart(defs, cmp_box)
    for i, j in young_boxes(shape(T1)):
        assert_apart(b_lab, board["diag"].cell(i, j), gap=0.0)

    scene.say("被擠出數字的格子，加上最後落腳的那一格，連成擠壓路徑 ", "$R$", t2c={"R": DEMO_COLOR})
    scene.play(FadeIn(defs[0:2], shift=0.15 * UP), run_time=0.8)
    scene.wait(1.2)
    scene.say("形狀多出來的那一格叫新格子 ", "$B$", "，它正是路徑的最後一格")
    scene.play(ShowCreation(b_outline), FadeIn(b_lab), FadeIn(defs[2:4], shift=0.15 * UP), run_time=0.9)
    scene.wait(1.2)
    scene.say("路徑每列至多一格，所以兩條路徑可以一列一列比較左右")
    scene.play(FadeIn(defs[4], shift=0.15 * UP), run_time=0.6)
    scene.play(ShowCreation(cmp_box), FadeIn(cmp_), run_time=0.9)
    scene.wait(2.4)


def lemma_panel(scene, case, center_x, label):
    """一種情況：先插 x（路徑 R 青色）、再插 x′（路徑 R′ 粉紅）。回傳畫面上的物件。"""
    x, x2, Ta, Ra, Ba, Tb, Rb, Bb = case
    cs = 0.55
    final = shape(Tb)
    width = final[0] * cs
    board = make_board(T0, final, cs, (center_x - width / 2, 1.1))
    rel = r"\le " if x <= x2 else ">"
    head = mixed(label, "$x" + rel + "x'$", font_size=26)
    head.move_to(np.array([center_x, 2.15, 0.0]))
    expr = Tex(r"T\leftarrow " + str(x) + r"\leftarrow " + str(x2), font_size=36)
    assert len(expr) == 5                # 字形：T、←、x、←、x′
    expr[2].set_fill(R_COLOR)
    expr[4].set_fill(R2_COLOR)
    expr.move_to(np.array([center_x, 1.6, 0.0]))
    group0 = board_group(board)

    scene.play(FadeIn(head), FadeIn(expr), FadeIn(group0), run_time=0.7)
    got_a = insert_anim(scene, board, x, R_COLOR, step_time=0.35)
    assert got_a == (Ta, Ra, Ba)
    got_b = insert_anim(scene, board, x2, R2_COLOR, step_time=0.35)
    assert got_b == (Tb, Rb, Bb)

    lab_b = side_label(board, Ba, Tex("B", font_size=30, fill_color=R_COLOR))
    lab_b2 = side_label(board, Bb, Tex("B'", font_size=30, fill_color=R2_COLOR))
    for lab in (lab_b, lab_b2):
        for i, j in young_boxes(final):
            assert_apart(lab, board["diag"].cell(i, j), gap=0.0)
    assert_apart(lab_b, lab_b2)
    scene.play(FadeIn(lab_b), FadeIn(lab_b2), run_time=0.5)
    pic = VGroup(final_group(board), lab_b, lab_b2, VGroup(*[Dot(slot_point(board, r)) for r in range(5)]))
    assert_in_frame(head, expr, pic)
    assert_apart(head, expr)
    assert_apart(expr, pic)
    assert head.get_top()[1] < 2.55
    return board, VGroup(head, expr), pic


def part_lemma(scene, cases):
    stmt = mixed("列擠壓引理：在 ", "$T$", " 中先插入 ", "$x$", "、再插入 ", "$x'$", "，得到路徑 ",
                 "$R,R'$", " 與新格子 ", "$B,B'$", font_size=26)
    stmt[3].set_fill(R_COLOR)
    stmt[5].set_fill(R2_COLOR)
    stmt.move_to(2.8 * UP)
    assert_in_frame(stmt)
    scene.say("連續插入兩個數：兩條路徑與兩個新格子的位置，有固定的規律")
    scene.play(FadeIn(stmt, shift=0.15 * DOWN), run_time=0.8)
    scene.wait(0.8)

    # ---------------------------------------------------- 情況 (1)
    x, x2 = cases[0][:2]
    scene.say("情況 (1)：先插 ", "$" + str(x) + "$", " 再插 ", "$" + str(x2) + "$", "，後插的數不比先插的小")
    b1, top1, pic1 = lemma_panel(scene, cases[0], -3.4, "情況 (1)：")
    concl1 = VGroup(
        colored_mixed(["$R$", " 嚴格在 ", "$R'$", " 的左邊"], {0: R_COLOR, 2: R2_COLOR}),
        colored_mixed(["$B$", " 嚴格在 ", "$B'$", " 左邊，而且不比 ", "$B'$", " 高"],
                      {0: R_COLOR, 2: R2_COLOR, 4: R2_COLOR}),
    ).arrange(DOWN, buff=0.18)
    concl1.next_to(pic1[0], DOWN, buff=0.35)
    concl1.set_x(-3.4)
    assert_in_frame(concl1)
    assert_apart(pic1, concl1)
    scene.say("$R'$", " 每一列都在 ", "$R$", " 的右邊；", "$B'$", " 在 ", "$B$", " 的右邊，而且不比它低")
    scene.play(FadeIn(concl1, shift=0.15 * UP), run_time=0.8)
    scene.wait(1.6)
    scene.say("理由：第 1 列裡 ", "$x'$", " 只能擠掉 ", "$x$", " 右邊的數，被擠出的兩數大小順序不變，逐列傳下去")
    scene.wait(2.3)

    # ---------------------------------------------------- 情況 (2)
    x, x2 = cases[1][:2]
    scene.say("情況 (2)：順序對調，先插 ", "$" + str(x) + "$", " 再插 ", "$" + str(x2) + "$")
    b2, top2, pic2 = lemma_panel(scene, cases[1], 3.4, "情況 (2)：")
    concl2 = VGroup(
        colored_mixed(["$R'$", " 弱在 ", "$R$", " 的左邊"], {0: R2_COLOR, 2: R_COLOR}),
        colored_mixed(["$B'$", " 嚴格在 ", "$B$", " 下面，而且不在 ", "$B$", " 右邊"],
                      {0: R2_COLOR, 2: R_COLOR, 4: R_COLOR}),
    ).arrange(DOWN, buff=0.18)
    concl2.next_to(pic2[0], DOWN, buff=0.35)
    concl2.set_x(3.4)
    assert_in_frame(concl2)
    assert_apart(pic2, concl2)
    for a in (top1, pic1, concl1):
        for b in (top2, pic2, concl2):
            assert_apart(a, b, gap=0.3)
    scene.say("這次 ", "$R'$", " 每列都不在 ", "$R$", " 右邊，還至少多走一列：", "$B'$", " 一定比 ", "$B$", " 低")
    scene.play(FadeIn(concl2, shift=0.15 * UP), run_time=0.8)
    scene.wait(1.6)
    scene.say("理由：", "$x'<x$", " 擠的位置不在 ", "$x$", " 右邊，被擠出的數也是後者較小，逐列傳下去")
    scene.wait(2.3)


def part_picture(scene):
    """書 p.10 的示意圖：以 B 為準，B′ 落在右上（x ≤ x′）或左下（x > x′）。"""
    s = 0.85
    P = np.array([0.4, 0.35, 0.0])                       # B 的右下角
    xl, xr, yb, yt = -5.6, 5.6, -2.55, 2.75
    h_line = Line(np.array([xl, P[1], 0]), np.array([xr, P[1], 0]), stroke_color=GREY_A, stroke_width=3)
    v_line = Line(np.array([P[0], yb, 0]), np.array([P[0], yt, 0]), stroke_color=GREY_A, stroke_width=3)
    zone1 = Rectangle(width=xr - P[0], height=yt - P[1], stroke_width=0)
    zone1.set_fill(ZONE1_COLOR, opacity=0.22).move_to(np.array([(xr + P[0]) / 2, (yt + P[1]) / 2, 0]))
    zone2 = Rectangle(width=P[0] - xl, height=P[1] - yb, stroke_width=0)
    zone2.set_fill(ZONE2_COLOR, opacity=0.22).move_to(np.array([(xl + P[0]) / 2, (yb + P[1]) / 2, 0]))
    b_sq = Square(side_length=s, stroke_color=R_COLOR, stroke_width=4)
    b_sq.set_fill(R_COLOR, opacity=FILL_OP).move_to(P + np.array([-s / 2, s / 2, 0]))
    b_tex = Tex("B", font_size=40, fill_color=WHITE).move_to(b_sq)

    t1 = VGroup(
        mixed("情況 (1) ", "$x\\le x'$", font_size=26),
        colored_mixed(["$B'$", " 在這一區"], {0: R2_COLOR}, font_size=26),
        mixed("嚴格在 ", "$B$", " 右邊、不比 ", "$B$", " 低", font_size=22, color=MUTED_COLOR),
    ).arrange(DOWN, buff=0.18)
    t1.move_to(zone1).shift(0.25 * RIGHT)
    t2 = VGroup(
        mixed("情況 (2) ", "$x>x'$", font_size=26),
        colored_mixed(["$B'$", " 在這一區"], {0: R2_COLOR}, font_size=26),
        mixed("嚴格在 ", "$B$", " 下面、不在 ", "$B$", " 右邊", font_size=22, color=MUTED_COLOR),
    ).arrange(DOWN, buff=0.18)
    t2.move_to(zone2).shift(0.2 * LEFT)
    assert_in_frame(h_line, v_line, zone1, zone2, t1, t2)
    for a in (t1, t2):
        assert_apart(a, b_sq, gap=0.3)
        assert_apart(a, h_line, gap=0.2)
        assert_apart(a, v_line, gap=0.2)
    assert zone1.get_left()[0] >= b_sq.get_right()[0] - 1e-6        # 右上區：嚴格在 B 的右邊
    assert zone1.get_bottom()[1] <= b_sq.get_bottom()[1] + 1e-6     # 而且包含 B 的那一列
    assert zone2.get_top()[1] <= b_sq.get_bottom()[1] + 1e-6        # 左下區：嚴格在 B 的下面
    assert zone2.get_right()[0] >= b_sq.get_right()[0] - 1e-6       # 而且包含 B 的那一行

    scene.say("整理成一張圖：以 ", "$B$", " 為準，", "$B'$", " 落在哪一區，只看 ", "$x$", " 和 ", "$x'$", " 誰大")
    scene.play(ShowCreation(h_line), ShowCreation(v_line), FadeIn(b_sq), FadeIn(b_tex), run_time=1.0)
    scene.play(FadeIn(zone1), FadeIn(t1), run_time=0.8)
    scene.wait(1.0)
    scene.play(FadeIn(zone2), FadeIn(t2), run_time=0.8)
    scene.wait(2.4)


def prop_panel(scene, prop, center_x, title_parts, step_time=0.3):
    seq, steps, news, U, mu = prop
    cs = 0.5
    board = make_board(T0, mu, cs, (center_x - mu[0] * cs / 2, 1.45))
    title = mixed(*title_parts, font_size=26)
    title.move_to(np.array([center_x, 2.2, 0.0]))
    scene.play(FadeIn(title), FadeIn(board_group(board)), run_time=0.6)
    tags = VGroup()
    for k, (x, (T_after, route, new)) in enumerate(zip(seq, [(s[1], s[2], s[3]) for s in steps]), start=1):
        got = insert_anim(scene, board, x, DEMO_COLOR, step_time=step_time, mover_color=YELLOW)
        assert got == (T_after, route, new)
        diag = board["diag"]
        tag = side_label(board, new, order_tag(k), buff=0.08, sh=mu)
        tags.add(tag)
        scene.play(*[diag.cell(i, j).animate.set_fill(BLACK, opacity=0.0) for i, j in route if (i, j) != new],
                   diag.cell(*new).animate.set_fill(NEW_COLOR, opacity=FILL_OP), FadeIn(tag, scale=1.3),
                   run_time=0.4)
    assert board["T"] == U
    for tag in tags:
        for i, j in young_boxes(mu):
            assert_apart(tag, board["diag"].cell(i, j), gap=0.0)
    for a, b in zip(tags[:-1], tags[1:]):
        assert_apart(a, b)
    pic = VGroup(final_group(board), tags, VGroup(*[Dot(slot_point(board, r)) for r in range(len(mu))]))
    assert_in_frame(title, pic)
    assert_apart(title, pic)
    return title, pic


def part_proposition(scene, props):
    stmt = mixed("推論：在 ", "$T$", " 中依序插入 ", "$x_1,x_2,x_3$", "，看三個新格子落在哪裡", font_size=26)
    stmt.move_to(2.8 * UP)
    scene.say("推論：連續插入一串數，看新格子落在哪裡")
    scene.play(FadeIn(stmt, shift=0.15 * DOWN), run_time=0.7)

    inc, dec = props
    s = inc[0]
    scene.say("插入弱遞增的 ", "$%d,%d,%d$" % s, "：每兩個相鄰的數都是情況 (1)")
    title1, pic1 = prop_panel(scene, inc, -3.3, ["弱遞增 ", "$%d\\le %d\\le %d$" % s])
    cols = [c + 1 for _, c in inc[2]]
    concl1 = VGroup(
        mixed("新格子在第 ", "$%d,%d,%d$" % tuple(cols), " 行：各不相同、由左到右", font_size=24),
        mixed("$\\Rightarrow$", " 水平條（沒有兩格同一行）", font_size=24),
    ).arrange(DOWN, buff=0.18)
    concl1.next_to(pic1[0], DOWN, buff=0.35).set_x(-3.3)
    concl1[1].set_fill(NEW_COLOR)
    assert_in_frame(stmt, concl1)
    assert_apart(pic1, concl1)
    assert_apart(stmt, title1)
    scene.say("新格子都在不同的行，一個比一個右邊：多出來的是一條水平條")
    scene.play(FadeIn(concl1, shift=0.15 * UP), run_time=0.8)
    scene.wait(1.8)

    s = dec[0]
    scene.say("插入嚴格遞減的 ", "$%d,%d,%d$" % s, "：每兩個相鄰的數都是情況 (2)")
    title2, pic2 = prop_panel(scene, dec, 3.4, ["嚴格遞減 ", "$%d>%d>%d$" % s])
    rows = [r + 1 for r, _ in dec[2]]
    concl2 = VGroup(
        mixed("新格子在第 ", "$%d,%d,%d$" % tuple(rows), " 列：各不相同、由上到下", font_size=24),
        mixed("$\\Rightarrow$", " 垂直條（沒有兩格同一列）", font_size=24),
    ).arrange(DOWN, buff=0.18)
    concl2.next_to(pic2[0], DOWN, buff=0.35).set_x(3.4)
    concl2[1].set_fill(NEW_COLOR)
    assert_in_frame(concl2)
    assert_apart(pic2, concl2)
    assert_apart(stmt, title2)
    for a in (title1, pic1, concl1):
        for b in (title2, pic2, concl2):
            assert_apart(a, b, gap=0.3)
    scene.say("新格子都在不同的列，一個比一個下面：多出來的是一條垂直條")
    scene.play(FadeIn(concl2, shift=0.15 * UP), run_time=0.8)
    scene.wait(1.8)
    scene.say("反過來，多出的格子若是水平條或垂直條，用反向擠壓就能唯一還原 ", "$T$", " 和這串數")
    scene.wait(3.0)


class SceneF05BumpingLemma(ChuScene):
    def construct(self):
        self.show_header("擠壓路徑與列擠壓引理")
        cases, props = check_math()
        part_route(self)
        self.clear_stage()
        part_lemma(self, cases)
        self.clear_stage()
        part_picture(self)
        self.clear_stage()
        part_proposition(self, props)
        self.wait(1.0)
