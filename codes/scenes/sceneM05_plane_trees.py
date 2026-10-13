"""
Scene M05 —— 平面樹（MIT 18.212 第 3 講）

    平面樹：有根，而且每個頂點的小孩由左到右排好順序
    同一棵「一般的樹」交換小孩的順序 -> 不同的平面樹（4 個頂點的例子）
    n+1 個頂點（n 條邊）的平面樹有 C_n 棵：1, 1, 2, 5
    n=3 的 5 棵依 binary_trees(3) 的順序（左小孩=第一個小孩、右小孩=下一個兄弟），和 00k 的欄位一致

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM05_plane_trees.py SceneM05PlaneTrees
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import tree_item
from utils.counting import (
    MIT_EXAMPLE_TREE,
    binary_to_plane,
    binary_trees,
    catalan,
    plane_to_binary,
    plane_tree_edges,
    plane_tree_preorder,
    plane_trees,
    plane_trees_bruteforce,
)
from utils.mit_draw import CATALAN_COLOR, ROOT_COLOR, PlaneTreeMob
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, YELLOW, boxed, mixed, zh

SWAP_A = (((),), ())        # 根的第一個小孩下面還有一個頂點
SWAP_B = ((), ((),))        # 交換根的兩個小孩
A_COLOR = YELLOW            # 有小孩的那一枝
B_COLOR = GREEN             # 單獨一片葉子的那一枝

ROW_TOP = {0: 2.75, 1: 2.2, 2: 1.1, 3: -0.45}     # 每一列的根的高度
TREE_X = [-2.7, -1.15, 0.4, 1.95, 3.5]
COUNT_X = 5.5
LABEL_X = -6.5


def canon(pt):
    """不管小孩順序的標準形（用來說明 SWAP_A、SWAP_B 是同一棵一般的樹）。"""
    return tuple(sorted(canon(c) for c in pt))


def swap_map(src, dst):
    """src -> dst 的頂點對應（保持父子關係），用前序編號。"""
    ps = [p for p, _ in plane_tree_preorder(src)]
    pd = [p for p, _ in plane_tree_preorder(dst)]
    m = {0: 0, 1: 2, 2: 3, 3: 1}
    assert len(ps) == len(pd) == 4
    for v in range(1, 4):
        assert pd[m[v]] == m[ps[v]]
    return m


def place_tree(mob, x, top_y):
    """把樹的根放在高度 top_y、整棵樹的水平中心放在 x。"""
    mob.shift((x - mob.get_center()[0]) * RIGHT + (top_y - mob.vertex(0)[1]) * UP)
    return mob


def row_tree(pt):
    return PlaneTreeMob(pt, leaf_gap=0.48, level_height=0.52, node_radius=0.07, root_color=ROOT_COLOR,
                        edge_width=3)


def root_label(mob):
    return zh("根", font_size=26, color=ROOT_COLOR).next_to(mob.nodes[0], UP, buff=0.1)


def color_branch(mob, verts, color):
    for v in verts:
        mob.nodes[v].set_fill(color)
        mob.edge_to(v).set_stroke(color)


class SceneM05PlaneTrees(ChuScene):
    def construct(self):
        self.show_header("平面樹")

        # ------------------------------------------------------------ 定義：小孩有順序
        all3 = plane_trees(3)
        assert SWAP_A in all3 and SWAP_B in all3 and SWAP_A != SWAP_B
        assert canon(SWAP_A) == canon(SWAP_B)
        assert plane_tree_edges(SWAP_A) == 3 and len(plane_tree_preorder(SWAP_A)) == 4
        vmap = swap_map(SWAP_A, SWAP_B)

        big = dict(leaf_gap=1.3, level_height=1.1, node_radius=0.11, root_color=ROOT_COLOR, edge_width=5)
        t1 = place_tree(PlaneTreeMob(SWAP_A, **big), -3.4, 2.2)
        color_branch(t1, (1, 2), A_COLOR)
        color_branch(t1, (3,), B_COLOR)
        t2 = place_tree(PlaneTreeMob(SWAP_B, **big), 3.4, 2.2)
        color_branch(t2, (vmap[1], vmap[2]), A_COLOR)
        color_branch(t2, (vmap[3],), B_COLOR)

        self.say("平面樹：有一個根，每個頂點的小孩由左到右排好順序")
        lab1 = root_label(t1)
        self.play(FadeIn(t1.nodes[0], scale=1.5), FadeIn(lab1), run_time=0.6)
        for v in range(1, 4):
            self.play(ShowCreation(t1.edge_to(v)), FadeIn(t1.nodes[v]), run_time=0.45)
        size_lab = zh("4 個頂點、3 條邊", font_size=24, color=MUTED_COLOR)
        size_lab.next_to(t1, DOWN, buff=0.35)
        self.play(FadeIn(size_lab), run_time=0.5)
        self.wait(0.8)

        # 交換根的兩個小孩
        self.say("把根的兩個小孩（連同它們下面的部分）左右交換")
        moving = t1.copy()
        self.play(moving.animate.shift((t2.vertex(0) - t1.vertex(0))), run_time=0.9)
        anims = []
        for v in range(1, 4):
            anims.append(Transform(moving.nodes[v], t2.nodes[vmap[v]], path_arc=-PI / 3))
            anims.append(Transform(moving.edge_to(v), t2.edge_to(vmap[v]), path_arc=-PI / 3))
        anims.append(FadeIn(root_label(t2)))
        self.play(*anims, run_time=1.4)
        self.remove(moving)
        self.add(t2)
        size_lab2 = size_lab.copy().next_to(t2, DOWN, buff=0.3)
        size_lab2.align_to(size_lab, UP)
        self.play(FadeIn(size_lab2), run_time=0.4)

        mid = np.array([0.0, 1.25, 0.0])
        eq = Tex("=", font_size=96).move_to(mid)
        eq_lab = zh("不管順序：同一棵樹", font_size=24, color=MUTED_COLOR).next_to(eq, DOWN, buff=0.3)
        self.say("如果不管小孩的順序，兩棵是同一棵樹")
        self.play(FadeIn(eq), FadeIn(eq_lab), run_time=0.6)
        self.wait(0.8)
        neq = Tex(r"\neq", font_size=96, fill_color=CROSSING_COLOR).move_to(mid)
        neq_lab = zh("平面樹：不同的兩棵", font_size=24, color=CROSSING_COLOR).next_to(neq, DOWN, buff=0.3)
        self.say("但平面樹要看順序：它們是不同的兩棵平面樹")
        self.play(Transform(eq, neq), FadeOut(eq_lab), FadeIn(neq_lab), run_time=0.8)
        defn = boxed(mixed("平面樹 ＝ 有根、而且小孩有左右順序的樹", font_size=30), buff=0.22)
        defn.move_to(1.85 * DOWN)
        self.play(FadeIn(defn[1]), ShowCreation(defn[0]), run_time=0.8)
        self.wait(2.2)

        # ------------------------------------------------------------ 計數：1, 1, 2, 5
        self.clear_stage()
        rows = {}
        self.say("$n+1$", " 個頂點（", "$n$", " 條邊）的平面樹有幾棵？")
        for n in range(4):
            trees = plane_trees(n)
            assert len(trees) == len(plane_trees_bruteforce(n)) == catalan(n)
            assert set(trees) == set(plane_trees_bruteforce(n))
            assert all(plane_tree_edges(pt) == n for pt in trees)
            label = mixed(f"$n={n}$", f"：{n + 1} 個頂點", font_size=26)
            label.move_to(np.array([0.0, ROW_TOP[n], 0.0]), aligned_edge=UP)
            label.shift((LABEL_X - label.get_left()[0]) * RIGHT + 0.06 * DOWN)
            mobs = VGroup(*[place_tree(row_tree(pt), x, ROW_TOP[n]) for pt, x in zip(trees, TREE_X)])
            count = Tex(f"C_{n}={catalan(n)}", font_size=40, t2c={f"C_{n}": CATALAN_COLOR})
            count.move_to(np.array([COUNT_X, label.get_center()[1], 0.0]))
            rows[n] = (label, mobs, count)
            rt = 1.6 if n == 3 else 0.9
            self.play(FadeIn(label, shift=0.2 * RIGHT), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(m, shift=0.15 * DOWN) for m in mobs], lag_ratio=0.3), run_time=rt)
            self.play(FadeIn(count, scale=1.3), run_time=0.4)
        # 剛才交換小孩的兩棵 = 這一列的第 2、3 棵
        assert plane_trees(3).index(SWAP_B) == 1 and plane_trees(3).index(SWAP_A) == 2
        pair_box = SurroundingRectangle(VGroup(rows[3][1][1], rows[3][1][2]), buff=0.15, color=YELLOW,
                                        stroke_width=3)
        self.say("剛才交換小孩的那兩棵，在這裡算成不同的兩棵（第 2、3 棵）")
        self.play(ShowCreation(pair_box), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(pair_box), run_time=0.4)
        assert [catalan(n) for n in range(4)] == [1, 1, 2, 5] and len(plane_trees(4)) == catalan(4) == 14
        self.say("$n+1$", " 個頂點的平面樹有 ", "$C_n$", " 棵：1, 1, 2, 5，下一個是 14", t2c={"C_n": CATALAN_COLOR})
        self.wait(1.6)

        # ------------------------------------------------------------ n=3 的 5 棵 <-> 00k 的 5 棵二元樹
        bts = binary_trees(3)
        assert MIT_EXAMPLE_TREE == bts[3]
        assert tuple(binary_to_plane(t) for t in bts) == plane_trees(3)
        assert all(plane_to_binary(binary_to_plane(t)) == t for t in bts)
        old = VGroup(*[m for n in range(3) for m in rows[n]], rows[3][0], rows[3][2])
        row3 = rows[3][1]
        xs = np.linspace(-5.0, 5.0, 5)
        top = 2.55
        self.play(FadeOut(old), run_time=0.6)
        for m, x in zip(row3, xs):
            m.generate_target()
            m.target.scale(1.25)
            place_tree(m.target, x, top)
        self.play(*[MoveToTarget(m) for m in row3], run_time=0.9)
        bins = VGroup()
        arrows = VGroup()
        for t, x in zip(bts, xs):
            b = tree_item(t, scale=1.8)
            b.move_to(np.array([x, 0.0, 0.0]))
            b.shift((-0.3 - b.get_top()[1]) * UP)
            assert b.get_bottom()[1] > -1.9
            bins.add(b)
            arrows.add(Tex(r"\updownarrow", font_size=40, fill_color=MUTED_COLOR).move_to(np.array([x, 0.12, 0.0])))
        # 二元樹的 3 個圓點（內部節點）變成平面樹的 3 個非根頂點，最上面再加一個根：3 個點 -> 4 個頂點
        assert all(len(plane_tree_preorder(binary_to_plane(t))) == 3 + 1 for t in bts)
        rule = boxed(mixed("只看圓點：左小孩 ＝ 第一個小孩，右小孩 ＝ 下一個兄弟，最上面再加一個根",
                           font_size=26), buff=0.18)
        rule.move_to(2.45 * DOWN)
        assert rule.get_width() < 13.4 and rule.get_top()[1] < min(b.get_bottom()[1] for b in bins) - 0.25
        # M05 的下一幕是 M06（弧圖），二元樹 -> 平面樹的細節在 M07
        self.say("排列順序和「同一個 5」那一幕的二元樹一樣（後面會再細講這個對應）")
        self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(b, shift=0.15 * UP) for b in bins], lag_ratio=0.15), run_time=1.4)
        self.play(FadeIn(rule[1]), ShowCreation(rule[0]), run_time=0.8)
        self.wait(2.0)

        # 貫穿的例子
        ex = VGroup(row3[3], arrows[3], bins[3])
        frame_box = SurroundingRectangle(ex, buff=0.14, color=YELLOW, stroke_width=3)
        assert frame_box.get_bottom()[1] > rule.get_top()[1] + 0.15 and frame_box.get_top()[1] < 3.2
        assert binary_to_plane(MIT_EXAMPLE_TREE) == (((), ()),) == plane_trees(3)[3]
        self.say("第 4 棵是後面幾幕一直用的例子：根下面一個頂點，它有兩片葉子")
        self.play(ShowCreation(frame_box), *[m.animate.set_opacity(0.35) for i in (0, 1, 2, 4)
                                             for m in (row3[i], bins[i], arrows[i])], run_time=0.9)
        self.wait(2.6)
