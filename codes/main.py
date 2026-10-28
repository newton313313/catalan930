"""
main.py —— 所有場景的總入口

在 codes/ 資料夾內執行：

    manimgl main.py                              列出所有場景，輸入編號或名稱選擇
    manimgl main.py Scene00cTriangulationRecurrence   直接播放某一個場景
    manimgl main.py CatalanIntroDemo             卡塔蘭基礎模組（00a–00m）連續播放
    manimgl main.py FullDemo                     Chu 的部分（01–09）連續播放
    manimgl main.py CompleteDemo                 卡塔蘭基礎模組 + Chu（03–09）完整版
    manimgl main.py MITDemo                      MIT 18.212 L1–4 補充（M01–M14）連續播放
    manimgl main.py MITCompleteDemo              00a–00k + M01–M14 + 00l、00m + Chu（03–09）
    manimgl main.py FultonDemo                   Fulton《Young Tableaux》第 1 章（F01–F08），獨立
    manimgl main.py FultonDemo2                  Fulton 第 2–4 章（F09–F19），獨立
    manimgl main.py FultonDemo3                  Fulton 第 5–6 章（F20–F27），獨立
    manimgl main.py FultonDemo4                  Fulton 第 7 章（F28–F41），獨立
    manimgl main.py FultonDemo5                  Fulton 第 8 章（F42–F45），獨立
    manimgl main.py FultonDemo6                  Fulton 第 9–10 章（F46–F55），獨立
    manimgl main.py FultonDemo7                  Fulton 附錄 A–B 與全書回顧（F56–F65），獨立
    manimgl main.py RaneyLemmaDemo               Raney 引理筆記（R01–R06），獨立
    manimgl main.py RaneyPaperDemo               Raney (1960) 導讀（N01–N12），獨立
    manimgl main.py RaneyLadderDemo              從卡塔蘭到 Chu 的對照（N13–N16），獨立
    manimgl main.py CompleteDemo -w --hd         把完整版輸出成一支 1080p 影片

每個場景也可以從它自己的檔案單獨執行，例如：
    manimgl scenes/scene00a_catalan_definition.py Scene00aCatalanDefinition
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manimlib import *

from scenes import scene00a_catalan_definition as s00a
from scenes import scene00b_triangulation as s00b
from scenes import scene00c_triangulation_recurrence as s00c
from scenes import scene00d_parenthesization as s00d
from scenes import scene00e_binary_trees as s00e
from scenes import scene00f_lattice_paths as s00f
from scenes import scene00g_dyck_paths as s00g
from scenes import scene00h_balanced_parentheses as s00h
from scenes import scene00i_ballot as s00i
from scenes import scene00j_noncrossing_matchings as s00j
from scenes import scene00k_one_number_many_objects as s00k
from scenes import scene00l_catalan_generating_function as s00l
from scenes import scene00m_bridge_to_chu as s00m
from scenes import scene01_classical_catalan as s01
from scenes import scene02_from_pairs_to_blocks as s02
from scenes import scene03_generalized_setup as s03
from scenes import scene04_paper_example as s04
from scenes import scene05_root_decomposition as s05
from scenes import scene06_recurrence as s06
from scenes import scene07_generating_function as s07
from scenes import scene08_formula_verification as s08
from scenes import scene09_summary as s09
from scenes import sceneM01_cauchy_product as sM01
from scenes import sceneM02_closed_form as sM02
from scenes import sceneM03_drunkards_walk as sM03
from scenes import sceneM04_cyclic_shift as sM04
from scenes import sceneM05_plane_trees as sM05
from scenes import sceneM06_arc_diagrams as sM06
from scenes import sceneM07_triangulation_dual_tree as sM07
from scenes import sceneM08_tree_dyck_matching as sM08
from scenes import sceneM09_stack_queue_sorting as sM09
from scenes import sceneM10_pattern_avoidance as sM10
from scenes import sceneM11_partitions_young as sM11
from scenes import sceneM12_syt_dyck as sM12
from scenes import sceneM13_hook_length as sM13
from scenes import sceneM14_hook_walk as sM14
from scenes import sceneF01_young_diagrams as sF01
from scenes import sceneF02_tableaux as sF02
from scenes import sceneF03_schur as sF03
from scenes import sceneF04_row_insertion as sF04
from scenes import sceneF05_bumping_lemma as sF05
from scenes import sceneF06_product as sF06
from scenes import sceneF07_jeu_de_taquin as sF07
from scenes import sceneF08_rectify_product as sF08
from scenes import sceneF09_words_knuth as sF09
from scenes import sceneF10_slides_theorem as sF10
from scenes import sceneF11_pieri as sF11
from scenes import sceneF12_kostka as sF12
from scenes import sceneF13_column_words as sF13
from scenes import sceneF14_increasing as sF14
from scenes import sceneF15_uniqueness as sF15
from scenes import sceneF16_rs_correspondence as sF16
from scenes import sceneF17_rsk_arrays as sF17
from scenes import sceneF18_matrix_ball as sF18
from scenes import sceneF19_rsk_applications as sF19
from scenes import sceneF20_factor_tableaux as sF20
from scenes import sceneF21_lr_symmetry as sF21
from scenes import sceneF22_yamanouchi as sF22
from scenes import sceneF23_lr_rule as sF23
from scenes import sceneF24_lr_other as sF24
from scenes import sceneF25_bases as sF25
from scenes import sceneF26_jacobi_trudi as sF26
from scenes import sceneF27_symmetric_functions as sF27
from scenes import sceneF28_six_shuffles as sF28
from scenes import sceneF29_rows_columns as sF29
from scenes import sceneF30_collision as sF30
from scenes import sceneF31_tabloids_plane as sF31
from scenes import sceneF32_irreducible_basis as sF32
from scenes import sceneF33_matrices_characters as sF33
from scenes import sceneF34_young_rule as sF34
from scenes import sceneF35_induction_dictionary as sF35
from scenes import sceneF36_frobenius as sF36
from scenes import sceneF37_branching_sign as sF37
from scenes import sceneF38_column_tabloids as sF38
from scenes import sceneF39_straightening as sF39
from scenes import sceneF40_symmetrizer_mod3 as sF40
from scenes import sceneF41_four_views as sF41
from scenes import sceneF42_schur_module as sF42
from scenes import sceneF43_weights as sF43
from scenes import sceneF44_schur_weyl as sF44
from scenes import sceneF45_quadratic_relations as sF45
from scenes import sceneF46_plucker as sF46
from scenes import sceneF47_flag_ring as sF47
from scenes import sceneF48_grass_cells as sF48
from scenes import sceneF49_four_lines as sF49
from scenes import sceneF50_flag_cells as sF50
from scenes import sceneF51_divided_differences as sF51
from scenes import sceneF52_schubert_polys as sF52
from scenes import sceneF53_pipe_dreams as sF53
from scenes import sceneF54_bruhat as sF54
from scenes import sceneF55_grassmannian_schur as sF55
from scenes import sceneF56_evacuation as sF56
from scenes import sceneF57_column_bumping as sF57
from scenes import sceneF58_burge as sF58
from scenes import sceneF59_four_corners as sF59
from scenes import sceneF60_zero_one as sF60
from scenes import sceneF61_keys as sF61
from scenes import sceneF62_cells_homology as sF62
from scenes import sceneF63_classes_degrees as sF63
from scenes import sceneF64_chern_classes as sF64
from scenes import sceneF65_book_map as sF65
from scenes import sceneR01_raney_lemma as sR01
from scenes import sceneR02_last_minimum as sR02
from scenes import sceneR03_positive_counts as sR03
from scenes import sceneR04_stack_catalan as sR04
from scenes import sceneR05_card_game as sR05
from scenes import sceneR06_summary as sR06
from scenes import sceneN01_prefix_words as sN01
from scenes import sceneN02_rank_counter as sN02
from scenes import sceneN03_three_readings as sN03
from scenes import sceneN04_raney_proof as sN04
from scenes import sceneN05_double_counting as sN05
from scenes import sceneN06_random_examples as sN06
from scenes import sceneN07_split_first as sN07
from scenes import sceneN08_lstar as sN08
from scenes import sceneN09_lagrange as sN09
from scenes import sceneN10_trinomial as sN10
from scenes import sceneN11_convolution as sN11
from scenes import sceneN12_summary as sN12
from scenes import sceneN13_catalan_words as sN13
from scenes import sceneN14_chu_groups as sN14
from scenes import sceneN15_ladder as sN15
from scenes import sceneN16_walk_sums as sN16


# ManimGL 只會列出「定義在這個檔案裡」的場景，所以這裡各做一個同名的子類別。
# ------------------------------------------------------------ 卡塔蘭基礎模組
class Scene00aCatalanDefinition(s00a.Scene00aCatalanDefinition):
    pass


class Scene00bTriangulation(s00b.Scene00bTriangulation):
    pass


class Scene00cTriangulationRecurrence(s00c.Scene00cTriangulationRecurrence):
    pass


class Scene00dParenthesization(s00d.Scene00dParenthesization):
    pass


class Scene00eBinaryTrees(s00e.Scene00eBinaryTrees):
    pass


class Scene00fLatticePaths(s00f.Scene00fLatticePaths):
    pass


class Scene00gDyckPaths(s00g.Scene00gDyckPaths):
    pass


class Scene00hBalancedParentheses(s00h.Scene00hBalancedParentheses):
    pass


class Scene00iBallot(s00i.Scene00iBallot):
    pass


class Scene00jNoncrossingMatchings(s00j.Scene00jNoncrossingMatchings):
    pass


class Scene00kOneNumberManyObjects(s00k.Scene00kOneNumberManyObjects):
    pass


class Scene00lCatalanGeneratingFunction(s00l.Scene00lCatalanGeneratingFunction):
    pass


class Scene00mBridgeToChu(s00m.Scene00mBridgeToChu):
    pass


# ------------------------------------------------------------ Chu (1987)
class Scene01ClassicalCatalan(s01.Scene01ClassicalCatalan):
    pass


class Scene02FromPairsToBlocks(s02.Scene02FromPairsToBlocks):
    pass


class Scene03GeneralizedSetup(s03.Scene03GeneralizedSetup):
    pass


class Scene04PaperExample(s04.Scene04PaperExample):
    pass


class Scene05RootDecomposition(s05.Scene05RootDecomposition):
    pass


class Scene06Recurrence(s06.Scene06Recurrence):
    pass


class Scene07GeneratingFunction(s07.Scene07GeneratingFunction):
    pass


class Scene08FormulaVerification(s08.Scene08FormulaVerification):
    pass


class Scene08RaneyProof(s08.Scene08RaneyProof):
    """第八個場景中，只有 Raney 公式證明的部分（第 1–5 段）。"""
    pass


class Scene09Summary(s09.Scene09Summary):
    pass


# ------------------------------------------------------------ MIT 18.212 L1–4 補充
class SceneM01CauchyProduct(sM01.SceneM01CauchyProduct):
    pass


class SceneM02ClosedForm(sM02.SceneM02ClosedForm):
    pass


class SceneM03DrunkardsWalk(sM03.SceneM03DrunkardsWalk):
    pass


class SceneM04CyclicShift(sM04.SceneM04CyclicShift):
    pass


class SceneM05PlaneTrees(sM05.SceneM05PlaneTrees):
    pass


class SceneM06ArcDiagrams(sM06.SceneM06ArcDiagrams):
    pass


class SceneM07TriangulationDualTree(sM07.SceneM07TriangulationDualTree):
    pass


class SceneM08TreeDyckMatching(sM08.SceneM08TreeDyckMatching):
    pass


class SceneM09StackQueueSorting(sM09.SceneM09StackQueueSorting):
    pass


class SceneM10PatternAvoidance(sM10.SceneM10PatternAvoidance):
    pass


class SceneM11PartitionsYoung(sM11.SceneM11PartitionsYoung):
    pass


class SceneM12SYTDyck(sM12.SceneM12SYTDyck):
    pass


class SceneM13HookLength(sM13.SceneM13HookLength):
    pass


class SceneM14HookWalk(sM14.SceneM14HookWalk):
    pass


# ------------------------------------------------------------ Fulton《Young Tableaux》第 1 章（獨立）
class SceneF01YoungDiagrams(sF01.SceneF01YoungDiagrams):
    pass


class SceneF02Tableaux(sF02.SceneF02Tableaux):
    pass


class SceneF03Schur(sF03.SceneF03Schur):
    pass


class SceneF04RowInsertion(sF04.SceneF04RowInsertion):
    pass


class SceneF05BumpingLemma(sF05.SceneF05BumpingLemma):
    pass


class SceneF06Product(sF06.SceneF06Product):
    pass


class SceneF07JeuDeTaquin(sF07.SceneF07JeuDeTaquin):
    pass


class SceneF08RectifyProduct(sF08.SceneF08RectifyProduct):
    pass


# ------------------------------------------------------------ Fulton《Young Tableaux》第 2–4 章（獨立）
class SceneF09WordsKnuth(sF09.SceneF09WordsKnuth):
    pass


class SceneF10SlidesTheorem(sF10.SceneF10SlidesTheorem):
    pass


class SceneF11Pieri(sF11.SceneF11Pieri):
    pass


class SceneF12Kostka(sF12.SceneF12Kostka):
    pass


class SceneF13ColumnWords(sF13.SceneF13ColumnWords):
    pass


class SceneF14Increasing(sF14.SceneF14Increasing):
    pass


class SceneF15Uniqueness(sF15.SceneF15Uniqueness):
    pass


class SceneF16RS(sF16.SceneF16RS):
    pass


class SceneF17RSKArrays(sF17.SceneF17RSKArrays):
    pass


class SceneF18MatrixBall(sF18.SceneF18MatrixBall):
    pass


class SceneF19RSKApplications(sF19.SceneF19RSKApplications):
    pass


# ------------------------------------------------------------ Fulton《Young Tableaux》第 5–6 章（獨立）
class SceneF20FactorTableaux(sF20.SceneF20FactorTableaux):
    pass


class SceneF21LRSymmetry(sF21.SceneF21LRSymmetry):
    pass


class SceneF22Yamanouchi(sF22.SceneF22Yamanouchi):
    pass


class SceneF23LRRule(sF23.SceneF23LRRule):
    pass


class SceneF24LROther(sF24.SceneF24LROther):
    pass


class SceneF25Bases(sF25.SceneF25Bases):
    pass


class SceneF26JacobiTrudi(sF26.SceneF26JacobiTrudi):
    pass


class SceneF27SymFunctions(sF27.SceneF27SymFunctions):
    pass


# ------------------------------------------------------------ Fulton《Young Tableaux》第 7 章（獨立）
class SceneF28SixShuffles(sF28.SceneF28SixShuffles):
    pass


class SceneF29RowsColumns(sF29.SceneF29RowsColumns):
    pass


class SceneF30Collision(sF30.SceneF30Collision):
    pass


class SceneF31TabloidsPlane(sF31.SceneF31TabloidsPlane):
    pass


class SceneF32IrreducibleBasis(sF32.SceneF32IrreducibleBasis):
    pass


class SceneF33MatricesCharacters(sF33.SceneF33MatricesCharacters):
    pass


class SceneF34YoungRule(sF34.SceneF34YoungRule):
    pass


class SceneF35InductionDictionary(sF35.SceneF35InductionDictionary):
    pass


class SceneF36Frobenius(sF36.SceneF36Frobenius):
    pass


class SceneF37BranchingSign(sF37.SceneF37BranchingSign):
    pass


class SceneF38ColumnTabloids(sF38.SceneF38ColumnTabloids):
    pass


class SceneF39Straightening(sF39.SceneF39Straightening):
    pass


class SceneF40SymmetrizerMod3(sF40.SceneF40SymmetrizerMod3):
    pass


class SceneF41FourViews(sF41.SceneF41FourViews):
    pass


# ------------------------------------------------------------ Fulton《Young Tableaux》第 8 章（獨立）
class SceneF42SchurModule(sF42.SceneF42SchurModule):
    pass


class SceneF43Weights(sF43.SceneF43Weights):
    pass


class SceneF44SchurWeyl(sF44.SceneF44SchurWeyl):
    pass


class SceneF45QuadraticRelations(sF45.SceneF45QuadraticRelations):
    pass


# ------------------------------------------------------------ Fulton《Young Tableaux》第 9–10 章（獨立）

class SceneF46Plucker(sF46.SceneF46Plucker):
    pass


class SceneF47FlagRing(sF47.SceneF47FlagRing):
    pass


class SceneF48GrassCells(sF48.SceneF48GrassCells):
    pass


class SceneF49FourLines(sF49.SceneF49FourLines):
    pass


class SceneF50FlagCells(sF50.SceneF50FlagCells):
    pass


class SceneF51DividedDifferences(sF51.SceneF51DividedDifferences):
    pass


class SceneF52SchubertPolys(sF52.SceneF52SchubertPolys):
    pass


class SceneF53PipeDreams(sF53.SceneF53PipeDreams):
    pass


class SceneF54Bruhat(sF54.SceneF54Bruhat):
    pass


class SceneF55GrassmannianSchur(sF55.SceneF55GrassmannianSchur):
    pass


# ------------------------------------------------------------ Fulton《Young Tableaux》附錄 A–B 與全書回顧（獨立）

class SceneF56Evacuation(sF56.SceneF56Evacuation):
    pass


class SceneF57ColumnBumping(sF57.SceneF57ColumnBumping):
    pass


class SceneF58Burge(sF58.SceneF58Burge):
    pass


class SceneF59FourCorners(sF59.SceneF59FourCorners):
    pass


class SceneF60ZeroOne(sF60.SceneF60ZeroOne):
    pass


class SceneF61Keys(sF61.SceneF61Keys):
    pass


class SceneF62CellsHomology(sF62.SceneF62CellsHomology):
    pass


class SceneF63ClassesDegrees(sF63.SceneF63ClassesDegrees):
    pass


class SceneF64ChernClasses(sF64.SceneF64ChernClasses):
    pass


class SceneF65BookMap(sF65.SceneF65BookMap):
    pass


# ------------------------------------------------------------ Raney 引理筆記（R01–R06）

class SceneR01RaneyLemma(sR01.SceneR01RaneyLemma):
    pass


class SceneR02LastMinimum(sR02.SceneR02LastMinimum):
    pass


class SceneR03PositiveCounts(sR03.SceneR03PositiveCounts):
    pass


class SceneR04StackCatalan(sR04.SceneR04StackCatalan):
    pass


class SceneR05CardGame(sR05.SceneR05CardGame):
    pass


class SceneR06Summary(sR06.SceneR06Summary):
    pass


# ------------------------------------------------------------ Raney (1960) 導讀（N01–N12）

class SceneN01PrefixWords(sN01.SceneN01PrefixWords):
    pass


class SceneN02RankCounter(sN02.SceneN02RankCounter):
    pass


class SceneN03ThreeReadings(sN03.SceneN03ThreeReadings):
    pass


class SceneN04RaneyProof(sN04.SceneN04RaneyProof):
    pass


class SceneN05DoubleCounting(sN05.SceneN05DoubleCounting):
    pass


class SceneN06RandomExamples(sN06.SceneN06RandomExamples):
    pass


class SceneN07SplitFirst(sN07.SceneN07SplitFirst):
    pass


class SceneN08LStar(sN08.SceneN08LStar):
    pass


class SceneN09Lagrange(sN09.SceneN09Lagrange):
    pass


class SceneN10Trinomial(sN10.SceneN10Trinomial):
    pass


class SceneN11Convolution(sN11.SceneN11Convolution):
    pass


class SceneN12Summary(sN12.SceneN12Summary):
    pass


class SceneN13CatalanWords(sN13.SceneN13CatalanWords):
    pass


class SceneN14ChuGroups(sN14.SceneN14ChuGroups):
    pass


class SceneN15Ladder(sN15.SceneN15Ladder):
    pass


class SceneN16WalkSums(sN16.SceneN16WalkSums):
    pass


INTRO_SCENES = [
    s00a.Scene00aCatalanDefinition,
    s00b.Scene00bTriangulation,
    s00c.Scene00cTriangulationRecurrence,
    s00d.Scene00dParenthesization,
    s00e.Scene00eBinaryTrees,
    s00f.Scene00fLatticePaths,
    s00g.Scene00gDyckPaths,
    s00h.Scene00hBalancedParentheses,
    s00i.Scene00iBallot,
    s00j.Scene00jNoncrossingMatchings,
    s00k.Scene00kOneNumberManyObjects,
    s00l.Scene00lCatalanGeneratingFunction,
    s00m.Scene00mBridgeToChu,
]

ALL_SCENES = [                      # Chu 的部分（原本的九個場景）
    s01.Scene01ClassicalCatalan,
    s02.Scene02FromPairsToBlocks,
    s03.Scene03GeneralizedSetup,
    s04.Scene04PaperExample,
    s05.Scene05RootDecomposition,
    s06.Scene06Recurrence,
    s07.Scene07GeneratingFunction,
    s08.Scene08FormulaVerification,
    s09.Scene09Summary,
]

# 完整版：卡塔蘭模組之後直接接 Scene03。
# Scene01（經典卡塔蘭與配對）已由 00a、00j 取代；Scene02（從弦到多邊形、兩個向量）已由 00m 取代。
COMPLETE_SCENES = INTRO_SCENES + ALL_SCENES[2:]

MIT_SCENES = [                      # MIT 18.212 Lecture 1–4 補充（notes/mit_plan.md）
    sM01.SceneM01CauchyProduct,
    sM02.SceneM02ClosedForm,
    sM03.SceneM03DrunkardsWalk,
    sM04.SceneM04CyclicShift,
    sM05.SceneM05PlaneTrees,
    sM06.SceneM06ArcDiagrams,
    sM07.SceneM07TriangulationDualTree,
    sM08.SceneM08TreeDyckMatching,
    sM09.SceneM09StackQueueSorting,
    sM10.SceneM10PatternAvoidance,
    sM11.SceneM11PartitionsYoung,
    sM12.SceneM12SYTDyck,
    sM13.SceneM13HookLength,
    sM14.SceneM14HookWalk,
]

# MIT 完整版：卡塔蘭模組 00a–00k → MIT 補充 → 00l（C=1+xC² 的根＋左＋右讀法，並提問「一組不只 2 點呢？」）
# → 00m（接到 Chu）→ Chu 的 03–09。
MIT_COMPLETE_SCENES = INTRO_SCENES[:11] + MIT_SCENES + INTRO_SCENES[11:] + ALL_SCENES[2:]

FULTON_SCENES = [                   # Fulton《Young Tableaux》Notation 與第 1 章（notes/fulton_plan.md），獨立播放
    sF01.SceneF01YoungDiagrams,
    sF02.SceneF02Tableaux,
    sF03.SceneF03Schur,
    sF04.SceneF04RowInsertion,
    sF05.SceneF05BumpingLemma,
    sF06.SceneF06Product,
    sF07.SceneF07JeuDeTaquin,
    sF08.SceneF08RectifyProduct,
]

FULTON2_SCENES = [                  # Fulton 第 2–4 章（notes/fulton_plan_ch2-4.md），獨立播放
    sF09.SceneF09WordsKnuth,
    sF10.SceneF10SlidesTheorem,
    sF11.SceneF11Pieri,
    sF12.SceneF12Kostka,
    sF13.SceneF13ColumnWords,
    sF14.SceneF14Increasing,
    sF15.SceneF15Uniqueness,
    sF16.SceneF16RS,
    sF17.SceneF17RSKArrays,
    sF18.SceneF18MatrixBall,
    sF19.SceneF19RSKApplications,
]

FULTON3_SCENES = [                  # Fulton 第 5–6 章（notes/fulton_plan_ch5-6.md），獨立播放
    sF20.SceneF20FactorTableaux,
    sF21.SceneF21LRSymmetry,
    sF22.SceneF22Yamanouchi,
    sF23.SceneF23LRRule,
    sF24.SceneF24LROther,
    sF25.SceneF25Bases,
    sF26.SceneF26JacobiTrudi,
    sF27.SceneF27SymFunctions,
]

FULTON4_SCENES = [                  # Fulton 第 7 章（notes/fulton_plan_ch7.md），獨立播放
    sF28.SceneF28SixShuffles,
    sF29.SceneF29RowsColumns,
    sF30.SceneF30Collision,
    sF31.SceneF31TabloidsPlane,
    sF32.SceneF32IrreducibleBasis,
    sF33.SceneF33MatricesCharacters,
    sF34.SceneF34YoungRule,
    sF35.SceneF35InductionDictionary,
    sF36.SceneF36Frobenius,
    sF37.SceneF37BranchingSign,
    sF38.SceneF38ColumnTabloids,
    sF39.SceneF39Straightening,
    sF40.SceneF40SymmetrizerMod3,
    sF41.SceneF41FourViews,
]

FULTON5_SCENES = [                  # Fulton 第 8 章（notes/fulton_plan_ch8.md），獨立播放
    sF42.SceneF42SchurModule,
    sF43.SceneF43Weights,
    sF44.SceneF44SchurWeyl,
    sF45.SceneF45QuadraticRelations,
]

FULTON6_SCENES = [                  # Fulton 第 9–10 章（notes/fulton_plan_ch9-10.md），獨立播放
    sF46.SceneF46Plucker,
    sF47.SceneF47FlagRing,
    sF48.SceneF48GrassCells,
    sF49.SceneF49FourLines,
    sF50.SceneF50FlagCells,
    sF51.SceneF51DividedDifferences,
    sF52.SceneF52SchubertPolys,
    sF53.SceneF53PipeDreams,
    sF54.SceneF54Bruhat,
    sF55.SceneF55GrassmannianSchur,
]

FULTON7_SCENES = [                  # Fulton 附錄 A–B（notes/fulton_plan_appAB.md），獨立播放
    sF56.SceneF56Evacuation,
    sF57.SceneF57ColumnBumping,
    sF58.SceneF58Burge,
    sF59.SceneF59FourCorners,
    sF60.SceneF60ZeroOne,
    sF61.SceneF61Keys,
    sF62.SceneF62CellsHomology,
    sF63.SceneF63ClassesDegrees,
    sF64.SceneF64ChernClasses,
    sF65.SceneF65BookMap,
]

RANEY_SCENES = [                    # Raney 引理筆記（notes/ran_note015_改寫.pdf），獨立播放
    sR01.SceneR01RaneyLemma,
    sR02.SceneR02LastMinimum,
    sR03.SceneR03PositiveCounts,
    sR04.SceneR04StackCatalan,
    sR05.SceneR05CardGame,
    sR06.SceneR06Summary,
]

RANEY_PAPER_SCENES = [              # Raney (1960) 導讀（notes/raney1960_導讀.pdf），獨立播放
    sN01.SceneN01PrefixWords,
    sN02.SceneN02RankCounter,
    sN03.SceneN03ThreeReadings,
    sN04.SceneN04RaneyProof,
    sN05.SceneN05DoubleCounting,
    sN06.SceneN06RandomExamples,
    sN07.SceneN07SplitFirst,
    sN08.SceneN08LStar,
    sN09.SceneN09Lagrange,
    sN10.SceneN10Trinomial,
    sN11.SceneN11Convolution,
    sN12.SceneN12Summary,
]

RANEY_LADDER_SCENES = [             # 從卡塔蘭到 Chu（Raney 導讀第 2.4 小節），獨立播放
    sN13.SceneN13CatalanWords,
    sN14.SceneN14ChuGroups,
    sN15.SceneN15Ladder,
    sN16.SceneN16WalkSums,
]


def play_sequence(scene, classes):
    """依序播放多個場景；場景之間把畫面清空、鏡頭歸位。"""
    for k, scene_class in enumerate(classes):
        scene_class.construct(scene)
        if k < len(classes) - 1:
            scene.fade_all(run_time=0.8)
            scene.frame.to_default_state()
            scene.wait(0.4)


# 連續播放的場景都繼承 Scene08，是為了用到它拆出來的各段方法（part0_roadmap 等）；
# 其他場景只有 construct，直接借用即可。新增場景時，輔助函式請寫成模組層級的函式。
class FullDemo(s08.Scene08FormulaVerification):
    """Chu 的部分：九個場景（01–09）連續播放。"""

    def construct(self):
        play_sequence(self, ALL_SCENES)


class CatalanIntroDemo(s08.Scene08FormulaVerification):
    """卡塔蘭基礎模組：十三個場景（00a–00m）連續播放。"""

    def construct(self):
        play_sequence(self, INTRO_SCENES)


class CompleteDemo(s08.Scene08FormulaVerification):
    """完整版：卡塔蘭基礎模組（00a–00m）＋ Chu（03–09）。"""

    def construct(self):
        play_sequence(self, COMPLETE_SCENES)


class MITDemo(s08.Scene08FormulaVerification):
    """MIT 18.212 Lecture 1–4 補充：十四個場景（M01–M14）連續播放。"""

    def construct(self):
        play_sequence(self, MIT_SCENES)


class MITCompleteDemo(s08.Scene08FormulaVerification):
    """MIT 完整版：00a–00k ＋ M01–M14 ＋ 00l、00m ＋ Chu（03–09）。"""

    def construct(self):
        play_sequence(self, MIT_COMPLETE_SCENES)


class FultonDemo(s08.Scene08FormulaVerification):
    """Fulton《Young Tableaux》Notation 與第 1 章：八個場景（F01–F08）連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, FULTON_SCENES)


class FultonDemo2(s08.Scene08FormulaVerification):
    """Fulton《Young Tableaux》第 2–4 章（字與 Knuth 等價、遞增子序列、R-S-K）：F09–F19 連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, FULTON2_SCENES)


class FultonDemo3(s08.Scene08FormulaVerification):
    """Fulton《Young Tableaux》第 5–6 章（Littlewood–Richardson 規則、對稱函數）：F20–F27 連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, FULTON3_SCENES)


class FultonDemo4(s08.Scene08FormulaVerification):
    """Fulton《Young Tableaux》第 7 章（對稱群的表示）：F28–F41 連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, FULTON4_SCENES)


class FultonDemo5(s08.Scene08FormulaVerification):
    """Fulton《Young Tableaux》第 8 章（一般線性群的表示）：F42–F45 連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, FULTON5_SCENES)


class FultonDemo6(s08.Scene08FormulaVerification):
    """Fulton《Young Tableaux》第 9–10 章（旗流形、Schubert 簇與 Schubert 多項式）：F46–F55 連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, FULTON6_SCENES)


class FultonDemo7(s08.Scene08FormulaVerification):
    """Fulton《Young Tableaux》附錄 A（組合的變形）、附錄 B（拓撲）與全書回顧：F56–F65 連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, FULTON7_SCENES)


class RaneyLemmaDemo(s08.Scene08FormulaVerification):
    """Raney 引理筆記（ran_note015 的勘誤與改寫）：R01–R06 連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, RANEY_SCENES)


class RaneyPaperDemo(s08.Scene08FormulaVerification):
    """Raney (1960) 論文導讀：N01–N12 連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, RANEY_PAPER_SCENES)


class RaneyLadderDemo(s08.Scene08FormulaVerification):
    """從卡塔蘭到 Chu：只有 2 和 0 的字、圓周群組、推廣階梯、走路的部分和（N13–N16）連續播放，不接其他影片。"""

    def construct(self):
        play_sequence(self, RANEY_LADDER_SCENES)
