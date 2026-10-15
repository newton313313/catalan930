"""
Scene N07 —— 定理 2.3（切成兩段）與定理 2.4（看第一個符號）（Raney 導讀第 6.2–6.3 節；原文 p. 444）
執行（在 codes/ 內）：manimgl scenes/sceneN07_split_first.py SceneN07SplitFirst

1. 定理 2.3：2 字列 2003000 唯一的「1 字列開頭」是 200（秩路徑第一次到 −1 的地方）。
2. 組成 (2; 0,1,1) 的 12 個 2 字列依「第一個字的組成 b」分堆：5 + 1 + 1 + 5 = 12 = Chu 講義的 A₂(1,1)。
3. 定理 2.4：同樣 12 個依第一個符號分堆：0 開頭 5、2 開頭 3、3 開頭 4。
4. k = 0：L(1;0,1,1) = 0 + L(2;0,0,1) + L(3;0,1,0) = 2 + 3 = 5（Chu 講義第 6 節的收尾、場景 06 的 2 + 3 = 5）。
5. 生成函數：F_{m+n} = F_m F_n、F_1 = 1 + Σ x_i F_1^i（Chu 原文式 (6)）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import raney_A
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import L_formula, head_ranks, lists_with, split_head, split_words
from utils.raney_draw import forest_mob, level_line, rank_walk, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

EX = (2, 0, 0, 3, 0, 0, 0)
LISTS = lists_with(2, (0, 1, 1))
WORDS = lists_with(1, (0, 1, 1))


def first_word_comp(s):
    w = split_words(s)[0]
    return (sum(1 for x in w if x == 2), sum(1 for x in w if x == 3))


def check_math():
    assert split_head(EX, 1) == ((2, 0, 0), (3, 0, 0, 0)) and head_ranks(EX)[3] == -1
    assert len(LISTS) == 12 == raney_A(2, (1, 1), (2, 3))
    by_b = {}
    for s in LISTS:
        by_b.setdefault(first_word_comp(s), []).append(s)
    assert [len(by_b[b]) for b in [(0, 0), (1, 0), (0, 1), (1, 1)]] == [5, 1, 1, 5]
    by_first = {}
    for s in LISTS:
        by_first.setdefault(s[0], []).append(s)
    assert [len(by_first[x]) for x in (0, 2, 3)] == [5, 3, 4]
    assert [L_formula(1, (0, 1, 1)), L_formula(3, (0, 0, 1)), L_formula(4, (0, 1, 0))] == [5, 3, 4]
    assert [sum(1 for w in WORDS if w[0] == x) for x in (2, 3)] == [2, 3]
    assert [L_formula(2, (0, 0, 1)), L_formula(3, (0, 1, 0))] == [2, 3]


def group_box(items, title, count, width=2.9):
    tiles = VGroup(*[word_tiles(s, size=0.22, font_size=14, buff=0.02) for s in items]).arrange(DOWN, buff=0.1)
    head = VGroup(title, Tex(r"\times %d" % count, font_size=30, fill_color=YELLOW)).arrange(RIGHT, buff=0.2)
    g = VGroup(head, tiles).arrange(DOWN, buff=0.22)
    frame = RoundedRectangle(width=width, height=g.get_height() + 0.35, corner_radius=0.1, stroke_color=GREY_C, stroke_width=1.5)
    frame.move_to(g)
    return VGroup(frame, g)


class SceneN07SplitFirst(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N07　定理 2.3（切成兩段）與定理 2.4（看第一個符號）")

        # 1. 唯一的 1 字列開頭
        tiles = word_tiles(EX, size=0.55, font_size=30, sep_after=(2,)).move_to(np.array([-2.6, 2.3, 0]))
        tiles_plain = word_tiles(EX, size=0.55, font_size=30).move_to(tiles)
        walk = rank_walk(EX, unit=0.45, origin=np.array([-4.2, 0.5, 0]))
        z, f1, f2 = level_line(walk, 0, 0, 7), level_line(walk, -1, 0, 7, color=TEAL), level_line(walk, -2, 0, 7, color=MAROON_B)
        dot = Dot(walk.vertex(3), radius=0.09, fill_color=TEAL).set_z_index(3)
        forest = forest_mob(split_words(EX), gap=0.8, x_gap=0.45, y_gap=0.6).move_to(np.array([3.6, 0.6, 0]))
        thm = mixed("定理 2.3：", "$(m+n)$", " 字列恰有一個開頭是 ", "$m$", " 字列（前 ", "$m$", " 個字）", font_size=28)
        thm.move_to(np.array([0, -1.6, 0]))
        eqn = Tex(r"L(m+n;a)=\sum_{b+c=a}L(m;b)\,L(n;c)", font_size=36).next_to(thm, DOWN, buff=0.3)
        assert_in_frame(tiles, walk, forest, thm, eqn)
        assert_apart(walk, forest)
        self.say("2 字列 ", "$2003000$", "：秩路徑第一次碰到 ", "$-1$", " 的地方，就是第一個字的結尾")
        self.play(FadeIn(tiles_plain), FadeIn(VGroup(z, f1, f2)), ShowCreation(walk), run_time=2)
        self.play(FadeIn(dot, scale=1.5), Transform(tiles_plain, tiles), run_time=1)
        self.play(FadeIn(forest))
        self.play(FadeIn(thm), Write(eqn), run_time=1.5)
        self.say("這就是 Chu 引用的 Raney 公式 ", "$A_{s+t}=\\sum A_sA_t$")
        self.wait(3)
        self.play(FadeOut(VGroup(tiles_plain, walk, z, f1, f2, dot, forest, thm, eqn)))

        # 2. 依第一個字的組成分堆
        by_b = {}
        for s in LISTS:
            by_b.setdefault(first_word_comp(s), []).append(s)
        titles = [mixed("$b$", "：只有引數", font_size=20), mixed("$b$", "：一個 2", font_size=20),
                  mixed("$b$", "：一個 3", font_size=20), mixed("$b$", "：2 和 3", font_size=20)]
        groups = VGroup(*[group_box(by_b[b], t, len(by_b[b])) for b, t in zip([(0, 0), (1, 0), (0, 1), (1, 1)], titles)])
        groups.arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(np.array([0, 0.9, 0]))
        tot = Tex(r"5+1+1+5=12=L(2;0,1,1)=A_2(1,1)", font_size=36).next_to(groups, DOWN, buff=0.4)
        assert_in_frame(groups, tot)
        self.say("組成 ", "$(2;0,1,1)$", " 的 12 個 2 字列，依「第一個字用掉什麼」分堆")
        self.play(LaggedStartMap(FadeIn, groups, lag_ratio=0.3), run_time=2.5)
        self.play(Write(tot))
        self.say("每一堆 ", "$=L(1;b)\\cdot L(1;a-b)$", "：", "$1\\cdot5,\\ 1\\cdot1,\\ 1\\cdot1,\\ 5\\cdot1$")
        self.wait(3)
        self.play(FadeOut(VGroup(groups, tot)))

        # 3. 依第一個符號分堆
        by_first = {}
        for s in LISTS:
            by_first.setdefault(s[0], []).append(s)
        t2 = [mixed("0 開頭", font_size=20), mixed("2 開頭", font_size=20), mixed("3 開頭", font_size=20)]
        g2 = VGroup(*[group_box(by_first[x], t, len(by_first[x]), width=3.2) for x, t in zip((0, 2, 3), t2)])
        g2.arrange(RIGHT, buff=0.45, aligned_edge=UP).move_to(np.array([0, 1.0, 0]))
        e2 = Tex(r"L(2;0,1,1)=L(1;0,1,1)+L(3;0,0,1)+L(4;0,1,0)=5+3+4", font_size=34).next_to(g2, DOWN, buff=0.4)
        rule = mixed("定理 2.4：第一個是 0 ", "$\\Rightarrow$", " 剩下 ", "$k$", " 字列；是 ", "$i$", " ", "$\\Rightarrow$",
                     " 剩下 ", "$k+i$", " 字列", font_size=26).next_to(e2, DOWN, buff=0.3)
        assert_in_frame(g2, e2, rule)
        self.say("同樣 12 個，改成看第一個符號")
        self.play(LaggedStartMap(FadeIn, g2, lag_ratio=0.3), run_time=2.2)
        self.play(Write(e2), run_time=1.5)
        self.play(FadeIn(rule))
        self.wait(3)
        self.play(FadeOut(VGroup(g2, e2, rule)))

        # 4. k = 0：Chu 的收尾
        b2 = [w for w in WORDS if w[0] == 2]
        b3 = [w for w in WORDS if w[0] == 3]
        g3 = VGroup(group_box(b2, mixed("2 開頭", font_size=20), 2, width=2.6),
                    group_box(b3, mixed("3 開頭", font_size=20), 3, width=2.6)).arrange(RIGHT, buff=0.6, aligned_edge=UP)
        g3.move_to(np.array([-3.0, 0.5, 0]))
        lines = VGroup(
            Tex(r"L(1;0,1,1)=L(2;0,0,1)+L(3;0,1,0)", font_size=32),
            Tex(r"5=2+3", font_size=40),
            mixed("Chu 講義第 6 節：", "$\\frac{2}{5}\\cdot5+\\frac35\\cdot5=5$", font_size=26),
            zh("（manim 場景 06 的「驗算 2 + 3 = 5」）", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.28).move_to(np.array([3.0, 0.6, 0]))
        assert_in_frame(g3, lines)
        assert_apart(g3, lines)
        self.say("$k=0$", "：一個字的第一個符號就是樹根——這正是 Chu 證明的「收尾」")
        self.play(FadeIn(g3), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, lines, lag_ratio=0.4), run_time=2.5)
        self.wait(2.5)
        self.play(FadeOut(VGroup(g3, lines)))

        # 5. 生成函數
        gf = VGroup(
            mixed("令 ", "$F_n=\\sum_a L(n;a)\\,x^a$", "（", "$n$", " 字列的生成函數）", font_size=30),
            mixed("定理 2.3：", "$F_{m+n}=F_mF_n\\ \\Rightarrow\\ F_n=F_1^{\\,n}$", font_size=30),
            mixed("定理 2.4（", "$k=0$", "）：", "$F_1=1+\\sum_i x_iF_1^{\\,i}$", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        box = boxed(gf, color=YELLOW).move_to(0.5 * UP)
        note = mixed("最後一行就是 Chu 原文式 (6)：", "$D=1+\\sum_i x_iD^{v_i}$", font_size=28, color=GREY_A).next_to(box, DOWN, buff=0.4)
        assert_in_frame(box, note)
        self.say("用生成函數看：Raney 第 4 節要說的就是這兩件事")
        self.play(FadeIn(box, shift=0.2 * UP), run_time=1.5)
        self.play(FadeIn(note))
        self.wait(3.5)
