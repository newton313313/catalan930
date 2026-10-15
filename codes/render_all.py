"""
render_all.py —— 一次把場景輸出成影片（存到 renders/）

在 codes/ 資料夾內執行：

    python render_all.py                全部場景（00a–00m、Chu 01–09、08r、MIT M01–M14、Fulton F01–F55、Raney R01–R06、N01–N12），1080p
    python render_all.py --intro        只輸出卡塔蘭模組（00a–00m）
    python render_all.py --chu          只輸出 Chu 的部分（01–09 與 08r）
    python render_all.py --mit          只輸出 MIT 18.212 L1–4 補充（M01–M14）
    python render_all.py --fulton       只輸出 Fulton《Young Tableaux》第 1 章（F01–F08）
    python render_all.py --fulton2      只輸出 Fulton 第 2–4 章（F09–F19）
    python render_all.py --fulton3      只輸出 Fulton 第 5–6 章（F20–F27）
    python render_all.py --fulton4      只輸出 Fulton 第 7 章（F28–F41）
    python render_all.py --fulton5      只輸出 Fulton 第 8 章（F42–F45）
    python render_all.py --fulton6      只輸出 Fulton 第 9–10 章（F46–F55）
    python render_all.py --raney        只輸出 Raney 引理筆記（R01–R06）
    python render_all.py --raney-paper  只輸出 Raney (1960) 導讀（N01–N12）
    python render_all.py 00c 05 M03     只輸出指定的場景（代號見下表；"5" 也可以，等於 "05"）
    python render_all.py -l             改用低畫質 480p（最快，用來預覽）；另有 -m（720p）、--uhd（4K）

    連續播放的完整影片（可以和上面一起用）：
    python render_all.py --intro-demo   CatalanIntroDemo：卡塔蘭模組連續播放
    python render_all.py --full         FullDemo：Chu 的部分連續播放
    python render_all.py --complete     CompleteDemo：卡塔蘭模組 + Chu 的完整版
    python render_all.py --mit-demo     MITDemo：MIT 補充 M01–M14 連續播放
    python render_all.py --mit-complete MITCompleteDemo：00a–00k + M01–M14 + 00l、00m + Chu 03–09
    python render_all.py --fulton-demo  FultonDemo：F01–F08 連續播放（獨立）
    python render_all.py --fulton2-demo FultonDemo2：F09–F19 連續播放（獨立）
    python render_all.py --fulton3-demo FultonDemo3：F20–F27 連續播放（獨立）
    python render_all.py --fulton4-demo FultonDemo4：F28–F41 連續播放（獨立）
    python render_all.py --fulton5-demo FultonDemo5：F42–F45 連續播放（獨立）
    python render_all.py --fulton6-demo FultonDemo6：F46–F55 連續播放（獨立）
    python render_all.py --raney-demo   RaneyLemmaDemo：R01–R06 連續播放（獨立）
    python render_all.py --raney-paper-demo  RaneyPaperDemo：N01–N12 連續播放（獨立）
    只要連續播放的影片、不要單一場景時，加 --demos-only。
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

INTRO = [
    ("00a", "scenes/scene00a_catalan_definition.py", "Scene00aCatalanDefinition"),
    ("00b", "scenes/scene00b_triangulation.py", "Scene00bTriangulation"),
    ("00c", "scenes/scene00c_triangulation_recurrence.py", "Scene00cTriangulationRecurrence"),
    ("00d", "scenes/scene00d_parenthesization.py", "Scene00dParenthesization"),
    ("00e", "scenes/scene00e_binary_trees.py", "Scene00eBinaryTrees"),
    ("00f", "scenes/scene00f_lattice_paths.py", "Scene00fLatticePaths"),
    ("00g", "scenes/scene00g_dyck_paths.py", "Scene00gDyckPaths"),
    ("00h", "scenes/scene00h_balanced_parentheses.py", "Scene00hBalancedParentheses"),
    ("00i", "scenes/scene00i_ballot.py", "Scene00iBallot"),
    ("00j", "scenes/scene00j_noncrossing_matchings.py", "Scene00jNoncrossingMatchings"),
    ("00k", "scenes/scene00k_one_number_many_objects.py", "Scene00kOneNumberManyObjects"),
    ("00l", "scenes/scene00l_catalan_generating_function.py", "Scene00lCatalanGeneratingFunction"),
    ("00m", "scenes/scene00m_bridge_to_chu.py", "Scene00mBridgeToChu"),
]
CHU = [
    ("01", "scenes/scene01_classical_catalan.py", "Scene01ClassicalCatalan"),
    ("02", "scenes/scene02_from_pairs_to_blocks.py", "Scene02FromPairsToBlocks"),
    ("03", "scenes/scene03_generalized_setup.py", "Scene03GeneralizedSetup"),
    ("04", "scenes/scene04_paper_example.py", "Scene04PaperExample"),
    ("05", "scenes/scene05_root_decomposition.py", "Scene05RootDecomposition"),
    ("06", "scenes/scene06_recurrence.py", "Scene06Recurrence"),
    ("07", "scenes/scene07_generating_function.py", "Scene07GeneratingFunction"),
    ("08", "scenes/scene08_formula_verification.py", "Scene08FormulaVerification"),
    ("09", "scenes/scene09_summary.py", "Scene09Summary"),
    ("08r", "scenes/scene08_formula_verification.py", "Scene08RaneyProof"),   # 只有 Raney 證明
]
MIT = [
    ("M01", "scenes/sceneM01_cauchy_product.py", "SceneM01CauchyProduct"),
    ("M02", "scenes/sceneM02_closed_form.py", "SceneM02ClosedForm"),
    ("M03", "scenes/sceneM03_drunkards_walk.py", "SceneM03DrunkardsWalk"),
    ("M04", "scenes/sceneM04_cyclic_shift.py", "SceneM04CyclicShift"),
    ("M05", "scenes/sceneM05_plane_trees.py", "SceneM05PlaneTrees"),
    ("M06", "scenes/sceneM06_arc_diagrams.py", "SceneM06ArcDiagrams"),
    ("M07", "scenes/sceneM07_triangulation_dual_tree.py", "SceneM07TriangulationDualTree"),
    ("M08", "scenes/sceneM08_tree_dyck_matching.py", "SceneM08TreeDyckMatching"),
    ("M09", "scenes/sceneM09_stack_queue_sorting.py", "SceneM09StackQueueSorting"),
    ("M10", "scenes/sceneM10_pattern_avoidance.py", "SceneM10PatternAvoidance"),
    ("M11", "scenes/sceneM11_partitions_young.py", "SceneM11PartitionsYoung"),
    ("M12", "scenes/sceneM12_syt_dyck.py", "SceneM12SYTDyck"),
    ("M13", "scenes/sceneM13_hook_length.py", "SceneM13HookLength"),
    ("M14", "scenes/sceneM14_hook_walk.py", "SceneM14HookWalk"),
]
FULTON = [
    ("F01", "scenes/sceneF01_young_diagrams.py", "SceneF01YoungDiagrams"),
    ("F02", "scenes/sceneF02_tableaux.py", "SceneF02Tableaux"),
    ("F03", "scenes/sceneF03_schur.py", "SceneF03Schur"),
    ("F04", "scenes/sceneF04_row_insertion.py", "SceneF04RowInsertion"),
    ("F05", "scenes/sceneF05_bumping_lemma.py", "SceneF05BumpingLemma"),
    ("F06", "scenes/sceneF06_product.py", "SceneF06Product"),
    ("F07", "scenes/sceneF07_jeu_de_taquin.py", "SceneF07JeuDeTaquin"),
    ("F08", "scenes/sceneF08_rectify_product.py", "SceneF08RectifyProduct"),
]
FULTON2 = [                          # 第 2–4 章（notes/fulton_plan_ch2-4.md）
    ("F09", "scenes/sceneF09_words_knuth.py", "SceneF09WordsKnuth"),
    ("F10", "scenes/sceneF10_slides_theorem.py", "SceneF10SlidesTheorem"),
    ("F11", "scenes/sceneF11_pieri.py", "SceneF11Pieri"),
    ("F12", "scenes/sceneF12_kostka.py", "SceneF12Kostka"),
    ("F13", "scenes/sceneF13_column_words.py", "SceneF13ColumnWords"),
    ("F14", "scenes/sceneF14_increasing.py", "SceneF14Increasing"),
    ("F15", "scenes/sceneF15_uniqueness.py", "SceneF15Uniqueness"),
    ("F16", "scenes/sceneF16_rs_correspondence.py", "SceneF16RS"),
    ("F17", "scenes/sceneF17_rsk_arrays.py", "SceneF17RSKArrays"),
    ("F18", "scenes/sceneF18_matrix_ball.py", "SceneF18MatrixBall"),
    ("F19", "scenes/sceneF19_rsk_applications.py", "SceneF19RSKApplications"),
]
FULTON3 = [                          # 第 5–6 章（notes/fulton_plan_ch5-6.md）
    ("F20", "scenes/sceneF20_factor_tableaux.py", "SceneF20FactorTableaux"),
    ("F21", "scenes/sceneF21_lr_symmetry.py", "SceneF21LRSymmetry"),
    ("F22", "scenes/sceneF22_yamanouchi.py", "SceneF22Yamanouchi"),
    ("F23", "scenes/sceneF23_lr_rule.py", "SceneF23LRRule"),
    ("F24", "scenes/sceneF24_lr_other.py", "SceneF24LROther"),
    ("F25", "scenes/sceneF25_bases.py", "SceneF25Bases"),
    ("F26", "scenes/sceneF26_jacobi_trudi.py", "SceneF26JacobiTrudi"),
    ("F27", "scenes/sceneF27_symmetric_functions.py", "SceneF27SymFunctions"),
]
FULTON4 = [                          # 第 7 章（notes/fulton_plan_ch7.md）
    ("F28", "scenes/sceneF28_six_shuffles.py", "SceneF28SixShuffles"),
    ("F29", "scenes/sceneF29_rows_columns.py", "SceneF29RowsColumns"),
    ("F30", "scenes/sceneF30_collision.py", "SceneF30Collision"),
    ("F31", "scenes/sceneF31_tabloids_plane.py", "SceneF31TabloidsPlane"),
    ("F32", "scenes/sceneF32_irreducible_basis.py", "SceneF32IrreducibleBasis"),
    ("F33", "scenes/sceneF33_matrices_characters.py", "SceneF33MatricesCharacters"),
    ("F34", "scenes/sceneF34_young_rule.py", "SceneF34YoungRule"),
    ("F35", "scenes/sceneF35_induction_dictionary.py", "SceneF35InductionDictionary"),
    ("F36", "scenes/sceneF36_frobenius.py", "SceneF36Frobenius"),
    ("F37", "scenes/sceneF37_branching_sign.py", "SceneF37BranchingSign"),
    ("F38", "scenes/sceneF38_column_tabloids.py", "SceneF38ColumnTabloids"),
    ("F39", "scenes/sceneF39_straightening.py", "SceneF39Straightening"),
    ("F40", "scenes/sceneF40_symmetrizer_mod3.py", "SceneF40SymmetrizerMod3"),
    ("F41", "scenes/sceneF41_four_views.py", "SceneF41FourViews"),
]
FULTON5 = [                          # 第 8 章（notes/fulton_plan_ch8.md）
    ("F42", "scenes/sceneF42_schur_module.py", "SceneF42SchurModule"),
    ("F43", "scenes/sceneF43_weights.py", "SceneF43Weights"),
    ("F44", "scenes/sceneF44_schur_weyl.py", "SceneF44SchurWeyl"),
    ("F45", "scenes/sceneF45_quadratic_relations.py", "SceneF45QuadraticRelations"),
]
FULTON6 = [                          # 第 9–10 章（notes/fulton_plan_ch9-10.md）
    ("F46", "scenes/sceneF46_plucker.py", "SceneF46Plucker"),
    ("F47", "scenes/sceneF47_flag_ring.py", "SceneF47FlagRing"),
    ("F48", "scenes/sceneF48_grass_cells.py", "SceneF48GrassCells"),
    ("F49", "scenes/sceneF49_four_lines.py", "SceneF49FourLines"),
    ("F50", "scenes/sceneF50_flag_cells.py", "SceneF50FlagCells"),
    ("F51", "scenes/sceneF51_divided_differences.py", "SceneF51DividedDifferences"),
    ("F52", "scenes/sceneF52_schubert_polys.py", "SceneF52SchubertPolys"),
    ("F53", "scenes/sceneF53_pipe_dreams.py", "SceneF53PipeDreams"),
    ("F54", "scenes/sceneF54_bruhat.py", "SceneF54Bruhat"),
    ("F55", "scenes/sceneF55_grassmannian_schur.py", "SceneF55GrassmannianSchur"),
]
RANEY = [                            # Raney 引理筆記（notes/ran_note015_改寫.pdf）
    ("R01", "scenes/sceneR01_raney_lemma.py", "SceneR01RaneyLemma"),
    ("R02", "scenes/sceneR02_last_minimum.py", "SceneR02LastMinimum"),
    ("R03", "scenes/sceneR03_positive_counts.py", "SceneR03PositiveCounts"),
    ("R04", "scenes/sceneR04_stack_catalan.py", "SceneR04StackCatalan"),
    ("R05", "scenes/sceneR05_card_game.py", "SceneR05CardGame"),
    ("R06", "scenes/sceneR06_summary.py", "SceneR06Summary"),
]
RANEY_PAPER = [                      # Raney (1960) 導讀（notes/raney1960_導讀.pdf、notes/raney/manim_plan.md）
    ("N01", "scenes/sceneN01_prefix_words.py", "SceneN01PrefixWords"),
    ("N02", "scenes/sceneN02_rank_counter.py", "SceneN02RankCounter"),
    ("N03", "scenes/sceneN03_three_readings.py", "SceneN03ThreeReadings"),
    ("N04", "scenes/sceneN04_raney_proof.py", "SceneN04RaneyProof"),
    ("N05", "scenes/sceneN05_double_counting.py", "SceneN05DoubleCounting"),
    ("N06", "scenes/sceneN06_random_examples.py", "SceneN06RandomExamples"),
    ("N07", "scenes/sceneN07_split_first.py", "SceneN07SplitFirst"),
    ("N08", "scenes/sceneN08_lstar.py", "SceneN08LStar"),
    ("N09", "scenes/sceneN09_lagrange.py", "SceneN09Lagrange"),
    ("N10", "scenes/sceneN10_trinomial.py", "SceneN10Trinomial"),
    ("N11", "scenes/sceneN11_convolution.py", "SceneN11Convolution"),
    ("N12", "scenes/sceneN12_summary.py", "SceneN12Summary"),
]
DEMOS = {
    "--intro-demo": ("main.py", "CatalanIntroDemo"),
    "--full": ("main.py", "FullDemo"),
    "--complete": ("main.py", "CompleteDemo"),
    "--mit-demo": ("main.py", "MITDemo"),
    "--mit-complete": ("main.py", "MITCompleteDemo"),
    "--fulton-demo": ("main.py", "FultonDemo"),
    "--fulton2-demo": ("main.py", "FultonDemo2"),
    "--fulton3-demo": ("main.py", "FultonDemo3"),
    "--fulton4-demo": ("main.py", "FultonDemo4"),
    "--fulton5-demo": ("main.py", "FultonDemo5"),
    "--fulton6-demo": ("main.py", "FultonDemo6"),
    "--raney-demo": ("main.py", "RaneyLemmaDemo"),
    "--raney-paper-demo": ("main.py", "RaneyPaperDemo"),
}
QUALITY_FLAGS = {"-l", "-m", "--hd", "--uhd"}


def main(argv):
    quality = "--hd"
    groups, keys, demos = [], [], []
    demos_only = False
    by_key = {k: (f, s) for k, f, s in INTRO + CHU + MIT + FULTON + FULTON2 + FULTON3 + FULTON4 + FULTON5 + FULTON6 + RANEY + RANEY_PAPER}
    for arg in argv:
        if arg in QUALITY_FLAGS:
            quality = arg
        elif arg == "--intro":
            groups.append(INTRO)
        elif arg == "--chu":
            groups.append(CHU)
        elif arg == "--mit":
            groups.append(MIT)
        elif arg == "--fulton":
            groups.append(FULTON)
        elif arg == "--fulton2":
            groups.append(FULTON2)
        elif arg == "--fulton3":
            groups.append(FULTON3)
        elif arg == "--fulton4":
            groups.append(FULTON4)
        elif arg == "--fulton5":
            groups.append(FULTON5)
        elif arg == "--fulton6":
            groups.append(FULTON6)
        elif arg == "--raney":
            groups.append(RANEY)
        elif arg == "--raney-paper":
            groups.append(RANEY_PAPER)
        elif arg in DEMOS:
            demos.append(DEMOS[arg])
        elif arg == "--demos-only":
            demos_only = True
        elif arg in by_key:
            keys.append(arg)
        elif arg.upper() in by_key:
            keys.append(arg.upper())
        elif arg.isdigit() and f"0{arg}" in by_key:
            keys.append(f"0{arg}")
        else:
            print(f"看不懂的參數：{arg}")
            print(__doc__)
            return 2

    jobs = []
    if not demos_only:
        if keys:
            jobs += [by_key[k] for k in keys]
        if groups:
            for g in groups:
                jobs += [(f, s) for _, f, s in g]
        if not keys and not groups:
            jobs += [(f, s) for _, f, s in INTRO + CHU + MIT + FULTON + FULTON2 + FULTON3 + FULTON4 + FULTON5 + FULTON6 + RANEY + RANEY_PAPER]
    jobs += demos

    failed = []
    for file, scene in jobs:
        print(f"\n=== {scene} ({quality}) ===", flush=True)
        start = time.time()
        result = subprocess.run(["manimgl", file, scene, "-w", quality], cwd=HERE)
        out = HERE / "renders" / f"{scene}.mp4"
        if result.returncode != 0 or not out.exists():
            failed.append(scene)
            print(f"失敗：{scene}")
        else:
            print(f"完成：{out}  （{time.time() - start:.0f} 秒）")

    print("\n全部完成。" if not failed else f"\n有 {len(failed)} 個場景失敗：{failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
