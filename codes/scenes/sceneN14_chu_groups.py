"""
Scene N14 —— 符號 v ＝ v 點群組：Chu 的圓周圖就是字（Raney 導讀第 2.4 小節）
執行（在 codes/ 內）：manimgl scenes/sceneN14_chu_groups.py SceneN14ChuGroups

1. Chu 講義的物件：圓周上 N 個點分成互不交叉的群組（弦 = 2 點、三角形 = 3 點）。
2. 讀成字（固定一個點，Chu 講義第 4 節）：固定點所在的 v 點群組寫 v；它把其餘的點切成 v 段，
   每段用同一個規則寫下去，沒有點的段寫 0。例：5 點、弦 {1,2}、三角形 {3,4,5} → 2 0 3 0 0 0。
3. 長度 N+1、0 的個數 1 + Σ(v−1)；5 種分法 ↔ 5 個字；1/(N+1)·(N+1)!/(1!1!4!) = 30/6 = 5。
4. 只用弦：6 點 3 條弦的 5 種配對 ↔ N13 的 5 個字（卡塔蘭）。
"""
import sys
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.circle_points import label_points
from utils.counting import catalan, raney_A
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.polygon_groups import circular_segment, make_configuration
from utils.raney import L_formula, a0_of, is_word, lists_with, partition_to_word
from utils.raney_draw import WordTreeMob, word_tiles
from utils.scene_base import ChuScene
from utils.styles import REGION_COLORS, block_color, boxed, mixed, zh

EX = [(0, 1), (2, 3, 4)]
EX_WORD = (2, 0, 3, 0, 0, 0)
CHU_FIG1 = [[(3, 4), (0, 1, 2)], [(4, 0), (1, 2, 3)], [(0, 1), (2, 3, 4)], [(1, 2), (3, 4, 0)], [(2, 3), (4, 0, 1)]]
MATCHINGS = [[(0, 5), (1, 4), (2, 3)], [(0, 5), (1, 2), (3, 4)], [(0, 3), (1, 2), (4, 5)],
             [(0, 1), (2, 5), (3, 4)], [(0, 1), (2, 3), (4, 5)]]


def check_math():
    assert partition_to_word(EX, 5) == EX_WORD and is_word(EX_WORD)
    words = [partition_to_word(b, 5) for b in CHU_FIG1]
    assert sorted(words) == lists_with(1, (0, 1, 1)) and len(set(words)) == 5
    assert len(EX_WORD) == 5 + 1 and a0_of(1, (0, 1, 1)) == 4 == 1 + (2 - 1) + (3 - 1)
    assert factorial(6) // (factorial(1) * factorial(1) * factorial(4)) == 30 and 30 // 6 == 5
    assert L_formula(1, (0, 1, 1)) == raney_A(1, (1, 1), (2, 3)) == 5
    mw = [partition_to_word(m, 6) for m in MATCHINGS]
    assert sorted(mw) == lists_with(1, (0, 3)) and len(mw) == catalan(3)


class SceneN14ChuGroups(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N14　符號 v ＝ v 點群組：Chu 的圓周圖")

        # 1. Chu 的物件
        R, C = 2.0, np.array([-3.6, 0.35, 0])
        cfg = make_configuration(5, EX, radius=R, center=C)
        labs = label_points(cfg.coords, C, buff=0.35, font_size=28)
        legend = VGroup(
            VGroup(Line(LEFT * 0.4, RIGHT * 0.4, stroke_color=block_color(2), stroke_width=6),
                   zh("弦 ＝ 2 點群組", font_size=26)).arrange(RIGHT, buff=0.25),
            VGroup(Triangle(stroke_color=block_color(3), fill_color=block_color(3), fill_opacity=0.3).set_height(0.45),
                   zh("三角形 ＝ 3 點群組", font_size=26)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(np.array([3.0, 1.8, 0]))
        assert_in_frame(cfg, labs, legend)
        self.say("Chu 講義數的東西：圓周上 ", "$N$", " 個點，分成互不交叉的群組")
        self.play(ShowCreation(cfg.circle), FadeIn(cfg.dots), FadeIn(labs))
        self.play(LaggedStartMap(ShowCreation, cfg.blocks, lag_ratio=0.5), run_time=1.5)
        self.play(FadeIn(legend))
        self.say("這裡 ", "$N=5$", "：一條弦 ", "$\\{1,2\\}$", "、一個三角形 ", "$\\{3,4,5\\}$")
        self.wait(2.5)

        # 2. 讀成字
        tiles = word_tiles(EX_WORD, size=0.62, font_size=36).move_to(np.array([3.0, 0.3, 0]))
        for t in tiles:
            t.set_opacity(0)
        rule = VGroup(
            zh("規則（固定點 1）：", font_size=26),
            zh("① 點 1 所在的群組有 v 個點 → 寫 v", font_size=26),
            zh("② 它把其餘的點切成 v 段，依順時針", font_size=26),
            zh("　 每段用同一個規則寫下去", font_size=26),
            zh("③ 沒有點的段 → 寫 0", font_size=26),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(np.array([3.0, -1.85, 0]))
        assert_in_frame(tiles, rule)
        self.play(FadeOut(legend), FadeIn(rule))
        self.say("把圖讀成一串數字：先固定點 1（橘色）")
        self.play(cfg.dots[0].animate.set_fill(ORANGE).scale(1.6))
        self.wait(1)

        def show_tile(k):
            tiles[k].set_opacity(1)
            tiles[k][0].set_fill(opacity=0.2)
            return FadeIn(tiles[k], scale=1.3)

        self.say("點 1 在一條弦裡，弦有 2 個點 → 寫 2")
        self.play(Indicate(cfg.blocks[0], scale_factor=1.1), show_tile(0))
        self.wait(1)
        regs = VGroup(circular_segment(0, 1, 5, R, C, color=REGION_COLORS[0], opacity=0.3),
                      circular_segment(1, 0, 5, R, C, color=REGION_COLORS[1], opacity=0.3))
        self.say("這條弦把圓切成 2 段：點 1 到點 2 之間（沒有點），點 2 到點 1 之間（點 3、4、5）")
        self.play(FadeIn(regs[0]))
        self.play(FadeIn(regs[1]))
        self.wait(1.5)
        self.say("第 1 段沒有點 → 寫 0")
        self.play(Indicate(regs[0]), show_tile(1))
        self.wait(1)
        self.say("第 2 段：它的第一個點是 3，3 在三角形裡，三角形有 3 個點 → 寫 3")
        self.play(Indicate(cfg.blocks[1], scale_factor=1.08), show_tile(2))
        self.wait(1)
        subs = VGroup(*[circular_segment(a, b, 5, R, C, color=YELLOW, opacity=0.35) for a, b in [(2, 3), (3, 4), (4, 0)]])
        self.say("三角形再切成 3 小段，都沒有點 → 寫 0、0、0")
        for k, s in enumerate(subs):
            self.play(FadeIn(s), show_tile(3 + k), run_time=0.7)
        self.play(FadeOut(subs))
        self.wait(1)
        self.say("得到字 ", "$203000$", "：Chu 的圖就是 Raney 的字")
        self.play(Indicate(tiles, scale_factor=1.08))
        self.wait(2)

        # 樹
        tree = WordTreeMob(EX_WORD, x_gap=0.6, y_gap=0.7).move_to(np.array([3.0, -1.05, 0]))
        tlab = zh("字也是一棵樹：根 ＝ 點 1 所在的群組", font_size=26).next_to(tree, DOWN, buff=0.35)
        assert_in_frame(tree, tlab)
        self.play(FadeOut(rule), FadeIn(tree), FadeIn(tlab))
        self.wait(2.5)
        cnt = VGroup(
            mixed("字長 ", "$=N+1=6$", font_size=28),
            mixed("0 的個數 ", "$=1+(2-1)+(3-1)=4$", font_size=28),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(np.array([3.0, -1.5, 0]))
        assert_in_frame(cnt)
        self.say("每個點對應一個非 0 的位置，再多一個 0；0 的個數 ", "$=1+\\sum(v-1)$", "（同 N13 的計數器）")
        self.play(FadeOut(VGroup(tree, tlab)), FadeIn(cnt))
        self.wait(3.5)
        self.play(FadeOut(VGroup(cfg, labs, regs, tiles, cnt)))

        # 3. 全部 5 種
        cfgs = VGroup(*[make_configuration(5, b, radius=0.75, root=0) for b in CHU_FIG1]).arrange(RIGHT, buff=0.75)
        cfgs.move_to(1.5 * UP)
        wts = VGroup(*[word_tiles(partition_to_word(b, 5), size=0.32, font_size=20, buff=0.03).next_to(c, DOWN, buff=0.35)
                       for b, c in zip(CHU_FIG1, cfgs)])
        assert_in_frame(cfgs, wts)
        self.say("5 個點分成一條弦和一個三角形，一共 5 種（Chu 原文 Fig. 1）")
        self.play(LaggedStartMap(FadeIn, cfgs, lag_ratio=0.2), run_time=2)
        self.say("每一種讀成一個字：5 種分法 ", "$\\leftrightarrow$", " 5 個字（一個 2、一個 3、四個 0）")
        self.play(LaggedStartMap(FadeIn, wts, lag_ratio=0.2), run_time=2)
        self.wait(2)
        calc = VGroup(
            mixed("2、3、0、0、0、0 的排法：", "$\\dfrac{6!}{1!\\,1!\\,4!}=30$", font_size=27),
            mixed("轉一圈的 6 種讀法中恰有 1 種是字：", "$30/6=5$", font_size=27),
            boxed(mixed("Chu：", "$C_{\\vec v}(\\vec n)=\\dfrac{1}{N+1}\\dbinom{N+1}{\\vec n}$", font_size=27)),
        ).arrange(DOWN, buff=0.2).move_to(1.55 * DOWN)
        assert_apart(calc, wts)
        assert_in_frame(calc)
        self.say("個數怎麼算？和 N13 一樣：先隨便排，再除以轉一圈的讀法數")
        self.play(FadeIn(calc[0]))
        self.wait(1.5)
        self.play(FadeIn(calc[1]))
        self.wait(2)
        self.say("一般的情形就是 Chu 的公式（", "$N=\\sum n_iv_i$", "）")
        self.play(FadeIn(calc[2]))
        self.wait(3)
        self.play(FadeOut(VGroup(cfgs, wts, calc)))

        # 4. 只用弦 = 卡塔蘭
        mcf = VGroup(*[make_configuration(6, m, radius=0.75, root=0) for m in MATCHINGS]).arrange(RIGHT, buff=0.75)
        mcf.move_to(1.2 * UP)
        mwt = VGroup(*[word_tiles(partition_to_word(m, 6), size=0.3, font_size=19, buff=0.03).next_to(c, DOWN, buff=0.35)
                       for m, c in zip(MATCHINGS, mcf)])
        note = mixed("只用弦（", "$v=2$", "）：6 個點配成 3 對，不交叉的配對 ", "$C_3=5$", " 種", font_size=30).move_to(1.6 * DOWN)
        assert_in_frame(mcf, mwt, note)
        self.say("如果只用弦呢？")
        self.play(LaggedStartMap(FadeIn, mcf, lag_ratio=0.2), run_time=2)
        self.play(LaggedStartMap(FadeIn, mwt, lag_ratio=0.2), run_time=2)
        self.say("讀出來正好是 N13 那 5 個只有 2 和 0 的字：卡塔蘭數")
        self.play(FadeIn(note))
        self.wait(3.5)
        self.play(FadeOut(VGroup(mcf, mwt, note)))
        self.clear_caption()
