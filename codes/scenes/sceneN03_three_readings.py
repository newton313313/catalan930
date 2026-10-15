"""
Scene N03 —— 三種讀法：Raney、Chu 講義、Gessel（Raney 導讀第 2.3、4.5、12.3 節）
執行（在 codes/ 內）：manimgl scenes/sceneN03_three_readings.py SceneN03ThreeReadings

1. 2 字列 3000200：Raney 的秩路徑（由左往右、符號 j 走 j−1）停在 −2 之上，最後一步才碰到。
2. 倒過來讀、符號 j 走 1−j：Chu 講義第 7 節的好路徑（出發後 > 0，終點高度 2）。理由：高度 = −(後綴的秩)。
3. 對應的森林（兩棵樹）。
4. Gessel 的後序碼：森林 [2(0,0), 1(0)] 的前序碼 20010、後序碼 00201（先寫子樹、最後寫根）；
   reduced code 的部分和 −1,−2,−1,−2,−2 全 < 0；後序碼 ≠ 前序碼倒過來（01002），差一個左右鏡射。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import chu_heights, gessel_suffix_code, head_ranks, is_list, prefix_code, split_words
from utils.raney_draw import WordTreeMob, chu_walk, forest_mob, level_line, rank_walk, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

L2 = (3, 0, 0, 0, 2, 0, 0)
G_FOREST = [(2, ((0, ()), (0, ()))), (1, ((0, ()),))]


def check_math():
    assert is_list(L2, 2) and head_ranks(L2) == [0, 2, 1, 0, -1, 0, -1, -2]
    assert chu_heights(L2) == [0, 1, 2, 1, 2, 3, 4, 2] and min(chu_heights(L2)[1:]) > 0
    assert prefix_code(G_FOREST) == (2, 0, 0, 1, 0) and gessel_suffix_code(G_FOREST) == (0, 0, 2, 0, 1)
    assert head_ranks((0, 0, 2, 0, 1))[1:] == [-1, -2, -1, -2, -2]


class SceneN03ThreeReadings(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N03　三種讀法：Raney、Chu 講義、Gessel")

        tiles = word_tiles(L2, size=0.55, font_size=30).move_to(2.5 * UP)
        self.say("同一個 2 字列 ", "$3000200$", "，三種畫法")
        self.play(FadeIn(tiles))

        # 1. Raney 的秩路徑
        rw = rank_walk(L2, unit=0.36, origin=np.array([-5.6, 0.4, 0]))
        r0, r2 = level_line(rw, 0, 0, 7), level_line(rw, -2, 0, 7, color=MAROON_B)
        rlab = VGroup(zh("Raney：由左往右讀", font_size=24), mixed("符號 ", "$j$", " 走 ", "$j-1$", font_size=24)).arrange(DOWN, buff=0.12)
        rlab.next_to(VGroup(rw, r2), DOWN, buff=0.35)
        # 2. Chu 講義的路徑
        cw = chu_walk(L2, unit=0.36, origin=np.array([-1.25, -0.6, 0]))
        c0 = level_line(cw, 0, 0, 7, color=MAROON_B)
        clab = VGroup(zh("Chu 講義：倒過來讀", font_size=24), mixed("符號 ", "$j$", " 走 ", "$1-j$", font_size=24)).arrange(DOWN, buff=0.12)
        clab.next_to(VGroup(cw, c0), DOWN, buff=0.35).align_to(rlab, DOWN)
        # 3. 森林
        forest = forest_mob(split_words(L2), gap=0.8, x_gap=0.45, y_gap=0.6).move_to(np.array([4.4, 0.6, 0]))
        flab = zh("森林（2 棵樹）", font_size=24).next_to(forest, DOWN, buff=0.4).align_to(rlab, DOWN)
        assert_in_frame(rw, rlab, cw, clab, forest, flab)
        assert_apart(VGroup(rw, rlab), VGroup(cw, clab))
        assert_apart(VGroup(cw, clab), VGroup(forest, flab))

        self.play(FadeIn(VGroup(r0, r2, rw.dots[0])))
        self.play(ShowCreation(rw.steps, lag_ratio=1), FadeIn(rw.dots), run_time=2.2)
        self.play(FadeIn(rlab))
        self.say("Raney 的秩路徑停在 ", "$-2$", " 之上，最後一步才碰到")
        self.wait(2)
        rev = tiles.copy()
        self.play(rev.animate.arrange(RIGHT, buff=0.06).move_to(2.5 * UP), run_time=0.01)
        self.play(*[t.animate.move_to(tiles[len(L2) - 1 - k].get_center()) for k, t in enumerate(rev)],
                  tiles.animate.set_opacity(0.25), run_time=1.5)
        self.say("倒過來讀，符號 ", "$j$", " 換成 ", "$1-j$", "：就是 Chu 講義第 7 節的路徑")
        self.play(FadeIn(VGroup(c0, cw.dots[0])))
        self.play(ShowCreation(cw.steps, lag_ratio=1), FadeIn(cw.dots), run_time=2.2)
        self.play(FadeIn(clab))
        self.say("出發後一直 ", "$>0$", "、終點高度 2：終點高度 ", "$t=2$", " 的好路徑")
        self.wait(2)
        self.play(FadeIn(forest), FadeIn(flab))
        self.wait(1.5)

        why = VGroup(
            mixed("倒過來讀過的是一段後綴 ", "$\\tau$", "，高度 ", "$=-r(\\tau)$", font_size=26),
            mixed("$\\sigma=\\rho\\tau$", "：", "$r(\\rho)>-n\\ \\Leftrightarrow\\ r(\\tau)<0\\ \\Leftrightarrow$", " 高度 ", "$>0$", font_size=26),
        ).arrange(DOWN, buff=0.2).move_to(np.array([0, -2.35, 0]))
        assert_in_frame(why)
        self.say("為什麼兩種條件一樣？")
        self.play(FadeOut(VGroup(rlab, clab, flab)), FadeIn(why))
        self.wait(3.5)
        self.play(FadeOut(VGroup(tiles, rev, rw, r0, r2, cw, c0, forest, why)))

        # 4. Gessel 的後序碼
        trees = VGroup(*[WordTreeMob(w, x_gap=0.5, y_gap=0.65) for w in [(2, 0, 0), (1, 0)]]).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        trees.move_to(np.array([-4.6, 0.8, 0]))
        rows = VGroup(
            VGroup(zh("Raney 的前序碼（先根）", font_size=24), word_tiles((2, 0, 0, 1, 0), size=0.42, font_size=24)),
            VGroup(zh("Gessel 的後序碼（先子樹、最後根）", font_size=24), word_tiles((0, 0, 2, 0, 1), size=0.42, font_size=24)),
            VGroup(zh("後序碼每項減 1 的部分和", font_size=24), Tex(r"-1,\ -2,\ -1,\ -2,\ -2", font_size=30)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.35)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(np.array([1.9, 0.9, 0]))
        note = VGroup(
            mixed("部分和都 ", "$<0$", "、總和 ", "$-2$", "：Gessel 的「", "$k$", "-森林」判別法（引理 4.5.1）", font_size=26),
            mixed("後序碼 ", "$00201\\neq$", " 前序碼倒過來 ", "$01002$", "：差一個左右鏡射", font_size=26),
        ).arrange(DOWN, buff=0.22).move_to(np.array([0, -1.7, 0]))
        assert_in_frame(trees, rows, note)
        assert_apart(trees, rows)
        self.say("Gessel (2016) 用後序碼：先寫子樹，最後寫根的小孩數")
        self.play(FadeIn(trees))
        for r in rows:
            self.play(FadeIn(r, shift=0.2 * RIGHT), run_time=0.9)
            self.wait(0.6)
        self.play(FadeIn(note[0]))
        self.wait(1.5)
        self.say("三種編碼是同一個一一對應的不同寫法，計數完全相同")
        self.play(FadeIn(note[1]))
        self.wait(3)
