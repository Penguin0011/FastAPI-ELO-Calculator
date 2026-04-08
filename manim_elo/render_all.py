"""
Master render script for all ELO explanation scenes.
Renders each scene and can concatenate them into a final video.

Usage:
    python render_all.py --quality l    # Low quality preview
    python render_all.py --quality h    # High quality final
    python render_all.py --scene 1      # Render only scene 1
"""

import subprocess
import os
import argparse

# Scene configuration: (module, scene_classes)
SCENES = [
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
]


def render_scene(module_name, scene_class, quality="l"):
    """Render a single scene."""
    quality_flag = f"-pq{quality}"
    cmd = [
        "python", "-m", "manim", quality_flag,
        f"scenes/{module_name}.py", scene_class
    ]
    print(f"Rendering: {module_name}.{scene_class}")
    subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))


def render_all(quality="l", scene_num=None):
    """Render all scenes or a specific scene."""
    if scene_num is not None:
        # Render specific scene
        idx = scene_num - 1
        if 0 <= idx < len(SCENES):
            module, classes = SCENES[idx]
            for cls in classes:
                render_scene(module, cls, quality)
        else:
            print(f"Invalid scene number: {scene_num}")
    else:
        # Render all
        for module, classes in SCENES:
            for cls in classes:
                render_scene(module, cls, quality)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render ELO explanation animations")
    parser.add_argument("--quality", "-q", default="l", 
                       help="Quality: l=low, m=medium, h=high")
    parser.add_argument("--scene", "-s", type=int, default=None,
                       help="Scene number to render (1-10)")
    
    args = parser.parse_args()
    render_all(args.quality, args.scene)
