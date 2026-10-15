"""
Scene N08 —— 大代數與 L*（Raney 導讀第 7–8 節；原文 §3–§4，pp. 444–446）
執行（在 codes/ 內）：manimgl scenes/sceneN08_lstar.py SceneN08LStar

1. A^P：每種元數一個變數 E₁, E₂, E₃, …（E_i 讀成「一個 i 元節點」），E₀ = 1。
2. L* = Σ L(1; p̄) E^p̄ ＝ 所有樹的生成函數：1 + E₁ + (E₁² + E₂) + (E₁³ + 3E₁E₂ + E₃) + …
3. 定理 4.1：(L*)ⁿ 數 n 字列；L* = Σ E_i (L*)^i（樹 = 葉子，或 i 元的根接 i 棵子樹）。
   驗算 E₁E₂ 的係數：3 = 1（1200）+ 2（2010、2100）。
4. 代換（誘導同態 H）：E_i ↦ x^i（依邊數）得 T = 1 + xT²，e 條邊的平面樹有 C_e 棵；
   E_i ↦ x（依節點數）不行：只有一個內部節點的樹就有無限多棵；
   E_{v_i} ↦ x_i（Chu）：(4.1) → Chu 原文 (6)，定理 4.1 + 2.2 → (8)，定理 2.3 → (9)，定理 2.4 → (10)。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import L_formula, lists_with, lstar_coeffs, mv_pow
from utils.raney_draw import WordTreeMob, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh


def check_math():
    Ls = lstar_coeffs(4, 4)
    assert Ls[(1, 1, 0, 0)] == 3 and Ls[(2, 1, 0, 0)] == 6 and Ls[(0, 2, 0, 0)] == 2 and Ls[(1, 0, 1, 0)] == 4
    assert lists_with(1, (0, 1)) == [(2, 0, 0)] and lists_with(2, (1,)) == [(0, 1, 0), (1, 0, 0)]
    assert L_formula(1, (0, 1)) + L_formula(2, (1,)) == 3
    for e in range(6):
        assert sum(v for p, v in lstar_coeffs(5, 5).items() if sum(i * c for i, c in enumerate(p, 1)) == e) == catalan(e)
    assert mv_pow(lstar_coeffs(3, 3), 2, 3, 3)[(1, 0, 0)] == 2


class SceneN08LStar(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N08　大代數與 L*：樹的萬用方程")

        # 1–2. 變數與 L*
        vars_ = VGroup(*[VGroup(WordTreeMob(w, x_gap=0.3, y_gap=0.38), Tex(t, font_size=34))
                         .arrange(DOWN, buff=0.2) for w, t in
                         [((0,), r"E_0=1"), ((1, 0), r"E_1"), ((2, 0, 0), r"E_2"), ((3, 0, 0, 0), r"E_3")]])
        vars_.arrange(RIGHT, buff=0.9, aligned_edge=DOWN).move_to(np.array([0, 1.9, 0]))
        dots = Tex(r"\cdots", font_size=40).next_to(vars_, RIGHT, buff=0.4)
        self.say("Raney 的「大代數」：每種元數一個變數，", "$E_i$", " 讀成「一個 ", "$i$", " 元節點」")
        self.play(LaggedStartMap(FadeIn, vars_, lag_ratio=0.25), FadeIn(dots), run_time=2)
        self.wait(1)
        ls = Tex(r"L^*=\sum_{\bar p}L(1;\bar p)\,E_1^{p_1}E_2^{p_2}\cdots", font_size=40)
        ser = Tex(r"=1+E_1+\big(E_1^2+E_2\big)+\big(E_1^3+3E_1E_2+E_3\big)+\big(E_1^4+6E_1^2E_2+2E_2^2+4E_1E_3+E_4\big)+\cdots",
                  font_size=30)
        VGroup(ls, ser).arrange(DOWN, buff=0.3).move_to(np.array([0, -0.2, 0]))
        assert_in_frame(vars_, dots, ls, ser)
        self.say("$L^*$", " 是所有樹的生成函數：係數 ", "$=$", " 有幾個這種組成的字")
        self.play(Write(ls), run_time=1.5)
        self.play(FadeIn(ser), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(VGroup(vars_, dots, ls, ser)))

        # 3. 定理 4.1
        thm = VGroup(zh("定理 4.1", font_size=32, color=YELLOW),
                     mixed("$(L^*)^n$", " 的係數 ", "$=L(n;\\bar p)$", "：", "$n$", " 次方數的是 ", "$n$", " 字列", font_size=28),
                     Tex(r"L^*=\sum_{i\ge0}E_i\,(L^*)^i=1+E_1L^*+E_2(L^*)^2+E_3(L^*)^3+\cdots", font_size=36),
                     ).arrange(DOWN, buff=0.3)
        box = boxed(thm, color=YELLOW).move_to(np.array([0, 1.8, 0]))
        meaning = mixed("一棵樹 ", "$=$", " 一片葉子，或一個 ", "$i$", " 元的根接上 ", "$i$", " 棵子樹", font_size=28).next_to(box, DOWN, buff=0.35)
        chk = VGroup(
            mixed("驗算 ", "$E_1E_2$", " 的係數 3：", font_size=26),
            VGroup(Tex(r"E_1\cdot L^*", font_size=30), Tex(r":", font_size=30), word_tiles((1, 2, 0, 0), size=0.36, font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Tex(r"E_2\cdot (L^*)^2", font_size=30), Tex(r":", font_size=30), word_tiles((2, 0, 1, 0), size=0.36, font_size=22),
                   word_tiles((2, 1, 0, 0), size=0.36, font_size=22)).arrange(RIGHT, buff=0.15),
            Tex(r"3=1+2", font_size=34),
        ).arrange(DOWN, buff=0.22).next_to(meaning, DOWN, buff=0.4)
        assert_in_frame(box, meaning, chk)
        self.say("定理 2.3 ", "$\\Rightarrow$", " 冪次數字列；定理 2.4 ", "$\\Rightarrow$", " 不動點方程")
        self.play(FadeIn(box, shift=0.2 * UP), run_time=1.5)
        self.play(FadeIn(meaning))
        self.wait(1.5)
        self.play(LaggedStartMap(FadeIn, chk, lag_ratio=0.4), run_time=2.5)
        self.wait(2.5)
        self.play(FadeOut(VGroup(box, meaning, chk)))

        # 4. 代換
        self.say("Raney 的同態 ", "$H$", "：把每個 ", "$E_i$", " 換成別的東西（先算好、再代換）")
        rows = VGroup(
            VGroup(Tex(r"E_i\mapsto x^i", font_size=34), zh("依邊數：", font_size=26),
                   Tex(r"T=1+xT+x^2T^2+\cdots=\frac{1}{1-xT}\ \Rightarrow\ T=1+xT^2", font_size=30)),
            VGroup(Tex(r"E_i\mapsto x", font_size=34), zh("依節點數：", font_size=26),
                   mixed("不行！只有一個內部節點的樹 ", "$10,\\,200,\\,3000,\\ldots$", " 就有無限多棵", font_size=26)),
            VGroup(Tex(r"E_{v_i}\mapsto x_i", font_size=34), zh("Chu：", font_size=26),
                   Tex(r"D=1+x_1D^{v_1}+\cdots+x_kD^{v_k}", font_size=32)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.35)
        rows.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(np.array([0, 1.0, 0]))
        cat = mixed("$e$", " 條邊的平面樹有 ", "$C_e$", " 棵：", "$1,1,2,5,14,\\ldots$", font_size=24, color=GREY_A)
        cat.next_to(rows[0][2], DOWN, buff=0.1, aligned_edge=LEFT)
        rows[1][2][1].set_color(RED_B)
        assert_in_frame(rows, cat)
        for k, r in enumerate(rows):
            self.play(FadeIn(r, shift=0.2 * RIGHT), run_time=1.0)
            if k == 0:
                self.play(FadeIn(cat))
            self.wait(1.5)
        chu = VGroup(
            zh("Chu 的第三步 ＝ Raney 定理 4.1 在這個代換下的影像", font_size=28, color=YELLOW),
            mixed("(4.1) ", "$\\to$", " Chu (6)；定理 4.1＋2.2 ", "$\\to$", " (8)；定理 2.3 ", "$\\to$", " (9)；定理 2.4 ", "$\\to$", " (10)",
                  font_size=26),
        ).arrange(DOWN, buff=0.25).move_to(np.array([0, -2.1, 0]))
        assert_in_frame(chu)
        assert_apart(chu, VGroup(rows, cat))
        self.say("Chu 1987 的貢獻：把這些係數解釋成圓周上的不交叉分法")
        self.play(FadeIn(chu), run_time=1.5)
        self.wait(3.5)
