"""
Scene R01 —— Raney 引理：和為 1 的整數序列恰有一種好讀法（notes/ran_note015_改寫.pdf 第 2–3 節）
執行（在 codes/ 內）：manimgl scenes/sceneR01_raney_lemma.py SceneR01RaneyLemma

主例 x = (2, −1, −3, 1, 2)：總和 1；畫成路徑（每步改變高度 x_j）；5 種循環讀法中只有從第 3 點開始的
(1, 2, 2, −1, −3) 出發後一直在 0 之上。最後說明這是 Chu 講義循環引理 t = 1 的情形。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import NOTE015_SEQ, good_starts, heights, reading
from utils.raney_draw import IntPathMob, level_line, readings_row, step_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

SEQ = NOTE015_SEQ


def check_math():
    assert sum(SEQ) == 1 and heights(SEQ) == [0, 2, 1, -2, -1, 1]
    assert good_starts(SEQ) == [3] and reading(SEQ, 3) == (1, 2, 2, -1, -3)
    assert heights(reading(SEQ, 3))[1:] == [1, 3, 5, 4, 1]


class SceneR01RaneyLemma(ChuScene):
    def construct(self):
        check_math()
        self.show_header("R01　Raney 引理：和為 1 的整數序列")

        # 1. 序列與總和
        tiles = step_tiles(SEQ, size=0.7, font_size=34).move_to(2.3 * UP)
        total = Tex(r"2-1-3+1+2=1", font_size=40).next_to(tiles, DOWN, buff=0.35)
        self.say("一串整數 ", "$x_1,\\ldots,x_M$", "，總和是 ", "$1$")
        self.play(LaggedStartMap(FadeIn, tiles, lag_ratio=0.15), run_time=1.2)
        self.play(Write(total))
        self.wait(1)

        # 2. 畫成路徑
        path = IntPathMob(SEQ, unit=0.62, origin=np.array([-1.55, -0.45, 0]))
        base = level_line(path, 0, -0.5, 5.5)
        hlabs = VGroup(*[Tex(str(h), font_size=26, fill_color=GREY_A).next_to(path.vertex(j), UP if j != 3 else DOWN,
                                                                             buff=0.12)
                         for j, h in enumerate(path.heights)])
        assert_in_frame(tiles, total, path, hlabs)
        assert_apart(total, VGroup(path, hlabs))
        self.say("每一步改變高度 ", "$x_j$", "：畫成一條路徑，終點高度 1")
        self.play(FadeIn(base), ShowCreation(path.steps, lag_ratio=1), FadeIn(path.dots), run_time=2.5)
        self.play(FadeIn(hlabs), run_time=0.8)
        self.wait(2.5)

        # 3. 五種循環讀法
        self.play(FadeOut(VGroup(path, base, hlabs, total)), tiles.animate.scale(0.75).move_to(2.55 * UP))
        self.say("從第 ", "$i$", " 點開始讀一圈：", "$x_{i+1},x_{i+2},\\ldots$", "，共 5 種讀法")
        row = readings_row(SEQ, range(5), center=np.array([0, 0.6, 0]), spacing=2.55, unit=0.24, mark=None)
        assert_in_frame(row)
        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.2), run_time=2.5)
        self.wait(2)
        self.say("好讀法：出發後每一點的高度都 ", "$>0$")
        marks = readings_row(SEQ, range(5), center=np.array([0, 0.6, 0]), spacing=2.55, unit=0.24).tags
        self.play(LaggedStartMap(FadeIn, marks, lag_ratio=0.25), run_time=2)
        good = row[3]
        frame = SurroundingRectangle(VGroup(good, marks[3]), color=YELLOW, buff=0.15)
        self.play(ShowCreation(frame))
        self.say("只有從第 3 點開始的 ", "$1,2,2,-1,-3$", " 是好讀法：高度 ", "$1,3,5,4,1$")
        self.wait(3)

        # 4. 定理
        self.play(FadeOut(VGroup(row, marks, frame, tiles)))
        thm = VGroup(
            zh("Raney 引理", font_size=36, color=YELLOW),
            mixed("整數 ", "$x_1,\\ldots,x_M$", " 的總和是 ", "$1$", font_size=32),
            mixed("則 ", "$M$", " 種循環讀法中，恰有一種是好讀法", font_size=32),
        ).arrange(DOWN, buff=0.3)
        box = boxed(thm, color=YELLOW).move_to(0.9 * UP)
        note = mixed("這是 Chu 講義第 7 節循環引理的 ", "$t=1$", " 情形", font_size=28, color=GREY_A)
        note.next_to(box, DOWN, buff=0.5)
        assert_in_frame(box, note)
        self.play(FadeIn(box, shift=0.2 * UP), run_time=1.2)
        self.say("下一幕：為什麼一定有、而且只有一種？")
        self.play(FadeIn(note))
        self.wait(2.5)
