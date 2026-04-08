"""
Scene 9: DNF Handling - The Robbery Protocol
Explains how mechanical DNFs are handled asymmetrically.
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.colors import *


class DNFIntro(Scene):
    def construct(self):
        title = Text("The 'Robbery' Protocol", font_size=48, color=RED)
        subtitle = Text("Handling Mechanical Failures", font_size=28, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))


class DNFProblem(Scene):
    def construct(self):
        title = Text("The Problem with DNFs", font_size=40, color=ORANGE)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(title), run_time=1)
        
        # Standard approach
        standard = VGroup(
            Text("Standard ELO:", font_size=28, color=GREY),
            Text("DNF = Loss = Rating drops", font_size=26, color=RED),
        )
        standard.arrange(DOWN, buff=0.1).shift(UP)
        self.play(Write(standard), run_time=1.5)
        
        # Our insight
        insight = VGroup(
            Text("Our Model:", font_size=28, color=TEAL),
            Text("Mechanical DNF ≠ Loss", font_size=26, color=WHITE),
            Text("Mechanical DNF = Information Loss", font_size=26, color=GOLD),
        )
        insight.arrange(DOWN, buff=0.1).shift(DOWN)
        self.play(Write(insight), run_time=2)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RobberyProtocol(Scene):
    def construct(self):
        title = Text("The Robbery Protocol", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(title), run_time=1)
        
        # Step 1: Voiding
        step1 = VGroup(
            Text("1. VOIDING", font_size=28, color=TEAL),
            Text("Comparisons below are nullified", font_size=22, color=WHITE),
            Text("(You didn't lose to them - you vanished)", font_size=20, color=GREY),
        )
        step1.arrange(DOWN, buff=0.1).shift(UP * 0.8)
        self.play(Write(step1), run_time=1.5)
        
        # Step 2: Compensation
        step2 = VGroup(
            Text("2. COMPENSATION", font_size=28, color=ORANGE),
            MathTex(r"K_{mech} = 5.0 \times K_{base}", font_size=36),
            Text("500% volatility for assumed performance", font_size=20, color=GREY),
        )
        step2.arrange(DOWN, buff=0.1).shift(DOWN * 1)
        self.play(Write(step2), run_time=1.5)
        
        # Key insight
        insight = Text(
            "Peak capability is protected from mechanical misfortune",
            font_size=24, color=YELLOW
        )
        insight.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(insight), run_time=1.5)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class StolenWinExample(Scene):
    def construct(self):
        title = Text("Example: The Stolen Win", font_size=40, color=RED)
        title.to_edge(UP).shift(DOWN * 0.3)
        self.play(Write(title), run_time=1)
        
        scenario = VGroup(
            Text("Scenario: Driver leads every lap", font_size=24, color=WHITE),
            Text("Engine failure on final lap", font_size=24, color=RED),
            Text("Classified: DNF", font_size=24, color=GREY),
        )
        scenario.arrange(DOWN, buff=0.15).shift(UP * 0.5)
        self.play(Write(scenario), run_time=2)
        
        # What happens
        result = VGroup(
            Text("Standard ELO: Massive rating loss", font_size=22, color=RED),
            Text("Our Model: Rating preserved (was winning!)", font_size=22, color=ELO_POSITIVE),
        )
        result.arrange(DOWN, buff=0.2).shift(DOWN * 1.2)
        self.play(Write(result), run_time=1.5)
        
        conclusion = Text(
            "We protect peak ELO from reliability issues",
            font_size=26, color=GOLD
        )
        conclusion.shift(DOWN * 2.5)
        self.play(Write(conclusion), run_time=1)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


if __name__ == "__main__":
    pass
