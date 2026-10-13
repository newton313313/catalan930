"""
Scene 05 —— 整篇論文最重要的一步：固定一個點，群組把其餘的點切成獨立的幾段

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene05_root_decomposition.py Scene05RootDecomposition
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.circle_points import make_circle_points
from utils.polygon_groups import dot_color_anims, make_block, root_regions
from utils.scene_base import ChuScene
from utils.styles import (
    D_COLOR,
    REGION_COLORS,
    ROOT_COLOR,
    TYPE1_COLOR,
    TYPE2_COLOR,
    block_color,
    zh,
)

N_POINTS = 12
ROOT = (0, 4, 9)                 # 固定點 0 所在的群組（三角形，v_i = 3）
ALT_ROOT = (0, 4, 5)             # 用來說明「至多」：4 與 5 相鄰，中間那一段是空的
# 每一段裡的子結構（手動指定）
SUB_BLOCKS = [
    [(1, 2, 3)],                 # R_1：3 個點 -> 一個三角形
    [(5, 8), (6, 7)],            # R_2：4 個點 -> 兩條弦
    [(10, 11)],                  # R_3：2 個點 -> 一條弦
]
ALT_R2 = [(5, 6), (7, 8)]        # R_2 的另一種分法
REGION_POINTS = [(1, 2, 3), (5, 6, 7, 8), (10, 11)]


def region_label_positions(regions, center, radius, buff=0.48):
    return [center + (radius + buff) * normalize(r.arc_mid - center) for r in regions]


class Scene05RootDecomposition(ChuScene):
    def construct(self):
        self.show_header("證明的關鍵：固定一個點")

        center = 3.35 * LEFT + 0.1 * UP
        radius = 2.3
        circle, dots, coords = make_circle_points(N_POINTS, radius=radius, center=center)
        self.play(ShowCreation(circle), run_time=0.8)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), run_time=1.0)
        self.say("圓周上有一些點（這裡畫 12 個），我們要數不交叉的分法")
        self.wait(1.2)

        # ------------------------------------------------------------ Step 1：固定點
        root_dot = dots[0]
        p0_label = VGroup(
            zh("固定點", font_size=28, color=ROOT_COLOR),
            Tex("p_0", font_size=38, fill_color=ROOT_COLOR),
        ).arrange(RIGHT, buff=0.12).next_to(coords[0], UP, buff=0.25)
        self.say("先在圓周上固定一個點")
        self.play(
            root_dot.animate.set_fill(ROOT_COLOR).scale(1.7),
            Flash(coords[0], color=ROOT_COLOR, flash_radius=0.35),
            FadeIn(p0_label, shift=0.2 * DOWN),
            run_time=1.0,
        )
        self.play(self.frame.animate.scale(0.62).move_to(coords[0] + 0.9 * DOWN), run_time=1.2)
        self.wait(0.8)
        self.play(self.frame.animate.scale(1 / 0.62).move_to(ORIGIN), run_time=1.0)

        # ------------------------------------------------------------ Step 2：它所在的群組
        self.say("它一定屬於某個群組。假設這個群組有 ", "$v_i$", " 個點（這裡 ", "$v_i=3$", "）")
        root = make_block(ROOT, coords, stroke_width=7)
        self.play(
            *dot_color_anims(dots, ROOT[1:], TYPE2_COLOR),
            *[Flash(coords[i], color=TYPE2_COLOR, flash_radius=0.3) for i in ROOT[1:]],
            run_time=0.8,
        )
        self.play(ShowCreation(root), run_time=1.2)
        vi_tag = VGroup(
            zh("根群組：", font_size=30, color=TYPE2_COLOR),
            Tex("v_i=3", font_size=52, fill_color=TYPE2_COLOR),
        ).arrange(RIGHT, buff=0.2).move_to(3.4 * RIGHT + 2.65 * UP)
        self.play(FadeIn(vi_tag, shift=0.2 * LEFT), run_time=0.6)
        self.wait(1.0)

        # ------------------------------------------------------------ Step 3：切出的區域
        regions = root_regions(ROOT, N_POINTS, radius, center, opacity=0.30)
        regions.set_z_index(-1)
        label_pos = region_label_positions(regions, center, radius)
        region_labels = VGroup(*[
            Tex(f"R_{k + 1}", font_size=46, fill_color=REGION_COLORS[k]).move_to(label_pos[k])
            for k in range(3)
        ])
        self.say("這個群組把其餘的點切成 3 段（一般是 ", "$v_i$", " 段）")
        for k in range(3):
            self.play(FadeIn(regions[k]), FadeIn(region_labels[k], scale=1.4), run_time=0.6)
            self.play(*[Indicate(dots[i], scale_factor=1.9, color=REGION_COLORS[k])
                        for i in REGION_POINTS[k]], run_time=0.7)
        self.wait(1.0)

        # ------------------------------------------------------------ Step 3b：為什麼說「至多」
        self.say("相鄰兩個頂點之間可能沒有點：那一段是空的（論文說「至多 ", "$v_i$", " 段」）")
        alt_root = make_block(ALT_ROOT, coords, stroke_width=7)
        alt_regions = root_regions(ALT_ROOT, N_POINTS, radius, center, opacity=0.30)
        alt_pos = region_label_positions(alt_regions, center, radius)
        root_backup, regions_backup = root.copy(), regions.copy()
        empty_note = zh("（空）", font_size=28, color=REGION_COLORS[1])
        self.play(
            Transform(root, alt_root),
            *[Transform(r, ar) for r, ar in zip(regions, alt_regions)],
            *[lab.animate.move_to(p) for lab, p in zip(region_labels, alt_pos)],
            *dot_color_anims(dots, [9], WHITE),
            *dot_color_anims(dots, [5], TYPE2_COLOR),
            run_time=1.4,
        )
        empty_note.next_to(region_labels[1], RIGHT, buff=0.1)
        self.play(FadeIn(empty_note), run_time=0.4)
        self.wait(1.6)
        self.play(
            FadeOut(empty_note),
            Transform(root, root_backup),
            *[Transform(r, rb) for r, rb in zip(regions, regions_backup)],
            *[lab.animate.move_to(p) for lab, p in zip(region_labels, label_pos)],
            *dot_color_anims(dots, [5], WHITE),
            *dot_color_anims(dots, [9], TYPE2_COLOR),
            run_time=1.2,
        )

        # ------------------------------------------------------------ Step 4：各段是獨立的小問題
        self.say("群組不能交叉，所以每個群組只能整個待在同一段裡")
        subs = [VGroup(*[make_block(b, coords) for b in blocks]) for blocks in SUB_BLOCKS]
        for k in range(3):
            recolor = []
            for b in SUB_BLOCKS[k]:
                recolor += dot_color_anims(dots, b, block_color(len(b)))
            self.play(
                LaggedStart(*[ShowCreation(b) for b in subs[k]], lag_ratio=0.5),
                *recolor,
                run_time=1.0,
            )
            self.wait(0.3)
        self.say("每一段裡面，都是一個比較小的同類問題")
        self.wait(1.5)

        self.say("其中一段換一種分法，完全不影響其他段：各段互相獨立")
        r2_backup = subs[1].copy()
        r2_alt = VGroup(*[make_block(b, coords) for b in ALT_R2])
        ring = regions[1].copy().set_fill(opacity=0).set_stroke(REGION_COLORS[1], width=5)
        ring.set_z_index(1)
        self.play(ShowCreation(ring), run_time=0.6)
        self.play(Transform(subs[1], r2_alt), run_time=0.9)
        self.wait(0.8)
        self.play(Transform(subs[1], r2_backup), run_time=0.9)
        self.wait(0.5)
        self.play(Transform(subs[1], r2_alt.copy()), run_time=0.9)
        self.wait(0.5)
        self.play(Transform(subs[1], r2_backup.copy()), FadeOut(ring), run_time=0.9)
        self.wait(0.6)

        # ------------------------------------------------------------ Step 5：翻譯成代數
        x0 = 3.4
        d_letters = VGroup(*[Tex("D", font_size=84, fill_color=REGION_COLORS[k]) for k in range(3)])
        times = VGroup(*[Tex(R"\times", font_size=60) for _ in range(2)])
        row = VGroup(d_letters[0], times[0], d_letters[1], times[1], d_letters[2])
        row.arrange(RIGHT, buff=0.35).move_to(x0 * RIGHT + 1.25 * UP)
        under = VGroup(*[
            Tex(f"R_{k + 1}", font_size=32, fill_color=REGION_COLORS[k]).next_to(d_letters[k], DOWN, buff=0.2)
            for k in range(3)
        ])
        self.say("用 ", "$D$", " 代表「一段裡所有可能的分法」；各段獨立，所以相乘")
        self.play(
            LaggedStart(*[TransformFromCopy(region_labels[k], d_letters[k]) for k in range(3)],
                        lag_ratio=0.3),
            run_time=1.8,
        )
        self.play(FadeIn(times), FadeIn(under), run_time=0.6)
        self.wait(1.2)

        equals = Tex("=", font_size=64)
        d_cubed = Tex("D^3", font_size=92, t2c={"D": D_COLOR})
        result = VGroup(equals, d_cubed).arrange(RIGHT, buff=0.3).move_to(x0 * RIGHT + 0.55 * DOWN)
        self.play(FadeIn(equals), TransformFromCopy(d_letters, d_cubed), run_time=1.2)
        self.wait(0.8)

        d_general = Tex("D^{v_i}", font_size=92, t2c={"D": D_COLOR, "v_i": TYPE2_COLOR})
        d_general.move_to(d_cubed, aligned_edge=LEFT)
        self.say("3 段給出 ", "$D^3$", "；一般的 ", "$v_i$", " 點群組給出 ", "$D^{v_i}$")
        self.play(
            FadeTransform(d_cubed, d_general),
            Indicate(vi_tag[1], scale_factor=1.25, color=TYPE2_COLOR),
            run_time=1.2,
        )
        self.wait(1.5)

        # ------------------------------------------------------------ Step 6：x_i
        self.say("根群組本身用掉一個第 ", "$i$", " 型群組，用變數 ", "$x_i$", " 記下來")
        x_i = Tex("x_i", font_size=92, fill_color=TYPE2_COLOR)
        term = VGroup(x_i, d_general.copy()).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        x_i.shift(0.1 * DOWN)
        term.move_to(x0 * RIGHT + 2.1 * DOWN)
        self.play(Indicate(root, scale_factor=1.06, color=TYPE2_COLOR), run_time=1.0)
        self.play(
            TransformFromCopy(root, x_i),
            TransformFromCopy(d_general, term[1]),
            run_time=1.4,
        )
        term_box = SurroundingRectangle(term, buff=0.22, color=YELLOW, stroke_width=3)
        self.play(ShowCreation(term_box), run_time=0.7)
        self.say("固定點落在第 ", "$i$", " 型群組上的所有情況，合起來就是 ", "$x_iD^{v_i}$",
                 t2c={"x_i": TYPE2_COLOR, "v_i": TYPE2_COLOR, "D": D_COLOR})
        self.wait(3.5)
