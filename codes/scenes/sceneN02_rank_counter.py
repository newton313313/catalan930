"""
Scene N02 —— 秩與「還欠幾個引數」（Raney 導讀第 4.2–4.4 節；原文 p. 442）
執行（在 codes/ 內）：manimgl scenes/sceneN02_rank_counter.py SceneN02RankCounter

1. 讀 230200010：一開始欠 1 個引數；讀到 i 元符號變化 i − 1。計數器 1,2,4,3,4,3,2,1,1,0 = 開頭的秩 + 1，同步畫秩路徑。
2. Rosenbloom 判別法：r = −1，而且每個真開頭的秩 ≥ 0。
3. 020：讀完第一個 0 就欠 0 個了，後面的 20 多出來，不是字；它的循環變形 200 才是字。
4. 字列：3000200 一開始欠 2 個，欠到 1 時第一個字結束：3000 | 200；判別法 r = −n、真開頭 > −n。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import head_ranks, is_list, is_word, list_shifts, split_words
from utils.raney_draw import draws_badge, forest_mob, level_line, rank_walk, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

W = (2, 3, 0, 2, 0, 0, 0, 1, 0)
BAD = (0, 2, 0)
LIST2 = (3, 0, 0, 0, 2, 0, 0)


def check_math():
    assert [h + 1 for h in head_ranks(W)] == [1, 2, 4, 3, 4, 3, 2, 1, 1, 0] and is_word(W)
    assert head_ranks(BAD) == [0, -1, 0, -1] and not is_word(BAD) and list_shifts(BAD) == [1]
    assert [h + 2 for h in head_ranks(LIST2)] == [2, 4, 3, 2, 1, 2, 1, 0] and is_list(LIST2, 2)
    assert split_words(LIST2) == [(3, 0, 0, 0), (2, 0, 0)]


def read_word(scene, word, start, tiles, walk, badge, label, pointer_y):
    """逐個符號讀：箭頭移動、計數器更新、秩路徑長出一步。回傳最後的 badge。"""
    owe = start
    for j, x in enumerate(word):
        owe += x - 1
        nb = draws_badge(owe).move_to(badge)
        arrow = scene.pointer
        scene.play(arrow.animate.move_to(np.array([tiles[j].get_center()[0], pointer_y, 0])),
                   Transform(badge, nb), ShowCreation(walk.steps[j]), FadeIn(walk.dots[j + 1]), run_time=0.55)
    return badge


class SceneN02RankCounter(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N02　秩與「還欠幾個引數」")

        # 1. 讀 230200010
        tiles = word_tiles(W, size=0.6, font_size=32).move_to(np.array([-1.0, 2.2, 0]))
        lab = zh("還欠", font_size=26, color=GREY_A).move_to(np.array([3.6, 2.2, 0]))
        badge = draws_badge(1, radius=0.3, font_size=30).next_to(lab, RIGHT, buff=0.2)
        walk = rank_walk(W, unit=0.42, origin=np.array([-2.9, -0.2, 0]))
        zero = level_line(walk, 0, 0, len(W))
        floor = level_line(walk, -1, 0, len(W), color=MAROON_B)
        zl = Tex("0", font_size=24, fill_color=GREY_B).next_to(zero, LEFT, buff=0.15)
        fl = Tex("-1", font_size=24, fill_color=MAROON_B).next_to(floor, LEFT, buff=0.15)
        self.pointer = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)
        py = tiles.get_top()[1] + 0.25
        self.pointer.move_to(np.array([tiles[0].get_center()[0] - 0.8, py, 0]))
        rule = mixed("讀到 ", "$i$", " 元符號：填掉 1 個空位、開出 ", "$i$", " 個 ", "$\\Rightarrow$", " 變化 ", "$i-1$",
                     font_size=26).move_to(np.array([0, -1.35, 0]))
        assert_in_frame(tiles, lab, badge, walk, rule, fl)
        assert_apart(rule, walk)
        self.say("讀前序運算式時，記住「還要再讀幾個完整的引數，運算式才結束」")
        self.play(FadeIn(tiles), FadeIn(lab), FadeIn(badge), FadeIn(self.pointer))
        self.wait(1)
        self.play(FadeIn(VGroup(zero, floor, zl, fl, walk.dots[0])), FadeIn(rule))
        self.say("一開始欠 1 個（整個運算式）；下面同時畫「秩路徑」：每個符號走 ", "$i-1$")
        badge = read_word(self, W, 1, tiles, walk, badge, lab, py)
        self.say("欠的個數 ", "$=$", " 開頭的秩 ", "$+1$", "：欠到 0 的那一刻，運算式結束")
        self.wait(2.5)

        thm = VGroup(zh("Rosenbloom 判別法", font_size=30, color=YELLOW),
                     mixed("$\\gamma$", " 是字 ", "$\\Leftrightarrow$", " ", "$r(\\gamma)=-1$", "，而且每個真開頭的秩 ", "$\\ge 0$",
                           font_size=28)).arrange(DOWN, buff=0.25)
        box = boxed(thm, color=YELLOW).move_to(np.array([0, -2.2, 0]))
        assert_in_frame(box)
        self.play(FadeOut(rule), FadeIn(box, shift=0.2 * UP))
        self.say("秩路徑在 0 以上，到最後一步才第一次碰到 ", "$-1$")
        self.wait(3)
        self.play(FadeOut(VGroup(tiles, lab, badge, walk, zero, floor, zl, fl, box, self.pointer)))

        # 2. 020 不是字
        t2 = word_tiles(BAD, size=0.6, font_size=32).move_to(np.array([-2.6, 1.6, 0]))
        b2 = draws_badge(1, radius=0.3, font_size=30).next_to(t2, RIGHT, buff=0.7)
        w2 = rank_walk(BAD, unit=0.5, origin=np.array([-3.35, -0.2, 0]))
        z2, f2 = level_line(w2, 0, 0, 3), level_line(w2, -1, 0, 3, color=MAROON_B)
        self.pointer.move_to(np.array([t2[0].get_center()[0] - 0.8, t2.get_top()[1] + 0.25, 0]))
        extra = SurroundingRectangle(VGroup(t2[1], t2[2]), color=RED, buff=0.08)
        note = mixed("讀完第一個 0 就欠 0 個了：後面的 ", "$20$", " 是多出來的", font_size=26).move_to(np.array([2.4, 0.5, 0]))
        rot = VGroup(mixed("它的循環變形 ", font_size=26), word_tiles((2, 0, 0), size=0.45, font_size=26),
                     mixed(" 才是字", font_size=26)).arrange(RIGHT, buff=0.15).next_to(note, DOWN, buff=0.5)
        assert_in_frame(t2, b2, w2, note, rot)
        self.say("秩是 ", "$-1$", " 不一定是字：例如 ", "$020$")
        self.play(FadeIn(t2), FadeIn(b2), FadeIn(self.pointer), FadeIn(VGroup(z2, f2, w2.dots[0])))
        owe = 1
        for j, x in enumerate(BAD):
            owe += x - 1
            nb = draws_badge(owe, radius=0.3, font_size=30).move_to(b2)
            self.play(self.pointer.animate.move_to(np.array([t2[j].get_center()[0], t2.get_top()[1] + 0.25, 0])),
                      Transform(b2, nb), ShowCreation(w2.steps[j]), FadeIn(w2.dots[j + 1]), run_time=0.6)
            if j == 0:
                self.play(ShowCreation(extra), FadeIn(note))
                self.wait(1)
        self.play(FadeIn(rot))
        self.wait(2.5)
        self.play(FadeOut(VGroup(t2, b2, w2, z2, f2, extra, note, rot, self.pointer)))

        # 3. 字列
        t3 = word_tiles(LIST2, size=0.6, font_size=32).move_to(np.array([-1.5, 2.2, 0]))
        b3 = draws_badge(2, radius=0.3, font_size=30).next_to(t3, RIGHT, buff=0.8)
        w3 = rank_walk(LIST2, unit=0.42, origin=np.array([-4.6, 0.3, 0]))
        z3, f3 = level_line(w3, 0, 0, 7), level_line(w3, -2, 0, 7, color=MAROON_B)
        f3l = Tex("-2", font_size=24, fill_color=MAROON_B).next_to(f3, LEFT, buff=0.15)
        forest = forest_mob(split_words(LIST2), gap=0.9, x_gap=0.5, y_gap=0.6).move_to(np.array([3.4, 0.0, 0]))
        self.pointer.move_to(np.array([t3[0].get_center()[0] - 0.8, t3.get_top()[1] + 0.25, 0]))
        assert_in_frame(t3, b3, w3, forest, f3l)
        assert_apart(w3, forest)
        self.say("$n$", " 個字接成「字列」：一開始欠 ", "$n$", " 個，欠到 0 才結束")
        self.play(FadeIn(t3), FadeIn(b3), FadeIn(self.pointer), FadeIn(VGroup(z3, f3, f3l, w3.dots[0])))
        owe = 2
        cut = None
        for j, x in enumerate(LIST2):
            owe += x - 1
            nb = draws_badge(owe, radius=0.3, font_size=30).move_to(b3)
            self.play(self.pointer.animate.move_to(np.array([t3[j].get_center()[0], t3.get_top()[1] + 0.25, 0])),
                      Transform(b3, nb), ShowCreation(w3.steps[j]), FadeIn(w3.dots[j + 1]), run_time=0.55)
            if j == 3:
                cut = DashedLine(t3[3].get_corner(UR) + 0.04 * RIGHT + 0.1 * UP, t3[3].get_corner(DR) + 0.04 * RIGHT + 0.1 * DOWN,
                                 stroke_color=YELLOW, stroke_width=4)
                self.play(ShowCreation(cut), run_time=0.5)
        self.say("欠到 1 時第一個字結束：", "$3000\\mid 200$", "，兩棵樹的森林")
        self.play(FadeIn(forest), run_time=1.2)
        crit = mixed("$n$", " 字列 ", "$\\Leftrightarrow$", " ", "$r=-n$", "，每個真開頭的秩 ", "$>-n$", font_size=28)
        crit.move_to(np.array([0, -2.3, 0]))
        assert_in_frame(crit)
        self.play(FadeIn(crit))
        self.wait(3)
