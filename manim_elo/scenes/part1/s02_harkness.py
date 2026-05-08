# Section 2: The Pre-Probabilistic Era - Harkness System
# 5 Scenes covering the failures of linear ranking

from manim import *
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *
import numpy as np


class Scene2_1_NeedForRanking(Scene):
    """Scene 2.1: The Need for Ranking - Pre-rating chaos."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Before the Elo System", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1.5)

        # Chaotic labels
        labels = ["Master", "Novice", "Strong", "Weak", "Expert", "Beginner"]
        positions = [
            LEFT * 3.5 + UP * 1.2,
            RIGHT * 3.0 + UP * 1.8,
            LEFT * 1.5 + DOWN * 0.5,
            RIGHT * 3.5 + UP * 0.2,
            ORIGIN + UP * 1.2,
            LEFT * 3.0 + DOWN * 1.8
        ]
        colors_list = [ELO_BLUE, TEXT_GRAY, ELO_GOLD, TEXT_GRAY, ELO_GREEN, TEXT_GRAY]

        chaos_group = VGroup()
        for label, pos, col in zip(labels, positions, colors_list):
            text = Text(label, font_size=26, color=col)
            text.move_to(pos)
            chaos_group.add(text)

        self.play(
            LaggedStart(*[FadeIn(t, scale=0.6) for t in chaos_group], lag_ratio=0.08),
            run_time=4.8
        )

        # Random jitter (2D only - no z-component)
        np.random.seed(42)
        shifts = [(np.random.uniform(-0.4, 0.4), np.random.uniform(-0.3, 0.3)) for _ in labels]
        self.play(
            *[t.animate.shift(RIGHT * sx + UP * sy)
              for t, (sx, sy) in zip(chaos_group, shifts)],
            run_time=3.2, rate_func=there_and_back
        )

        # USCF appears
        uscf = Text("USCF", font_size=72, color=ELO_GOLD, weight=BOLD)
        uscf.move_to(ORIGIN + DOWN * 0.2)

        uscf_sub = Text("United States Chess Federation", font_size=22, color=TEXT_GRAY)
        uscf_sub.next_to(uscf, DOWN, buff=0.3)

        self.play(
            chaos_group.animate.set_opacity(0.2),
            FadeIn(uscf, scale=0.7),
            run_time=3.6
        )
        self.play(FadeIn(uscf_sub, shift=UP * 0.2), run_time=2)

        # Harkness intro
        intro_box = Rectangle(
            width=8, height=0.9,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_BLUE, stroke_width=1.5
        )
        intro_box.to_edge(DOWN, buff=0.7)
        intro_text = Text(
            "Kenneth Harkness proposes a solution - 1950s",
            font_size=24, color=TEXT_LIGHT
        )
        intro_text.move_to(intro_box)

        self.play(FadeIn(intro_box), Write(intro_text, run_time=4.8))
        self.wait(30)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene2_2_LinearMechanics(Scene):
    """Scene 2.2: The Mechanics of Linear Approximation."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Harkness Formula", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1.5)

        # ---- Top half: Two formula boxes side by side ----
        # Formula for scores >= 50%
        box_high = Rectangle(
            width=5.5, height=2.2,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_GREEN, stroke_width=1.5
        )
        box_high.move_to(LEFT * 3 + UP * 0.7)

        high_label = Text("Score >= 50%", font_size=20, color=ELO_GREEN)
        high_label.move_to(box_high.get_top() + DOWN * 0.35)

        formula_high = MathTex(
            r"P_r = R_{avg} + 10 \times (P\% - 50)",
            font_size=30, color=TEXT_WHITE
        )
        formula_high.move_to(box_high.get_center() + DOWN * 0.15)

        # Formula for scores < 50%
        box_low = Rectangle(
            width=5.5, height=2.2,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_RED, stroke_width=1.5
        )
        box_low.move_to(RIGHT * 3 + UP * 0.7)

        low_label = Text("Score < 50%", font_size=20, color=ELO_RED)
        low_label.move_to(box_low.get_top() + DOWN * 0.35)

        formula_low = MathTex(
            r"P_r = R_{avg} - 10 \times (50 - P\%)",
            font_size=30, color=TEXT_WHITE
        )
        formula_low.move_to(box_low.get_center() + DOWN * 0.15)

        self.play(
            FadeIn(box_high), FadeIn(high_label), Write(formula_high, run_time=4),
            run_time=4.8
        )
        self.play(
            FadeIn(box_low), FadeIn(low_label), Write(formula_low, run_time=4),
            run_time=4.8
        )

        # ---- Bottom half: Number line (separated from formulas) ----
        axes = Axes(
            x_range=[-500, 500, 100],
            y_range=[0, 100, 25],
            x_length=9, y_length=1.8,
            axis_config={"include_numbers": True, "font_size": 14},
            tips=False
        )
        axes.move_to(DOWN * 2.1)

        x_label = Text("Rating diff from opponents", font_size=16, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.25)
        y_label = Text("Score %", font_size=14, color=TEXT_GRAY)
        y_label.next_to(axes, LEFT, buff=0.1)
        y_label.rotate(90 * DEGREES)

        linear_line = axes.plot(lambda x: 50 + x * 0.1, x_range=[-500, 500], color=ELO_GOLD)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=3.2)
        self.play(Create(linear_line), run_time=4)

        # Key point annotations with rounded backgrounds so they stand out from the line
        for x_val, label_str, col in [(-500, "0%", ELO_RED), (0, "50%", TEXT_GRAY), (500, "100%", ELO_GREEN)]:
            dot = Dot(axes.c2p(x_val, 50 + x_val * 0.1), color=col, radius=0.1)
            ann = Text(label_str, font_size=14, color=col)
            ann.next_to(dot, UP, buff=0.12)
            ann_bg = RoundedRectangle(
                width=ann.width + 0.2, height=ann.height + 0.16,
                corner_radius=0.1,
                fill_color=DARK_BG, fill_opacity=0.75, stroke_width=0
            )
            ann_bg.move_to(ann)
            self.play(FadeIn(dot), FadeIn(ann_bg), FadeIn(ann), run_time=1.2)

        self.wait(30)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene2_3_LosingWinnerParadox(MovingCameraScene):
    """Scene 2.3: The Losing Winner Paradox - fatal flaw."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The 'Losing Winner' Paradox", font_size=44, color=ELO_RED)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)

        # Scenario box (left column)
        scenario_box = Rectangle(
            width=4.8, height=3.5,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_BLUE, stroke_width=1.5
        )
        scenario_box.move_to(LEFT * 3.2 + UP * 0.3)

        scenario_title = Text("Scenario", font_size=22, color=ELO_BLUE)
        scenario_title.move_to(scenario_box.get_top() + DOWN * 0.4)

        details = VGroup(
            Text("Club player rating: 1500", font_size=18, color=TEXT_LIGHT),
            Text("Enters elite tournament", font_size=18, color=TEXT_GRAY),
            Text("Avg opponent rating: 2200", font_size=18, color=ELO_GOLD),
            Text("Loses ALL games (0%)", font_size=18, color=ELO_RED),
        )
        details.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        details.next_to(scenario_title, DOWN, buff=0.25)

        self.play(FadeIn(scenario_box), Write(scenario_title), run_time=2.4)
        self.play(
            LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in details], lag_ratio=0.15),
            run_time=4.8
        )

        # Calculation box (right column)
        calc_box = Rectangle(
            width=5.2, height=3.5,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_GOLD, stroke_width=1.5
        )
        calc_box.move_to(RIGHT * 3 + UP * 0.3)

        calc_title = Text("Harkness Calculation", font_size=22, color=ELO_GOLD)
        calc_title.move_to(calc_box.get_top() + DOWN * 0.4)

        calc_steps = VGroup(
            MathTex(r"P_r = 2200 - 10 \times (50 - 0)", font_size=26),
            MathTex(r"= 2200 - 500", font_size=26),
            MathTex(r"= 1700", font_size=30, color=ELO_RED),
        )
        calc_steps.arrange(DOWN, buff=0.22)
        calc_steps.next_to(calc_title, DOWN, buff=0.3)

        self.play(FadeIn(calc_box), Write(calc_title), run_time=2.4)
        for step in calc_steps:
            self.play(Write(step), run_time=2.8)

        # Box around result and indicate it
        result_box = SurroundingRectangle(calc_steps[-1], color=ELO_RED, buff=0.12, stroke_width=2)
        self.play(Create(result_box), run_time=1.6)
        self.play(Indicate(calc_steps[-1], color=ELO_RED, scale_factor=1.1), run_time=2.4)

        # Zoom into the paradox result for emphasis
        self.play(
            self.camera.frame.animate.scale(0.55).move_to(calc_steps[-1].get_center()),
            run_time=3.2
        )
        self.wait(12)
        self.play(
            self.camera.frame.animate.scale(1 / 0.55).move_to(ORIGIN),
            run_time=2.8
        )

        # Bottom: clear explanation of what 1700 means
        # 1700 is the PERFORMANCE RATING for this tournament, not the new rating directly.
        # When averaged with current 1500 rating, actual rating RISES despite losing every game.
        explanation = VGroup(
            Text("1700 = performance rating for this tournament", font_size=19, color=ELO_GOLD),
            Text("(200 pts ABOVE current rating of 1500!)", font_size=19, color=ELO_GOLD),
            Text("When averaged in: actual rating RISES despite losing every game", font_size=18, color=ELO_RED),
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        explanation.to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(e, shift=UP * 0.3) for e in explanation], lag_ratio=0.3),
            run_time=4.8
        )
        self.wait(30)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene2_4_EliteNotProtected(Scene):
    """Scene 2.4: Lack of Protection for the Elite."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Elite Problem", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)

        # Scenario (left)
        scenario = VGroup(
            Text("Grandmaster rating:  2600", font_size=22, color=ELO_GOLD),
            Text("Enters amateur tournament", font_size=22, color=TEXT_GRAY),
            Text("Avg opponent rating:  1400", font_size=22, color=TEXT_GRAY),
            Text("Wins ALL games (100%)", font_size=22, color=ELO_GREEN),
        )
        scenario.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        scenario.move_to(LEFT * 3.3 + UP * 0.8)

        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in scenario], lag_ratio=0.15),
            run_time=4.8
        )

        # Calculation (right)
        calc = VGroup(
            MathTex(r"P_r = 1400 + 10 \times (100 - 50)", font_size=26),
            MathTex(r"= 1400 + 500", font_size=26),
            MathTex(r"= 1900", font_size=30, color=ELO_RED),
        )
        calc.arrange(DOWN, buff=0.22)
        calc.move_to(RIGHT * 3 + UP * 0.8)

        for step in calc:
            self.play(Write(step), run_time=2.8)

        result_box = SurroundingRectangle(calc[-1], color=ELO_RED, buff=0.1)
        self.play(Create(result_box), run_time=1.6)

        # Rating bar visualization
        bar_axes = Axes(
            x_range=[0, 3, 1], y_range=[0, 3000, 500],
            x_length=4, y_length=3.5,
            axis_config={"include_numbers": False, "font_size": 14},
            tips=False
        )
        bar_axes.move_to(LEFT * 1 + DOWN * 1.2)

        y_label = Text("Rating", font_size=14, color=TEXT_GRAY)
        y_label.next_to(bar_axes.y_axis, LEFT, buff=0.15)
        y_label.rotate(90 * DEGREES)

        self.play(Create(bar_axes), FadeIn(y_label), run_time=2.4)

        # Before bar (2600)
        before_bar = Rectangle(
            width=0.8, height=abs(bar_axes.c2p(1, 2600)[1] - bar_axes.c2p(1, 0)[1]),
            fill_color=ELO_BLUE, fill_opacity=0.8, stroke_width=0
        )
        before_bar.align_to(bar_axes.c2p(1, 0), DOWN)
        before_bar.move_to(bar_axes.c2p(1, 0), aligned_edge=DOWN)

        before_label = Text("2600", font_size=16, color=ELO_BLUE)
        before_label.next_to(before_bar, UP, buff=0.1)
        before_label_bg = RoundedRectangle(
            width=before_label.width + 0.2, height=before_label.height + 0.16,
            corner_radius=0.12, fill_color=BLACK, fill_opacity=0.55, stroke_width=0
        )
        before_label_bg.move_to(before_label)
        before_title = Text("Before", font_size=15, color=TEXT_GRAY)
        before_title.next_to(before_bar, DOWN, buff=0.1)

        # After bar (lower due to performance rating of 1900)
        after_bar = Rectangle(
            width=0.8, height=abs(bar_axes.c2p(2, 2500)[1] - bar_axes.c2p(2, 0)[1]),
            fill_color=ELO_RED, fill_opacity=0.8, stroke_width=0
        )
        after_bar.align_to(bar_axes.c2p(2, 0), DOWN)
        after_bar.move_to(bar_axes.c2p(2, 0), aligned_edge=DOWN)

        after_label = Text("~2500", font_size=16, color=ELO_RED)
        after_label.next_to(after_bar, UP, buff=0.1)
        after_label_bg = RoundedRectangle(
            width=after_label.width + 0.2, height=after_label.height + 0.16,
            corner_radius=0.12, fill_color=BLACK, fill_opacity=0.55, stroke_width=0
        )
        after_label_bg.move_to(after_label)
        after_title = Text("After", font_size=15, color=TEXT_GRAY)
        after_title.next_to(after_bar, DOWN, buff=0.1)

        drop_arrow = Arrow(
            before_bar.get_top() + RIGHT * 0.4,
            after_bar.get_top() + LEFT * 0.4,
            color=ELO_RED, buff=0.05, stroke_width=2
        )
        drop_text = Text("-100 pts!", font_size=18, color=ELO_RED)
        drop_text.next_to(drop_arrow, UP, buff=0.1)
        drop_text_bg = RoundedRectangle(
            width=drop_text.width + 0.2, height=drop_text.height + 0.16,
            corner_radius=0.12, fill_color=BLACK, fill_opacity=0.55, stroke_width=0
        )
        drop_text_bg.move_to(drop_text)

        self.play(FadeIn(before_bar), FadeIn(before_label_bg), FadeIn(before_label),
                  FadeIn(before_title), run_time=2)
        self.play(FadeIn(after_bar), FadeIn(after_label_bg), FadeIn(after_label),
                  FadeIn(after_title), Create(drop_arrow),
                  FadeIn(drop_text_bg), FadeIn(drop_text), run_time=3.6)

        caption = Text(
            "Punished for winning!  Elite players avoid open tournaments.",
            font_size=22, color=ELO_RED
        )
        caption.to_edge(DOWN, buff=0.5)
        caption_bg = RoundedRectangle(
            width=caption.width + 0.4, height=caption.height + 0.3,
            corner_radius=0.12, fill_color=BLACK, fill_opacity=0.75, stroke_width=0
        )
        caption_bg.move_to(caption)
        self.play(FadeIn(caption_bg), FadeIn(caption, shift=UP * 0.3), run_time=4)
        self.wait(30)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene2_5_NeedForProbability(MovingCameraScene):
    """Scene 2.5: The Need for Probability - Linear vs Reality."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Core Insight", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1.5)

        axes = Axes(
            x_range=[-500, 500, 100],
            y_range=[0, 100, 25],
            x_length=9, y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 14},
            tips=False
        )
        axes.shift(UP * 0.2)

        x_label = Text("Rating Difference (A - B)", font_size=16, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Win %", font_size=16, color=TEXT_GRAY)
        y_label.next_to(axes, LEFT, buff=0.3)
        y_label.rotate(90 * DEGREES)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=3.6)

        # Harkness (linear)
        linear_graph = axes.plot(
            lambda x: min(100, max(0, 50 + x * 0.1)),
            x_range=[-500, 500], color=ELO_RED, stroke_width=3
        )
        linear_label = Text("Harkness  (Linear)", font_size=18, color=ELO_RED)
        linear_label.next_to(axes.c2p(250, 80), UP * 0.5)
        linear_label_bg = BackgroundRectangle(linear_label, fill_opacity=0.75, buff=0.06)

        self.play(Create(linear_graph), FadeIn(linear_label_bg), FadeIn(linear_label), run_time=4.8)
        self.wait(8)

        # Reality (S-curve / logistic)
        def sigmoid_pct(x):
            return 100 / (1 + 10 ** (-x / 400))

        prob_graph = axes.plot(sigmoid_pct, x_range=[-500, 500],
                               color=ELO_GREEN, stroke_width=3)
        prob_label = Text("Reality  (S-curve)", font_size=18, color=ELO_GREEN)
        prob_label.next_to(axes.c2p(-250, 22), DOWN * 0.5)
        prob_label_bg = BackgroundRectangle(prob_label, fill_opacity=0.75, buff=0.06)

        self.play(Create(prob_graph), FadeIn(prob_label_bg), FadeIn(prob_label), run_time=4.8)

        # Highlight problematic regions
        bad_dot = Dot(axes.c2p(-500, 0), color=ELO_RED, radius=0.12)
        good_dot = Dot(axes.c2p(-500, sigmoid_pct(-500)), color=ELO_GREEN, radius=0.12)

        bad_ann = Text("Linear: impossible (0%)", font_size=13, color=ELO_RED)
        bad_ann.next_to(bad_dot, LEFT, buff=0.1)
        bad_ann_bg = BackgroundRectangle(bad_ann, fill_opacity=0.80, buff=0.05)
        good_ann = Text("Reality: ~3%\n(upsets DO happen)", font_size=13, color=ELO_GREEN)
        good_ann.next_to(good_dot, UP, buff=0.1)
        good_ann_bg = BackgroundRectangle(good_ann, fill_opacity=0.80, buff=0.05)

        self.play(FadeIn(bad_dot), FadeIn(good_dot), run_time=2)
        self.play(FadeIn(bad_ann_bg), FadeIn(bad_ann), FadeIn(good_ann_bg), FadeIn(good_ann), run_time=3.2)

        # Zoom into the extreme left to highlight the difference in models
        self.play(
            self.camera.frame.animate.scale(0.55).move_to(axes.c2p(-490, 50)),
            run_time=3.6
        )
        self.wait(12)
        self.play(
            self.camera.frame.animate.scale(1 / 0.55).move_to(ORIGIN),
            run_time=2.8
        )

        caption = Text(
            "Linear model fails at the extremes - we need probability!",
            font_size=24, color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption, shift=UP * 0.3), run_time=4)
        self.wait(30)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)
