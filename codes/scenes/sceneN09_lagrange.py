"""
Scene N09 —— Lagrange 反演（Raney 導讀第 9 節；原文 §5，pp. 446–448）
執行（在 codes/ 內）：manimgl scenes/sceneN09_lagrange.py SceneN09Lagrange

1. w = x·φ(w)，φ(x) = Σ a_n xⁿ。Lagrange：[xⁿ]w = (1/n)[xⁿ⁻¹]φⁿ（Raney 寫成 (Dⁿ⁻¹ zⁿ)(0)/n!）。
2. 式 (5.6)：[xⁿ]w ＝ 所有 n 個節點的平面樹的權重和，有 i 個小孩的節點權重 a_i。
   φ = 1+x+x²、n = 4：1110、1200、2010、2100 四棵 → Motzkin 數 4 = (1/4)·16。
   φ = 2+3x+x³、n = 3：110（2·3² = 18）與 200（2²·0 = 0）→ 18 = (1/3)·54。
3. 同態 E_j ↦ a₀^{j−1}a_j x^j（θ 數邊數）作用在 L* = Σ E_j(L*)^j 上，乘 a₀x（多一個節點、多一片葉子）就得 w = xΣa_j w^j。
4. 四個 φ 的係數：1/(1−x) → C_{n−1}、(1+x)² → C_n、1+x+x² → Motzkin、e^x → n^{n−1}/n!。
5. 冪次：[xⁿ]w^t = (t/n)[xⁿ⁻ᵗ]φⁿ（Gessel (2.2.1)），由 (L*)^t 數 t 字列直接得到。
"""
import sys
from fractions import Fraction
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import exp_series, lagrange_coeff, lists_with, ps_pow, solve_w
from utils.raney_draw import WordTreeMob, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

MOTZ = lists_with(1, (3, 0)) + lists_with(1, (1, 1))
N = 6


def poly(cs, n=N):
    return [Fraction(c) for c in cs] + [Fraction(0)] * (n + 1 - len(cs))


PHIS = [(r"\frac{1}{1-x}", [Fraction(1)] * (N + 1), r"C_{n-1}"),
        (r"(1+x)^2", poly([1, 2, 1]), r"C_n"),
        (r"1+x+x^2", poly([1, 1, 1]), r"M_{n-1}"),
        (r"e^x", exp_series(1, N), r"n^{n-1}/n!")]


def fmt(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else r"\tfrac{%d}{%d}" % (x.numerator, x.denominator)


def check_math():
    assert MOTZ == [(1, 1, 1, 0), (1, 2, 0, 0), (2, 0, 1, 0), (2, 1, 0, 0)]
    assert ps_pow(poly([1, 1, 1], 4), 4, 3)[3] == 16 and lagrange_coeff(poly([1, 1, 1]), 4) == 4
    odd = poly([2, 3, 0, 1])
    assert lagrange_coeff(odd, 3) == 18 == Fraction(1, 3) * ps_pow(odd, 3, 2)[2] and ps_pow(odd, 3, 2)[2] == 54
    for _, phi, _ in PHIS:
        assert solve_w(phi, N)[1:] == [lagrange_coeff(phi, n) for n in range(1, N + 1)]
    assert [solve_w(PHIS[3][1], N)[n] * factorial(n) for n in range(1, 6)] == [1, 2, 9, 64, 625]
    w = solve_w(PHIS[1][1], N)
    assert all(ps_pow(w, 2, N)[n] == lagrange_coeff(PHIS[1][1], n, 2) for n in range(1, N + 1))


class SceneN09Lagrange(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N09　Lagrange 反演：係數是樹的權重和")

        # 1. 公式
        eq = Tex(r"w=x\,\phi(w),\qquad \phi(x)=a_0+a_1x+a_2x^2+\cdots", font_size=40).move_to(2.3 * UP)
        lag = Tex(r"[x^n]\,w=\frac{1}{n}\,[x^{n-1}]\,\phi(x)^n", font_size=44).next_to(eq, DOWN, buff=0.45)
        raney = mixed("Raney 的寫法：", "$\\dfrac{(D^{n-1}\\bar z^{\\,n})(0)}{n!}$", "（", "$D$", " 是微分，不是 Chu 的生成函數）",
                      font_size=26, color=GREY_A).next_to(lag, DOWN, buff=0.35)
        assert_in_frame(eq, lag, raney)
        self.say("Lagrange 反演：方程 ", "$w=x\\phi(w)$", " 的解的係數")
        self.play(Write(eq), run_time=1.5)
        self.play(Write(lag), run_time=1.5)
        self.play(FadeIn(raney))
        self.wait(2)

        # 2. 樹的權重和
        mean = mixed("$[x^n]w=$", " 所有 ", "$n$", " 個節點的平面樹的權重和；有 ", "$i$", " 個小孩的節點權重 ", "$a_i$", font_size=28, color=YELLOW)
        mean.next_to(raney, DOWN, buff=0.45)
        assert_in_frame(mean)
        self.say("Raney 式 (5.6)：用定理 2.2 把多項式係數換成 ", "$L(1;\\bar p)$")
        self.play(FadeIn(mean))
        self.wait(2.5)
        self.play(FadeOut(VGroup(eq, raney)), VGroup(lag, mean).animate.arrange(DOWN, buff=0.3).move_to(2.3 * UP))
        trees = VGroup(*[VGroup(WordTreeMob(w, x_gap=0.4, y_gap=0.45), word_tiles(w, size=0.3, font_size=18, buff=0.03))
                         .arrange(DOWN, buff=0.25) for w in MOTZ]).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
        trees.move_to(np.array([0, -0.15, 0]))
        res = mixed("$\\phi=1+x+x^2$", "，", "$n=4$", "：4 棵樹，權重都是 1 ", "$\\Rightarrow\\ 4=\\frac14\\cdot16$", "（Motzkin 數）", font_size=26)
        res.next_to(trees, DOWN, buff=0.35)
        assert_in_frame(trees, res)
        self.say("例：", "$\\phi=1+x+x^2$", "，4 個節點、每個節點至多 2 個小孩的樹")
        self.play(LaggedStartMap(FadeIn, trees, lag_ratio=0.25), run_time=2)
        self.play(FadeIn(res))
        self.wait(2.5)
        self.play(FadeOut(VGroup(trees, res)))
        t2 = VGroup(*[VGroup(WordTreeMob(w, x_gap=0.45, y_gap=0.5), Tex(t, font_size=30)).arrange(DOWN, buff=0.3)
                      for w, t in [((1, 1, 0), r"a_0a_1^2=2\cdot3^2=18"), ((2, 0, 0), r"a_0^2a_2=2^2\cdot0=0")]])
        t2.arrange(RIGHT, buff=1.5).move_to(np.array([0, -0.1, 0]))
        r2 = mixed("$\\phi=2+3x+x^3$", "，", "$n=3$", "：", "$18=\\frac13[x^2]\\phi^3=\\frac{54}{3}$", font_size=28).next_to(t2, DOWN, buff=0.45)
        assert_in_frame(t2, r2)
        self.say("權重不是 1 的例子：", "$a_0=2,\\ a_1=3,\\ a_2=0,\\ a_3=1$")
        self.play(FadeIn(t2), run_time=1.2)
        self.play(FadeIn(r2))
        self.wait(2.5)
        self.play(FadeOut(VGroup(t2, r2, lag, mean)))

        # 3. 同態
        steps = VGroup(
            mixed("代換 ", "$H$", "：", "$E_j\\mapsto a_0^{\\,j-1}a_j\\,x^j$", "（", "$x$", " 數邊數）", font_size=30),
            Tex(r"HL^*=1+\sum_{j\ge1}a_0^{\,j-1}a_j\,x^j\,(HL^*)^j", font_size=38),
            mixed("乘 ", "$a_0x$", "：", "$w=a_0x\\,HL^*$", " 滿足 ", "$w=x\\sum_j a_jw^j$", font_size=30),
            mixed("節點數 ", "$=$", " 邊數 ", "$+1$", "（多一個 ", "$x$", "）；葉子數 ", "$=1+\\sum(j-1)p_j$", "（多一個 ", "$a_0$", "）", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(0.6 * UP)
        assert_in_frame(steps)
        self.say("Raney 的證明：把 ", "$L^*=\\sum_j E_j(L^*)^j$", " 送到一個變數的冪級數")
        self.play(LaggedStartMap(FadeIn, steps, lag_ratio=0.5), run_time=4)
        self.say("整個證明沒有用到微積分：內容就是定理 2.2 與定理 4.1")
        self.wait(3)
        self.play(FadeOut(steps))

        # 4. 係數表
        head = VGroup(Tex(r"\phi", font_size=32), *[Tex(r"n=%d" % n, font_size=28) for n in range(1, N + 1)], zh("名稱", font_size=24))
        rows = [head]
        for name, phi, nm in PHIS:
            vals = [lagrange_coeff(phi, n) for n in range(1, N + 1)]
            rows.append(VGroup(Tex(name, font_size=32), *[Tex(fmt(v), font_size=30) for v in vals], Tex(nm, font_size=30)))
        table = VGroup(*rows)
        col_x = [-5.0] + [-3.1 + 1.25 * k for k in range(N)] + [5.1]
        for r, row in enumerate(table):
            for c, cell in enumerate(row):
                cell.move_to(np.array([col_x[c], 1.9 - 0.85 * r, 0]))
        line = Line(np.array([-5.8, 1.5, 0]), np.array([5.9, 1.5, 0]), stroke_color=GREY_C, stroke_width=1.5)
        power = mixed("冪次版本：", "$[x^n]\\,w^t=\\frac{t}{n}[x^{n-t}]\\phi^n$", "（由 ", "$(L^*)^t$", " 數 ", "$t$", " 字列）", font_size=28)
        power.move_to(np.array([0, -2.45, 0]))
        assert_in_frame(table, power)
        self.say("四個例子：逐次代入解方程得到的係數，和 Lagrange 公式一致")
        self.play(FadeIn(table[0]), ShowCreation(line))
        self.play(LaggedStartMap(FadeIn, VGroup(*table[1:]), lag_ratio=0.3), run_time=2.5)
        self.wait(2)
        self.play(FadeIn(power))
        self.wait(3)
