"""
Scene N11 —— 卷積公式（Raney 導讀第 11 節；原文 §7，pp. 449–451）
執行（在 codes/ 內）：manimgl scenes/sceneN11_convolution.py SceneN11Convolution

1. 定理 7.1：a(m,n) = [xⁿ]φ^m 滿足卷積 ⇒ b(m,n) = m/(m+n)·a(m+n,n) 也滿足；b(m,n) ＝ m 棵樹、n 條邊的森林的權重和。
2. φ = 1/(1−x)：投票數 b(m,n) = m/(m+n)·C(m+2n−1, n)；ψ(y) = c(y)；b(2,3) = 14 = 5+2+2+5。
3. Gould 的 G(α,n;β,γ) = α/n!·Π_{m=1}^{n−1}(α+βn−γm)；γ = 1：α/(α+βn)·C(α+βn, n) = Chu 的 A_t((n),(v))（α = t、β = v），
   而且 α 不必是整數：α = ½、β = 2：1, ½, 7/8, 33/16（c(x)^{1/2} 的係數），G(1,2;2,1) = 2 = 7/8 + 1/4 + 7/8。
4. γ = 0：Abel，G = α(α+βn)^{n−1}/n!；k(n+k)^{n−1} = 根恰為 1..k 的有根森林數；n = 3、k = l = 1：50 = 16+9+9+16。
5. Raney 的證明：φ(x) = γx e^{βx}/(e^{γx} − 1)，再用 (7.4)–(7.6)。
"""
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan, raney_A
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import b_from_a, c_from_b, gould_G, gould_phi
from utils.raney_draw import forest_mob
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

GEO = [Fraction(1)] * 10


def fmt(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else r"\tfrac{%d}{%d}" % (x.numerator, x.denominator)


def check_math():
    assert [b_from_a(GEO, 1, n) for n in range(6)] == [catalan(n) for n in range(6)]
    assert [b_from_a(GEO, 3, n) for n in range(6)] == [1, 3, 9, 28, 90, 297]
    assert all(b_from_a(GEO, m, n) == Fraction(m, m + n) * comb(m + 2 * n - 1, n) for m in range(1, 4) for n in range(6))
    assert b_from_a(GEO, 2, 3) == 14 == sum(catalan(k) * catalan(3 - k) for k in range(4))
    for v in (2, 3):
        for t in (1, 2):
            assert all(gould_G(t, n, v, 1) == raney_A(t, (n,), (v,)) for n in range(5))
    h = Fraction(1, 2)
    assert [gould_G(h, n, 2, 1) for n in range(4)] == [1, h, Fraction(7, 8), Fraction(33, 16)]
    assert gould_G(1, 2, 2, 1) == 2 == sum(gould_G(h, k, 2, 1) * gould_G(h, 2 - k, 2, 1) for k in range(3))
    assert gould_G(2, 3, 1, 0) * 6 == 50
    assert [comb(3, i) * Fraction(i + 1) ** (i - 1) * Fraction(4 - i) ** (2 - i) for i in range(4)] == [16, 9, 9, 16]
    phi = gould_phi(2, 1, 6)
    assert all(c_from_b(phi, Fraction(3, 5), n) == gould_G(Fraction(3, 5), n, 2, 1) for n in range(6))


def fit_below(group, anchor, buff=0.45, bottom=-2.95):
    """把 group 放在 anchor 下方；放不下就整組縮小到剛好放得下（字幕在 −3.45）。"""
    avail = anchor.get_bottom()[1] - buff - bottom
    if group.get_height() > avail:
        group.set_height(avail)
    group.next_to(anchor, DOWN, buff=buff)


class SceneN11Convolution(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N11　卷積公式：投票數、Hagen–Rothe、Abel")

        # 1. 定理 7.1
        thm = VGroup(zh("定理 7.1", font_size=32, color=YELLOW),
                     mixed("$a(m,n)=[x^n]\\,\\phi^m$", " 滿足 ", "$a(m_1+m_2,n)=\\sum a(m_1,n_1)\\,a(m_2,n_2)$", font_size=28),
                     mixed("$\\Rightarrow\\ b(m,n)=\\dfrac{m}{m+n}\\,a(m+n,n)$", " 也滿足同樣的卷積", font_size=28)).arrange(DOWN, buff=0.3)
        box = boxed(thm, color=YELLOW).move_to(1.7 * UP)
        mean = mixed("$b(m,n)=$", " ", "$m$", " 棵樹、共 ", "$n$", " 條邊的森林的權重和；森林可以唯一地切成兩片（定理 2.3）", font_size=26)
        mean.next_to(box, DOWN, buff=0.4)
        forest = forest_mob([(2, 0, 0), (0,), (2, 2, 0, 0, 0)], gap=0.6, x_gap=0.4, y_gap=0.5).next_to(mean, DOWN, buff=0.45)
        cut = DashedLine(forest.get_top() + 0.15 * UP, forest.get_bottom() + 0.15 * DOWN, stroke_color=YELLOW).move_to(
            (forest[0].get_right() + forest[1].get_left()) / 2 * RIGHT + forest.get_center()[1] * UP)
        assert_in_frame(box, mean, forest)
        self.say("Raney 第 7 節：從字列的計數得到卷積恆等式")
        self.play(FadeIn(box, shift=0.2 * UP), run_time=1.5)
        self.play(FadeIn(mean))
        self.play(FadeIn(forest), ShowCreation(cut))
        self.wait(3)
        self.play(FadeOut(VGroup(box, mean, forest, cut)))

        # 2. 投票數
        f = mixed("$\\phi=\\frac{1}{1-x}$", "：", "$b(m,n)=\\dfrac{m}{m+n}\\dbinom{m+2n-1}{n}$", "（投票數），", "$\\psi(y)=c(y)$", font_size=30).move_to(2.4 * UP)
        rows = VGroup()
        for m in (1, 2, 3):
            row = VGroup(Tex(r"m=%d" % m, font_size=30), *[Tex(fmt(b_from_a(GEO, m, n)), font_size=30) for n in range(6)])
            for c, cell in enumerate(row):
                cell.move_to(np.array([-3.6 + 1.3 * c, 0, 0]))
            rows.add(row)
        head = VGroup(*[Tex(r"n=%d" % n, font_size=26, fill_color=GREY_B).move_to(np.array([-3.6 + 1.3 * (n + 1), 0, 0])) for n in range(6)])
        tab = VGroup(head, *rows).arrange(DOWN, buff=0.28).next_to(f, DOWN, buff=0.45)
        conv = Tex(r"b(2,3)=14=b(1,0)b(1,3)+b(1,1)b(1,2)+b(1,2)b(1,1)+b(1,3)b(1,0)=5+2+2+5", font_size=30)
        conv.next_to(tab, DOWN, buff=0.45)
        assert_in_frame(f, tab, conv)
        self.say("例：", "$\\phi=1/(1-x)$", "；", "$b(1,n)=C_n$", "，", "$b(2,n)=C_{n+1}$")
        self.play(FadeIn(f), run_time=1.2)
        self.play(FadeIn(tab), run_time=1.5)
        self.play(Write(conv), run_time=1.5)
        self.say("卷積就是卡塔蘭遞迴")
        self.wait(3)
        self.play(FadeOut(VGroup(f, tab, conv)))

        # 3. Gould、γ = 1
        g = Tex(r"G(\alpha,n;\beta,\gamma)=\frac{\alpha}{n!}\prod_{m=1}^{n-1}(\alpha+\beta n-\gamma m),\qquad "
                r"G(\alpha_1+\alpha_2,n)=\sum_{n_1+n_2=n}G(\alpha_1,n_1)\,G(\alpha_2,n_2)", font_size=30).move_to(2.4 * UP)
        g1 = VGroup(mixed("$\\gamma=1$", "（Hagen–Rothe）：", "$G(\\alpha,n;\\beta,1)=\\dfrac{\\alpha}{\\alpha+\\beta n}\\dbinom{\\alpha+\\beta n}{n}$", font_size=28),
                    mixed("取 ", "$\\alpha=t$", "、", "$\\beta=v$", "：就是 Chu 講義的 ", "$A_t\\big((n),(v)\\big)$", "，卷積就是 Raney 公式", font_size=28),
                    mixed("但 ", "$\\alpha$", " 不必是整數：", "$\\alpha=\\tfrac12,\\ \\beta=2$", "：", "$1,\\ \\tfrac12,\\ \\tfrac78,\\ \\tfrac{33}{16},\\ldots$",
                          "（", "$c(x)^{1/2}$", " 的係數）", font_size=28),
                    Tex(r"G(1,2;2,1)=2=1\cdot\tfrac78+\tfrac12\cdot\tfrac12+\tfrac78\cdot1", font_size=34),
                    ).arrange(DOWN, buff=0.3)
        fit_below(g1, g)
        assert_in_frame(g, g1)
        self.say("Gould (1957) 的公式：一條同時包含 Vandermonde 型與 Abel 型的卷積")
        self.play(Write(g), run_time=2)
        self.wait(1)
        for item in g1:
            self.play(FadeIn(item, shift=0.15 * UP), run_time=1.0)
            self.wait(1.2)
        self.wait(1.5)
        self.play(FadeOut(g1))

        # 4. γ = 0：Abel
        g0 = VGroup(mixed("$\\gamma=0$", "（Abel）：", "$G(\\alpha,n;\\beta,0)=\\dfrac{\\alpha(\\alpha+\\beta n)^{n-1}}{n!}$", font_size=28),
                    mixed("$n!\\,G(k,n;1,0)=k(n+k)^{n-1}$", "：頂點 ", "$1,\\ldots,n+k$", "、根恰為 ", "$1,\\ldots,k$", " 的有根森林數", font_size=28),
                    mixed("$n=3,\\ k=l=1$", "：", "$2\\cdot5^2=50=\\sum_i\\binom3i(i+1)^{i-1}(4-i)^{2-i}=16+9+9+16$", font_size=28),
                    zh("卷積 ＝ 把森林分成兩片（Gessel 的 Abel 恆等式）", font_size=26, color=GREY_A),
                    ).arrange(DOWN, buff=0.3)
        proof = mixed("Raney 的證明：取 ", "$\\phi(x)=\\dfrac{\\gamma x e^{\\beta x}}{e^{\\gamma x}-1}$", "，再用 (7.4)–(7.6)", font_size=26, color=GREY_A)
        g0.add(proof)
        proof.next_to(g0[3], DOWN, buff=0.3)
        fit_below(g0, g)
        assert_in_frame(g0)
        self.say("$\\gamma=0$", "：Abel 卷積，數的是標號森林")
        for item in g0[:4]:
            self.play(FadeIn(item, shift=0.15 * UP), run_time=1.0)
            self.wait(1.0)
        self.play(FadeIn(proof))
        self.wait(3)
