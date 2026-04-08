"""
Scene 6: Composite Effective Strength
Explains how the Bayesian model combines driver and car ratings.

This scene covers:
- R_effective = R_driver + R_car
- The modified probability formula
- The handicap system effect
- Visual demonstrations
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.formulas import *


class CompositeIntro(Scene):
    """Introduction to composite rating concept."""
    
    def construct(self):
        title = Text("Separating Man from Machine", font_size=48, color=LIGHT_BLUE)
        subtitle = Text("The Core Innovation", font_size=28, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(subtitle))


class TwoRatings(Scene):
    """Show that we track TWO ratings."""
    
    def construct(self):
        title = Text("Two Separate Ratings", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Driver rating explanation
        driver_box = RoundedRectangle(
            corner_radius=0.15, width=5, height=2.5,
            fill_color=TEAL, fill_opacity=0.15,
            stroke_color=TEAL, stroke_width=3
        )
        driver_box.shift(LEFT * 3)
        
        driver_title = Text("Driver Rating", font_size=28, color=TEAL)
        driver_title.move_to(driver_box.get_center() + UP * 0.7)
        
        driver_symbol = MathTex(r"R_{driver}", font_size=48, color=TEAL)
        driver_symbol.move_to(driver_box.get_center())
        
        driver_desc = Text("Pure driving skill\nreaction, racecraft, consistency", 
                          font_size=16, color=GREY)
        driver_desc.move_to(driver_box.get_center() + DOWN * 0.7)
        
        driver_group = VGroup(driver_box, driver_title, driver_symbol, driver_desc)
        
        # Car rating explanation
        car_box = RoundedRectangle(
            corner_radius=0.15, width=5, height=2.5,
            fill_color=ORANGE, fill_opacity=0.15,
            stroke_color=ORANGE, stroke_width=3
        )
        car_box.shift(RIGHT * 3)
        
        car_title = Text("Car Rating", font_size=28, color=ORANGE)
        car_title.move_to(car_box.get_center() + UP * 0.7)
        
        car_symbol = MathTex(r"R_{car}", font_size=48, color=ORANGE)
        car_symbol.move_to(car_box.get_center())
        
        car_desc = Text("Car performance\npower unit, aero, reliability", 
                       font_size=16, color=GREY)
        car_desc.move_to(car_box.get_center() + DOWN * 0.7)
        
        car_group = VGroup(car_box, car_title, car_symbol, car_desc)
        
        self.play(FadeIn(driver_group), run_time=1)
        self.play(FadeIn(car_group), run_time=1)
        
        self.wait(1)
        
        # Key insight
        insight = Text(
            "Unlike standard ELO, we model both separately!",
            font_size=26, color=YELLOW
        )
        insight.shift(DOWN * 2.3)
        
        self.play(Write(insight), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class CompositeFormula(Scene):
    """Present the composite strength formula."""
    
    def construct(self):
        title = Text("Composite Effective Strength", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Build the formula
        we_define = Text("We define:", font_size=26, color=GREY)
        we_define.shift(UP * 1.5)
        
        formula = MathTex(
            r"R_{effective}", r"=", r"R_{driver}", r"+", r"R_{car}",
            font_size=52
        )
        formula[0].set_color(PURPLE)
        formula[2].set_color(TEAL)
        formula[4].set_color(ORANGE)
        formula.shift(UP * 0.5)
        
        self.play(Write(we_define), run_time=0.5)
        self.play(Write(formula), run_time=2)
        self.wait(1)
        
        # Example calculation
        example_title = Text("Example:", font_size=24, color=GOLD)
        example_title.shift(DOWN * 0.5)
        
        example = VGroup(
            MathTex(r"R_{driver} = 1700", font_size=28, color=TEAL),
            MathTex(r"R_{car} = 1850", font_size=28, color=ORANGE),
            MathTex(r"R_{effective} = 1700 + 1850 = 3550", font_size=28, color=PURPLE),
        )
        example.arrange(DOWN, buff=0.15)
        example.shift(DOWN * 1.5)
        
        self.play(Write(example_title), run_time=0.5)
        for line in example:
            self.play(Write(line), run_time=0.8)
        
        self.wait(1)
        
        # Interpretation
        interp = Text(
            "This represents their TOTAL package on track",
            font_size=24, color=WHITE
        )
        interp.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(Write(interp), run_time=1)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class ModifiedProbability(Scene):
    """Show the modified probability formula."""
    
    def construct(self):
        title = Text("Modified Probability Formula", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Standard ELO
        standard_label = Text("Standard ELO:", font_size=24, color=GREY)
        standard_label.shift(UP * 1.5 + LEFT * 3)
        
        standard_formula = MathTex(
            r"P(A > B) = \frac{1}{1 + 10^{\frac{R_B - R_A}{400}}}",
            font_size=32
        )
        standard_formula.shift(UP * 0.8)
        
        self.play(Write(standard_label), Write(standard_formula), run_time=1.5)
        
        # Arrow down
        arrow = Arrow(UP * 0.3, DOWN * 0.3, color=YELLOW)
        transform_text = Text("Becomes", font_size=20, color=YELLOW)
        transform_text.next_to(arrow, RIGHT, buff=0.2)
        
        self.play(GrowArrow(arrow), Write(transform_text), run_time=0.8)
        
        # New formula
        new_label = Text("Bayesian F1 Model:", font_size=24, color=LIGHT_BLUE)
        new_label.shift(DOWN * 0.8 + LEFT * 3)
        
        new_formula = MathTex(
            r"P(A > B) = \frac{1}{1 + 10^{\frac{(R_{d_B} + R_{c_B}) - (R_{d_A} + R_{c_A})}{400}}}",
            font_size=28
        )
        new_formula.shift(DOWN * 1.5)
        
        self.play(Write(new_label), run_time=0.5)
        self.play(Write(new_formula), run_time=2)
        
        self.wait(1)
        
        # Simplified version
        simple = MathTex(
            r"P(A > B) = \frac{1}{1 + 10^{\frac{Package_B - Package_A}{400}}}",
            font_size=32, color=WHITE
        )
        simple.shift(DOWN * 2.5)
        
        self.play(Write(simple), run_time=1.5)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class HandicapVisualization(Scene):
    """Visualize the handicap effect."""
    
    def construct(self):
        title = Text("The Handicap Effect", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Driver A in dominant car
        driver_a_bar = self.create_stacked_bar("Driver A", 1600, 1900, LEFT * 3)
        driver_a_label = Text("Max @ Red Bull", font_size=20, color=GREY)
        driver_a_label.next_to(driver_a_bar, DOWN, buff=0.2)
        
        # Driver B in slower car
        driver_b_bar = self.create_stacked_bar("Driver B", 1550, 1300, RIGHT * 3)
        driver_b_label = Text("Lando @ McLaren (2022)", font_size=20, color=GREY)
        driver_b_label.next_to(driver_b_bar, DOWN, buff=0.2)
        
        self.play(
            FadeIn(driver_a_bar), Write(driver_a_label),
            FadeIn(driver_b_bar), Write(driver_b_label),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Totals
        total_a = Text("Total: 3500", font_size=24, color=PURPLE)
        total_a.next_to(driver_a_bar, UP, buff=0.3)
        
        total_b = Text("Total: 2850", font_size=24, color=PURPLE)
        total_b.next_to(driver_b_bar, UP, buff=0.3)
        
        self.play(Write(total_a), Write(total_b), run_time=0.8)
        
        # The implication
        implication = VGroup(
            Text("If Driver A wins:", font_size=24, color=WHITE),
            Text("\"Expected! Car advantage was huge\"", font_size=22, color=ELO_NEUTRAL),
            Text("→ Minimal rating gain", font_size=22, color=GREY),
        )
        implication.arrange(DOWN, buff=0.1)
        implication.shift(DOWN * 2.3)
        
        self.play(Write(implication), run_time=1.5)
        self.wait(1)
        
        # Other case
        self.play(FadeOut(implication))
        
        implication2 = VGroup(
            Text("If Driver B wins:", font_size=24, color=WHITE),
            Text("\"Incredible! Overcame a 650 point package deficit!\"", font_size=22, color=ELO_POSITIVE),
            Text("→ Massive rating gain", font_size=22, color=TEAL),
        )
        implication2.arrange(DOWN, buff=0.1)
        implication2.shift(DOWN * 2.3)
        
        self.play(Write(implication2), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def create_stacked_bar(self, label, driver_rating, car_rating, position):
        """Create a stacked bar showing driver + car."""
        # Scale factor for visualization
        scale = 0.002
        
        # Driver portion (bottom)
        driver_height = driver_rating * scale
        driver_bar = Rectangle(
            width=1.5, height=driver_height,
            fill_color=TEAL, fill_opacity=0.7,
            stroke_color=TEAL, stroke_width=2
        )
        
        # Car portion (top)
        car_height = car_rating * scale
        car_bar = Rectangle(
            width=1.5, height=car_height,
            fill_color=ORANGE, fill_opacity=0.7,
            stroke_color=ORANGE, stroke_width=2
        )
        
        # Stack them
        driver_bar.move_to(position + DOWN * car_height/2)
        car_bar.next_to(driver_bar, UP, buff=0)
        
        # Labels inside bars
        driver_text = Text(f"Driver: {driver_rating}", font_size=14, color=WHITE)
        driver_text.move_to(driver_bar.get_center())
        
        car_text = Text(f"Car: {car_rating}", font_size=14, color=WHITE)
        car_text.move_to(car_bar.get_center())
        
        return VGroup(driver_bar, car_bar, driver_text, car_text)


class HandicapInsight(Scene):
    """Key insight about the handicap system."""
    
    def construct(self):
        title = Text("The Key Insight", font_size=44, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.5)
        
        self.play(Write(title), run_time=1)
        
        # Main points
        points = VGroup(
            Text("If you're in a dominant car:", font_size=28, color=ORANGE),
            Text("• You START with a massive advantage in the math", font_size=24, color=WHITE),
            Text("• Winning is EXPECTED", font_size=24, color=WHITE),
            Text("• To gain rating, you must win MORE than the car predicts", font_size=24, color=YELLOW),
        )
        points.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        points.shift(UP * 0.5)
        
        for point in points:
            self.play(Write(point), run_time=0.8)
        
        self.wait(1)
        
        # Conclusion
        conclusion_box = RoundedRectangle(
            corner_radius=0.15, width=10, height=1.5,
            fill_color=LIGHT_BLUE, fill_opacity=0.15,
            stroke_color=LIGHT_BLUE, stroke_width=2
        )
        conclusion_box.shift(DOWN * 1.8)
        
        conclusion = Text(
            "Merely winning isn't enough!\nYou must OUTPERFORM your car.",
            font_size=26, color=LIGHT_BLUE
        )
        conclusion.move_to(conclusion_box.get_center())
        
        self.play(Create(conclusion_box), Write(conclusion), run_time=1.5)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class CompositeConclusion(Scene):
    """Conclude and transition."""
    
    def construct(self):
        title = Text("Composite Strength: Summary", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.5)
        
        self.play(Write(title), run_time=1)
        
        summary = VGroup(
            Text("✓ Track Driver and Car ratings separately", font_size=24, color=TEAL),
            Text("✓ Combine them for match probability", font_size=24, color=TEAL),
            Text("✓ Car rating acts as a handicap", font_size=24, color=TEAL),
            Text("✓ True skill is isolated from machinery", font_size=24, color=TEAL),
        )
        summary.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        summary.center()
        
        for line in summary:
            self.play(Write(line), run_time=0.6)
        
        self.wait(1)
        
        next_text = Text(
            "But how fast should ratings change?",
            font_size=28, color=ORANGE
        )
        next_text.shift(DOWN * 1.5)
        
        self.play(Write(next_text), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        next_title = Text("Next: K-Factor Dynamics", font_size=48, color=LIGHT_BLUE)
        self.play(Write(next_title), run_time=1)
        self.wait(1)
        self.play(FadeOut(next_title))


if __name__ == "__main__":
    pass
