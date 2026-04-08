# Section 14: Volatility, K-Factors, and Entropy
# 4 Scenes covering dynamic variance

from manim import *
import numpy as np
import sys
sys.path.append('..')
from utils.colors import *


class Scene14_1_DynamicVariance(Scene):
    """Scene 14.1: Dynamic Variance (Glicko-2)."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Glicko-2: Dynamic Uncertainty", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Core concept
        concept = VGroup(
            Text("Rating Deviation (RD) is ALIVE", font_size=24, color=ELO_GOLD),
            Text("Not static like in Elo", font_size=18, color=TEXT_GRAY)
        )
        concept.arrange(DOWN, buff=0.1)
        concept.move_to(UP * 1.2)
        
        self.play(FadeIn(concept), run_time=0.8)
        
        # Two behaviors
        behaviors = VGroup(
            VGroup(
                Text("When INACTIVE:", font_size=20, color=ELO_RED),
                Text("RD increases", font_size=16, color=TEXT_GRAY),
                Text("(Uncertainty grows)", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                Text("When PLAYING:", font_size=20, color=ELO_GREEN),
                Text("RD decreases", font_size=16, color=TEXT_GRAY),
                Text("(Learning shrinks it)", font_size=14, color=TEXT_GRAY)
            )
        )
        
        for b in behaviors:
            b.arrange(DOWN, buff=0.1)
        behaviors.arrange(RIGHT, buff=2)
        behaviors.move_to(ORIGIN)
        
        self.play(FadeIn(behaviors), run_time=1)
        
        # Timeline visual
        axes = Axes(
            x_range=[0, 12, 2],
            y_range=[0, 150, 50],
            x_length=8,
            y_length=2.5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.shift(DOWN * 1.8)
        
        x_label = Text("Months", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        
        y_label = Text("RD", font_size=14, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        
        # RD trajectory
        rd_values = [50, 55, 60, 40, 45, 80, 85, 50, 45, 55, 60, 45]
        rd_trace = VMobject(color=ELO_PURPLE)
        rd_trace.set_points_smoothly([axes.c2p(i, rd) for i, rd in enumerate(rd_values)])
        
        self.play(Create(rd_trace), run_time=1.5)
        
        # Labels for activity
        active_label = Text("Active", font_size=12, color=ELO_GREEN)
        active_label.move_to(axes.c2p(3, 30))
        
        inactive_label = Text("Break", font_size=12, color=ELO_RED)
        inactive_label.move_to(axes.c2p(6, 100))
        
        self.play(FadeIn(active_label), FadeIn(inactive_label), run_time=0.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene14_2_VolatilityParameter(Scene):
    """Scene 14.2: The Volatility Parameter."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Volatility: The Third Parameter", font_size=44, color=ELO_PURPLE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Three parameters
        params = VGroup(
            VGroup(MathTex(r"\mu", font_size=48, color=ELO_BLUE), Text("Rating", font_size=16, color=TEXT_GRAY)),
            VGroup(MathTex(r"\phi", font_size=48, color=ELO_GOLD), Text("Deviation", font_size=16, color=TEXT_GRAY)),
            VGroup(MathTex(r"\sigma", font_size=48, color=ELO_PURPLE), Text("Volatility", font_size=16, color=TEXT_GRAY))
        )
        for p in params:
            p.arrange(DOWN, buff=0.1)
        params.arrange(RIGHT, buff=1.5)
        params.move_to(UP * 0.5)
        
        self.play(FadeIn(params), run_time=1)
        
        # Volatility explanation
        explanation = VGroup(
            Text("Volatility responds to SURPRISE:", font_size=22, color=ELO_GOLD),
            Text("• Unexpected win/loss → σ rises", font_size=18, color=TEXT_GRAY),
            Text("• Expected results → σ stable", font_size=18, color=TEXT_GRAY),
            Text("• Acts like adaptive K-factor", font_size=18, color=ELO_GREEN)
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explanation.move_to(DOWN * 1.5)
        
        self.play(FadeIn(explanation), run_time=1)
        
        # Caption
        caption = Text(
            "High volatility = Allow rapid correction",
            font_size=20,
            color=TEXT_LIGHT
        )
        caption.to_edge(DOWN, buff=0.4)
        
        self.play(Write(caption), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene14_3_ShannonEntropy(Scene):
    """Scene 14.3: Shannon Entropy."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Shannon Entropy", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Formula
        formula = MathTex(
            r"H = -\sum_{i} p_i \log p_i",
            font_size=44
        )
        formula.move_to(UP * 1)
        
        self.play(Write(formula), run_time=1)
        
        # Intuition
        intuition = Text("Measures unpredictability of outcome", font_size=20, color=TEXT_LIGHT)
        intuition.move_to(UP * 0.2)
        
        self.play(Write(intuition), run_time=0.8)
        
        # Two race scenarios
        low_entropy = VGroup(
            Text("Low Entropy Race", font_size=20, color=ELO_BLUE),
            Text("Dry conditions", font_size=16, color=TEXT_GRAY),
            Text("Dominant team", font_size=16, color=TEXT_GRAY),
            Text("→ Predictable", font_size=16, color=ELO_BLUE)
        )
        low_entropy.arrange(DOWN, buff=0.1)
        low_entropy.move_to(LEFT * 3.5 + DOWN * 1.5)
        
        high_entropy = VGroup(
            Text("High Entropy Race", font_size=20, color=ELO_RED),
            Text("Rain chaos", font_size=16, color=TEXT_GRAY),
            Text("Safety cars", font_size=16, color=TEXT_GRAY),
            Text("→ Unpredictable!", font_size=16, color=ELO_RED)
        )
        high_entropy.arrange(DOWN, buff=0.1)
        high_entropy.move_to(RIGHT * 3.5 + DOWN * 1.5)
        
        self.play(FadeIn(low_entropy), FadeIn(high_entropy), run_time=1)
        
        # Caption
        caption = Text(
            "High entropy = less informative about true skill",
            font_size=18,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.4)
        
        self.play(Write(caption), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene14_4_EntropyWeighting(Scene):
    """Scene 14.4: Entropy-Weighted Updates."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Entropy-Weighted Learning", font_size=44, color=ELO_GREEN)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Concept
        concept = Text(
            "Weight updates by race informativeness",
            font_size=24,
            color=TEXT_LIGHT
        )
        concept.move_to(UP * 1.2)
        
        self.play(Write(concept), run_time=0.8)
        
        # Formula
        formula = MathTex(
            r"w_{update} \propto e^{-H}",
            font_size=40
        )
        formula.move_to(UP * 0.3)
        
        self.play(Write(formula), run_time=1)
        
        # Interpretation
        interpretation = VGroup(
            Text("• Low entropy (H small) → e⁻ᴴ ≈ 1 → Full weight", font_size=18, color=ELO_GREEN),
            Text("• High entropy (H large) → e⁻ᴴ → 0 → Reduced weight", font_size=18, color=ELO_RED)
        )
        interpretation.arrange(DOWN, buff=0.2)
        interpretation.move_to(DOWN * 0.8)
        
        self.play(FadeIn(interpretation), run_time=1)
        
        # Example
        example = VGroup(
            Text("Example:", font_size=20, color=ELO_GOLD),
            Text("Rain race with 5 retirements → H = 2.5 → w = 0.08", font_size=16, color=TEXT_GRAY),
            Text("Dry race, expected order → H = 0.3 → w = 0.74", font_size=16, color=TEXT_GRAY)
        )
        example.arrange(DOWN, buff=0.1)
        example.move_to(DOWN * 2.2)
        
        self.play(FadeIn(example), run_time=1)
        
        # Caption
        caption = Text(
            '"Don\'t overfit to lottery results"',
            font_size=18,
            color=TEXT_LIGHT
        )
        caption.to_edge(DOWN, buff=0.3)
        
        self.play(Write(caption), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene14_3a_ExplainEntropy(Scene):
    """Scene 14.3a: Shannon Entropy — Measuring Chaos."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Shannon Entropy: Measuring Chaos", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"H = -\sum_{i=1}^{n} p_i \log(p_i)",
            font_size=44
        )
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=1.5)

        # What p_i is
        pi_explain = VGroup(
            MathTex(r"p_i", font_size=28, color=ELO_GOLD),
            Text("= probability that driver i wins", font_size=16, color=TEXT_GRAY)
        )
        pi_explain.arrange(RIGHT, buff=0.2)
        pi_explain.move_to(UP * 0.4)
        self.play(FadeIn(pi_explain), run_time=0.5)
        self.wait(0.3)

        # Example 1: Low entropy — dominant team
        self.play(FadeOut(pi_explain), run_time=0.2)

        examples_title = Text("Two Scenarios", font_size=22, color=ELO_GOLD)
        examples_title.move_to(UP * 0.5)
        self.play(FadeIn(examples_title), run_time=0.3)

        # Low entropy bar chart
        low_probs = [0.45, 0.35, 0.10, 0.05, 0.03, 0.02]
        high_probs = [0.06, 0.06, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.05, 0.05,
                      0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.04, 0.03, 0.03]

        import math
        low_h = -sum(p * math.log(p) for p in low_probs if p > 0)
        high_h = -sum(p * math.log(p) for p in high_probs if p > 0)

        # Low entropy
        low_bars = VGroup()
        for i, p in enumerate(low_probs):
            bar = Rectangle(
                width=0.3, height=p * 5,
                fill_color=ELO_BLUE, fill_opacity=0.7, stroke_width=0.5
            )
            bar.move_to(LEFT * 5 + RIGHT * i * 0.4 + DOWN * 1.5, aligned_edge=DOWN)
            low_bars.add(bar)

        low_title = VGroup(
            Text("Dominant team", font_size=14, color=ELO_BLUE),
            MathTex(f"H = {low_h:.2f}", font_size=20, color=ELO_BLUE),
            Text("(predictable)", font_size=12, color=TEXT_GRAY)
        )
        low_title.arrange(DOWN, buff=0.06)
        low_title.move_to(LEFT * 3.8 + DOWN * 0.2)

        # High entropy
        high_bars = VGroup()
        for i, p in enumerate(high_probs):
            bar = Rectangle(
                width=0.15, height=p * 5,
                fill_color=ELO_RED, fill_opacity=0.7, stroke_width=0.5
            )
            bar.move_to(RIGHT * 1 + RIGHT * i * 0.25 + DOWN * 1.5, aligned_edge=DOWN)
            high_bars.add(bar)

        high_title = VGroup(
            Text("Anyone can win", font_size=14, color=ELO_RED),
            MathTex(f"H = {high_h:.2f}", font_size=20, color=ELO_RED),
            Text("(chaotic)", font_size=12, color=TEXT_GRAY)
        )
        high_title.arrange(DOWN, buff=0.06)
        high_title.move_to(RIGHT * 3.5 + DOWN * 0.2)

        self.play(FadeIn(low_bars), FadeIn(low_title), run_time=0.8)
        self.play(FadeIn(high_bars), FadeIn(high_title), run_time=0.8)

        # Key insight
        insight = VGroup(
            MathTex(r"H = 0 \implies \text{perfectly predictable}", font_size=20, color=ELO_GREEN),
            MathTex(r"H = \log(N) \implies \text{maximum chaos}", font_size=20, color=ELO_RED),
        )
        insight.arrange(DOWN, buff=0.1)
        insight.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(insight), run_time=0.8)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene14_4a_ExplainEntropyWeight(Scene):
    """Scene 14.4a: Downweighting Chaos — w ∝ e^{-H}."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Downweighting Chaos", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"w_{\text{update}} \propto e^{-H}",
            font_size=48
        )
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=1.5)

        # Case 1: Low entropy
        cases = VGroup(
            VGroup(
                Text("Predictable race (H ≈ 0):", font_size=20, color=ELO_GREEN),
                MathTex(r"w = e^{0} = 1.0", font_size=28, color=ELO_GREEN),
                Text("→ Full weight: this race is informative!", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                Text("Moderate chaos (H ≈ 1.5):", font_size=20, color=ELO_GOLD),
                MathTex(r"w = e^{-1.5} = 0.22", font_size=28, color=ELO_GOLD),
                Text("→ 22% weight: take with a grain of salt", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                Text("Full chaos (H ≈ 2.5):", font_size=20, color=ELO_RED),
                MathTex(r"w = e^{-2.5} = 0.08", font_size=28, color=ELO_RED),
                Text("→ 8% weight: mostly noise, ignore", font_size=14, color=TEXT_GRAY)
            ),
        )

        for case in cases:
            case.arrange(DOWN, buff=0.08)
        cases.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        cases.move_to(DOWN * 0.3)

        for case in cases:
            self.play(FadeIn(case), run_time=0.6)
            self.wait(0.3)

        self.wait(0.5)

        # Visual: weight bar shrinking
        self.play(FadeOut(cases), run_time=0.3)

        bar_title = Text("Weight vs Entropy", font_size=22, color=ELO_GOLD)
        bar_title.next_to(header, DOWN, buff=0.4)
        self.play(FadeIn(bar_title), run_time=0.3)

        axes = Axes(
            x_range=[0, 3, 0.5], y_range=[0, 1, 0.25],
            x_length=8, y_length=3, tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.move_to(DOWN * 0.5)

        x_label = MathTex(r"H \text{ (entropy)}", font_size=16, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = MathTex(r"w \text{ (weight)}", font_size=16, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)

        def weight_fn(h):
            return np.exp(-h)

        curve = axes.plot(weight_fn, x_range=[0, 3], color=ELO_GREEN)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), Create(curve), run_time=1)

        # Mark key points
        for h, w_str, color in [(0, "1.00", ELO_GREEN), (1.5, "0.22", ELO_GOLD), (2.5, "0.08", ELO_RED)]:
            dot = Dot(axes.c2p(h, weight_fn(h)), color=color, radius=0.08)
            label = Text(w_str, font_size=12, color=color)
            label.next_to(dot, UR, buff=0.1)
            self.play(FadeIn(dot), FadeIn(label), run_time=0.3)

        # F1 example
        f1_note = Text(
            "F1: Spa 2021 (2 laps, red flag) → high H → tiny weight in Elo update",
            font_size=16, color=ELO_GOLD
        )
        f1_note.to_edge(DOWN, buff=0.3)
        self.play(Write(f1_note), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
