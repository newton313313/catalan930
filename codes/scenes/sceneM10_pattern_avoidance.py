"""
Scene M10 —— 模式迴避（MIT 18.212 L3）

    w 含有模式 π  <=>  w 有一個子序列，大小順序和 π 一樣
    例：41532 的 4,5,3 -> 231；52143 的 10 個子序列都不是 231 -> 避開 231
    n=3：6 個中 5 個避開 231；n=4：24 個中 14 個
    定理：堆疊可排序 <=> 避開 231；避開任一個長度 3 的模式都恰有 C_n 個

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM10_pattern_avoidance.py SceneM10PatternAvoidance
"""
import sys
from itertools import combinations, permutations
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import PATTERNS_3, avoiders, catalan, contains_pattern, stack_sort, standardize
from utils.mit_draw import CATALAN_COLOR, perm_row
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, OK_COLOR, boxed, mixed, zh

W = (4, 1, 5, 3, 2)          # 含 231（4, 5, 3）
AV = (5, 2, 1, 4, 3)         # 避開 231（也能用堆疊排序，接 M09）
PAT = (2, 3, 1)
RANK_NAME = {1: "小", 2: "中", 3: "大"}
X_LIM, Y_LO, Y_HI = 6.8, -3.0, 3.2


# ---------------------------------------------------------------------- 模組層級的小工具
def word(p) -> str:
    return "".join(str(x) for x in p)


def check_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= -X_LIM and m.get_right()[0] <= X_LIM, m
        assert m.get_bottom()[1] >= Y_LO and m.get_top()[1] <= Y_HI, m


def name_row(perm, name, center, size=0.7, **kw):
    """perm_row 加上左邊的名字（例如 w =）。"""
    row = perm_row(perm, size=size, center=center, **kw)
    lab = Tex(name, font_size=42).next_to(row, LEFT, buff=0.25)
    return row, lab


def neutral_item(p, size):
    return perm_row(p, size=size, buff=0.05, color=GREY_B, fill_opacity=0.08, font_size=24)


def judged_item(p, size):
    """避開 231 -> 整排藍色；含 231 -> 第一個出現的位置標紅，其餘變暗。"""
    occ = contains_pattern(p, PAT)
    if occ is None:
        return perm_row(p, size=size, buff=0.05, color=CATALAN_COLOR, fill_opacity=0.35, font_size=24)
    return perm_row(p, size=size, buff=0.05, highlight=occ, highlight_color=CROSSING_COLOR,
                    color=GREY_D, text_color=GREY_B, fill_opacity=0.15, font_size=24)


def count_label(k):
    return mixed(f"${k}$", " 個", font_size=26, color=CATALAN_COLOR)


def reverse(p):
    return tuple(reversed(p))


def complement(p):
    return tuple(len(p) + 1 - x for x in p)


class SceneM10PatternAvoidance(ChuScene):
    def construct(self):
        self.show_header("模式迴避")

        # ============================================================ 1. 定義：41532 含有 231
        occ = contains_pattern(W, PAT)
        sub = tuple(W[i] for i in occ)
        assert occ == (0, 2, 3) and sub == (4, 5, 3) and standardize(sub) == PAT

        w_row, w_lab = name_row(W, "w=", np.array([-1.6, 2.1, 0.0]))
        p_row, p_lab = name_row(PAT, "\\pi=", np.array([4.3, 2.1, 0.0]))
        self.say("排列 ", "$w=41532$", "，模式 ", "$\\pi=231$")
        self.play(FadeIn(w_lab), LaggedStartMap(FadeIn, w_row, lag_ratio=0.15), run_time=1.0)
        self.play(FadeIn(p_lab), FadeIn(p_row), run_time=0.6)
        self.say("$w$", " 含有 ", "$\\pi$", "：", "$w$", " 有一個子序列，大小順序和 ", "$\\pi$", " 一樣")
        self.play(*[w_row[i].square.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.3) for i in occ],
                  run_time=0.7)

        sub_row = perm_row(sub, size=0.7, highlight=(0, 1, 2), fill_opacity=0.3,
                           center=np.array([-3.0, 0.45, 0.0]))
        self.play(TransformFromCopy(VGroup(*[w_row[i] for i in occ]), sub_row), run_time=1.0)
        ranks = VGroup(*[zh(RANK_NAME[r], font_size=26, color=YELLOW).next_to(b, DOWN, buff=0.15)
                         for r, b in zip(standardize(sub), sub_row)])
        std_row = perm_row(standardize(sub), size=0.7, highlight=(0, 1, 2), fill_opacity=0.3,
                           center=np.array([2.0, 0.45, 0.0]))
        arrow = Arrow(sub_row.get_right(), std_row.get_left(), buff=0.3, stroke_width=4)
        arrow_lab = zh("只看大小順序", font_size=22, color=MUTED_COLOR).next_to(arrow, UP, buff=0.12)
        eq_pi = Tex("=\\pi", font_size=44, fill_color=YELLOW).next_to(std_row, RIGHT, buff=0.25)
        self.play(LaggedStartMap(FadeIn, ranks, lag_ratio=0.25), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(arrow_lab), run_time=0.6)
        self.play(TransformFromCopy(sub_row, std_row), run_time=0.8)
        self.play(FadeIn(eq_pi, shift=0.2 * LEFT), run_time=0.5)

        pos = ",".join(str(i + 1) for i in occ)
        assert pos == "1,3,4"
        result = boxed(mixed("$41532$", " 含有模式 ", "$231$", font_size=30), buff=0.2)
        result.move_to(np.array([0.0, -1.15, 0.0]))
        note = mixed("子序列的數不必相鄰：這裡取第 ", f"${pos}$", " 個數", font_size=24, color=MUTED_COLOR)
        note.next_to(result, DOWN, buff=0.3)
        check_in_frame(w_lab, w_row, p_lab, p_row, ranks, eq_pi, result, note)
        self.play(FadeIn(result), run_time=0.6)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.6)

        # ============================================================ 1b. 52143 避開 231
        self.clear_stage()
        triples = list(combinations(range(len(AV)), 3))
        assert len(triples) == comb(5, 3) == 10
        assert contains_pattern(AV, PAT) is None and stack_sort(AV)[0]
        pats = [standardize([AV[i] for i in t]) for t in triples]
        assert PAT not in pats
        seen = list(dict.fromkeys(pats))          # 依第一次出現的順序
        assert seen == [(3, 2, 1), (3, 1, 2), (2, 1, 3), (1, 3, 2)]

        a_row, a_lab = name_row(AV, "w=", np.array([0.4, 2.1, 0.0]))
        self.say("再看 ", "$w=52143$", "：", "$\\binom{5}{3}=10$", " 個子序列逐一檢查")
        self.play(FadeIn(a_lab), LaggedStartMap(FadeIn, a_row, lag_ratio=0.15), run_time=0.9)

        items = VGroup()
        for k, (t, pt) in enumerate(zip(triples, pats)):
            it = VGroup(Tex(word(AV[i] for i in t), font_size=34),
                        Tex("\\to", font_size=34, fill_color=MUTED_COLOR),
                        Tex(word(pt), font_size=34, fill_color=OK_COLOR)).arrange(RIGHT, buff=0.15)
            it.move_to(np.array([-4.8 + 2.4 * (k % 5), 0.75 - 0.85 * (k // 5), 0.0]))
            items.add(it)
        rects = None
        for t, it in zip(triples, items):
            new = VGroup(*[SurroundingRectangle(a_row[i], buff=0.05, color=YELLOW, stroke_width=4) for i in t])
            anims = [FadeIn(it, shift=0.15 * DOWN)]
            anims.append(ShowCreation(new) if rects is None else Transform(rects, new))
            self.play(*anims, run_time=0.38)
            if rects is None:
                rects = new
        self.play(FadeOut(rects), run_time=0.3)

        av_res = boxed(mixed("沒有一個是 ", "$231$", "：", "$52143$", " 避開 ", "$231$", font_size=30),
                       buff=0.2)
        av_res.move_to(np.array([0.0, -1.35, 0.0]))
        av_note = mixed("（它也能用堆疊排序，見 M09）", font_size=24, color=MUTED_COLOR)
        av_note.next_to(av_res, DOWN, buff=0.3)
        check_in_frame(a_lab, a_row, items, av_res, av_note)
        self.say("出現了 ", "$" + ",".join(word(q) for q in seen) + "$", "，就是沒有 ", "$231$")
        self.play(FadeIn(av_res), run_time=0.6)
        self.play(FadeIn(av_note), run_time=0.5)
        self.wait(1.4)

        # ============================================================ 2. n=3、n=4 全部列出
        self.clear_stage()
        col_x = [-4.8 + 1.8 * k for k in range(6)]
        perms3 = list(permutations(range(1, 4)))
        perms4 = list(permutations(range(1, 5)))
        av3, av4 = avoiders(3, PAT), avoiders(4, PAT)
        assert len(perms3) == factorial(3) == 6 and len(perms4) == factorial(4) == 24
        assert len(av3) == 5 == catalan(3) and len(av4) == 14 == catalan(4)
        assert [p for p in perms3 if p not in av3] == [PAT]
        assert perms4 == sorted(perms4) and all(p[0] == k // 6 + 1 for k, p in enumerate(perms4))

        y3, ys4 = 2.45, [1.4, 0.82, 0.24, -0.34]
        lab3 = Tex("n=3", font_size=36).move_to(np.array([-6.25, y3, 0.0]))
        lab4 = Tex("n=4", font_size=36).move_to(np.array([-6.25, np.mean(ys4), 0.0]))
        n3 = VGroup(*[neutral_item(p, 0.42).move_to(np.array([x, y3, 0.0])) for p, x in zip(perms3, col_x)])
        j3 = VGroup(*[judged_item(p, 0.42).move_to(m) for p, m in zip(perms3, n3)])
        n4 = VGroup(*[neutral_item(p, 0.36).move_to(np.array([col_x[k % 6], ys4[k // 6], 0.0]))
                      for k, p in enumerate(perms4)])
        j4 = VGroup(*[judged_item(p, 0.36).move_to(m) for p, m in zip(perms4, n4)])
        c3 = count_label(len(av3)).move_to(np.array([5.9, y3, 0.0]))
        c4 = count_label(len(av4)).move_to(np.array([5.9, np.mean(ys4), 0.0]))

        self.say("$n=3$", "：6 個排列，哪些避開 ", "$231$", "？")
        self.play(FadeIn(lab3), LaggedStartMap(FadeIn, n3, lag_ratio=0.12), run_time=1.0)
        self.play(*[Transform(a, b) for a, b in zip(n3, j3)], run_time=0.9)
        self.say("只有 ", "$231$", " 自己含有 ", "$231$", "：5 個避開")
        self.play(FadeIn(c3, shift=0.2 * LEFT), run_time=0.5)
        self.wait(0.6)

        self.say("$n=4$", "：24 個排列（字典序，每一列開頭相同）")
        self.play(FadeIn(lab4), LaggedStartMap(FadeIn, n4, lag_ratio=0.04), run_time=1.3)
        self.say("藍色：避開 ", "$231$", "；紅色格子：找到的一個 ", "$231$")
        self.play(LaggedStart(*[Transform(a, b) for a, b in zip(n4, j4)], lag_ratio=0.05), run_time=2.2)
        self.play(FadeIn(c4, shift=0.2 * LEFT), run_time=0.5)

        summ = boxed(mixed("$5=C_3,\\quad 14=C_4$", "：又是卡塔蘭數", font_size=30,
                           t2c={"C_3": CATALAN_COLOR, "C_4": CATALAN_COLOR}), buff=0.2)
        summ.move_to(np.array([0.0, -1.55, 0.0]))
        check_in_frame(lab3, lab4, n3, j3, n4, j4, c3, c4, summ)
        self.play(FadeIn(summ), run_time=0.6)
        self.wait(1.6)

        # ============================================================ 3. 定理與計數表
        self.clear_stage()
        N = 6
        table = {p: [len(avoiders(n, p)) for n in range(1, N + 1)] for p in PATTERNS_3}
        cat = [catalan(n) for n in range(1, N + 1)]
        assert cat == [1, 2, 5, 14, 42, 132]
        assert all(v == cat for v in table.values()) and len(PATTERNS_3) == 6
        for n in range(1, N + 1):
            assert all(stack_sort(p)[0] == (contains_pattern(p, PAT) is None)
                       for p in permutations(range(1, n + 1)))

        thm = VGroup(
            mixed("堆疊可排序 ", "$\\Longleftrightarrow$", " 避開 ", "$231$", "（M09）", font_size=28),
            mixed("避開任何一個長度 3 的模式：個數都是 ", "$C_n$", font_size=28, t2c={"C_n": CATALAN_COLOR}),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        thm_box = boxed(thm, buff=0.22)
        thm_box.move_to(np.array([0.0, 2.3, 0.0]))

        pat_x, n_x = -3.9, [-2.3 + 1.25 * k for k in range(N)]
        y_head, row_y, y_cat = 1.05, [0.58 - 0.43 * r for r in range(6)], -2.15
        head = VGroup(zh("模式", font_size=26, color=MUTED_COLOR).move_to(np.array([pat_x, y_head, 0.0])),
                      *[Tex(f"n={n}", font_size=30, fill_color=MUTED_COLOR).move_to(np.array([x, y_head, 0.0]))
                        for n, x in zip(range(1, N + 1), n_x)])
        rows_lab = VGroup(*[Tex(word(p), font_size=32, fill_color=YELLOW if p == PAT else WHITE)
                            .move_to(np.array([pat_x, y, 0.0])) for p, y in zip(PATTERNS_3, row_y)])
        cols = VGroup(*[VGroup(*[Tex(str(table[p][k]), font_size=32).move_to(np.array([x, y, 0.0]))
                                 for p, y in zip(PATTERNS_3, row_y)]) for k, x in enumerate(n_x)])
        cat_row = VGroup(Tex("C_n", font_size=34, fill_color=CATALAN_COLOR).move_to(np.array([pat_x, y_cat, 0.0])),
                         *[Tex(str(c), font_size=34, fill_color=CATALAN_COLOR).move_to(np.array([x, y_cat, 0.0]))
                           for c, x in zip(cat, n_x)])
        left_x, right_x = pat_x - 0.7, n_x[-1] + 0.6
        lines = VGroup(
            Line(np.array([left_x, y_head - 0.24, 0.0]), np.array([right_x, y_head - 0.24, 0.0])),
            Line(np.array([left_x, y_cat + 0.3, 0.0]), np.array([right_x, y_cat + 0.3, 0.0])),
            Line(np.array([pat_x + 0.65, y_head + 0.25, 0.0]), np.array([pat_x + 0.65, y_cat - 0.25, 0.0])),
        ).set_stroke(GREY_B, 2)
        check_in_frame(thm_box, head, rows_lab, cols, cat_row, lines)

        self.say("定理（第一行在 M09 已經看過）")
        self.play(FadeIn(thm_box[1][0]), ShowCreation(thm_box[0]), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(thm_box[1][1]), run_time=0.7)
        self.say("6 個長度 3 的模式，", "$n\\le 6$", " 由程式逐一數出")
        self.play(FadeIn(head), ShowCreation(lines), LaggedStartMap(FadeIn, rows_lab, lag_ratio=0.1), run_time=1.0)
        for col in cols:
            self.play(LaggedStartMap(FadeIn, col, lag_ratio=0.08), run_time=0.45)
        self.play(FadeIn(cat_row, shift=0.2 * UP), run_time=0.7)
        col_h = row_y[0] - y_cat + 0.42
        col_boxes = VGroup(*[Rectangle(width=0.95, height=col_h).move_to(np.array([x, (row_y[0] + y_cat) / 2, 0.0]))
                             for x in n_x]).set_stroke(CATALAN_COLOR, 2.5)
        check_in_frame(col_boxes)
        self.play(LaggedStartMap(ShowCreation, col_boxes, lag_ratio=0.12), run_time=1.0)

        # 左右反轉、上下翻轉（補）不改變個數 -> 只分成兩類
        cls_a = {PAT, reverse(PAT), complement(PAT), reverse(complement(PAT))}
        cls_b = {(1, 2, 3), reverse((1, 2, 3))}
        assert cls_a == {(1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2)} and cls_b == {(1, 2, 3), (3, 2, 1)}
        assert cls_a | cls_b == set(PATTERNS_3) and complement((1, 2, 3)) == (3, 2, 1)
        self.say("左右反轉、上下翻轉不改變個數：", "$\\{132,213,231,312\\}$", "、", "$\\{123,321\\}$", " 各一類")
        self.wait(2.2)
