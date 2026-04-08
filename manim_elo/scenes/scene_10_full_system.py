"""
Scene 10: Complete System Overview
Final summary bringing all components together.
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.colors import *


class SystemOverviewIntro(Scene):
    def construct(self):
        title = Text("The Complete System", font_size=52, color=GOLD)
        subtitle = Text("Putting It All Together", font_size=28, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))


class SystemFlowchart(Scene):
    def construct(self):
        title = Text("System Architecture", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(title), run_time=1)
        
        # Input
        input_box = RoundedRectangle(corner_radius=0.1, width=2.5, height=1,
            fill_color=GREY, fill_opacity=0.3, stroke_color=GREY)
        input_box.shift(LEFT * 4.5)
        input_text = Text("Race Result", font_size=18, color=WHITE)
        input_text.move_to(input_box)
        
        # Processing stages
        stages = [
            ("Composite\nStrength", TEAL),
            ("K-Factor\nDynamics", ORANGE),
            ("Physics\nBonuses", PINK),
            ("DNF\nHandling", RED),
        ]
        
        boxes = VGroup()
        prev = input_box
        for i, (label, color) in enumerate(stages):
            box = RoundedRectangle(corner_radius=0.1, width=2, height=1,
                fill_color=color, fill_opacity=0.2, stroke_color=color)
            box.next_to(prev, RIGHT, buff=0.3)
            text = Text(label, font_size=14, color=color)
            text.move_to(box)
            boxes.add(VGroup(box, text))
            prev = box
        
        # Output
        output_box = RoundedRectangle(corner_radius=0.1, width=2.5, height=1,
            fill_color=GOLD, fill_opacity=0.3, stroke_color=GOLD)
        output_box.next_to(prev, RIGHT, buff=0.3)
        output_text = Text("Updated\nRatings", font_size=18, color=GOLD)
        output_text.move_to(output_box)
        
        # Animate
        self.play(Create(input_box), Write(input_text), run_time=0.8)
        for box in boxes:
            arrow = Arrow(box.get_left() + LEFT * 0.3, box.get_left(), 
                         color=WHITE, stroke_width=2, buff=0)
            self.play(Create(arrow), FadeIn(box), run_time=0.5)
        
        arrow = Arrow(output_box.get_left() + LEFT * 0.3, output_box.get_left(),
                     color=WHITE, stroke_width=2, buff=0)
        self.play(Create(arrow), Create(output_box), Write(output_text), run_time=0.8)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class FinalFormula(Scene):
    def construct(self):
        title = Text("The Final Update Equation", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(title), run_time=1)
        
        formula = MathTex(
            r"R'_{driver} = R_{driver} + K_{final} \cdot \sum_{opponents} (S - E)",
            font_size=36
        )
        formula.shift(UP * 0.5)
        self.play(Write(formula), run_time=2)
        
        where = VGroup(
            Text("Where:", font_size=22, color=GREY),
            MathTex(r"K_{final} = K_{base} \times K_{grid} \times W_{tm} \times K_{season} \times Bonuses", font_size=24),
            MathTex(r"E = \frac{1}{1 + 10^{(Package_B - Package_A)/400}}", font_size=24),
        )
        where.arrange(DOWN, buff=0.2)
        where.shift(DOWN * 1)
        self.play(Write(where), run_time=2)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class WhatItAchieves(Scene):
    def construct(self):
        title = Text("What This Achieves", font_size=44, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(title), run_time=1)
        
        conclusion = Text(
            "Predicts who would win if everyone drove the same car",
            font_size=28, color=GOLD
        )
        conclusion.shift(UP * 0.5)
        
        box = SurroundingRectangle(conclusion, color=GOLD, buff=0.2)
        self.play(Write(conclusion), Create(box), run_time=2)
        
        benefits = VGroup(
            Text("✓ Separates driver skill from car performance", font_size=24, color=TEAL),
            Text("✓ Accounts for grid competitiveness", font_size=24, color=TEAL),
            Text("✓ Rewards driving style with telemetry", font_size=24, color=TEAL),
            Text("✓ Protects ratings from mechanical failures", font_size=24, color=TEAL),
        )
        benefits.arrange(DOWN, buff=0.25).shift(DOWN * 1.3)
        
        for benefit in benefits:
            self.play(Write(benefit), run_time=0.7)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class Conclusion(Scene):
    def construct(self):
        # Final message
        thanks = Text("The Bayesian F1 Engine", font_size=52, color=GOLD)
        self.play(Write(thanks), run_time=2)
        self.wait(1)
        
        subtitle = Text(
            "From Chess to Facemash to Formula 1",
            font_size=28, color=GREY
        )
        subtitle.next_to(thanks, DOWN, buff=0.5)
        self.play(FadeIn(subtitle), run_time=1)
        
        self.wait(3)
        self.play(FadeOut(thanks), FadeOut(subtitle))


if __name__ == "__main__":
    pass
