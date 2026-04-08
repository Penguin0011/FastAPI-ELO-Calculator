"""
Scene 1: History of ELO
Covers the origins of the ELO rating system with Arpad Elo and Chess.

This scene introduces:
- Arpad Elo (1903-1992), Hungarian-American physics professor
- The problem of ranking chess players fairly
- The old subjective title system vs objective ratings
- The core insight: using probability theory
"""

from manim import *
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *
from utils.formulas import EXPECTED_SCORE, RATING_UPDATE


class EloHistoryIntro(Scene):
    """Opening scene: Title and hook."""
    
    def construct(self):
        # Title
        title = Text("The Mathematics of Ranking", font_size=56, color=LIGHT_BLUE)
        subtitle = Text("How do we objectively compare skill?", font_size=32, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        title_group = VGroup(title, subtitle)
        
        # Animate title
        self.play(Write(title), run_time=2)
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.wait(2)
        
        # Transition out
        self.play(FadeOut(title_group, shift=UP))
        self.wait(0.5)


class ArpadEloIntro(Scene):
    """Introduce Arpad Elo and the historical context."""
    
    def construct(self):
        # Section title
        section_title = Text("The Birth of ELO", font_size=48, color=GOLD)
        section_title.to_edge(UP).shift(DOWN * 0.5)
        
        # Arpad Elo info
        name = Text("Arpad Elo", font_size=44, color=LIGHT_BLUE)
        years = Text("1903 - 1992", font_size=28, color=GREY)
        profession = Text("Hungarian-American Physics Professor", font_size=24, color=WHITE)
        
        chess_master = Text("& Chess Master", font_size=24, color=ORANGE)
        
        name.shift(UP * 1)
        years.next_to(name, DOWN, buff=0.2)
        profession.next_to(years, DOWN, buff=0.3)
        chess_master.next_to(profession, DOWN, buff=0.1)
        
        info_group = VGroup(name, years, profession, chess_master)
        
        # Chess icon (simple representation)
        chess_board = self.create_mini_chess_board()
        chess_board.scale(0.8)
        chess_board.shift(DOWN * 1.5 + LEFT * 3)
        
        # Physics icon (simple atom)
        physics_icon = self.create_physics_icon()
        physics_icon.scale(0.6)
        physics_icon.shift(DOWN * 1.5 + RIGHT * 3)
        
        # Animations
        self.play(Write(section_title), run_time=1)
        self.wait(0.5)
        
        self.play(Write(name), run_time=1)
        self.play(FadeIn(years), run_time=0.5)
        self.wait(0.5)
        
        self.play(Write(profession), run_time=1)
        self.play(Write(chess_master), run_time=0.8)
        
        self.wait(0.5)
        
        # Show icons
        self.play(
            Create(chess_board),
            Create(physics_icon),
            run_time=1.5
        )
        
        self.wait(2)
        
        # Highlight the connection
        connection_text = Text(
            "He asked: How can we apply mathematics to ranking chess players?",
            font_size=24, color=YELLOW
        )
        connection_text.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(Write(connection_text), run_time=2)
        self.wait(3)
        
        # Fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
    
    def create_mini_chess_board(self):
        """Create a simple 4x4 chess board representation."""
        board = VGroup()
        colors = [WHITE, DARK_GREY]
        
        for i in range(4):
            for j in range(4):
                square = Square(
                    side_length=0.4,
                    fill_color=colors[(i + j) % 2],
                    fill_opacity=0.8,
                    stroke_width=0.5
                )
                square.move_to([i * 0.4 - 0.6, j * 0.4 - 0.6, 0])
                board.add(square)
        
        # Add a simple king piece
        king = Text("♔", font_size=32)
        king.move_to([0.2, 0.2, 0])
        board.add(king)
        
        return board
    
    def create_physics_icon(self):
        """Create a simple atom/physics representation."""
        # Central nucleus
        nucleus = Dot(color=ORANGE, radius=0.15)
        
        # Electron orbits
        orbit1 = Circle(radius=0.5, color=LIGHT_BLUE, stroke_width=1.5)
        orbit2 = Circle(radius=0.7, color=LIGHT_BLUE, stroke_width=1.5)
        orbit2.rotate(PI/3)
        orbit3 = Circle(radius=0.6, color=LIGHT_BLUE, stroke_width=1.5)
        orbit3.rotate(-PI/4)
        
        # Electrons
        e1 = Dot(color=LIGHT_BLUE, radius=0.08)
        e1.move_to([0.5, 0, 0])
        e2 = Dot(color=LIGHT_BLUE, radius=0.08)
        e2.move_to([-0.35, 0.5, 0])
        
        return VGroup(orbit1, orbit2, orbit3, nucleus, e1, e2)


class TheProblemBeforeElo(Scene):
    """Show the problem with ranking before ELO."""
    
    def construct(self):
        # Title
        title = Text("The Problem: Subjective Rankings", font_size=40, color=RED)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Old system - titles
        old_system_title = Text("Before 1960:", font_size=28, color=GREY)
        old_system_title.shift(UP * 2 + LEFT * 3)
        
        titles = VGroup(
            Text("Grandmaster", font_size=26, color=GOLD),
            Text("International Master", font_size=26, color=ORANGE),
            Text("FIDE Master", font_size=26, color=YELLOW),
            Text("Candidate Master", font_size=26, color=WHITE),
            Text("Amateur", font_size=26, color=GREY),
        )
        titles.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        titles.shift(LEFT * 3 + DOWN * 0.5)
        
        self.play(Write(old_system_title), run_time=0.8)
        
        for t in titles:
            self.play(FadeIn(t, shift=RIGHT * 0.2), run_time=0.3)
        
        self.wait(1)
        
        # Problems with old system
        problem_title = Text("Problems:", font_size=28, color=RED)
        problem_title.shift(UP * 2 + RIGHT * 2)
        
        problems = VGroup(
            Text("• Who decides promotions?", font_size=22, color=WHITE),
            Text("• How to compare across countries?", font_size=22, color=WHITE),
            Text("• Titles are sticky (never demoted)", font_size=22, color=WHITE),
            Text("• No quantitative predictions", font_size=22, color=WHITE),
        )
        problems.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        problems.shift(RIGHT * 2 + DOWN * 0.3)
        
        self.play(Write(problem_title), run_time=0.5)
        
        for p in problems:
            self.play(Write(p), run_time=0.6)
        
        self.wait(2)
        
        # The key question
        big_question = Text(
            "How do we objectively measure skill?",
            font_size=36, color=YELLOW
        )
        big_question.to_edge(DOWN).shift(UP * 0.8)
        
        box = SurroundingRectangle(big_question, color=YELLOW, buff=0.2)
        
        self.play(Write(big_question), Create(box), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class EloInsight(Scene):
    """Elo's key insight: probability theory."""
    
    def construct(self):
        # Title
        title = Text("Elo's Insight", font_size=44, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # The insight text
        insight1 = Text(
            "Don't count wins and losses.",
            font_size=32, color=WHITE
        )
        insight1.shift(UP * 1.5)
        
        insight2 = Text(
            "Predict probabilities.",
            font_size=36, color=GOLD
        )
        insight2.shift(UP * 0.5)
        
        self.play(Write(insight1), run_time=1.5)
        self.wait(0.5)
        self.play(Write(insight2), run_time=1.5)
        self.wait(1)
        
        # Explanation
        explanation = VGroup(
            Text("If a Grandmaster beats a Novice → Expected", font_size=26, color=GREY),
            Text("Ratings barely change", font_size=24, color=ELO_NEUTRAL),
        )
        explanation.arrange(DOWN, buff=0.15)
        explanation.shift(DOWN * 0.5)
        
        explanation2 = VGroup(
            Text("If a Novice beats a Grandmaster → SURPRISE!", font_size=26, color=ORANGE),
            Text("Ratings change dramatically", font_size=24, color=ELO_POSITIVE),
        )
        explanation2.arrange(DOWN, buff=0.15)
        explanation2.shift(DOWN * 2)
        
        self.play(Write(explanation), run_time=1.5)
        self.wait(1)
        self.play(Write(explanation2), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class ChessSymmetry(Scene):
    """Explain why ELO works perfectly for Chess."""
    
    def construct(self):
        title = Text("Why It Works for Chess", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Three key properties
        props = VGroup(
            self.create_property_box("1. Symmetry", "Both players use identical pieces", TEAL),
            self.create_property_box("2. Zero-Sum", "If I win, you lose", ORANGE),
            self.create_property_box("3. Isolation", "It's purely 1 vs 1", PURPLE),
        )
        props.arrange(DOWN, buff=0.4)
        props.shift(DOWN * 0.3)
        
        for prop in props:
            self.play(FadeIn(prop, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.5)
        
        self.wait(1)
        
        # Conclusion
        conclusion = Text(
            "These assumptions enable pure skill comparison",
            font_size=28, color=YELLOW
        )
        conclusion.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(Write(conclusion), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def create_property_box(self, title_text, desc_text, color):
        """Create a property box with title and description."""
        box = RoundedRectangle(
            corner_radius=0.1,
            width=10, height=1.2,
            fill_color=color, fill_opacity=0.15,
            stroke_color=color, stroke_width=2
        )
        
        title = Text(title_text, font_size=28, color=color)
        desc = Text(desc_text, font_size=22, color=WHITE)
        
        title.move_to(box.get_center() + UP * 0.25)
        desc.move_to(box.get_center() + DOWN * 0.25)
        
        return VGroup(box, title, desc)


class BasicEloFormula(Scene):
    """Introduce the basic ELO formula with animations."""
    
    def construct(self):
        title = Text("The ELO Formula", font_size=44, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Expected Score Formula
        formula_label = Text("Expected Score (Probability of Winning):", font_size=26, color=GREY)
        formula_label.shift(UP * 1.5)
        
        formula = MathTex(
            r"E_A = \frac{1}{1 + 10^{\frac{R_B - R_A}{400}}}",
            font_size=48
        )
        formula.set_color_by_tex_to_color_map({
            "E_A": LIGHT_BLUE,
            "R_A": TEAL,
            "R_B": ORANGE,
        })
        formula.shift(UP * 0.3)
        
        self.play(Write(formula_label), run_time=1)
        self.play(Write(formula), run_time=2)
        self.wait(1)
        
        # Explanation of terms
        terms = VGroup(
            MathTex(r"E_A", color=LIGHT_BLUE).scale(0.8),
            Text(" = Expected score for Player A", font_size=22, color=WHITE),
        )
        terms.arrange(RIGHT, buff=0.1)
        terms.shift(DOWN * 1)
        
        terms2 = VGroup(
            MathTex(r"R_A", color=TEAL).scale(0.8),
            Text(" = Rating of Player A", font_size=22, color=WHITE),
        )
        terms2.arrange(RIGHT, buff=0.1)
        terms2.shift(DOWN * 1.6)
        
        terms3 = VGroup(
            MathTex(r"R_B", color=ORANGE).scale(0.8),
            Text(" = Rating of Player B", font_size=22, color=WHITE),
        )
        terms3.arrange(RIGHT, buff=0.1)
        terms3.shift(DOWN * 2.2)
        
        self.play(Write(terms), run_time=0.8)
        self.play(Write(terms2), run_time=0.8)
        self.play(Write(terms3), run_time=0.8)
        
        self.wait(2)
        
        # Clean up for sigmoid visualization
        self.play(
            FadeOut(terms), FadeOut(terms2), FadeOut(terms3),
            FadeOut(formula_label),
            formula.animate.shift(UP * 0.5).scale(0.8)
        )
        
        # Create sigmoid curve
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.25],
            x_length=8,
            y_length=3.5,
            axis_config={"color": GREY, "include_tip": False},
        )
        axes.shift(DOWN * 1.2)
        
        x_label = Text("Rating Difference (R_A - R_B) / 400", font_size=18, color=GREY)
        x_label.next_to(axes, DOWN, buff=0.3)
        
        y_label = Text("P(Win)", font_size=18, color=GREY)
        y_label.next_to(axes, LEFT, buff=0.3)
        
        # Sigmoid function
        def sigmoid(x):
            return 1 / (1 + 10**(-x))
        
        graph = axes.plot(sigmoid, color=LIGHT_BLUE, stroke_width=3)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
        self.play(Create(graph), run_time=2)
        
        # Highlight key points
        # Equal ratings
        dot_equal = Dot(axes.c2p(0, 0.5), color=YELLOW, radius=0.1)
        label_equal = Text("Equal ratings → 50%", font_size=18, color=YELLOW)
        label_equal.next_to(dot_equal, UP + RIGHT, buff=0.1)
        
        self.play(Create(dot_equal), Write(label_equal), run_time=1)
        self.wait(1)
        
        # +400 higher
        dot_high = Dot(axes.c2p(1, sigmoid(1)), color=TEAL, radius=0.1)
        label_high = Text("+400 → 91%", font_size=18, color=TEAL)
        label_high.next_to(dot_high, UP, buff=0.1)
        
        self.play(Create(dot_high), Write(label_high), run_time=1)
        self.wait(1)
        
        # -400 lower
        dot_low = Dot(axes.c2p(-1, sigmoid(-1)), color=ORANGE, radius=0.1)
        label_low = Text("-400 → 9%", font_size=18, color=ORANGE)
        label_low.next_to(dot_low, DOWN, buff=0.1)
        
        self.play(Create(dot_low), Write(label_low), run_time=1)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RatingUpdateFormula(Scene):
    """Show how ratings get updated after a match."""
    
    def construct(self):
        title = Text("Rating Updates", font_size=44, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Update formula
        formula = MathTex(
            r"R'_A = R_A + K(S_A - E_A)",
            font_size=44
        )
        formula.shift(UP * 1.5)
        
        self.play(Write(formula), run_time=1.5)
        self.wait(0.5)
        
        # Term explanations
        explanations = VGroup(
            Text("R'_A = New rating after match", font_size=24, color=WHITE),
            Text("K = Volatility factor (typically 24)", font_size=24, color=WHITE),
            Text("S_A = Actual score (1=win, 0.5=draw, 0=loss)", font_size=24, color=WHITE),
            Text("E_A = Expected score (probability)", font_size=24, color=WHITE),
        )
        explanations.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        explanations.shift(DOWN * 0.3 + LEFT)
        
        for exp in explanations:
            self.play(Write(exp), run_time=0.7)
        
        self.wait(1)
        
        # Key insight box
        insight_box = RoundedRectangle(
            corner_radius=0.15, width=10, height=1.5,
            fill_color=DARK_BLUE, fill_opacity=0.2,
            stroke_color=LIGHT_BLUE, stroke_width=2
        )
        insight_box.shift(DOWN * 2.5)
        
        insight_text = Text(
            "You gain points when you EXCEED expectations,\nlose points when you UNDERPERFORM.",
            font_size=24, color=WHITE, line_spacing=1.3
        )
        insight_text.move_to(insight_box.get_center())
        
        self.play(Create(insight_box), Write(insight_text), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class HistoryConclusion(Scene):
    """Conclude the history section and set up the transition."""
    
    def construct(self):
        # Summary
        title = Text("The ELO Legacy", font_size=44, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.5)
        
        self.play(Write(title), run_time=1)
        
        facts = VGroup(
            Text("✓ Adopted by FIDE in 1970", font_size=28, color=TEAL),
            Text("✓ Used in video game matchmaking", font_size=28, color=TEAL),
            Text("✓ Adapted for many other sports", font_size=28, color=TEAL),
            Text("✓ Foundation for modern rating systems", font_size=28, color=TEAL),
        )
        facts.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        facts.center()
        
        for fact in facts:
            self.play(Write(fact), run_time=0.8)
            self.wait(0.3)
        
        self.wait(1)
        
        # Transition teaser
        transition = Text(
            "But what happens when we apply this to... social networks?",
            font_size=30, color=ORANGE
        )
        transition.to_edge(DOWN).shift(UP * 0.8)
        
        self.play(Write(transition), run_time=2)
        self.wait(2)
        
        # Fade to next section
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        next_title = Text("Next: Facemash", font_size=48, color=ORANGE)
        self.play(Write(next_title), run_time=1)
        self.wait(1)
        self.play(FadeOut(next_title))


# Main entry point for rendering
if __name__ == "__main__":
    # This allows running individual scenes from command line
    # Example: manim -pql scene_01_elo_history.py EloHistoryIntro
    pass
