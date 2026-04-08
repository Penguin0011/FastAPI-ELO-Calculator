"""
Scene 3: Core ELO Mathematics
Deep dive into the mathematical foundations of the Elo rating system.

This scene covers:
- Expected Score formula derivation intuition
- The sigmoid curve and its meaning
- K-factor and its role in volatility
- Rating update dynamics with examples
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.formulas import *


class EloMathIntro(Scene):
    """Introduction to the mathematical deep dive."""
    
    def construct(self):
        title = Text("The Mathematics of ELO", font_size=48, color=LIGHT_BLUE)
        subtitle = Text("A deep dive into the formulas", font_size=28, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(subtitle))


class ExpectedScoreDerivation(Scene):
    """Derive the expected score formula intuitively."""
    
    def construct(self):
        title = Text("Expected Score: The Core Idea", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Start with the question
        question = Text(
            "What's the probability that Player A beats Player B?",
            font_size=28, color=WHITE
        )
        question.shift(UP * 1.5)
        
        self.play(Write(question), run_time=1.5)
        self.wait(1)
        
        # Key insight
        insight = VGroup(
            Text("Elo's Answer:", font_size=28, color=TEAL),
            Text("It depends on the rating DIFFERENCE", font_size=28, color=WHITE),
        )
        insight.arrange(DOWN, buff=0.1)
        insight.shift(UP * 0.3)
        
        self.play(Write(insight), run_time=1.5)
        self.wait(1)
        
        # Define delta
        delta_def = MathTex(
            r"\Delta R = R_A - R_B",
            font_size=40
        )
        delta_def.shift(DOWN * 0.5)
        delta_def.set_color_by_tex_to_color_map({
            r"\Delta R": YELLOW,
            "R_A": TEAL,
            "R_B": ORANGE,
        })
        
        self.play(Write(delta_def), run_time=1)
        self.wait(1)
        
        # Cases
        cases = VGroup(
            Text("If ΔR = 0 (equal)    → P(Win) should be 50%", font_size=22, color=WHITE),
            Text("If ΔR > 0 (A higher) → P(Win) should be > 50%", font_size=22, color=ELO_POSITIVE),
            Text("If ΔR < 0 (A lower)  → P(Win) should be < 50%", font_size=22, color=ELO_NEGATIVE),
        )
        cases.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        cases.shift(DOWN * 1.8)
        
        for case in cases:
            self.play(Write(case), run_time=0.7)
        
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != title])
        
        # Why 400?
        why_400 = Text("But why 400? Why base 10?", font_size=32, color=ORANGE)
        why_400.shift(UP * 1)
        
        self.play(Write(why_400), run_time=1)
        
        # Explanation
        explanation = VGroup(
            Text("Elo chose 400 so that:", font_size=26, color=WHITE),
            Text("• +400 rating → ~91% win probability", font_size=24, color=GREY),
            Text("• +200 rating → ~76% win probability", font_size=24, color=GREY),
            Text("• These felt \"right\" based on historical chess data", font_size=24, color=GREY),
        )
        explanation.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        explanation.shift(DOWN * 0.5)
        
        self.play(Write(explanation), run_time=2)
        self.wait(2)
        
        # The formula
        formula_text = Text("The resulting formula:", font_size=28, color=TEAL)
        formula_text.shift(DOWN * 2)
        
        self.play(Write(formula_text), run_time=0.8)
        self.wait(0.5)
        
        self.play(FadeOut(why_400), FadeOut(explanation), FadeOut(formula_text))
        self.play(FadeOut(title))


class ExpectedScoreFormula(Scene):
    """Show the complete expected score formula."""
    
    def construct(self):
        title = Text("The Expected Score Formula", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Build up the formula step by step
        step1 = MathTex(r"E_A = \text{?}", font_size=44)
        step1.shift(UP * 1)
        
        self.play(Write(step1), run_time=0.8)
        self.wait(0.5)
        
        step2 = MathTex(
            r"E_A = \frac{1}{1 + ?}",
            font_size=44
        )
        step2.shift(UP * 1)
        
        self.play(Transform(step1, step2), run_time=1)
        self.wait(0.5)
        
        step3 = MathTex(
            r"E_A = \frac{1}{1 + 10^{?}}",
            font_size=44
        )
        step3.shift(UP * 1)
        
        self.play(Transform(step1, step3), run_time=1)
        self.wait(0.5)
        
        # Final formula
        final = MathTex(
            r"E_A = \frac{1}{1 + 10^{\frac{R_B - R_A}{400}}}",
            font_size=48
        )
        final.shift(UP * 1)
        
        self.play(Transform(step1, final), run_time=1.5)
        self.wait(1)
        
        # Add color coding
        final_colored = MathTex(
            r"E_A", r"=", r"\frac{1}{1 + 10^{\frac{", r"R_B", r"-", r"R_A", r"}{400}}}",
            font_size=48
        )
        final_colored[0].set_color(LIGHT_BLUE)
        final_colored[3].set_color(ORANGE)
        final_colored[5].set_color(TEAL)
        final_colored.shift(UP * 1)
        
        self.play(Transform(step1, final_colored), run_time=1)
        self.wait(1)
        
        # Intuitive explanation
        intuition = VGroup(
            Text("If ", font_size=26, color=WHITE),
            MathTex("R_A > R_B", font_size=28).set_color(TEAL),
            Text(": Exponent is negative → Value < 1 → E_A > 0.5", font_size=26, color=WHITE),
        )
        intuition.arrange(RIGHT, buff=0.1)
        intuition.shift(DOWN * 0.5)
        
        intuition2 = VGroup(
            Text("If ", font_size=26, color=WHITE),
            MathTex("R_A < R_B", font_size=28).set_color(ORANGE),
            Text(": Exponent is positive → Value > 1 → E_A < 0.5", font_size=26, color=WHITE),
        )
        intuition2.arrange(RIGHT, buff=0.1)
        intuition2.shift(DOWN * 1.2)
        
        intuition3 = VGroup(
            Text("If ", font_size=26, color=WHITE),
            MathTex("R_A = R_B", font_size=28).set_color(YELLOW),
            Text(": Exponent is zero → Value = 1 → E_A = 0.5", font_size=26, color=WHITE),
        )
        intuition3.arrange(RIGHT, buff=0.1)
        intuition3.shift(DOWN * 1.9)
        
        self.play(Write(intuition), run_time=1)
        self.play(Write(intuition2), run_time=1)
        self.play(Write(intuition3), run_time=1)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class SigmoidVisualization(Scene):
    """Create an interactive sigmoid curve visualization."""
    
    def construct(self):
        title = Text("The Sigmoid Curve", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Create axes
        axes = Axes(
            x_range=[-800, 800, 200],
            y_range=[0, 1, 0.25],
            x_length=10,
            y_length=4.5,
            axis_config={
                "color": GREY,
                "include_tip": False,
                "include_numbers": True,
                "font_size": 20,
            },
            x_axis_config={"numbers_to_include": [-800, -400, 0, 400, 800]},
            y_axis_config={"numbers_to_include": [0, 0.25, 0.5, 0.75, 1.0]},
        )
        axes.shift(DOWN * 0.3)
        
        x_label = Text("Rating Difference (R_A - R_B)", font_size=18, color=GREY)
        x_label.next_to(axes, DOWN, buff=0.3)
        
        y_label = Text("P(A wins)", font_size=18, color=GREY)
        y_label.next_to(axes, LEFT, buff=0.3).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
        
        # Sigmoid function for ELO
        def elo_prob(delta_r):
            return 1 / (1 + 10 ** (-delta_r / 400))
        
        # Draw the curve
        graph = axes.plot(
            elo_prob,
            x_range=[-800, 800],
            color=LIGHT_BLUE,
            stroke_width=4
        )
        
        self.play(Create(graph), run_time=2)
        self.wait(0.5)
        
        # Key points
        points_data = [
            (0, "Equal Skill\nP = 50%", YELLOW, UP),
            (200, "P = 76%", ELO_POSITIVE, UP),
            (400, "P = 91%", ELO_POSITIVE, UP + RIGHT),
            (-200, "P = 24%", ELO_NEGATIVE, DOWN),
            (-400, "P = 9%", ELO_NEGATIVE, DOWN + LEFT),
        ]
        
        dots = VGroup()
        labels = VGroup()
        
        for delta_r, label_text, color, direction in points_data:
            y_val = elo_prob(delta_r)
            dot = Dot(axes.c2p(delta_r, y_val), color=color, radius=0.08)
            label = Text(label_text, font_size=14, color=color)
            label.next_to(dot, direction, buff=0.1)
            dots.add(dot)
            labels.add(label)
        
        self.play(Create(dots[0]), Write(labels[0]), run_time=0.8)
        self.wait(0.5)
        
        for i in range(1, len(dots)):
            self.play(Create(dots[i]), Write(labels[i]), run_time=0.5)
        
        self.wait(2)
        
        # Highlight the S-shape meaning
        explanation = Text(
            "The 'S' shape ensures smooth probability transitions",
            font_size=24, color=WHITE
        )
        explanation.to_edge(DOWN).shift(UP * 0.3)
        
        self.play(Write(explanation), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class KFactorExplained(Scene):
    """Explain the K-factor in detail."""
    
    def construct(self):
        title = Text("The K-Factor: Volatility Control", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # The update formula
        formula = MathTex(
            r"R'_A = R_A + ", r"K", r"(S_A - E_A)",
            font_size=44
        )
        formula[1].set_color(ORANGE)
        formula.shift(UP * 1.5)
        
        self.play(Write(formula), run_time=1.5)
        
        # Highlight K
        k_box = SurroundingRectangle(formula[1], color=ORANGE, buff=0.1)
        self.play(Create(k_box), run_time=0.5)
        
        # What is K?
        k_explanation = VGroup(
            Text("K controls how much ratings change per game", font_size=26, color=WHITE),
            Text("Higher K = More volatile ratings", font_size=24, color=ELO_POSITIVE),
            Text("Lower K = More stable ratings", font_size=24, color=LIGHT_BLUE),
        )
        k_explanation.arrange(DOWN, buff=0.2)
        k_explanation.shift(UP * 0)
        
        self.play(Write(k_explanation), run_time=1.5)
        self.wait(1)
        
        # Common K values
        k_values = VGroup(
            Text("Common K Values:", font_size=28, color=GOLD),
            Text("• FIDE Chess (GM): K = 10 (very stable)", font_size=22, color=GREY),
            Text("• FIDE Chess (new players): K = 40 (volatile)", font_size=22, color=GREY),
            Text("• Most online games: K = 24-32", font_size=22, color=GREY),
        )
        k_values.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        k_values.shift(DOWN * 1.5)
        
        self.play(Write(k_values), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RatingUpdateExample(Scene):
    """Concrete example of rating update calculation."""
    
    def construct(self):
        title = Text("A Complete Example", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Scenario setup
        scenario = VGroup(
            Text("Player A: Rating = 1600", font_size=28, color=TEAL),
            Text("Player B: Rating = 1400", font_size=28, color=ORANGE),
            Text("K = 24", font_size=28, color=YELLOW),
        )
        scenario.arrange(DOWN, buff=0.2)
        scenario.shift(UP * 1.5 + LEFT * 3)
        
        self.play(Write(scenario), run_time=1.5)
        self.wait(0.5)
        
        # Step 1: Calculate expected score
        step1_title = Text("Step 1: Expected Score", font_size=24, color=GOLD)
        step1_title.shift(UP * 0.3 + RIGHT * 2)
        
        step1 = MathTex(
            r"E_A = \frac{1}{1 + 10^{\frac{1400 - 1600}{400}}}",
            font_size=32
        )
        step1.next_to(step1_title, DOWN, buff=0.2)
        
        step1_simplified = MathTex(
            r"E_A = \frac{1}{1 + 10^{-0.5}} = \frac{1}{1 + 0.316}",
            font_size=32
        )
        step1_simplified.next_to(step1, DOWN, buff=0.15)
        
        step1_result = MathTex(
            r"E_A = 0.76",
            font_size=36, color=ELO_POSITIVE
        )
        step1_result.next_to(step1_simplified, DOWN, buff=0.15)
        
        self.play(Write(step1_title), run_time=0.5)
        self.play(Write(step1), run_time=1)
        self.play(Write(step1_simplified), run_time=1)
        self.play(Write(step1_result), run_time=0.8)
        
        interpretation = Text("A is expected to win 76% of the time", font_size=20, color=GREY)
        interpretation.next_to(step1_result, DOWN, buff=0.1)
        self.play(Write(interpretation), run_time=1)
        
        self.wait(1)
        
        # Clear for step 2
        self.play(
            FadeOut(step1_title), FadeOut(step1), 
            FadeOut(step1_simplified), FadeOut(step1_result),
            FadeOut(interpretation)
        )
        
        # Step 2: A wins
        result_text = Text("Result: A wins! (S_A = 1)", font_size=28, color=ELO_POSITIVE)
        result_text.shift(RIGHT * 2 + UP * 0.5)
        
        self.play(Write(result_text), run_time=1)
        
        # Step 3: Update
        step3_title = Text("Step 2: Update Rating", font_size=24, color=GOLD)
        step3_title.shift(DOWN * 0.3 + RIGHT * 2)
        
        step3 = MathTex(
            r"R'_A = 1600 + 24(1 - 0.76)",
            font_size=32
        )
        step3.next_to(step3_title, DOWN, buff=0.2)
        
        step3_calc = MathTex(
            r"R'_A = 1600 + 24(0.24)",
            font_size=32
        )
        step3_calc.next_to(step3, DOWN, buff=0.15)
        
        step3_result = MathTex(
            r"R'_A = 1600 + 5.76 = 1606",
            font_size=36, color=ELO_POSITIVE
        )
        step3_result.next_to(step3_calc, DOWN, buff=0.15)
        
        self.play(Write(step3_title), run_time=0.5)
        self.play(Write(step3), run_time=1)
        self.play(Write(step3_calc), run_time=1)
        self.play(Write(step3_result), run_time=1)
        
        self.wait(1)
        
        # Key insight
        insight_box = RoundedRectangle(
            corner_radius=0.1, width=8, height=1.2,
            fill_color=DARK_BG, fill_opacity=0.9,
            stroke_color=TEAL, stroke_width=2
        )
        insight_box.to_edge(DOWN).shift(UP * 0.5)
        
        insight_text = Text(
            "A gained only 6 points because the win was EXPECTED",
            font_size=24, color=WHITE
        )
        insight_text.move_to(insight_box.get_center())
        
        self.play(Create(insight_box), Write(insight_text), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class UpsetScenario(Scene):
    """Show what happens in an upset."""
    
    def construct(self):
        title = Text("The Upset: When Underdogs Win", font_size=40, color=ORANGE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Same scenario, but B wins
        scenario = VGroup(
            Text("Player A: Rating = 1600 (favorite)", font_size=26, color=TEAL),
            Text("Player B: Rating = 1400 (underdog)", font_size=26, color=ORANGE),
            Text("Expected: E_A = 0.76, E_B = 0.24", font_size=24, color=GREY),
        )
        scenario.arrange(DOWN, buff=0.2)
        scenario.shift(UP * 1.5)
        
        self.play(Write(scenario), run_time=1.5)
        
        # B wins!
        result = Text("BUT B WINS!", font_size=44, color=ORANGE)
        result.shift(UP * 0)
        
        self.play(Write(result), run_time=1)
        self.wait(0.5)
        
        # Calculations
        calc = VGroup(
            MathTex(r"R'_B = 1400 + 24(1 - 0.24)", font_size=30),
            MathTex(r"R'_B = 1400 + 24(0.76)", font_size=30),
            MathTex(r"R'_B = 1400 + 18.2 = 1418", font_size=34, color=ELO_POSITIVE),
        )
        calc.arrange(DOWN, buff=0.15)
        calc.shift(DOWN * 1)
        
        self.play(Write(calc[0]), run_time=0.8)
        self.play(Write(calc[1]), run_time=0.8)
        self.play(Write(calc[2]), run_time=1)
        
        self.wait(1)
        
        # Comparison box
        comparison = VGroup(
            Text("Expected win: +6 points", font_size=24, color=GREY),
            Text("Upset win: +18 points", font_size=24, color=ELO_POSITIVE),
        )
        comparison.arrange(DOWN, buff=0.1)
        comparison.to_edge(DOWN).shift(UP * 0.8)
        
        box = SurroundingRectangle(comparison, color=YELLOW, buff=0.2)
        
        self.play(Write(comparison), Create(box), run_time=1.5)
        
        insight = Text(
            "Surprising results create bigger rating changes!",
            font_size=26, color=YELLOW
        )
        insight.to_edge(DOWN).shift(UP * 0.2)
        
        self.play(Write(insight), run_time=1)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class EloMathConclusion(Scene):
    """Conclude the math section and transition to F1."""
    
    def construct(self):
        title = Text("The Elegant Mathematics of ELO", font_size=44, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.5)
        
        self.play(Write(title), run_time=1)
        
        # Summary
        summary = VGroup(
            Text("✓ Expected Score: Probability based on rating difference", font_size=24, color=TEAL),
            Text("✓ Sigmoid Curve: Smooth S-shaped probability function", font_size=24, color=TEAL),
            Text("✓ K-Factor: Controls how quickly ratings change", font_size=24, color=TEAL),
            Text("✓ Update Rule: Gain when exceeding expectations", font_size=24, color=TEAL),
        )
        summary.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.center()
        
        for line in summary:
            self.play(Write(line), run_time=0.8)
        
        self.wait(1)
        
        # But...
        but_text = Text(
            "This works perfectly for SYMMETRIC games...",
            font_size=32, color=WHITE
        )
        but_text.shift(DOWN * 1.5)
        
        self.play(Write(but_text), run_time=1.5)
        self.wait(1)
        
        question = Text(
            "But what about Formula 1?",
            font_size=36, color=ORANGE
        )
        question.shift(DOWN * 2.3)
        
        self.play(Write(question), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        next_title = Text("Next: The F1 Paradox", font_size=48, color=RED)
        self.play(Write(next_title), run_time=1)
        self.wait(1)
        self.play(FadeOut(next_title))


if __name__ == "__main__":
    pass
