"""
Scene M13 —— 鉤長與鉤長公式（MIT 18.212 L4）

    鉤 = 格子本身 + 同列右邊（臂）+ 同行下面（腿），h = 臂長 + 腿長 + 1
    λ = (4,3,1)：鉤長 6,4,3,1 / 4,2,1 / 1，乘積 576，8!/576 = 70 = f^λ
    鉤長公式 f^λ = n!/∏h(c)；(3,2)：5、(3,3)：5 = C_3；(n,n)：∏h = (n+1)! n! -> C_n
    角落遞迴：最大的數 n 一定在角落 -> f^λ = Σ_角落 f^{λ−c}
    化約：只需證 Σ_c (1/n) H(λ)/H(λ−c) = 1（下一幕 M14 用鉤上漫步證明）

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM13_hook_length.py SceneM13HookLength
"""
import sys
from fractions import Fraction
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import (
    catalan,
    conjugate,
    corner_prob_formula,
    corners,
    hook_cells,
    hook_formula,
    hook_length,
    hook_lengths,
    hook_product,
    remove_corner,
    syt,
    syt_count,
    young_cells,
)
from utils.mit_draw import (
    CORNER_COLOR,
    HOOK_COLOR,
    LEFT_COLOR,
    RIGHT_COLOR,
    ROOT_COLOR,
    YoungDiagramMob,
)
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, boxed, mixed, zh

LAM = (4, 3, 1)          # 主例
EX_CELL = (0, 1)         # 示範鉤的格子（畫面上是第 1 列第 2 格）
SMALL = (3, 2)           # 接 M11
SQUARE = (3, 3)          # 接 M12（f = C_3）

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


# =============================================================================
# 小工具（模組層級）
# =============================================================================
def lam_tex(lam) -> str:
    return "(" + ",".join(str(x) for x in lam) + ")"


def dot_join(values) -> str:
    return r"\cdot ".join(str(v) for v in values)


def flat(table):
    return [x for row in table for x in row]


def fit_width(mob, max_width):
    if mob.get_width() > max_width:
        mob.set_width(max_width)
    return mob


def assert_in_frame(*mobs):
    for m in mobs:
        l, r = m.get_left()[0], m.get_right()[0]
        b, t = m.get_bottom()[1], m.get_top()[1]
        assert X_MIN - 1e-6 <= l and r <= X_MAX + 1e-6, (l, r)
        assert Y_MIN - 1e-6 <= b and t <= Y_MAX + 1e-6, (b, t)


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊。"""
    sep_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    sep_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert sep_x or sep_y, (a.get_bounding_box()[[0, 2]].round(2).tolist(), b.get_bounding_box()[[0, 2]].round(2).tolist())


def hook_numbers(yd, lam, font_size=None, row_colors=None):
    """每格寫上鉤長（不加入 yd，回傳 VGroup，順序 = young_cells）。"""
    table = hook_lengths(lam)
    fs = font_size or 48 * yd.cell_size
    out = VGroup()
    for i, row in enumerate(table):
        for j, h in enumerate(row):
            col = row_colors[i] if row_colors else WHITE
            t = Tex(str(h), font_size=fs, fill_color=col).move_to(yd.cell_center(i, j))
            t.set_z_index(1)
            out.add(t)
    return out


def tableau_mob(T, lam, cell_size, center, mark=None, mark_color=CORNER_COLOR):
    """一個標準 Young 表；mark 的那個數字（與格子）用 mark_color 標出。"""
    yd = YoungDiagramMob(lam, cell_size=cell_size, center=center, stroke_width=2)
    for i, row in enumerate(T):
        for j, v in enumerate(row):
            if v == mark:
                yd.fill_cells([(i, j)], mark_color, opacity=0.45)
    yd.set_entries(T, font_size=46 * cell_size)
    return yd


# =============================================================================
# 第 1 段：鉤與鉤長，λ = (4,3,1)
# =============================================================================
def part_hook(scene):
    lam = LAM
    n = sum(lam)
    table = hook_lengths(lam)
    H = hook_product(lam)
    assert table == [(6, 4, 3, 1), (4, 2, 1), (1,)]
    assert n == 8 and H == 576 and factorial(n) == 40320
    assert hook_formula(lam) == 70 == syt_count(lam) == factorial(n) // H

    ci, cj = EX_CELL
    hook = hook_cells(lam, ci, cj)
    arm = [(a, b) for a, b in hook if a == ci and b > cj]
    leg = [(a, b) for a, b in hook if b == cj and a > ci]
    assert hook[0] == EX_CELL and len(hook) == 1 + len(arm) + len(leg)
    assert arm == [(0, 2), (0, 3)] and leg == [(1, 1)]
    assert len(arm) == lam[ci] - cj - 1 and len(leg) == conjugate(lam)[cj] - ci - 1
    h_ex = hook_length(lam, ci, cj)
    assert h_ex == len(arm) + len(leg) + 1 == 4

    cs = 0.8
    yd = YoungDiagramMob(lam, cell_size=cs, top_left=np.array([-6.3, 2.2, 0.0]))
    lam_lab = Tex(r"\lambda=" + lam_tex(lam), font_size=42).next_to(yd, DOWN, buff=0.45)
    scene.say("Young 圖 ", "$\\lambda=" + lam_tex(lam) + "$", "：每一格都有一個「鉤」")
    scene.play(LaggedStartMap(FadeIn, yd.cells, lag_ratio=0.08), FadeIn(lam_lab), run_time=1.2)

    # ---- 一個格子的鉤
    ov = yd.hook_highlight(ci, cj, color=HOOK_COLOR, opacity=0.45, cell_color=ROOT_COLOR, cell_opacity=0.75)
    arm_brace = Brace(yd.cell_group(arm), UP, buff=0.08)
    arm_lab = zh("臂", font_size=28, color=HOOK_COLOR).next_to(arm_brace, UP, buff=0.08)
    leg_brace = Brace(yd.cell_group(leg), DOWN, buff=0.08)
    leg_lab = zh("腿", font_size=28, color=HOOK_COLOR).next_to(leg_brace, DOWN, buff=0.06)
    assert_apart(leg_lab, yd.cell(2, 0))

    rules = VGroup(
        mixed("鉤 ＝ ", zh("格子本身", font_size=30, color=ROOT_COLOR), " ＋ ",
              zh("臂", font_size=30, color=HOOK_COLOR), " ＋ ", zh("腿", font_size=30, color=HOOK_COLOR),
              font_size=30),
        zh("臂：同一列、在它右邊的格子", font_size=28),
        zh("腿：同一行、在它下面的格子", font_size=28),
        mixed("鉤長 ", "$h(c)$", " ＝ 臂長 ＋ 腿長 ＋ 1", font_size=30),
        Tex(r"h=" + f"{len(arm)}+{len(leg)}+1={h_ex}", font_size=46, fill_color=HOOK_COLOR),
    ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    rules.move_to(np.array([2.0, 0.6, 0.0]))
    assert_in_frame(rules, yd, lam_lab, arm_lab, leg_lab)
    assert rules.get_left()[0] > yd.get_right()[0] + 0.5

    scene.say("第 1 列第 2 格的鉤：它自己，加上同列右邊的格子（臂）和同行下面的格子（腿）")
    scene.play(FadeIn(ov[0]), FadeIn(rules[0]), run_time=0.8)
    scene.play(FadeIn(ov[1:3]), GrowFromCenter(arm_brace), FadeIn(arm_lab), FadeIn(rules[1]), run_time=0.8)
    scene.play(FadeIn(ov[3:]), GrowFromCenter(leg_brace), FadeIn(leg_lab), FadeIn(rules[2]), run_time=0.8)
    scene.wait(0.6)
    nums = hook_numbers(yd, lam)
    ex_k = young_cells(lam).index(EX_CELL)
    scene.say("鉤長 ", "$h$", " ＝ 鉤裡的格子數：", "$2+1+1=4$")
    scene.play(FadeIn(rules[3]), run_time=0.6)
    scene.play(Write(rules[4]), TransformFromCopy(rules[4][-1], nums[ex_k]), run_time=1.0)
    scene.wait(0.7)

    # ---- 每一格的鉤長
    scene.say("每一格都這樣數，填上鉤長")
    scene.play(FadeOut(VGroup(ov, arm_brace, arm_lab, leg_brace, leg_lab, rules)), run_time=0.5)
    for k, (i, j) in enumerate(young_cells(lam)):
        if (i, j) == EX_CELL:
            continue
        o = yd.hook_highlight(i, j, color=HOOK_COLOR, opacity=0.4, cell_color=ROOT_COLOR, cell_opacity=0.7)
        scene.play(FadeIn(o), FadeIn(nums[k]), run_time=0.28)
        scene.play(FadeOut(o), run_time=0.16)
    scene.wait(0.4)

    # ---- 乘積與 n!/H
    l1 = Tex(r"H(\lambda)=\prod_{c\in\lambda}h(c)", font_size=44)
    l2 = Tex("=" + dot_join(flat(table)) + f"={H}", font_size=44)
    l3 = Tex(r"\frac{" + f"{n}!" + r"}{H(\lambda)}=\frac{" + f"{factorial(n)}" + "}{" + f"{H}" + "}=" +
             f"{factorial(n) // H}", font_size=46)
    l4 = mixed("＝ ", "$f^{\\lambda}$", "＝ 形狀 ", "$\\lambda$", " 的標準 Young 表個數", font_size=28)
    upper = VGroup(l1, l2).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    l2.shift(0.5 * RIGHT)
    lower = VGroup(l3, l4).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    block = VGroup(upper, lower).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    block.move_to(np.array([2.1, 0.6, 0.0]))
    fit_width(block, X_MAX - 0.2 - (yd.get_right()[0] + 0.6))
    box = SurroundingRectangle(lower, buff=0.18, color=YELLOW, stroke_width=3)
    assert_in_frame(block, box)
    assert block.get_left()[0] > yd.get_right()[0] + 0.5
    assert box.get_top()[1] < l2.get_bottom()[1] - 0.12   # 黃框不碰到上一行
    scene.say("把所有鉤長乘起來：", "$H(\\lambda)=576$")
    scene.play(FadeIn(l1), run_time=0.6)
    digits = VGroup(*[l2[1 + 2 * k] for k in range(len(nums))])
    others = VGroup(*[g for g in l2 if g not in digits.submobjects])
    scene.play(TransformFromCopy(nums, digits), FadeIn(others), run_time=1.2)
    scene.wait(0.6)
    scene.say("$8!$", " 除以它，正好是 70 ＝ 標準 Young 表的個數 ", "$f^{\\lambda}$")
    scene.play(Write(l3), run_time=1.0)
    scene.play(FadeIn(l4, shift=0.2 * UP), run_time=0.6)
    scene.play(ShowCreation(box), run_time=0.5)
    scene.wait(1.2)


# =============================================================================
# 第 2 段：鉤長公式與驗算
# =============================================================================
def part_formula(scene):
    scene.clear_stage()
    formula = Tex(r"f^{\lambda}=\frac{n!}{\prod_{c\in\lambda}h(c)}", font_size=50)
    title = zh("Frame–Robinson–Thrall（1954）", font_size=26, color=MUTED_COLOR)
    fbox = boxed(formula, buff=0.2)
    top = VGroup(fbox, title).arrange(RIGHT, buff=0.5).move_to(np.array([0.6, 2.36, 0.0]))
    assert_in_frame(top)
    scene.say("鉤長公式：", "$f^{\\lambda}=n!/\\prod h(c)$", "，對每個形狀都成立")
    scene.play(Write(formula), ShowCreation(fbox[0]), FadeIn(title), run_time=1.2)

    # ---- (3,2)：接 M11
    hs = hook_lengths(SMALL)
    Hs = hook_product(SMALL)
    ns = sum(SMALL)
    assert hs == [(4, 3, 1), (2, 1)] and Hs == 24 and factorial(ns) == 120
    assert hook_formula(SMALL) == syt_count(SMALL) == len(syt(SMALL)) == 5
    yd_s = YoungDiagramMob(SMALL, cell_size=0.6, center=np.array([-3.6, 0.4, 0.0]))
    num_s = hook_numbers(yd_s, SMALL)
    lab_s = Tex(r"\lambda=" + lam_tex(SMALL), font_size=36).next_to(yd_s, LEFT, buff=0.35)
    eq_s = Tex(r"\frac{" + f"{ns}!" + "}{" + dot_join(flat(hs)) + r"}=\frac{" + f"{factorial(ns)}" + "}{" +
               f"{Hs}" + "}=" + f"{hook_formula(SMALL)}", font_size=40)
    eq_s.next_to(yd_s, DOWN, buff=0.35).set_x(-3.6)

    # ---- (3,3)：接 M12
    hq = hook_lengths(SQUARE)
    Hq = hook_product(SQUARE)
    nq = sum(SQUARE)
    assert hq == [(4, 3, 2), (3, 2, 1)] and Hq == 144 and factorial(nq) == 720
    assert hook_formula(SQUARE) == syt_count(SQUARE) == catalan(3) == 5
    yd_q = YoungDiagramMob(SQUARE, cell_size=0.6, center=np.array([3.0, 0.4, 0.0]))
    num_q = hook_numbers(yd_q, SQUARE, row_colors=[LEFT_COLOR, RIGHT_COLOR])
    lab_q = Tex(r"\lambda=" + lam_tex(SQUARE), font_size=36).next_to(yd_q, LEFT, buff=0.35)
    eq_q = Tex(r"\frac{" + f"{nq}!" + "}{(" + dot_join(hq[0]) + ")(" + dot_join(hq[1]) + r")}=\frac{" +
               f"{factorial(nq)}" + "}{" + f"{Hq}" + "}=" + f"{hook_formula(SQUARE)}=C_3", font_size=40)
    eq_q.next_to(yd_q, DOWN, buff=0.35).set_x(3.0)
    assert_in_frame(VGroup(yd_s, lab_s, eq_s), VGroup(yd_q, lab_q, eq_q))
    assert_apart(VGroup(yd_s, lab_s, eq_s), VGroup(yd_q, lab_q, eq_q), gap=0.4)
    assert_apart(top, VGroup(yd_s, lab_s, yd_q, lab_q), gap=0.3)

    scene.say("驗算 ", "$(3,2)$", "：", "$5!/24=5$", "，就是 M11 列出的 5 個標準 Young 表")
    scene.play(FadeIn(yd_s), FadeIn(lab_s), run_time=0.6)
    scene.play(LaggedStartMap(FadeIn, num_s, lag_ratio=0.15), run_time=0.9)
    scene.play(Write(eq_s), run_time=1.0)
    scene.wait(0.8)
    scene.say("$(3,3)$", "：", "$720/144=5=C_3$", "，和 M12 的 Dyck 路徑一樣多")
    scene.play(FadeIn(yd_q), FadeIn(lab_q), run_time=0.6)
    scene.play(LaggedStartMap(FadeIn, num_q, lag_ratio=0.12), run_time=0.9)
    scene.play(Write(eq_q), run_time=1.0)
    scene.wait(0.8)

    # ---- 一般 (n,n)
    for m in range(1, 8):
        hm = hook_lengths((m, m))
        assert list(hm[0]) == list(range(m + 1, 1, -1)) and list(hm[1]) == list(range(m, 0, -1))
        assert hook_product((m, m)) == factorial(m + 1) * factorial(m)
        assert hook_formula((m, m)) == syt_count((m, m)) == catalan(m)
    gen = Tex(r"\lambda=(n,n):\quad \prod h(c)=(n+1)!\cdot n!\quad\Longrightarrow\quad "
              r"f^{(n,n)}=\frac{(2n)!}{(n+1)!\cdot n!}=C_n",
              font_size=40, t2c={"(n+1)!": LEFT_COLOR, "n!": RIGHT_COLOR, "C_n": YELLOW})
    gen.move_to(np.array([0.0, -2.4, 0.0]))
    fit_width(gen, X_MAX - X_MIN - 0.4)
    assert_in_frame(gen)
    assert_apart(gen, VGroup(eq_s, eq_q), gap=0.2)
    scene.say("一般的 ", "$(n,n)$", "：第一列鉤長 ", "$n+1,\\dots,2$", "、第二列 ", "$n,\\dots,1$",
              "，公式給出 ", "$C_n$", t2c={"C_n": YELLOW})
    scene.play(Indicate(num_q[:3], color=LEFT_COLOR), Indicate(num_q[3:], color=RIGHT_COLOR), run_time=1.0)
    scene.play(Write(gen), run_time=1.5)
    scene.wait(1.4)


# =============================================================================
# 第 3 段：角落遞迴
# =============================================================================
def part_corner(scene):
    scene.clear_stage()
    lam = SMALL
    n = sum(lam)
    cs_list = corners(lam)
    assert cs_list == [(0, 2), (1, 1)]
    subs = [remove_corner(lam, c) for c in cs_list]
    assert subs == [(2, 2), (3, 1)]
    tabs = syt(lam)
    groups = []
    for c in cs_list:
        g = [T for T in tabs if T[c[0]][c[1]] == n]
        groups.append(g)
    assert sum(len(g) for g in groups) == len(tabs) == syt_count(lam) == 5
    # 最大的數一定在某個角落
    for T in tabs:
        pos = [(i, j) for i, row in enumerate(T) for j, v in enumerate(row) if v == n]
        assert len(pos) == 1 and pos[0] in cs_list
    fs_sub = [syt_count(s) for s in subs]
    assert [len(g) for g in groups] == fs_sub == [2, 3]

    top = mixed("最大的數 ", "$n$", zh("一定在角落：它的右邊、下面都不能再有格子", font_size=30,
                                     t2c={"角落": CORNER_COLOR}), font_size=30)
    top.move_to(np.array([0.0, 2.65, 0.0]))
    fit_width(top, 12.6)

    big = YoungDiagramMob(lam, cell_size=0.55, center=np.array([-5.55, 0.75, 0.0]))
    big.fill_cells(cs_list, CORNER_COLOR, opacity=0.55)
    big_lab = Tex(r"\lambda=" + lam_tex(lam), font_size=34).next_to(big, DOWN, buff=0.3)

    row_y = [1.45, -0.05]
    rows = VGroup()
    for r, (c, g, s, f) in enumerate(zip(cs_list, groups, subs, fs_sub)):
        tabs_mob = VGroup(*[tableau_mob(T, lam, 0.5, np.array([-3.1 + 1.75 * k, row_y[r], 0.0]), mark=n)
                            for k, T in enumerate(g)])
        arrow = Arrow(np.array([1.35, row_y[r], 0.0]), np.array([2.45, row_y[r], 0.0]), buff=0.0,
                      thickness=3, fill_color=GREY_B)
        arrow_lab = mixed("拿掉 ", "$" + str(n) + "$", font_size=22).next_to(arrow, UP, buff=0.08)
        sub_yd = YoungDiagramMob(s, cell_size=0.5, center=np.array([3.4, row_y[r], 0.0]), stroke_width=2)
        f_lab = Tex(r"f^{" + lam_tex(s) + "}=" + str(f), font_size=38).next_to(sub_yd, RIGHT, buff=0.35)
        rows.add(VGroup(tabs_mob, arrow, arrow_lab, sub_yd, f_lab))
    assert_in_frame(top, big, big_lab, *rows)
    assert_apart(rows[0], rows[1], gap=0.2)
    assert_apart(big, rows[0][0], gap=0.3)
    assert_apart(top, rows[0], gap=0.15)

    total = Tex(r"f^{" + lam_tex(lam) + "}=f^{" + lam_tex(subs[0]) + "}+f^{" + lam_tex(subs[1]) + "}=" +
                f"{fs_sub[0]}+{fs_sub[1]}={syt_count(lam)}", font_size=42)
    general = Tex(r"f^{\lambda}=\sum_{c}f^{\lambda-c}", font_size=46)
    general_zh = mixed("（", "$c$", " 跑遍所有角落）", font_size=24, color=MUTED_COLOR, buff=0.06)
    gen_grp = VGroup(general, general_zh).arrange(RIGHT, buff=0.25)
    gen_box = boxed(gen_grp, buff=0.18)
    bottom = VGroup(total, gen_box).arrange(RIGHT, buff=0.7).move_to(np.array([0.0, -1.95, 0.0]))
    fit_width(bottom, 13.0)
    assert_in_frame(bottom)
    assert_apart(bottom, rows[1], gap=0.15)

    scene.say("標準 Young 表裡，最大的數 ", "$n$", " 只能放在角落")
    scene.play(FadeIn(top), FadeIn(big), FadeIn(big_lab), run_time=0.9)
    scene.wait(0.5)
    scene.say("$(3,2)$", " 的 5 個表，依 5 的位置分成兩組")
    for r in range(2):
        scene.play(LaggedStartMap(FadeIn, rows[r][0], lag_ratio=0.2), run_time=0.9)
    scene.wait(0.6)
    scene.say("拿掉 5，剩下的正是較小形狀的標準 Young 表")
    for r in range(2):
        scene.play(GrowArrow(rows[r][1]), FadeIn(rows[r][2]), FadeIn(rows[r][3]), FadeIn(rows[r][4]),
                   run_time=0.8)
    scene.wait(0.5)
    scene.say("所以 ", "$f^{\\lambda}$", " ＝ 拿掉各個角落之後的 ", "$f$", " 相加")
    scene.play(Write(total), run_time=1.0)
    scene.play(FadeIn(gen_grp), ShowCreation(gen_box[0]), run_time=0.8)
    scene.wait(1.3)


# =============================================================================
# 第 4 段：化約成「機率和 = 1」
# =============================================================================
def part_reduce(scene):
    scene.clear_stage()
    lam = SMALL
    n = sum(lam)
    cs_list = corners(lam)
    subs = [remove_corner(lam, c) for c in cs_list]
    H = hook_product(lam)
    Hsub = [hook_product(s) for s in subs]
    assert H == 24 and Hsub == [12, 8]
    probs = [corner_prob_formula(lam, c) for c in cs_list]
    assert probs == [Fraction(2, 5), Fraction(3, 5)] and sum(probs) == 1
    for c, s, p in zip(cs_list, subs, probs):
        assert p == Fraction(H, n * hook_product(s))
        # F(λ−c)/F(λ) = (1/n)·H(λ)/H(λ−c)
        assert Fraction(factorial(n - 1), hook_product(s)) / Fraction(factorial(n), H) == p

    l1 = mixed("令 ", "$F(\\lambda)=n!/H(\\lambda)$", "。要證 ", "$F=f$", "，對 ", "$n$",
               " 歸納：只需 ", "$F$", " 也滿足角落遞迴", font_size=26)
    l2 = Tex(r"\sum_{c}F(\lambda-c)=F(\lambda)\quad\Longleftrightarrow\quad"
             r"\sum_{c}\frac{(n-1)!}{H(\lambda-c)}\cdot\frac{H(\lambda)}{n!}=1", font_size=36)
    l3 = Tex(r"\sum_{c}\frac{1}{n}\cdot\frac{H(\lambda)}{H(\lambda-c)}=1", font_size=42)
    b3 = boxed(l3, buff=0.18)
    head = VGroup(l1, l2, b3).arrange(DOWN, buff=0.26)
    fit_width(head, 13.0)
    head.move_to(np.array([0.0, Y_MAX - 0.05 - head.get_height() / 2, 0.0]))

    # 三個小圖：(3,2)、(2,2)、(3,1) 與它們的 H
    shapes = [lam] + subs
    xs = [-5.6, -3.4, -1.2]
    minis = VGroup()
    for x, s in zip(xs, shapes):
        yd = YoungDiagramMob(s, cell_size=0.55, center=np.array([x, -1.1, 0.0]), stroke_width=2)
        if s == lam:
            yd.fill_cells(cs_list, CORNER_COLOR, opacity=0.45)
        nums = hook_numbers(yd, s, font_size=26)
        lab = Tex(r"H" + lam_tex(s) + "=" + str(hook_product(s)), font_size=30).next_to(yd, DOWN, buff=0.2)
        minis.add(VGroup(yd, nums, lab))
    for mm in minis:
        mm[2].set_y(minis[0][2].get_y())
    calc = Tex(r"\frac{1}{" + str(n) + r"}\cdot\frac{" + str(H) + "}{" + str(Hsub[0]) + r"}+\frac{1}{" + str(n) +
               r"}\cdot\frac{" + str(H) + "}{" + str(Hsub[1]) + r"}=\frac{" + str(probs[0].numerator) + "}{" +
               str(probs[0].denominator) + r"}+\frac{" + str(probs[1].numerator) + "}{" +
               str(probs[1].denominator) + "}=1", font_size=40)
    calc.move_to(np.array([3.3, -1.25, 0.0]))
    fit_width(calc, X_MAX - 0.2 - (minis.get_right()[0] + 0.5))
    calc.set_x((minis.get_right()[0] + 0.5 + X_MAX - 0.2) / 2)
    assert_in_frame(head, minis, calc)
    assert_apart(head, VGroup(minis, calc), gap=0.25)
    assert_apart(minis, calc, gap=0.3)

    scene.say("怎麼證明鉤長公式？讓 ", "$n!/H(\\lambda)$", " 也滿足同一個角落遞迴")
    scene.play(FadeIn(l1), run_time=0.8)
    scene.play(Write(l2), run_time=1.4)
    scene.wait(0.6)
    scene.say("化約成：對所有角落 ", "$c$", " 加總，", "$\\tfrac{1}{n}H(\\lambda)/H(\\lambda-c)$", " 的和是 1")
    scene.play(TransformFromCopy(l2, l3), ShowCreation(b3[0]), run_time=1.1)
    scene.wait(0.6)
    scene.say("驗算 ", "$(3,2)$", "：兩個角落分別是 ", "$2/5$", " 和 ", "$3/5$", "，加起來正好是 1")
    scene.play(LaggedStartMap(FadeIn, minis, lag_ratio=0.25), run_time=1.2)
    scene.play(Write(calc), run_time=1.4)
    scene.wait(1.0)
    scene.say("這些數像機率：下一幕的「鉤上漫步」會讓它們真的變成機率")
    scene.play(Indicate(calc, color=YELLOW, scale_factor=1.05), run_time=1.0)
    scene.wait(1.5)


class SceneM13HookLength(ChuScene):
    def construct(self):
        self.show_header("鉤長公式")
        part_hook(self)
        part_formula(self)
        part_corner(self)
        part_reduce(self)
