"""
Scene F65 —— 全書回顧：一張地圖（Fulton《Young Tableaux》全書；無對應頁）
執行（在 codes/ 內）：manimgl scenes/sceneF65_book_map.py SceneF65BookMap
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.scene_base import ChuScene
from utils.schubert import box_product, pipe_dreams, pipe_weight, plucker, schubert_poly
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import lr_coefficient, row_insert, schur_poly, shape, standard_tableaux

SLOW = 7.5
OK = "#7CE38B"
ROW_COLORS = [TEAL, PINK, GOLD, BLUE_B]
# 每一排：(名稱, 範圍, [(站名, 第一幕, 最後一幕, 公式)])
ROWS = [
    ("組合", [("插入與滑動", 1, 8, r"123\leftarrow 2"), ("字與 Knuth", 9, 15, r"xzy\equiv zxy"),
              ("R-S-K", 16, 19, r"A\leftrightarrow(P,Q)"), ("LR 與對稱函數", 20, 27, r"s_\lambda s_\mu=\sum c^\nu_{\lambda\mu}s_\nu")]),
    ("表示", [("Specht 模與 Young 規則", 28, 34, r"S^\lambda,\ \dim S^\lambda=f^\lambda"), ("Frobenius 與拉直", 35, 41, r"\chi^\lambda\leftrightarrow s_\lambda"),
              ("Schur 模與 GL", 42, 45, r"E^\lambda,\ \mathrm{char}\,E^\lambda=s_\lambda")]),
    ("幾何", [("Plücker 與 Grassmannian", 46, 49, r"\sigma_1^4=2\,\sigma_{22}"), ("旗流形與差商", 50, 51, r"\partial_i f=\frac{f-s_if}{x_i-x_{i+1}}"),
              ("Schubert 多項式", 52, 55, r"\mathfrak S_{2413}=s_{21}(x_1,x_2)")]),
    ("附錄", [("組合變形", 56, 60, r"T^*,\ (R,S)"), ("鑰匙", 61, 61, r"K_-(T),\ K_+(T)"),
              ("拓撲", 62, 64, r"[V]\cdot[W],\ c(E)")]),
]
THREADS = [
    ("同一條交換關係", TEAL, [("Specht 模的拉直（第 7 章）", r"S^\lambda"), ("Schur 模的二次關係（第 8 章）", r"E^\lambda"),
                         ("Plücker 關係（第 9 章）", r"p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0")]),
    ("同一個 LR 係數", PINK, [("表的乘法（第 5 章）", r"s_\lambda s_\mu=\sum c^\nu_{\lambda\mu}s_\nu"),
                         ("表示的分解（第 7–8 章）", r"E^\lambda\otimes E^\mu=\bigoplus_\nu c^\nu_{\lambda\mu}E^\nu"),
                         ("Schubert 計算（第 9 章）", r"\sigma_\lambda\sigma_\mu=\sum c^\nu_{\lambda\mu}\sigma_\nu")]),
    ("同一個「2」", GOLD, [("四條線（第 9 章）", r"\sigma_1^4=2\,\sigma_{22}"), ("LR 係數（第 5 章）", r"c^{321}_{21,21}=2"),
                       ("pipe dream（第 10 章）", r"[x_1^2x_2x_3]\,\mathfrak S_{21543}=2")]),
]
W5 = (2, 1, 5, 4, 3)
FINAL_T = ((1, 2, 4), (3, 5), (6,))


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def fit(m, w, h):
    if m.get_width() > w:
        m.set_width(w)
    if m.get_height() > h:
        m.set_height(h)
    return m


def pad(f, m):
    return {tuple(e) + (0,) * (m - len(e)): c for e, c in f.items()}


def sigma1_power(k):
    cur = {(1,): 1}
    for _ in range(k - 1):
        nxt = {}
        for lam, c in cur.items():
            for nu, d in box_product(lam, (1,), 2, 2).items():
                nu = tuple(x for x in nu if x)
                nxt[nu] = nxt.get(nu, 0) + c * d
        cur = nxt
    return cur


def frange(lo, hi):
    return "F%02d" % lo if lo == hi else "F%02d–F%02d" % (lo, hi)


def check_math():
    nums = [n for _, st in ROWS for _, lo, hi, _ in st for n in range(lo, hi + 1)]
    assert nums == list(range(1, 65))                                  # 地圖蓋住 F01–F64，不重複
    assert row_insert(((1, 2, 3),), 2)[0] == ((1, 2, 2), (3,))
    assert sigma1_power(4) == {(2, 2): 2} and len(standard_tableaux((2, 2))) == 2
    assert lr_coefficient((2, 1), (2, 1), (3, 2, 1)) == 2
    assert schubert_poly(W5)[(2, 1, 1, 0, 0)] == 2
    assert len([D for D in pipe_dreams(W5) if pipe_weight(D, 5) == (2, 1, 1, 0, 0)]) == 2
    assert schubert_poly((2, 4, 1, 3)) == pad(schur_poly((2, 1), 2), 4)
    x = plucker([[1, 2, 0, 1], [0, 1, 3, 2]])
    assert x[(1, 2)] * x[(3, 4)] - x[(1, 3)] * x[(2, 4)] + x[(1, 4)] * x[(2, 3)] == 0
    assert shape(FINAL_T) == (3, 2, 1) and FINAL_T in standard_tableaux((3, 2, 1))


def card(name, lo, hi, formula, w, h, color):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12).set_stroke(color, 2).set_fill(color, 0.12)
    title = VGroup(zh(name, font_size=20), zh(frange(lo, hi), font_size=16, color=MUTED_COLOR)).arrange(RIGHT, buff=0.15)
    fit(title, w - 0.2, 0.3).move_to(box.get_top() + 0.24 * DOWN)
    body = fit(tex(formula, 26), w - 0.3, h - 0.5).move_to(box.get_center() + 0.14 * DOWN)
    return VGroup(box, title, body)


# ---------------------------------------------------------------- 1. 地圖
def build_map():
    rows = VGroup()
    for k, (name, stations) in enumerate(ROWS):
        y = 2.45 - 1.32 * k
        n = len(stations)
        w = (11.6 - 0.22 * (n - 1)) / n
        cards = VGroup(*[card(s, lo, hi, f, w, 1.05, ROW_COLORS[k]) for s, lo, hi, f in stations])
        cards.arrange(RIGHT, buff=0.22).move_to(np.array([0.9, y, 0]))
        lo, hi = stations[0][1], stations[-1][2]
        lab = VGroup(zh(name, font_size=30, color=ROW_COLORS[k]), zh(frange(lo, hi), font_size=16, color=MUTED_COLOR))
        lab.arrange(DOWN, buff=0.08).move_to(np.array([-5.95, y, 0]))
        rows.add(VGroup(lab, cards))
    arrows = VGroup(*[Arrow(rows[k][0].get_bottom(), rows[k + 1][0].get_top(), buff=0.05, stroke_width=3)
                      .set_color(GREY_B) for k in range(3)])
    assert_in_frame(rows, arrows)
    for a, b in zip(rows, rows[1:]):
        assert_apart(a[1], b[1], 0.1)
    for r in rows:
        assert_apart(r[0], r[1], 0.15)
        for c1, c2 in zip(r[1], r[1][1:]):
            assert_apart(c1, c2, 0.1)
    return rows, arrows


def part_map(scene):
    rows, arrows = build_map()
    caps = [("第 1–6 章：插入、字、R-S-K、LR 規則、對稱函數", 0.6),
            ("第 7–8 章：同樣的表變成 ", r"$S_n$", " 與 ", r"$GL$", " 的表示", 0.6),
            ("第 9–10 章：表變成旗流形裡的 Schubert 胞腔與多項式", 0.6),
            ("附錄：表的組合變形（evacuation、鑰匙）與代數簇的拓撲", 0.6)]
    scene.say("問：從第 1 章的「擠數字」走到第 10 章的「旗流形」，中間發生了什麼？", wait=SLOW * 0.6)
    for k in range(4):
        *parts, wt = caps[k]
        anims = [FadeIn(rows[k][0])] + ([GrowArrow(arrows[k - 1])] if k else [])
        scene.play(*anims, run_time=0.6)
        scene.play(LaggedStartMap(FadeIn, rows[k][1], shift=0.15 * RIGHT, lag_ratio=0.2), run_time=1.4)
        scene.say(*parts, wait=SLOW * wt)
    scene.say("每一站留下一個代表公式：同一種表，一路被重新解讀", wait=SLOW * 0.7)
    pts = [c.get_center() for r in rows for c in r[1]]
    path = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 3, opacity=0.8)
    dot = Dot(pts[0], radius=0.1).set_color(YELLOW)
    scene.say("全系列 64 幕：從擠數字一路走到旗流形的拓撲", wait=0)
    scene.play(ShowCreation(path), MoveAlongPath(dot, path), run_time=4.5, rate_func=linear)
    scene.play(FadeOut(path), FadeOut(dot), run_time=0.6)
    scene.wait(SLOW * 0.4)
    return rows


# ---------------------------------------------------------------- 2. 三條線
def thread_band(k, title, color, nodes):
    y = 1.95 - 2.0 * k
    head = zh(title, font_size=28, color=color).move_to(np.array([-6.6, y + 0.62, 0]), aligned_edge=LEFT)
    boxes = VGroup()
    for j, (name, f) in enumerate(nodes):
        lab = zh(name, font_size=20, color=MUTED_COLOR)
        body = fit(tex(f, 30), 3.7, 0.6)
        inner = VGroup(lab, body).arrange(DOWN, buff=0.12)
        rect = RoundedRectangle(width=4.05, height=1.15, corner_radius=0.12).set_stroke(color, 2.5).set_fill(color, 0.1)
        rect.move_to(np.array([-4.45 + 4.45 * j, y - 0.2, 0]))
        inner.move_to(rect.get_center())
        boxes.add(VGroup(rect, inner))
    links = VGroup(*[Line(boxes[j][0].get_right(), boxes[j + 1][0].get_left()).set_stroke(color, 4) for j in range(2)])
    return VGroup(head, boxes, links)


def part_threads(scene):
    bands = VGroup(*[thread_band(k, *t) for k, t in enumerate(THREADS)])
    assert_in_frame(bands)
    for a, b in zip(bands, bands[1:]):
        assert_apart(a, b, 0.1)
    for b in bands:
        assert_apart(b[0], b[1], 0.05)
        for x, y in zip(b[1], b[1][1:]):
            assert_apart(x, y, 0.2)

    scene.say("三條貫穿全書的線", wait=SLOW * 0.2)
    texts = [("同一條交換關係：拉直、二次關係、Plücker 關係，其實是同一條", 0.8),
             ("同一個 LR 係數：表的乘法、表示的分解、Schubert 計算", 0.8),
             ("同一個「2」：四條線、", r"$c^{321}_{21,21}$", "、兩張 pipe dream", 0.8)]
    more = [("Specht 模與 Schur 模用「交換」關係寫出來；在 ", "$Gr(2,4)$", " 上它就是 Plücker 關係", 0.7),
            ("同一個數 ", r"$c^\nu_{\lambda\mu}$", "：數 LR 表、數表示的重數、數 Schubert 類的交點", 0.7),
            ("四條一般直線有 2 條公共割線；", r"$\mathfrak S_{21543}$", " 的 ", r"$x_1^2x_2x_3$", " 有兩張 pipe dream", 0.8)]
    for k, b in enumerate(bands):
        scene.play(FadeIn(b[0], shift=0.2 * RIGHT), run_time=0.6)
        for j in range(3):
            anims = [FadeIn(b[1][j], shift=0.15 * RIGHT)] + ([ShowCreation(b[2][j - 1])] if j else [])
            scene.play(*anims, run_time=0.7)
        *parts, wt = texts[k]
        scene.say(*parts, wait=SLOW * wt)
        *parts, wt = more[k]
        scene.say(*parts, wait=SLOW * wt)
    scene.play(*[Indicate(b[1][j][1][1], color=YELLOW) for j in range(3) for b in bands[2:]], run_time=1.2)
    scene.say("組合裡數出來的數，在表示論與幾何裡又出現一次", wait=SLOW * 0.7)


# ---------------------------------------------------------------- 3. 收束
def part_finale(scene):
    t = tableau_mob(FINAL_T, cs=0.75).move_to(np.array([0, 0.55, 0]))
    labs = VGroup(zh("組合", font_size=34, color=ROW_COLORS[0]).move_to(np.array([-3.6, 1.6, 0])),
                  zh("表示", font_size=34, color=ROW_COLORS[1]).move_to(np.array([3.6, 1.6, 0])),
                  zh("幾何", font_size=34, color=ROW_COLORS[2]).move_to(np.array([0, -1.65, 0])))
    links = VGroup(*[Line(t.get_center(), l.get_center(), buff=0.0).set_stroke(GREY_C, 2) for l in labs])
    for ln, l in zip(links, labs):
        u = l.get_center() - t.get_center()
        u = u / np.linalg.norm(u)
        ln.put_start_and_end_on(t.get_center() + 1.25 * u, l.get_center() - 0.55 * u)
    end = zh("全系列完", font_size=40, color=OK).move_to(np.array([0, -2.55, 0]))
    assert_in_frame(t, labs, links, end)
    for l in labs:
        assert_apart(t, l, 0.3)
    assert_apart(labs, end, 0.15)

    scene.play(FadeIn(t), run_time=1.0)
    scene.play(LaggedStartMap(ShowCreation, links, lag_ratio=0.3), LaggedStartMap(FadeIn, labs, lag_ratio=0.3), run_time=1.5)
    scene.say("同一張表：在組合裡是填法，在表示論裡是基底，在幾何裡是胞腔", wait=SLOW * 0.8)
    scene.say("收束：Young 表是組合、表示與幾何共用的語言", wait=SLOW * 0.9)
    scene.play(FadeIn(end, shift=0.2 * UP), run_time=1.0)
    scene.say("全系列完", wait=SLOW * 0.5)


class SceneF65BookMap(ChuScene):
    def construct(self):
        self.show_header("全書回顧：一張地圖")
        check_math()
        part_map(self)
        self.clear_stage()
        part_threads(self)
        self.clear_stage()
        part_finale(self)
        self.wait(1.0)
