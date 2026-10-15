"""
Scene R03 —— 加強版：正的點數 1, 2, …, M 各恰出現一次（notes/ran_note015_改寫.pdf 第 4 節）
執行（在 codes/ 內）：manimgl scenes/sceneR03_positive_counts.py SceneR03PositiveCounts

x = (2,−1,−3,1,2)：從第 0..4 點讀，正的點數是 3,1,2,5,4。
排序法：把第 1..5 點依 (S_k, −k) 由小到大排成 3,4,5,2,1，從它們開始讀的正點數依序是 5,4,3,2,1。
公式 P(x) = #{x<k≤M: S_k>S_x} + #{k≤x: S_k≥S_x}（第二項用了 S_{k+M}=S_k+1 與整數）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import NOTE015_SEQ, heights, positive_count, positive_count_order, reading
from utils.raney_draw import readings_row, step_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

SEQ = NOTE015_SEQ
M = len(SEQ)
ORDER = positive_count_order(SEQ)


def check_math():
    assert [positive_count(reading(SEQ, i)) for i in range(M)] == [3, 1, 2, 5, 4]
    assert heights(SEQ)[1:] == [2, 1, -2, -1, 1] and ORDER == [3, 4, 5, 2, 1]
    assert [positive_count(reading(SEQ, k % M)) for k in ORDER] == [5, 4, 3, 2, 1]


def point_item(k: int, s: int) -> VGroup:
    box = Square(side_length=0.75, stroke_color=GREY_B, stroke_width=2.5)
    top = Tex(r"%d" % k, font_size=34).move_to(box)
    sub = Tex(r"S_{%d}=%d" % (k, s), font_size=24, fill_color=GREY_A).next_to(box, DOWN, buff=0.12)
    return VGroup(box, top, sub)


class SceneR03PositiveCounts(ChuScene):
    def construct(self):
        check_math()
        self.show_header("R03　加強版：正的點數各恰出現一次")

        tiles = step_tiles(SEQ, size=0.55, font_size=28).move_to(2.6 * UP)
        self.add(tiles)
        self.say("不只問「是不是好讀法」，而是數一數：出發後有幾個點的高度 ", "$>0$")
        row = readings_row(SEQ, range(M), center=np.array([0, 0.9, 0]), spacing=2.55, unit=0.24, mark="count")
        assert_in_frame(row)
        self.play(FadeIn(tiles), LaggedStartMap(FadeIn, row, lag_ratio=0.2), run_time=2.5)
        self.wait(2)
        self.say("正的點數是 ", "$3,1,2,5,4$", "：", "$1$", " 到 ", "$5$", " 每個恰出現一次")
        self.play(LaggedStartMap(Indicate, row.tags, lag_ratio=0.2, color=YELLOW), run_time=2)
        self.wait(2)

        # 排序法
        self.play(FadeOut(row), tiles.animate.move_to(2.65 * UP))
        S = heights(SEQ)
        items = VGroup(*[point_item(k, S[k]) for k in range(1, M + 1)]).arrange(RIGHT, buff=0.55)
        items.move_to(0.9 * UP)
        self.say("把第 ", "$1$", " 到 ", "$M$", " 點依高度 ", "$S_k$", " 由小到大排（一樣高時 ", "$k$", " 大的在前）")
        self.play(LaggedStartMap(FadeIn, items, lag_ratio=0.15), run_time=1.5)
        self.wait(1)
        slots = [items[k - 1].get_center().copy() for k in range(1, M + 1)]   # copy：get_center 會跟著物件移動
        self.play(*[items[k - 1].animate.move_to(slots[r]) for r, k in enumerate(ORDER)], run_time=2)
        counts = VGroup(*[Tex(r"%d" % positive_count(reading(SEQ, k % M)), font_size=40, fill_color=YELLOW)
                          for k in ORDER])
        for r, c in enumerate(counts):
            c.move_to(slots[r] + 1.35 * DOWN)
        lab = zh("從這點開始讀的正點數", font_size=24, color=GREY_A).next_to(counts, LEFT, buff=0.5)
        if lab.get_left()[0] < -6.7:
            lab.next_to(counts, DOWN, buff=0.3)
        assert_in_frame(items, counts, lab)
        self.say("排第 ", "$r$", " 位的點，從它開始讀有 ", "$M-r+1$", " 個正的點")
        self.play(LaggedStartMap(FadeIn, counts, lag_ratio=0.2), FadeIn(lab), run_time=1.8)
        self.wait(2.5)

        formula = VGroup(
            Tex(r"P(x)=\#\{x<k\le M:\ S_k>S_x\}+\#\{1\le k\le x:\ S_k\ge S_x\}", font_size=32),
            mixed("第二項：", "$S_{k+M}=S_k+1$", "，而且是整數", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(1.9 * DOWN)
        assert_in_frame(formula)
        assert_apart(formula, VGroup(counts, lab))
        self.say("理由：", "$P(x)$", " 數的正好是「排在 ", "$x$", " 之後或就是 ", "$x$", "」的點")
        self.play(Write(formula[0]), run_time=1.8)
        self.play(FadeIn(formula[1]))
        self.wait(3)

        # 定理
        self.play(FadeOut(VGroup(items, counts, lab, formula, tiles)))
        thm = VGroup(
            zh("加強版", font_size=36, color=YELLOW),
            mixed("整數 ", "$x_1,\\ldots,x_M$", " 的總和是 ", "$1$", font_size=30),
            mixed("對每個 ", "$k=1,\\ldots,M$", "，恰有一種讀法有 ", "$k$", " 個點高度 ", "$>0$", font_size=30),
            mixed("$k=M$", " 就是 Raney 引理", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        box = boxed(thm, color=YELLOW).move_to(0.6 * UP)
        assert_in_frame(box)
        self.say("原筆記第 40–48 行只有思路；這個結果對任意整數都成立")
        self.play(FadeIn(box, shift=0.2 * UP), run_time=1.2)
        self.wait(3)
