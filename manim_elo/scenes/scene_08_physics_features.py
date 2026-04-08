"""
Scene 8: Physics-Based Features
Explains telemetry-derived bonuses for driving style.
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.colors import *


class PhysicsIntro(Scene):
    def construct(self):
        title = Text("Physics-Based Features", font_size=48, color=LIGHT_BLUE)
        subtitle = Text("Rewarding Driving Style", font_size=28, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        
        insight = VGroup(
            Text("Results tell us WHAT happened", font_size=28, color=WHITE),
            Text("Telemetry tells us HOW it happened", font_size=28, color=GOLD),
        )
        insight.arrange(DOWN, buff=0.2).shift(DOWN)
        self.play(Write(insight), run_time=2)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class BrakingAggression(Scene):
    def construct(self):
        title = Text("1. Braking Aggression", font_size=40, color=ORANGE)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(title), run_time=1)
        
        formula = MathTex(r"a(t) = \frac{\Delta v}{\Delta t}", font_size=44)
        formula.shift(UP * 0.5)
        self.play(Write(formula), run_time=1)
        
        thresholds = VGroup(
            Text("Standard: ~4.0g", font_size=24, color=GREY),
            Text("Elite: >5.0g → 1.2x bonus", font_size=24, color=ORANGE),
            Text("\"Honey Badger\": >5.5g → 1.5x bonus", font_size=24, color=PINK),
        )
        thresholds.arrange(DOWN, buff=0.2).shift(DOWN)
        self.play(Write(thresholds), run_time=2)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class CarryJobGradient(Scene):
    def construct(self):
        title = Text("2. The 'Carry Job' Gradient", font_size=40, color=TEAL)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(title), run_time=1)
        
        formula = MathTex(
            r"Bonus = 1 + \frac{R_{driver} - R_{car}}{1000}",
            font_size=40
        )
        self.play(Write(formula), run_time=1.5)
        
        example = MathTex(
            r"\text{Driver 1600, Car 1400:} \quad Bonus = 1.2",
            font_size=32, color=ELO_POSITIVE
        )
        example.shift(DOWN * 1.2)
        self.play(Write(example), run_time=1)
        
        insight = Text("Outperforming machinery = extra reward", font_size=24, color=YELLOW)
        insight.shift(DOWN * 2.2)
        self.play(Write(insight), run_time=1)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


if __name__ == "__main__":
    pass
