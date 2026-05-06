# Section 16: Conclusion
# 3 Scenes

from manim import *
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *


class Scene16_1_SystemFlowchart(Scene):
    """Scene 16.1: Complete System Flowchart."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("The Complete System", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Simplified flowchart
        input_box = Rectangle(width=2, height=0.7, fill_color=ELO_RED, fill_opacity=0.6)
        input_box.move_to(LEFT * 4 + UP * 0.5)
        input_text = Text("Race Data", font_size=14).move_to(input_box)
        
        process_box = Rectangle(width=2, height=0.7, fill_color=ELO_BLUE, fill_opacity=0.6)
        process_box.move_to(ORIGIN + UP * 0.5)
        process_text = Text("Bayesian Model", font_size=14).move_to(process_box)
        
        output_box = Rectangle(width=2, height=0.7, fill_color=ELO_GREEN, fill_opacity=0.6)
        output_box.move_to(RIGHT * 4 + UP * 0.5)
        output_text = Text("Ratings", font_size=14).move_to(output_box)
        
        arrow1 = Arrow(input_box.get_right(), process_box.get_left(), color=TEXT_GRAY, buff=0.1)
        arrow2 = Arrow(process_box.get_right(), output_box.get_left(), color=TEXT_GRAY, buff=0.1)
        
        self.play(FadeIn(VGroup(input_box, input_text, process_box, process_text, output_box, output_text)), run_time=4)
        self.play(Create(VGroup(arrow1, arrow2)), run_time=2)
        
        # Components below
        components = VGroup(
            Text("• Plackett-Luce ranking", font_size=16, color=TEXT_GRAY),
            Text("• Hierarchical α + β decomposition", font_size=16, color=TEXT_GRAY),
            Text("• MCMC inference", font_size=16, color=TEXT_GRAY),
            Text("• Glicko-2 uncertainty", font_size=16, color=TEXT_GRAY)
        )
        components.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        components.move_to(DOWN * 1.5)
        
        self.play(FadeIn(components), run_time=4)
        
        self.wait(8)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene16_2_KeyInsights(Scene):
    """Scene 16.2: Key Insights."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Key Insights", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)
        
        insights = VGroup(
            Text("1. Skill is latent — observe noisy performance", font_size=20, color=TEXT_LIGHT),
            Text("2. Linear models fail at extremes -> Use probability", font_size=20, color=TEXT_LIGHT),
            Text("3. Multi-agent: Plackett-Luce > Elo", font_size=20, color=TEXT_LIGHT),
            Text("4. Separate Driver from Car", font_size=20, color=TEXT_LIGHT),
            Text("5. DNF != Loss -> Survival censoring", font_size=20, color=TEXT_LIGHT),
            Text("6. Track uncertainty, not just rating", font_size=20, color=TEXT_LIGHT)
        )
        insights.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        insights.move_to(ORIGIN)
        
        for insight in insights:
            self.play(Write(insight), run_time=2.4)
        
        self.wait(8)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene16_3_ClosingStatement(Scene):
    """Scene 16.3: Polished closing title card."""

    def construct(self):
        self.camera.background_color = DARK_BG

        # Breadcrumb timeline — recaps the journey
        crumbs = VGroup(
            Text("Harkness", font_size=18, color=ELO_RED),
            Text("->", font_size=18, color=TEXT_GRAY),
            Text("Elo", font_size=18, color=ELO_BLUE),
            Text("->", font_size=18, color=TEXT_GRAY),
            Text("Bradley-Terry", font_size=18, color=ELO_GOLD),
            Text("->", font_size=18, color=TEXT_GRAY),
            Text("Bayesian", font_size=18, color=ELO_GREEN),
        )
        crumbs.arrange(RIGHT, buff=0.25)
        crumbs.move_to(UP * 2.5)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in crumbs], lag_ratio=0.07),
            run_time=4.8
        )

        # Thin separator line
        sep = Line(LEFT * 5, RIGHT * 5, color=TEXT_GRAY, stroke_width=0.8)
        sep.next_to(crumbs, DOWN, buff=0.35)
        self.play(Create(sep), run_time=2)

        # Main message
        message = Text("The answer was never a number.", font_size=42, color=ELO_GOLD, weight=BOLD)
        message.move_to(UP * 0.8)
        self.play(Write(message, run_time=7.2))
        self.wait(1.2)

        sub1 = Text("It was a probability distribution.", font_size=32, color=TEXT_LIGHT)
        sub1.next_to(message, DOWN, buff=0.4)
        self.play(Write(sub1, run_time=4.8))
        self.wait(2)

        sub2 = Text("A belief, refined by evidence.", font_size=26, color=TEXT_GRAY, slant=ITALIC)
        sub2.next_to(sub1, DOWN, buff=0.3)
        self.play(FadeIn(sub2, shift=UP * 0.2), run_time=4)
        self.wait(4)

        # Final title card
        final = Text("The Mathematics of Ranking", font_size=44, color=ELO_BLUE, weight=BOLD)
        final.move_to(DOWN * 1.8)
        underline = Line(
            final.get_left() + DOWN * 0.08,
            final.get_right() + DOWN * 0.08,
            color=ELO_GOLD, stroke_width=2.5
        )

        self.play(FadeIn(final, shift=UP * 0.3), run_time=4.8)
        self.play(Create(underline), run_time=2.4)
        self.wait(12)

        # Elegant fade to black
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=6)
