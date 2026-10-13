# Fulton《Young Tableaux》第 8 章 → Manim：精簡計畫（2026-10-12）

> 本檔的相對路徑以 `C:\mypython\manim\projects\catalan930\` 為基準。
> 來源：`../ref/fulton78_manim_大綱_合併版.md` 的「第五幕」F800–F803（第 1758–1872 行），Fulton §8.1–§8.4（書 p.104–126）。
> 製作規則與場景骨架**沿用 `notes/fulton_plan_ch7.md` 第 4、5 節**（只差：資料不從 JSON 取，改由 `utils.tableaux` 現算並 assert）。

## 1. 決定
- 4 幕 F42–F45，獨立連續播放 `FultonDemo5`（不接 FultonDemo4；舊影片不動）。每幕約 3 分。
- 主例沿用 $\lambda=(2,1)$、$n=3$：從 $S_3$ 的 $S^{(2,1)}$（2 維）走到 $GL(E)$ 的 $E^{(2,1)}$（$m=3$ 時 8 維）。
- 記號用 Fulton：$E=\mathbb C^m$、$E^\lambda$（Schur 模）、$e_T$、$\operatorname{Char}$、$d_\lambda(m)$、$f^\lambda$；字幕「列＝row、行＝column」。
- 一個代理人做完 4 幕；接進 main.py／render_all.py、輸出 1080p、文件與 combkit 由我來做。

## 2. 已核對數字（`utils.tableaux`：`ssyt`、`content`、`hook_content_count`、`standard_tableaux`、`schur_poly`）
- $m=2$：$(2,1)$ 的半標準表 $\yts{11,2}$、$\yts{12,2}$；$d_{(2,1)}(2)=2$。$m=3$：8 個；$d_{(2,1)}(m)=m(m^2-1)/3$。
- $m=3$ 的權重分堆（content）：$(2,1,0)$:11/2；$(2,0,1)$:11/3；$(1,2,0)$:12/2；$(1,1,1)$:12/3、13/2（兩個）；$(1,0,2)$:13/3；$(0,2,1)$:22/3；$(0,1,2)$:23/3。最高權重向量 $e_{U(\lambda)}$＝11/2，權重 $(2,1,0)$。
- $\operatorname{Char}E^{(2,1)}=s_{(2,1)}(x_1,x_2,x_3)$：8 項，$x_1x_2x_3$ 係數 2（其餘係數 1）。
- Schur–Weyl，$n=3$：$m=2$：$8=4\cdot1+2\cdot2+0\cdot1$；$m=3$：$27=10\cdot1+8\cdot2+1\cdot1$（$d_\lambda(m)\cdot f^\lambda$，$\lambda=(3),(2,1),(1,1,1)$）。
- Plücker：$A=\begin{pmatrix}1&2&0&1\\0&1&3&2\end{pmatrix}$，$p_{ij}$＝第 $i,j$ 行的 $2\times2$ 子式：
  $p_{12}=1,p_{13}=3,p_{14}=2,p_{23}=6,p_{24}=3,p_{34}=-3$；$p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=-3-9+12=0$。

## 3. 場景卡（細節查來源卡；衝突時以本檔為準）
| 代號 | 卡 | 主題 | 要點（依序） |
|---|---|---|---|
| F42 | F800 | 把數字換成向量：Schur 模（§8.1，p.104–112） | (2,1) 編號表的 1,2,3 換成 $v_1,v_2,v_3\in E$；一列 → $\operatorname{Sym}^nE$、一行 → $\bigwedge^nE$；$E^\lambda$＝各行外冪的張量積模掉 F39 的同一條交換關係（兩條關係並排，只換符號）；基底＝半標準表：$m=2$ 兩個、$m=3$ 八個（列出）；收束：第 7 章數標準表 $f^\lambda=2$（固定），第 8 章數半標準表 $d_\lambda(m)$（隨 $m$ 變） |
| F43 | F801 | 對角矩陣數格子：權重（§8.2–8.3，p.112–120） | 只看 $\operatorname{diag}(x_1,x_2,x_3)$：$e_T\mapsto x^Te_T$；沿用 F42 的 8 個表按權重分 7 堆（$x_1x_2x_3$ 那堆 2 個）；最高權重 11/2；多項式不可約表示 ↔ 至多 $m$ 列的 $\lambda$；$\operatorname{Char}=s_\lambda$（第 6 章的物件換了身分） |
| F44 | F802 | 兩個群共用一個空間：Schur–Weyl（§8.3，p.116–124） | $E^{\otimes3}$：$GL(E)$ 同時作用三個因子、$S_3$ 交換因子，兩者可交換（一個小例子示範順序對調結果相同，例如 $g$ 作用與 $(1\,2)$ 交換在 $v_1\otimes v_2\otimes v_3$ 上）；$E^{\otimes n}\cong\bigoplus_\lambda E^\lambda\otimes S^\lambda$；維度表 $m=2,3$（第 2 節）；$E^\lambda\cong E^{\otimes n}\otimes_{\mathbb C[S_n]}S^\lambda$；列數 $>m$ 的項為 0 |
| F45 | F803 | 同一條二次關係，三個身分（§8.4，p.124–126；§7.4） | 三欄並排：Specht 的交換關係、Schur 模的關係、$2\times4$ 矩陣的 $2\times2$ 子式；用第 2 節的 $A$ 逐項算 $p_{12}p_{34}$、$p_{13}p_{24}$、$p_{14}p_{23}$ 並相消為 0；二次關係生成的理想，預告第 9 章 Grassmannian（不說已證明）；結尾總結第 7–8 章 |

## 4. 檔名與類別（`codes/scenes/`）
| 代號 | 檔名 | 類別 |
|---|---|---|
| F42 | `sceneF42_schur_module.py` | `SceneF42SchurModule` |
| F43 | `sceneF43_weights.py` | `SceneF43Weights` |
| F44 | `sceneF44_schur_weyl.py` | `SceneF44SchurWeyl` |
| F45 | `sceneF45_quadratic_relations.py` | `SceneF45QuadraticRelations` |

可用元件同 `fulton_plan_ch7.md` 第 6 節（`tableau_mob`、`MatrixMob`、`signed_sum`、`assert_in_frame` 等）。

> 完成（2026-10-12）：F42–F45 與 `FultonDemo5`（9 分 17 秒）。講義第 8 節：`notes/young_tableaux_導讀.tex`（內文 `notes/fulton/part6.tex`，數字由 `fulton/make_figs.py` 的 `check_numbers_ch8()` 核對），完成（2026-10-13）。
