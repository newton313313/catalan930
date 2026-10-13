"""
Scene 00b —— 凸多邊形的三角剖分：T_3=1, T_4=2, T_5=5, T_6=14（來源論文 Fig. 2.1）

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00b_triangulation.py Scene00bTriangulation
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import CATALAN_COLOR, TriangulationMob
from utils.circle_points import chords_intersection
from utils.counting import catalan, triangulations
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, YELLOW, mixed

TABLE_X = 4.85
BIG_CENTER = np.array([-2.4, 0.35, 0.0])


def table_row(m: int, y: float) -> Tex:
    n = m - 2
    row = Tex(f"T_{{{m}}}={catalan(n)}=C_{{{n}}}", font_size=46, t2c={f"C_{{{n}}}": CATALAN_COLOR})
    row.move_to(np.array([TABLE_X, y, 0.0]))
    return row


def diag_lines(tm: TriangulationMob, diags, width: float = 5.5) -> VGroup:
    return VGroup(*[Line(tm.vertex(a), tm.vertex(b), stroke_color=CATALAN_COLOR, stroke_width=width)
                    for a, b in diags])


class Scene00bTriangulation(ChuScene):
    def construct(self):
        self.show_header("凸多邊形的三角剖分")
        tris = {m: triangulations(m) for m in (3, 4, 5, 6)}
        assert [len(tris[m]) for m in (3, 4, 5, 6)] == [1, 2, 5, 14]

        t_def = mixed("$T_m$", "：凸 ", "$m$", " 邊形的三角剖分數", font_size=26, color=MUTED_COLOR)
        t_def.move_to(np.array([TABLE_X, 2.55, 0.0]))
        row_ys = {3: 1.7, 4: 0.85, 5: 0.0, 6: -0.85}

        # ------------------------------------------------------------ 三角形
        tri = TriangulationMob(3, [], radius=1.5, center=BIG_CENTER, edge_width=4, dot_radius=0.07)
        self.say("三角剖分：用互不相交的對角線，把凸多邊形切成三角形")
        self.play(ShowCreation(tri.outline), FadeIn(tri.dots), run_time=1.0)
        fill = tri.region([0, 1, 2], CATALAN_COLOR, 0.25)
        self.play(FadeIn(fill), FadeIn(t_def), run_time=0.7)
        self.say("三角形本身就是一個三角形：只有 1 種")
        row3 = table_row(3, row_ys[3])
        self.play(FadeIn(row3, shift=0.3 * LEFT), run_time=0.7)
        self.wait(1.0)

        # ------------------------------------------------------------ 正方形
        sq = TriangulationMob(4, [], radius=1.5, center=BIG_CENTER, edge_width=4, dot_radius=0.07)
        self.play(FadeOut(fill), ReplacementTransform(tri.outline, sq.outline),
                  ReplacementTransform(tri.dots, sq.dots), run_time=1.0)
        d1, d2 = diag_lines(sq, [(0, 2)])[0], diag_lines(sq, [(1, 3)])[0]
        self.say("正方形：畫一條對角線，就切成兩個三角形")
        self.play(ShowCreation(d1), run_time=0.8)
        self.wait(0.6)
        self.say("兩條對角線同時畫會交叉，所以只能選一條")
        self.play(ShowCreation(d2), run_time=0.6)
        hit = chords_intersection([sq.vertex(i) for i in range(4)], (0, 2), (1, 3))
        ring = Circle(radius=0.2, stroke_color=CROSSING_COLOR, stroke_width=5).move_to(hit)
        self.play(ShowCreation(ring), Flash(hit, color=CROSSING_COLOR, flash_radius=0.35), run_time=0.8)
        self.play(FadeOut(ring), FadeOut(d1), run_time=0.5)
        # 換成結構相同的 TriangulationMob 再變形（[fills, outline, diagonals, dots] 一一對應）
        sq_b = TriangulationMob(4, [(1, 3)], radius=1.5, center=BIG_CENTER, edge_width=4,
                                diag_width=5.5, dot_radius=0.07)
        self.remove(sq.outline, sq.dots, d2)
        self.add(sq_b)
        thumb_a = TriangulationMob(4, [(0, 2)], radius=1.1, center=np.array([-4.3, 0.35, 0]),
                                   edge_width=3.5, diag_width=5, dot_radius=0.06)
        thumb_b = TriangulationMob(4, [(1, 3)], radius=1.1, center=np.array([-0.6, 0.35, 0]),
                                   edge_width=3.5, diag_width=5, dot_radius=0.06)
        self.play(ReplacementTransform(sq_b, thumb_b), FadeIn(thumb_a, shift=0.5 * RIGHT), run_time=1.0)
        self.say("正方形有 2 種")
        row4 = table_row(4, row_ys[4])
        self.play(FadeIn(row4, shift=0.3 * LEFT), run_time=0.7)
        self.wait(1.0)

        # ------------------------------------------------------------ 五邊形
        big_center = np.array([-4.5, 0.85, 0.0])
        pent = TriangulationMob(5, [], radius=1.3, center=big_center, edge_width=4, dot_radius=0.07)
        self.play(FadeOut(thumb_a), FadeOut(thumb_b.diagonals),
                  ReplacementTransform(thumb_b.outline, pent.outline),
                  ReplacementTransform(thumb_b.dots, pent.dots), run_time=1.0)
        self.remove(pent.outline, pent.dots)
        self.add(pent)
        self.say("五邊形：每一種用 2 條對角線，切成 3 個三角形")
        xs = np.linspace(-6.2, 1.4, 5)
        thumbs5 = VGroup()
        current = None
        for j, diags in enumerate(tris[5]):
            new = diag_lines(pent, diags)
            if current is None:
                self.play(ShowCreation(new), run_time=0.7)
                current = new
            else:
                self.play(Transform(current, new), run_time=0.6)
            thumb = TriangulationMob(5, diags, radius=0.58, center=np.array([xs[j], -1.75, 0]),
                                     edge_width=2.5, diag_width=4, dot_radius=0.045)
            ghost = TriangulationMob(5, diags, radius=1.3, center=big_center, edge_width=4,
                                     diag_width=5.5, dot_radius=0.07)
            self.play(TransformFromCopy(ghost, thumb), run_time=0.6)
            thumbs5.add(thumb)
        self.say("五邊形有 5 種")
        row5 = table_row(5, row_ys[5])
        self.play(FadeIn(row5, shift=0.3 * LEFT), run_time=0.7)
        self.wait(1.0)

        # ------------------------------------------------------------ 六邊形：14 種
        self.play(FadeOut(VGroup(pent, current, thumbs5)), run_time=0.7)
        gallery = VGroup()
        for j, diags in enumerate(tris[6]):
            r, c = divmod(j, 7)
            center = np.array([-6.35 + 1.28 * c, 1.1 - 1.5 * r, 0.0])
            gallery.add(TriangulationMob(6, diags, radius=0.5, center=center, edge_width=2.2,
                                         diag_width=3.5, dot_radius=0.04))
        self.say("六邊形：每一種用 3 條對角線，切成 4 個三角形")
        self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in gallery], lag_ratio=0.12), run_time=3.0)
        count = Tex("14", font_size=40, fill_color=YELLOW).next_to(gallery, DOWN, buff=0.3)
        self.play(FadeIn(count, scale=1.4), run_time=0.5)
        self.say("六邊形有 14 種")
        row6 = table_row(6, row_ys[6])
        self.play(FadeIn(row6, shift=0.3 * LEFT), run_time=0.7)
        self.wait(1.0)

        # ------------------------------------------------------------ 規律
        table = VGroup(row3, row4, row5, row6)
        summary = VGroup(
            mixed("凸 ", "$(n+2)$", " 邊形有", font_size=28),
            mixed("$C_n$", " 種三角剖分", font_size=28, t2c={"C_n": CATALAN_COLOR}),
        ).arrange(DOWN, buff=0.15)
        summary_box = SurroundingRectangle(summary, buff=0.2, color=YELLOW, stroke_width=3)
        VGroup(summary, summary_box).move_to(np.array([TABLE_X, -2.15, 0.0]))
        self.play(LaggedStart(*[Indicate(r, scale_factor=1.12, color=YELLOW) for r in table], lag_ratio=0.25),
                  run_time=1.6)
        self.say("規律：多邊形的頂點數比卡塔蘭數的編號多 2")
        self.play(FadeIn(summary), ShowCreation(summary_box), run_time=1.0)
        self.wait(1.5)
        self.say("為什麼剛好是卡塔蘭數？下一段用「固定一條邊」來看")
        self.wait(2.5)
