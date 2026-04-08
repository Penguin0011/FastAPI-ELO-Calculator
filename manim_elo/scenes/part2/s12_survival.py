# Section 12: Survival Analysis - DNF Mathematics
# 5 Scenes covering censoring and hazard functions

from manim import *
import numpy as np
import sys
sys.path.append('..')
from utils.colors import *


class Scene12_1_DNFAsCensoring(Scene):
    """Scene 12.1: DNF as Censoring, Not Loss."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Survival Analysis for DNFs", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Standard Elo view
        standard = VGroup(
            Text("Standard Elo:", font_size=24, color=ELO_RED),
            Text("DNF = Lost to everyone", font_size=18, color=TEXT_GRAY),
            Text("→ Massive rating drop", font_size=18, color=ELO_RED)
        )
        standard.arrange(DOWN, buff=0.15)
        standard.move_to(LEFT * 3.5 + UP * 0.5)
        standard_box = SurroundingRectangle(standard, color=ELO_RED, buff=0.15)
        
        self.play(FadeIn(standard), Create(standard_box), run_time=1)
        
        # vs
        vs = Text("vs", font_size=28, color=TEXT_GRAY)
        vs.move_to(UP * 0.5)
        self.play(Write(vs), run_time=0.3)
        
        # Survival view
        survival = VGroup(
            Text("Survival View:", font_size=24, color=ELO_GREEN),
            Text("DNF = Observation interrupted", font_size=18, color=TEXT_GRAY),
            Text("→ Right-censored data", font_size=18, color=ELO_GREEN)
        )
        survival.arrange(DOWN, buff=0.15)
        survival.move_to(RIGHT * 3.5 + UP * 0.5)
        survival_box = SurroundingRectangle(survival, color=ELO_GREEN, buff=0.15)
        
        self.play(FadeIn(survival), Create(survival_box), run_time=1)
        
        # Key insight
        insight = VGroup(
            Text("Key Insight:", font_size=22, color=ELO_GOLD),
            Text("Information LOSS, not skill loss", font_size=18, color=TEXT_LIGHT),
            Text("The race just stopped giving us data", font_size=16, color=TEXT_GRAY)
        )
        insight.arrange(DOWN, buff=0.1)
        insight.move_to(DOWN * 2)
        
        self.play(FadeIn(insight), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene12_2_HazardFunction(Scene):
    """Scene 12.2: The Hazard Function."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("The Hazard Function", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Formula
        formula = MathTex(
            r"h(t) = \lim_{\Delta t \to 0} \frac{P(t \leq T < t+\Delta t | T \geq t)}{\Delta t}",
            font_size=32
        )
        formula.move_to(UP * 1.2)
        
        self.play(Write(formula), run_time=1.5)
        
        # Intuition
        intuition = Text(
            "Instantaneous DNF risk at time t, given survival until t",
            font_size=20,
            color=TEXT_LIGHT
        )
        intuition.move_to(UP * 0.4)
        
        self.play(Write(intuition), run_time=1)
        
        # Bathtub curve
        axes = Axes(
            x_range=[0, 60, 10],
            y_range=[0, 0.1, 0.02],
            x_length=8,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.shift(DOWN * 1.5)
        
        x_label = Text("Race Lap", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        
        y_label = Text("Hazard h(t)", font_size=14, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        
        # Bathtub shape
        t = np.linspace(0.1, 60, 100)
        # High at start (infant mortality), low middle, rise at end (wear-out)
        hazard = 0.05 * np.exp(-t/5) + 0.01 + 0.02 * (t/60)**3
        
        curve = VMobject(color=ELO_BLUE)
        curve.set_points_smoothly([axes.c2p(ti, hi) for ti, hi in zip(t, hazard)])
        
        self.play(Create(curve), run_time=1.5)
        
        # Labels for regions
        start_label = Text("Early failures", font_size=12, color=ELO_RED)
        start_label.move_to(axes.c2p(5, 0.07))
        
        mid_label = Text("Stable period", font_size=12, color=ELO_GREEN)
        mid_label.move_to(axes.c2p(30, 0.03))
        
        end_label = Text("Wear-out", font_size=12, color=ELO_GOLD)
        end_label.move_to(axes.c2p(55, 0.05))
        
        self.play(
            FadeIn(start_label), FadeIn(mid_label), FadeIn(end_label),
            run_time=0.8
        )
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene12_3_CoxProportional(Scene):
    """Scene 12.3: Cox Proportional Hazards."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Cox Proportional Hazards", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Formula
        formula = MathTex(
            r"h(t|X) = h_0(t) \exp(\beta^T X)",
            font_size=40
        )
        formula.move_to(UP * 1)
        
        self.play(Write(formula), run_time=1.5)
        
        # Breakdown
        breakdown = VGroup(
            MathTex(r"h_0(t)", font_size=28, color=ELO_BLUE),
            Text("= Baseline hazard", font_size=18, color=TEXT_GRAY),
            MathTex(r"\exp(\beta^T X)", font_size=28, color=ELO_GOLD),
            Text("= Covariate effect", font_size=18, color=TEXT_GRAY)
        )
        breakdown.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.3))
        breakdown.move_to(ORIGIN)
        
        self.play(FadeIn(breakdown), run_time=1)
        
        # Example covariates
        covariates = VGroup(
            Text("Covariates (X):", font_size=20, color=ELO_GOLD),
            Text("• Constructor reliability index", font_size=16, color=TEXT_GRAY),
            Text("• Driver aggression rating", font_size=16, color=TEXT_GRAY),
            Text("• Track characteristics", font_size=16, color=TEXT_GRAY),
            Text("• Weather conditions", font_size=16, color=TEXT_GRAY)
        )
        covariates.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        covariates.move_to(DOWN * 2)
        
        self.play(FadeIn(covariates), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene12_4_KaplanMeier(Scene):
    """Scene 12.4: Kaplan-Meier Curves."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Kaplan-Meier Survival Curves", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Create axes
        axes = Axes(
            x_range=[0, 60, 10],
            y_range=[0, 1, 0.2],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.shift(DOWN * 0.5)
        
        x_label = Text("Lap", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        
        y_label = Text("P(Still Racing)", font_size=14, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        
        # Survival curve (step function)
        # At each DNF, probability steps down
        times = [0, 5, 12, 23, 35, 48, 58]
        probs = [1.0, 0.95, 0.90, 0.85, 0.80, 0.78, 0.75]
        
        survival_curve = VGroup()
        for i in range(len(times) - 1):
            # Horizontal line
            h_line = Line(
                axes.c2p(times[i], probs[i]),
                axes.c2p(times[i+1], probs[i]),
                color=ELO_BLUE
            )
            # Vertical drop
            v_line = Line(
                axes.c2p(times[i+1], probs[i]),
                axes.c2p(times[i+1], probs[i+1]),
                color=ELO_BLUE
            )
            survival_curve.add(h_line, v_line)
        
        # Last horizontal segment
        last_line = Line(
            axes.c2p(times[-1], probs[-1]),
            axes.c2p(60, probs[-1]),
            color=ELO_BLUE
        )
        survival_curve.add(last_line)
        
        self.play(Create(survival_curve), run_time=2)
        
        # Confidence bands
        upper_points = [(t, min(1, p + 0.05)) for t, p in zip(times, probs)]
        lower_points = [(t, max(0, p - 0.05)) for t, p in zip(times, probs)]
        
        upper_band = VMobject(color=ELO_BLUE, stroke_opacity=0.3)
        upper_band.set_points_smoothly([axes.c2p(t, p) for t, p in upper_points])
        
        lower_band = VMobject(color=ELO_BLUE, stroke_opacity=0.3)
        lower_band.set_points_smoothly([axes.c2p(t, p) for t, p in lower_points])
        
        self.play(Create(upper_band), Create(lower_band), run_time=0.8)
        
        # Caption
        caption = Text(
            "Each step down = observed DNF event",
            font_size=18,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.4)
        
        self.play(Write(caption), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene12_5_IPCWWeighting(Scene):
    """Scene 12.5: IPCW Weighting - Partial race contributions."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("IPCW: Inverse Probability Weighting", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Formula
        formula = MathTex(
            r"w_i = \frac{1}{\hat{G}(C_i)}",
            font_size=40
        )
        formula.move_to(UP * 1.2)
        
        formula_text = Text(
            "Weight inversely by probability of being censored",
            font_size=18,
            color=TEXT_GRAY
        )
        formula_text.next_to(formula, DOWN, buff=0.2)
        
        self.play(Write(formula), FadeIn(formula_text), run_time=1)
        
        # Example
        example = VGroup(
            Text("Example:", font_size=22, color=ELO_GOLD),
            Text("Driver leads for 50 of 58 laps → then DNF", font_size=18, color=TEXT_GRAY)
        )
        example.arrange(DOWN, buff=0.1)
        example.move_to(UP * 0)
        
        self.play(FadeIn(example), run_time=0.8)
        
        # Visual: lap progress bar
        bar_bg = Rectangle(width=8, height=0.5, stroke_color=TEXT_GRAY, fill_opacity=0)
        bar_bg.move_to(DOWN * 1)
        
        completed = Rectangle(
            width=8 * (50/58), height=0.5,
            fill_color=ELO_GREEN, fill_opacity=0.7,
            stroke_width=0
        )
        completed.align_to(bar_bg, LEFT)
        completed.move_to(DOWN * 1)
        
        dnf_marker = Line(
            completed.get_right() + UP * 0.4,
            completed.get_right() + DOWN * 0.4,
            color=ELO_RED, stroke_width=4
        )
        dnf_label = Text("DNF", font_size=14, color=ELO_RED)
        dnf_label.next_to(dnf_marker, UP, buff=0.1)
        
        self.play(
            Create(bar_bg),
            FadeIn(completed),
            Create(dnf_marker), FadeIn(dnf_label),
            run_time=1
        )
        
        # Contribution statement
        contribution = VGroup(
            Text("50 laps of P1 → contributes evidence!", font_size=20, color=ELO_GREEN),
            Text("Not 'lost to everyone'", font_size=18, color=TEXT_GRAY),
            Text("Weighted by survival probability", font_size=18, color=TEXT_GRAY)
        )
        contribution.arrange(DOWN, buff=0.15)
        contribution.move_to(DOWN * 2.5)
        
        self.play(FadeIn(contribution), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene12_2a_ExplainHazard(Scene):
    """Scene 12.2a: Hazard Rate in Simple Terms."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Hazard Rate in Simple Terms", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"h(t) = \lim_{\Delta t \to 0} \frac{P(\text{DNF in } [t, t+\Delta t] \,|\, \text{survived to } t)}{\Delta t}",
            font_size=28
        )
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=1.5)

        # Translation
        translation = VGroup(
            Text("In plain English:", font_size=22, color=ELO_GOLD),
            Text("\"If you've survived to lap t, what's your", font_size=18, color=TEXT_GRAY),
            Text("instantaneous risk of DNF RIGHT NOW?\"", font_size=18, color=TEXT_GRAY),
        )
        translation.arrange(DOWN, buff=0.1)
        translation.move_to(UP * 0.1)
        self.play(FadeIn(translation), run_time=0.8)
        self.wait(1)

        # Bathtub curve
        self.play(FadeOut(translation), run_time=0.3)

        bath_title = Text("The 'Bathtub' Curve in F1", font_size=22, color=ELO_GOLD)
        bath_title.move_to(UP * 0.2)
        self.play(FadeIn(bath_title), run_time=0.3)

        axes = Axes(
            x_range=[0, 58, 10], y_range=[0, 1, 0.25],
            x_length=9, y_length=3, tips=False,
            axis_config={"include_numbers": True, "font_size": 10}
        )
        axes.move_to(DOWN * 1)

        x_label = Text("Lap number", font_size=12, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.15)
        y_label = Text("h(t) Risk", font_size=12, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.1)

        def bathtub(t):
            # High at start (chaos), low in middle, rising at end (tyre deg)
            start = 0.7 * np.exp(-t / 5)
            end = 0.3 * np.exp((t - 58) / 8)
            base = 0.05
            return start + end + base

        curve = axes.plot(bathtub, x_range=[0, 58], color=ELO_RED)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.5)
        self.play(Create(curve), run_time=1.5)

        # Labels for the three regions
        lap1_label = Text("Lap 1 chaos", font_size=10, color=ELO_RED)
        lap1_label.move_to(axes.c2p(5, 0.85))
        mid_label = Text("Steady state", font_size=10, color=ELO_GREEN)
        mid_label.move_to(axes.c2p(30, 0.2))
        end_label = Text("Tyre\ndegradation", font_size=10, color=ELO_RED)
        end_label.move_to(axes.c2p(52, 0.5))

        self.play(FadeIn(lap1_label), FadeIn(mid_label), FadeIn(end_label), run_time=0.8)

        note = Text(
            "h(t) is NOT the same as P(DNF during the whole race)!",
            font_size=16, color=ELO_GOLD
        )
        note.to_edge(DOWN, buff=0.3)
        self.play(Write(note), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene12_3a_ExplainCoxPH(Scene):
    """Scene 12.3a: Cox Model — Personal Risk Factors."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Cox Model: Personal Risk Factors", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"h(t|X)", r"=", r"h_0(t)", r"\cdot", r"\exp(\beta^T X)",
            font_size=40
        )
        formula[2].set_color(ELO_BLUE)
        formula[4].set_color(ELO_RED)
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=1.5)

        # Part 1: baseline hazard
        parts = VGroup(
            VGroup(
                MathTex(r"h_0(t)", font_size=28, color=ELO_BLUE),
                Text("= Baseline hazard (same for everyone)", font_size=16, color=TEXT_GRAY),
                Text("The \"average\" risk over time", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                MathTex(r"\exp(\beta^T X)", font_size=28, color=ELO_RED),
                Text("= Personal risk multiplier", font_size=16, color=TEXT_GRAY),
                Text("YOUR specific risk factors scale the baseline", font_size=14, color=TEXT_GRAY)
            ),
        )
        for p in parts:
            p.arrange(DOWN, buff=0.06)
        parts.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        parts.move_to(LEFT * 2 + DOWN * 0.3)

        self.play(FadeIn(parts), run_time=1)
        self.wait(0.5)

        # Worked example
        self.play(FadeOut(parts), run_time=0.3)

        ex_title = Text("Example: Engine Age", font_size=22, color=ELO_GOLD)
        ex_title.next_to(formula, DOWN, buff=0.4)
        self.play(FadeIn(ex_title), run_time=0.3)

        ex = VGroup(
            Text("Covariate: X₁ = engine age (in races)", font_size=18, color=TEXT_GRAY),
            MathTex(r"\beta_1 = 0.5", font_size=24, color=TEXT_WHITE),
            MathTex(r"\exp(0.5) = 1.65", font_size=28, color=ELO_RED),
            Text("→ 65% higher DNF risk with an older engine!", font_size=18, color=ELO_RED),
        )
        ex.arrange(DOWN, buff=0.2)
        ex.move_to(DOWN * 0.8)

        for line in ex:
            self.play(FadeIn(line), run_time=0.5)
            self.wait(0.2)

        # Multiple covariates
        multi = VGroup(
            Text("Multiple factors multiply independently:", font_size=16, color=TEXT_GRAY),
            MathTex(r"\exp(\beta_1 X_1 + \beta_2 X_2) = \exp(\beta_1 X_1) \cdot \exp(\beta_2 X_2)",
                    font_size=22, color=ELO_GREEN)
        )
        multi.arrange(DOWN, buff=0.1)
        multi.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(multi), run_time=0.8)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene12_5a_ExplainIPCW(Scene):
    """Scene 12.5a: IPCW — Counting Partial Races."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("IPCW: Counting Partial Races", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"w_i = \frac{1}{\hat{G}(C_i)}",
            font_size=44
        )
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=1)

        # What each part means
        parts = VGroup(
            VGroup(
                MathTex(r"\hat{G}(C_i)", font_size=28, color=ELO_BLUE),
                Text("= Probability of censoring at time C_i", font_size=16, color=TEXT_GRAY)
            ),
            VGroup(
                MathTex(r"w_i", font_size=28, color=ELO_GREEN),
                Text("= Weight given to this observation", font_size=16, color=TEXT_GRAY)
            ),
        )
        for p in parts:
            p.arrange(RIGHT, buff=0.2)
        parts.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        parts.move_to(DOWN * 0.2)
        self.play(FadeIn(parts), run_time=0.8)
        self.wait(0.5)

        # Intuition
        self.play(FadeOut(parts), run_time=0.3)

        intuition = VGroup(
            Text("The Intuition:", font_size=22, color=ELO_GOLD),
            Text("Low Ĝ(C_i) → unlikely to be censored", font_size=16, color=TEXT_GRAY),
            Text("→ weight ≈ 1 (normal)", font_size=16, color=ELO_GREEN),
            Text("", font_size=6),
            Text("High Ĝ(C_i) → commonly censored here", font_size=16, color=TEXT_GRAY),
            Text("→ upweight to compensate for missing data", font_size=16, color=ELO_RED),
        )
        intuition.arrange(DOWN, buff=0.12)
        intuition.move_to(DOWN * 0.2)
        self.play(FadeIn(intuition), run_time=1)
        self.wait(0.5)

        # Worked example
        self.play(FadeOut(intuition), run_time=0.3)

        ex = VGroup(
            Text("Example: DNF at lap 50 of 58", font_size=22, color=ELO_GOLD),
            MathTex(r"\hat{G}(50) = 0.30", font_size=28, color=ELO_BLUE),
            Text("(30% chance of censoring at lap 50)", font_size=14, color=TEXT_GRAY),
            MathTex(r"w = \frac{1}{0.30} = 3.33", font_size=32, color=ELO_GREEN),
            Text("This driver's partial data counts as 3.3× a full race!", font_size=16, color=ELO_GREEN),
        )
        ex.arrange(DOWN, buff=0.2)
        ex.move_to(DOWN * 0.5)

        for line in ex:
            self.play(FadeIn(line), run_time=0.5)
            self.wait(0.2)

        takeaway = Text(
            "IPCW ensures partial race info isn't thrown away — it's weighted fairly",
            font_size=18, color=ELO_GOLD
        )
        takeaway.to_edge(DOWN, buff=0.3)
        self.play(Write(takeaway), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
