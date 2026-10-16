"""
Scene F59 —— 從四個角看矩陣（Fulton §A.4.2 定理 1，書 p.201–203）
執行（在 codes/ 內）：manimgl scenes/sceneF59_four_corners.py SceneF59FourCorners
"""
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import burge, corners, evacuation, matrix_to_pairs, rsk_array
from utils.fulton_draw import BallMatrixMob, assert_apart, assert_in_frame, tableau_mob, tuple_str
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import ball_numbering, shape

SLOW = 11.5
ACC = YELLOW
DIAG1 = TEAL_B
DIAG2 = ORANGE
A = [[1, 2, 0], [0, 1, 1], [1, 1, 1]]
LABEL = {"nw": "(P,Q)", "se": "(P^*,Q^*)", "sw": "(R,S^*)", "ne": "(R^*,S)"}
NAME = {"nw": "左上", "se": "右下", "sw": "左下", "ne": "右上"}
CENTER = {"nw": (-4.4, 1.85), "ne": (4.4, 1.85), "sw": (-4.4, -1.6), "se": (4.4, -1.6)}
DIRS = {"nw": UL, "ne": UR, "sw": DL, "se": DR}


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def two_by_two_checks():
    n = 0
    for a in product(range(3), repeat=4):
        B = [list(a[:2]), list(a[2:])]
        if not any(a):
            continue
        P, Q = rsk_array(*zip(*matrix_to_pairs(B)))
        R, S = burge(B)
        c = corners(B)
        assert c["nw"] == (P, Q) and c["se"] == (evacuation(P, 2), evacuation(Q, 2))
        assert c["sw"] == (R, evacuation(S, 2)) and c["ne"] == (evacuation(R, 2), S)
        n += 1
    return n


def check_math():
    c = corners(A)
    P, Q = rsk_array(*zip(*matrix_to_pairs(A)))
    R, S = burge(A)
    assert P == ((1, 1, 2, 2, 2, 3), (2, 3)) and Q == ((1, 1, 1, 2, 2, 3), (3, 3))
    assert c["nw"] == (P, Q) and c["se"] == (evacuation(P, 3), evacuation(Q, 3))
    assert evacuation(P, 3) == P and evacuation(Q, 3) == ((1, 1, 1, 3, 3, 3), (2, 2))
    assert c["sw"] == (R, evacuation(S, 3)) and evacuation(S, 3) == ((1, 1, 1, 2, 3), (2, 3), (3,))
    assert c["ne"] == (evacuation(R, 3), S) and evacuation(R, 3) == ((1, 1, 2, 2, 3), (2, 2), (3,))
    assert R == ((1, 1, 2, 2, 2), (2, 3), (3,)) and S == ((1, 1, 1, 3, 3), (2, 2), (3,))
    assert two_by_two_checks() == 80


def corner_block(key, cs=0.37):
    T1, T2 = corners(A)[key]
    t1, t2 = tableau_mob(T1, cs=cs), tableau_mob(T2, cs=cs)
    pair = VGroup(t1, t2).arrange(RIGHT, buff=0.3, aligned_edge=UP)
    name = zh(NAME[key] + "角", font_size=26, color=ACC)
    name.next_to(pair, UP, buff=0.18)
    g = VGroup(name, pair)
    g.move_to(np.array([*CENTER[key], 0]))
    g.name, g.pair = name, pair
    return g


# ---------------------------------------------------------------- 1. 回顧矩陣球
def part_recall(scene):
    M = BallMatrixMob(A, numbering=ball_numbering(A), cell=0.95, center=np.array([-2.6, 0.2, 0]))
    note = VGroup(
        mixed("R-S-K 的矩陣球：", font_size=28),
        mixed("從左上角（西北）開始，", font_size=28),
        mixed("一層一層地編號", font_size=28),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(np.array([3.0, 0.4, 0]))
    assert_in_frame(M, note)
    assert_apart(M, note, 0.5)
    scene.say("問：R-S-K 的矩陣球是從左上角開始編號；", wait=SLOW * 0.25)
    scene.play(FadeIn(M.grid), FadeIn(M.labels), run_time=0.8)
    scene.play(LaggedStart(*[GrowFromCenter(b) for b in M.balls], lag_ratio=0.15), run_time=1.6)
    scene.play(FadeIn(note), run_time=0.8)
    scene.say("每個球的號碼＝它左上方（西北）所有球的最大號碼再加 1", wait=SLOW * 0.3)
    scene.say("R-S-K 的 ", "$(P,Q)$", " 就從這些號碼一層一層讀出來", wait=SLOW * 0.3)
    scene.say("如果從另外三個角開始呢？", wait=SLOW * 0.35)


# ---------------------------------------------------------------- 2. 四個觀察者
def part_corners(scene):
    M = BallMatrixMob(A, cell=0.75, center=np.array([0, 0.2, 0]), show_labels=False)
    arrows = {}
    for k, d in DIRS.items():
        corner = M.grid.get_corner(d)
        arrows[k] = Arrow(corner + 0.6 * d, corner + 0.05 * d, buff=0).set_color(ACC)
    blocks = {k: corner_block(k) for k in DIRS}
    assert_in_frame(M, *arrows.values(), *blocks.values())
    for k in DIRS:
        assert_apart(blocks[k], M, 0.4)
        assert_apart(blocks[k], arrows[k], 0.15)
    assert_apart(blocks["nw"], blocks["sw"], 0.3)
    assert_apart(blocks["nw"], blocks["ne"], 0.5)

    scene.say("同一個 ", "$A$", "，四個角各站一個觀察者", wait=SLOW * 0.2)
    scene.play(FadeIn(M), run_time=0.8)
    scene.play(*[GrowArrow(a) for a in arrows.values()], run_time=0.9)
    plan = [
        ("nw", None, ("左上角：照常做 R-S-K，得到 ", "$P=112223/23$", "，", "$Q=111223/33$")),
        ("se", (PI, OUT), ("右下角：上下、左右都倒過來（", r"$i\mapsto 4-i,\ j\mapsto 4-j$", "）再做 R-S-K")),
        ("sw", (PI, RIGHT), ("左下角：只把列倒過來（", r"$i\mapsto 4-i$", "）再做 R-S-K")),
        ("ne", (PI, UP), ("右上角：只把行倒過來（", r"$j\mapsto 4-j$", "）再做 R-S-K")),
    ]
    for key, rot, cap in plan:
        scene.play(Indicate(arrows[key], scale_factor=1.3), run_time=0.7)
        scene.say(*cap, wait=0.3)
        if rot is not None:
            scene.play(Rotate(M, rot[0], axis=rot[1]), run_time=1.4)
            scene.wait(0.6)
        scene.play(FadeIn(blocks[key].name), FadeIn(blocks[key].pair, shift=0.2 * DIRS[key]), run_time=0.9)
        scene.wait(SLOW * 0.2)
        T1, T2 = corners(A)[key]
        assert shape(T1) == shape(T2)
        scene.say(NAME[key] + "角得到兩張形狀 ", "$" + tuple_str(shape(T1)) + "$", " 的表", wait=SLOW * 0.2)
        if rot is not None:
            scene.play(Rotate(M, -rot[0], axis=rot[1]), run_time=1.0)
    return M, arrows, blocks


# ---------------------------------------------------------------- 3. 揭曉關係
def part_reveal(scene, M, arrows, blocks):
    R, S = burge(A)
    tr, ts = tableau_mob(R, cs=0.34), tableau_mob(S, cs=0.34)
    lr, ls = tex("R=", 30), tex("S=", 30)
    rs = VGroup(VGroup(lr, tr).arrange(RIGHT, buff=0.15), VGroup(ls, ts).arrange(RIGHT, buff=0.15))
    rs.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(np.array([0, 0.15, 0]))
    bl = zh("Burge", font_size=26, color=DIAG2).next_to(rs, UP, buff=0.25)
    news = {}
    for k in DIRS:
        col = DIAG1 if k in ("nw", "se") else DIAG2
        news[k] = tex(LABEL[k], 30, col).move_to(blocks[k].name)
    assert_in_frame(rs, bl, *news.values())
    for k in DIRS:
        assert_apart(VGroup(rs, bl), blocks[k], 0.2)

    scene.say("揭曉：對角的兩個只差一個 ", "$*$", "（evacuation）", wait=SLOW * 0.2)
    scene.play(Transform(blocks["nw"].name, news["nw"]), Transform(blocks["se"].name, news["se"]), run_time=1.0)
    scene.play(Indicate(blocks["nw"].pair, color=DIAG1), Indicate(blocks["se"].pair, color=DIAG1), run_time=1.2)
    scene.say("右下角是 ", "$(P^*,Q^*)$", "：這個例子恰好 ", "$P^*=P$", "，", "$Q^*=111333/22$", wait=SLOW * 0.45)
    scene.play(FadeOut(M), *[FadeOut(a) for a in arrows.values()], run_time=0.7)
    scene.play(FadeIn(bl), FadeIn(rs), run_time=0.9)
    scene.say("左下、右上用的是 Burge 的 ", "$(R,S)$", "（上一幕）", wait=SLOW * 0.3)
    scene.play(Transform(blocks["sw"].name, news["sw"]), Transform(blocks["ne"].name, news["ne"]), run_time=1.0)
    assert blocks["sw"].pair[0].lam == tr.lam and corners(A)["sw"][0] == R and corners(A)["ne"][1] == S
    scene.play(Indicate(blocks["sw"].pair[0], color=DIAG2), Indicate(tr, color=DIAG2), run_time=1.2)
    scene.say("左下 ", "$(R,S^*)$", "：第一張就是 ", "$R$", "，第二張 ", "$S^*=11123/23/3$", wait=SLOW * 0.35)
    scene.play(Indicate(blocks["ne"].pair[1], color=DIAG2), Indicate(ts, color=DIAG2), run_time=1.2)
    scene.say("右上 ", "$(R^*,S)$", "：第二張就是 ", "$S$", "，第一張 ", "$R^*=11223/22/3$", wait=SLOW * 0.35)
    scene.say("所以 Burge 的 ", "$R$", " 從左下角讀、", "$S$", " 從右上角讀", wait=SLOW * 0.3)


# ---------------------------------------------------------------- 4. 定理 1
def part_summary(scene):
    title = mixed("定理 1（§A.4.2）", font_size=32, color=ACC).move_to(np.array([0, 2.45, 0]))
    cells = {}
    pos = {"nw": (-2.4, 1.1), "ne": (2.4, 1.1), "sw": (-2.4, -0.6), "se": (2.4, -0.6)}
    for k, (x, y) in pos.items():
        col = DIAG1 if k in ("nw", "se") else DIAG2
        cells[k] = VGroup(zh(NAME[k], font_size=26, color=MUTED_COLOR), tex(LABEL[k], 40, col)).arrange(
            RIGHT, buff=0.35).move_to(np.array([x, y, 0]))
    h = Line(np.array([-4.6, 0.25, 0]), np.array([4.6, 0.25, 0])).set_stroke(GREY_C, 2)
    v = Line(np.array([0, 1.8, 0]), np.array([0, -1.3, 0])).set_stroke(GREY_C, 2)
    chk = mixed("程式核對：全部 ", "$80$", " 個 ", r"$2\times2$", " 矩陣（元素 ", "$0..2$", "）都成立",
                font_size=26, color=MUTED_COLOR).move_to(np.array([0, -2.3, 0]))
    assert_in_frame(title, *cells.values(), h, v, chk)
    assert_apart(title, VGroup(*cells.values(), v), 0.15)
    assert_apart(VGroup(*cells.values(), h, v), chk, 0.3)
    scene.say("整理成一張表", wait=0.3)
    scene.play(FadeIn(title), ShowCreation(h), ShowCreation(v), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(cells[k]) for k in ("nw", "se", "sw", "ne")], lag_ratio=0.4), run_time=1.8)
    scene.say("對角線：", "$(P,Q)$", " 與 ", "$(P^*,Q^*)$", "；", "$(R,S^*)$", " 與 ", "$(R^*,S)$", wait=SLOW * 0.4)
    scene.play(FadeIn(chk), run_time=0.7)
    scene.say("程式用所有 ", r"$2\times2$", "（元素 ", "$0..2$", "）的矩陣核對過定理 1", wait=SLOW * 0.4)
    scene.say("收束：四個角，兩個對應，再加上 ", "$*$", wait=SLOW * 0.5)


class SceneF59FourCorners(ChuScene):
    def construct(self):
        self.show_header("F59 從四個角看矩陣")
        check_math()
        part_recall(self)
        self.clear_stage()
        M, arrows, blocks = part_corners(self)
        part_reveal(self, M, arrows, blocks)
        self.clear_stage()
        part_summary(self)
        self.wait(1.0)
