"""
Scene 00j —— 圓上的不交叉完美配對，以及「固定一點」的遞迴

    圓周上 2n 個點的不交叉完美配對有 C_n 種（Motzkin；也是 Chu 論文的出發點）
    固定一個點：它的弦把其餘的點分成 2 個獨立的區域 -> C_n = sum C_k C_{n-1-k}
這正是 Chu 證明中「v_i = 2」的情形（之後一組有 v_i 個點 -> v_i 個區域）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00j_noncrossing_matchings.py Scene00jNoncrossingMatchings
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    LEFT_COLOR,
    RIGHT_COLOR,
    catalan_product_tex,
    matching_item,
)
from utils.circle_points import chords_intersection, label_points, make_circle_points
from utils.counting import binary_trees, catalan, dyck_to_matching, tree_to_dyck
from utils.polygon_groups import circular_segment, make_block
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, ROOT_COLOR, YELLOW, mixed, zh

N = 3
CENTER = np.array([-4.2, -0.15, 0.0])
RADIUS = 1.85
GOOD = [(0, 5), (1, 2), (3, 4)]
BAD = [(0, 3), (1, 4), (2, 5)]


class Scene00jNoncrossingMatchings(ChuScene):
    def construct(self):
        self.show_header("圓上的不交叉配對")
        trees = binary_trees(N)
        matchings = [dyck_to_matching(tree_to_dyck(t)) for t in trees]
        partners = [dict(m)[0] for m in matchings]
        assert partners == [1, 1, 3, 5, 5]

        circle, dots, coords = make_circle_points(2 * N, radius=RADIUS, center=CENTER)
        labels = label_points(coords, CENTER, buff=0.32)
        self.say("圓周上 ", "$2n$", " 個點，用 ", "$n$", " 條弦兩兩配對，弦不可以互相交叉")
        self.play(ShowCreation(circle), FadeIn(dots), FadeIn(labels), run_time=1.0)

        good = VGroup(*[make_block(p, coords, color=CATALAN_COLOR) for p in GOOD])
        self.play(LaggedStart(*[ShowCreation(c) for c in good], lag_ratio=0.3), run_time=1.2)
        ok = zh("不交叉", font_size=28, color=CATALAN_COLOR).next_to(circle, DOWN, buff=0.3)
        self.play(FadeIn(ok), run_time=0.4)
        self.wait(0.6)
        bad = VGroup(*[make_block(p, coords, color=CROSSING_COLOR) for p in BAD])
        hit = chords_intersection(coords, BAD[0], BAD[1])
        no = zh("交叉：不算", font_size=28, color=CROSSING_COLOR).move_to(ok)
        self.play(FadeOut(good), FadeOut(ok), run_time=0.4)
        self.play(ShowCreation(bad), FadeIn(no), Flash(hit, color=CROSSING_COLOR, flash_radius=0.4), run_time=1.0)
        self.wait(0.6)
        self.play(FadeOut(bad), FadeOut(no), run_time=0.4)

        # 五種（n = 3）
        xs = np.linspace(0.0, 6.0, 5)
        thumbs = VGroup(*[matching_item(t, radius=0.52) for t in trees])
        for x, th in zip(xs, thumbs):
            th.move_to(np.array([x, 1.85, 0.0]))
        self.say("6 個點的不交叉完美配對有 5 種：", "$C_3=5$", "（這就是 Motzkin 的結果）")
        self.play(LaggedStart(*[FadeIn(th, scale=0.7) for th in thumbs], lag_ratio=0.2), run_time=1.6)
        self.wait(1.0)

        # ------------------------------------------------------------ 固定一點
        root_dot = dots[0]
        self.say("固定一個點（1 號，橘色）：它一定和某一點配成一對")
        self.play(root_dot.animate.set_fill(ROOT_COLOR).scale(1.7),
                  Flash(coords[0], color=ROOT_COLOR, flash_radius=0.35), run_time=0.9)
        self.wait(0.5)

        # 配到奇數號（3 號、5 號）不行：兩邊會剩奇數個點
        odd_try = make_block((0, 2), coords, color=CROSSING_COLOR)
        odd_note = mixed("配 3 號：一邊剩 1 個點、一邊剩 3 個點，一定有點配不到", font_size=24,
                         color=CROSSING_COLOR)
        odd_note.move_to(np.array([3.0, 0.45, 0.0]))
        self.say("它不能配 3 號或 5 號：那樣弦的兩側各剩奇數個點，一定有點配不到")
        self.play(ShowCreation(odd_try), FadeIn(odd_note), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(odd_try), FadeOut(odd_note), run_time=0.4)

        # 右邊的式子
        lhs = Tex("C_3=", font_size=46)
        terms = [catalan_product_tex(k, N - 1 - k, font_size=46) for k in range(N)]
        pluses = [Tex("+", font_size=46) for _ in range(N - 1)]
        pieces = [lhs]
        for k in range(N):
            pieces.append(terms[k])
            if k < N - 1:
                pieces.append(pluses[k])
        equation = VGroup(*pieces).arrange(RIGHT, buff=0.2).move_to(np.array([2.9, 0.35, 0.0]))
        self.play(FadeIn(lhs), run_time=0.4)

        root_chord, regions, region_labels = None, None, None
        for k, q in enumerate([1, 3, 5]):
            inside = q - 1                    # 弦內側的點數 = 2k
            new_chord = make_block((0, q), coords, color=ROOT_COLOR, stroke_width=7)
            new_regions = VGroup(
                circular_segment(0, q, 2 * N, RADIUS, CENTER, color=LEFT_COLOR, opacity=0.3),
                circular_segment(q, 0, 2 * N, RADIUS, CENTER, color=RIGHT_COLOR, opacity=0.3),
            )
            new_regions.set_z_index(-1)
            labs = VGroup()
            for reg, text, color in ((new_regions[0], f"C_{{{k}}}", LEFT_COLOR),
                                     (new_regions[1], f"C_{{{N - 1 - k}}}", RIGHT_COLOR)):
                lab = Tex(text, font_size=36, fill_color=color)
                direction = normalize(reg.arc_mid - CENTER)
                depth = 0.55 if reg.steps >= 3 else -0.35          # 太窄的區域把標籤放到圓外
                lab.move_to(reg.arc_mid - depth * direction)
                labs.add(lab)
            if root_chord is None:
                self.play(ShowCreation(new_chord), dots[q].animate.set_fill(ROOT_COLOR), run_time=0.7)
                self.play(FadeIn(new_regions), FadeIn(labs), run_time=0.7)
                root_chord, regions, region_labels = new_chord, new_regions, labs
            else:
                prev_q = [1, 3, 5][k - 1]
                self.play(Transform(root_chord, new_chord), Transform(regions, new_regions),
                          Transform(region_labels, labs), dots[prev_q].animate.set_fill(WHITE),
                          dots[q].animate.set_fill(ROOT_COLOR), run_time=1.0)
            self.say(f"配 {q + 1} 號：弦內側 {inside} 個點（", f"$C_{{{k}}}$", f" 種），外側 {2 * N - 2 - inside} 個點（",
                     f"$C_{{{N - 1 - k}}}$", " 種），兩側各自獨立")
            anims = [TransformFromCopy(region_labels, terms[k])]
            if k > 0:
                anims.append(FadeIn(pluses[k - 1]))
            self.play(*anims, run_time=0.9)
            self.wait(0.9)

        values = [catalan(k) * catalan(N - 1 - k) for k in range(N)]
        total = Tex("=" + "+".join(str(v) for v in values) + f"={sum(values)}", font_size=46, fill_color=YELLOW)
        total.next_to(equation, DOWN, buff=0.35).align_to(equation, LEFT).shift(0.95 * RIGHT)
        self.play(Write(total), run_time=1.0)
        assert sum(values) == catalan(N)

        # 縮圖也依「1 號配到誰」上色、分組
        colored = VGroup(*[matching_item(t, radius=0.52, colored=True) for t in trees])
        for c, th in zip(colored, thumbs):
            c.move_to(th)
        self.say("上面的 5 種，依 1 號配到誰分成 2 + 1 + 2")
        self.play(*[Transform(th, c) for th, c in zip(thumbs, colored)], run_time=1.0)
        frames = VGroup(
            SurroundingRectangle(VGroup(thumbs[0], thumbs[1]), buff=0.12, color=GREY_C, stroke_width=1.5),
            SurroundingRectangle(thumbs[2], buff=0.12, color=GREY_C, stroke_width=1.5),
            SurroundingRectangle(VGroup(thumbs[3], thumbs[4]), buff=0.12, color=GREY_C, stroke_width=1.5),
        )
        self.play(LaggedStart(*[ShowCreation(f) for f in frames], lag_ratio=0.25), run_time=1.0)
        self.wait(1.2)

        # ------------------------------------------------------------ 重點
        key = VGroup(
            mixed("固定一個點：它所在的那一組（一條弦）", font_size=26),
            mixed("把其餘的點分成 ", "$2$", " 個獨立的區域", font_size=26),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        key_box = SurroundingRectangle(key, buff=0.2, color=YELLOW, stroke_width=3)
        VGroup(key, key_box).move_to(np.array([2.9, -1.95, 0.0]))
        self.play(FadeIn(key), ShowCreation(key_box), run_time=0.9)
        self.say("Chu 的證明就是這個想法：一組有 ", "$v_i$", " 個點時，會分成 ", "$v_i$", " 個區域")
        self.wait(3.0)
