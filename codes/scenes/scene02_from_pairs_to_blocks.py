"""
Scene 02 —— 從「兩點一組」推廣成「v 點一組」

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene02_from_pairs_to_blocks.py Scene02FromPairsToBlocks
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.circle_points import make_circle_points
from utils.polygon_groups import dot_color_anims, make_block, make_configuration
from utils.scene_base import ChuScene
from utils.styles import block_color, zh

N_POINTS = 10
# (群組點數 v, 點編號, 名稱)；全部手動指定
STEPS = [
    (2, (0, 3), "弦"),
    (3, (0, 3, 6), "三角形"),
    (4, (0, 2, 5, 7), "四邊形"),
    (5, (0, 2, 4, 6, 8), "五邊形"),
]
CAPTIONS = [
    ("經典情形：每一組恰有 2 個點，連起來是一條弦",),
    ("如果一組有 3 個點？把它們連起來，得到三角形",),
    ("一組 4 個點：四邊形",),
    ("一組 5 個點：五邊形",),
]


class Scene02FromPairsToBlocks(ChuScene):
    def construct(self):
        self.show_header("從「兩點一組」到「v 點一組」")

        center = 1.3 * RIGHT + 0.3 * UP
        radius = 2.25
        circle, dots, coords = make_circle_points(N_POINTS, radius=radius, center=center)
        self.play(ShowCreation(circle), FadeIn(dots), run_time=0.9)

        rows = VGroup()
        block = None
        tag = None
        prev_indices = ()
        for k, (v, indices, name) in enumerate(STEPS):
            color = block_color(v)
            new_block = make_block(indices, coords)
            new_tag = VGroup(
                Tex(f"v={v}", font_size=68, fill_color=color),
                zh(name, font_size=40, color=color),
            ).arrange(DOWN, buff=0.3).next_to(circle, RIGHT, buff=0.8)

            recolor = [
                *dot_color_anims(dots, [i for i in prev_indices if i not in indices], WHITE),
                *dot_color_anims(dots, indices, color),
            ]
            if block is None:
                self.play(ShowCreation(new_block), FadeIn(new_tag, shift=0.3 * LEFT), *recolor, run_time=1.0)
            else:
                self.play(
                    ReplacementTransform(block, new_block),
                    FadeOut(tag, shift=0.3 * UP),
                    FadeIn(new_tag, shift=0.3 * UP),
                    *recolor,
                    run_time=1.1,
                )
            block, tag, prev_indices = new_block, new_tag, indices
            self.say(*CAPTIONS[k])
            self.wait(0.7)

            # 左邊的清單：小圖 + v = ... + 名稱
            icon = make_configuration(N_POINTS, [indices], radius=0.42)
            row = VGroup(
                icon,
                Tex(f"v={v}", font_size=38, fill_color=color),
                zh(name, font_size=28, color=color),
            ).arrange(RIGHT, buff=0.3)
            row.move_to((1.95 - 1.15 * k) * UP)
            row.to_edge(LEFT, buff=0.7)
            self.play(
                TransformFromCopy(block, icon.blocks[0]),
                FadeIn(icon.circle), FadeIn(icon.dots),
                FadeIn(row[1:], shift=0.2 * RIGHT),
                run_time=0.9,
            )
            rows.add(row)
            self.wait(0.3)

        self.say("一個 ", "$v$", " 點群組，畫出來就是一個凸 ", "$v$", " 邊形")
        self.wait(1.8)

        # ------------------------------------------------------------ 兩個向量
        big = VGroup(circle, dots, block, tag)
        self.play(FadeOut(big, shift=0.5 * RIGHT), run_time=0.7)

        v_vec = Tex(R"\vec v=(v_1,\,v_2,\,\ldots,\,v_k)", font_size=60)
        v_note = zh("有哪幾種群組大小（每種群組的點數）", font_size=30, color=GREY_A)
        n_vec = Tex(R"\vec n=(n_1,\,n_2,\,\ldots,\,n_k)", font_size=60)
        n_note = zh("每種大小各要幾個", font_size=30, color=GREY_A)
        right = VGroup(v_vec, v_note, n_vec, n_note).arrange(DOWN, buff=0.35)
        n_vec.shift(0.35 * DOWN)
        n_note.shift(0.35 * DOWN)
        right.move_to(2.2 * RIGHT + 0.6 * UP)

        self.say("Chu 的推廣：同時允許好幾種大小的群組")
        self.play(Write(v_vec), run_time=1.2)
        self.play(FadeIn(v_note, shift=0.2 * UP), run_time=0.6)
        self.wait(0.8)
        self.play(Write(n_vec), run_time=1.2)
        self.play(FadeIn(n_note, shift=0.2 * UP), run_time=0.6)
        self.wait(1.0)

        rule = VGroup(
            zh("要", font_size=44),
            Tex("n_i", font_size=60, fill_color=YELLOW),
            zh("個", font_size=44),
            Tex("v_i", font_size=60, fill_color=YELLOW),
            zh("點群組", font_size=44),
        ).arrange(RIGHT, buff=0.2)
        rule.next_to(right, DOWN, buff=0.7)
        rule_box = SurroundingRectangle(rule, buff=0.25, color=YELLOW, stroke_width=3)
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=0.8)
        self.play(ShowCreation(rule_box), run_time=0.8)
        self.say("$\\vec v$", " 說明群組的大小，", "$\\vec n$", " 說明每種大小要幾個")
        self.wait(3.0)
