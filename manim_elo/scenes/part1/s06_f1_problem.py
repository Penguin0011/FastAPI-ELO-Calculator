# Section 6: The Limits of Pairwise Models - The Formula 1 Problem
# 6 Scenes covering why Elo fails for F1

from manim import *
import numpy as np
import sys
sys.path.append('..')
from utils.colors import *


class Scene6_1_StructuralIncompatibility(Scene):
    """Scene 6.1: Structural Incompatibility - 1v1 vs 20-way."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The F1 Problem", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Chess: 2 players (left)
        chess_label = Text("Chess", font_size=28, color=ELO_BLUE)
        chess_label.move_to(LEFT * 4 + UP * 1)

        chess_board = Square(side_length=2, color=ELO_BLUE, fill_opacity=0.3)
        chess_board.next_to(chess_label, DOWN, buff=0.3)

        p1 = Dot(chess_board.get_center() + LEFT * 0.4, color=TEXT_WHITE)
        p2 = Dot(chess_board.get_center() + RIGHT * 0.4, color=TEXT_GRAY)

        vs_text = Text("1 vs 1", font_size=20, color=TEXT_GRAY)
        vs_text.next_to(chess_board, DOWN, buff=0.2)

        self.play(
            Write(chess_label),
            Create(chess_board),
            FadeIn(p1), FadeIn(p2),
            FadeIn(vs_text, shift=UP * 0.2),
            run_time=1
        )

        # Separation arrow
        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, color=TEXT_GRAY)
        arrow.move_to(DOWN * 0.5)
        self.play(Create(arrow), run_time=0.5)

        # F1: 20 drivers (right)
        f1_label = Text("Formula 1", font_size=28, color=ELO_RED)
        f1_label.move_to(RIGHT * 4 + UP * 1)

        f1_grid = Rectangle(width=3, height=2, color=ELO_RED, fill_opacity=0.3)
        f1_grid.next_to(f1_label, DOWN, buff=0.3)

        # 20 dots in grid formation (4 rows x 5 cols)
        drivers = VGroup()
        for i in range(4):
            for j in range(5):
                dot = Dot(
                    f1_grid.get_corner(UL) + RIGHT * (0.3 + j * 0.55) + DOWN * (0.3 + i * 0.4),
                    color=ELO_GOLD,
                    radius=0.08
                )
                drivers.add(dot)

        all_text = Text("1 vs 19", font_size=20, color=TEXT_GRAY)
        all_text.next_to(f1_grid, DOWN, buff=0.2)

        self.play(
            Write(f1_label),
            Create(f1_grid),
            LaggedStart(*[FadeIn(d, scale=0.3) for d in drivers], lag_ratio=0.03),
            FadeIn(all_text, shift=UP * 0.2),
            run_time=1.5
        )

        # Problem statement
        problem = Text(
            "Elo designed for 2-player games, not 20-competitor races",
            font_size=24,
            color=ELO_GOLD
        )
        problem.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(problem, shift=UP * 0.3), run_time=1.5)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene6_2_PairwiseExplosion(Scene):
    """Scene 6.2: The Pairwise Explosion - 190 comparisons.

    Uses 6 drivers in a clean circle. Lines are drawn one-by-one with LaggedStart
    to avoid showing all connections simultaneously (visual mess).
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Combinatorial Explosion", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Formula - positioned at top-right, not overlapping circle
        formula = MathTex(
            r"\binom{20}{2} = \frac{20 \times 19}{2} = 190",
            font_size=36
        )
        formula.move_to(RIGHT * 4.5 + UP * 1.2)
        formula_box = SurroundingRectangle(formula, color=ELO_BLUE, buff=0.15, corner_radius=0.1)
        self.play(Write(formula), Create(formula_box), run_time=1.5)

        # Visual: 6 drivers in a circle (clean representation)
        n_drivers = 6
        circle_radius = 2.0
        driver_colors = [DRIVER_1, DRIVER_2, DRIVER_3, DRIVER_4, ELO_GOLD, ELO_GREEN]
        driver_names = ["VER", "HAM", "LEC", "PER", "ALO", "NOR"]

        drivers = VGroup()
        driver_positions = []
        for i in range(n_drivers):
            angle = (i / n_drivers) * TAU - PI / 2
            pos = circle_radius * np.array([np.cos(angle), np.sin(angle), 0])
            pos += LEFT * 2  # shift circle left to give room for formula
            driver_positions.append(pos)
            dot = Dot(pos, color=driver_colors[i], radius=0.14)
            name = Text(driver_names[i], font_size=14, color=driver_colors[i], weight=BOLD)
            name.next_to(dot, normalize(pos - (LEFT * 2)), buff=0.18)
            drivers.add(VGroup(dot, name))

        drivers.shift(DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in drivers], lag_ratio=0.1),
            run_time=1
        )

        # Build connections one by one with LaggedStart (not all at once)
        lines = []
        for i in range(n_drivers):
            for j in range(i + 1, n_drivers):
                pi = drivers[i][0].get_center()
                pj = drivers[j][0].get_center()
                line = Line(pi, pj, color=ELO_BLUE, stroke_opacity=0.4, stroke_width=1.2)
                lines.append(line)

        self.play(
            LaggedStart(*[Create(l) for l in lines], lag_ratio=0.08),
            run_time=2.5
        )

        # Count label: 6 drivers -> C(6,2) = 15 pairings shown
        count_label = Text("6 drivers = 15 pairings shown", font_size=18, color=TEXT_GRAY)
        count_label.move_to(RIGHT * 4.5 + DOWN * 0.2)

        actual_label = Text("20 drivers = 190 pairings!", font_size=22, color=ELO_GOLD, weight=BOLD)
        actual_label.move_to(RIGHT * 4.5 + DOWN * 1.0)
        actual_box = SurroundingRectangle(actual_label, color=ELO_GOLD, buff=0.1)

        self.play(FadeIn(count_label, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(actual_label, shift=UP * 0.2), Create(actual_box), run_time=0.8)

        # Caption
        caption = Text(
            "Each race creates 190 implicit 'matches' - most are meaningless",
            font_size=20,
            color=TEXT_LIGHT
        )
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.3), run_time=1.5)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene6_3_DNFAnomaly(Scene):
    """Scene 6.3: The DNF Anomaly - Punished for mechanical failure.

    Makes the '19 losses' more dramatic using a counter animation and
    color flash.
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The DNF Tragedy", font_size=48, color=ELO_RED)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Scenario (left)
        scenario = VGroup(
            Text("Race scenario:", font_size=24, color=TEXT_LIGHT),
            Text("  Verstappen leading by 30 seconds", font_size=20, color=ELO_BLUE),
            Text("  Lap 45 of 58", font_size=20, color=TEXT_GRAY),
            Text("  Engine failure  ->  DNF", font_size=20, color=ELO_RED)
        )
        scenario.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        scenario.move_to(LEFT * 3 + UP * 1.2)

        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in scenario], lag_ratio=0.2),
            run_time=1.2
        )

        # Timeline visualization (right)
        timeline = Line(LEFT * 2, RIGHT * 2, color=TEXT_GRAY)
        timeline.move_to(RIGHT * 2.5 + UP * 1)

        start_dot = Dot(timeline.get_left(), color=ELO_GREEN)
        start_label = Text("Lap 1", font_size=14, color=TEXT_GRAY)
        start_label.next_to(start_dot, DOWN, buff=0.1)

        dnf_dot = Dot(timeline.get_center() + RIGHT * 0.5, color=ELO_RED)
        # No emoji - use text only
        dnf_label = Text("DNF", font_size=16, color=ELO_RED, weight=BOLD)
        dnf_label.next_to(dnf_dot, UP, buff=0.1)

        self.play(
            Create(timeline),
            FadeIn(start_dot), FadeIn(start_label),
            FadeIn(dnf_dot), FadeIn(dnf_label),
            run_time=1
        )

        # Elo misinterpretation - dramatic (left)
        elo_title = Text("Elo interprets:", font_size=22, color=ELO_RED)
        elo_title.move_to(LEFT * 3 + DOWN * 0.2)

        lost_to_all = Text('"Lost to everyone"', font_size=22, color=ELO_RED, slant=ITALIC)
        lost_to_all.next_to(elo_title, DOWN, buff=0.1)

        self.play(FadeIn(elo_title, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(lost_to_all, shift=UP * 0.2), run_time=0.5)

        # Dramatic "19 losses" counter
        losses_box = RoundedRectangle(
            width=3.5, height=1.2, corner_radius=0.15,
            fill_color=ELO_RED, fill_opacity=0.2,
            stroke_color=ELO_RED, stroke_width=2
        )
        losses_box.move_to(LEFT * 3 + DOWN * 1.4)

        losses_label = Text("= 19 LOSSES", font_size=36, color=ELO_RED, weight=BOLD)
        losses_label.move_to(losses_box)

        self.play(FadeIn(losses_box), run_time=0.3)
        self.play(Write(losses_label), run_time=0.5)
        self.play(Indicate(losses_label, color=ELO_RED, scale_factor=1.2), run_time=0.5)
        self.play(Indicate(losses_label, color=WARNING, scale_factor=1.1), run_time=0.4)

        # Rating plummet visualization
        bar_baseline = DOWN * 1.8
        rating_before = Rectangle(width=0.7, height=2.5,
                                   fill_color=ELO_BLUE, fill_opacity=0.7, stroke_width=0)
        rating_before.move_to(RIGHT * 1.8 + DOWN * 1.55)
        rating_before.align_to(bar_baseline, DOWN)
        label_before = Text("2800", font_size=16, color=ELO_BLUE)
        label_before.next_to(rating_before, UP, buff=0.1)

        rating_after = Rectangle(width=0.7, height=1.5,
                                  fill_color=ELO_RED, fill_opacity=0.7, stroke_width=0)
        rating_after.align_to(bar_baseline, DOWN)
        rating_after.move_to(RIGHT * 3.2 + DOWN * 2.05)
        rating_after.align_to(bar_baseline, DOWN)
        label_after = Text("2650", font_size=16, color=ELO_RED)
        label_after.next_to(rating_after, UP, buff=0.1)

        drop_arrow = Arrow(
            rating_before.get_top() + RIGHT * 0.35,
            rating_after.get_top() + LEFT * 0.35,
            color=ELO_RED, stroke_width=2
        )
        drop_label = Text("-150!", font_size=22, color=ELO_RED, weight=BOLD)
        drop_label.next_to(drop_arrow, UP, buff=0.1)

        self.play(FadeIn(rating_before), FadeIn(label_before), run_time=0.5)
        self.play(
            FadeIn(rating_after), FadeIn(label_after),
            Create(drop_arrow), FadeIn(drop_label),
            run_time=1
        )

        # Caption
        caption = Text(
            "Mechanical failure != Skill failure",
            font_size=24, color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(caption, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene6_4_CarVsDriver(Scene):
    """Scene 6.4: The Car vs Driver Problem - Entanglement."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Entanglement Problem", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # What Elo sees (left)
        elo_box = RoundedRectangle(
            width=3.2, height=2.0, corner_radius=0.15,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_BLUE, stroke_width=1.5
        )
        elo_box.move_to(LEFT * 4 + UP * 0.5)

        elo_title = Text("What Elo sees:", font_size=20, color=TEXT_GRAY)
        elo_title.move_to(elo_box.get_top() + DOWN * 0.35)

        elo_inner = Rectangle(width=2.0, height=0.9,
                               fill_color=ELO_BLUE, fill_opacity=0.5,
                               stroke_color=ELO_BLUE)
        elo_inner.move_to(elo_box.get_center() + DOWN * 0.2)

        elo_inner_label = Text('"Agent" perf.', font_size=16, color=TEXT_GRAY)
        elo_inner_label.move_to(elo_inner)

        self.play(
            FadeIn(elo_box), FadeIn(elo_title),
            FadeIn(elo_inner), FadeIn(elo_inner_label),
            run_time=1
        )

        # Reality (right) - stacked components
        reality_title = Text("Reality:", font_size=20, color=ELO_GOLD)
        reality_title.move_to(RIGHT * 2 + UP * 2.1)
        self.play(FadeIn(reality_title, shift=LEFT * 0.2), run_time=0.5)

        car = Rectangle(width=2.2, height=0.9,
                        fill_color=ELO_GOLD, fill_opacity=0.7,
                        stroke_color=ELO_GOLD)
        car_label = Text("Car Performance", font_size=14, color=TEXT_WHITE, weight=BOLD)
        car_label.move_to(car)

        driver = Rectangle(width=2.2, height=0.9,
                           fill_color=ELO_BLUE, fill_opacity=0.7,
                           stroke_color=ELO_BLUE)
        driver_label = Text("Driver Skill", font_size=14, color=TEXT_WHITE, weight=BOLD)
        driver_label.move_to(driver)

        stacked = VGroup(car, driver)
        stacked.arrange(UP, buff=0)
        stacked.move_to(RIGHT * 2 + UP * 0.5)

        self.play(FadeIn(car), FadeIn(car_label), run_time=0.5)
        self.play(FadeIn(driver), FadeIn(driver_label), run_time=0.5)

        plus = MathTex("+", font_size=36, color=TEXT_WHITE)
        plus.move_to(car.get_top())
        self.play(Write(plus), run_time=0.3)

        # Equals observed result
        equals = MathTex("=", font_size=36, color=TEXT_WHITE)
        equals.move_to(RIGHT * 2 + DOWN * 1.0)

        observed = Rectangle(width=2.2, height=0.8,
                              fill_color=ELO_GREEN, fill_opacity=0.5,
                              stroke_color=ELO_GREEN)
        observed_label = Text("Observed Result", font_size=14, color=TEXT_WHITE)
        observed_label.move_to(observed)
        observed.next_to(equals, DOWN, buff=0.15)
        observed_label.move_to(observed)

        self.play(Write(equals), FadeIn(observed), FadeIn(observed_label), run_time=0.8)

        # Problem statement
        problem_box = RoundedRectangle(
            width=9, height=0.9, corner_radius=0.1,
            fill_color=ELO_RED, fill_opacity=0.15,
            stroke_color=ELO_RED, stroke_width=1.5
        )
        problem_box.to_edge(DOWN, buff=0.5)
        problem = Text(
            "Standard Elo sees only the sum, not the components",
            font_size=22, color=ELO_RED
        )
        problem.move_to(problem_box)
        self.play(FadeIn(problem_box), FadeIn(problem, shift=UP * 0.2), run_time=1.5)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene6_5_RussellExample(Scene):
    """Scene 6.5: The Russell Example - Car change proves the point."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The George Russell Effect", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Split screen
        divider = Line(UP * 2, DOWN * 2, color=TEXT_GRAY)
        self.play(Create(divider), run_time=0.3)

        # Left: Williams
        williams = VGroup(
            Text("2020: Williams", font_size=24, color=TEXT_GRAY),
            Rectangle(width=2.5, height=1.5, fill_color="#005AFF", fill_opacity=0.5),
            Text("Backmarker car", font_size=18, color=TEXT_GRAY),
            Text("P15-P20 finishes", font_size=16, color=TEXT_GRAY),
            MathTex(r"R_{Russell} \approx 1800", font_size=24, color=TEXT_GRAY)
        )
        williams.arrange(DOWN, buff=0.2)
        williams.move_to(LEFT * 3.5 + DOWN * 0.3)
        self.play(FadeIn(williams, shift=RIGHT * 0.3), run_time=1)

        # Arrow
        arrow = Arrow(LEFT * 1, RIGHT * 1, color=ELO_GOLD)
        arrow.move_to(DOWN * 0.3)
        arrow_label = Text("Same driver!", font_size=18, color=ELO_GOLD, weight=BOLD)
        arrow_label.next_to(arrow, UP, buff=0.1)
        self.play(Create(arrow), FadeIn(arrow_label), run_time=0.8)

        # Right: Mercedes
        mercedes = VGroup(
            Text("2020: Mercedes (sub)", font_size=24, color=ELO_BLUE),
            Rectangle(width=2.5, height=1.5, fill_color="#00D2BE", fill_opacity=0.5),
            Text("Championship car", font_size=18, color=ELO_GREEN),
            Text("P2 at Sakhir GP", font_size=16, color=ELO_GREEN),
            MathTex(r"R_{Russell} \approx 2400?", font_size=24, color=ELO_GREEN)
        )
        mercedes.arrange(DOWN, buff=0.2)
        mercedes.move_to(RIGHT * 3.5 + DOWN * 0.3)
        self.play(FadeIn(mercedes, shift=LEFT * 0.3), run_time=1)

        # Question
        question = VGroup(
            Text("Did Russell suddenly become", font_size=24, color=TEXT_LIGHT),
            Text("600 rating points better?", font_size=24, color=ELO_GOLD)
        )
        question.arrange(DOWN, buff=0.1)
        question.move_to(DOWN * 2.5)
        self.play(
            LaggedStart(*[FadeIn(q, shift=UP * 0.2) for q in question], lag_ratio=0.3),
            run_time=1
        )
        self.wait(1)

        # Answer
        answer_box = RoundedRectangle(
            width=8, height=0.8, corner_radius=0.1,
            fill_color=ELO_RED, fill_opacity=0.2,
            stroke_color=ELO_RED, stroke_width=2
        )
        answer_box.to_edge(DOWN, buff=0.3)
        answer = Text(
            "NO - the CAR changed, not the driver!",
            font_size=24, color=ELO_RED, weight=BOLD
        )
        answer.move_to(answer_box)
        self.play(FadeIn(answer_box), Write(answer, run_time=1))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene6_6_AdvancedSolutionsPreview(Scene):
    """Scene 6.6: Advanced Solutions Preview."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("We Need Better Models", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1)

        # Problems summary (left)
        problems_title = Text("Elo Fails At:", font_size=22, color=ELO_RED)
        problems_title.move_to(LEFT * 3.5 + UP * 1.2)

        problems = VGroup(
            Text("Binary comparisons only", font_size=22, color=ELO_RED),
            Text("DNF handling", font_size=22, color=ELO_RED),
            Text("Car vs driver entanglement", font_size=22, color=ELO_RED)
        )
        problems.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        problems.next_to(problems_title, DOWN, buff=0.15)

        self.play(FadeIn(problems_title, shift=DOWN * 0.2), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in problems], lag_ratio=0.2),
            run_time=1
        )

        # Arrow
        arrow = Arrow(LEFT * 1, RIGHT * 1, color=ELO_GREEN, stroke_width=3)
        arrow.move_to(UP * 0.5)
        self.play(Create(arrow), run_time=0.5)

        # Solutions (right)
        solutions_title = Text("Better Approaches:", font_size=22, color=ELO_GREEN)
        solutions_title.move_to(RIGHT * 3.5 + UP * 1.2)

        solutions = VGroup(
            Text("Rank-ordered models", font_size=22, color=ELO_GREEN),
            Text("Survival analysis", font_size=22, color=ELO_GREEN),
            Text("Hierarchical decomposition", font_size=22, color=ELO_GREEN)
        )
        solutions.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        solutions.next_to(solutions_title, DOWN, buff=0.15)

        self.play(FadeIn(solutions_title, shift=DOWN * 0.2), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(s, shift=LEFT * 0.2) for s in solutions], lag_ratio=0.2),
            run_time=1
        )

        # Key insight box
        insight_box = RoundedRectangle(
            width=8, height=1.6, corner_radius=0.15,
            fill_color=ELO_GOLD, fill_opacity=0.12,
            stroke_color=ELO_GOLD, stroke_width=2
        )
        insight_box.move_to(DOWN * 1.8)

        insight = VGroup(
            Text("Key Insight:", font_size=22, color=ELO_GOLD, weight=BOLD),
            Text("Move from point estimates to probability distributions", font_size=19, color=TEXT_LIGHT)
        )
        insight.arrange(DOWN, buff=0.1)
        insight.move_to(insight_box)

        self.play(FadeIn(insight_box), FadeIn(insight, shift=UP * 0.2), run_time=1.5)

        # Caption
        caption = Text(
            "Enter: Bayesian Statistics",
            font_size=28, color=ELO_BLUE, weight=BOLD
        )
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
