"""
Scene M08 —— 平面樹 -> Dyck 路徑 -> 不交叉配對（MIT 18.212 第 3 講）

    沿著平面樹的輪廓走一圈（深度優先）：往下走記 U、往上走記 D -> Dyck 路徑 UUDUDD
    同一條邊「下去」的 U 和「上來」的 D 配成一對 -> 弧 (1,6),(2,3),(4,5)
    弧圖收回成圓上的不交叉配對（M06 的反向）
    一條鏈：三角剖分 <-> 二元樹 <-> 平面樹 <-> Dyck 路徑 <-> 不交叉配對

例子是 mit_plan.md 第 3 節貫穿全程的 EX = binary_trees(3)[3]（00k 第 4 欄）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM08_tree_dyck_matching.py SceneM08TreeDyckMatching
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import CATALAN_COLOR, EDGE_COLOR, catalan_item, dyck_path_mob, part_color
from utils.circle_points import label_points, make_circle_points
from utils.counting import (
    MIT_EXAMPLE_TREE,
    binary_to_plane,
    binary_trees,
    catalan,
    dyck_parts,
    dyck_to_matching,
    matching_is_noncrossing,
    matching_parts,
    matching_to_dyck,
    plane_to_binary,
    plane_tree_dfs,
    plane_tree_edges,
    plane_tree_preorder,
    plane_tree_walk,
    tree_to_dyck,
)
from utils.mit_draw import ArcDiagramMob, PlaneTreeMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, YELLOW, boxed, mixed, zh

EX = MIT_EXAMPLE_TREE
PT = binary_to_plane(EX)            # 根 -> A -> 兩片葉子
WALK_COLOR = YELLOW                 # 正在走的邊、正在配對的 U／D
UNIT = 0.75                         # Dyck 路徑一步的寬度 = 弧圖的點距
PATH_ORIGIN = np.array([0.4, 0.95, 0.0])
LETTER_Y = PATH_ORIGIN[1] - 0.42
ARC_Y = -1.75
TREE_ROOT = np.array([-4.6, 2.1, 0.0])
CIRCLE_CENTER = np.array([2.65, 0.3, 0.0])
CIRCLE_RADIUS = 1.5
CUT_ANGLE = PI / 2 + PI / 6         # 點 1（90°）與點 6（150°）之間：和 M06 剪開的位置相同
TREE_NAMES = {1: "A", 2: "B", 3: "C"}   # M07 依前序取的名字
LABEL_SIDE = {0: UP, 1: RIGHT, 2: LEFT, 3: RIGHT}


# ----------------------------------------------------------------------------- 資料
def walk_steps(pt) -> list:
    """[(u, v, 'U'/'D', 邊的下端頂點)]：第 k 步從 walk[k] 走到 walk[k+1]。"""
    walk = plane_tree_walk(pt)
    parents = [p for p, _ in plane_tree_preorder(pt)]
    steps = []
    for u, v in zip(walk, walk[1:]):
        if parents[v] == u:
            steps.append((u, v, "U", v))
        else:
            assert parents[u] == v
            steps.append((u, v, "D", u))
    return steps


def edge_pairs(steps) -> list:
    """每條邊（以下端頂點表示，依頂點編號）-> (往下那一步, 往上那一步)。"""
    down, up = {}, {}
    for k, (_, _, c, low) in enumerate(steps):
        (down if c == "U" else up)[low] = k
    assert sorted(down) == sorted(up)
    return [(down[v], up[v]) for v in sorted(down)]


def plane_parts(pt) -> dict:
    """
    平面樹頂點 v >= 1 在二元樹裡屬於 root／left／right（左小孩 = 第一個小孩、右小孩 = 下一個兄弟）：
    頂點 1 = 二元樹的根；頂點 1 的子孫 = 左子樹；根的其他小孩與它們的子孫 = 右子樹。
    """
    pre = plane_tree_preorder(pt)
    parts = {}
    for v in range(1, len(pre)):
        top = v
        while pre[top][0] != 0:
            top = pre[top][0]
        parts[v] = "root" if v == 1 else ("left" if top == 1 else "right")
    return parts


def roll_pos(u: float, alpha: float, line_left, line_len: float, center, radius: float) -> np.ndarray:
    """
    把直線（左端 line_left、長 line_len）捲成圓：直線上比例 u 的點在進度 alpha 的位置。
    中間的形狀是一段順時針的圓弧（切線方向 alpha*(CUT_ANGLE-90°-360°u)，長度由直線長變成圓周長），
    外框中心由直線中點移到圓心（先快後慢，避免掉到字幕區）。
    alpha=1 時正好是圓上角度 CUT_ANGLE - 360°u 的點，所以 u=(i+0.5)/2n 落在第 i 點。
    """
    ell = (1 - alpha) * line_len + alpha * TAU * radius
    a, b = alpha * (CUT_ANGLE - PI / 2), alpha * TAU
    if b < 1e-6:                                       # 還是直線
        rel = lambda x: ell * x * np.array([np.cos(a), np.sin(a), 0.0])
        box_mid = rel(0.5)
    else:                                              # 曲率中心 q、半徑 r，位置角從 a+90° 順時針轉 b
        r = ell / b
        q = r * np.array([np.sin(a), -np.cos(a), 0.0])
        rel = lambda x: q + r * np.array([-np.sin(a - b * x), np.cos(a - b * x), 0.0])
        phi0 = a + PI / 2
        angles = [phi0, phi0 - b] + [k * PI / 2 for k in range(-8, 9) if phi0 - b <= k * PI / 2 <= phi0]
        ext = np.array([q + r * np.array([np.cos(t), np.sin(t), 0.0]) for t in angles])
        box_mid = (ext.min(axis=0) + ext.max(axis=0)) / 2
    s = 1 - (1 - alpha) ** 2
    line_mid = np.array(line_left, dtype=float) + 0.5 * line_len * RIGHT
    return (1 - s) * line_mid + s * np.array(center, dtype=float) + rel(u) - box_mid


def bulge_points(p, q, height_ratio: float, samples: int = 25) -> list:
    """p 到 q 的壓扁半圓（凸向 p->q 的左邊，高度 = height_ratio × 半弦長）；height_ratio=0 是直線。"""
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    mid, half = (p + q) / 2, (q - p) / 2
    normal = np.array([-half[1], half[0], 0.0])
    return [mid - np.cos(t) * half + height_ratio * np.sin(t) * normal for t in np.linspace(0, PI, samples)]


# ----------------------------------------------------------------------------- 圖形
def plane_tree_item(pt, colored: bool = False) -> PlaneTreeMob:
    """鏈裡用的小平面樹；colored=True 時邊與頂點依二元樹的 根／左／右 上色。"""
    mob = PlaneTreeMob(pt, leaf_gap=0.55, level_height=0.55, node_radius=0.07, edge_width=3)
    mob.nodes[0].set_fill(WHITE)
    if colored:
        for v, part in plane_parts(pt).items():
            mob.edge_to(v).set_stroke(part_color(part))
            mob.nodes[v].set_fill(part_color(part))
    return mob


def fit_item(mob: Mobject, width: float, height: float) -> Mobject:
    if mob.get_width() / width > mob.get_height() / height:
        mob.set_width(width)
    else:
        mob.set_height(height)
    return mob


def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= -6.8 and m.get_right()[0] <= 6.8, m
        assert m.get_bottom()[1] >= -3.0 and m.get_top()[1] <= 3.2, m


def assert_apart(a: Mobject, b: Mobject, gap: float = 0.05):
    """兩個物件的外框不重疊。"""
    sep_x = max(a.get_left()[0] - b.get_right()[0], b.get_left()[0] - a.get_right()[0])
    sep_y = max(a.get_bottom()[1] - b.get_top()[1], b.get_bottom()[1] - a.get_top()[1])
    assert max(sep_x, sep_y) >= gap, (a, b)


class SceneM08TreeDyckMatching(ChuScene):
    def construct(self):
        self.show_header("平面樹 → Dyck 路徑 → 配對")

        # ------------------------------------------------------------ 數學資料
        steps = walk_steps(PT)
        word = "".join(s[2] for s in steps)
        pairs = edge_pairs(steps)
        parts = plane_parts(PT)
        assert EX == binary_trees(3)[3] and PT == (((), ()),) and plane_to_binary(PT) == EX
        assert plane_tree_edges(PT) == 3 and len(plane_tree_preorder(PT)) == 4
        assert plane_tree_walk(PT) == [0, 1, 2, 1, 3, 1, 0]
        assert word == plane_tree_dfs(PT) == tree_to_dyck(EX) == "UUDUDD"
        assert pairs == dyck_to_matching(word) == [(0, 5), (1, 2), (3, 4)]
        assert matching_to_dyck(pairs) == word and matching_is_noncrossing(pairs)
        assert [parts[s[3]] for s in steps] == dyck_parts(EX)
        assert [parts[v] for v in sorted(parts)] == matching_parts(EX)
        assert catalan(3) == 5

        # ------------------------------------------------------------ 平面樹與地面
        tree_labels = {0: zh("根", font_size=24, color=MUTED_COLOR)}
        tree_labels.update({v: zh(name, font_size=26) for v, name in TREE_NAMES.items()})
        tree = PlaneTreeMob(PT, root_pos=TREE_ROOT, leaf_gap=1.6, level_height=1.25, node_radius=0.12,
                            edge_width=5, labels=tree_labels)
        tree.nodes[0].set_fill(WHITE)
        for v, side in LABEL_SIDE.items():          # 離頂點遠一點，黃點走過時不會蓋住字
            tree.labels[v].next_to(tree.vertex(v), side, buff=0.26)
        assert sorted(tree.labels) == [0, 1, 2, 3]
        path = dyck_path_mob(word, unit=UNIT, origin=PATH_ORIGIN, color=CATALAN_COLOR, stroke_width=6,
                             dot_radius=0.06)
        ground = Line(PATH_ORIGIN + 0.3 * LEFT, PATH_ORIGIN + (len(word) * UNIT + 0.3) * RIGHT,
                      stroke_color=GREY_A, stroke_width=2.5)
        assert_in_frame(tree, path, ground)
        self.say("上一幕由三角剖分得到的平面樹：根 → A → B、C（3 條邊、4 個頂點）")
        self.play(ShowCreation(tree.edges), FadeIn(tree.nodes), FadeIn(tree.label_group), run_time=1.2)
        self.wait(1.2)

        # ------------------------------------------------------------ 沿著輪廓走
        walker = Dot(tree.vertex(0), radius=0.14, fill_color=WALK_COLOR).set_z_index(3)
        self.say("從根出發，沿著樹的輪廓走一圈：往下走記 ", "$U$", "，往上走記 ", "$D$")
        self.play(FadeIn(walker, scale=0.5), ShowCreation(ground), FadeIn(path.dots[0]), run_time=0.7)
        letters = VGroup()
        prev_edge = None
        for k, (u, v, c, low) in enumerate(steps):
            edge = tree.edge_to(low)
            mid_x = PATH_ORIGIN[0] + (k + 0.5) * UNIT
            letter = Tex(c, font_size=38).move_to(np.array([mid_x, LETTER_Y, 0.0]))
            letters.add(letter)
            anims = [walker.animate.move_to(tree.vertex(v)), ShowCreation(path.steps[k]),
                     FadeIn(path.dots[k + 1]), FadeIn(letter, shift=0.15 * (UP if c == "U" else DOWN))]
            if edge is not prev_edge:
                anims.append(edge.animate.set_stroke(WALK_COLOR))
                if prev_edge is not None:
                    anims.append(prev_edge.animate.set_stroke(EDGE_COLOR))
            self.play(*anims, run_time=1.1)
            prev_edge = edge
            self.wait(0.3)
        self.play(prev_edge.animate.set_stroke(EDGE_COLOR), run_time=0.3)
        self.say("高度＝深度，不會低於地面；走回根＝回到地面 → Dyck 路徑 ", "$UUDUDD$")
        self.play(Indicate(letters, color=WALK_COLOR, scale_factor=1.15), run_time=1.0)
        self.wait(1.2)

        # ------------------------------------------------------------ 同一條邊的 U 與 D 配對
        base = ArcDiagramMob(len(word), gap=UNIT, center=np.array([PATH_ORIGIN[0] + len(word) / 2 * UNIT, ARC_Y, 0.0]),
                             height_ratio=0.55, line_margin=UNIT / 2)
        assert all(abs(base.point(k)[0] - letters[k].get_center()[0]) < 1e-6 for k in range(len(word)))
        self.say("每條邊走兩次：下去一次（", "$U$", "）、上來一次（", "$D$", "）→ 這兩步配成一對")
        self.play(FadeIn(base.baseline), FadeIn(base.dots), FadeIn(base.labels), FadeOut(walker), run_time=0.8)
        arcs = VGroup()
        for a, b in pairs:
            low = steps[a][3]
            assert steps[b][3] == low and steps[a][2] == "U" and steps[b][2] == "D"
            hl = [tree.edge_to(low), path.steps[a], path.steps[b]]
            self.play(*[m.animate.set_stroke(WALK_COLOR) for m in hl],
                      letters[a].animate.set_fill(WALK_COLOR), letters[b].animate.set_fill(WALK_COLOR),
                      run_time=0.5)
            arc = base.make_arc(a, b, color=CATALAN_COLOR)
            self.play(ShowCreation(arc), run_time=0.8)
            arcs.add(arc)
            self.wait(0.3)
            self.play(tree.edge_to(low).animate.set_stroke(EDGE_COLOR),
                      path.steps[a].animate.set_stroke(CATALAN_COLOR), path.steps[b].animate.set_stroke(CATALAN_COLOR),
                      letters[a].animate.set_fill(WHITE), letters[b].animate.set_fill(WHITE), run_time=0.3)
        assert_in_frame(base, arcs)
        assert arcs.get_top()[1] < letters.get_bottom()[1] - 0.2

        one_based = ",\\ ".join(f"({i + 1},{j + 1})" for i, j in pairs)
        assert one_based == "(1,6),\\ (2,3),\\ (4,5)"
        result = Tex(one_based, font_size=40).move_to(np.array([TREE_ROOT[0], -1.25, 0.0]))
        assert_apart(result, tree)
        assert_apart(result, base)
        self.say("3 條邊 ↔ 3 對 ", "$(U,D)$", " ↔ 3 條弧：配對 ", "$" + one_based + "$")
        self.play(TransformFromCopy(arcs, result), run_time=1.0)
        self.wait(1.2)
        self.say("子樹走完才回頭：兩條弧不是一條包住另一條，就是分開，不會交叉")
        self.wait(1.8)
        self.say("反過來，從配對讀回：左端記 ", "$U$", "、右端記 ", "$D$", " → 一一對應")
        self.wait(1.4)

        # ------------------------------------------------------------ 弧圖收回成圓（M06 的反向）
        self.play(FadeOut(path), FadeOut(ground), FadeOut(letters), run_time=0.6)
        circle, cdots, coords = make_circle_points(len(word), radius=CIRCLE_RADIUS, center=CIRCLE_CENTER)
        clabels = label_points(coords, CIRCLE_CENTER, buff=0.32)
        assert_in_frame(VGroup(circle, clabels))
        assert_apart(VGroup(circle, clabels), result)
        # 直線從剪開處（點 6 與點 1 之間）順時針捲成圓：直線左端接到點 1、右端接到點 6（00j／M06 的點序）
        line_left, line_len = base.baseline.get_start(), base.baseline.get_length()
        n_pts = len(word)
        us = [(i + 0.5) / n_pts for i in range(n_pts)]
        roll = lambda u, al: roll_pos(u, al, line_left, line_len, CIRCLE_CENTER, CIRCLE_RADIUS)
        for i in range(n_pts):
            assert np.allclose(roll(us[i], 0.0), base.point(i), atol=1e-6)
            assert np.allclose(roll(us[i], 1.0), coords[i], atol=1e-6)
        assert np.allclose(roll(0.0, 1.0), roll(1.0, 1.0), atol=1e-6)    # 第 6 點之後接回第 1 點之前
        lab_off_line = [base.labels[i].get_center() - base.point(i) for i in range(n_pts)]
        lab_off_ring = [clabels[i].get_center() - coords[i] for i in range(n_pts)]
        c0, w0 = base.baseline.get_stroke_color(), base.baseline.get_stroke_width()
        c1, w1 = circle.get_stroke_color(), circle.get_stroke_width()
        ratio0 = 0.55
        samples = np.linspace(0, 1, 73)

        def roll_update(_mob, al):
            base.baseline.set_points_smoothly([roll(u, al) for u in samples])
            base.baseline.set_stroke(interpolate_color(c0, c1, al), width=w0 + (w1 - w0) * al)
            for i in range(n_pts):
                pos = roll(us[i], al)
                base.dots[i].move_to(pos)
                base.labels[i].move_to(pos + (1 - al) * lab_off_line[i] + al * lab_off_ring[i])
            for arc, (i, j) in zip(arcs, pairs):
                arc.set_points_smoothly(bulge_points(roll(us[i], al), roll(us[j], al), ratio0 * (1 - al)))

        self.say("把直線捲回圓上（第 6 點接回第 1 點）：弧變成弦，就是圓上的不交叉配對")
        self.play(UpdateFromAlphaFunc(VGroup(base.baseline, base.dots, base.labels, arcs), roll_update),
                  run_time=2.4)
        self.remove(base.baseline)          # 換成封閉的圓，接縫處才不會有缺口
        self.add(circle)
        self.bring_to_back(circle)
        for arc, (i, j) in zip(arcs, pairs):
            assert np.allclose(arc.get_start(), coords[i], atol=1e-6) and np.allclose(arc.get_end(), coords[j], atol=1e-6)
        self.wait(2.0)

        # ------------------------------------------------------------ 一條鏈
        self.clear_stage()
        names = ["三角剖分", "二元樹", "平面樹", "Dyck 路徑", "不交叉配對"]
        items = [
            catalan_item("triangulation", EX, scale=1.6, colored=True),
            catalan_item("tree", EX, scale=1.6, colored=True),
            plane_tree_item(PT, colored=True),
            catalan_item("dyck", EX, scale=1.6, colored=True),
            catalan_item("matching", EX, scale=1.6, colored=True),
        ]
        xs = np.linspace(-5.6, 5.6, len(items))
        chain_y = 0.7
        for mob, x in zip(items, xs):
            fit_item(mob, 1.75, 1.7).move_to(np.array([x, chain_y, 0.0]))
        name_mobs = VGroup(*[zh(t, font_size=24).next_to(np.array([x, chain_y - 1.05, 0.0]), DOWN, buff=0)
                             for t, x in zip(names, xs)])
        rules = ["對偶圖", "小孩／兄弟", "輪廓走法", ("$U$", " 配 ", "$D$")]
        arrows, rule_mobs = VGroup(), VGroup()
        for k, text in enumerate(rules):
            left, right = items[k].get_right()[0], items[k + 1].get_left()[0]
            arr = Tex(r"\longleftrightarrow", font_size=40, fill_color=GREY_A)
            arr.move_to(np.array([(left + right) / 2, chain_y, 0.0]))
            assert arr.get_width() < right - left - 0.1
            lab = (mixed(*text, font_size=20, color=MUTED_COLOR, buff=0.06) if isinstance(text, tuple)
                   else zh(text, font_size=20, color=MUTED_COLOR)).next_to(arr, UP, buff=0.12)
            arrows.add(arr)
            rule_mobs.add(lab)
        chain = VGroup(*items, name_mobs, arrows, rule_mobs)
        assert_in_frame(chain)
        for k in range(len(items) - 1):
            assert_apart(rule_mobs[k], items[k])
            assert_apart(rule_mobs[k], items[k + 1])
        self.say("一條鏈：", "三角剖分", "$\\leftrightarrow$", "二元樹", "$\\leftrightarrow$", "平面樹",
                 "$\\leftrightarrow$", "Dyck 路徑", "$\\leftrightarrow$", "不交叉配對")
        self.play(FadeIn(items[0]), FadeIn(name_mobs[0]), run_time=0.5)
        for k in range(len(items) - 1):
            self.play(GrowFromCenter(arrows[k]), FadeIn(rule_mobs[k]), FadeIn(items[k + 1], shift=0.3 * RIGHT),
                      FadeIn(name_mobs[k + 1]), run_time=0.7)
        self.wait(0.8)
        self.say("同一個例子：根（橘）和左子樹（青）在每一種裡都對得上")
        self.wait(2.0)

        conclusion = mixed("每一步都是一一對應 ", "$\\Rightarrow$", " 每一種都有 ", "$C_n$", " 個（",
                           "$n=3$", f"：{catalan(3)} 個）", font_size=30)
        box = boxed(conclusion).move_to(np.array([0.0, -1.85, 0.0]))
        assert_in_frame(box)
        assert_apart(box, chain)
        self.say("所以這五種物件的個數全部相同")
        self.play(FadeIn(box, shift=0.2 * UP), run_time=0.8)
        self.wait(2.5)
