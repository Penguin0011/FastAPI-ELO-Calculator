"""
Master render script — renders ALL scenes (original + part1/part2/part3 + explanatory).
Outputs to manim_elo/media/videos/ (Manim's default media_dir).

Usage:
    python render_all_scenes.py          # Low quality (fast)
    python render_all_scenes.py --hq     # High quality
"""

import subprocess
import sys
import os
import time

# All scene files with their classes
# Format: (relative_path_from_scenes_dir, [class_names])
ALL_SCENES = [
    # ===== STANDALONE (old) SCENES =====
    ("scene_01_elo_history", [
        "EloHistoryIntro", "ArpadEloIntro", "TheProblemBeforeElo",
        "EloInsight", "ChessSymmetry", "BasicEloFormula",
        "RatingUpdateFormula", "HistoryConclusion"
    ]),
    ("scene_02_facemash", [
        "FacemashIntro", "FacemashStory", "FacemashMechanism",
        "FacemashFormula", "FacemashImpact", "FacemashBroaderApplications"
    ]),
    ("scene_03_elo_math", [
        "EloMathIntro", "ExpectedScoreDerivation", "ExpectedScoreFormula",
        "SigmoidVisualization", "KFactorExplained", "RatingUpdateExample",
        "UpsetScenario", "EloMathConclusion"
    ]),
    ("scene_04_f1_paradox", [
        "F1ParadoxIntro", "ChessVsF1", "TheThoughtExperiment",
        "EloMisattribution", "RealWorldExamples", "TheRequirement"
    ]),
    ("scene_05_bayesian_primer", [
        "BayesianIntro", "FrequentistVsBayesian", "TheBayesianCycle",
        "BayesianF1Example", "NoisyExperiment", "DistributionVisualization",
        "BayesianConclusion"
    ]),
    ("scene_06_composite_strength", [
        "CompositeIntro", "TwoRatings", "CompositeFormula",
        "ModifiedProbability", "HandicapVisualization",
        "HandicapInsight", "CompositeConclusion"
    ]),
    ("scene_07_k_factor_dynamics", [
        "KFactorIntro", "TeammateIsolation", "TeammateVisualization",
        "GoldenEraMultiplier", "SeasonNormalization",
        "CombinedKFactor", "KFactorConclusion"
    ]),
    ("scene_08_physics_features", [
        "PhysicsIntro", "BrakingAggression", "CarryJobGradient"
    ]),
    ("scene_09_dnf_handling", [
        "DNFIntro", "DNFProblem", "RobberyProtocol", "StolenWinExample"
    ]),
    ("scene_10_full_system", [
        "SystemOverviewIntro", "SystemFlowchart", "FinalFormula",
        "WhatItAchieves", "Conclusion"
    ]),

    # ===== PART 1 SCENES =====
    ("part1/s00_goat_intro", [
        "Scene0_1_BasketballDebate", "Scene0_2_SoccerDebate",
        "Scene0_3_MoreDebates", "Scene0_4_TheQuestion",
        "Scene0_5_VideoTitle",
    ]),
    ("part1/s01_introduction", [
        "Scene1_1_TitleHook", "Scene1_2_LatentVariable",
        "Scene1_3_EvolutionTimeline",
    ]),
    ("part1/s02_harkness", [
        "Scene2_1_NeedForRanking", "Scene2_2_LinearMechanics",
        "Scene2_3_LosingWinnerParadox", "Scene2_4_EliteNotProtected",
        "Scene2_5_NeedForProbability",
    ]),
    ("part1/s03_elo_physics", [
        "Scene3_1_EloBackground", "Scene3_2_PerformanceRandom",
        "Scene3_3_NormalDistribution", "Scene3_4_DifferenceOfNormals",
        "Scene3_5_LogisticTransition", "Scene3_6_LogisticFormula",
        "Scene3_7_SigmoidVisualization",
    ]),
    ("part1/s04_update_kfactor", [
        "Scene4_1_FeedbackLoop", "Scene4_2_UpdateEquation",
        "Scene4_3_OutperformanceExample",
        "Scene4_4_UnderperformanceExample", "Scene4_5_KFactorSpectrum",
        "Scene4_5a_ExplainKFactor", "Scene4_2a_ExplainUpdateEquation",
    ]),
    ("part1/s05_facemash", [
        "Scene5_1_CulturalExplosion", "Scene5_2_EloForAesthetics",
        "Scene5_3_HollywoodScandal", "Scene5_4_CatastrophicError",
        "Scene5_5_CorrectFormula", "Scene5_3a_ExplainFacemashError",
    ]),
    ("part1/s06_f1_problem", [
        "Scene6_1_StructuralIncompatibility", "Scene6_2_PairwiseExplosion",
        "Scene6_3_DNFAnomaly", "Scene6_4_CarVsDriver",
        "Scene6_5_RussellExample", "Scene6_6_AdvancedSolutionsPreview",
    ]),
    ("part1/s07_bayesian_intro", [
        "Scene7_1_PointVsDistribution", "Scene7_2_BayesTheorem",
        "Scene7_3_RankingContext", "Scene7_4_GaussianGhost",
        "Scene7_5_ScorpionAnalogy", "Scene7_6_TrueSkill",
        "Scene7_2a_ExplainBayesTheorem", "Scene7_6a_ExplainTrueSkill",
    ]),

    # ===== PART 2 SCENES =====
    ("part2/s08_bradley_terry", [
        "Scene8_1_BTLFoundation", "Scene8_2_LogDomain",
        "Scene8_3_Intransitivity", "Scene8_4_HodgeDecomposition",
        "Scene8_1a_ExplainBTL", "Scene8_2a_ExplainLogSigmoid",
        "Scene8_4a_ExplainHodge",
    ]),
    ("part2/s09_plackett_luce", [
        "Scene9_1_BeyondPairwise", "Scene9_2_SequentialSurvival",
        "Scene9_3_LikelihoodFormula", "Scene9_4_InformationWeighting",
        "Scene9_4a_ExplainPLLikelihood", "Scene9_5a_ExplainInfoWeighting",
    ]),
    ("part2/s10_hierarchical", [
        "Scene10_1_LatentDecomposition", "Scene10_2_IdentifiabilityProblem",
        "Scene10_3_DriverPriors", "Scene10_4_ConstructorEvolution",
        "Scene10_5_RuleChangeInflation", "Scene10_6_ThurstoneMosteller",
        "Scene10_1a_ExplainHierarchical", "Scene10_4a_ExplainAutoregressive",
        "Scene10_6a_ExplainThurstone",
    ]),
    ("part2/s11_physics_telemetry", [
        "Scene11_1_TelemetryTruth", "Scene11_2_KalmanFilter",
        "Scene11_3_KalmanEquations", "Scene11_4_BrakingAggression",
        "Scene11_5_FrictionCircle", "Scene11_3a_ExplainKalmanCycle",
        "Scene11_5a_ExplainFrictionCircle",
    ]),
    ("part2/s12_survival", [
        "Scene12_1_DNFAsCensoring", "Scene12_2_HazardFunction",
        "Scene12_3_CoxProportional", "Scene12_4_KaplanMeier",
        "Scene12_5_IPCWWeighting", "Scene12_2a_ExplainHazard",
        "Scene12_3a_ExplainCoxPH", "Scene12_5a_ExplainIPCW",
    ]),

    # ===== PART 3 SCENES =====
    ("part3/s13_mcmc", [
        "Scene13_1_IntractablePosterior", "Scene13_2_GibbsSampler",
        "Scene13_3_TracePlots", "Scene13_4_GelmanRubin",
        "Scene13_2a_ExplainGibbs", "Scene13_4a_ExplainGelmanRubin",
    ]),
    ("part3/s14_volatility", [
        "Scene14_1_DynamicVariance", "Scene14_2_VolatilityParameter",
        "Scene14_3_ShannonEntropy", "Scene14_4_EntropyWeighting",
        "Scene14_3a_ExplainEntropy", "Scene14_4a_ExplainEntropyWeight",
    ]),
    ("part3/s15_historical", [
        "Scene15_1_RidgePlot", "Scene15_2_OverlapProbability",
        "Scene15_3_HHITimeline", "Scene15_4_EraAdjusted", "Scene15_5_PeakComparison",
    ]),
    ("part3/s16_conclusion", [
        "Scene16_1_SystemFlowchart", "Scene16_2_KeyInsights",
        "Scene16_3_ClosingStatement",
    ]),
    ("part3/s17_appendix", [
        "Scene17_1_EloExpectation", "Scene17_2_EloUpdate",
        "Scene17_3_PlackettLuce", "Scene17_4_BradleyTerry",
        "Scene17_5_HierarchicalModel", "Scene17_6_TrueSkill",
        "Scene17_7_Bayes",
    ]),
]


def main():
    quality = "h" if "--hq" in sys.argv else "l"
    parts_only = "--parts-only" in sys.argv
    list_only = "--list" in sys.argv

    scenes_to_render = ALL_SCENES
    if parts_only:
        scenes_to_render = [s for s in ALL_SCENES if s[0].startswith("part")]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(base_dir, "media")

    total_scenes = sum(len(classes) for _, classes in scenes_to_render)

    if list_only:
        print(f"\nListing {len(scenes_to_render)} modules ({total_scenes} scenes):")
        for module, classes in scenes_to_render:
            print(f"  - {module} ({len(classes)} classes)")
        return

    print(f"\n{'='*60}")
    print(f"  RENDERING {total_scenes} SCENES (quality={quality}, parts_only={parts_only})")
    print(f"  Output: {media_dir}/videos/")
    print(f"{'='*60}\n")

    success = 0
    failed = []
    start = time.time()

    for module_path, classes in scenes_to_render:
        scene_file = os.path.join(base_dir, "scenes", module_path.replace("/", os.sep) + ".py")
        if not os.path.exists(scene_file):
            print(f"  [SKIP] File not found: {scene_file}")
            for cls in classes:
                failed.append(f"{module_path}::{cls} (file not found)")
            continue

        for cls in classes:
            rel_path = f"scenes/{module_path}.py"
            cmd = [
                sys.executable, "-m", "manim", "render",
                f"-q{quality}",
                "--media_dir", media_dir,
                rel_path, cls
            ]
            print(f"  [{success+len(failed)+1}/{total_scenes}] {module_path}::{cls} ... ", end="", flush=True)
            try:
                result = subprocess.run(
                    cmd, cwd=base_dir,
                    capture_output=True, text=True, timeout=300
                )
                if result.returncode == 0:
                    success += 1
                    print("OK")
                else:
                    failed.append(f"{module_path}::{cls}")
                    # Print last line of stderr for debugging
                    err = result.stderr.strip().split("\n")[-1] if result.stderr else "unknown"
                    print(f"FAIL ({err})")
            except subprocess.TimeoutExpired:
                failed.append(f"{module_path}::{cls} (timeout)")
                print("TIMEOUT")
            except Exception as e:
                failed.append(f"{module_path}::{cls} ({e})")
                print(f"ERROR ({e})")

    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  DONE in {elapsed:.0f}s")
    print(f"  Success: {success}/{total_scenes}")
    print(f"  Failed:  {len(failed)}/{total_scenes}")
    if failed:
        print(f"\n  Failed scenes:")
        for f in failed:
            print(f"    - {f}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
