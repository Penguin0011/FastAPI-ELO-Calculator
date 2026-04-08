# Section 13: MCMC Methods
# 4 Scenes covering computational inference

from manim import *
import numpy as np
import sys
sys.path.append('..')
from utils.colors import *


class Scene13_1_IntractablePosterior(Scene):
    """Scene 13.1: Intractable Posteriors."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("The Computational Challenge", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Joint posterior
        formula = MathTex(
            r"P(\alpha, \beta, \gamma | D) \propto P(D | \alpha, \beta, \gamma) P(\alpha) P(\beta) P(\gamma)",
            font_size=28
        )
        formula.move_to(UP * 1)
        
        self.play(Write(formula), run_time=1.5)
        
        # Problem
        problem = VGroup(
            Text("Problem:", font_size=24, color=ELO_RED),
            Text("• 20 drivers × 10 constructors × 20 tracks = 400+ parameters", font_size=18, color=TEXT_GRAY),
            Text("• No closed-form solution", font_size=18, color=TEXT_GRAY),
            Text("• Integration is intractable", font_size=18, color=TEXT_GRAY)
        )
        problem.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        problem.move_to(ORIGIN)
        
        self.play(FadeIn(problem), run_time=1)
        
        # Solution teaser
        solution = VGroup(
            Text("Solution:", font_size=24, color=ELO_GREEN),
            Text("Markov Chain Monte Carlo (MCMC)", font_size=20, color=ELO_GREEN),
            Text("Sample from the posterior distribution!", font_size=18, color=TEXT_GRAY)
        )
        solution.arrange(DOWN, buff=0.1)
        solution.move_to(DOWN * 2)
        
        solution_box = SurroundingRectangle(solution, color=ELO_GREEN, buff=0.15)
        
        self.play(FadeIn(solution), Create(solution_box), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene13_2_GibbsSampler(Scene):
    """Scene 13.2: Gibbs Sampler Algorithm."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Gibbs Sampler", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Algorithm steps
        steps = VGroup(
            Text("Algorithm:", font_size=24, color=ELO_GOLD),
            Text("1. Initialize all parameters (α₀, β₀, γ₀)", font_size=18, color=TEXT_GRAY),
            Text("2. For each iteration:", font_size=18, color=TEXT_GRAY),
            Text("   • Sample α | β, γ, D", font_size=16, color=ELO_BLUE),
            Text("   • Sample β | α, γ, D", font_size=16, color=ELO_GOLD),
            Text("   • Sample γ | α, β, D", font_size=16, color=ELO_GREEN),
            Text("3. Repeat until convergence", font_size=18, color=TEXT_GRAY)
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        steps.move_to(LEFT * 2)
        
        self.play(FadeIn(steps), run_time=1.5)
        
        # Visual: cycling through conditionals
        params = VGroup(
            Rectangle(width=1.5, height=0.8, fill_color=ELO_BLUE, fill_opacity=0.5),
            Rectangle(width=1.5, height=0.8, fill_color=ELO_GOLD, fill_opacity=0.5),
            Rectangle(width=1.5, height=0.8, fill_color=ELO_GREEN, fill_opacity=0.5)
        )
        labels = VGroup(
            Text("α", font_size=24),
            Text("β", font_size=24),
            Text("γ", font_size=24)
        )
        
        for p, l in zip(params, labels):
            l.move_to(p)
        
        params.arrange(DOWN, buff=0.3)
        params.move_to(RIGHT * 4 + DOWN * 0.5)
        
        for p, l in zip(params, labels):
            l.move_to(p)
        
        self.play(FadeIn(params), FadeIn(labels), run_time=0.8)
        
        # Highlight cycling
        highlight = SurroundingRectangle(params[0], color=WHITE, buff=0.05)
        
        self.play(Create(highlight), run_time=0.3)
        self.play(
            highlight.animate.move_to(params[1]),
            run_time=0.5
        )
        self.play(
            highlight.animate.move_to(params[2]),
            run_time=0.5
        )
        self.play(
            highlight.animate.move_to(params[0]),
            run_time=0.5
        )
        
        self.wait(1)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene13_3_TracePlots(Scene):
    """Scene 13.3: Trace Plots - Convergence visualization."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Trace Plots", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Good trace (left)
        axes_good = Axes(
            x_range=[0, 500, 100],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=2.5,
            tips=False,
            axis_config={"font_size": 10}
        )
        axes_good.move_to(LEFT * 3.2 + DOWN * 0.5)
        
        good_label = Text("Good Mixing", font_size=18, color=ELO_GREEN)
        good_label.next_to(axes_good, UP, buff=0.1)
        
        # Generate hairy caterpillar
        np.random.seed(42)
        good_samples = np.cumsum(np.random.normal(0, 0.3, 500))
        good_samples = good_samples - np.mean(good_samples)
        good_samples = np.clip(good_samples, -1.8, 1.8)
        
        good_trace = VMobject(color=ELO_GREEN)
        good_trace.set_points_smoothly([
            axes_good.c2p(i, s) for i, s in enumerate(good_samples)
        ])
        
        self.play(Create(axes_good), FadeIn(good_label), run_time=0.5)
        self.play(Create(good_trace), run_time=1.5)
        
        # Bad trace (right)
        axes_bad = Axes(
            x_range=[0, 500, 100],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=2.5,
            tips=False,
            axis_config={"font_size": 10}
        )
        axes_bad.move_to(RIGHT * 3.2 + DOWN * 0.5)
        
        bad_label = Text("Poor Mixing", font_size=18, color=ELO_RED)
        bad_label.next_to(axes_bad, UP, buff=0.1)
        
        # Slow-moving, stuck chain
        np.random.seed(123)
        bad_samples = np.cumsum(np.random.normal(0, 0.05, 500))  # Much smaller steps
        bad_samples = np.clip(bad_samples, -1.8, 1.8)
        
        bad_trace = VMobject(color=ELO_RED)
        bad_trace.set_points_smoothly([
            axes_bad.c2p(i, s) for i, s in enumerate(bad_samples)
        ])
        
        self.play(Create(axes_bad), FadeIn(bad_label), run_time=0.5)
        self.play(Create(bad_trace), run_time=1.5)
        
        # Descriptions
        good_desc = Text('"Hairy caterpillar"', font_size=14, color=ELO_GREEN)
        good_desc.next_to(axes_good, DOWN, buff=0.2)
        
        bad_desc = Text('"Wandering snake"', font_size=14, color=ELO_RED)
        bad_desc.next_to(axes_bad, DOWN, buff=0.2)
        
        self.play(FadeIn(good_desc), FadeIn(bad_desc), run_time=0.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene13_4_GelmanRubin(Scene):
    """Scene 13.4: Gelman-Rubin Convergence Diagnostic."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Gelman-Rubin Diagnostic", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Formula
        formula = MathTex(
            r"\hat{R} = \sqrt{\frac{\hat{V}}{W}}",
            font_size=44
        )
        formula.move_to(UP * 1)
        
        self.play(Write(formula), run_time=1)
        
        # Explanation
        explain = VGroup(
            MathTex(r"\hat{V}", font_size=28, color=ELO_BLUE),
            Text("= Total variance estimate", font_size=16, color=TEXT_GRAY),
            MathTex(r"W", font_size=28, color=ELO_GOLD),
            Text("= Within-chain variance", font_size=16, color=TEXT_GRAY)
        )
        explain.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.2))
        explain.move_to(DOWN * 0.3)
        
        self.play(FadeIn(explain), run_time=0.8)
        
        # Convergence condition
        condition = VGroup(
            Text("Convergence criterion:", font_size=22, color=ELO_GOLD),
            MathTex(r"\hat{R} < 1.1", font_size=36, color=ELO_GREEN)
        )
        condition.arrange(DOWN, buff=0.2)
        condition.move_to(DOWN * 2)
        
        condition_box = SurroundingRectangle(condition, color=ELO_GREEN, buff=0.15)
        
        self.play(Write(condition), Create(condition_box), run_time=1)
        
        # Intuition
        intuition = Text(
            "If chains from different starts agree → converged!",
            font_size=18,
            color=TEXT_LIGHT
        )
        intuition.to_edge(DOWN, buff=0.3)
        
        self.play(Write(intuition), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene13_2a_ExplainGibbs(Scene):
    """Scene 13.2a: Gibbs Sampling — One Variable at a Time."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Gibbs Sampling: One Variable at a Time", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # The problem
        problem = VGroup(
            Text("We need the joint posterior of α, β, γ", font_size=22, color=ELO_GOLD),
            Text("...but we can't sample all 3 at once!", font_size=18, color=ELO_RED),
        )
        problem.arrange(DOWN, buff=0.1)
        problem.move_to(UP * 1)
        self.play(FadeIn(problem), run_time=0.8)
        self.wait(0.5)

        # Solution: cycle through variables
        self.play(FadeOut(problem), run_time=0.3)

        solution = Text("Solution: Sample one variable at a time, holding others fixed",
                        font_size=18, color=ELO_GREEN)
        solution.move_to(UP * 1.2)
        self.play(FadeIn(solution), run_time=0.5)

        # Three variable boxes
        alpha_box = VGroup(
            Rectangle(width=2.5, height=1.5, fill_color=ELO_BLUE, fill_opacity=0.15, stroke_color=ELO_BLUE),
            MathTex(r"\alpha", font_size=36, color=ELO_BLUE),
            Text("Driver skill", font_size=12, color=TEXT_GRAY)
        )
        alpha_box[1].move_to(alpha_box[0].get_center() + UP * 0.15)
        alpha_box[2].move_to(alpha_box[0].get_center() + DOWN * 0.35)

        beta_box = VGroup(
            Rectangle(width=2.5, height=1.5, fill_color=ELO_GOLD, fill_opacity=0.15, stroke_color=ELO_GOLD),
            MathTex(r"\beta", font_size=36, color=ELO_GOLD),
            Text("Car strength", font_size=12, color=TEXT_GRAY)
        )
        beta_box[1].move_to(beta_box[0].get_center() + UP * 0.15)
        beta_box[2].move_to(beta_box[0].get_center() + DOWN * 0.35)

        gamma_box = VGroup(
            Rectangle(width=2.5, height=1.5, fill_color=ELO_GREEN, fill_opacity=0.15, stroke_color=ELO_GREEN),
            MathTex(r"\gamma", font_size=36, color=ELO_GREEN),
            Text("Track fit", font_size=12, color=TEXT_GRAY)
        )
        gamma_box[1].move_to(gamma_box[0].get_center() + UP * 0.15)
        gamma_box[2].move_to(gamma_box[0].get_center() + DOWN * 0.35)

        boxes = VGroup(alpha_box, beta_box, gamma_box)
        boxes.arrange(RIGHT, buff=0.5)
        boxes.move_to(DOWN * 0.3)

        self.play(FadeIn(boxes), run_time=1)

        # Steps: cycle through highlighting
        step_labels = [
            (r"\alpha | \beta, \gamma, D", ELO_BLUE, "Sample α, fix β and γ"),
            (r"\beta | \alpha, \gamma, D", ELO_GOLD, "Sample β, fix α and γ"),
            (r"\gamma | \alpha, \beta, D", ELO_GREEN, "Sample γ, fix α and β"),
        ]

        step_text_pos = DOWN * 2.2
        highlight_rects = [
            SurroundingRectangle(alpha_box, color=ELO_BLUE, buff=0.1),
            SurroundingRectangle(beta_box, color=ELO_GOLD, buff=0.1),
            SurroundingRectangle(gamma_box, color=ELO_GREEN, buff=0.1),
        ]

        prev_step = None
        prev_rect = None

        # Do 2 full cycles
        for cycle in range(2):
            for i, (math_str, color, desc) in enumerate(step_labels):
                step_grp = VGroup(
                    MathTex(f"\\text{{Sample: }} {math_str}", font_size=22, color=color),
                    Text(desc, font_size=14, color=TEXT_GRAY)
                )
                step_grp.arrange(DOWN, buff=0.08)
                step_grp.move_to(step_text_pos)

                anims = [FadeIn(step_grp), Create(highlight_rects[i])]
                if prev_step:
                    anims.extend([FadeOut(prev_step), FadeOut(prev_rect)])
                self.play(*anims, run_time=0.5)
                self.wait(0.3)

                prev_step = step_grp
                prev_rect = highlight_rects[i]
                highlight_rects[i] = SurroundingRectangle(boxes[i], color=step_labels[i][1], buff=0.1)

        self.play(FadeOut(prev_step), FadeOut(prev_rect), run_time=0.3)

        repeat = Text(
            "Repeat 10,000× → histogram of samples ≈ the posterior distribution!",
            font_size=18, color=ELO_GOLD
        )
        repeat.to_edge(DOWN, buff=0.3)
        self.play(Write(repeat), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene13_4a_ExplainGelmanRubin(Scene):
    """Scene 13.4a: R̂ — Are the Chains Agreeing?"""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("R̂: Are the Chains Agreeing?", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"\hat{R} = \sqrt{\frac{\hat{V}}{W}}",
            font_size=48
        )
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=1.5)

        # Definitions
        defs = VGroup(
            VGroup(
                MathTex(r"W", font_size=28, color=ELO_BLUE),
                Text("= Average variance WITHIN each chain", font_size=16, color=TEXT_GRAY)
            ),
            VGroup(
                MathTex(r"\hat{V}", font_size=28, color=ELO_RED),
                Text("= Total variance (within + between chains)", font_size=16, color=TEXT_GRAY)
            ),
        )
        for d in defs:
            d.arrange(RIGHT, buff=0.2)
        defs.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        defs.move_to(DOWN * 0.2)
        self.play(FadeIn(defs), run_time=0.8)
        self.wait(0.5)

        # Two scenarios
        self.play(FadeOut(defs), run_time=0.3)

        # Converged
        good = VGroup(
            Text("Chains AGREE (converged):", font_size=20, color=ELO_GREEN),
            Text("Between-chain variance ≈ 0", font_size=16, color=TEXT_GRAY),
            MathTex(r"\hat{V} \approx W \implies \hat{R} \approx 1.0", font_size=24, color=ELO_GREEN),
            Text("✓ Safe to use results!", font_size=14, color=ELO_GREEN),
        )
        good.arrange(DOWN, buff=0.1)
        good.move_to(LEFT * 3 + DOWN * 0.3)

        # Not converged
        bad = VGroup(
            Text("Chains DISAGREE:", font_size=20, color=ELO_RED),
            Text("Between-chain variance >> 0", font_size=16, color=TEXT_GRAY),
            MathTex(r"\hat{V} \gg W \implies \hat{R} \gg 1", font_size=24, color=ELO_RED),
            Text("✗ NOT converged — run longer!", font_size=14, color=ELO_RED),
        )
        bad.arrange(DOWN, buff=0.1)
        bad.move_to(RIGHT * 3 + DOWN * 0.3)

        self.play(FadeIn(good), FadeIn(bad), run_time=1)

        # Rule of thumb
        rule = VGroup(
            Text("Rule of Thumb:", font_size=22, color=ELO_GOLD),
            MathTex(r"\hat{R} < 1.1 \implies \text{converged}", font_size=28, color=ELO_GREEN),
        )
        rule.arrange(DOWN, buff=0.1)
        rule.to_edge(DOWN, buff=0.3)
        rule_box = SurroundingRectangle(rule, color=ELO_GOLD, buff=0.15)
        self.play(FadeIn(rule), Create(rule_box), run_time=0.8)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
