"""
Scene N05 —— 定理 2.2：mL = nM（Raney 導讀第 6.1 節；原文 pp. 443–444）
執行（在 codes/ 內）：manimgl scenes/sceneN05_double_counting.py SceneN05DoubleCounting

1. 組成 (1; 0,1,1)：4 個 0、一個 2、一個 3，排法 M = 6!/(4!1!1!) = 30。
   30 個字串依「循環類」排成 5 列 × 6 欄：每列是同一個字的 6 種輪換，每列恰有 1 個是字 → 30 = 6 × 5。
2. 定理 2.2：m·L(n; a) = n·M(a₀, a₁, …)；Chu 講義的寫法 A_t(n⃗) = t/(N+t)·C(N+t; n⃗)。
3. Chu 原文 Fig. 1 的 5 種分法 ↔ 5 個字（固定點 1 所在的群組當根，依序寫出它切出的各段）：
   弦 {1,2}、三角形 {3,4,5} → 2 | 0 | 3000 = 203000。所以 Chu 的定理直接由定理 2.2 得到。
4. Cayley：L(1; 0, k) = C(2k+1, k)/(2k+1) = C_k：1, 1, 2, 5, 14, 42。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan, raney_A
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.polygon_groups import make_configuration
from utils.raney import L_formula, cyclic_variant, is_word, lists_with, multinomial, partition_to_word, strings_with
from utils.raney_draw import WordTreeMob, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

A = (0, 1, 1)
WORDS = lists_with(1, A)
CHU_FIG1 = [((3, 4), (0, 1, 2)), ((4, 0), (1, 2, 3)), ((0, 1), (2, 3, 4)), ((1, 2), (3, 4, 0)), ((2, 3), (4, 0, 1))]


def check_math():
    assert multinomial(4, 0, 1, 1) == 30 == len(strings_with(1, A)) and L_formula(1, A) == 5 == len(WORDS)
    classes = {frozenset(cyclic_variant(w, k) for k in range(6)) for w in WORDS}
    assert len(classes) == 5 and all(len(c) == 6 for c in classes)
    assert set().union(*classes) == set(strings_with(1, A))
    words = [partition_to_word(b, 5) for b in CHU_FIG1]
    assert sorted(words) == WORDS and words[2] == (2, 0, 3, 0, 0, 0)
    assert raney_A(1, (1, 1), (2, 3)) == 5
    assert [L_formula(1, (0, k)) for k in range(6)] == [catalan(k) for k in range(6)] == [1, 1, 2, 5, 14, 42]


class SceneN05DoubleCounting(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N05　定理 2.2：雙重計數")

        # 1. 30 = 6 × 5
        self.say("組成 ", "$(1;0,1,1)$", "：四個 0、一個 2、一個 3，排成一列有 ", "$\\frac{6!}{4!\\,1!\\,1!}=30$", " 種")
        grid = VGroup()
        goods = VGroup()
        for r, w in enumerate(WORDS):
            row = VGroup()
            pos = [2, 5, 0, 3, 1][r]                 # 這一列的字放在第 pos 欄，各列不同
            for k in range(6):
                s = cyclic_variant(w, (pos - k) % 6)
                t = word_tiles(s, size=0.24, buff=0.02, font_size=16)
                row.add(t)
                if is_word(s):
                    goods.add(t)
            row.arrange(RIGHT, buff=0.42)
            grid.add(row)
        grid.arrange(DOWN, buff=0.32).move_to(0.6 * UP)
        assert_in_frame(grid)
        self.play(LaggedStartMap(FadeIn, VGroup(*[t for r in grid for t in r]), lag_ratio=0.03), run_time=3)
        self.wait(1)
        self.say("同一列是同一個字串的 6 種循環讀法")
        rects = VGroup(*[SurroundingRectangle(r, color=GREY_C, buff=0.08, stroke_width=1.5) for r in grid])
        self.play(ShowCreation(rects), run_time=1.2)
        self.wait(1)
        self.say("循環引理：每一列恰有 1 個是字")
        boxes = VGroup(*[SurroundingRectangle(g, color=YELLOW, buff=0.05) for g in goods])
        self.play(LaggedStartMap(ShowCreation, boxes, lag_ratio=0.2), run_time=1.5)
        eq = Tex(r"30=6\times5\quad\Rightarrow\quad L(1;0,1,1)=5", font_size=40).next_to(grid, DOWN, buff=0.45)
        assert_in_frame(eq)
        self.play(Write(eq))
        self.wait(2.5)
        self.play(FadeOut(VGroup(grid, rects, boxes, eq)))

        # 2. 定理
        thm = VGroup(zh("定理 2.2", font_size=32, color=YELLOW),
                     Tex(r"m\,L(n;a_1,a_2,\ldots)=n\,M(a_0,a_1,a_2,\ldots)", font_size=40),
                     mixed("$m$", " ＝ 字串長度、", "$M$", " ＝ 排法數；證明：數（輪換, 字串）的配對", font_size=26),
                     mixed("Chu 講義：", "$A_t(\\vec n)=\\frac{t}{N+t}\\binom{N+t}{\\vec n}$", "（", "$t=n$", "、", "$a_{v_i}=n_i$", "）", font_size=28),
                     ).arrange(DOWN, buff=0.3)
        box = boxed(thm, color=YELLOW).move_to(0.6 * UP)
        assert_in_frame(box)
        self.say("一般情形：每個字串恰有 ", "$n$", " 種好讀法，每個字列被 ", "$m$", " 個字串讀到")
        self.play(FadeIn(box, shift=0.2 * UP), run_time=1.2)
        self.wait(3.5)
        self.play(FadeOut(box))

        # 3. Chu 原文 Fig. 1
        cfgs = VGroup()
        for chord, tri in CHU_FIG1:
            cfgs.add(make_configuration(5, [chord, tri], radius=0.75, root=0))
        cfgs.arrange(RIGHT, buff=0.75).move_to(1.6 * UP)
        words = [partition_to_word(b, 5) for b in CHU_FIG1]
        wt = VGroup(*[word_tiles(w, size=0.3, font_size=20, buff=0.03).next_to(c, DOWN, buff=0.3) for w, c in zip(words, cfgs)])
        trees = VGroup(*[WordTreeMob(w, x_gap=0.28, y_gap=0.36).next_to(t, DOWN, buff=0.3) for w, t in zip(words, wt)])
        assert_in_frame(cfgs, wt, trees)
        self.say("Chu 原文 Fig. 1：5 個點分成一條弦和一個三角形，共 5 種")
        self.play(LaggedStartMap(FadeIn, cfgs, lag_ratio=0.2), run_time=2)
        self.wait(1)
        self.say("對應：點 1（橘）所在的群組當根，依序寫出它切出的各段，空段寫 0")
        c3 = cfgs[2]
        self.play(c3.blocks[0].animate.set_stroke(width=9), run_time=0.6)
        self.play(FadeIn(wt[2][0]), run_time=0.5)
        self.play(FadeIn(wt[2][1]), run_time=0.5)
        self.play(c3.blocks[1].animate.set_stroke(width=8), FadeIn(wt[2][2:]), run_time=0.9)
        expl = mixed("弦 ", "$\\{1,2\\}$", " → 根 2；1、2 之間空 → 0；", "$\\{3,4,5\\}$", " 是三角形 → 3000", font_size=26)
        expl.move_to(np.array([0, -2.45, 0]))
        assert_in_frame(expl)
        self.play(FadeIn(expl), FadeIn(trees[2]))
        self.wait(2)
        self.play(*[FadeIn(wt[k]) for k in (0, 1, 3, 4)], *[FadeIn(trees[k]) for k in (0, 1, 3, 4)], run_time=1.5)
        self.say("5 種分法 ", "$\\leftrightarrow$", " 組成 ", "$(1;0,1,1)$", " 的 5 個字：Chu 的定理直接由定理 2.2 得到")
        self.wait(3)
        self.play(FadeOut(VGroup(cfgs, wt, trees, expl)))

        # 4. Cayley
        cay = VGroup(zh("Cayley 的問題：只有二元符號（", font_size=30),
                     Tex(r"a_2=k", font_size=36), zh("）", font_size=30)).arrange(RIGHT, buff=0.1)
        f = Tex(r"L(1;0,k)=\frac{1}{2k+1}\binom{2k+1}{k}=\frac{1}{k+1}\binom{2k}{k}=C_k", font_size=42)
        vals = Tex(r"1,\ 1,\ 2,\ 5,\ 14,\ 42,\ \ldots", font_size=40)
        VGroup(cay, f, vals).arrange(DOWN, buff=0.45).move_to(0.5 * UP)
        assert_in_frame(cay, f, vals)
        self.say("原文第 444 頁：Raney 寫成 ", "$(k+1)^{-1}C_{2k,k}$", "，這裡的 ", "$C_{2k,k}$", " 是二項式係數")
        self.play(FadeIn(cay))
        self.play(Write(f), run_time=1.5)
        self.play(FadeIn(vals))
        self.wait(3)
