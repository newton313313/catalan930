"""
Scene M11 —— 整數分割、合成、Young 圖、標準 Young 表（MIT 18.212 L3）

    整數分割 λ ⊢ n：λ1 ≥ λ2 ≥ … ≥ λk > 0，總和 n；5 的分割有 7 個
    合成：有順序的和，5 的合成有 16 = 2^4 個；(3,2) 是分割，(2,3) 只是合成
    注意：整數分割 ≠ Chu 的集合分割（把有編號的點分成區塊）
    Young 圖（英式）：(5,3,3,2,1)；SYT：列 →、行 ↓ 都遞增；f^(3,2) = 5

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM11_partitions_young.py SceneM11PartitionsYoung
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.circle_points import label_points
from utils.counting import (
    integer_compositions,
    integer_partitions,
    is_noncrossing,
    partition_count,
    syt,
    syt_bruteforce,
    syt_count,
    catalan,
    young_cells,
)
from utils.mit_draw import CATALAN_COLOR, YoungDiagramMob
from utils.polygon_groups import make_configuration
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh

N = 5
YOUNG_EX = (5, 3, 3, 2, 1)
SHAPE = (3, 2)
GOOD_T = ((1, 2, 4), (3, 5))          # 第 3 節的 SYT (3,3) 拿掉 6 就是它
BAD_T = ((1, 4, 5), (2, 3))           # 每列都遞增，但第 2 行 4 在 3 上面
SET_BLOCKS = [(0, 1, 4), (2, 3)]      # Chu 的集合分割 {1,2,5},{3,4}（0 起算）

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊（至少一個方向分開 gap）。"""
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a, b)


def sum_tex(parts, font_size=34, color=WHITE):
    return Tex("+".join(str(p) for p in parts), font_size=font_size, fill_color=color)


def tuple_tex(parts, font_size=26, color=WHITE):
    return Tex("(" + ",".join(str(p) for p in parts) + ")", font_size=font_size, fill_color=color)


def is_nonincreasing(c):
    return all(c[k] >= c[k + 1] for k in range(len(c) - 1))


def rows_increase(T):
    return all(r[j] < r[j + 1] for r in T for j in range(len(r) - 1))


def bad_columns(T):
    return [j for j in range(len(T[0])) for i in range(len(T) - 1)
            if j < len(T[i + 1]) and T[i][j] > T[i + 1][j]]


def check_math():
    parts = integer_partitions(N)
    comps = integer_compositions(N)
    assert len(parts) == 7 == partition_count(N)
    assert len(comps) == 16 == 2 ** (N - 1)
    assert sorted(c for c in comps if is_nonincreasing(c)) == sorted(parts)
    assert (3, 2) in parts and (2, 3) in comps and (2, 3) not in parts
    assert parts == [(5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1)]
    assert is_nonincreasing(YOUNG_EX) and sum(YOUNG_EX) == 14 and YOUNG_EX in integer_partitions(14)
    assert len(young_cells(YOUNG_EX)) == 14
    tabs = syt(SHAPE)
    assert len(tabs) == 5 == syt_count(SHAPE) == len(syt_bruteforce(SHAPE))
    assert set(tabs) == syt_bruteforce(SHAPE)
    assert GOOD_T in tabs and tabs.index(GOOD_T) == 1
    assert BAD_T not in syt_bruteforce(SHAPE) and rows_increase(BAD_T) and bad_columns(BAD_T) == [1]
    assert sorted(v for r in BAD_T for v in r) == list(range(1, 6))
    assert is_noncrossing(SET_BLOCKS)
    assert all(syt_count((k, k)) == catalan(k) for k in range(1, 7))   # 結尾預告 f^(n,n)=C_n
    return parts, comps, tabs


# =============================================================================
def part_partitions(scene, parts, comps):
    defn = Tex(r"\lambda=(\lambda_1,\lambda_2,\dots,\lambda_k),\quad "
               r"\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_k>0", font_size=40)
    defn2 = mixed("$\\lambda_1+\\lambda_2+\\cdots+\\lambda_k=n$", "，記作 ", "$\\lambda\\vdash n$", font_size=28)
    VGroup(defn, defn2).arrange(DOWN, buff=0.3).move_to(2.5 * UP)
    scene.say("整數分割：把 ", "$n$", " 寫成由大到小排好的正整數之和")
    scene.play(Write(defn), run_time=1.4)
    scene.play(FadeIn(defn2, shift=0.2 * UP), run_time=0.7)
    scene.wait(0.8)

    # ---------------------------------------------------- 5 的 7 個分割
    p_label = mixed("$n=5$", " 的整數分割共 ", "$7$", " 個：", font_size=26)
    p_items = VGroup(*[sum_tex(p, 36) for p in parts]).arrange(RIGHT, buff=0.6)
    p_label.move_to(1.2 * UP)
    p_items.move_to(0.62 * UP)
    scene.say("例如 ", "$n=5$", "：由大到小排好，共有 7 種寫法")
    scene.play(FadeIn(p_label), LaggedStart(*[FadeIn(m, shift=0.15 * UP) for m in p_items], lag_ratio=0.15),
               run_time=1.6)
    scene.wait(0.8)

    # ---------------------------------------------------- 5 的 16 個合成
    c_label = mixed("合成（composition）：順序不同就算不同，共 ", "$16=2^{4}$", " 個", font_size=26)
    c_label.move_to(0.05 * DOWN)
    xs = [-4.8, -1.6, 1.6, 4.8]
    ys = [-0.62, -1.27, -1.92, -2.57]
    c_items = VGroup()
    for k, c in enumerate(comps):
        m = sum_tex(c, 32, GREY_B)
        m.move_to(np.array([xs[k % 4], ys[k // 4], 0.0]))
        c_items.add(m)
    assert all(m.get_width() < 2.6 for m in c_items)
    assert_in_frame(defn, defn2, p_label, p_items, c_label, c_items)
    assert_apart(p_items, c_label)
    assert_apart(c_label, c_items)
    assert_apart(defn2, p_label)
    scene.say("如果順序不同算不同的，叫做「合成」：5 的合成有 ", "$2^{4}=16$", " 個")
    scene.play(FadeIn(c_label),
               LaggedStart(*[FadeIn(m) for m in c_items], lag_ratio=0.06), run_time=1.8)
    scene.wait(0.6)

    is_p = [is_nonincreasing(c) for c in comps]
    assert sum(is_p) == 7
    scene.say("其中由大到小排好的 7 個，正好就是 5 的整數分割")
    scene.play(*[m.animate.set_fill(CATALAN_COLOR) for m, ok in zip(c_items, is_p) if ok],
               *[m.animate.set_fill(CATALAN_COLOR) for m in p_items], run_time=0.9)
    scene.wait(1.0)

    # ---------------------------------------------------- (3,2) 對 (2,3)
    k32, k23 = comps.index((3, 2)), comps.index((2, 3))
    box32 = SurroundingRectangle(c_items[k32], buff=0.1, color=OK_COLOR, stroke_width=3)
    box23 = SurroundingRectangle(c_items[k23], buff=0.1, color=CROSSING_COLOR, stroke_width=3)
    box32p = SurroundingRectangle(p_items[parts.index((3, 2))], buff=0.1, color=OK_COLOR, stroke_width=3)
    scene.say("$3+2$", " 是分割 ", "$(3,2)$", "；", "$2+3$", " 不是由大到小，只是合成 ", "$(2,3)$")
    scene.play(ShowCreation(box32), ShowCreation(box32p), ShowCreation(box23),
               c_items[k23].animate.set_fill(CROSSING_COLOR), run_time=0.9)
    scene.wait(2.0)


def part_warning(scene):
    title = zh("注意：兩種「分割」不是同一個東西", font_size=34, color=YELLOW)
    title.move_to(2.45 * UP)

    title_y, mid_y = 1.75, 0.15
    left_title = zh("整數分割（L3–L4、本幕）", font_size=28, color=CATALAN_COLOR)
    left_math = Tex("5=3+2", font_size=60)
    left_note = zh("只看每一份有多大", font_size=24, color=MUTED_COLOR)
    left_title.move_to(np.array([-3.3, title_y, 0.0]))
    left_math.move_to(np.array([-3.3, mid_y, 0.0]))

    right_title = zh("Chu 的集合分割（區塊）", font_size=28, color=OK_COLOR)
    right_title.move_to(np.array([3.3, title_y, 0.0]))
    c_center = np.array([3.3, mid_y, 0.0])
    conf = make_configuration(5, SET_BLOCKS, radius=0.8, center=c_center)
    labs = label_points(conf.coords, center=c_center, buff=0.3, font_size=24)
    right_math = Tex(r"\{1,2,5\},\ \{3,4\}", font_size=36)
    right_math.next_to(VGroup(conf, labs), DOWN, buff=0.25)
    right_note = zh("把有編號的點分成區塊", font_size=24, color=MUTED_COLOR)
    right_note.next_to(right_math, DOWN, buff=0.3)
    left_note.move_to(np.array([-3.3, right_note.get_center()[1], 0.0]))
    left = VGroup(left_title, left_math, left_note)
    right = VGroup(right_title, conf, labs, right_math, right_note)

    neq = Tex(r"\neq", font_size=90, fill_color=YELLOW).move_to(np.array([0.0, left_math.get_center()[1], 0.0]))
    frame_box = SurroundingRectangle(VGroup(title, left, right), buff=0.3, color=YELLOW, stroke_width=3)
    assert_in_frame(frame_box)
    assert_apart(VGroup(conf, labs), right_title)
    assert_apart(VGroup(conf, labs), right_math)
    assert_apart(left, neq)
    assert_apart(right, neq)

    scene.say("注意：這裡的「分割」是整數分割，和 Chu 論文裡的集合分割不同")
    scene.play(ShowCreation(frame_box), FadeIn(title), run_time=0.8)
    scene.play(FadeIn(left, shift=0.2 * RIGHT), run_time=0.8)
    scene.play(FadeIn(right_title), FadeIn(conf), FadeIn(labs), FadeIn(right_math), FadeIn(right_note),
               run_time=0.9)
    scene.play(FadeIn(neq, scale=1.4), run_time=0.5)
    scene.say("整數分割只看大小；Chu 的分割是把有編號的點分成區塊（不交叉）")
    scene.wait(2.6)


def part_young(scene, parts):
    cs = 0.55
    big = YoungDiagramMob(YOUNG_EX, cell_size=cs, top_left=np.array([-5.9, 2.55, 0.0]),
                          fill_color=CATALAN_COLOR, fill_opacity=0.25)
    row_labels = VGroup()
    for i, r in enumerate(YOUNG_EX):
        lab = Tex(str(r), font_size=30, fill_color=YELLOW)
        lab.next_to(big.cell(i, r - 1), RIGHT, buff=0.22)
        row_labels.add(lab)

    lam_tex = Tex(r"\lambda=(5,3,3,2,1)\vdash 14", font_size=44)
    lam_tex.move_to(np.array([2.3, 2.05, 0.0]))
    rules = VGroup(
        mixed("第 ", "$i$", " 列放 ", "$\\lambda_i$", " 個格子，每列靠左", font_size=26),
        mixed("下一列不比上一列長（英式畫法）", font_size=26),
        mixed("格子總數 ", "$=5+3+3+2+1=14$", font_size=26),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    rules.next_to(lam_tex, DOWN, buff=0.45)

    scene.say("Young 圖：第 ", "$i$", " 列畫 ", "$\\lambda_i$", " 個格子（英式：每列靠左、下一列不比上一列長）")
    scene.play(FadeIn(lam_tex), run_time=0.6)
    for i, r in enumerate(YOUNG_EX):
        row = VGroup(*[big.cell(i, j) for j in range(r)])
        scene.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in row], lag_ratio=0.12),
                   FadeIn(row_labels[i]), run_time=0.55)
    scene.play(LaggedStart(*[FadeIn(r, shift=0.15 * UP) for r in rules], lag_ratio=0.4), run_time=1.4)
    scene.wait(1.0)

    # ---------------------------------------------------- 5 的 7 個分割畫成 Young 圖
    small_cs = 0.28
    top_y = -0.85
    max_h = max(len(p) for p in parts) * small_cs
    cols, smalls, small_labs = VGroup(), VGroup(), VGroup()
    for p in parts:
        d = YoungDiagramMob(p, cell_size=small_cs, top_left=np.array([0.0, top_y, 0.0]),
                            fill_color=CATALAN_COLOR, fill_opacity=0.25, stroke_width=2)
        lab = tuple_tex(p, 28)
        lab.move_to(np.array([d.get_center()[0], top_y - max_h - 0.28, 0.0]))
        smalls.add(d)
        small_labs.add(lab)
        cols.add(VGroup(d, lab))
    cols.arrange(RIGHT, buff=0.55, aligned_edge=UP)
    cols.shift((0.0 - cols.get_center()[0]) * RIGHT + (top_y - cols.get_top()[1]) * UP)
    for a, b in zip(cols[:-1], cols[1:]):
        assert_apart(a, b, gap=0.3)
    assert_in_frame(big, row_labels, lam_tex, rules, smalls, small_labs)
    assert_apart(VGroup(big, row_labels), rules)
    assert_apart(big, smalls)
    assert_apart(rules, smalls)

    scene.say("剛才 5 的 7 個分割，畫成 Young 圖就是這 7 個形狀")
    scene.play(LaggedStart(*[FadeIn(VGroup(d, l), shift=0.15 * UP) for d, l in zip(smalls, small_labs)],
                           lag_ratio=0.15), run_time=1.6)
    scene.wait(1.6)


def part_syt(scene, tabs):
    cs = 0.72
    good = YoungDiagramMob(SHAPE, cell_size=cs, top_left=np.array([-5.6, 2.55, 0.0]), entries=GOOD_T,
                           font_size=36)
    bad = YoungDiagramMob(SHAPE, cell_size=cs, top_left=np.array([-1.6, 2.55, 0.0]), entries=BAD_T,
                          font_size=36)
    good_lab = mixed("是 SYT", font_size=26, color=OK_COLOR).next_to(good, DOWN, buff=0.25)
    bad_lab = mixed("第 2 行 ", "$4>3$", "：不是 SYT", font_size=26, color=CROSSING_COLOR)
    bad_lab.next_to(bad, DOWN, buff=0.25)

    rules = VGroup(
        mixed("$1,2,\\dots,n$", " 各填一次", font_size=26),
        mixed("每一列 ", "$\\rightarrow$", " 遞增", font_size=26),
        mixed("每一行 ", "$\\downarrow$", " 遞增", font_size=26),
    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    rules.move_to(np.array([4.4, 1.75, 0.0]))
    rules[1][1].set_fill(YELLOW)
    rules[2][1].set_fill(TEAL)

    scene.say("標準 Young 表（SYT）：把 ", "$1,\\dots,n$", " 填進格子，每列向右、每行向下都遞增")
    scene.play(ShowCreation(good.cells), FadeIn(rules[0]), run_time=0.8)
    order = sorted(((v, (i, j)) for i, r in enumerate(GOOD_T) for j, v in enumerate(r)))
    for v, (i, j) in order:
        scene.play(FadeIn(good.entry(i, j), scale=1.4), run_time=0.35)
    row_rects = VGroup(*[SurroundingRectangle(VGroup(*[good.cell(i, j) for j in range(r)]), buff=0.04,
                                              color=YELLOW, stroke_width=4) for i, r in enumerate(SHAPE)])
    col_rects = VGroup(*[SurroundingRectangle(VGroup(*[good.cell(i, j) for i in range(len(SHAPE))
                                                       if j < SHAPE[i]]), buff=0.04, color=TEAL, stroke_width=4)
                         for j in range(SHAPE[0])])
    scene.play(ShowCreation(row_rects), FadeIn(rules[1]), run_time=0.7)
    scene.wait(0.4)
    scene.play(FadeOut(row_rects), ShowCreation(col_rects), FadeIn(rules[2]), run_time=0.7)
    scene.wait(0.4)
    scene.play(FadeOut(col_rects), FadeIn(good_lab), run_time=0.5)

    # ---------------------------------------------------- 反例
    red_cells = [(0, 1), (1, 1)]
    scene.say("反例：每一列都遞增，但第 2 行上面是 4、下面是 3，不是 SYT")
    scene.play(FadeIn(bad), run_time=0.7)
    scene.play(*[bad.cell(i, j).animate.set_fill(CROSSING_COLOR, opacity=0.45) for i, j in red_cells],
               FadeIn(bad_lab), run_time=0.7)
    scene.wait(1.4)

    # ---------------------------------------------------- (3,2) 的全部 5 個 SYT
    s_cs = 0.55
    alls = VGroup(*[YoungDiagramMob(SHAPE, cell_size=s_cs, entries=T, font_size=28) for T in tabs])
    alls.arrange(RIGHT, buff=0.85)
    alls.move_to(np.array([0.0, -0.95, 0.0]))
    f_tex = Tex(r"f^{(3,2)}=5", font_size=44, t2c={"5": CATALAN_COLOR})
    f_def = mixed("$f^{\\lambda}$", " ＝ 形狀 ", "$\\lambda$", " 的 SYT 個數", font_size=26)
    f_group = VGroup(f_def, f_tex).arrange(RIGHT, buff=0.6)
    f_box = SurroundingRectangle(f_group, buff=0.2, color=YELLOW, stroke_width=3)
    VGroup(f_group, f_box).next_to(alls, DOWN, buff=0.3)
    assert_in_frame(good, bad, good_lab, bad_lab, rules, alls, f_box)
    assert_apart(VGroup(good, good_lab), VGroup(bad, bad_lab))
    assert_apart(VGroup(bad, bad_lab), rules)
    assert_apart(VGroup(good_lab, bad_lab), alls)
    assert_apart(alls, f_box)
    for a, b in zip(alls[:-1], alls[1:]):
        assert_apart(a, b, gap=0.3)

    scene.say("形狀 ", "$(3,2)$", " 的 SYT 全部列出來：剛好 5 個")
    k = tabs.index(GOOD_T)
    scene.play(TransformFromCopy(good, alls[k]), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(alls[m], shift=0.15 * UP) for m in range(len(tabs)) if m != k],
                           lag_ratio=0.2), run_time=1.4)
    scene.play(FadeIn(f_group), ShowCreation(f_box), run_time=0.8)
    scene.say("記 ", "$f^{\\lambda}$", " ＝ SYT 的個數；下一幕：形狀 ", "$(n,n)$", " 的 SYT 個數正是 ", "$C_n$",
              t2c={"C_n": CATALAN_COLOR})
    scene.wait(2.5)


class SceneM11PartitionsYoung(ChuScene):
    def construct(self):
        self.show_header("整數分割、Young 圖與 SYT")
        parts, comps, tabs = check_math()
        part_partitions(self, parts, comps)
        self.clear_stage()
        part_warning(self)
        self.clear_stage()
        part_young(self, parts)
        self.clear_stage()
        part_syt(self, tabs)
        self.wait(1.0)
