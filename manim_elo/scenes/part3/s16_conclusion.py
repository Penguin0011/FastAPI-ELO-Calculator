# Section 16: Conclusion
# 3 Scenes

from manim import *
import sys
sys.path.append('..')
from utils.colors import *


class Scene16_1_SystemFlowchart(Scene):
    """Scene 16.1: Complete System Flowchart."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("The Complete System", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
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
        
        self.play(FadeIn(VGroup(input_box, input_text, process_box, process_text, output_box, output_text)), run_time=1)
        self.play(Create(VGroup(arrow1, arrow2)), run_time=0.5)
        
        # Components below
        components = VGroup(
            Text("• Plackett-Luce ranking", font_size=16, color=TEXT_GRAY),
            Text("• Hierarchical α + β decomposition", font_size=16, color=TEXT_GRAY),
            Text("• MCMC inference", font_size=16, color=TEXT_GRAY),
            Text("• Glicko-2 uncertainty", font_size=16, color=TEXT_GRAY)
        )
        components.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        components.move_to(DOWN * 1.5)
        
        self.play(FadeIn(components), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene16_2_KeyInsights(Scene):
    """Scene 16.2: Key Insights."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Key Insights", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)
        
        insights = VGroup(
            Text("1. Skill is latent — observe noisy performance", font_size=20, color=TEXT_LIGHT),
            Text("2. Linear models fail at extremes → Use probability", font_size=20, color=TEXT_LIGHT),
            Text("3. Multi-agent: Plackett-Luce > Elo", font_size=20, color=TEXT_LIGHT),
            Text("4. Separate Driver from Car", font_size=20, color=TEXT_LIGHT),
            Text("5. DNF ≠ Loss → Survival censoring", font_size=20, color=TEXT_LIGHT),
            Text("6. Track uncertainty, not just rating", font_size=20, color=TEXT_LIGHT)
        )
        insights.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        insights.move_to(ORIGIN)
        
        for insight in insights:
            self.play(Write(insight), run_time=0.6)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene16_3_ClosingStatement(Scene):
    """Scene 16.3: Closing."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        message = Text("Context Is Everything", font_size=56, color=ELO_GOLD)
        message.move_to(UP * 1)
        self.play(Write(message), run_time=2)
        
        subtitle = Text("70 years of ranking evolution", font_size=24, color=TEXT_LIGHT)
        subtitle.next_to(message, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=1)
        
        self.wait(2)
        
        final = Text("The Mathematics of Ranking", font_size=48, color=ELO_BLUE)
        final.move_to(DOWN * 1)
        self.play(FadeIn(final), run_time=1.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
