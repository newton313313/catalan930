"""
Scene 09 —— 總結：整篇論文的邏輯流程圖

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene09_summary.py Scene09Summary
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.formulas import GF_T2C, general_formula
from utils.polygon_groups import make_configuration
from utils.root_figure import RootFigure
from utils.scene_base import ChuScene
from utils.styles import D_COLOR, TYPE1_COLOR, TYPE2_COLOR, zh

BOX_WIDTH = 5.6
BOX_HEIGHT = 0.6

# 論文 Fig. 1 的五種分法（弦依序取五組相鄰點對）
FIG1_CONFIGS = [
    [((k + 3) % 5, (k + 4) % 5), (k % 5, (k + 1) % 5, (k + 2) % 5)] for k in range(5)
]


def flow_box(content: Mobject, color=GREY_B) -> VGroup:
    rect = RoundedRectangle(width=BOX_WIDTH, height=BOX_HEIGHT, corner_radius=0.12,
                            stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.10)
    if content.get_width() > BOX_WIDTH - 0.4:
        content.set_width(BOX_WIDTH - 0.4)
    content.move_to(rect)
    return VGroup(rect, content)


def line(*parts, font_size=26, t2c=None):
    """中文與數學式混排成一行（'$...$' 為數學式）。"""
    mobs = []
    for p in parts:
        if p.startswith("$"):
            mobs.append(Tex(p.strip("$"), font_size=font_size * 1.35, t2c=t2c or {}))
        else:
            mobs.append(zh(p, font_size=font_size))
    return VGroup(*mobs).arrange(RIGHT, buff=0.12)


class Scene09Summary(ChuScene):
    def construct(self):
        self.show_header("總結")

        gf_t2c = {"D": D_COLOR, "x_i": TYPE2_COLOR, "v_i": TYPE2_COLOR}
        contents = [
            (line("圓周上的 ", "$N=\\langle\\vec n,\\vec v\\rangle$", " 個點"), GREY_B),
            (line("分成 ", "$n_i$", " 個 ", "$v_i$", " 點群組，互不交叉"), TYPE1_COLOR),
            (line("固定一個點，看它所在的群組"), ORANGE),
            (line("其餘的點被切成 ", "$v_i$", " 段，各段獨立"), TEAL),
            (line("這種情況貢獻 ", "$x_iD^{v_i}$", t2c=gf_t2c), TYPE2_COLOR),
            (line("$D=1+\\textstyle\\sum_i x_iD^{v_i}$", t2c=gf_t2c), D_COLOR),
            (line("Raney 公式（或 Lagrange 反演）"), PINK),
            (line("廣義卡塔蘭數 ", "$C_{\\vec v}(\\vec n)$"), YELLOW),
        ]
        boxes = VGroup(*[flow_box(c, color) for c, color in contents])
        boxes.arrange(DOWN, buff=0.2)
        boxes.move_to(3.55 * LEFT + 0.2 * DOWN)
        arrows = VGroup(*[
            Arrow(a.get_bottom(), b.get_top(), buff=0.02, thickness=2.0,
                  fill_color=GREY_B, max_tip_length_to_length_ratio=0.9,
                  max_width_to_length_ratio=1.0)
            for a, b in zip(boxes[:-1], boxes[1:])
        ])

        # ------------------------------------------------------------ 右側的配圖
        right_x = 3.5
        thumbs = VGroup(*[make_configuration(5, c, radius=0.45) for c in FIG1_CONFIGS])
        thumbs.arrange(RIGHT, buff=0.25).move_to(right_x * RIGHT + 3.0 * UP)
        thumbs_tag = Tex(R"C_{(2,3)}(1,1)=5", font_size=34, fill_color=GREY_A)
        thumbs_tag.next_to(thumbs, DOWN, buff=0.15)

        fig = RootFigure(center=right_x * RIGHT + 0.8 * UP, radius=1.0,
                         label_font_size=28, label_buff=0.3)

        # ------------------------------------------------------------ 依序出現
        self.play(FadeIn(boxes[0], shift=0.2 * DOWN), run_time=0.7)
        self.wait(0.4)
        self.play(GrowArrow(arrows[0]), FadeIn(boxes[1], shift=0.2 * DOWN), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in thumbs], lag_ratio=0.15),
                  FadeIn(thumbs_tag), run_time=1.2)
        self.wait(0.6)

        self.play(GrowArrow(arrows[1]), FadeIn(boxes[2], shift=0.2 * DOWN), run_time=0.8)
        self.play(FadeIn(fig.config.circle), FadeIn(fig.config.dots), run_time=0.6)
        self.play(Flash(fig.coords[0], color=ORANGE, flash_radius=0.25), run_time=0.6)

        self.play(GrowArrow(arrows[2]), FadeIn(boxes[3], shift=0.2 * DOWN), run_time=0.8)
        self.play(FadeIn(fig.root), FadeIn(fig.regions), FadeIn(fig.region_labels), run_time=0.8)
        self.play(*[FadeIn(s) for s in fig.subs], run_time=0.7)
        self.wait(0.6)

        for k in range(3, 7):
            self.play(GrowArrow(arrows[k]), FadeIn(boxes[k + 1], shift=0.2 * DOWN), run_time=0.8)
            self.wait(0.5)
        self.wait(0.8)

        # ------------------------------------------------------------ 最後的結論
        statement = VGroup(
            Tex(R"C_{\vec v}(\vec n)\;=", font_size=46),
            zh("指定各種群組個數時，", font_size=26),
        ).arrange(RIGHT, buff=0.2)
        statement2 = zh("圓周上不交叉分法的數目", font_size=26)
        formula = general_formula(font_size=34)
        block = VGroup(statement, statement2, formula).arrange(DOWN, buff=0.18)
        statement2.align_to(statement[1], LEFT)
        block.move_to(right_x * RIGHT + 2.2 * DOWN)
        block_box = SurroundingRectangle(block, buff=0.2, color=YELLOW, stroke_width=3)

        self.play(
            FadeIn(block, shift=0.2 * UP),
            Indicate(boxes[-1][0], scale_factor=1.04, color=YELLOW),
            run_time=1.2,
        )
        self.play(ShowCreation(block_box), run_time=0.9)
        self.wait(5.0)
