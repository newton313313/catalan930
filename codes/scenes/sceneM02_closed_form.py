"""
Scene M02 —— 解出 C(x) 的封閉形式（MIT 18.212 第 1 講）

    C = 1 + xC^2  ->  xC^2 - C + 1 = 0  ->  C = (1 ± sqrt(1-4x)) / (2x)
    x -> 0：「+」約為 1/x 爆掉，「-」趨近 1 = C_0  ->  取減號
    sqrt(1-4x) = sum binom(1/2, m) (-4x)^m，binom(1/2, m)(-4)^m = -(2/m) binom(2m-2, m-1)
             = 1 - 2x - 2x^2 - 4x^3 - 10x^4 - 28x^5 - ...
    代回：C_n = -(1/2)[x^{n+1}] sqrt(1-4x) = binom(2n, n) / (n+1) = 1, 1, 2, 5, 14, ...

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM02_closed_form.py SceneM02ClosedForm
"""
import sys
from fractions import Fraction
from math import comb, factorial, sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *
from manimlib.utils.tex import num_tex_symbols

from utils.counting import binom_general, catalan, catalan_from_sqrt, sqrt_1m4x_coeffs
from utils.mit_draw import CATALAN_COLOR
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh

M_MAX = 5                       # 表格與級數展開到 x^5（才算得到 C_4 = 14）
X_LIM, Y_LIM = 6.8, (-3.0, 3.2)  # 可用畫面範圍
HALF = Fraction(1, 2)


# ---------------------------------------------------------------------------- 數學資料
def odd_product(k):
    """1·3·5···k（k 為奇數；k < 1 時是空乘積 1）。"""
    out = 1
    for j in range(1, k + 1, 2):
        out *= j
    return out


def minus_branch(x):
    """(1 - sqrt(1-4x)) / (2x) = 2 / (1 + sqrt(1-4x))：在 x = 0 也有定義（= 1）。"""
    return 2.0 / (1.0 + sqrt(max(0.0, 1.0 - 4.0 * x)))


def plus_branch(x):
    return (1.0 + sqrt(max(0.0, 1.0 - 4.0 * x))) / (2.0 * x)


def check_math():
    s = sqrt_1m4x_coeffs(M_MAX + 1)
    assert s == [1, -2, -2, -4, -10, -28]
    binoms = [binom_general(HALF, m) for m in range(M_MAX + 1)]
    assert binoms == [1, Fraction(1, 2), Fraction(-1, 8), Fraction(1, 16), Fraction(-5, 128), Fraction(7, 256)]
    powers = [(-4) ** m for m in range(M_MAX + 1)]
    assert all(b * p == c for b, p, c in zip(binoms, powers, s))
    # 一般項：binom(1/2,m)(-4)^m = -2^m·1·3···(2m-3)/m! = -(2/m) binom(2m-2, m-1)
    for m in range(1, 12):
        lhs = binom_general(HALF, m) * (-4) ** m
        assert lhs == -Fraction(2 ** m * odd_product(2 * m - 3), factorial(m))
        assert lhs == -Fraction(2, m) * comb(2 * m - 2, m - 1)
    # 取減號：sqrt(1-4x) ≈ 1 - 2x，所以 (1-(1-2x))/(2x) = 1 = C_0
    assert s[0] == 1 and s[1] == -2 and catalan(0) == 1
    # 代回：C_n = -[x^{n+1}] sqrt(1-4x) / 2 = binom(2n,n)/(n+1)
    cs = catalan_from_sqrt(M_MAX)
    assert cs == [1, 1, 2, 5, 14] == [catalan(n) for n in range(M_MAX)]
    assert cs == [-s[n + 1] // 2 for n in range(M_MAX)] == [comb(2 * n, n) // (n + 1) for n in range(M_MAX)]
    for n in range(12):
        assert Fraction(-1, 2) * (-Fraction(2, n + 1) * comb(2 * n, n)) == catalan(n)
    # 圖形：「−」在 0 是 1；「+」在 0.16 是 5；兩支在 x = 1/4 會合於 2
    assert abs(minus_branch(0.0) - 1) < 1e-12 and abs(plus_branch(0.16) - 5) < 1e-9
    assert abs(minus_branch(0.25) - 2) < 1e-12 and abs(plus_branch(0.25) - 2) < 1e-12
    return s, binoms, powers, cs


# ---------------------------------------------------------------------------- 文字工具
def frac_tex(q):
    q = Fraction(q)
    if q.denominator == 1:
        return str(q.numerator)
    sign = "-" if q < 0 else ""
    return sign + R"\frac{%d}{%d}" % (abs(q.numerator), q.denominator)


def monomial(c, p):
    """c x^p 的 Tex（c > 0）。"""
    if p == 0:
        return str(c)
    coef = "" if c == 1 else str(c)
    return coef + ("x" if p == 1 else "x^{%d}" % p)


def pieces_tex(pieces, **kwargs):
    """把多段 Tex 字串接成一個 Tex，並回傳每段對應的字形範圍 [(start, end)]。"""
    spans, pos = [], 0
    for p in pieces:
        k = num_tex_symbols(p)
        spans.append((pos, pos + k))
        pos += k
    tex = Tex("".join(pieces), **kwargs)
    assert len(tex) == pos, (len(tex), pos, "".join(pieces))
    return tex, spans


def glyphs(tex, span):
    return tex[span[0]:span[1]]


def consolidate(scene, whole, parts):
    """動畫把 whole 的字形分成好幾塊加進場景；收回成一個物件，之後才能整體移動。"""
    scene.remove(*parts)
    scene.add(whole)


def check_inside(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= -X_LIM - 1e-6 and m.get_right()[0] <= X_LIM + 1e-6, m
        assert m.get_bottom()[1] >= Y_LIM[0] - 1e-6 and m.get_top()[1] <= Y_LIM[1] + 1e-6, m


def check_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊。"""
    sep_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    sep_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert sep_x or sep_y, (a, b)


# ---------------------------------------------------------------------------- 畫面零件
def series_line(s, font_size):
    """sqrt(1-4x) = 1 - 2x - 2x^2 - ...；回傳 (群組, 本體, 每個 m 的字形範圍（含負號）, 其他範圍)。"""
    prefix = Tex(R"\sqrt{1-4x}", font_size=font_size)
    pieces = ["=", str(s[0])]
    for m in range(1, len(s)):
        assert s[m] < 0
        pieces += ["-", monomial(-s[m], m)]
    pieces += ["-", R"\cdots"]
    body, spans = pieces_tex(pieces, font_size=font_size)
    assert "".join(pieces) == "=1-2x-2x^{2}-4x^{3}-10x^{4}-28x^{5}-\\cdots"
    terms = [spans[1]] + [(spans[2 * m][0], spans[2 * m + 1][1]) for m in range(1, len(s))]
    rest = [spans[0], (spans[-2][0], spans[-1][1])]
    VGroup(prefix, body).arrange(RIGHT, buff=0.14)
    body.align_to(prefix, DOWN)
    return VGroup(prefix, body), body, terms, rest


def binomial_table(s, binoms, powers, font_size=30, col_gap=1.75, row_gap=0.68, x0=-3.35, y0=1.45):
    heads_tex = ["m", R"\binom{1/2}{m}", "(-4)^m", R"\binom{1/2}{m}(-4)^m"]
    heads = VGroup(*[Tex(h, font_size=font_size) for h in heads_tex])
    cols = VGroup()
    for m in range(len(s)):
        col = VGroup(
            Tex(str(m), font_size=font_size, fill_color=MUTED_COLOR),
            Tex(frac_tex(binoms[m]), font_size=font_size),
            Tex(str(powers[m]), font_size=font_size),
            Tex(str(s[m]), font_size=font_size + 4, fill_color=YELLOW),
        )
        for r, cell in enumerate(col):
            cell.move_to(np.array([x0 + m * col_gap, y0 - r * row_gap, 0.0]))
        cols.add(col)
    for r, h in enumerate(heads):
        h.move_to(np.array([x0 - 1.0 - h.get_width() / 2, y0 - r * row_gap, 0.0]))
    heads[3].set_fill(YELLOW)
    top, bottom = y0 + 0.28, y0 - 3 * row_gap - 0.4   # 上端不要伸進上方的黃框
    left = heads.get_left()[0] - 0.15
    right = x0 + (len(s) - 1) * col_gap + 0.6
    v_line = Line(np.array([x0 - 0.75, top, 0.0]), np.array([x0 - 0.75, bottom, 0.0]),
                  stroke_color=GREY_C, stroke_width=2)
    h_line = Line(np.array([left, y0 - row_gap / 2, 0.0]), np.array([right, y0 - row_gap / 2, 0.0]),
                  stroke_color=GREY_C, stroke_width=2)
    return heads, cols, VGroup(v_line, h_line)


def branch_graph(center):
    axes = Axes(x_range=(0, 0.25, 0.05), y_range=(0, 5, 1), width=4.4, height=4.2,
                axis_config=dict(stroke_color=GREY_B, stroke_width=2, include_tip=False))
    axes.move_to(center)
    ticks = VGroup(
        Tex("0", font_size=26).next_to(axes.c2p(0, 0), DL, buff=0.1),
        Tex("1", font_size=26).next_to(axes.c2p(0, 1), LEFT, buff=0.15),
        Tex("2", font_size=26).next_to(axes.c2p(0, 2), LEFT, buff=0.15),
        Tex(R"\tfrac{1}{4}", font_size=30).next_to(axes.c2p(0.25, 0), DOWN, buff=0.15),
        Tex("x", font_size=30).next_to(axes.c2p(0.25, 0), RIGHT, buff=0.2),
    )
    minus = axes.get_graph(minus_branch, x_range=(0.0, 0.25, 0.0025), color=OK_COLOR, stroke_width=5)
    plus = axes.get_graph(plus_branch, x_range=(0.16, 0.25, 0.001), color=CROSSING_COLOR, stroke_width=5)
    tip_start = axes.c2p(0.16, plus_branch(0.16))
    tip_dir = normalize(axes.c2p(0.15, plus_branch(0.15)) - tip_start)
    up_arrow = Arrow(tip_start, tip_start + 0.75 * tip_dir, buff=0, stroke_width=5, stroke_color=CROSSING_COLOR)
    inf_lab = Tex(R"\infty", font_size=36, fill_color=CROSSING_COLOR).next_to(up_arrow, RIGHT, buff=0.15).align_to(up_arrow, UP)
    plus_lab = Tex("+", font_size=40, fill_color=CROSSING_COLOR)
    plus_lab.next_to(axes.c2p(0.2, plus_branch(0.2)), RIGHT, buff=0.25)
    minus_lab = Tex("-", font_size=40, fill_color=OK_COLOR)
    minus_lab.next_to(axes.c2p(0.12, minus_branch(0.12)), DOWN, buff=0.3)
    c0_dot = Dot(axes.c2p(0, 1), radius=0.09, fill_color=OK_COLOR).set_z_index(2)
    c0_lab = Tex("C_0=1", font_size=32, fill_color=OK_COLOR).next_to(c0_dot, UP, buff=0.3).shift(0.55 * RIGHT)
    return VGroup(axes, ticks), minus, VGroup(plus, up_arrow, inf_lab, plus_lab), VGroup(minus_lab, c0_dot, c0_lab)


# ---------------------------------------------------------------------------- 場景
class SceneM02ClosedForm(ChuScene):
    def construct(self):
        s, binoms, powers, cs = check_math()
        self.show_header("解出 C(x) 的封閉形式")
        t2c = {"C": CATALAN_COLOR}

        # ======================================================== A. 解二次方程式、選減號
        eq1 = Tex("C=1+xC^2", font_size=60, t2c=t2c).move_to(2.3 * UP)
        eq2 = Tex("xC^2-C+1=0", font_size=60, t2c=t2c).move_to(1.15 * UP)
        eq3 = Tex(R"C=\frac{1\pm\sqrt{1-4x}}{2x}", font_size=60, t2c=t2c).move_to(0.45 * DOWN)
        note = mixed("二次公式：", "$a=x,\\ b=-1,\\ c=1$", font_size=24, color=MUTED_COLOR)
        note.next_to(eq3, DOWN, buff=0.35)
        check_inside(eq1, eq2, eq3, note)
        self.say("上一幕：", "$C=1+xC^2$", "。把它看成 ", "$C$", " 的二次方程式")
        self.play(FadeIn(eq1, shift=0.2 * DOWN), run_time=0.8)
        self.wait(0.6)
        self.play(TransformFromCopy(eq1, eq2), run_time=1.0)
        self.wait(0.4)
        self.say("用二次公式解出 ", "$C$", "，有正負兩個根")
        self.play(TransformFromCopy(eq2, eq3), FadeIn(note, shift=0.2 * UP), run_time=1.0)
        self.wait(1.0)

        # 兩個根：左邊算式，右邊圖形
        top_eq_pos = np.array([-3.4, 2.3, 0.0])
        plus_f = Tex(R"\frac{1+\sqrt{1-4x}}{2x}\approx\frac{2}{2x}=\frac{1}{x}", font_size=40,
                     fill_color=CROSSING_COLOR)
        plus_row = VGroup(zh("取＋", font_size=28, color=CROSSING_COLOR), plus_f).arrange(RIGHT, buff=0.3)
        plus_note = mixed("$x\\to 0$", " 時發散：不可能是", "$C_0+C_1x+\\cdots$",
                          font_size=22, color=CROSSING_COLOR)
        minus_f = Tex(R"\frac{1-\sqrt{1-4x}}{2x}\approx\frac{1-(1-2x)}{2x}=1", font_size=40,
                      fill_color=OK_COLOR)
        minus_row = VGroup(zh("取－", font_size=28, color=OK_COLOR), minus_f).arrange(RIGHT, buff=0.3)
        minus_note = mixed("用 ", "$\\sqrt{1-4x}\\approx 1-2x$", "：", "$x\\to 0$", " 時趨近 ", "$1=C_0$",
                           font_size=22, color=OK_COLOR)
        plus_row.move_to(np.array([-3.4, 0.75, 0.0]))
        plus_note.next_to(plus_row, DOWN, buff=0.22).align_to(plus_f, LEFT)
        minus_row.move_to(np.array([-3.4, -1.15, 0.0])).align_to(plus_row, LEFT)
        minus_note.next_to(minus_row, DOWN, buff=0.22).align_to(minus_f, LEFT)
        axes_grp, minus_curve, plus_parts, minus_parts = branch_graph(np.array([3.9, 0.05, 0.0]))
        check_inside(plus_row, plus_note, minus_row, minus_note, axes_grp, plus_parts, minus_parts)
        for a in (plus_row, plus_note, minus_row, minus_note):
            check_apart(a, axes_grp)
        check_apart(plus_note, minus_row)

        self.say("看 ", "$x\\to 0$", "：生成函數在 0 的值必須是 ", "$C_0=1$")
        self.play(FadeOut(VGroup(eq1, eq2, note)), eq3.animate.scale(0.8).move_to(top_eq_pos), run_time=0.9)
        self.play(ShowCreation(axes_grp[0]), FadeIn(axes_grp[1]), run_time=0.9)
        self.play(FadeIn(plus_row, shift=0.2 * RIGHT), ShowCreation(plus_parts[0]), run_time=1.0)
        self.play(GrowArrow(plus_parts[1]), FadeIn(plus_parts[2:]), FadeIn(plus_note), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(minus_row, shift=0.2 * RIGHT), ShowCreation(minus_curve), run_time=1.0)
        self.play(FadeIn(minus_parts), FadeIn(minus_note), run_time=0.8)
        self.wait(0.8)
        pick = SurroundingRectangle(VGroup(minus_row, minus_note), buff=0.15, color=YELLOW, stroke_width=3)
        self.say("「＋」在 0 附近爆掉，「－」趨近 ", "$1=C_0$", "，所以取減號")
        self.play(ShowCreation(pick), Indicate(minus_parts[1], color=YELLOW), run_time=0.9)
        self.wait(1.2)

        # ======================================================== B. 二項級數展開 sqrt(1-4x)
        chosen = Tex(R"C=\frac{1-\sqrt{1-4x}}{2x}", font_size=44, t2c=t2c)
        chosen_box = SurroundingRectangle(chosen, buff=0.15, color=YELLOW, stroke_width=3)
        chosen_grp = VGroup(chosen_box, chosen).move_to(np.array([-4.85, 2.48, 0.0]))
        binom_line = Tex(R"\sqrt{1-4x}=(1-4x)^{1/2}=\sum_{m\ge 0}\binom{1/2}{m}(-4x)^m", font_size=40)
        binom_line.move_to(np.array([1.9, 2.4, 0.0]))
        heads, cols, grid = binomial_table(s, binoms, powers)
        identity = Tex(R"\binom{1/2}{m}(-4)^m=-\frac{2^m\cdot 1\cdot 3\cdot 5\cdots(2m-3)}{m!}"
                       R"=-\frac{2}{m}\binom{2m-2}{m-1}", font_size=34)
        id_cond = mixed("（", "$m\\ge 1$", "）", font_size=22, color=MUTED_COLOR)
        id_grp = VGroup(identity, id_cond).arrange(RIGHT, buff=0.2).move_to(1.5 * DOWN)
        series, body, terms, rest = series_line(s, font_size=40)
        series.move_to(2.5 * DOWN)
        check_inside(chosen_grp, binom_line, heads, cols, grid, id_grp, series)
        check_apart(chosen_grp, binom_line)
        check_apart(chosen_grp, VGroup(heads, grid))
        check_apart(VGroup(heads, grid), id_grp)
        check_apart(binom_line, cols)
        check_apart(cols, id_grp)
        check_apart(id_grp, series)

        self.say("用牛頓的廣義二項式定理展開 ", "$\\sqrt{1-4x}$")
        self.play(FadeOut(VGroup(plus_row, plus_note, minus_row, minus_note, pick, axes_grp, minus_curve,
                                 plus_parts, minus_parts)),
                  ReplacementTransform(eq3, chosen), FadeIn(chosen_box), run_time=1.0)
        self.play(Write(binom_line), run_time=1.2)
        self.wait(0.5)
        self.say("逐項計算：", "$\\tbinom{1/2}{m}$", " 乘上 ", "$(-4)^m$", "，結果全是整數")
        self.play(FadeIn(heads), ShowCreation(grid), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(col[:3], shift=0.15 * DOWN) for col in cols], lag_ratio=0.25),
                  run_time=1.6)
        self.play(LaggedStart(*[FadeIn(col[3], scale=1.4) for col in cols], lag_ratio=0.2), run_time=1.2)
        self.wait(0.6)
        self.say("一般項：", "$m$", " 個因子各帶一個 ", "$\\tfrac{1}{2}$", "，奇數連乘積再寫成階乘")
        self.play(FadeIn(id_grp, shift=0.2 * UP), run_time=1.0)
        self.wait(1.6)
        self.say("把黃色那一列排回去，就是 ", "$\\sqrt{1-4x}$", " 的展開式")
        parts = [series[0]] + [glyphs(body, r) for r in rest] + [glyphs(body, r) for r in terms]
        self.play(*[FadeIn(p) for p in parts[:1 + len(rest)]],
                  *[TransformFromCopy(cols[m][3], parts[1 + len(rest) + m]) for m in range(len(s))],
                  run_time=1.5)
        consolidate(self, series, parts)
        self.wait(1.0)

        # ======================================================== C. 代回，得到 C_n
        id_target = id_grp.copy().scale(0.85).move_to(0.45 * DOWN)
        series_target = series.copy().move_to(np.array([1.9, 2.4, 0.0]))
        self.say("代回 ", "$C=\\tfrac{1-\\sqrt{1-4x}}{2x}$", "：減掉後負號全部翻正")
        self.play(FadeOut(VGroup(binom_line, heads, cols, grid)), run_time=0.6)
        self.play(Transform(series, series_target), Transform(id_grp, id_target), run_time=1.0)

        # C(x) = (2x + 2x^2 + ...)/(2x) = 1 + x + 2x^2 + 5x^3 + 14x^4 + ...
        num_pieces = []
        for m in range(1, len(s)):
            num_pieces += [monomial(-s[m], m), "+"]
        num_pieces.append(R"\cdots")
        num, num_spans = pieces_tex(num_pieces, font_size=38)
        assert "".join(num_pieces) == "2x+2x^{2}+4x^{3}+10x^{4}+28x^{5}+\\cdots"
        den = Tex("2x", font_size=38)
        bar = Line(ORIGIN, (num.get_width() + 0.2) * RIGHT, stroke_width=2.5)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.12)
        lhs = Tex("C(x)=", font_size=40, t2c=t2c)
        rhs_pieces = ["="]
        for n, c in enumerate(cs):
            rhs_pieces += [monomial(c, n), "+"]
        rhs_pieces.append(R"\cdots")
        rhs, rhs_spans = pieces_tex(rhs_pieces, font_size=40)
        assert "".join(rhs_pieces) == "=1+x+2x^{2}+5x^{3}+14x^{4}+\\cdots"
        line = VGroup(lhs, frac, rhs).arrange(RIGHT, buff=0.2)
        bar_y = bar.get_center()[1]
        lhs.shift((bar_y - lhs[-1].get_center()[1]) * UP)
        rhs.shift((bar_y - rhs[0].get_center()[1]) * UP)
        line.move_to(1.05 * UP)
        num_terms = [num_spans[2 * k] for k in range(len(cs))]
        num_rest = [num_spans[2 * k + 1] for k in range(len(cs))] + [num_spans[-1]]
        rhs_terms = [rhs_spans[1 + 2 * n] for n in range(len(cs))]
        rhs_rest = [rhs_spans[0]] + [rhs_spans[2 + 2 * n] for n in range(len(cs))] + [rhs_spans[-1]]
        for r in rhs_terms:
            glyphs(rhs, r).set_fill(CATALAN_COLOR)
        c_labels = VGroup(*[Tex("C_{%d}" % n, font_size=26, fill_color=MUTED_COLOR)
                            .next_to(glyphs(rhs, rhs_terms[n]), DOWN, buff=0.22) for n in range(len(cs))])
        c_labels.align_to(c_labels[0], UP)
        check_inside(line, c_labels, series_target, id_target)
        check_apart(series_target, line)
        check_apart(c_labels, id_target)

        self.play(FadeIn(lhs), ShowCreation(bar), FadeIn(den),
                  *[FadeIn(glyphs(num, r)) for r in num_rest],
                  *[TransformFromCopy(glyphs(body, terms[m])[1:], glyphs(num, num_terms[m - 1]))
                    for m in range(1, len(s))], run_time=1.4)
        self.wait(0.5)
        self.say("再除以 ", "$2x$", "：係數除以 2、次方減 1，得到 ", "$1,1,2,5,14$")
        self.play(*[FadeIn(glyphs(rhs, r)) for r in rhs_rest],
                  *[TransformFromCopy(glyphs(num, num_terms[n]), glyphs(rhs, rhs_terms[n])) for n in range(len(cs))],
                  run_time=1.4)
        self.play(LaggedStart(*[FadeIn(lab, shift=0.1 * UP) for lab in c_labels], lag_ratio=0.15), run_time=0.8)
        self.wait(0.8)

        # 一般項：m = n+1
        g1 = Tex(R"C_n=-\frac{1}{2}[x^{n+1}]\sqrt{1-4x}", font_size=38)
        g2 = Tex(R"=-\frac{1}{2}\cdot\left(-\frac{2}{n+1}\binom{2n}{n}\right)", font_size=38)
        g3 = Tex(R"=\frac{1}{n+1}\binom{2n}{n}", font_size=46)
        general = VGroup(g1, g2, g3).arrange(RIGHT, buff=0.2)
        g3.shift(0.25 * RIGHT)
        general.move_to(2.05 * DOWN)
        g3_box = SurroundingRectangle(g3, buff=0.15, color=YELLOW, stroke_width=3)
        check_inside(general, g3_box)
        check_apart(g2, g3_box)
        check_apart(id_target, general)
        self.say("一般地，取 ", "$m=n+1$", " 代入上面的一般項")
        self.play(FadeIn(g1, shift=0.2 * UP), run_time=0.8)
        self.play(FadeIn(g2, shift=0.2 * UP), Indicate(id_grp, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.play(FadeIn(g3, shift=0.2 * UP), run_time=0.8)
        self.play(ShowCreation(g3_box), run_time=0.6)
        self.say("封閉形式 ", "$C_n=\\tfrac{1}{n+1}\\tbinom{2n}{n}$", "：前幾項 1, 1, 2, 5, 14，正是卡塔蘭數")
        self.wait(2.2)
