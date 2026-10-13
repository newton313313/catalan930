# Fulton《Young Tableaux》第 7–8 章 → Manim 演示：大綱（2026-10-12）

> **已併入**（2026-10-12）：`C:\mypython\manim\projectsefulton78_manim_大綱_合併版.md`（以使用者的 F700–F725、X701–X705 為準，第八章延伸改稱 F800–F803）。本檔只留作紀錄。


**路徑的寫法：** 本檔的相對路徑相對於 `C:\mypython\manim\projects\catalan930`。

## 0. 範圍、來源、原則
- 參考：`C:\mypython\manim\projects\ref\Fulton78_整合參考.md`（Fulton 第 7–8 章為主、Sagan 第 1–2 章為輔；附錄 A 是定理對照，附錄 B 是已核對的小例子）。
  原文：`ref\fulton\md\07_…`、`08_…`（OCR）、`ref\sagan\sagan_c1c3.md`。
- 新的一組 F28–F37，獨立播放（不接 F01–F27），連續播放 `FultonDemo4`；舊影片不動。
- **記號**：Fulton（編號 $T$、$R(T)$、$C(T)$、$\{T\}$、$v_T$、$S^\lambda$、$M^\lambda$、$E^\lambda$、$\chi^\lambda_\mu$）；字幕用台灣的「列＝row、行＝column」（與 F01–F27 一致）。
- **生動**：每幕一個鉤子；盡量用 $\lambda=(2,1)$、$n=3$ 這個「貫穿例子」（參考檔 §9.1），一路從 $S_3$ 走到 $GL_m$。
- **省 token**：先寫數學（`tableaux.py` 第 9 節）與檢查，再由 3 個代理人平行做場景；主對話只看總覽圖。

## 1. 數學（`codes/utils/tableaux.py` 第 9 節，待寫）
- 置換：`perm_compose`、`cycle_type`、`conj_class(mu, n)`（列出類裡的置換）、`sign`。
- 編號與 tabloid：`act(sigma, T)`、`row_group(T)`、`col_group(T)`、`tabloid(T)`（frozenset 的 tuple）、`tabloids(lam)`。
- 置換模組與 Specht：向量 = `{tabloid: 係數}`；`polytabloid(T)` = $v_T$；`act_vec`；`specht_basis(lam)`（標準表的 $v_T$）；
  `rep_matrix(lam, sigma)`（$S^\lambda$ 在標準基底下的矩陣，用解線性方程把 $\sigma v_T$ 寫回標準基底）；`trace` → 特徵標，與第 8 節 `character_table` 比對。
- `young_symmetrizer(T)`（群環元素 = `{perm: 係數}`）、`group_ring_mul`；檢查 $c_T^2=n_\lambda c_T$、$n_\lambda=n!/f^\lambda$。
- 第 7.3 節：`induced_character`、`restrict`；檢查 Young's rule、分支律、LR 規則（用特徵標內積 = 第 8 節的 $c^\nu_{\lambda\mu}$）、$S^\lambda\otimes\mathbb U_n\cong S^{\tilde\lambda}$。
- 第 7.4 節：`straighten(T)`（Fulton 的交換關係，把 $[T]$ 寫成標準 $[T]$ 的組合），與 `rep_matrix` 交叉驗證。
- 第 8 章：`semistandard(lam, m)`（已有 `ssyt`）、`weight(T)`、`schur_dim(lam, m)`（= `hook_content_count`）、
  `tensor_power_dims(n, m)`（$m^n=\sum_\lambda d_\lambda(m)f^\lambda$）、`plucker_relation`（$2\times4$ 矩陣的 $p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0$）。

## 2. 場景大綱（書頁碼 p.N；長度是目標）

### 第 7 章：對稱群的表示（F28–F33）
| 代號 | 鉤子 | 內容 | 長度 |
|---|---|---|---|
| F28 | **「同一個形狀，兩種洗牌」**：把 $1,2,3$ 填進 $(2,1)$，允許「同列內洗牌」與「同行內洗牌」 | $\sigma\cdot T$；列群 $R(T)$、行群 $C(T)$（$T=12/3$：$R=\langle(12)\rangle$、$C=\langle(13)\rangle$）；共軛類＝循環型、大小 $n!/z(\mu)$（$S_3$：1、3、2）；Lemma 1：碰撞或可重排（小例子動畫）（p.83–85） | ~70s |
| F29 | **「忘記順序的抽屜」**：tabloid＝每一列只記內容 | $M^{(2,1)}$ 的 3 個 tabloid $t_1,t_2,t_3$；$S_3$ 如何搬動它們（置換矩陣）；$a_T$、$b_T$、$c_T$；$v_T=b_T\{T\}=t_3-t_1$；Specht 模 $S^{(2,1)}$＝「和為 0」的平面（3D 小動畫：$M^{(2,1)}=\mathbb C^3$ 裡的一條線＋一個平面）（p.85–87） | ~75s |
| F30 | **「交錯化讓碰撞消失」** | Lemma 2：同列又同行的一對數 → $b_T\{T'\}=0$；(5a)(5b) → 不可約；命題 1：$S^\lambda$ 正好是全部不可約表示（個數＝分割數＝共軛類數）（p.86–88） | ~70s |
| F31 | **「標準表就是基底」** | 命題 2：標準表的 $v_T$ 是基底，$\dim S^\lambda=f^\lambda$；$\sum(f^\lambda)^2=n!$（接 R-S-K）；$S^{(2,1)}$ 的 2×2 矩陣（Sagan 的 Young 自然表示，對換與 3-循環），跡＝特徵標 $2,0,-1$（p.88–89） | ~75s |
| F32 | **「表示也能相乘：誘導積」** | $M^\lambda=\operatorname{Ind}_{R(T)}^{S_n}\mathbb I$；$M^\lambda$ 的特徵標＝固定的 tabloid 數＝$\xi^\lambda_\mu$；表示環 $R$ 與 $\varphi(h_\lambda)=[M^\lambda]$、$\varphi(s_\lambda)=[S^\lambda]$ 的「翻譯字典」；Young's rule（$M^{(2,1)}=S^{(3)}\oplus S^{(2,1)}$）、LR、分支律（Young 格上加一格／減一格）、Frobenius 公式（接第 6 章的 $\chi$ 表）、$S^\lambda\otimes\mathbb U_n\cong S^{\tilde\lambda}$（p.89–94） | ~80s |
| F33 | **「把歪掉的表扳正」**：straightening | 帶定向的行 tabloid $[T]$；Fulton 的交換關係（相鄰兩行前 $k$ 個互換）；完整手算 $[21/3]=[12/3]-[13/2]$ 與一個 3 行的例子；Garnir（Sagan）一句；$S^\lambda\cong\widetilde M^\lambda/Q^\lambda$；預告第 8 章同樣的關係（p.95–101） | ~75s |

### 第 8 章：一般線性群的表示（F34–F37）
| 代號 | 鉤子 | 內容 | 長度 |
|---|---|---|---|
| F34 | **「把數字換成向量」** | 從編號到向量填法；$E^{(n)}=\operatorname{Sym}^nE$、$E^{(1^n)}=\bigwedge^nE$；$E^\lambda=$（各行的外冪張量積）／（交換關係）；半標準表 ↔ 基底（$m=2,3$ 時 $(2,1)$ 的 2 個、8 個基底）（p.104–110） | ~75s |
| F35 | **「對角矩陣數格子」**：權重 | 對角矩陣 $\operatorname{diag}(x_1..x_m)$ 作用在 $e_T$ 上乘 $x^T$ → 權重空間；最高權重向量 $e_{U(\lambda)}$（每列填自己的列號）；分類定理：多項式不可約表示 ↔ $\lambda$（至多 $m$ 列）；$\operatorname{Char}(E^\lambda)=s_\lambda(x_1..x_m)$（p.111–116、120） | ~75s |
| F36 | **「兩個群共用一個空間」**：Schur–Weyl | $E^{\otimes n}$ 上 $GL(E)$ 左作用、$S_n$ 右作用互相交換；$E^{\otimes n}\cong\bigoplus_\lambda E^\lambda\otimes S^\lambda$；維度檢查 $m^n=\sum d_\lambda(m)f^\lambda$（$m=2,n=3$：$8=4\cdot1+2\cdot2$）；$E(S^\lambda)=E^\lambda$；表示環 $\mathcal R(m)\cong\Lambda(m)$，Pieri／LR 搬過來（p.116–124） | ~80s |
| F37 | **「同一條二次關係，三個身分」** | Specht 的交換關係 = Schur 模的關係 = Plücker 關係：$2\times4$ 矩陣的 $p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0$（隨機矩陣數值驗算）；二次關係生成的理想、Grassmannian 預告（第 9 章）（p.124–126） | ~70s |

連續播放：`FultonDemo4` = F28–F37。

## 3. 實作規則（同 `fulton_plan_ch5-6.md` 第 4 節）
- ManimGL、`ChuScene`、模組層級函式、每個數字都 assert、`fulton_draw` 的版面檢查；字幕繁中、自己的話。
- 新的畫圖工具（若需要）放 `utils/fulton_draw.py` 以外的新檔（例如 `utils/rep_draw.py`：tabloid、置換矩陣、群環元素的條列），由主對話先寫好再交給代理人。
- 自查：`combkit/tools/render_check.py`；整合：`main.py` 加 `FULTON4_SCENES`、`FultonDemo4`，`render_all.py` 加 `--fulton4`、`--fulton4-demo`；之後 combkit 升 1.3.0。

## 4. 待決定（開工前）
- F37 的 Plücker 部分偏幾何，若想把第 8 章留到之後再做，可以只做 F28–F33（第 7 章）。
- 是否另做講義（併入 `young_tableaux_導讀.tex` 第 7–8 節）。
