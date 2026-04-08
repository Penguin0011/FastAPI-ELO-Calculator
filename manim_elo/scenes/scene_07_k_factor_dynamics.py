"""
Scene 7: K-Factor Dynamics
Explains the context-aware volatility factors in the model.

This scene covers:
- Teammate Isolation (50% weighting)
- Golden Era Multiplier
- Season Length Normalization
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.formulas import *


class KFactorIntro(Scene):
    """Introduction to dynamic K-factor."""
    
    def construct(self):
        title = Text("Dynamic K-Factor", font_size=48, color=GOLD)
        subtitle = Text("Context-Aware Volatility", font_size=28, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(1)
        
        # Question
        question = Text(
            "How fast should ratings change?",
            font_size=32, color=LIGHT_BLUE
        )
        question.shift(DOWN * 1)
        
        self.play(Write(question), run_time=1.5)
        self.wait(1)
        
        answer = Text(
            "It depends on the CONTEXT!",
            font_size=32, color=ORANGE
        )
        answer.shift(DOWN * 2)
        
        self.play(Write(answer), run_time=1)
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(question), FadeOut(answer))


class TeammateIsolation(Scene):
    """Explain the teammate isolation concept."""
    
    def construct(self):
        title = Text("1. Teammate Isolation", font_size=40, color=TEAL)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # The insight
        insight = Text(
            "The ONLY fair comparison in F1 is your teammate",
            font_size=28, color=WHITE
        )
        insight.shift(UP * 1.5)
        
        self.play(Write(insight), run_time=1.5)
        
        why_box = RoundedRectangle(
            corner_radius=0.1, width=9, height=1.5,
            fill_color=DARK_BG, fill_opacity=0.8,
            stroke_color=TEAL, stroke_width=2
        )
        why_box.shift(UP * 0.3)
        
        why_text = Text(
            "Same car, same setup, same conditions\n= Perfect control group for driver skill",
            font_size=22, color=WHITE
        )
        why_text.move_to(why_box.get_center())
        
        self.play(Create(why_box), Write(why_text), run_time=1.5)
        self.wait(1)
        
        # The formula
        formula_label = Text("50% of rating from teammate battles:", font_size=24, color=GOLD)
        formula_label.shift(DOWN * 0.8)
        
        formula = MathTex(
            r"Weight_{teammate} = N_{drivers} - 2",
            font_size=40
        )
        formula.shift(DOWN * 1.5)
        
        self.play(Write(formula_label), run_time=0.8)
        self.play(Write(formula), run_time=1)
        
        # Example
        example = MathTex(
            r"\text{Grid of 20:} \quad Weight_{teammate} = 20 - 2 = 18",
            font_size=32
        )
        example.shift(DOWN * 2.3)
        
        self.play(Write(example), run_time=1)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class TeammateVisualization(Scene):
    """Visualize the 18x weighting."""
    
    def construct(self):
        title = Text("Teammate Weight Visualization", font_size=36, color=TEAL)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Grid of 20 drivers
        grid = VGroup()
        for i in range(20):
            circle = Circle(radius=0.25, stroke_width=2)
            if i == 0:  # Driver
                circle.set_color(LIGHT_BLUE)
                circle.set_fill(LIGHT_BLUE, opacity=0.5)
            elif i == 1:  # Teammate
                circle.set_color(GOLD)
                circle.set_fill(GOLD, opacity=0.5)
            else:
                circle.set_color(GREY)
                circle.set_fill(GREY, opacity=0.2)
            
            grid.add(circle)
        
        # Arrange in 4 rows
        rows = []
        for r in range(4):
            row = VGroup(*grid[r*5:(r+1)*5])
            row.arrange(RIGHT, buff=0.4)
            rows.append(row)
        
        full_grid = VGroup(*rows)
        full_grid.arrange(DOWN, buff=0.3)
        full_grid.shift(LEFT * 2)
        
        self.play(Create(full_grid), run_time=1.5)
        
        # Labels
        you_label = Text("You", font_size=16, color=LIGHT_BLUE)
        you_label.next_to(grid[0], UP, buff=0.1)
        
        tm_label = Text("Teammate", font_size=16, color=GOLD)
        tm_label.next_to(grid[1], UP, buff=0.1)
        
        self.play(Write(you_label), Write(tm_label), run_time=0.8)
        
        # Weight comparison on right
        weights = VGroup(
            Text("Teammate match:", font_size=22, color=GOLD),
            Text("Weight = 18", font_size=28, color=GOLD),
            Text("", font_size=10),
            Text("Each other opponent:", font_size=22, color=GREY),
            Text("Weight = 1", font_size=28, color=GREY),
        )
        weights.arrange(DOWN, buff=0.1)
        weights.shift(RIGHT * 3)
        
        self.play(Write(weights), run_time=1.5)
        
        # Conclusion
        conclusion = Text(
            "Your 1 teammate carries the same weight as ALL 18 other drivers combined!",
            font_size=22, color=YELLOW
        )
        conclusion.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(Write(conclusion), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class GoldenEraMultiplier(Scene):
    """Explain the grid competitiveness factor."""
    
    def construct(self):
        title = Text("2. Golden Era Multiplier", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # The insight
        insight = Text(
            "Not all grids are equal!",
            font_size=32, color=WHITE
        )
        insight.shift(UP * 1.5)
        
        self.play(Write(insight), run_time=1)
        
        # Comparison
        comparison = VGroup(
            Text("2012: 6 World Champions on the grid", font_size=24, color=GOLD),
            Text("vs", font_size=20, color=GREY),
            Text("2020: 4 World Champions on the grid", font_size=24, color=GREY),
        )
        comparison.arrange(DOWN, buff=0.15)
        comparison.shift(UP * 0.3)
        
        self.play(Write(comparison), run_time=1.5)
        
        # Formula
        formula = MathTex(
            r"K_{grid} = 1 + (0.05 \times N_{WDC})",
            font_size=40
        )
        formula.shift(DOWN * 0.8)
        
        self.play(Write(formula), run_time=1)
        
        # Examples
        examples = VGroup(
            MathTex(r"\text{2012: } K_{grid} = 1 + (0.05 \times 6) = 1.30", font_size=28, color=GOLD),
            MathTex(r"\text{2020: } K_{grid} = 1 + (0.05 \times 4) = 1.20", font_size=28, color=GREY),
        )
        examples.arrange(DOWN, buff=0.2)
        examples.shift(DOWN * 2)
        
        self.play(Write(examples), run_time=1.5)
        
        # Meaning
        meaning = Text(
            "A win in 2012 is worth 30% more than a win in a 'thin' year",
            font_size=22, color=YELLOW
        )
        meaning.to_edge(DOWN).shift(UP * 0.3)
        
        self.play(Write(meaning), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class SeasonNormalization(Scene):
    """Explain season length normalization."""
    
    def construct(self):
        title = Text("3. Season Length Normalization", font_size=40, color=ORANGE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # The problem
        problem = Text(
            "Modern seasons have MORE races",
            font_size=28, color=WHITE
        )
        problem.shift(UP * 1.5)
        
        self.play(Write(problem), run_time=1)
        
        # Timeline
        timeline = VGroup(
            Text("1980s: ~16 races/season", font_size=24, color=GREY),
            Text("2000s: ~18 races/season", font_size=24, color=GREY),
            Text("2024: 24 races/season", font_size=24, color=ORANGE),
        )
        timeline.arrange(DOWN, buff=0.2)
        timeline.shift(UP * 0.3)
        
        self.play(Write(timeline), run_time=1.5)
        
        # The bias
        bias = Text(
            "Without correction: Modern drivers accumulate stats faster!",
            font_size=24, color=RED
        )
        bias.shift(DOWN * 0.8)
        
        self.play(Write(bias), run_time=1)
        
        # Solution formula
        solution = MathTex(
            r"K_{season} = \frac{20}{N_{races}}",
            font_size=44
        )
        solution.shift(DOWN * 1.8)
        
        self.play(Write(solution), run_time=1)
        
        # Examples
        examples = VGroup(
            Text("1985 (16 races): K_season = 20/16 = 1.25 (worth MORE)", font_size=20, color=ELO_POSITIVE),
            Text("2024 (24 races): K_season = 20/24 = 0.83 (worth LESS)", font_size=20, color=ELO_NEGATIVE),
        )
        examples.arrange(DOWN, buff=0.1)
        examples.shift(DOWN * 2.8)
        
        self.play(Write(examples), run_time=1.5)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class CombinedKFactor(Scene):
    """Show the complete K-factor formula."""
    
    def construct(self):
        title = Text("The Complete K-Factor", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # The components
        components = VGroup(
            MathTex(r"K_{base}", r"= 24", font_size=32).set_color_by_tex("K_{base}", WHITE),
            MathTex(r"K_{grid}", r"= 1 + 0.05 \times N_{WDC}", font_size=32).set_color_by_tex("K_{grid}", GOLD),
            MathTex(r"W_{tm}", r"= N_{drivers} - 2", font_size=32).set_color_by_tex("W_{tm}", TEAL),
            MathTex(r"K_{season}", r"= \frac{20}{N_{races}}", font_size=32).set_color_by_tex("K_{season}", ORANGE),
        )
        components.arrange(DOWN, buff=0.25)
        components.shift(UP * 0.8)
        
        for comp in components:
            self.play(Write(comp), run_time=0.8)
        
        self.wait(1)
        
        # Combined formula
        combined_label = Text("Combined:", font_size=24, color=YELLOW)
        combined_label.shift(DOWN * 0.8)
        
        combined = MathTex(
            r"K_{final} = K_{base} \times K_{grid} \times W_{tm} \times K_{season}",
            font_size=36
        )
        combined.shift(DOWN * 1.5)
        
        self.play(Write(combined_label), run_time=0.5)
        self.play(Write(combined), run_time=1.5)
        
        # Box around it
        box = SurroundingRectangle(combined, color=YELLOW, buff=0.2)
        self.play(Create(box), run_time=0.5)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class KFactorConclusion(Scene):
    """Summary and transition."""
    
    def construct(self):
        title = Text("K-Factor: Summary", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.5)
        
        self.play(Write(title), run_time=1)
        
        summary = VGroup(
            Text("✓ Teammate battles weighted 18x (50% of total)", font_size=24, color=TEAL),
            Text("✓ Champion-dense grids increase volatility", font_size=24, color=TEAL),
            Text("✓ Season length normalizes era comparisons", font_size=24, color=TEAL),
        )
        summary.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.center()
        
        for line in summary:
            self.play(Write(line), run_time=0.7)
        
        self.wait(1)
        
        transition = Text(
            "But can we reward driving STYLE?",
            font_size=28, color=ORANGE
        )
        transition.shift(DOWN * 1.5)
        
        self.play(Write(transition), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        next_title = Text("Next: Physics-Based Features", font_size=48, color=LIGHT_BLUE)
        self.play(Write(next_title), run_time=1)
        self.wait(1)
        self.play(FadeOut(next_title))


if __name__ == "__main__":
    pass
