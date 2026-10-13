"""
Scene M07 —— 三角剖分 ↔ 二元樹（對偶圖）↔ 平面樹（MIT 18.212 第 3 講）

    每個三角形          -> 一個節點；含底邊的三角形 -> 根
    共用一條對角線      -> 兩個節點連一條邊
    其他（非底邊）的邊  -> 一片葉子
    二元樹 -> 平面樹：左小孩 = 第一個小孩、右小孩 = 下一個兄弟，再加一個新的根

例子是 mit_plan.md 第 3 節的 EX = binary_trees(3)[3]（00k 第 4 欄）：
五邊形對角線 {1,4}、{2,4}；對偶樹 = EX；平面樹 = 根 -> A -> 兩片葉子。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM07_triangulation_dual_tree.py SceneM07TriangulationDualTree
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    EDGE_COLOR,
    LEFT_COLOR,
    RIGHT_COLOR,
    BinaryTreeMob,
    TriangulationMob,
    catalan_item,
    triangulation_item,
)
from utils.counting import (
    MIT_EXAMPLE_TREE,
    binary_to_plane,
    binary_trees,
    catalan,
    plane_to_binary,
    plane_tree_dfs,
    plane_tree_preorder,
    plane_trees,
    plane_trees_bruteforce,
    tree_size,
    tree_to_dyck,
    tree_to_triangulation,
    triangulation_dual,
    triangulation_to_tree,
)
from utils.mit_draw import PlaneTreeMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, ROOT_COLOR, YELLOW, mixed, zh

EX = MIT_EXAMPLE_TREE
POLY_CENTER = np.array([-3.0, 0.15, 0.0])
POLY_R = 1.75
LEAF_OUT = 0.6                               # 葉子放在多邊形邊外面多遠
TREE_ROOT = np.array([2.6, 1.45, 0.0])       # 標準畫法的二元樹（根的位置）
GAP, LEVEL = 1.0, 0.95
LETTERS = "ABCDEFG"
LABEL_SIDE = {"A": RIGHT, "B": LEFT, "C": RIGHT}


# =============================================================================
# 模組層級的小工具（連續播放時場景物件不同，不能寫成方法）
# =============================================================================
def poly_center(tm: TriangulationMob) -> np.ndarray:
    """正多邊形的外心 = 頂點的平均（外框的 bounding box 中心不是外心）。"""
    return np.mean([tm.vertex(k) for k in range(tm.m)], axis=0)


def centroid(tm: TriangulationMob, tri) -> np.ndarray:
    return np.mean([tm.vertex(k) for k in tri], axis=0)


def leaf_point(tm: TriangulationMob, e: int, out: float = LEAF_OUT) -> np.ndarray:
    """多邊形邊 (e, e+1) 外面的一點。"""
    mid = (tm.vertex(e) + tm.vertex(e + 1)) / 2
    return mid + out * normalize(mid - poly_center(tm))


def child_point(ref, node_pts, leaf_pts) -> np.ndarray:
    kind, i = ref
    return node_pts[i] if kind == "tri" else leaf_pts[i]


def check_tree_matches_dual(tree_mob: BinaryTreeMob, dual) -> None:
    """BinaryTreeMob 的 edges[2i]、edges[2i+1] 是第 i 個節點（中序）的左、右邊，和 triangulation_dual 一致。"""
    assert len(tree_mob.nodes) == len(dual)
    for i, d in enumerate(dual):
        for s, side in enumerate(("left", "right")):
            kind, j = d[side]
            k = 2 * i + s
            assert tree_mob.edge_kinds[k] == ("node" if kind == "tri" else "leaf")
            end = tree_mob.node_pos[j] if kind == "tri" else tree_mob.leaf_pos[j]
            assert np.allclose(tree_mob.edges[k].get_start(), tree_mob.node_pos[i])
            assert np.allclose(tree_mob.edges[k].get_end(), end)


def embedded_tree(target: BinaryTreeMob, dual, node_pts, leaf_pts, root: int) -> BinaryTreeMob:
    """把標準畫法的樹複製一份，節點搬到三角形中心、葉子搬到多邊形邊外（結構相同，可直接 Transform）。"""
    emb = target.copy()
    for i, d in enumerate(dual):
        emb.nodes[i].move_to(node_pts[i])
        for s, side in enumerate(("left", "right")):
            emb.edges[2 * i + s].put_start_and_end_on(node_pts[i], child_point(d[side], node_pts, leaf_pts))
    for e, lf in enumerate(emb.leaves):
        lf.move_to(leaf_pts[e])
    emb.nodes.set_fill(CATALAN_COLOR)
    emb.nodes[root].set_fill(ROOT_COLOR)
    emb.edges.set_stroke(GREY_A)
    emb.leaves.set_fill(GREY_B)
    return emb


def binary_preorder(t, offset: int = 0) -> list:
    """二元樹內部節點的前序，以中序編號表示（中序編號 = BinaryTreeMob.nodes 的位置）。"""
    if t is None:
        return []
    me = offset + tree_size(t[0])
    return [me] + binary_preorder(t[0], offset) + binary_preorder(t[1], me + 1)


def plane_parents_by_rule(t, dual) -> list:
    """
    依「左小孩 = 第一個小孩、右小孩 = 下一個兄弟、加一個新的根」算平面樹每個頂點的父親。
    二元樹的節點依前序變成平面樹的頂點 1, 2, ...（0 是新的根）。
    """
    pre = binary_preorder(t)
    plane_id = {b: v + 1 for v, b in enumerate(pre)}
    parent = [None] * (len(pre) + 1)
    for b in pre:                                   # 前序：父親一定先處理
        p = dual[b]["parent"]
        if p is None:
            parent[plane_id[b]] = 0                 # 二元樹的根 -> 新根的第一個小孩
        elif dual[p]["left"] == ("tri", b):
            parent[plane_id[b]] = plane_id[p]       # 左小孩 -> 第一個小孩
        else:
            parent[plane_id[b]] = parent[plane_id[p]]   # 右小孩 -> 下一個兄弟（同一個父親）
    return parent


def incoming_edge_index(dual, b: int):
    """二元樹節點 b（中序）從父親連進來的邊在 BinaryTreeMob.edges 的位置；根回傳 None。"""
    p = dual[b]["parent"]
    if p is None:
        return None
    return 2 * p + (0 if dual[p]["left"] == ("tri", b) else 1)


def arrow_line(left, right, font_size: float = 28, left_color=WHITE, right_color=WHITE) -> VGroup:
    return mixed(zh(left, font_size=font_size, color=left_color), "$\\longrightarrow$",
                 zh(right, font_size=font_size, color=right_color), font_size=font_size, buff=0.18)


def small_plane_tree(pt) -> PlaneTreeMob:
    return PlaneTreeMob(pt, leaf_gap=0.4, level_height=0.33, node_radius=0.055, edge_width=2.5,
                        root_color=WHITE)


def row_label(title: str, sub: str) -> VGroup:
    return VGroup(zh(title, font_size=26), zh(sub, font_size=21, color=MUTED_COLOR)).arrange(DOWN, buff=0.1)


def in_frame(mob: Mobject, x_max: float = 6.8, y_min: float = -3.0, y_max: float = 3.2) -> bool:
    return (mob.get_left()[0] >= -x_max and mob.get_right()[0] <= x_max
            and mob.get_bottom()[1] >= y_min and mob.get_top()[1] <= y_max)


# =============================================================================
class SceneM07TriangulationDualTree(ChuScene):
    def construct(self):
        self.show_header("三角剖分 ↔ 二元樹 ↔ 平面樹")

        # ------------------------------------------------------------ 資料（全部由 counting 算出）
        t = EX
        n = tree_size(t)
        m = n + 2
        diags = sorted(tree_to_triangulation(t, 0, m - 1))
        dual = triangulation_dual(t)
        root = tree_size(t[0])                       # 根在中序的位置
        apex = root + 1
        pt = binary_to_plane(t)
        pre = binary_preorder(t)
        assert t == binary_trees(3)[3] and n == 3 and m == 5
        assert [tuple(x + 1 for x in d) for d in diags] == [(1, 4), (2, 4)]          # 畫面：{1,4}、{2,4}
        assert [d["tri"] for d in dual] == [(0, 1, 3), (1, 2, 3), (0, 3, 4)]
        assert dual[root]["parent"] is None and dual[root]["base"] == (0, m - 1)
        assert dual[root]["tri"] == (0, apex, m - 1)
        leaf_refs = sorted(d[s][1] for d in dual for s in ("left", "right") if d[s][0] == "leaf")
        assert leaf_refs == list(range(m - 1)) and len(leaf_refs) == 4                # 4 片葉子 = 4 條非底邊
        assert triangulation_to_tree(m, diags) == t                                   # 反方向也對
        assert pt == (((), ()),) and plane_to_binary(pt) == t
        assert pre == [2, 0, 1]                                                       # A, B, C
        assert plane_parents_by_rule(t, dual) == [p for p, _ in plane_tree_preorder(pt)]
        assert len(plane_tree_preorder(pt)) == n + 1 == 4                            # 4 個頂點、3 條邊
        assert plane_tree_dfs(pt) == tree_to_dyck(t) == "UUDUDD"
        # 一般的 n：對偶樹的反方向、平面樹轉換都是一一對應
        for k in range(0, 6):
            for s in binary_trees(k):
                mm = k + 2
                assert triangulation_to_tree(mm, tree_to_triangulation(s, 0, mm - 1)) == s
                assert plane_to_binary(binary_to_plane(s)) == s
                if k >= 1:
                    assert plane_parents_by_rule(s, triangulation_dual(s)) == \
                        [p for p, _ in plane_tree_preorder(binary_to_plane(s))]
            assert set(plane_trees(k)) == plane_trees_bruteforce(k) and len(plane_trees(k)) == catalan(k)

        # ------------------------------------------------------------ 1. 五邊形
        tm = TriangulationMob(m, diags, radius=POLY_R, center=POLY_CENTER, edge_width=4, diag_width=5,
                              dot_radius=0.07)
        vlabels = VGroup(*[
            Tex(str(k + 1), font_size=30, fill_color=GREY_A).move_to(
                POLY_CENTER + (POLY_R + 0.32) * normalize(tm.vertex(k) - POLY_CENTER))
            for k in range(m)
        ])
        self.say("貫穿各幕的例子：五邊形，對角線 ", "$\\{1,4\\},\\ \\{2,4\\}$", "，底邊是 1–5")
        self.play(ShowCreation(tm.outline), FadeIn(tm.dots), FadeIn(vlabels), run_time=1.2)
        self.play(ShowCreation(tm.diagonals), run_time=0.8)
        self.wait(0.8)

        # 右邊的規則表
        rules = VGroup(
            arrow_line("三角形", "節點（含底邊的是根）"),
            arrow_line("共用的對角線", "連一條邊"),
            arrow_line("其他的多邊形邊", "葉子"),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        rules.move_to(np.array([0.9, 0.3, 0.0]), aligned_edge=LEFT)
        assert in_frame(rules)

        # ------------------------------------------------------------ 2. 三角形 -> 節點
        node_pts = [centroid(tm, d["tri"]) for d in dual]
        leaf_pts = [leaf_point(tm, e) for e in range(m - 1)]
        target = BinaryTreeMob(t, root_pos=TREE_ROOT, leaf_gap=GAP, level_height=LEVEL, node_radius=0.11,
                               leaf_size=0.11, edge_width=4, colored=True)
        check_tree_matches_dual(target, dual)
        emb = embedded_tree(target, dual, node_pts, leaf_pts, root)

        tri_fills = VGroup(*[
            tm.region(d["tri"], ROOT_COLOR if i == root else CATALAN_COLOR, 0.35 if i == root else 0.14)
            for i, d in enumerate(dual)
        ]).set_z_index(-1)
        base = tm.edge(0, m - 1, ROOT_COLOR, 7)
        base_lab = zh("底邊", font_size=24, color=ROOT_COLOR).next_to(base, DOWN, buff=0.15)
        self.say("每個三角形中間放一個節點；含底邊的三角形就是根（橘）")
        self.play(FadeIn(tri_fills), ShowCreation(base), FadeIn(base_lab), FadeIn(rules[0], shift=0.2 * UP),
                  run_time=0.9)
        self.play(LaggedStart(*[GrowFromCenter(emb.nodes[i]) for i in range(n)], lag_ratio=0.3), run_time=1.0)
        self.wait(1.0)

        # ------------------------------------------------------------ 3. 共用的對角線 -> 邊
        self.say("兩個三角形共用一條對角線 → 兩個節點連一條邊")
        self.play(FadeIn(rules[1], shift=0.2 * UP), run_time=0.5)
        diag_of = {tuple(sorted(d.pair)): d for d in tm.diagonals}
        for i, d in enumerate(dual):
            for s, side in enumerate(("left", "right")):
                kind, j = d[side]
                if kind != "tri":
                    continue
                shared = tuple(sorted(dual[j]["base"]))
                assert shared in diag_of and shared in {tuple(sorted(x)) for x in (d["tri"][:2], d["tri"][1:],
                                                                                   (d["tri"][0], d["tri"][2]))}
                self.play(Indicate(diag_of[shared], color=YELLOW, scale_factor=1.0),
                          ShowCreation(emb.edges[2 * i + s]), run_time=0.9)
        self.wait(0.6)

        # ------------------------------------------------------------ 4. 其他的多邊形邊 -> 葉子
        self.say("其他每條多邊形邊（不含底邊），外面放一片葉子：共 4 片")
        self.play(FadeIn(rules[2], shift=0.2 * UP), run_time=0.5)
        leaf_anims = []
        for i, d in enumerate(dual):
            for s, side in enumerate(("left", "right")):
                kind, e = d[side]
                if kind == "leaf":
                    leaf_anims.append(AnimationGroup(ShowCreation(emb.edges[2 * i + s]),
                                                     FadeIn(emb.leaves[e], scale=0.5)))
        self.play(LaggedStart(*leaf_anims, lag_ratio=0.3), run_time=1.6)
        self.add(emb)                                # 收成一棵樹（同時把上面零散加入的子物件換掉）
        self.wait(1.0)

        # ------------------------------------------------------------ 5. 拿掉多邊形
        self.say("拿掉多邊形：剩下一棵滿二元樹（3 個節點、4 片葉子）")
        self.play(FadeOut(tm), FadeOut(vlabels), FadeOut(tri_fills), FadeOut(base), FadeOut(base_lab),
                  FadeOut(rules), run_time=1.0)
        self.wait(0.8)
        self.say("整理成標準畫法：根（橘）、左子樹（青）、右子樹（粉紅）")
        self.play(Transform(emb, target), run_time=1.6)
        self.wait(0.6)

        # 對照：上色的三角剖分（與 00c 相同）
        right_part = list(range(apex, m))
        assert right_part == [3, 4]                  # 右邊只剩一條邊 = 一片葉子
        assert len(range(0, apex + 1)) == 4          # 左邊：頂點 1..4 圍成四邊形
        ct = triangulation_item(t, radius=1.5, center=POLY_CENTER + 0.1 * DOWN, colored=True, edge_width=4,
                                diag_width=5, dot_radius=0.06)
        ct_right = ct.edge(right_part[0], right_part[1], RIGHT_COLOR, 7)
        ct_labels = VGroup(*[
            Tex(str(k + 1), font_size=26, fill_color=GREY_A).move_to(
                ct.vertex(k) + 0.3 * normalize(ct.vertex(k) - poly_center(ct)))
            for k in range(m)
        ])
        self.say("對照多邊形：根三角形（橘）、左邊的四邊形（青）、右邊只剩一條邊（粉紅）")
        self.play(FadeIn(ct), FadeIn(ct_labels), ShowCreation(ct_right), run_time=1.0)
        self.wait(1.4)
        self.say("反過來，從根往下一塊一塊切，就切回原來的三角剖分：一一對應")
        self.wait(1.8)

        # ------------------------------------------------------------ 6. 二元樹 -> 平面樹
        self.play(FadeOut(ct), FadeOut(ct_labels), FadeOut(ct_right), run_time=0.6)
        tree = emb                                   # 現在的位置、樣子 = target
        leaf_edges = [tree.edges[k] for k, kind in enumerate(tree.edge_kinds) if kind == "leaf"]
        self.say("接著：二元樹 → 平面樹。葉子只是空位，先拿掉")
        title = zh("二元樹 → 平面樹", font_size=30, color=YELLOW)
        panel = VGroup(
            title,
            arrow_line("左小孩", "第一個小孩", left_color=LEFT_COLOR),
            arrow_line("右小孩", "下一個兄弟", left_color=RIGHT_COLOR),
            zh("再加一個新的根（白）", font_size=28),
        ).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        panel.move_to(np.array([-6.3, 0.6, 0.0]), aligned_edge=LEFT)
        assert in_frame(panel) and panel.get_right()[0] < tree.get_left()[0] - 0.5
        self.play(FadeOut(tree.leaves), *[FadeOut(e) for e in leaf_edges], FadeIn(title), run_time=0.9)

        # 節點依前序叫 A、B、C；邊改成「左小孩（青）／右小孩（粉紅）」
        names = {b: LETTERS[v] for v, b in enumerate(pre)}
        assert [names[b] for b in range(n)] == ["B", "C", "A"]
        node_mobs = {b: tree.nodes[b] for b in range(n)}
        labels = {}
        for b in range(n):
            lab = zh(names[b], font_size=28)
            lab.next_to(node_mobs[b], LABEL_SIDE.get(names[b], RIGHT), buff=0.15)
            labels[b] = lab
        side_edges = {}                              # 二元樹的內部邊：(父, 子) -> (邊, 'left'/'right')
        for i, d in enumerate(dual):
            for s, side in enumerate(("left", "right")):
                if d[side][0] == "tri":
                    side_edges[d[side][1]] = (tree.edges[2 * i + s], side)
        self.say("節點依前序叫 A、B、C；邊的顏色改成：左小孩（青）、右小孩（粉紅）")
        self.play(*[mob.animate.set_fill(CATALAN_COLOR) for mob in node_mobs.values()],
                  *[e.animate.set_stroke(LEFT_COLOR if side == "left" else RIGHT_COLOR)
                    for e, side in side_edges.values()],
                  *[FadeIn(lab) for lab in labels.values()],
                  FadeIn(panel[1]), FadeIn(panel[2]), run_time=1.0)
        self.wait(1.4)

        # 加一個新的根
        pt_target = PlaneTreeMob(pt, root_pos=tree.node_pos[root] + LEVEL * UP, leaf_gap=GAP, level_height=LEVEL,
                                 node_radius=0.11, edge_width=4, root_color=WHITE)
        assert np.allclose(pt_target.vertex(1), node_mobs[root].get_center())
        assert in_frame(pt_target)
        new_root = pt_target.nodes[0].copy()
        root_edge = Line(new_root.get_center(), node_mobs[root].get_center(), stroke_color=EDGE_COLOR,
                         stroke_width=4)
        self.say("加一個新的根：A 是它的第一個小孩（A 沒有右小孩，所以根只有這一個小孩）")
        self.play(FadeIn(panel[3]), GrowFromCenter(new_root), ShowCreation(root_edge), run_time=1.0)
        self.wait(1.2)

        # 右小孩 -> 下一個兄弟：重新掛到父親底下
        moves = []
        for b in pre:
            v = pre.index(b) + 1
            p = dual[b]["parent"]
            if p is not None and dual[p]["right"] == ("tri", b):
                parent_v = plane_parents_by_rule(t, dual)[v]
                parent_pos = pt_target.vertex(parent_v)
                child_pos = pt_target.vertex(v)
                edge, _ = side_edges[b]
                new_edge = Line(parent_pos, child_pos, stroke_color=RIGHT_COLOR, stroke_width=4)
                moves += [Transform(edge, new_edge), node_mobs[b].animate.move_to(child_pos),
                          labels[b].animate.next_to(child_pos, LABEL_SIDE.get(names[b], RIGHT), buff=0.15)]
        assert len(moves) == 3                       # 只有 C 是右小孩
        self.say("C 是 B 的右小孩 → 變成 B 的下一個兄弟：改掛到 A 底下、排在 B 右邊")
        self.play(*moves, run_time=1.6)
        self.wait(0.8)
        for v in range(1, n + 1):                     # 每個頂點都到了標準平面樹的位置
            assert np.allclose(node_mobs[pre[v - 1]].get_center(), pt_target.vertex(v))
        self.say("得到平面樹：根 → A → B、C（4 個頂點、3 條邊）；反過來讀就回到二元樹")
        self.wait(2.2)

        # ------------------------------------------------------------ 7. n = 3 的五種，同一欄對應
        trees = binary_trees(3)
        hl = trees.index(t)
        assert hl == 3 and plane_trees(3)[hl] == pt
        assert len(trees) == len(plane_trees(3)) == catalan(3) == 5     # 畫面：5 種、5 棵、5 棵
        xs = np.linspace(-3.2, 5.4, 5)
        ys = [2.25, 0.75, -0.72]
        tri_row = VGroup(*[catalan_item("triangulation", s, scale=1.5).move_to(np.array([x, ys[0], 0.0]))
                           for x, s in zip(xs, trees)])
        bin_row = VGroup(*[catalan_item("tree", s, scale=1.5).move_to(np.array([x, ys[1], 0.0]))
                           for x, s in zip(xs, trees)])
        pl_row = VGroup(*[small_plane_tree(p).move_to(np.array([x, ys[2], 0.0]))
                          for x, p in zip(xs, plane_trees(3))])
        for s, item in zip(trees, tri_row):          # 每一欄：三角剖分 -> 對偶樹 -> 平面樹 是同一個
            assert triangulation_to_tree(m, [d.pair for d in item.diagonals]) == s
        heads = VGroup(row_label("三角剖分", "五邊形"), row_label("二元樹", f"{n} 個節點"),
                       row_label("平面樹", f"{n + 1} 個頂點"))
        for h, y in zip(heads, ys):
            h.move_to(np.array([-5.6, y, 0.0]))
        rows = [tri_row, bin_row, pl_row]
        for row in rows:
            for a, b in zip(row[:-1], row[1:]):
                assert a.get_right()[0] < b.get_left()[0] - 0.3
        for r1, r2 in zip(rows[:-1], rows[1:]):
            assert r1.get_bottom()[1] > r2.get_top()[1] + 0.15
        assert heads.get_right()[0] < xs[0] - 0.9
        col = VGroup(tri_row[hl], bin_row[hl], pl_row[hl])
        col_box = SurroundingRectangle(col, buff=0.15, color=YELLOW, stroke_width=3)
        for mob in (tri_row, bin_row, pl_row, heads, col_box):
            assert in_frame(mob), mob

        # 現在畫面上的平面樹拆成零件，一一飛到第 3 列第 4 欄
        target_small = pl_row[hl]
        piece_anims = [ReplacementTransform(new_root, target_small.nodes[0]),
                       ReplacementTransform(root_edge, target_small.edge_to(1))]
        for v in range(1, n + 1):
            b = pre[v - 1]
            piece_anims.append(ReplacementTransform(node_mobs[b], target_small.nodes[v]))
            if v >= 2:
                piece_anims.append(ReplacementTransform(side_edges[b][0], target_small.edge_to(v)))
        self.play(FadeOut(panel), *[FadeOut(lab) for lab in labels.values()], run_time=0.5)
        self.say("$n=3$", "：5 種三角剖分、5 棵二元樹、5 棵平面樹，同一欄一一對應")
        self.play(*piece_anims, run_time=1.2)
        self.play(FadeIn(heads), LaggedStart(*[FadeIn(i, scale=0.8) for i in tri_row], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(i, scale=0.8) for i in bin_row], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(pl_row[j], scale=0.8) for j in range(5) if j != hl], lag_ratio=0.1),
                  run_time=1.6)
        self.play(ShowCreation(col_box), run_time=0.7)
        self.wait(1.0)

        statement = mixed("三角剖分", "$\\longleftrightarrow$", "滿二元樹", "$\\longleftrightarrow$", "平面樹",
                          "：數目都是 ", "$C_n$", font_size=28, buff=0.15)
        box = SurroundingRectangle(statement, buff=0.2, color=YELLOW, stroke_width=3)
        VGroup(statement, box).move_to(np.array([0.9, -2.3, 0.0]))
        assert in_frame(box) and box.get_top()[1] < pl_row.get_bottom()[1] - 0.1
        self.play(FadeIn(statement), ShowCreation(box), run_time=0.8)
        self.say("下一幕：沿平面樹的輪廓走一圈，就讀出 Dyck 路徑 UUDUDD")
        self.wait(2.0)
