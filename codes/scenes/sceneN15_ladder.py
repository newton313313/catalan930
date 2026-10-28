"""
Scene N15 —— 推廣的階梯：一種元數 → 一種別的元數 → 多種元數 → 多棵樹（Raney 導讀第 2.4 小節、表「推廣的階梯」）
執行（在 codes/ 內）：manimgl scenes/sceneN15_ladder.py SceneN15Ladder

1. Fuss–Catalan：只用三角形，6 點 2 個三角形 ↔ 只有 3 和 0 的字，3 種 = (1/5)·C(6,2)。
2. t：Chu 的 A_t 是 C^t 的係數 = t 個分法排成一列 ↔ t 個字接成的字列（t 棵樹的森林）。
   沒有點的分法 ↔ 字 0。一條弦＋一個三角形、t = 2：5 + 5 + 1 + 1 = 12 = (2/7)·42。
3. 階梯總表：卡塔蘭、Fuss–Catalan、Chu 的 C_v(n)、Chu 的 A_t(n) —— 全部是 Raney 的 L(t; a) = (t/m)·M。
"""
import sys
from math import comb, factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan, raney_A
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.polygon_groups import make_configuration
from utils.raney import L_brute, L_formula, lists_with, partition_to_word, split_words
from utils.raney_draw import word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

TRIS = [[(0, 1, 2), (3, 4, 5)], [(0, 1, 5), (2, 3, 4)], [(0, 4, 5), (1, 2, 3)]]
CHU5 = [[(3, 4), (0, 1, 2)], [(4, 0), (1, 2, 3)], [(0, 1), (2, 3, 4)], [(1, 2), (3, 4, 0)], [(2, 3), (4, 0, 1)]]
LADDER = [  # (標題, 例子的分法（一列）, 公式, 例子說明, 個數)
    ("卡塔蘭", [(6, [(0, 5), (1, 4), (2, 3)])], r"\frac{1}{2n+1}\binom{2n+1}{n}", "只用弦，3 條：", 5),
    ("Fuss–Catalan", [(6, [(0, 1, 2), (3, 4, 5)])], r"\frac{1}{(v-1)n+1}\binom{vn}{n}", "只用三角形，2 個：", 3),
    ("Chu 的 C(n)", [(5, [(0, 1), (2, 3, 4)])], r"\frac{1}{N+1}\binom{N+1}{\vec n}", "一條弦＋一個三角形：", 5),
    ("Chu 的 A_t(n)", [(2, [(0, 1)]), (3, [(0, 1, 2)])], r"\frac{t}{N+t}\binom{N+t}{\vec n}", "同上，t = 2：", 12),
]


def check_math():
    tw = [partition_to_word(b, 6) for b in TRIS]
    assert sorted(tw) == lists_with(1, (0, 0, 2)) and comb(6, 2) // 5 == 3
    lists2 = lists_with(2, (0, 1, 1))
    assert len(lists2) == 12 == L_formula(2, (0, 1, 1)) == raney_A(2, (1, 1), (2, 3))
    kinds = [tuple(len(w) for w in split_words(s)) for s in lists2]
    assert kinds.count((1, 6)) == 5 and kinds.count((6, 1)) == 5 and kinds.count((3, 4)) == 1 and kinds.count((4, 3)) == 1
    assert factorial(7) // (factorial(5)) == 42 and 2 * 42 // 7 == 12
    assert [L_brute(1, (0, 3)), L_brute(1, (0, 0, 2)), L_brute(1, (0, 1, 1)), L_brute(2, (0, 1, 1))] == [x[-1] for x in LADDER]
    assert catalan(3) == 5


def mini_row(parts, radius=0.42):
    """一列小分法（t 個），每個下面寫它的字；沒有點的分法畫成「∅」。"""
    cells = VGroup()
    for n_pts, blocks in parts:
        if n_pts == 0:
            c = Tex(r"\varnothing", font_size=36)
            w = word_tiles((0,), size=0.26, font_size=16)
        else:
            c = make_configuration(n_pts, blocks, radius=radius, root=0)
            w = word_tiles(partition_to_word(blocks, n_pts), size=0.26, font_size=16, buff=0.02)
        w.next_to(c, DOWN, buff=0.18)
        cells.add(VGroup(c, w))
    return cells.arrange(RIGHT, buff=0.35, aligned_edge=UP)


class SceneN15Ladder(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N15　推廣的階梯：從卡塔蘭到 Chu")

        # 1. Fuss–Catalan
        self.say("第一步推廣：不用弦，只用三角形（3 點群組）")
        cf = VGroup(*[make_configuration(6, b, radius=0.95, root=0) for b in TRIS]).arrange(RIGHT, buff=1.4).move_to(1.4 * UP)
        wt = VGroup(*[word_tiles(partition_to_word(b, 6), size=0.36, font_size=22, buff=0.03).next_to(c, DOWN, buff=0.35)
                      for b, c in zip(TRIS, cf)])
        f1 = VGroup(
            mixed("只有 3 和 0 的字：", "$n$", " 個 3、", "$2n+1$", " 個 0（每個 3 讓需求 ", "$+2$", "）", font_size=28),
            mixed("$n=2$", "：", "$\\dfrac{1}{5}\\dbinom{6}{2}=3$", "；一般 ", "$v$", "：", "$\\dfrac{1}{(v-1)n+1}\\dbinom{vn}{n}$",
                  "（Fuss–Catalan 數）", font_size=28),
        ).arrange(DOWN, buff=0.3).move_to(1.7 * DOWN)
        assert_in_frame(cf, wt, f1)
        self.play(LaggedStartMap(FadeIn, cf, lag_ratio=0.25), run_time=1.8)
        self.play(LaggedStartMap(FadeIn, wt, lag_ratio=0.25), run_time=1.5)
        self.say("6 個點分成 2 個不交叉的三角形：3 種 ", "$\\leftrightarrow$", " 3 個只有 3 和 0 的字")
        self.wait(2)
        self.play(FadeIn(f1[0]))
        self.wait(2)
        self.play(FadeIn(f1[1]))
        self.wait(3)
        self.play(FadeOut(VGroup(cf, wt, f1)))

        # 2. 第二步：多種元數（N14 的回顧）
        self.say("第二步：弦和三角形一起用，就是 N14 的 Chu 公式 ", "$C_{\\vec v}(\\vec n)$")
        c5 = VGroup(*[make_configuration(5, b, radius=0.6, root=0) for b in CHU5]).arrange(RIGHT, buff=0.6).move_to(0.6 * UP)
        self.play(LaggedStartMap(FadeIn, c5, lag_ratio=0.15), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(c5))

        # 3. 第三步：t
        self.say("第三步：不只一個分法，而是 ", "$t$", " 個分法排成一列")
        head = VGroup(
            mixed("Chu：", "$A_t(\\vec n)=$", " ", "$C^t$", " 的係數 ", "$=$", " ", "$t$", " 個分法排成一列，群組總數是 ", "$\\vec n$", font_size=28),
            mixed("Raney：", "$t$", " 個字接起來（", "$t$", " 字列）", "$=$", " ", "$t$", " 棵樹的森林", font_size=28),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(2.35 * UP)
        assert_in_frame(head)
        self.play(FadeIn(head[0]))
        self.wait(2)
        self.play(FadeIn(head[1]))
        self.wait(2)
        empty = VGroup(Tex(r"\varnothing", font_size=44), mixed("（沒有點的分法）", "$\\leftrightarrow$", " 字 ", "$0$", "（一片樹葉）", font_size=26))
        empty.arrange(RIGHT, buff=0.3).move_to(1.15 * UP)
        assert_in_frame(empty)
        self.say("注意：「沒有點」也算一種分法，它對應最短的字 0")
        self.play(FadeIn(empty))
        self.wait(2.5)
        self.play(FadeOut(empty))

        # 12 = 5 + 5 + 1 + 1
        self.say("例：一條弦＋一個三角形分給 2 個位置（", "$t=2$", "），有幾種？")
        groups = VGroup(
            VGroup(mini_row([(0, []), (5, [(0, 1), (2, 3, 4)])], radius=0.4), mixed("$\\varnothing$", " 在前：5 種", font_size=24)),
            VGroup(mini_row([(5, [(0, 1), (2, 3, 4)]), (0, [])], radius=0.4), mixed("$\\varnothing$", " 在後：5 種", font_size=24)),
            VGroup(mini_row([(2, [(0, 1)]), (3, [(0, 1, 2)])], radius=0.4), zh("弦｜三角形：1 種", font_size=24)),
            VGroup(mini_row([(3, [(0, 1, 2)]), (2, [(0, 1)])], radius=0.4), zh("三角形｜弦：1 種", font_size=24)),
        )
        for g in groups:
            g[1].next_to(g[0], DOWN, buff=0.3)
        groups.arrange(RIGHT, buff=0.75, aligned_edge=UP).move_to(0.0 * UP)
        tot = VGroup(
            mixed("$5+5+1+1=12$", font_size=34),
            mixed("公式：", "$\\dfrac{t}{N+t}\\dbinom{N+t}{\\vec n}=\\dfrac{2}{7}\\cdot\\dfrac{7!}{1!\\,1!\\,5!}=\\dfrac{2}{7}\\cdot 42=12$", font_size=30),
        ).arrange(DOWN, buff=0.25).move_to(2.15 * DOWN)
        assert_in_frame(groups, tot)
        assert_apart(head, groups)
        for g in groups:
            self.play(FadeIn(g, lag_ratio=0.1), run_time=1.0)
            self.wait(0.8)
        self.say("每一列的字接起來就是一個 2 字列，例如 ", "$0\\,|\\,203000$", "、", "$200\\,|\\,3000$")
        self.wait(3)
        self.play(FadeIn(tot[0]))
        self.wait(1.5)
        self.say("數出來的 12 和公式一樣；把分成兩段的方式加起來，就是 Raney 公式 ", "$A_{s+t}=\\sum A_sA_t$")
        self.play(FadeIn(tot[1]))
        self.wait(4)
        self.play(FadeOut(VGroup(head, groups, tot)))

        # 4. 階梯總表
        self.say("把這幾步排成一個階梯")
        rows = VGroup()
        for title, parts, formula, ex, count in LADDER:
            t = zh(title, font_size=26) if "_" not in title else mixed("Chu 的 ", "$A_t(\\vec n)$", font_size=26)
            if title == "Chu 的 C(n)":
                t = mixed("Chu 的 ", "$C_{\\vec v}(\\vec n)$", font_size=26)
            pic = mini_row(parts, radius=0.32)
            fm = Tex(formula, font_size=30)
            e = mixed(ex, "$%d$" % count, font_size=24)
            rows.add(VGroup(t, pic, fm, e))
        xs = (-5.3, -2.4, 0.9, 4.4)
        for r in rows:
            for part, x in zip(r, xs):
                part.set_x(x)
        ys = (1.95, 0.55, -0.85, -2.25)
        for r, y in zip(rows, ys):
            for part in r:
                part.set_y(y)
        heads = VGroup(*[zh(s, font_size=24, color=GREY_B) for s in ("推廣", "Chu 的圖＋Raney 的字", "個數", "例子")])
        for h, x in zip(heads, xs):
            h.move_to(np.array([x, 2.95, 0]))
        assert_in_frame(rows, heads)
        self.play(FadeIn(heads))
        for r, cap in zip(rows, ["只用弦：只有 2 和 0 的字（N13）", "只用一種 v 點群組：只有 v 和 0 的字",
                                 "多種群組：多種符號（N14）", "t 個分法排成一列：t 個字接成的字列"]):
            self.say(cap)
            self.play(FadeIn(r, lag_ratio=0.1), run_time=1.2)
            self.wait(2)
        big = boxed(mixed("四個公式都是 Raney 定理 2.2：", "$L(t;a)=\\frac{t}{m}\\,M$", "（", "$m=N+t$", "，", "$M$", " ＝ 全部排法）", font_size=26))
        big.move_to(2.38 * DOWN)
        rows.generate_target()
        rows.target.scale(0.88)
        rows.target.shift((3.1 - rows.target.get_top()[1]) * UP)
        self.play(FadeOut(heads), MoveToTarget(rows))
        assert_in_frame(big, rows)
        assert_apart(big, rows)
        self.say("每一格都是「全部排法 × ", "$t$", " ÷ 長度」：下一段用走路來看為什麼")
        self.play(FadeIn(big))
        self.wait(4)
        self.play(FadeOut(VGroup(rows, big)))
        self.clear_caption()
