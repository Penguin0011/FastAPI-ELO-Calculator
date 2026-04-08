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
    ("part1/s01_introduction", [
        "Scene1_1_WelcomeHook", "Scene1_2_Chess960History",
        "Scene1_3_TimelineOfElo", "Scene1_4_ProjectGoal",
    ]),
    ("part1/s02_harkness", [
        "Scene2_1_HarknessOpening", "Scene2_2_HarknessTable",
        "Scene2_3_HarknessProblems", "Scene2_4_EloInsight",
    ]),
    ("part1/s03_elo_physics", [
        "Scene3_1_PhysicsOfUncertainty", "Scene3_2_NormalDistOrigin",
        "Scene3_3_NormalDistribution",
        "Scene3_3a_ExplainNormalPDF",        # NEW
        "Scene3_4_DifferenceOfNormals", "Scene3_5_FromNormalToLogistic",
        "Scene3_6_LogisticRevelation",
        "Scene3_6a_ExplainLogisticVsNormal",  # NEW
        "Scene3_7_ModernEloFormula",
        "Scene3_7a_ExplainEloFormula",        # NEW
    ]),
    ("part1/s04_update_kfactor", [
        "Scene4_1_LiveRating", "Scene4_2_UpdateEquation",
        "Scene4_2a_ExplainUpdateEquation",    # NEW
        "Scene4_3_SurpriseQuantified", "Scene4_4_WorkedExample1500v1700",
        "Scene4_5_KFactorIntro",
        "Scene4_5a_ExplainKFactor",           # NEW
    ]),
    ("part1/s05_facemash", [
        "Scene5_1_DormRoomStory", "Scene5_2_FacemashCode",
        "Scene5_3_FacemashError",
        "Scene5_3a_ExplainFacemashError",     # NEW
        "Scene5_4_GrandVision",
    ]),
    ("part1/s06_f1_problem", [
        "Scene6_1_WhyEloFails", "Scene6_2_PairwiseLimit",
        "Scene6_3_SharedCars", "Scene6_4_RequirementStatement",
    ]),
    ("part1/s07_bayesian_intro", [
        "Scene7_1_BayesianWorldview", "Scene7_2_BayesColored",
        "Scene7_2a_ExplainBayesTheorem",      # NEW
        "Scene7_3_PriorPosterior", "Scene7_4_F1RookieExample",
        "Scene7_5_DistributionVisualization", "Scene7_6_TrueSkillPreview",
        "Scene7_6a_ExplainTrueSkill",         # NEW
    ]),

    # ===== PART 2 SCENES =====
    ("part2/s08_bradley_terry", [
        "Scene8_1_PairwiseProbability", "Scene8_2_LogDomainTrick",
        "Scene8_1a_ExplainBTL",               # NEW
        "Scene8_2a_ExplainLogSigmoid",        # NEW
        "Scene8_3_ConnectToElo", "Scene8_4_HodgeDecomposition",
        "Scene8_4a_ExplainHodge",             # NEW
    ]),
    ("part2/s09_plackett_luce", [
        "Scene9_1_RacingExtension", "Scene9_2_SequentialElimination",
        "Scene9_3_F1LikelihoodDemo", "Scene9_4_PlackettLuceLikelihood",
        "Scene9_4a_ExplainPLLikelihood",      # NEW
        "Scene9_5_InformationWeighting",
        "Scene9_5a_ExplainInfoWeighting",     # NEW
    ]),
    ("part2/s10_hierarchical", [
        "Scene10_1_PerformanceDecomposition",
        "Scene10_1a_ExplainHierarchical",     # NEW
        "Scene10_2_DAGVisualization",
        "Scene10_3_GammaExplained", "Scene10_4_ConstructorDrift",
        "Scene10_4a_ExplainAutoregressive",   # NEW
        "Scene10_5_ShrinkageVisualization", "Scene10_6_ThurstoneMosteller",
        "Scene10_6a_ExplainThurstone",        # NEW
    ]),
    ("part2/s11_physics_telemetry", [
        "Scene11_1_TelemetryIntro", "Scene11_2_SpeedTraceWalkthrough",
        "Scene11_3_KalmanSmoothing",
        "Scene11_3a_ExplainKalmanCycle",      # NEW
        "Scene11_4_BrakingMetric", "Scene11_5_FrictionCircle",
        "Scene11_5a_ExplainFrictionCircle",   # NEW
        "Scene11_6_CornerApexVisualization",
    ]),
    ("part2/s12_survival", [
        "Scene12_1_DNFProblem", "Scene12_2_SurvivalCurve",
        "Scene12_2a_ExplainHazard",           # NEW
        "Scene12_3_CoxModel",
        "Scene12_3a_ExplainCoxPH",            # NEW
        "Scene12_4_RobberyProtocol", "Scene12_5_IPCWExplainer",
        "Scene12_5a_ExplainIPCW",             # NEW
    ]),

    # ===== PART 3 SCENES =====
    ("part3/s13_mcmc", [
        "Scene13_1_MCMCMotivation", "Scene13_2_GibbsVisualization",
        "Scene13_2a_ExplainGibbs",            # NEW
        "Scene13_3_ConvergenceDiagnostics", "Scene13_4_GelmanRubin",
        "Scene13_4a_ExplainGelmanRubin",      # NEW
    ]),
    ("part3/s14_volatility", [
        "Scene14_1_RaceEntropy", "Scene14_2_EntropyCalculation",
        "Scene14_3_EntropyWeighting",
        "Scene14_3a_ExplainEntropy",          # NEW
        "Scene14_4_VolatilityUpdate",
        "Scene14_4a_ExplainEntropyWeight",    # NEW
    ]),
    ("part3/s15_historical", [
        "Scene15_1_HistoryReel", "Scene15_2_CrossEraGraph",
        "Scene15_3_TopDriversReveal",
    ]),
    ("part3/s16_conclusion", [
        "Scene16_1_RecapMontage", "Scene16_2_FutureIdeas",
        "Scene16_3_CloseOut",
    ]),
    ("part3/s17_appendix", [
        "Scene17_1_FullFormulaSheet", "Scene17_2_ParameterTable",
    ]),
]


def main():
    quality = "h" if "--hq" in sys.argv else "l"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(base_dir, "media")

    total_scenes = sum(len(classes) for _, classes in ALL_SCENES)
    print(f"\n{'='*60}")
    print(f"  RENDERING ALL {total_scenes} SCENES (quality={quality})")
    print(f"  Output: {media_dir}/videos/")
    print(f"{'='*60}\n")

    success = 0
    failed = []
    start = time.time()

    for module_path, classes in ALL_SCENES:
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
