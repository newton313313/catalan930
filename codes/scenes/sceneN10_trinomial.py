"""
Scene N10 —— 用級數解方程：三項式、Problem 4983、模 2（Raney 導讀第 3.3、10 節；原文 §6，pp. 448–449）
執行（在 codes/ 內）：manimgl scenes/sceneN10_trinomial.py SceneN10Trinomial

1. 代換 E_n ↦ x、其他 ↦ 0：w = 1 + x wⁿ 的解 w = Σ L(1; k d̄_n) x^k = Σ C(nk,k)/(1+(n−1)k) x^k（Fuss–Catalan 表）。
2. Problem 4983（Klamkin–Shepp 1961，Kelly 1962）：n 個因子、每次乘 r+1 個；r = 2：n = 4 不可能，n = 5 有 3 種；
   Kelly 的 y = x + y^{r+1} 由代換 E_{r+1} ↦ x^r、y = x·H(L*) 得到；P_n(r) = C((r+1)k, k)/n。
3. Etherington：P_n(r) ＝ 凸 (n+1) 邊形切成 (r+2) 邊形的方法數；六邊形切成兩個四邊形 3 種。
4. 模 2：c ≡ 1 + x c(x²)，所以 C_n 是奇數 ⇔ n = 2^j − 1（0, 1, 3, 7, 15）。
"""
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import L_formula, kelly_P, kelly_P_brute, lists_with, polygon_dissections_brute, trinomial_coeff
from utils.raney_draw import WordTreeMob
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

PRODUCTS = ["((abc)de)", "(a(bcd)e)", "(ab(cde))"]


def check_math():
    for n in (2, 3, 4):
        assert all(trinomial_coeff(n, k) == L_formula(1, tuple(k if i == n else 0 for i in range(1, n + 1))) for k in range(7))
    assert [trinomial_coeff(3, k) for k in range(7)] == [1, 1, 3, 12, 55, 273, 1428]
    assert kelly_P(4, 2) == 0 == kelly_P_brute(4, 2) and kelly_P(5, 2) == 3 == kelly_P_brute(5, 2)
    assert lists_with(1, (0, 0, 2)) == [(3, 0, 0, 3, 0, 0, 0), (3, 0, 3, 0, 0, 0, 0), (3, 3, 0, 0, 0, 0, 0)]
    assert polygon_dissections_brute(6, 4) == 3 == kelly_P(5, 2)
    assert [catalan(n) % 2 for n in range(16)] == [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]


class SceneN10Trinomial(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N10　用級數解方程：三項式、Problem 4983、模 2")

        # 1. 三項式
        eq = Tex(r"w=1+x\,w^{\,n}\qquad(E_n\mapsto x,\ \text{others}\mapsto0)", font_size=38).move_to(2.4 * UP)
        sol = Tex(r"w=\sum_{k\ge0}L(1;k\bar d_n)\,x^k=\sum_{k\ge0}\frac{1}{1+(n-1)k}\binom{nk}{k}x^k", font_size=38)
        sol.next_to(eq, DOWN, buff=0.4)
        rows = VGroup()
        for n in (2, 3, 4):
            vals = [trinomial_coeff(n, k) for k in range(7)]
            row = VGroup(Tex(r"n=%d" % n, font_size=30), *[Tex(str(v), font_size=30) for v in vals])
            for c, cell in enumerate(row):
                cell.move_to(np.array([-4.4 + 1.35 * c, 0, 0]))
            rows.add(row)
        rows.arrange(DOWN, buff=0.3).next_to(sol, DOWN, buff=0.5)
        note = mixed("Chu 講義的高階卡塔蘭數 ", "$C_k(n)$", "：字母對調（那裡 ", "$k$", " 是群組大小）", font_size=24, color=GREY_A)
        note.next_to(rows, DOWN, buff=0.35)
        assert_in_frame(eq, sol, rows, note)
        self.say("三項式方程：只留一種元數 ", "$n$", " 的代換")
        self.play(Write(eq), run_time=1.5)
        self.play(Write(sol), run_time=1.8)
        self.play(LaggedStartMap(FadeIn, rows, lag_ratio=0.3), run_time=2)
        self.play(FadeIn(note))
        self.wait(2.5)
        self.play(FadeOut(VGroup(eq, sol, rows, note)))

        # 2. Problem 4983
        q = mixed("Problem 4983：", "$a_1a_2\\cdots a_n$", " 加括號，每對括號恰好包 ", "$r+1$", " 個項", font_size=30).move_to(2.5 * UP)
        no = mixed("$r=2,\\ n=4$", "：乘掉 3 個後剩 2 項，湊不成 3 個 ", "$\\Rightarrow P_4(2)=0$", font_size=26).next_to(q, DOWN, buff=0.35)
        prods = VGroup()
        for p, w in zip(PRODUCTS, lists_with(1, (0, 0, 2))[::-1]):
            prods.add(VGroup(Tex(p, font_size=32), WordTreeMob(w, x_gap=0.32, y_gap=0.45)).arrange(DOWN, buff=0.3))
        prods.arrange(RIGHT, buff=1.2).next_to(no, DOWN, buff=0.5)
        kelly = mixed("Kelly：", "$y=x+y^{r+1}$", "（", "$E_{r+1}\\mapsto x^r$", "、", "$y=x\\,H(L^*)$", "）；", "$P_n(r)=\\frac1n\\binom{(r+1)k}{k}$",
                      "，", "$n=rk+1$", font_size=26).next_to(prods, DOWN, buff=0.45)
        assert_in_frame(q, no, prods, kelly)
        self.say("1961 年 Amer. Math. Monthly 的問題；編輯附註指向 Raney 的論文")
        self.play(FadeIn(q))
        self.play(FadeIn(no))
        self.wait(1)
        self.say("$r=2,\\ n=5$", "：3 種乘積 ", "$=$", " 兩個三元節點的 3 棵樹")
        self.play(LaggedStartMap(FadeIn, prods, lag_ratio=0.3), run_time=2)
        self.play(FadeIn(kelly))
        self.wait(3)
        self.play(FadeOut(VGroup(q, no, prods, kelly)))

        # 3. 六邊形
        hexes = VGroup()
        for a, b in [(0, 3), (1, 4), (2, 5)]:
            hx = RegularPolygon(6, start_angle=PI / 2, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12).scale(1.0)
            v = hx.get_vertices()
            d = Line(v[a], v[b], stroke_color=GREEN, stroke_width=5)
            dots = VGroup(*[Dot(p, radius=0.05) for p in v])
            hexes.add(VGroup(hx, d, dots))
        hexes.arrange(RIGHT, buff=1.2).move_to(0.5 * UP)
        eth = mixed("Etherington (1940)：", "$P_n(r)=$", " 凸 ", "$(n+1)$", " 邊形切成 ", "$(r+2)$", " 邊形的方法數", font_size=28)
        eth.next_to(hexes, DOWN, buff=0.55)
        more = mixed("八邊形切成四邊形 ", "$12$", " 種、切成五邊形 ", "$4$", " 種（程式窮舉驗證）", font_size=24, color=GREY_A).next_to(eth, DOWN, buff=0.25)
        assert_in_frame(hexes, eth, more)
        self.say("$n=5,\\ r=2$", "：六邊形切成兩個四邊形，也是 3 種")
        self.play(LaggedStartMap(FadeIn, hexes, lag_ratio=0.3), run_time=2)
        self.play(FadeIn(eth))
        self.play(FadeIn(more))
        self.wait(3)
        self.play(FadeOut(VGroup(hexes, eth, more)))

        # 4. 模 2
        m2 = Tex(r"c(x)=1+x\,c(x)^2\equiv1+x\,c(x^2)\pmod 2", font_size=40).move_to(2.2 * UP)
        why = mixed("模 2 時 ", "$(\\sum c_nx^n)^2=\\sum c_nx^{2n}$", "（交叉項 ", "$2c_ic_j=0$", "）", font_size=26).next_to(m2, DOWN, buff=0.3)
        cells = VGroup()
        for n in range(16):
            odd = catalan(n) % 2 == 1
            sq = Square(side_length=0.62, stroke_color=YELLOW if odd else GREY_D, stroke_width=3 if odd else 1.5,
                        fill_color=YELLOW, fill_opacity=0.25 if odd else 0)
            cells.add(VGroup(sq, Tex(str(catalan(n) % 2), font_size=28).move_to(sq),
                             Tex(str(n), font_size=20, fill_color=GREY_B).next_to(sq, UP, buff=0.08)))
        cells.arrange(RIGHT, buff=0.12).next_to(why, DOWN, buff=0.6)
        concl = mixed("$C_n$", " 是奇數 ", "$\\Leftrightarrow$", " ", "$n$", " 的二進位全是 1：", "$n=0,1,3,7,15,\\ldots$", font_size=30)
        concl.next_to(cells, DOWN, buff=0.5)
        assert_in_frame(m2, why, cells, concl)
        self.say("Raney 說也能用在係數模質數的級數上；例子：卡塔蘭數的奇偶")
        self.play(Write(m2), run_time=1.5)
        self.play(FadeIn(why))
        self.play(LaggedStartMap(FadeIn, cells, lag_ratio=0.05), run_time=1.8)
        self.play(FadeIn(concl))
        self.wait(3)
