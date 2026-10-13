"""
Scene 00a —— 卡塔蘭數是什麼（卡塔蘭基礎模組的開頭）

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00a_catalan_definition.py Scene00aCatalanDefinition
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, TYPE1_COLOR, YELLOW, boxed, zh

SHOWN = 9          # 顯示 C_0 .. C_8
EXAMPLES = [       # (n, 代入公式的寫法)
    (0, R"C_0=\frac{1}{1}\binom{0}{0}=1"),
    (1, R"C_1=\frac{1}{2}\binom{2}{1}=1"),
    (2, R"C_2=\frac{1}{3}\binom{4}{2}=\frac{6}{3}=2"),
    (3, R"C_3=\frac{1}{4}\binom{6}{3}=\frac{20}{4}=5"),
    (4, R"C_4=\frac{1}{5}\binom{8}{4}=\frac{70}{5}=14"),
]
ROADMAP = ["三角剖分", "遞迴", "括號", "二元樹", "格子路徑",
           "Dyck 路徑", "投票", "不交叉配對", "生成函數", "Chu 的推廣"]


class Scene00aCatalanDefinition(ChuScene):
    def construct(self):
        values = [catalan(n) for n in range(SHOWN)]
        assert values == [1, 1, 2, 5, 14, 42, 132, 429, 1430]

        # ------------------------------------------------------------ 數列一個一個出現
        cells = VGroup()
        for v in values:
            num = Tex(str(v), font_size=62)
            comma = Tex(",", font_size=62)
            comma.next_to(num, RIGHT, buff=0.06, aligned_edge=DOWN)
            cells.add(VGroup(num, comma))
        dots = Tex(R"\ldots", font_size=62)
        row = VGroup(*cells, dots).arrange(RIGHT, buff=0.42, aligned_edge=DOWN)
        if row.get_width() > 12.6:
            row.set_width(12.6)
        row.move_to(2.25 * UP)
        for cell in cells:
            self.play(FadeIn(cell, shift=0.25 * UP), run_time=0.35)
        self.play(FadeIn(dots), run_time=0.3)
        self.say("這串數字會在許多看起來毫不相關的問題裡出現")
        self.wait(1.2)

        question = zh("為什麼同一串數字到處出現？", font_size=46, color=YELLOW)
        question.move_to(0.4 * UP)
        self.play(Write(question), run_time=1.2)
        self.wait(1.8)
        self.show_header("卡塔蘭數（Catalan numbers）")

        # ------------------------------------------------------------ 編號與公式
        labels = VGroup()
        for n, cell in enumerate(cells):
            lab = Tex(f"C_{{{n}}}", font_size=30, fill_color=MUTED_COLOR)
            lab.next_to(cell[0], DOWN, buff=0.25)
            labels.add(lab)
        formula = Tex(R"C_n=\frac{1}{n+1}\binom{2n}{n}", font_size=66)
        formula_box = boxed(formula, color=TYPE1_COLOR, buff=0.28)
        formula_box.move_to(0.25 * UP)
        tag = Tex(R"n=0,1,2,\ldots", font_size=32, fill_color=MUTED_COLOR)
        tag.next_to(formula_box, RIGHT, buff=0.4)
        self.play(FadeOut(question, shift=0.3 * DOWN), LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.1),
                  run_time=1.2)
        self.say("第 ", "$n$", " 個卡塔蘭數記作 ", "$C_n$", "，有一個公式")
        self.play(Write(formula), ShowCreation(formula_box[0]), run_time=1.6)
        self.play(FadeIn(tag), run_time=0.5)
        self.wait(1.0)

        examples = VGroup(*[Tex(s, font_size=38) for _, s in EXAMPLES])
        row1 = VGroup(*examples[:3]).arrange(RIGHT, buff=0.7)
        row2 = VGroup(*examples[3:]).arrange(RIGHT, buff=0.7)
        VGroup(row1, row2).arrange(DOWN, buff=0.35).move_to(1.72 * DOWN)
        self.say("代入 ", "$n=0,1,2,3,4$", " 驗算")
        for (n, _), ex in zip(EXAMPLES, examples):
            self.play(FadeIn(ex, shift=0.2 * UP),
                      Indicate(cells[n][0], scale_factor=1.3, color=YELLOW),
                      Indicate(labels[n], scale_factor=1.3, color=YELLOW),
                      run_time=0.8)
        self.wait(1.5)

        # ------------------------------------------------------------ 名字的由來（約 12 秒）
        self.play(FadeOut(examples), FadeOut(tag), formula_box.animate.scale(0.75).move_to(0.35 * UP),
                  run_time=0.8)
        history = VGroup(
            zh("Euler、Segner（18 世紀）：研究凸多邊形的三角剖分；Segner 給出遞迴式", font_size=26),
            zh("明安圖（清代）：在三角函數的展開式裡，獨立發現這串數", font_size=26),
            zh("Catalan（1838 年）：研究括號問題；這串數後來以他命名", font_size=26),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        history.move_to(1.35 * DOWN)
        self.say("一點歷史")
        self.play(LaggedStart(*[FadeIn(h, shift=0.2 * RIGHT) for h in history], lag_ratio=0.5),
                  run_time=2.4)
        self.wait(5.0)

        # ------------------------------------------------------------ 這一段的路線
        self.play(FadeOut(history), run_time=0.6)
        items = VGroup(*[zh(s, font_size=24, color=WHITE) for s in ROADMAP])
        boxes = VGroup()
        for it in items:
            rect = RoundedRectangle(width=it.get_width() + 0.32, height=0.5, corner_radius=0.1,
                                    stroke_color=GREY_B, stroke_width=1.5)
            rect.set_fill(GREY_E, opacity=0.6)
            boxes.add(VGroup(rect, it.move_to(rect)))
        boxes[-1][0].set_stroke(YELLOW, width=2.5)
        top = VGroup(*boxes[:5]).arrange(RIGHT, buff=0.42)
        bottom = VGroup(*boxes[5:]).arrange(RIGHT, buff=0.42)
        VGroup(top, bottom).arrange(DOWN, buff=0.55).move_to(1.45 * DOWN)
        arrows = VGroup()
        for a, b in list(zip(boxes[:4], boxes[1:5])) + list(zip(boxes[5:9], boxes[6:10])):
            arrows.add(Arrow(a.get_right(), b.get_left(), buff=0.06, thickness=2, fill_color=GREY_B))
        turn = Arrow(boxes[4].get_bottom(), boxes[5].get_top(), buff=0.08, thickness=2, fill_color=GREY_B)
        arrows.add(turn)
        self.say("接下來：同一個 ", "$C_n$", " 在不同的地方出現，最後接到 Chu 的推廣")
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in boxes], lag_ratio=0.12),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=2.6)
        self.wait(3.0)
