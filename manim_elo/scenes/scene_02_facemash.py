"""
Scene 2: Facemash Algorithm
Covers Mark Zuckerberg's Facemash project at Harvard as a modern application of ELO.

This scene introduces:
- The 2003 Facemash incident
- Pairwise comparison system
- How ELO-style ratings emerge from simple choices
- The connection to broader applications
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *


class FacemashIntro(Scene):
    """Opening for the Facemash section."""
    
    def construct(self):
        # Title with dramatic reveal
        title = Text("From Chess to...", font_size=40, color=WHITE)
        title.shift(UP * 0.5)
        
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        
        title2 = Text("Social Networks", font_size=52, color=ORANGE)
        title2.shift(DOWN * 0.5)
        
        self.play(Write(title2), run_time=1.5)
        self.wait(1)
        
        # Date reveal
        year = Text("2003 • Harvard University", font_size=28, color=GREY)
        year.shift(DOWN * 2)
        
        self.play(FadeIn(year), run_time=1)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class FacemashStory(Scene):
    """The story of Facemash creation."""
    
    def construct(self):
        # Section title
        title = Text("The Facemash Story", font_size=44, color=ORANGE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Story elements
        story_parts = [
            ("October 28, 2003", "One night in Harvard's Kirkland House", GREY),
            ("Mark Zuckerberg", "19-year-old sophomore", LIGHT_BLUE),
            ("A simple question:", "", GREY),
            ("\"Who is more attractive?\"", "", ORANGE),
        ]
        
        current_y = 1.5
        story_group = VGroup()
        
        for main_text, sub_text, color in story_parts:
            main = Text(main_text, font_size=32 if sub_text else 36, color=color)
            main.shift(UP * current_y)
            
            if sub_text:
                sub = Text(sub_text, font_size=22, color=GREY)
                sub.next_to(main, DOWN, buff=0.1)
                story_group.add(VGroup(main, sub))
                current_y -= 1.1
            else:
                story_group.add(main)
                current_y -= 0.8
            
            self.play(Write(main), run_time=0.8)
            if sub_text:
                self.play(FadeIn(sub), run_time=0.5)
            self.wait(0.5)
        
        self.wait(1)
        
        # The concept
        concept_box = RoundedRectangle(
            corner_radius=0.15, width=10, height=1.8,
            fill_color=DARK_BG, fill_opacity=0.9,
            stroke_color=ORANGE, stroke_width=2
        )
        concept_box.shift(DOWN * 1.8)
        
        concept_text = VGroup(
            Text("Take student photos from dormitories", font_size=24, color=WHITE),
            Text("Show two at a time", font_size=24, color=WHITE),
            Text("Let visitors vote → Build a ranking", font_size=24, color=YELLOW),
        )
        concept_text.arrange(DOWN, buff=0.15)
        concept_text.move_to(concept_box.get_center())
        
        self.play(Create(concept_box), run_time=0.8)
        self.play(Write(concept_text), run_time=1.5)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class FacemashMechanism(Scene):
    """Visualize the pairwise comparison mechanism."""
    
    def construct(self):
        title = Text("The Comparison Engine", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Create two "photo" boxes
        photo_a = self.create_photo_box("A", LEFT * 2.5)
        photo_b = self.create_photo_box("B", RIGHT * 2.5)
        
        self.play(FadeIn(photo_a), FadeIn(photo_b), run_time=1)
        
        # VS text
        vs_text = Text("VS", font_size=48, color=ORANGE)
        
        self.play(Write(vs_text), run_time=0.5)
        self.wait(1)
        
        # Ratings underneath
        rating_a = Text("Rating: 1500", font_size=20, color=GREY)
        rating_a.next_to(photo_a, DOWN, buff=0.3)
        rating_b = Text("Rating: 1500", font_size=20, color=GREY)
        rating_b.next_to(photo_b, DOWN, buff=0.3)
        
        self.play(Write(rating_a), Write(rating_b), run_time=0.8)
        self.wait(0.5)
        
        # User clicks A (winner)
        click_text = Text("User clicks A!", font_size=28, color=TEAL)
        click_text.shift(DOWN * 2.5)
        
        self.play(Write(click_text), run_time=0.8)
        
        # Highlight A as winner
        winner_glow = SurroundingRectangle(photo_a, color=TEAL, stroke_width=4, buff=0.1)
        self.play(Create(winner_glow), run_time=0.5)
        
        self.wait(0.5)
        
        # Update ratings animation
        arrow_up = Arrow(
            rating_a.get_center() + DOWN * 0.3,
            rating_a.get_center(),
            color=ELO_POSITIVE, stroke_width=3
        ).scale(0.5)
        
        arrow_down = Arrow(
            rating_b.get_center(),
            rating_b.get_center() + DOWN * 0.3,
            color=ELO_NEGATIVE, stroke_width=3
        ).scale(0.5)
        
        new_rating_a = Text("Rating: 1512", font_size=20, color=ELO_POSITIVE)
        new_rating_a.move_to(rating_a.get_center())
        
        new_rating_b = Text("Rating: 1488", font_size=20, color=ELO_NEGATIVE)
        new_rating_b.move_to(rating_b.get_center())
        
        self.play(
            GrowArrow(arrow_up), GrowArrow(arrow_down),
            Transform(rating_a, new_rating_a),
            Transform(rating_b, new_rating_b),
            run_time=1
        )
        
        self.wait(1)
        
        # Explanation
        explanation = Text(
            "Same math as Chess ELO - winner gains, loser loses!",
            font_size=26, color=YELLOW
        )
        explanation.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(
            FadeOut(click_text),
            Write(explanation),
            run_time=1
        )
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def create_photo_box(self, label, position):
        """Create a simple photo placeholder."""
        box = RoundedRectangle(
            corner_radius=0.1, width=2.5, height=3,
            fill_color=DARK_GREY, fill_opacity=0.8,
            stroke_color=WHITE, stroke_width=2
        )
        box.move_to(position)
        
        # Person icon (simplified)
        circle = Circle(radius=0.4, fill_color=GREY, fill_opacity=1, stroke_width=0)
        circle.move_to(position + UP * 0.3)
        
        body = Ellipse(width=1.2, height=0.8, fill_color=GREY, fill_opacity=1, stroke_width=0)
        body.move_to(position + DOWN * 0.7)
        
        label_text = Text(label, font_size=24, color=WHITE)
        label_text.move_to(position + DOWN * 1.2)
        
        return VGroup(box, circle, body, label_text)


class FacemashFormula(Scene):
    """Show this is the same ELO formula."""
    
    def construct(self):
        title = Text("The Math Behind Facemash", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Same formula as ELO
        same_text = Text("The exact same formula!", font_size=32, color=ORANGE)
        same_text.shift(UP * 1.5)
        
        self.play(Write(same_text), run_time=1)
        
        # ELO formula
        formula = MathTex(
            r"E_A = \frac{1}{1 + 10^{\frac{R_B - R_A}{400}}}",
            font_size=44
        )
        formula.shift(UP * 0.3)
        
        self.play(Write(formula), run_time=1.5)
        
        # Variables changed
        translation = VGroup(
            Text("Chess Player A → Photo A", font_size=24, color=WHITE),
            Text("Rating → Attractiveness Score", font_size=24, color=WHITE),
            Text("Win/Lose → Get Selected / Not Selected", font_size=24, color=WHITE),
        )
        translation.arrange(DOWN, buff=0.2)
        translation.shift(DOWN * 1.5)
        
        for line in translation:
            self.play(Write(line), run_time=0.7)
        
        self.wait(1)
        
        # Key insight
        insight = VGroup(
            Text("From thousands of simple choices,", font_size=28, color=WHITE),
            Text("an ordered ranking emerges automatically!", font_size=28, color=YELLOW),
        )
        insight.arrange(DOWN, buff=0.15)
        insight.to_edge(DOWN).shift(UP * 0.5)
        
        box = SurroundingRectangle(insight, color=YELLOW, buff=0.2)
        
        self.play(Write(insight), Create(box), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class FacemashImpact(Scene):
    """The impact and aftermath."""
    
    def construct(self):
        title = Text("The Aftermath", font_size=40, color=RED)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Stats
        stats = VGroup(
            Text("22,000 votes in 4 hours", font_size=32, color=LIGHT_BLUE),
            Text("Crashed Harvard's network", font_size=28, color=ORANGE),
            Text("Zuckerberg faced disciplinary action", font_size=26, color=RED),
        )
        stats.arrange(DOWN, buff=0.4)
        stats.shift(UP * 0.5)
        
        for stat in stats:
            self.play(Write(stat), run_time=0.8)
            self.wait(0.5)
        
        self.wait(1)
        
        # But...
        but_text = Text("But the idea lived on...", font_size=36, color=GREY)
        but_text.shift(DOWN * 1)
        
        self.play(Write(but_text), run_time=1)
        self.wait(0.5)
        
        # Facebook evolution
        evolution = VGroup(
            Text("Facemash (2003)", font_size=28, color=ORANGE),
            Text("→", font_size=36, color=WHITE),
            Text("TheFacebook (2004)", font_size=28, color=TEAL),
            Text("→", font_size=36, color=WHITE),
            Text("Facebook (2005)", font_size=28, color=LIGHT_BLUE),
        )
        evolution.arrange(RIGHT, buff=0.3)
        evolution.shift(DOWN * 2.2)
        
        self.play(Write(evolution), run_time=2)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class FacemashBroaderApplications(Scene):
    """Show ELO's broader applications beyond chess and Facemash."""
    
    def construct(self):
        title = Text("ELO Is Everywhere", font_size=44, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Applications grid
        apps = [
            ("Chess", "Original use", LIGHT_BLUE),
            ("Video Games", "Matchmaking (LoL, DOTA, etc.)", PURPLE),
            ("Football", "FIFA Rankings", GREEN),
            ("Basketball", "FiveThirtyEight", ORANGE),
            ("Dating Apps", "Tinder, Hinge", PINK),
            ("Search / A-B", "A/B Testing", TEAL),
        ]
        
        # Create 2x3 grid
        grid = VGroup()
        for i, (icon_text, desc, color) in enumerate(apps):
            box = RoundedRectangle(
                corner_radius=0.1, width=4, height=1.3,
                fill_color=color, fill_opacity=0.15,
                stroke_color=color, stroke_width=2
            )
            
            title_t = Text(icon_text, font_size=24, color=color)
            desc_t = Text(desc, font_size=16, color=WHITE)
            
            title_t.move_to(box.get_center() + UP * 0.2)
            desc_t.move_to(box.get_center() + DOWN * 0.3)
            
            cell = VGroup(box, title_t, desc_t)
            grid.add(cell)
        
        # Arrange in 2 rows
        row1 = VGroup(*grid[:3])
        row1.arrange(RIGHT, buff=0.3)
        row2 = VGroup(*grid[3:])
        row2.arrange(RIGHT, buff=0.3)
        
        full_grid = VGroup(row1, row2)
        full_grid.arrange(DOWN, buff=0.3)
        full_grid.shift(DOWN * 0.3)
        
        for cell in grid:
            self.play(FadeIn(cell, shift=UP * 0.2), run_time=0.4)
        
        self.wait(2)
        
        # Transition
        transition = Text(
            "But can we use it for... Formula 1?",
            font_size=32, color=ORANGE
        )
        transition.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(Write(transition), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Next title
        next_title = Text("Next: The F1 Paradox", font_size=48, color=RED)
        self.play(Write(next_title), run_time=1)
        self.wait(1)
        self.play(FadeOut(next_title))


if __name__ == "__main__":
    pass
