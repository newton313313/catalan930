"""
Scene M01 —— 冪級數的乘法（Cauchy 乘積）：C² 的係數就是卡塔蘭遞迴（MIT 18.212 第 1 講）

    把 C(x) 的項排成乘法表：第 i 列 × 第 j 行 = C_i C_j x^{i+j}
    次方相同的格子在同一條反對角線 i+j=n 上：[x^n] C² = sum_{k=0}^{n} C_k C_{n-k}
    和遞迴 C_{n+1} = sum_{k=0}^{n} C_k C_{n-k} 一比 -> C - 1 = x C² -> C = 1 + x C²
    青色 = 左邊的因子 C_k，粉紅 = 右邊的因子 C_{n-k}（互相獨立 -> 相乘）

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM01_cauchy_product.py SceneM01CauchyProduct
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan, series_mul
from utils.mit_draw import LEFT_COLOR, RIGHT_COLOR
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, YELLOW, mixed, zh

N_TAB = 4                                        # 乘法表 4×4：i, j = 0..3
CAT = [catalan(n) for n in range(N_TAB + 1)]     # C_0..C_4
SQ = series_mul(CAT, CAT, N_TAB)                 # [x^n] C²，n = 0..3

HEAD_W, CELL_W, CELL_H = 1.2, 1.4, 0.75          # 表頭欄寬、格寬、格高
TAB_LEFT, HEAD_Y = -6.6, 1.55                    # 表的左緣、表頭列的 y
PANEL_L, PANEL_R = 0.55, 6.7                     # 右側算式區
X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2
CAP_FS = 32 * 1.3                                # 字幕裡數學式的大小（同 styles.mixed）


# ---------------------------------------------------------------------------- 小工具
def xpow(k: int) -> str:
    return "" if k == 0 else ("x" if k == 1 else f"x^{k}")


def term_str(coef: int, k: int) -> str:
    """係數 coef 的 x^k 項（係數 1 且 k>0 時省略 1）"""
    return (str(coef) if (coef != 1 or k == 0) else "") + xpow(k)


def split_tex(pieces, font_size=36, color=WHITE):
    """整串一起編譯（間距正常），再依各段的字形數切開，方便分段上色、分段出現。"""
    full = Tex("".join(pieces), font_size=font_size, fill_color=color)
    counts = [len(Tex(p, font_size=font_size)) for p in pieces]
    assert sum(counts) == len(full), (pieces, counts, len(full))
    parts, a = [], 0
    for c in counts:
        parts.append(full[a:a + c])
        a += c
    return full, parts


def color_ck(piece):
    """「C_iC_j…」：前兩個字形（C_i）青、後兩個（C_j）粉紅"""
    piece[0:2].set_fill(LEFT_COLOR)
    piece[2:4].set_fill(RIGHT_COLOR)
    return piece


def ctex(s: str, color=WHITE) -> Tex:
    """字幕裡用的彩色數學式"""
    return Tex(s, font_size=CAP_FS, fill_color=color)


def in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def no_overlap(a, b, gap=0.05):
    sep_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    sep_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert sep_x or sep_y, (a, b)


def cell_center(i, j):
    return np.array([TAB_LEFT + HEAD_W + (j + 0.5) * CELL_W, HEAD_Y - (i + 1) * CELL_H, 0.0])


def build_table():
    """乘法表：列頭 C_i x^i（青）、行頭 C_j x^j（粉紅）、格子 C_iC_j x^{i+j}"""
    row_heads, col_heads = VGroup(), VGroup()
    for i in range(N_TAB):
        y = HEAD_Y - (i + 1) * CELL_H
        row_heads.add(Tex(f"C_{i}" + xpow(i), font_size=32, fill_color=LEFT_COLOR)
                      .move_to(np.array([TAB_LEFT + HEAD_W / 2, y, 0.0])))
    for j in range(N_TAB):
        col_heads.add(Tex(f"C_{j}" + xpow(j), font_size=32, fill_color=RIGHT_COLOR)
                      .move_to(np.array([cell_center(0, j)[0], HEAD_Y, 0.0])))
    corner = Tex(R"\times", font_size=36, fill_color=MUTED_COLOR)
    corner.move_to(np.array([TAB_LEFT + HEAD_W / 2, HEAD_Y, 0.0]))
    rects, terms = {}, {}
    for i in range(N_TAB):
        for j in range(N_TAB):
            rects[(i, j)] = Rectangle(width=CELL_W, height=CELL_H, stroke_color=GREY_C, stroke_width=1.5,
                                      fill_color=YELLOW, fill_opacity=0).move_to(cell_center(i, j))
            terms[(i, j)] = color_ck(Tex(f"C_{i}C_{j}" + xpow(i + j), font_size=30)).move_to(cell_center(i, j))
            assert terms[(i, j)].get_width() < CELL_W - 0.15
    return row_heads, col_heads, corner, rects, terms


def diag_lines(n):
    """第 n 條反對角線的算式：[x^n]C² = C_0C_n + … ；= 數值 + … = SQ[n]"""
    p1 = [f"[{xpow(n) or 'x^0'}]C^2", "="]          # n=1 寫成 [x]，不寫 [x^1]
    for k in range(n + 1):
        if k:
            p1.append("+")
        p1.append(f"C_{k}C_{n - k}")
    line1, parts1 = split_tex(p1, font_size=34)
    term_parts = [parts1[2 + 2 * k] for k in range(n + 1)]
    for t in term_parts:
        color_ck(t)
    prods = [CAT[k] * CAT[n - k] for k in range(n + 1)]
    assert sum(prods) == SQ[n]
    p2 = ["="]
    if n > 0:
        for k, v in enumerate(prods):
            if k:
                p2.append("+")
            p2.append(str(v))
        p2.append("=")
    p2.append(str(SQ[n]))
    line2, parts2 = split_tex(p2, font_size=34)
    parts2[-1].set_fill(YELLOW)
    line1.move_to(np.array([0.0, 0.7, 0.0]))
    line1.shift((PANEL_L + 0.1 - line1.get_left()[0]) * RIGHT)
    line2.move_to(np.array([0.0, -0.05, 0.0]))
    line2.shift((parts1[1].get_center()[0] - parts2[0].get_center()[0]) * RIGHT)
    assert line1.get_right()[0] <= PANEL_R and line2.get_right()[0] <= PANEL_R, n
    return line1, parts1, term_parts, line2, parts2


def place_series(pieces, powers, y, font_size=40, eq_x=-3.7, col0=-2.7, col_w=1.6):
    """
    冪級數排成一欄一欄：pieces = [左邊, "=", 項, "+", 項, …, "+", "\\cdots"]，
    powers[t] 是第 t 個項的次方；x^p 的項放在第 p 欄，上下對齊（只橫移，基線不變）。
    """
    full, parts = split_tex(pieces, font_size=font_size)
    full.move_to(np.array([0.0, y, 0.0]))

    def to_x(m, x):
        m.shift((x - m.get_center()[0]) * RIGHT)

    parts[0].shift((eq_x - 0.28 - parts[0].get_right()[0]) * RIGHT)
    to_x(parts[1], eq_x)
    body = parts[2:]
    t = 0
    for idx, m in enumerate(body):
        if idx % 2 == 0:                      # 項（最後一個是 \cdots）
            p = powers[t] if t < len(powers) else powers[-1] + 1
            to_x(m, col0 + p * col_w)
            t += 1
        else:                                 # 加號：放在兩欄中間
            to_x(m, col0 + (powers[t - 1] + 0.5) * col_w)
    return full, parts


# ---------------------------------------------------------------------------- 場景
class SceneM01CauchyProduct(ChuScene):
    def construct(self):
        self.show_header("冪級數的乘法：Cauchy 乘積")
        assert CAT == [1, 1, 2, 5, 14]
        assert SQ == [1, 2, 5, 14]
        assert [CAT[k] * CAT[2 - k] for k in range(3)] == [2, 1, 2]
        assert all(SQ[n] == CAT[n + 1] for n in range(N_TAB))

        # ------------------------------------------------------------ C(x)
        gf_pieces = ["C(x)=", "C_0+C_1x+C_2x^2+C_3x^3+\\cdots", "="]
        gf_pieces.append("+".join(term_str(CAT[k], k) for k in range(N_TAB)) + "+\\cdots")
        assert gf_pieces[-1] == "1+x+2x^2+5x^3+\\cdots"
        gf, gf_parts = split_tex(gf_pieces, font_size=40)
        gf.move_to(np.array([0.0, 2.65, 0.0]))
        self.say("把 ", "$C(x)$", " 自己乘自己：", "$C(x)^2$", " 的係數是多少？")
        self.play(Write(gf), run_time=1.3)
        self.wait(0.4)

        # ------------------------------------------------------------ 乘法表
        row_heads, col_heads, corner, rects, terms = build_table()
        table = VGroup(row_heads, col_heads, corner, *rects.values(), *terms.values())
        in_frame(table, gf)
        no_overlap(gf, VGroup(col_heads, corner))
        self.say("第一個 ", "$C(x)$", " 的項排成列（青），第二個排成行（粉紅）")
        self.play(FadeIn(corner), LaggedStart(*[FadeIn(h, shift=0.2 * RIGHT) for h in row_heads], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(h, shift=0.2 * DOWN) for h in col_heads], lag_ratio=0.15), run_time=1.1)
        self.play(*[ShowCreation(r) for r in rects.values()], run_time=0.5)
        self.say("格子 ", "$(i,j)$", " 放兩項的乘積 ", ctex("C_i", LEFT_COLOR), ctex("C_j", RIGHT_COLOR),
                 ctex("x^{i+j}"))
        self.play(LaggedStart(*[FadeIn(terms[(i, j)], scale=0.8) for i in range(N_TAB) for j in range(N_TAB)],
                              lag_ratio=0.06), run_time=1.3)
        self.wait(0.4)

        # ------------------------------------------------------------ 反對角線 i+j=n
        sq_pieces = ["C^2", "="]
        for n in range(N_TAB):
            sq_pieces.append(("+" if n else "") + term_str(SQ[n], n))
        sq_pieces.append("+\\cdots")
        assert "".join(sq_pieces) == "C^2=1+2x+5x^2+14x^3+\\cdots"
        sq_line, sq_parts = split_tex(sq_pieces, font_size=38)
        sq_line.move_to(np.array([0.0, HEAD_Y, 0.0]))
        sq_line.shift((PANEL_L + 0.1 - sq_line.get_left()[0]) * RIGHT)
        assert sq_line.get_right()[0] <= PANEL_R
        self.say("同一條反對角線 ", "$i+j=n$", " 上的格子，次方都是 ", "$x^n$")
        self.play(FadeIn(VGroup(sq_parts[0], sq_parts[1])), run_time=0.5)

        captions = {
            0: None,                      # n=0 沿用「同一條反對角線」的字幕，讓它停留夠久
            1: ("$x$", " 的係數：兩格相加"),
            2: ("$x^2$", " 的係數：三格相加，", "$2+1+2=5$"),
            3: ("$x^3$", " 的係數：四格相加，", "$5+2+2+5=14$"),
        }
        prev, shown = [], None
        for n in range(N_TAB):
            diag = [(k, n - k) for k in range(n + 1)]
            line1, parts1, term_parts, line2, parts2 = diag_lines(n)
            anims = [rects[c].animate.set_fill(YELLOW, opacity=0.25) for c in diag]
            anims += [rects[c].animate.set_fill(opacity=0) for c in prev]
            if shown is not None:
                anims.append(FadeOut(shown))
            if captions[n]:
                self.say(*captions[n])
            self.play(*anims, run_time=0.6)
            slow = 1.4 if n == 2 else 1.0
            others = [p for idx, p in enumerate(parts1) if idx < 2 or idx % 2 == 1]
            self.play(FadeIn(VGroup(*others)),
                      *[TransformFromCopy(terms[c][0:4], t) for c, t in zip(diag, term_parts)],
                      run_time=0.9 * slow)
            if n == 2:
                self.wait(0.5)
            self.play(Write(line2), run_time=0.7 * slow)
            if n == 2:
                self.wait(0.6)
            self.play(TransformFromCopy(parts2[-1], sq_parts[2 + n]), run_time=0.7)
            self.wait(0.2 if n < 2 else 0.5)
            prev, shown = diag, VGroup(line1, line2)
        self.play(FadeOut(shown), *[rects[c].animate.set_fill(opacity=0) for c in prev],
                  FadeIn(sq_parts[-1]), run_time=0.6)

        # ------------------------------------------------------------ 一般式
        gen, gen_parts = split_tex(["[x^n]C^2", "=", "\\sum_{k=0}^{n}", "C_k", "C_{n-k}"], font_size=44)
        gen_parts[3].set_fill(LEFT_COLOR)
        gen_parts[4].set_fill(RIGHT_COLOR)
        gen.move_to(np.array([(PANEL_L + PANEL_R) / 2, 0.15, 0.0]))
        gen_box = SurroundingRectangle(gen, buff=0.22, color=YELLOW, stroke_width=3)
        in_frame(gen_box)
        no_overlap(gen_box, sq_line)
        self.say("一般來說：左邊取 ", ctex("C_k", LEFT_COLOR), "、右邊取 ", ctex("C_{n-k}", RIGHT_COLOR),
                 "，", "$k$", " 從 ", "$0$", " 到 ", "$n$")
        self.play(Write(gen), run_time=1.2)
        self.play(ShowCreation(gen_box), run_time=0.5)
        self.wait(1.0)

        # ------------------------------------------------------------ 對照遞迴
        eq_x = -0.6
        self.play(FadeOut(VGroup(table, gf, *sq_parts, gen_box)),
                  gen.animate.shift(np.array([eq_x - gen_parts[1].get_center()[0], 2.4 - gen.get_center()[1], 0.0])),
                  run_time=0.9)
        rec, rec_parts = split_tex(["C_{n+1}", "=", "\\sum_{k=0}^{n}", "C_k", "C_{n-k}"], font_size=44)
        rec_parts[3].set_fill(LEFT_COLOR)
        rec_parts[4].set_fill(RIGHT_COLOR)
        rec.move_to(np.array([0.0, 0.75, 0.0]))
        rec.shift((eq_x - rec_parts[1].get_center()[0]) * RIGHT)
        br_l = Brace(rec_parts[3], DOWN, buff=0.12).set_fill(LEFT_COLOR)
        br_r = Brace(rec_parts[4], DOWN, buff=0.12).set_fill(RIGHT_COLOR)
        lab_l = zh("左邊", font_size=24, color=LEFT_COLOR).next_to(br_l, DOWN, buff=0.08)
        lab_r = zh("右邊", font_size=24, color=RIGHT_COLOR).next_to(br_r, DOWN, buff=0.08)
        lab_l.shift(0.1 * LEFT)
        lab_r.shift(0.1 * RIGHT)
        no_overlap(lab_l, lab_r)
        no_overlap(gen, rec)
        self.say("卡塔蘭遞迴：拿掉根之後，左邊有 ", ctex("C_k", LEFT_COLOR), " 種、右邊有 ",
                 ctex("C_{n-k}", RIGHT_COLOR), " 種")
        self.play(Write(rec), run_time=1.1)
        self.play(GrowFromCenter(br_l), GrowFromCenter(br_r), FadeIn(lab_l), FadeIn(lab_r), run_time=0.7)
        self.say("左右互相獨立，方法數相乘，再對 ", "$k$", " 加總")
        self.wait(1.6)

        box_a = SurroundingRectangle(VGroup(*gen_parts[2:]), buff=0.06, color=YELLOW, stroke_width=3)
        box_b = SurroundingRectangle(VGroup(*rec_parts[2:]), buff=0.06, color=YELLOW, stroke_width=3)
        self.say("兩個式子的右邊一模一樣！")
        self.play(FadeOut(VGroup(br_l, br_r, lab_l, lab_r)), ShowCreation(box_a), ShowCreation(box_b),
                  run_time=0.8)
        self.wait(0.6)
        res, res_parts = split_tex(["C_{n+1}", "=", "[x^n]C^2"], font_size=48)
        res.move_to(np.array([0.0, -1.0, 0.0]))
        res.shift((eq_x - res_parts[1].get_center()[0]) * RIGHT)
        no_overlap(res, VGroup(lab_l, lab_r))
        no_overlap(box_a, box_b)
        no_overlap(box_a, gen_parts[1], gap=0.08)
        no_overlap(box_b, rec_parts[1], gap=0.08)
        self.say("所以 ", "$C^2$", " 的 ", "$x^n$", " 係數就是下一個卡塔蘭數 ", "$C_{n+1}$")
        self.play(TransformFromCopy(rec_parts[0], res_parts[0]), TransformFromCopy(gen_parts[0], res_parts[2]),
                  FadeIn(res_parts[1]), run_time=1.0)
        self.wait(1.0)

        # ------------------------------------------------------------ C - 1 = x C^2
        self.play(FadeOut(VGroup(gen, rec, box_a, box_b)),
                  res.animate.move_to(np.array([0.0, 2.45, 0.0])), run_time=0.8)
        tail = ["+", "\\cdots"]
        p_sq = ["C^2", "="]
        p_xsq = ["xC^2", "="]
        for n in range(N_TAB):
            if n:
                p_sq.append("+")
                p_xsq.append("+")
            p_sq.append(term_str(SQ[n], n))
            p_xsq.append(term_str(SQ[n], n + 1))
        p_c = ["C", "="]
        for n in range(N_TAB + 1):
            if n:
                p_c.append("+")
            p_c.append(term_str(CAT[n], n))
        p_sq += tail
        p_xsq += tail
        p_c += tail
        assert "".join(p_xsq) == "xC^2=x+2x^2+5x^3+14x^4+\\cdots"
        assert "".join(p_c) == "C=1+x+2x^2+5x^3+14x^4+\\cdots"
        L0, L0p = place_series(p_sq, list(range(N_TAB)), 1.35)
        L1, L1p = place_series(p_xsq, list(range(1, N_TAB + 1)), 0.45)
        L2, L2p = place_series(p_c, list(range(N_TAB + 1)), -0.45)
        in_frame(L0, L1, L2, res)
        for a, b in [(res, L0), (L0, L1), (L1, L2)]:
            no_overlap(a, b)
        self.say("上面是剛剛算出的 ", "$C^2$", "；乘上 ", "$x$", "，每一項往右移一格")
        self.play(FadeIn(VGroup(*L0p)), run_time=0.7)
        self.play(*[TransformFromCopy(a, b) for a, b in zip(L0p, L1p)], run_time=1.2)
        self.wait(0.5)
        self.say("和 ", "$C$", " 比較：只差一個常數項 ", "$1$")
        self.play(FadeIn(VGroup(*L2p), shift=0.2 * UP), run_time=0.8)
        one_box = SurroundingRectangle(L2p[2], buff=0.1, color=YELLOW, stroke_width=3)
        same = [SurroundingRectangle(VGroup(L1p[2 + 2 * t], L2p[4 + 2 * t]), buff=0.09, color=GREY_B,
                                     stroke_width=2) for t in range(N_TAB)]
        for t, s in enumerate(same):
            for nb in (L1p[3 + 2 * t], L2p[3 + 2 * t], L2p[5 + 2 * t]):
                no_overlap(s, nb, gap=0.03)
        no_overlap(one_box, L2p[3], gap=0.03)
        self.play(ShowCreation(one_box), *[ShowCreation(s) for s in same], run_time=0.8)
        self.wait(0.6)

        eq1 = Tex("C-1=xC^2", font_size=52).move_to(np.array([0.0, -1.65, 0.0]))
        eq2 = Tex("C=1+xC^2", font_size=56).move_to(eq1)
        eq_box = SurroundingRectangle(eq2, buff=0.25, color=YELLOW, stroke_width=3)
        in_frame(eq_box)
        no_overlap(eq_box, L2)
        self.say("所以 ", "$C-1=xC^2$", "，也就是 ", "$C=1+xC^2$")
        self.play(Write(eq1), run_time=0.9)
        self.wait(0.3)
        self.play(ReplacementTransform(eq1, eq2), run_time=0.9)
        self.play(ShowCreation(eq_box), run_time=0.5)
        self.wait(2.0)
