"""
Scene N04 —— 循環引理（定理 2.1）：Raney 的證明（Raney 導讀第 5 節；原文 pp. 442–443）
執行（在 codes/ 內）：manimgl scenes/sceneN04_raney_proof.py SceneN04RaneyProof

σ = 0020030（秩 −2，就是 Chu 講義第 7.2 節的路徑倒過來）。
0. 7 個循環變形的秩路徑：k = 2、5 是 2 字列（路徑停在 −2 之上直到最後）。
1. 第 1 步：把符號排在圓周上；α = 總秩最大的一段弧（同秩取最長）= 「3」，秩 2。
2. 第 2 步：從 α 開始讀 σ₁ = σg₅ = 3000200：每個真開頭的秩都 > −2（兩種情形都和 α 的選法矛盾）。
3. 第 3 步：取最短的秩 −1 開頭切成 3000 | 200，輪換得 σg₅ 與 σg₂。
4. 第 4 步：從字的中間開始（例 k = 3：σg₃ = 00|3000|2，δ = 2 的秩 ≥ 0）一定提早掉到 −2。
5. 細節：200200 的 k = 0 與 k = 3 給出同一個字串——定理數的是 k。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import cyclic_variant, head_ranks, list_shifts, raney_proof_trace, rank
from utils.raney_draw import level_line, rank_walk, symbol_color, word_tiles
from utils.scene_base import ChuScene
from utils.styles import mixed, zh

SIGMA = (0, 0, 2, 0, 0, 3, 0)
M = len(SIGMA)
TRACE = raney_proof_trace(SIGMA)
DUP = (2, 0, 0, 2, 0, 0)


def check_math():
    assert rank(SIGMA) == -2 and list_shifts(SIGMA) == [2, 5]
    assert TRACE["alpha"] == (3,) and TRACE["k1"] == 5 and TRACE["sigma1"] == (3, 0, 0, 0, 2, 0, 0)
    assert TRACE["words"] == [(3, 0, 0, 0), (2, 0, 0)] and TRACE["rotations"][1] == (2, 0, 0, 3, 0, 0, 0)
    assert cyclic_variant(SIGMA, 3) == (0, 0, 3, 0, 0, 0, 2) and head_ranks(cyclic_variant(SIGMA, 3))[6] == -3
    assert min(head_ranks(TRACE["sigma1"])[:-1]) > -2
    assert list_shifts(DUP) == [0, 3] and cyclic_variant(DUP, 3) == DUP


def walk_cell(s, n, unit=0.2):
    w = rank_walk(s, unit=unit, stroke_width=4, dot_radius=0.03)
    return VGroup(level_line(w, 0, 0, len(s)), level_line(w, -n, 0, len(s), color=MAROON_B), w), w


class SceneN04RaneyProof(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N04　循環引理：Raney 的證明")

        # 0. 七個循環變形
        tiles = word_tiles(SIGMA, size=0.5, font_size=28).move_to(2.6 * UP)
        self.say("$\\sigma=0020030$", "，秩 ", "$-2$", "：7 種循環讀法中有幾種是 2 字列？")
        self.play(FadeIn(tiles))
        cells = VGroup()
        for k in range(M):
            v = cyclic_variant(SIGMA, k)
            g, w = walk_cell(v, 2)
            g.shift(np.array([-6.3 + 1.85 * k, 0.6, 0]) - w.vertex(0))      # 起點對齊：基線在同一高度
            ok = k in list_shifts(SIGMA)
            lab = Tex("k=%d" % k, font_size=24).move_to(np.array([g.get_center()[0], -0.75, 0]))
            mark = Tex(r"\checkmark" if ok else r"\times", font_size=30, fill_color=GREEN if ok else RED)
            mark.next_to(lab, DOWN, buff=0.12)
            cells.add(VGroup(g, lab, mark))
        assert_in_frame(cells)
        self.play(LaggedStartMap(FadeIn, VGroup(*[c[0] for c in cells]), lag_ratio=0.12), run_time=2.2)
        self.play(LaggedStartMap(FadeIn, VGroup(*[VGroup(c[1], c[2]) for c in cells]), lag_ratio=0.12), run_time=1.5)
        self.say("恰有 2 種（", "$k=2,5$", "）：路徑停在 ", "$-2$", " 之上，最後一步才碰到")
        self.wait(2.5)
        self.play(FadeOut(cells), tiles.animate.move_to(np.array([-3.8, 2.6, 0])))

        # 1. 圓周上最大的弧
        R = 1.6
        C = np.array([-3.8, 0.0, 0])
        ang = [PI / 2 - TAU * j / M for j in range(M)]
        ring = VGroup()
        for j, x in enumerate(SIGMA):
            sq = Square(side_length=0.5, stroke_color=symbol_color(x), stroke_width=3, fill_color=symbol_color(x), fill_opacity=0.2)
            sq.move_to(C + R * np.array([np.cos(ang[j]), np.sin(ang[j]), 0]))
            ring.add(VGroup(sq, Tex(str(x), font_size=28).move_to(sq)))
        circ = Circle(radius=R, stroke_color=GREY_D, stroke_width=2).move_to(C)
        idx = [Tex(str(j), font_size=20, fill_color=GREY_B).move_to(C + (R + 0.48) * np.array([np.cos(ang[j]), np.sin(ang[j]), 0]))
               for j in range(M)]
        alpha_box = SurroundingRectangle(ring[5], color=YELLOW, buff=0.08)
        step1 = VGroup(
            zh("第 1 步：在所有循環變形的所有開頭中", font_size=26, color=YELLOW),
            zh("取秩最大的；一樣大取最長的，叫它 α", font_size=26),
            zh("＝ 圓周上總秩最大的一段弧", font_size=26),
            mixed("這裡 ", "$\\alpha=3$", "，秩 ", "$2$", "（再長都會被 0 拉低）", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(np.array([2.6, 0.4, 0]))
        assert_in_frame(ring, step1, *idx)
        assert_apart(ring, step1)
        self.say("Raney 的證明：先在圓周上找「總秩最大的一段」")
        self.play(FadeOut(tiles), ShowCreation(circ), LaggedStartMap(FadeIn, ring, lag_ratio=0.1), *[FadeIn(i) for i in idx])
        self.play(FadeIn(step1[:3]), run_time=1.5)
        self.play(ShowCreation(alpha_box), FadeIn(step1[3]))
        self.wait(2.5)

        # 2. 從 α 開始讀
        self.play(FadeOut(step1))
        s1 = TRACE["sigma1"]
        g1, w1 = walk_cell(s1, 2, unit=0.45)
        g1.move_to(np.array([2.4, 0.9, 0]))
        shade = Rectangle(width=0.45, height=g1.get_height() + 0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.15)
        shade.move_to(np.array([w1.vertex(0)[0] + 0.225, g1.get_center()[1], 0]))
        t1 = word_tiles(s1, size=0.42, font_size=24).next_to(g1, UP, buff=0.35)
        lab1 = mixed("$\\sigma_1=\\sigma g_5$", font_size=28).next_to(t1, LEFT, buff=0.3)
        step2 = VGroup(
            zh("第 2 步：從 α 開始讀，每個真開頭的秩都 > −2", font_size=24, color=YELLOW),
            mixed("若某個 ", "$\\tau$", " 的秩 ", "$\\le-2$", "：比 ", "$\\alpha$", " 短 ", "$\\Rightarrow$", " 剩下的一段比 ", "$\\alpha$", " 大", font_size=22),
            mixed("比 ", "$\\alpha$", " 長 ", "$\\Rightarrow$", " 後面一段接上 ", "$\\alpha$", " 一樣大又更長", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(g1, DOWN, buff=0.45)
        assert_in_frame(g1, t1, lab1, step2)
        assert_apart(ring, VGroup(lab1, step2))
        self.say("從 ", "$\\alpha$", " 開始讀一圈：", "$\\sigma_1=\\sigma g_5=3000200$")
        self.play(FadeIn(t1), FadeIn(lab1), FadeIn(shade), FadeIn(g1), run_time=1.5)
        self.play(FadeIn(step2), run_time=1.5)
        self.wait(3)

        # 3. 切成字、輪換
        self.play(FadeOut(step2))
        cutx = (t1[3].get_right()[0] + t1[4].get_left()[0]) / 2
        cut = DashedLine(np.array([cutx, t1.get_top()[1] + 0.12, 0]), np.array([cutx, t1.get_bottom()[1] - 0.12, 0]),
                         stroke_color=YELLOW, stroke_width=4)
        dot = Dot(w1.vertex(4), radius=0.08, fill_color=MAROON_B).set_z_index(3)
        step3 = VGroup(
            zh("第 3 步：取最短的、秩為 −1 的開頭，一個一個切", font_size=24, color=YELLOW),
            mixed("$\\sigma_1=3000\\mid 200$", "，輪換：", "$200\\mid3000=\\sigma g_2$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(g1, DOWN, buff=0.45)
        assert_in_frame(step3)
        self.say("第 3 步：切成 2 個字，把它們輪流放到最前面")
        self.play(ShowCreation(cut), FadeIn(dot))
        self.play(FadeIn(step3), run_time=1.5)
        self.wait(2.5)

        # 4. 沒有別的
        self.play(FadeOut(VGroup(step3, t1, lab1, shade, g1, cut, dot)))
        v3 = cyclic_variant(SIGMA, 3)
        g3, w3 = walk_cell(v3, 2, unit=0.45)
        g3.move_to(np.array([2.4, 0.6, 0]))
        t3 = word_tiles(v3, size=0.42, font_size=24, sep_after=(1, 5)).next_to(g3, UP, buff=0.35)
        lab3 = mixed("$\\sigma g_3$", font_size=28).next_to(t3, LEFT, buff=0.3)
        bad = Dot(w3.vertex(6), radius=0.09, fill_color=RED).set_z_index(3)
        step4 = VGroup(
            zh("第 4 步：從字的中間開始讀就不行", font_size=24, color=YELLOW),
            mixed("$\\sigma g_3=\\beta\\gamma\\delta=00\\mid3000\\mid2$", "，", "$\\delta\\beta=200$", " 是字", font_size=24),
            mixed("$r(\\delta)\\ge0\\Rightarrow r(\\beta\\gamma)\\le-2$", "：提早碰到 ", "$-2$", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(g3, DOWN, buff=0.4)
        assert_in_frame(g3, t3, step4, lab3)
        self.say("其他的 ", "$k$", " 都從某個字的中間開始讀")
        self.play(FadeIn(t3), FadeIn(lab3), FadeIn(g3), run_time=1.2)
        self.play(FadeIn(bad, scale=1.6), FadeIn(step4), run_time=1.5)
        self.wait(3)

        # 5. 數的是 k
        self.play(FadeOut(VGroup(step4, t3, lab3, g3, bad, ring, circ, alpha_box, *idx)))
        dup = VGroup(word_tiles(DUP, size=0.5, font_size=28),
                     mixed("$k=0$", " 與 ", "$k=3$", " 讀出同一個字串 ", "$200200$", font_size=28),
                     mixed("定理說的是「恰有 ", "$n$", " 個 ", "$k$", "」，雙重計數數的是（字串, ", "$k$", "）的配對", font_size=28)
                     ).arrange(DOWN, buff=0.4).move_to(0.4 * UP)
        assert_in_frame(dup)
        self.say("一個細節：輪換出來的字串可能重複")
        self.play(FadeIn(dup[0]))
        self.play(FadeIn(dup[1]))
        self.play(FadeIn(dup[2]))
        self.wait(3)
