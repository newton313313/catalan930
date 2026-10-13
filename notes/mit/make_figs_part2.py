r"""
make_figs_part2.py —— 講義附錄 A 第 2 段（A.5–A.8，動畫 M05–M08）的 TikZ 圖

執行（任何資料夾皆可）：
    python C:\mypython\manim\projects\catalan930\notes\mit\make_figs_part2.py
會先檢查 mit/part2.tex 寫到的每一個數字，再寫出 mit/figs_part2.tex（part2.tex 開頭 \input 它）。

數學資料一律由 codes/utils/counting.py 算出；TikZ 的基本圖元（emit、place、tri_prims、tree_prims、
dyck_prims、matching_prims …）從 notes/make_catalan_figs.py 匯入，配色與第 1 節相同：
    根 = cTop（橘）、左 = cLeft（青）、右 = cRight（紫紅）、一般物件 = cA（藍）、交叉 = cBad（紅）。
例子與排列順序和場景 M05–M08 相同（貫穿的例子 = binary_trees(3)[3]，00k 第 4 欄）。
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # notes/mit
NOTES = HERE.parent
sys.path.insert(0, str(NOTES.parent / "codes"))
sys.path.insert(0, str(NOTES))

from make_catalan_figs import (  # noqa: E402
    COLOR,
    dyck_prims,
    emit,
    f,
    matching_prims,
    node,
    picture,
    place,
    polygon_vertices,
    pt,
    tree_prims,
    tri_prims,
)
from utils.counting import (  # noqa: E402
    MIT_EXAMPLE_TREE,
    arcs_cross,
    arcs_nest,
    binary_to_plane,
    binary_trees,
    catalan,
    dyck_parts,
    dyck_to_matching,
    dyck_to_nonnesting,
    is_dyck,
    matching_crossings,
    matching_is_noncrossing,
    matching_is_nonnesting,
    matching_nestings,
    matching_parts,
    matching_to_dyck,
    perfect_matchings,
    plane_to_binary,
    plane_tree_dfs,
    plane_tree_edges,
    plane_tree_preorder,
    plane_tree_walk,
    plane_trees,
    plane_trees_bruteforce,
    tree_size,
    tree_to_dyck,
    tree_to_triangulation,
    triangulation_dual,
    triangulation_to_tree,
)

OUT = HERE / "figs_part2.tex"
EX = MIT_EXAMPLE_TREE                      # ((None, (None, None)), None)
PT = binary_to_plane(EX)                   # 根 -> A -> 兩片葉子
SWAP_A = (((),), ())                       # M05：根的第一個小孩下面還有一個頂點
SWAP_B = ((), ((),))                       # 交換根的兩個小孩
SHARED = ((0, 1), (2, 3), (4, 5))          # (1,2),(3,4),(5,6)：不交叉也不巢狀
NEST = "violet!75!black"                   # 巢狀（場景 M06 的紫色）
NN_FRAME = "green!50!black"                # 「不巢狀」的框
BRANCH = {"kid": "cA", "leaf": "green!50!black"}   # M05 交換小孩的兩枝


# =============================================================================
# 小工具（只看 counting 的資料）
# =============================================================================
def norm(pairs):
    return tuple(sorted(tuple(sorted(p)) for p in pairs))


def one_based(pairs) -> list:
    return [(a + 1, b + 1) for a, b in pairs]


def canon(pt_):
    """不管小孩順序的標準形。"""
    return tuple(sorted(canon(c) for c in pt_))


def heights(word: str) -> list:
    h = [0]
    for c in word:
        h.append(h[-1] + (1 if c == "U" else -1))
    return h


def binary_preorder(t, offset: int = 0) -> list:
    """二元樹內部節點的前序，以中序編號表示（= triangulation_dual 的位置）。"""
    if t is None:
        return []
    me = offset + tree_size(t[0])
    return [me] + binary_preorder(t[0], offset) + binary_preorder(t[1], me + 1)


def plane_parents_by_rule(t) -> list:
    """「左小孩 = 第一個小孩、右小孩 = 下一個兄弟、加一個新的根」：平面樹每個頂點（前序）的父親。"""
    dual = triangulation_dual(t)
    pre = binary_preorder(t)
    pid = {b: v + 1 for v, b in enumerate(pre)}
    parent = [None] * (len(pre) + 1)
    for b in pre:
        p = dual[b]["parent"]
        if p is None:
            parent[pid[b]] = 0
        elif dual[p]["left"] == ("tri", b):
            parent[pid[b]] = pid[p]
        else:
            parent[pid[b]] = parent[pid[p]]
    return parent


def walk_steps(pt_) -> list:
    """[(u, v, 'U'/'D', 邊的下端頂點)]：第 k 步從 walk[k] 走到 walk[k+1]（與場景 M08 相同）。"""
    walk = plane_tree_walk(pt_)
    parents = [p for p, _ in plane_tree_preorder(pt_)]
    out = []
    for u, v in zip(walk, walk[1:]):
        if parents[v] == u:
            out.append((u, v, "U", v))
        else:
            assert parents[u] == v
            out.append((u, v, "D", u))
    return out


def edge_step_pairs(steps) -> dict:
    """邊（以下端頂點表示）-> (往下那一步, 往上那一步)，0 起算。"""
    down, up = {}, {}
    for k, (_, _, c, low) in enumerate(steps):
        (down if c == "U" else up)[low] = k
    return {v: (down[v], up[v]) for v in sorted(down)}


def plane_parts(pt_) -> dict:
    """平面樹頂點 v >= 1 在二元樹裡屬於 root／left／right（與場景 M08 相同）。"""
    pre = plane_tree_preorder(pt_)
    parts = {}
    for v in range(1, len(pre)):
        top = v
        while pre[top][0] != 0:
            top = pre[top][0]
        parts[v] = "root" if v == 1 else ("left" if top == 1 else "right")
    return parts


def lifo_ok(pairs) -> bool:
    """每個右端都配給「最近的、還沒配的」左端。"""
    return norm(pairs) == norm(dyck_to_matching(matching_to_dyck(pairs)))


def fifo_ok(pairs) -> bool:
    """每個右端都配給「最早的、還沒配的」左端。"""
    return norm(pairs) == norm(dyck_to_nonnesting(matching_to_dyck(pairs)))


# =============================================================================
# 講義 A.5–A.8 寫到的數字
# =============================================================================
def check_numbers():
    trees3 = binary_trees(3)
    words3 = [tree_to_dyck(t) for t in trees3]
    # ---------------------------------------------------------------- A.5 平面樹
    assert [catalan(n) for n in range(5)] == [1, 1, 2, 5, 14]
    for n in range(8):
        assert len(plane_trees(n)) == len(plane_trees_bruteforce(n)) == catalan(n)
        assert set(plane_trees(n)) == set(plane_trees_bruteforce(n))
        assert all(plane_tree_edges(p) == n and len(plane_tree_preorder(p)) == n + 1 for p in plane_trees(n))
    # 根＋左＋右：第一個小孩的子樹（k 條邊）與其餘部分（n-1-k 條邊），可以拼回去
    for n in range(1, 7):
        seen = set()
        for p in plane_trees(n):
            first, rest = p[0], p[1:]
            k = plane_tree_edges(first)
            assert plane_tree_edges(rest) == n - 1 - k
            assert (first,) + rest == p
            seen.add((first, rest))
        assert len(seen) == catalan(n) == sum(catalan(k) * catalan(n - 1 - k) for k in range(n))
    # 交換小孩的兩棵：同一棵一般的樹、不同的平面樹；4 個頂點、3 條邊；是 n=3 那一列的第 3、2 棵
    assert canon(SWAP_A) == canon(SWAP_B) and SWAP_A != SWAP_B
    assert plane_tree_edges(SWAP_A) == 3 and len(plane_tree_preorder(SWAP_A)) == 4
    assert plane_trees(3).index(SWAP_B) == 1 and plane_trees(3).index(SWAP_A) == 2
    # n=3 的五棵依 binary_trees(3) 的順序（和圖 onenumber 的欄一致）；第 4 棵是貫穿的例子
    assert tuple(binary_to_plane(t) for t in trees3) == plane_trees(3)
    assert EX == trees3[3] and PT == (((), ()),) == plane_trees(3)[3]

    # ---------------------------------------------------------------- A.6 弧圖
    four = [norm(m) for m in perfect_matchings(4)]
    assert four == [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    assert not arcs_cross(*four[0]) and not arcs_nest(*four[0])
    assert arcs_cross(*four[1]) and not arcs_nest(*four[1])
    assert arcs_nest(*four[2]) and not arcs_cross(*four[2])
    ex_m = norm(dyck_to_matching("UUDUDD"))
    assert one_based(ex_m) == [(1, 6), (2, 3), (4, 5)]
    assert matching_is_noncrossing(ex_m) and matching_nestings(ex_m) == [(0, 1), (0, 2)]  # (1,6) 包住另外兩條
    all6 = [norm(m) for m in perfect_matchings(6)]
    assert len(all6) == 15 == 5 * 3 * 1
    for idx, m in enumerate(all6):                     # 圖的第 c 欄：點 1 配點 c+2
        c, r = divmod(idx, 3)
        assert m[0] == (0, c + 1)
        rest = sorted(set(range(6)) - {0, c + 1})      # 剩下最左邊的點有 3 個對象（第 r 列），最後兩點只有 1 種
        assert m[1] == (rest[0], rest[1 + r]) and len(rest) - 1 == 3
    nc6 = [m for m in all6 if matching_is_noncrossing(m)]
    nn6 = [m for m in all6 if matching_is_nonnesting(m)]
    assert len(nc6) == len(nn6) == 5 == catalan(3)
    assert [m for m in nc6 if m in nn6] == [SHARED]
    both_bad = [m for m in all6 if matching_crossings(m) and matching_nestings(m)]
    assert len(both_bad) == 6 == 15 - (5 + 5 - 1)      # 其餘 6 種既有交叉也有巢狀
    assert words3 == ["UDUDUD", "UDUUDD", "UUDDUD", "UUDUDD", "UUUDDD"]
    nc_row = [norm(dyck_to_matching(w)) for w in words3]
    nn_row = [norm(dyck_to_nonnesting(w)) for w in words3]
    assert sorted(nc_row) == sorted(nc6) and sorted(nn_row) == sorted(nn6)
    assert one_based(nn_row[3]) == [(1, 3), (2, 5), (4, 6)]
    assert all(matching_to_dyck(a) == w == matching_to_dyck(b) for a, b, w in zip(nc_row, nn_row, words3))
    # 證明：左端 U、右端 D 一定是 Dyck 字；不交叉 <=> 後進先出；不巢狀 <=> 先進先出；都是 C_n
    for n in range(1, 6):
        ms = [norm(m) for m in perfect_matchings(2 * n)]
        dfact = math.prod(range(1, 2 * n, 2))
        assert len(ms) == dfact
        assert all(is_dyck(matching_to_dyck(m)) for m in ms)
        assert all(matching_is_noncrossing(m) == lifo_ok(m) for m in ms)
        assert all(matching_is_nonnesting(m) == fifo_ok(m) for m in ms)
        assert sum(map(matching_is_noncrossing, ms)) == sum(map(matching_is_nonnesting, ms)) == catalan(n)
        # 「D 配給 i，中間還有沒配的 U」<=> 有交叉；「i 之前還有沒配的 U」<=> 有巢狀
        for m in ms:
            partner = {a: b for a, b in m}
            mid_open = any(a < j < b < partner[j] for a, b in m for j in partner)
            early_open = any(h < a and b < partner[h] for a, b in m for h in partner)
            assert mid_open == bool(matching_crossings(m))
            assert early_open == bool(matching_nestings(m))

    # ---------------------------------------------------------------- A.7 對偶樹
    m = 5
    diags = sorted(tree_to_triangulation(EX, 0, m - 1))
    assert one_based(diags) == [(1, 4), (2, 4)]
    dual = triangulation_dual(EX)
    tri1 = [tuple(x + 1 for x in d["tri"]) for d in dual]       # 中序：B、C、A
    assert tri1 == [(1, 2, 4), (2, 3, 4), (1, 4, 5)]
    assert dual[2]["parent"] is None and dual[2]["base"] == (0, 4)          # A = {1,4,5} 是根
    assert dual[2]["left"] == ("tri", 0) and dual[2]["right"] == ("leaf", 3)  # 越過 {1,4} 是 B；{4,5} 是葉子
    assert dual[0]["left"] == ("leaf", 0) and dual[0]["right"] == ("tri", 1)  # B：{1,2} 葉子；越過 {2,4} 是 C
    assert dual[1]["left"] == ("leaf", 1) and dual[1]["right"] == ("leaf", 2)  # C：{2,3}、{3,4} 葉子
    leaves = sorted(d[s][1] for d in dual for s in ("left", "right") if d[s][0] == "leaf")
    assert [(e + 1, e + 2) for e in leaves] == [(1, 2), (2, 3), (3, 4), (4, 5)]
    assert triangulation_to_tree(m, diags) == EX
    assert tree_size(EX[0]) + 2 == 4                   # 根三角形的第三個頂點 = 左子樹節點數 + 2
    a, k, b = dual[2]["tri"]                           # 根 {1,4,5}：左邊四邊形 {1,2,3,4}、右邊只剩邊 {4,5}
    assert [x + 1 for x in range(a, k + 1)] == [1, 2, 3, 4] and (k + 1, b + 1) == (4, 5)
    assert tree_size(EX[0]) == 2 and EX[1] is None     # 左子樹 B、C 兩個節點；右子樹是一片葉子
    for n in range(0, 7):                              # 一般的 n：n 個三角形、n-1 條對角線、n+1 片葉子；一一對應
        for t in binary_trees(n):
            dg = tree_to_triangulation(t, 0, n + 1)
            assert len(dg) == max(n - 1, 0) and triangulation_to_tree(n + 2, dg) == t
            assert plane_to_binary(binary_to_plane(t)) == t
            if n >= 1:
                d = triangulation_dual(t)
                assert len(d) == n
                assert sum(1 for x in d for s in ("left", "right") if x[s][0] == "leaf") == n + 1
                assert tree_size(t[0]) + 2 == d[tree_size(t[0])]["tri"][1] + 1
                assert plane_parents_by_rule(t) == [p for p, _ in plane_tree_preorder(binary_to_plane(t))]
    pre = binary_preorder(EX)
    assert pre == [2, 0, 1]                            # A, B, C（中序位置）
    assert plane_parents_by_rule(EX) == [None, 0, 1, 1]  # 根 -> A -> B、C

    # ---------------------------------------------------------------- A.8 DFS
    steps = walk_steps(PT)
    word = "".join(s[2] for s in steps)
    assert plane_tree_walk(PT) == [0, 1, 2, 1, 3, 1, 0]      # 根 A B A C A 根
    assert word == plane_tree_dfs(PT) == tree_to_dyck(EX) == "UUDUDD"
    assert heights(word) == [0, 1, 2, 1, 2, 1, 0]
    assert [d for _, d in plane_tree_preorder(PT)] == [0, 1, 2, 2]
    assert all(heights(word)[k] == plane_tree_preorder(PT)[v][1] for k, v in enumerate(plane_tree_walk(PT)))
    esp = edge_step_pairs(steps)
    assert {v: (a + 1, b + 1) for v, (a, b) in esp.items()} == {1: (1, 6), 2: (2, 3), 3: (4, 5)}
    assert sorted(esp.values()) == dyck_to_matching(word) == [(0, 5), (1, 2), (3, 4)]
    for n in range(0, 8):                               # 一般的 n：DFS 是一一對應，而且與第 1 節的「根＋左＋右」相同
        for t in binary_trees(n):
            p = binary_to_plane(t)
            w = plane_tree_dfs(p)
            assert w == tree_to_dyck(t) and is_dyck(w) and len(w) == 2 * n
            assert sorted(edge_step_pairs(walk_steps(p)).values()) == dyck_to_matching(w)
            assert matching_is_noncrossing(dyck_to_matching(w)) and matching_to_dyck(dyck_to_matching(w)) == w
        assert len({plane_tree_dfs(p) for p in plane_trees(n)}) == catalan(n)
    # 鏈的上色：A 是根（橘），B、C 是左子樹（青）
    assert plane_parts(PT) == {1: "root", 2: "left", 3: "left"}
    assert [plane_parts(PT)[s[3]] for s in steps] == dyck_parts(EX)
    assert [plane_parts(PT)[v] for v in sorted(plane_parts(PT))] == matching_parts(EX)
    print("附錄 A 第 2 段（A.5–A.8）的數字檢查通過")


# =============================================================================
# 圖元
# =============================================================================
def plane_tree_layout(pt_, gap: float, level: float) -> list:
    """與 mit_draw.PlaneTreeMob 相同：葉子依 DFS 等距、內部頂點在第一個與最後一個小孩正中間；根在 (0, 0)。"""
    pre = plane_tree_preorder(pt_)
    kids = [[] for _ in pre]
    for v, (p, _) in enumerate(pre):
        if p is not None:
            kids[p].append(v)
    xs = [0.0] * len(pre)
    nxt = [0]

    def rec(v):
        if not kids[v]:
            xs[v] = nxt[0]
            nxt[0] += 1
            return
        for c in kids[v]:
            rec(c)
        xs[v] = (xs[kids[v][0]] + xs[kids[v][-1]]) / 2

    rec(0)
    return [((xs[v] - xs[0]) * gap, -d * level) for v, (_, d) in enumerate(pre)]


def plane_prims(pt_, gap: float, level: float, vcol=None, ecol=None, node_r=0.045, root_r=0.06,
                edge_w=0.8, hollow_root=False, labels=None):
    """平面樹。vcol／ecol：頂點 v／連到 v 的邊的顏色（dict），預設藍點、灰邊；根是黑點（或空心）。"""
    pos = plane_tree_layout(pt_, gap, level)
    pre = plane_tree_preorder(pt_)
    vcol, ecol = vcol or {}, ecol or {}
    prims = []
    for v in range(1, len(pre)):
        prims.append(("line", f"{ecol.get(v, 'gray!70')},line width={edge_w}pt,line cap=round", pos[pre[v][0]], pos[v]))
    if hollow_root:
        prims.append(("dot", "white", pos[0], root_r))
        prims.append(("circle", "black,line width=0.6pt", pos[0], root_r))
    else:
        prims.append(("dot", "black", pos[0], root_r))
    for v in range(1, len(pre)):
        prims.append(("dot", vcol.get(v, "cA"), pos[v], node_r))
    for v, (text, (dx, dy)) in (labels or {}).items():
        prims.append(node((pos[v][0] + dx, pos[v][1] + dy), text, "font=\\scriptsize,inner sep=0pt", (0.1, 0.1)))
    return prims, pos


def arc_diagram(pairs, npts: int, gap: float, x0: float, y0: float, colors=None, w=1.0, hr=1.0,
                labels=False, dot_r=0.03, margin=0.12, font="\\scriptsize", label_dy=0.2):
    """直線上的弧圖（點 i 在 x0 + i*gap）；弧是上半個橢圓，高 = hr × 半寬。回傳 TikZ 行。"""
    xs = [x0 + i * gap for i in range(npts)]
    lines = [rf"\draw[gray!60,line width=0.4pt] {pt(xs[0] - margin, y0)} -- {pt(xs[-1] + margin, y0)};"]
    for j, (a, b) in enumerate(pairs):
        col = colors[j] if colors else "cA"
        r = (xs[b] - xs[a]) / 2
        lines.append(rf"\draw[{col},line width={w}pt] {pt(xs[a], y0)} arc[start angle=180,end angle=0,"
                     rf"x radius={f(r)},y radius={f(hr * r)}];")
    for x in xs:
        lines.append(rf"\fill {pt(x, y0)} circle ({f(dot_r)});")
    if labels:
        names = labels if isinstance(labels, (list, tuple)) else [str(i + 1) for i in range(npts)]
        for x, s in zip(xs, names):
            lines.append(rf"\node[font={font},inner sep=0pt] at {pt(x, y0 - label_dy)} {{{s}}};")
    return lines


def frame(x0, y0, x1, y1, style) -> str:
    return rf"\draw[{style},rounded corners=2pt] {pt(x0, y0)} rectangle {pt(x1, y1)};"


def arrow(p, q, style="gray!60!black,line width=0.7pt", tip="-{Stealth[length=5pt]}") -> str:
    return rf"\draw[{tip},{style}] {pt(*p)} -- {pt(*q)}"


# =============================================================================
# 圖
# =============================================================================
def fig_m05_trees() -> str:
    """左：交換根的兩個小孩 -> 不同的平面樹。右：n = 0..3 的所有平面樹（順序同 binary_trees）。"""
    lines = []
    # ---- 左：交換小孩
    for x, tree, kid_branch in ((0.0, SWAP_A, (1, 2)), (2.6, SWAP_B, (2, 3))):
        vc = {v: BRANCH["kid"] if v in kid_branch else BRANCH["leaf"] for v in (1, 2, 3)}
        prims, pos = plane_prims(tree, 0.95, 0.75, vcol=vc, ecol=vc, node_r=0.07, root_r=0.085, edge_w=1.4)
        prims.append(node((pos[0][0], pos[0][1] + 0.3), "根", "font=\\scriptsize", (0.15, 0.12)))
        lines += emit(prims, x, 0.0)
    lines.append(r"\node[font=\Large] at (1.3,-0.55) {$\neq$};")
    lines.append(r"\node[font=\scriptsize,align=center,text=gray!40!black] at (1.3,-1.95) "
                 r"{不管順序是同一棵樹；\\作為平面樹是不同的兩棵};")
    lines.append(r"\draw[gray!40,line width=0.4pt] (3.95,0.45) -- (3.95,-2.75);")
    # ---- 右：n = 0..3
    x_lab, x0, step, x_cnt = 4.35, 5.85, 1.12, 11.55
    top = {0: 0.38, 1: -0.12, 2: -0.75, 3: -1.65}
    for n in range(4):
        y = top[n]
        lines.append(rf"\node[anchor=west,font=\small] at {pt(x_lab, y - 0.12)} {{$n={n}$}};")
        for i, p in enumerate(plane_trees(n)):
            prims, _ = plane_prims(p, 0.3, 0.3)
            lines += emit(prims, x0 + step * i, y)
            if n == 3:
                lines.append(rf"\node[font=\tiny,text=gray!60!black] at {pt(x0 + step * i, y - 1.12)} {{{i + 1}}};")
        lines.append(rf"\node[font=\small] at {pt(x_cnt, y - 0.12)} {{$C_{n}={catalan(n)}$}};")
    i0, i1 = plane_trees(3).index(SWAP_B), plane_trees(3).index(SWAP_A)
    lines.append(frame(x0 + step * i0 - 0.42, top[3] + 0.17, x0 + step * i1 + 0.42, top[3] - 1.0,
                       "gray!55,dashed,line width=0.5pt"))
    k = plane_trees(3).index(PT)
    lines.append(frame(x0 + step * k - 0.42, top[3] + 0.17, x0 + step * k + 0.42, top[3] - 1.0,
                       "cTop,line width=0.7pt"))
    return picture(lines)


def fig_m06_cut() -> str:
    """左：圓上的配對 (1,6),(2,3),(4,5) 在點 6、1 之間剪開，攤平成弧圖。右：兩條弧的三種關係。"""
    pairs = norm(dyck_to_matching("UUDUDD"))
    r = 0.9
    lines = emit(matching_prims(pairs, 6, r, labels=True))
    a = math.radians(120)                                   # 點 1（90°）與點 6（150°）之間
    c, s = math.cos(a), math.sin(a)
    # 剪開的記號只畫在弦 (1,6) 外側（弦到圓心的距離是 r·cos30°），不要和弦重疊
    lo, hi = r - 0.075, r + 0.2
    assert lo > r * math.cos(math.radians(30)) + 0.03
    lines.append(rf"\draw[cBad,line width=1.2pt] {pt(lo * c, lo * s)} -- {pt(hi * c, hi * s)};")
    lines.append(rf"\node[font=\scriptsize,text=cBad,anchor=south east] at {pt((hi - 0.04) * c, (hi - 0.04) * s)} {{剪開}};")
    lines.append(arrow((1.35, 0.0), (2.35, 0.0)) + r" node[midway,above,font=\scriptsize] {攤平};")
    lines += arc_diagram(pairs, 6, 0.5, 2.75, -0.45, w=1.1, labels=True)
    # ---- 右：i<j<k<l 的三種配法
    lines.append(r"\draw[gray!40,line width=0.4pt] (5.85,1.15) -- (5.85,-1.15);")
    four = [norm(m) for m in perfect_matchings(4)]
    cols = [("分開", r"(i,j),(k,l)", "cA", four[0]), ("交叉", r"(i,k),(j,l)", "cBad", four[1]),
            ("巢狀", r"(i,l),(j,k)", NEST, four[2])]
    gap = 0.4
    for idx, (name, formula, col, m) in enumerate(cols):
        cx = 7.0 + 2.0 * idx
        x0 = cx - 1.5 * gap
        lines += arc_diagram(m, 4, gap, x0, 0.15, colors=[col, col], w=1.1, hr=0.85, labels=list("ijkl"),
                             font="\\scriptsize", label_dy=0.17)
        lines.append(rf"\node[font=\small,text={col}] at {pt(cx, -0.42)} {{{name}}};")
        lines.append(rf"\node[font=\small] at {pt(cx, -0.85)} {{${formula}$}};")
    lines.append(r"\node[font=\small] at (9.0,1.0) {$i<j<k<l$};")
    return picture(lines)


def fig_m06_count() -> str:
    """
    左：6 點的 15 種完美配對（第 c 欄：點 1 配點 c+2）；藍框 = 不交叉，綠虛框 = 不巢狀。
    右：同一個 Dyck 字（左端 U、右端 D）的不交叉配對（後進先出）與不巢狀配對（先進先出）。
    """
    lines = []
    # ---- 左：15 種
    gap, cw, rh, hr = 0.22, 1.78, 0.86, 0.85
    for idx, m in enumerate(perfect_matchings(6)):
        m = norm(m)
        c, r = divmod(idx, 3)
        x0, y0 = c * cw, -r * rh
        lines += arc_diagram(m, 6, gap, x0, y0, w=0.9, hr=hr, dot_r=0.022, margin=0.1)
        left, right = x0 - 0.16, x0 + 5 * gap + 0.16
        top_in, top_out, bot_in, bot_out = 0.56, 0.62, -0.08, -0.14
        assert top_in > hr * 5 * gap / 2 + 0.05                  # 最高的弧在藍框裡
        assert rh - (top_out - bot_out) > 0.08                   # 上下兩列的綠框不相碰
        if matching_is_noncrossing(m):
            lines.append(frame(left, y0 + bot_in, right, y0 + top_in, "cA,line width=0.75pt"))
        if matching_is_nonnesting(m):
            lines.append(frame(left - 0.07, y0 + bot_out, right + 0.07, y0 + top_out,
                               f"{NN_FRAME},dashed,line width=0.75pt"))
    for c in range(5):
        lines.append(rf"\node[font=\scriptsize,text=gray!50!black] at {pt(c * cw + 2.5 * gap, 0.93)} "
                     rf"{{點 1 配點 {c + 2}}};")
    # ---- 右：依 Dyck 字排成兩欄
    xs = 9.35
    lines.append(rf"\draw[gray!40,line width=0.4pt] {pt(xs - 0.45, 1.05)} -- {pt(xs - 0.45, -2.05)};")
    gap2, pitch = 0.2, 0.6
    x_nc, x_w, x_nn = xs, xs + 1.95, xs + 2.95
    lines += [
        rf"\node[font=\scriptsize,text=cA] at {pt(x_nc + 2.5 * gap2, 0.93)} {{不交叉}};",
        rf"\node[font=\scriptsize] at {pt(x_w, 0.93)} {{Dyck 字}};",
        rf"\node[font=\scriptsize,text=green!40!black] at {pt(x_nn + 2.5 * gap2, 0.93)} {{不巢狀}};",
    ]
    words = [tree_to_dyck(t) for t in binary_trees(3)]
    for j, w in enumerate(words):
        y0 = 0.38 - j * pitch
        lines += arc_diagram(norm(dyck_to_matching(w)), 6, gap2, x_nc, y0, w=0.9, hr=0.75, dot_r=0.02, margin=0.08)
        lines.append(rf"\node[font=\scriptsize] at {pt(x_w, y0 + 0.13)} {{$\mathrm{{{w}}}$}};")
        lines += arc_diagram(norm(dyck_to_nonnesting(w)), 6, gap2, x_nn, y0, w=0.9, hr=0.75, dot_r=0.02,
                             margin=0.08, colors=[NN_FRAME] * 3)
    k = words.index("UUDUDD")
    yk = 0.38 - k * pitch
    lines.append(frame(x_nc - 0.15, yk - 0.09, x_nn + 5 * gap2 + 0.15, yk + 0.47, "cTop,line width=0.6pt"))
    return picture(lines)


def fig_m07_dual() -> str:
    """
    (a) 五邊形的三角剖分（對角線 {1,4}、{2,4}）與它的對偶圖；(b) 整理成標準畫法的滿二元樹；
    (c) 去掉葉子，左小孩的邊青色、右小孩的邊紫紅色；(d) 平面樹（新的根 -> A -> B、C）。
    """
    m, r = 5, 1.15
    v = polygon_vertices(m, r)
    dual = triangulation_dual(EX)
    pre = binary_preorder(EX)
    name = {b: "ABC"[i] for i, b in enumerate(pre)}           # 中序位置 -> 名字
    root = tree_size(EX[0])

    def centroid(tri):
        return (sum(v[i][0] for i in tri) / 3, sum(v[i][1] for i in tri) / 3)

    def leaf_pt(e, out=0.36):
        mx, my = (v[e][0] + v[e + 1][0]) / 2, (v[e][1] + v[e + 1][1]) / 2
        d = math.hypot(mx, my)
        return mx + out * mx / d, my + out * my / d

    lines = []
    # ---- (a)
    for i, d in enumerate(dual):
        fill = "cTop!30" if i == root else "cA!10"
        lines.append(rf"\fill[{fill}] " + " -- ".join(pt(*v[k]) for k in d["tri"]) + " -- cycle;")
    lines.append(r"\draw[gray!70,line width=0.6pt,line join=round] " + " -- ".join(pt(*p) for p in v) + " -- cycle;")
    for a, b in tree_to_triangulation(EX, 0, m - 1):
        lines.append(rf"\draw[cA,line width=1.1pt,line cap=round] {pt(*v[a])} -- {pt(*v[b])};")
    lines.append(rf"\draw[cTop,line width=2pt,line cap=round] {pt(*v[0])} -- {pt(*v[m - 1])};")
    lines.append(rf"\node[font=\scriptsize,text=cTop] at {pt(0, v[0][1] - 0.2)} {{底邊}};")
    for k, p in enumerate(v):
        lines.append(rf"\fill {pt(*p)} circle (0.033);")
        lp = polygon_vertices(m, r + 0.22)[k]
        lines.append(rf"\node[font=\scriptsize] at {pt(*lp)} {{{k + 1}}};")
    cen = [centroid(d["tri"]) for d in dual]
    for i, d in enumerate(dual):
        for side in ("left", "right"):
            kind, j = d[side]
            end = cen[j] if kind == "tri" else leaf_pt(j)
            lines.append(rf"\draw[black!50,line width=0.8pt,line cap=round] {pt(*cen[i])} -- {pt(*end)};")
    for e in range(m - 1):
        x, y = leaf_pt(e)
        lines.append(rf"\fill[gray!60] {pt(x - 0.042, y - 0.042)} rectangle {pt(x + 0.042, y + 0.042)};")
    offs = {"A": (0.02, -0.2), "B": (-0.16, 0.15), "C": (0.17, -0.1)}
    for i in range(len(dual)):
        lines.append(rf"\fill[{'cTop' if i == root else 'cA'}] {pt(*cen[i])} circle (0.055);")
        dx, dy = offs[name[i]]
        lines.append(rf"\node[font=\scriptsize] at {pt(cen[i][0] + dx, cen[i][1] + dy)} {{{name[i]}}};")
    # ---- (b) 標準畫法（根／左／右上色）
    lines.append(arrow((1.85, 0.05), (3.05, 0.05)) + r" node[midway,above,font=\scriptsize] {拿掉多邊形};")
    prims = tree_prims(EX, gap=0.5, level=0.5, colored=True, node_r=0.055, leaf_s=0.042, edge_w=1.0)
    dots = [p for p in prims if p[0] == "dot"]                 # 依中序：B、C、A
    loffs = {"A": (0.0, 0.19), "B": (-0.18, 0.06), "C": (0.18, 0.06)}
    for i, dp in enumerate(dots):
        dx, dy = loffs[name[i]]
        prims.append(node((dp[2][0] + dx, dp[2][1] + dy), name[i], "font=\\scriptsize,inner sep=0pt", (0.07, 0.07)))
    lines += place(prims, 4.1, 0.0)
    lines.append(r"\draw[gray!40,line width=0.4pt] (5.5,1.3) -- (5.5,-1.3);")
    # ---- (c) 去掉葉子
    par = plane_parents_by_rule(EX)
    assert par == [None, 0, 1, 1]
    X = 1.1                                                    # (c)(d) 整體往右移
    A, B, C = (5.45 + X, 0.55), (4.95 + X, -0.15), (5.45 + X, -0.85)   # B 是 A 的左小孩、C 是 B 的右小孩
    lines.append(rf"\draw[cLeft,line width=1.2pt,line cap=round] {pt(*A)} -- {pt(*B)};")
    lines.append(rf"\draw[cRight,line width=1.2pt,line cap=round] {pt(*B)} -- {pt(*C)};")
    for p, s, (dx, dy) in ((A, "A", (0.18, 0.05)), (B, "B", (-0.18, 0.0)), (C, "C", (0.18, 0.0))):
        lines.append(rf"\fill[cA] {pt(*p)} circle (0.06);")
        lines.append(rf"\node[font=\scriptsize] at {pt(p[0] + dx, p[1] + dy)} {{{s}}};")
    lines.append(rf"\node[font=\tiny,text=cLeft] at {pt(5.05 + X, 0.33)} {{左}};")
    lines.append(rf"\node[font=\tiny,text=cRight] at {pt(5.07 + X, -0.6)} {{右}};")
    lines.append(arrow((6.1 + X, -0.15), (8.65 + X, -0.15))
                 + r" node[midway,above,font=\scriptsize,align=center] "
                   r"{\textcolor{cLeft}{左小孩} $\to$ 第一個小孩\\\textcolor{cRight}{右小孩} $\to$ 下一個兄弟}"
                 + r" node[midway,below,font=\scriptsize] {加一個新的根};")
    # ---- (d) 平面樹
    prims, _ = plane_prims(PT, 0.9, 0.62, vcol={1: "cA", 2: "cA", 3: "cA"},
                           ecol={1: "gray!60", 2: "cLeft", 3: "cRight"}, node_r=0.06, root_r=0.07,
                           edge_w=1.2, hollow_root=True,
                           labels={0: ("新的根", (0.0, 0.22)), 1: ("A", (0.18, 0.04)),
                                   2: ("B", (-0.18, 0.0)), 3: ("C", (0.18, 0.0))})
    lines += emit(prims, 9.5 + X, 0.75)
    return picture(lines)


def fig_m08_walk() -> str:
    """平面樹沿輪廓走一圈（邊旁的數字是第幾步）-> Dyck 路徑 UUDUDD -> 弧圖 -> 圓上的配對。"""
    steps = walk_steps(PT)
    word = "".join(s[2] for s in steps)
    esp = edge_step_pairs(steps)
    lines = []
    # ---- 平面樹
    tx, ty = 0.0, 0.35
    pos = [(x + tx, y + ty) for x, y in plane_tree_layout(PT, 1.6, 0.95)]
    par = [p for p, _ in plane_tree_preorder(PT)]
    for vtx in range(1, 4):
        lines.append(rf"\draw[gray!70,line width=1.1pt,line cap=round] {pt(*pos[par[vtx]])} -- {pt(*pos[vtx])};")
    lines.append(rf"\fill {pt(*pos[0])} circle (0.07);")
    for vtx in range(1, 4):
        lines.append(rf"\fill[cA] {pt(*pos[vtx])} circle (0.06);")
    names = {0: ("根", (0.0, 0.24)), 1: ("A", (0.3, 0.02)), 2: ("B", (0.0, -0.24)), 3: ("C", (0.0, -0.24))}
    for vtx, (s, (dx, dy)) in names.items():
        lines.append(rf"\node[font=\scriptsize] at {pt(pos[vtx][0] + dx, pos[vtx][1] + dy)} {{{s}}};")
    for vtx, (down, up) in esp.items():
        (x0, y0), (x1, y1) = pos[par[vtx]], pos[vtx]
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy)
        nx, ny = dy / ln, -dx / ln                       # 往下走時在這一側（d 順時針轉 90°）
        mx, my = x0 + 0.5 * dx, y0 + 0.5 * dy
        o = 0.24
        lines.append(rf"\node[font=\scriptsize,text=cTop] at {pt(mx + o * nx, my + o * ny)} {{{down + 1}$\downarrow$}};")
        lines.append(rf"\node[font=\scriptsize,text=cTop] at {pt(mx - o * nx, my - o * ny)} {{{up + 1}$\uparrow$}};")
    # ---- Dyck 路徑（每一步的中點對準下方弧圖的點）
    u, px, py = 0.5, 1.75, -0.3
    lines += emit(dyck_prims(word, u, w=1.3), px, py)
    for k, c in enumerate(word):
        lines.append(rf"\node[font=\scriptsize] at {pt(px + (k + 0.5) * u, py - 0.22)} {{{c}}};")
    lines.append(rf"\node[font=\scriptsize,anchor=west,text=gray!50!black] at {pt(px + 6 * u + 0.08, py)} {{地面}};")
    # ---- 弧圖
    ay = -1.95
    lines += arc_diagram(dyck_to_matching(word), 6, u, px + 0.5 * u, ay, w=1.1, hr=0.6, labels=True)
    # ---- 捲回圓上
    cx, cy, r = 7.55, -1.2, 0.75
    lines.append(arrow((px + 6 * u + 0.2, ay + 0.3), (cx - r - 0.42, cy - 0.15))
                 + r" node[midway,above,sloped,font=\scriptsize] {捲回圓上};")
    lines += emit(matching_prims(dyck_to_matching(word), 6, r, labels=True), cx, cy)
    return picture(lines)


def fig_m08_chain() -> str:
    """貫穿的例子的五種樣子，依根／左／右上色（與圖 onenumber 第 4 欄、場景 M08 結尾相同）。"""
    word, parts = tree_to_dyck(EX), dyck_parts(EX)
    pp = plane_parts(PT)
    pcol = {v: COLOR[p] for v, p in pp.items()}
    plane, _ = plane_prims(PT, 0.62, 0.5, vcol=pcol, ecol=pcol, node_r=0.055, root_r=0.065, edge_w=1.2,
                           hollow_root=True)
    items = [
        ("三角剖分", tri_prims(5, tree_to_triangulation(EX, 0, 4), 0.72, tree=EX)),
        ("二元樹", tree_prims(EX, gap=0.42, level=0.4)),
        ("平面樹", plane),
        ("Dyck 路徑", dyck_prims(word, 0.26, parts, w=1.3)),
        ("不交叉配對", matching_prims(dyck_to_matching(word), 6, 0.62, parts=matching_parts(EX), root=True)),
    ]
    rules = ["對偶圖", "小孩／兄弟", "輪廓走法", "U 配 D"]
    sp = 3.3
    lines = []
    for j, (name, prims) in enumerate(items):
        lines += place(prims, j * sp, 0.0)
        lines.append(rf"\node[font=\small] at {pt(j * sp, -1.05)} {{{name}}};")
    for j, rule in enumerate(rules):
        a, b = j * sp + 0.95, (j + 1) * sp - 0.95
        lines.append(arrow((a, 0.0), (b, 0.0), tip="{Stealth[length=4pt]}-{Stealth[length=4pt]}")
                     + rf" node[midway,above,font=\scriptsize,text=gray!40!black] {{{rule}}};")
    return picture(lines)


FIGURES = [
    ("FigMfiveTrees", fig_m05_trees),
    ("FigMsixCut", fig_m06_cut),
    ("FigMsixCount", fig_m06_count),
    ("FigMsevenDual", fig_m07_dual),
    ("FigMeightWalk", fig_m08_walk),
    ("FigMeightChain", fig_m08_chain),
]


def main():
    check_numbers()
    out = [
        "% figs_part2.tex —— 由 mit/make_figs_part2.py 產生，請勿手動修改（附錄 A.5–A.8，動畫 M05–M08）。\n"
        "% 重新產生：python notes/mit/make_figs_part2.py\n"
    ]
    for name, func in FIGURES:
        body = func()
        assert "\n\n" not in body
        out.append(f"\\newcommand{{\\{name}}}{{%\n{body}}}\n")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"已寫出 {OUT.name}：{len(FIGURES)} 張圖")


if __name__ == "__main__":
    main()
