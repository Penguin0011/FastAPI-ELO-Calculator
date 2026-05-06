# Section 17: Appendix Equations
# 7 Scenes animating all key formulas

from manim import *
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *


class Scene17_1_EloExpectation(Scene):
    """Scene 17.1: Elo Expected Score."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Elo Expected Score", font_size=36, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        
        formula = MathTex(
            r"E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}",
            font_size=48
        )
        formula.move_to(ORIGIN)
        
        box = SurroundingRectangle(formula, color=ELO_GOLD, buff=0.3)
        
        self.play(Write(formula), run_time=6)
        self.play(Create(box), run_time=2)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene17_2_EloUpdate(Scene):
    """Scene 17.2: Elo Update Equation."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Elo Update Equation", font_size=36, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        
        formula = MathTex(
            r"R'_A = R_A + K(S_A - E_A)",
            font_size=48
        )
        formula.move_to(ORIGIN)
        
        box = SurroundingRectangle(formula, color=ELO_GOLD, buff=0.3)
        
        self.play(Write(formula), run_time=6)
        self.play(Create(box), run_time=2)
        
        legend = VGroup(
            Text("K = adjustment factor (16-32)", font_size=18, color=TEXT_GRAY),
            Text("S = actual score (1/0.5/0)", font_size=18, color=TEXT_GRAY),
            Text("E = expected score", font_size=18, color=TEXT_GRAY)
        )
        legend.arrange(DOWN, buff=0.1)
        legend.move_to(DOWN * 2)
        
        self.play(FadeIn(legend), run_time=3.2)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene17_3_PlackettLuce(Scene):
    """Scene 17.3: Plackett-Luce Likelihood."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Plackett-Luce Likelihood", font_size=36, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        
        formula = MathTex(
            r"P(\pi) = \prod_{k=1}^{n} \frac{\exp(s_{\pi_k})}{\sum_{l=k}^{n} \exp(s_{\pi_l})}",
            font_size=44
        )
        formula.move_to(ORIGIN)
        
        box = SurroundingRectangle(formula, color=ELO_GOLD, buff=0.3)
        
        self.play(Write(formula), run_time=6)
        self.play(Create(box), run_time=2)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene17_4_BradleyTerry(Scene):
    """Scene 17.4: Bradley-Terry Model."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Bradley-Terry Model", font_size=36, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        
        formula = MathTex(
            r"P(i > j) = \frac{v_i}{v_i + v_j}",
            font_size=48
        )
        formula.move_to(ORIGIN)
        
        box = SurroundingRectangle(formula, color=ELO_GOLD, buff=0.3)
        
        self.play(Write(formula), run_time=6)
        self.play(Create(box), run_time=2)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene17_5_HierarchicalModel(Scene):
    """Scene 17.5: Hierarchical Decomposition."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Hierarchical Decomposition", font_size=36, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        
        formula = MathTex(
            r"\lambda_{ijr} = \alpha_i + \beta_j + \gamma_{ij} + \epsilon_{ijr}",
            font_size=44
        )
        formula.move_to(ORIGIN)
        
        box = SurroundingRectangle(formula, color=ELO_GOLD, buff=0.3)
        
        self.play(Write(formula), run_time=6)
        self.play(Create(box), run_time=2)
        
        legend = VGroup(
            MathTex(r"\alpha", font_size=28, color=ELO_BLUE),
            Text("= Driver", font_size=16, color=TEXT_GRAY),
            MathTex(r"\beta", font_size=28, color=ELO_GOLD),
            Text("= Car", font_size=16, color=TEXT_GRAY),
            MathTex(r"\gamma", font_size=28, color=ELO_GREEN),
            Text("= Track", font_size=16, color=TEXT_GRAY)
        )
        legend.arrange_in_grid(rows=3, cols=2, buff=(0.3, 0.15))
        legend.move_to(DOWN * 2)
        
        self.play(FadeIn(legend), run_time=3.2)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene17_6_TrueSkill(Scene):
    """Scene 17.6: TrueSkill Rating."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("TrueSkill Rating", font_size=36, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        
        formula = MathTex(
            r"R = \mu - 3\sigma",
            font_size=52
        )
        formula.move_to(ORIGIN)
        
        box = SurroundingRectangle(formula, color=ELO_GOLD, buff=0.3)
        
        self.play(Write(formula), run_time=6)
        self.play(Create(box), run_time=2)
        
        legend = VGroup(
            Text("μ = Mean skill estimate", font_size=18, color=TEXT_GRAY),
            Text("σ = Uncertainty (std dev)", font_size=18, color=TEXT_GRAY)
        )
        legend.arrange(DOWN, buff=0.1)
        legend.move_to(DOWN * 2)
        
        self.play(FadeIn(legend), run_time=3.2)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene17_7_Bayes(Scene):
    """Scene 17.7: Bayes' Theorem."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Bayes' Theorem", font_size=36, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        
        formula = MathTex(
            r"P(\theta|D) = \frac{P(D|\theta) P(\theta)}{P(D)}",
            font_size=48
        )
        formula.move_to(ORIGIN)
        
        box = SurroundingRectangle(formula, color=ELO_GOLD, buff=0.3)
        
        self.play(Write(formula), run_time=6)
        self.play(Create(box), run_time=2)
        
        # Color labels
        labels = VGroup(
            Text("Posterior", font_size=16, color=ELO_GREEN),
            Text("Likelihood", font_size=16, color=ELO_GOLD),
            Text("Prior", font_size=16, color=ELO_BLUE)
        )
        labels.arrange(RIGHT, buff=1.5)
        labels.move_to(DOWN * 2)
        
        self.play(FadeIn(labels), run_time=3.2)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)
