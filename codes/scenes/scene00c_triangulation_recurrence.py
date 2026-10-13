"""
Scene 00c —— 用三角剖分推出卡塔蘭數的遞迴（Segner 遞迴）：
    C_n = sum_{k=0}^{n-1} C_k C_{n-1-k},  C_0 = 1

固定底邊 -> 含底邊的三角形（根）-> 左、右兩個獨立的小多邊形。
這和之後 Chu 的「固定一點 -> v_i 個獨立區域」是同一個想法（這裡是 2 個區域）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00c_triangulation_recurrence.py Scene00cTriangulationRecurrence
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    LEFT_COLOR,
    RIGHT_COLOR,
    TriangulationMob,
    catalan_product_tex,
    triangulation_item,
)
from utils.counting import binary_trees, catalan, triangulation_apex, triangulations
from utils.scene_base import ChuScene
from utils.styles import ROOT_COLOR, YELLOW, mixed, zh

N = 4                       # 六邊形 = 凸 (n+2) 邊形，n = 4
M = N + 2
HEX_CENTER = np.array([-4.3, -0.35, 0.0])
HEX_RADIUS = 1.75
EXAMPLES = [0, 6, 13]       # 先展示的三種三角剖分（第三個頂點分別是 1、2、4）


def polygon_centroid(tm: TriangulationMob, indices) -> np.ndarray:
    return np.mean([tm.vertex(i) for i in indices], axis=0)


class Scene00cTriangulationRecurrence(ChuScene):
    def construct(self):
        self.show_header("卡塔蘭數的遞迴")
        tris = triangulations(M)
        trees = binary_trees(N)
        apexes = [triangulation_apex(t, M) for t in trees]
        assert len(tris) == catalan(N) == 14
        assert [apexes.count(a) for a in (1, 2, 3, 4)] == [5, 2, 2, 5]

        hexagon = TriangulationMob(M, [], radius=HEX_RADIUS, center=HEX_CENTER, edge_width=4,
                                   dot_radius=0.075)
        self.play(ShowCreation(hexagon.outline), FadeIn(hexagon.dots), run_time=1.0)

        # ------------------------------------------------------------ 固定一條邊
        base = hexagon.edge(0, M - 1, color=ROOT_COLOR, width=9)
        base_tag = zh("底邊", font_size=26, color=ROOT_COLOR).next_to(base, DOWN, buff=0.18)
        self.say("先固定一條邊，叫它底邊")
        self.play(ShowCreation(base), FadeIn(base_tag), run_time=0.9)
        self.wait(0.6)

        # 每一種三角剖分裡，底邊恰好屬於一個三角形
        self.say("在每一種三角剖分裡，底邊恰好屬於一個三角形")
        shown = None
        for idx in EXAMPLES:
            a = apexes[idx]
            diags = VGroup(*[Line(hexagon.vertex(p), hexagon.vertex(q), stroke_color=CATALAN_COLOR,
                                  stroke_width=5) for p, q in tris[idx]])
            root = hexagon.region([0, a, M - 1], ROOT_COLOR, 0.5)
            new = VGroup(root, diags)
            if shown is None:
                self.play(ShowCreation(diags), run_time=0.8)
                self.play(FadeIn(root), run_time=0.5)
                shown = new
            else:
                self.play(Transform(shown, new), run_time=0.9)
            self.wait(0.6)
        self.play(FadeOut(shown), run_time=0.5)

        # ------------------------------------------------------------ 第三個頂點走過所有位置
        self.say("這個三角形的第三個頂點，可以是上面 4 個頂點中的任何一個")
        candidates = VGroup(*[hexagon.dots[a] for a in range(1, M - 1)])
        self.play(LaggedStart(*[Indicate(d, scale_factor=2.2, color=ROOT_COLOR) for d in candidates],
                              lag_ratio=0.25), run_time=1.6)

        # 右邊的式子：C_4 = C_0C_3 + C_1C_2 + C_2C_1 + C_3C_0
        lhs = Tex("C_4", "=", font_size=48)
        terms, pluses = [], []
        for k in range(N):
            term = VGroup(Tex(f"C_{{{k}}}", font_size=48, fill_color=LEFT_COLOR),
                          Tex(f"C_{{{N - 1 - k}}}", font_size=48, fill_color=RIGHT_COLOR))
            term.arrange(RIGHT, buff=0.05)
            terms.append(term)
            if k < N - 1:
                pluses.append(Tex("+", font_size=48))
        pieces = [lhs]
        for k in range(N):
            pieces.append(terms[k])
            if k < N - 1:
                pieces.append(pluses[k])
        equation = VGroup(*pieces).arrange(RIGHT, buff=0.2)
        equation.move_to(np.array([2.75, 2.15, 0.0]))
        self.play(FadeIn(lhs), run_time=0.5)

        values = []
        root_tri = None
        fills = None
        labels = None
        for k in range(N):
            a = k + 1
            left, right = list(range(0, a + 1)), list(range(a, M))
            new_root = hexagon.region([0, a, M - 1], ROOT_COLOR, 0.55)
            new_fills = VGroup()
            if len(left) >= 3:
                new_fills.add(hexagon.region(left, LEFT_COLOR, 0.35))
            if len(right) >= 3:
                new_fills.add(hexagon.region(right, RIGHT_COLOR, 0.35))
            # 標籤：左邊 C_k、右邊 C_{n-1-k}；退化成一條邊時放在那條邊外側
            def label_at(indices, text, color):
                lab = Tex(text, font_size=36, fill_color=color)
                if len(indices) >= 3:
                    lab.move_to(polygon_centroid(hexagon, indices))
                else:
                    mid = polygon_centroid(hexagon, indices)
                    lab.move_to(mid + 0.45 * normalize(mid - HEX_CENTER))
                return lab
            new_labels = VGroup(label_at(left, f"C_{{{k}}}", LEFT_COLOR),
                                label_at(right, f"C_{{{N - 1 - k}}}", RIGHT_COLOR))
            if root_tri is None:
                self.play(FadeIn(new_root), run_time=0.6)
                self.play(FadeIn(new_fills), FadeIn(new_labels), run_time=0.7)
                root_tri, fills, labels = new_root, new_fills, new_labels
            else:
                self.play(Transform(root_tri, new_root), FadeOut(fills), FadeOut(labels), run_time=0.8)
                self.play(FadeIn(new_fills), FadeIn(new_labels), run_time=0.6)
                fills, labels = new_fills, new_labels
            if k == 0:
                self.say("左邊只剩一條邊，算 1 種（", "$C_0=1$", "）；右邊是五邊形，", "$C_3$", " 種")
            elif k == 1:
                self.say("左邊是三角形（", "$C_1$", "），右邊是四邊形（", "$C_2$", "）：兩邊各自獨立，所以相乘")
            elif k == 2:
                self.say("左邊四邊形（", "$C_2$", "），右邊三角形（", "$C_1$", "）")
            else:
                self.say("左邊五邊形（", "$C_3$", "），右邊只剩一條邊（", "$C_0=1$", "）")
            anims = [TransformFromCopy(labels[0], terms[k][0]), TransformFromCopy(labels[1], terms[k][1])]
            if k > 0:
                anims.append(FadeIn(pluses[k - 1]))
            self.play(*anims, run_time=0.9)
            values.append(catalan(k) * catalan(N - 1 - k))
            self.wait(0.8)

        # 數值（第二列），總和（第三列），等號對齊
        eq_x = lhs[-1].get_center()[0]          # lhs 的最後一個 glyph 是「=」
        num_row = VGroup()
        num_row.add(Tex("=", font_size=48).move_to(np.array([eq_x, 1.3, 0.0])))
        for k in range(N):
            val = Tex(f"{catalan(k)}\\cdot {catalan(N - 1 - k)}", font_size=40)
            val.move_to(np.array([terms[k].get_center()[0], 1.3, 0.0]))
            num_row.add(val)
            if k < N - 1:
                num_row.add(Tex("+", font_size=40).move_to(np.array([pluses[k].get_center()[0], 1.3, 0.0])))
        total = Tex(f"={sum(values)}", font_size=48, fill_color=YELLOW)
        total.move_to(np.array([eq_x, 0.5, 0.0]), aligned_edge=LEFT)
        total.shift((eq_x - total[0].get_center()[0]) * RIGHT)
        assert sum(values) == catalan(N)
        self.say("第三個頂點的位置不同，就是不同的情況，所以相加")
        self.play(LaggedStart(*[FadeIn(m, shift=0.15 * DOWN) for m in num_row], lag_ratio=0.15), run_time=1.6)
        self.play(Write(total), run_time=0.8)
        self.wait(1.2)

        # ------------------------------------------------------------ 回頭看 14 種：5 + 2 + 2 + 5
        self.play(FadeOut(VGroup(hexagon, base, base_tag, root_tri, fills, labels)), run_time=0.7)
        groups = VGroup()
        for a in range(1, M - 1):
            k = a - 1
            thumbs = VGroup(*[triangulation_item(t, radius=0.36, colored=True, edge_width=1.8,
                                                 diag_width=2.6, dot_radius=0.028)
                              for t, ap in zip(trees, apexes) if ap == a])
            thumbs.arrange(RIGHT, buff=0.16)
            label = catalan_product_tex(k, N - 1 - k, f"={values[k]}", font_size=32)
            label.next_to(thumbs, UP, buff=0.18)
            frame = SurroundingRectangle(VGroup(label, thumbs), buff=0.14, color=GREY_C, stroke_width=1.5)
            groups.add(VGroup(frame, label, thumbs))
        row1 = VGroup(groups[0], groups[1]).arrange(RIGHT, buff=0.45)
        row2 = VGroup(groups[2], groups[3]).arrange(RIGHT, buff=0.45)
        VGroup(row1, row2).arrange(DOWN, buff=0.3).move_to(1.0 * DOWN)
        self.say("回頭看六邊形的 14 種三角剖分：依第三個頂點分組，正好是 5、2、2、5")
        self.play(LaggedStart(*[FadeIn(g, shift=0.2 * UP) for g in groups], lag_ratio=0.3), run_time=2.4)
        self.wait(2.5)

        # ------------------------------------------------------------ 一般的遞迴式
        self.play(FadeOut(groups), run_time=0.6)
        general = Tex(R"C_n=\sum_{k=0}^{n-1}C_kC_{n-1-k},\qquad C_0=1", font_size=56,
                      t2c={"C_k": LEFT_COLOR, "C_{n-1-k}": RIGHT_COLOR})
        general.move_to(0.25 * DOWN)
        box = SurroundingRectangle(general, buff=0.25, color=YELLOW, stroke_width=3)
        rules = VGroup(
            mixed("左右兩邊各自獨立 ", "$\\Rightarrow$", " 相乘", font_size=28),
            mixed("第三個頂點的位置不同 ", "$\\Rightarrow$", " 相加", font_size=28),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        rules.next_to(box, DOWN, buff=0.35)
        self.say("一般的凸 ", "$(n+2)$", " 邊形也一樣：這就是 Segner 的遞迴式")
        self.play(Write(general), run_time=1.6)
        self.play(ShowCreation(box), run_time=0.6)
        self.play(FadeIn(rules, shift=0.2 * UP), run_time=0.8)
        self.wait(1.5)
        self.say("「固定一個根，切成兩個獨立的小問題」：後面會一再看到這個結構")
        self.wait(3.0)
