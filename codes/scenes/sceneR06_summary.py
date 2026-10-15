"""
Scene R06 —— 小結與原筆記的勘誤重點（notes/ran_note015_改寫.pdf 第 1、7 節）
執行（在 codes/ 內）：manimgl scenes/sceneR06_summary.py SceneR06Summary

三件事各用一句話與一個小圖回顧（R01–R05），再列出原筆記 ran_note015.txt 的五個勘誤重點。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import raney_A
from utils.fulton_draw import assert_in_frame
from utils.raney import NOTE015_SEQ, card_game_formula, good_starts, reading, stack_ops_to_steps
from utils.raney_draw import IntPathMob, level_line
from utils.scene_base import ChuScene
from utils.styles import mixed, zh

ERRATA = [
    ("第 19 行", "下標錯一位：", "$S_{i+M}=S_i+x_{i+1}+\\cdots+x_{i+M}$"),
    ("第 32 行", "唯一性少一種情形，而且要用到「整數」", ""),
    ("第 84 行", "符號寫反：", "$\\sum(w_i-1)+(-1)(m-n)=0$"),
    ("第 98–100 行", "答案對，理由要換成「交換標號的對稱性」", ""),
    ("例題二", "公式的 ", "$n$"),
]


def check_math():
    assert good_starts(NOTE015_SEQ) == [3] and raney_A(1, (3,), (2,)) == 5 and card_game_formula((1, 2), 3) == 3


def mini_path(steps, unit=0.22):
    p = IntPathMob(steps, unit=unit, stroke_width=4, dot_radius=0.03)
    return VGroup(level_line(p, 0, 0, len(steps)), p)


class SceneR06Summary(ChuScene):
    def construct(self):
        check_math()
        self.show_header("R06　小結與原筆記的勘誤")

        rows = VGroup()
        items = [
            (mini_path(reading(NOTE015_SEQ, 3)), ["Raney 引理：總和 ", "$1$", " 的整數序列恰有一種好讀法（", "$t=1$", " 的循環引理）"]),
            (mini_path(NOTE015_SEQ), ["加強版：正的點數 ", "$1,\\ldots,M$", " 各恰出現一次；依 ", "$(S_k,-k)$", " 排序就知道是哪一種"]),
            (mini_path((1,) + stack_ops_to_steps("PPOPOO")), ["出棧序列：前面加一個 ", "$\\uparrow$", "，", "$\\frac{1}{2n+1}\\binom{2n+1}{n}=C_n$"]),
            (VGroup(Tex(r"2010", font_size=34, fill_color=YELLOW)), ["摸牌：合格的牌序就是 Raney 的字，答案 ", "$\\frac{m!}{m-n+1}$"]),
        ]
        for k, (pic, txt) in enumerate(items):
            y = 2.0 - 1.25 * k
            if pic.get_width() > 1.4:
                pic.set_width(1.4)
            if pic.get_height() > 0.95:
                pic.set_height(0.95)
            pic.move_to(np.array([-5.7, y, 0]))
            t = mixed(*txt, font_size=26)
            t.move_to(np.array([0, y, 0])).align_to(np.array([-4.6, 0, 0]), LEFT)
            rows.add(VGroup(pic, t))
        assert_in_frame(rows)
        self.say("回顧：同一個引理，三種用法")
        for r in rows:
            self.play(FadeIn(r, shift=0.2 * RIGHT), run_time=1.0)
            self.wait(1.5)
        self.wait(1.5)

        self.play(FadeOut(rows))
        title = zh("原筆記 ran_note015.txt：結論都對，推導有幾處要改", font_size=30, color=YELLOW).move_to(2.5 * UP)
        errs = VGroup()
        for where, a, b in ERRATA:
            parts = [where + "　", a] + ([b] if b else [])
            if where == "例題二":
                parts = [where + "　", "公式的 ", "$n$", " 只能算 ", "$w_i\\ge 1$", " 的牌"]
            errs.add(mixed(*parts, font_size=26))
        errs.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(title, DOWN, buff=0.5)
        assert_in_frame(title, errs)
        self.say("完整的勘誤表在 ", "ran_note015_改寫.pdf", " 第 1 節")
        self.play(FadeIn(title))
        self.play(LaggedStartMap(FadeIn, errs, lag_ratio=0.4), run_time=4)
        self.wait(4)
