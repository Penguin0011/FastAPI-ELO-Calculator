# Section 5: The Facemash Interlude
# 5 Scenes covering the Hollywood math error

from manim import *
import numpy as np
import sys
sys.path.append('..')
from utils.colors import *


class Scene5_1_CulturalExplosion(Scene):
    """Scene 5.1: Cultural Explosion - Elo enters mainstream."""

    def construct(self):
        self.camera.background_color = DARK_BG

        # Movie theater atmosphere
        year = Text("2010", font_size=72, color=ELO_GOLD)
        year.move_to(UP * 2)
        self.play(Write(year), run_time=1)

        # Movie title
        movie = Text("The Social Network", font_size=56, color=TEXT_WHITE)
        movie.next_to(year, DOWN, buff=0.5)
        self.play(Write(movie), run_time=1.5)

        # Tagline
        tagline = Text(
            "The Elo algorithm enters mainstream consciousness",
            font_size=28,
            color=TEXT_GRAY
        )
        tagline.next_to(movie, DOWN, buff=0.5)
        self.play(FadeIn(tagline, shift=DOWN * 0.3), run_time=1)

        # Award recognition (no emoji)
        awards = Text("3 Academy Awards", font_size=24, color=ELO_GOLD)
        awards.move_to(DOWN * 1.5)
        self.play(FadeIn(awards, shift=UP * 0.2), run_time=0.8)

        # But...
        but_box = RoundedRectangle(
            width=7, height=0.9, corner_radius=0.12,
            fill_color=ELO_RED, fill_opacity=0.15,
            stroke_color=ELO_RED, stroke_width=2
        )
        but_box.move_to(DOWN * 2.5)
        but_text = Text(
            "But there's a mathematical problem...",
            font_size=32,
            color=ELO_RED
        )
        but_text.move_to(but_box)

        self.wait(1)
        self.play(FadeIn(but_box), Write(but_text, run_time=1.5))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene5_2_EloForAesthetics(Scene):
    """Scene 5.2: Elo for Subjective Aesthetics."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Facemash: Elo for Aesthetics", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Concept explanation (left)
        concept = VGroup(
            Text("Elo doesn't require 'skill'", font_size=24, color=TEXT_LIGHT),
            Text("It requires:", font_size=24, color=TEXT_GRAY)
        )
        concept.arrange(DOWN, buff=0.2)
        concept.move_to(UP * 1.5 + LEFT * 3)
        self.play(FadeIn(concept, shift=DOWN * 0.2), run_time=1)

        # Requirements
        reqs = VGroup(
            Text("1. A property that can be ordered", font_size=20, color=TEXT_GRAY),
            Text("2. A method of pairwise comparison", font_size=20, color=TEXT_GRAY)
        )
        reqs.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        reqs.next_to(concept, DOWN, buff=0.3)
        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in reqs], lag_ratio=0.2),
            run_time=0.9
        )

        # Facemash mapping (right)
        mapping_box = RoundedRectangle(
            width=4.5, height=2.5, corner_radius=0.15,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_GOLD, stroke_width=1.5
        )
        mapping_box.move_to(RIGHT * 3 + UP * 1)
        mapping = VGroup(
            Text("In Facemash:", font_size=24, color=ELO_GOLD),
            Text('"Skill" = Attractiveness', font_size=20, color=TEXT_GRAY),
            Text('"Match" = User click', font_size=20, color=TEXT_GRAY)
        )
        mapping.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        mapping.move_to(mapping_box)
        self.play(FadeIn(mapping_box), FadeIn(mapping, shift=LEFT * 0.2), run_time=1)

        # Pairwise comparison visualization
        photo_a = Rectangle(
            width=2, height=2.5,
            fill_color=ELO_BLUE, fill_opacity=0.5,
            stroke_color=ELO_BLUE
        )
        photo_a.move_to(LEFT * 2 + DOWN * 1.5)
        label_a = Text("Photo A", font_size=18)
        label_a.next_to(photo_a, DOWN, buff=0.1)

        photo_b = Rectangle(
            width=2, height=2.5,
            fill_color=ELO_RED, fill_opacity=0.5,
            stroke_color=ELO_RED
        )
        photo_b.move_to(RIGHT * 2 + DOWN * 1.5)
        label_b = Text("Photo B", font_size=18)
        label_b.next_to(photo_b, DOWN, buff=0.1)

        vs = Text("vs", font_size=32, color=TEXT_GRAY)
        vs.move_to(DOWN * 1.5)

        self.play(
            FadeIn(photo_a), FadeIn(label_a),
            FadeIn(photo_b), FadeIn(label_b),
            Write(vs),
            run_time=1
        )

        # Click animation (no emoji - use text)
        click = Text("User clicks", font_size=20, color=ELO_GREEN)
        click.next_to(photo_a, UP, buff=0.2)
        self.play(FadeIn(click, scale=0.5), run_time=0.3)
        self.play(
            photo_a.animate.set_stroke(ELO_GREEN, width=4),
            run_time=0.3
        )

        # Ratings update
        result = VGroup(
            Text("Photo A: +K points", font_size=18, color=ELO_GREEN),
            Text("Photo B: -K points", font_size=18, color=ELO_RED)
        )
        result.arrange(DOWN, buff=0.1)
        result.next_to(vs, DOWN, buff=0.5)
        self.play(FadeIn(result, shift=UP * 0.2), run_time=0.8)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene5_3_HollywoodScandal(Scene):
    """Scene 5.3: The Hollywood Math Scandal - Wrong formula on screen."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Hollywood Math Error", font_size=48, color=ELO_RED)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Scene description
        scene_desc = Text(
            "Eduardo writes the algorithm on the dorm window...",
            font_size=24,
            color=TEXT_GRAY
        )
        scene_desc.move_to(UP * 1.8)
        self.play(FadeIn(scene_desc, shift=DOWN * 0.3), run_time=1)

        # The WRONG formula (as shown in the movie)
        wrong_label = Text("What he wrote:", font_size=20, color=ELO_RED)
        wrong_label.move_to(UP * 0.8 + LEFT * 3.5)

        wrong_formula = MathTex(
            r"E_A = \frac{1}{1 + 10 \times \frac{R_B - R_A}{400}}",
            font_size=40
        )
        wrong_formula.set_color(ELO_RED)
        wrong_formula.move_to(UP * 0.8 + RIGHT * 1)

        # Text "WRONG" instead of emoji X
        wrong_x = Text("WRONG", font_size=28, color=ELO_RED, weight=BOLD)
        wrong_x.next_to(wrong_formula, RIGHT, buff=0.3)

        self.play(Write(wrong_label), run_time=0.5)
        self.play(Write(wrong_formula), run_time=1.5)
        self.play(FadeIn(wrong_x, scale=0.5), run_time=0.3)

        # The CORRECT formula
        correct_label = Text("What it should be:", font_size=20, color=ELO_GREEN)
        correct_label.move_to(DOWN * 0.8 + LEFT * 3.5)

        correct_formula = MathTex(
            r"E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}",
            font_size=40
        )
        correct_formula.set_color(ELO_GREEN)
        correct_formula.move_to(DOWN * 0.8 + RIGHT * 1)

        # Text "CORRECT" instead of emoji checkmark
        correct_check = Text("CORRECT", font_size=28, color=ELO_GREEN, weight=BOLD)
        correct_check.next_to(correct_formula, RIGHT, buff=0.3)

        self.play(Write(correct_label), run_time=0.5)
        self.play(Write(correct_formula), run_time=1.5)
        self.play(FadeIn(correct_check, scale=0.5), run_time=0.3)

        # Highlight the key difference
        diff_box = RoundedRectangle(
            width=6, height=1.4, corner_radius=0.15,
            stroke_color=ELO_GOLD, stroke_width=3,
            fill_color=DARKER_BG, fill_opacity=0.8
        )
        diff_box.move_to(DOWN * 2.5)

        diff_text = VGroup(
            Text("MULTIPLICATION", font_size=24, color=ELO_RED),
            Text("vs", font_size=20, color=TEXT_GRAY),
            Text("EXPONENTIATION", font_size=24, color=ELO_GREEN)
        )
        diff_text.arrange(RIGHT, buff=0.3)
        diff_text.move_to(diff_box)

        self.play(FadeIn(diff_box), Write(diff_text), run_time=1)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene5_4_CatastrophicError(Scene):
    """Scene 5.4: Why It's Catastrophic - Negative probability.

    Dramatic color flash on the negative result.
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Why This Breaks Everything", font_size=44, color=ELO_RED)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Example setup
        example = Text(
            "Example: Photo A rated 1800, Photo B rated 1400",
            font_size=22, color=TEXT_GRAY
        )
        example.move_to(UP * 1.8)
        self.play(FadeIn(example, shift=DOWN * 0.2), run_time=0.8)

        # Hollywood calculation (left column)
        calc_label = Text("Hollywood formula:", font_size=20, color=ELO_RED)
        calc_label.move_to(UP * 1 + LEFT * 4)

        calc = MathTex(
            r"E_A &= \frac{1}{1 + 10 \times \frac{1400 - 1800}{400}} \\",
            r"&= \frac{1}{1 + 10 \times (-1)} \\",
            r"&= \frac{1}{1 - 10} \\",
            r"&= \frac{1}{-9} \\",
            r"&= -0.111\ldots",
            font_size=28
        )
        calc.move_to(ORIGIN + RIGHT * 1)

        self.play(Write(calc_label), run_time=0.5)
        for i, line in enumerate(calc):
            self.play(Write(line), run_time=0.6)
            if i == len(calc) - 1:
                line.set_color(ELO_RED)

        # Dramatic result with flash
        result = Text("NEGATIVE PROBABILITY: -11%", font_size=36, color=ELO_RED)
        result.move_to(DOWN * 2)
        result_box = SurroundingRectangle(result, color=ELO_RED, buff=0.2, stroke_width=3)

        self.play(Write(result), Create(result_box), run_time=1)

        # Dramatic flash (Indicate with scale)
        self.play(Indicate(result, color=ELO_RED, scale_factor=1.15), run_time=0.5)
        self.play(Indicate(result, color=WARNING, scale_factor=1.1), run_time=0.4)

        # System crash message (no emoji)
        crash_box = RoundedRectangle(
            width=5, height=0.8, corner_radius=0.1,
            fill_color=ELO_RED, fill_opacity=0.25,
            stroke_color=ELO_RED, stroke_width=2
        )
        crash_box.move_to(DOWN * 3)
        crash = Text("SYSTEM CRASH", font_size=32, color=ELO_RED, weight=BOLD)
        crash.move_to(crash_box)

        self.play(FadeIn(crash_box), FadeIn(crash, scale=0.5), run_time=0.5)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene5_5_CorrectFormula(Scene):
    """Scene 5.5: The Correct Formula - Symmetry restored.

    Shows precise calculation: 10^(-1) = 0.1, denominator = 1.1,
    E_A = 1/1.1 = 0.909 (shown precisely, not rounded to 0.91).
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Correct Approach", font_size=48, color=ELO_GREEN)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Side by side titles
        wrong_title = Text("Multiplication (Wrong)", font_size=20, color=ELO_RED)
        wrong_title.move_to(LEFT * 3 + UP * 1.5)

        correct_title = Text("Exponentiation (Right)", font_size=20, color=ELO_GREEN)
        correct_title.move_to(RIGHT * 3 + UP * 1.5)

        self.play(
            FadeIn(wrong_title, shift=RIGHT * 0.2),
            FadeIn(correct_title, shift=LEFT * 0.2),
            run_time=0.8
        )

        # Results for same example (rating diff = -400, so R_B - R_A = 400 -> exponent = 400/400 = 1)
        # Correct: 10^(-400/400) = 10^(-1) = 0.1; denominator = 1 + 0.1 = 1.1; E_A = 1/1.1 = 0.909
        wrong_result = VGroup(
            Text("Rating diff: -400", font_size=18, color=TEXT_GRAY),
            MathTex(r"1 + 10 \times (-1) = -9", font_size=24, color=ELO_RED),
            MathTex(r"E_A = \frac{1}{-9} \approx -0.11", font_size=24, color=ELO_RED),
            Text("Crashes! (invalid)", font_size=20, color=ELO_RED)
        )
        wrong_result.arrange(DOWN, buff=0.2)
        wrong_result.move_to(LEFT * 3 + DOWN * 0.5)

        correct_result = VGroup(
            Text("Rating diff: -400", font_size=18, color=TEXT_GRAY),
            MathTex(r"1 + 10^{-1} = 1 + 0.1 = 1.1", font_size=24, color=ELO_GREEN),
            MathTex(r"E_A = \frac{1}{1.1} \approx 0.909", font_size=24, color=ELO_GREEN),
            Text("Valid probability!", font_size=20, color=ELO_GREEN)
        )
        correct_result.arrange(DOWN, buff=0.2)
        correct_result.move_to(RIGHT * 3 + DOWN * 0.5)

        divider = Line(ORIGIN + UP * 2, ORIGIN + DOWN * 2, color=TEXT_GRAY)
        self.play(Create(divider), run_time=0.3)
        self.play(
            FadeIn(wrong_result, shift=UP * 0.2),
            FadeIn(correct_result, shift=UP * 0.2),
            run_time=1.5
        )

        # Indicate the correct result
        self.play(Indicate(correct_result[-1], color=ELO_GREEN, scale_factor=1.1), run_time=0.6)

        # Symmetry proof
        symmetry = VGroup(
            Text("Symmetry Proof:", font_size=24, color=ELO_GOLD),
            MathTex(r"E_A + E_B = 1", font_size=32, color=ELO_GOLD)
        )
        symmetry.arrange(DOWN, buff=0.2)
        symmetry.move_to(DOWN * 2.5)

        symmetry_box = SurroundingRectangle(symmetry, color=ELO_GOLD, buff=0.2, corner_radius=0.1)
        self.play(Write(symmetry), Create(symmetry_box), run_time=1)

        # Explanation
        explain = Text(
            "Points gained by winner = Points lost by loser",
            font_size=22,
            color=TEXT_LIGHT
        )
        explain.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(explain, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene5_3a_ExplainFacemashError(Scene):
    """Scene 5.3a: Why exponentiation is not multiplication in the Elo formula."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Why Exponent != Multiply", font_size=44, color=ELO_RED)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Step 1: Show both formulas
        step1 = Text("The Two Versions", font_size=22, color=ELO_GOLD)
        step1.next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(step1, shift=DOWN * 0.2), run_time=0.3)

        wrong = VGroup(
            Text("MOVIE (Wrong):", font_size=20, color=ELO_RED),
            MathTex(r"1 + 10 \times \frac{R_B - R_A}{400}", font_size=28, color=ELO_RED)
        )
        wrong.arrange(DOWN, buff=0.15)
        wrong.move_to(LEFT * 3.5 + UP * 0.3)

        right = VGroup(
            Text("CORRECT:", font_size=20, color=ELO_GREEN),
            MathTex(r"1 + 10^{(R_B - R_A)/400}", font_size=28, color=ELO_GREEN)
        )
        right.arrange(DOWN, buff=0.15)
        right.move_to(RIGHT * 3.5 + UP * 0.3)

        vs = Text("vs", font_size=24, color=TEXT_GRAY)
        vs.move_to(UP * 0.3)

        self.play(
            FadeIn(wrong, shift=RIGHT * 0.2),
            Write(vs),
            FadeIn(right, shift=LEFT * 0.2),
            run_time=1
        )
        self.wait(0.5)

        # Key difference
        diff_items = VGroup(
            Text("Multiply: result can be ANY number (including negative!)", font_size=16, color=ELO_RED),
            Text("Exponent: result is ALWAYS positive", font_size=16, color=ELO_GREEN)
        )
        diff_items.arrange(DOWN, buff=0.15)
        diff_items.move_to(DOWN * 1)
        self.play(
            LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in diff_items], lag_ratio=0.3),
            run_time=0.8
        )
        self.wait(1)

        # Step 2: Plot both denominators
        self.play(*[FadeOut(m) for m in [step1, wrong, right, vs, diff_items]], run_time=0.3)

        step3 = Text("Plotting Both Denominators", font_size=22, color=ELO_GOLD)
        step3.next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(step3, shift=DOWN * 0.2), run_time=0.3)

        axes = Axes(
            x_range=[-800, 800, 200], y_range=[-15, 15, 5],
            x_length=10, y_length=5, tips=False,
            axis_config={"include_numbers": True, "font_size": 10}
        )
        axes.move_to(DOWN * 0.5)

        x_label = Text("Rating gap (R_B - R_A)", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Denominator value", font_size=14, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.5)

        def wrong_denom(x):
            return 1 + 10 * (x / 400)

        def correct_denom(x):
            return 1 + 10 ** (x / 400)

        wrong_line = axes.plot(wrong_denom, x_range=[-800, 800], color=ELO_RED)
        correct_line = axes.plot(correct_denom, x_range=[-800, 400], color=ELO_GREEN)

        wrong_label = Text("Multiply (linear)", font_size=14, color=ELO_RED)
        wrong_label.move_to(axes.c2p(-500, wrong_denom(-500)) + UP * 0.4)
        correct_label = Text("Exponent (exponential)", font_size=14, color=ELO_GREEN)
        correct_label.move_to(axes.c2p(200, 6))

        self.play(Create(wrong_line), FadeIn(wrong_label), run_time=1)
        self.play(Create(correct_line), FadeIn(correct_label), run_time=1)

        # Zero line
        zero_line = DashedLine(axes.c2p(-800, 0), axes.c2p(800, 0), color=ELO_GOLD, stroke_width=2)
        zero_text = Text("Below here: NEGATIVE denominator!", font_size=14, color=ELO_GOLD)
        zero_text.move_to(axes.c2p(400, -2))

        self.play(Create(zero_line), FadeIn(zero_text), run_time=0.8)

        # Crossing point
        cross_dot = Dot(axes.c2p(-40, 0), color=ELO_RED, radius=0.1)
        cross_label = Text("Crosses zero at gap = -40!", font_size=14, color=ELO_RED)
        cross_label.next_to(cross_dot, DOWN, buff=0.2)
        self.play(FadeIn(cross_dot), FadeIn(cross_label), run_time=0.8)
        self.wait(1)

        # Step 3: Consequence
        self.play(*[FadeOut(m) for m in [step3, axes, x_label, y_label,
                    wrong_line, correct_line, wrong_label, correct_label,
                    zero_line, zero_text, cross_dot, cross_label]], run_time=0.3)

        step4 = Text("The Consequence", font_size=22, color=ELO_GOLD)
        step4.next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(step4, shift=DOWN * 0.2), run_time=0.3)

        consequence = VGroup(
            Text("Multiply version: when stronger player is favored by > 40 points...", font_size=18, color=TEXT_GRAY),
            MathTex(r"E_A = \frac{1}{\text{negative}} = \text{NEGATIVE PROBABILITY}", font_size=28, color=ELO_RED),
            Text("", font_size=6),
            Text("Exponent version: denominator is ALWAYS > 1", font_size=18, color=TEXT_GRAY),
            MathTex(r"E_A = \frac{1}{1 + \underbrace{10^{\text{anything}}}_{\text{always } > 0}} \in (0, 1)",
                    font_size=28, color=ELO_GREEN),
        )
        consequence.arrange(DOWN, buff=0.2)
        consequence.move_to(DOWN * 0.5)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in consequence], lag_ratio=0.15),
            run_time=1.5
        )

        takeaway = Text(
            "Exponentiation guarantees valid probabilities for ANY rating gap",
            font_size=18, color=ELO_GOLD
        )
        takeaway.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(takeaway, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
