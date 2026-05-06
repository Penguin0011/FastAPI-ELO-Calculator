# Section 4: The Update Mechanism & K-Factor
from manim import *
from manim.utils.color.core import interpolate_color as manim_interpolate_color
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *
import numpy as np


class Scene4_1_FeedbackLoop(Scene):
    """Scene 4.1: The Feedback Loop."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Self-Correcting Loop", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1.5)

        stages = [
            ("PREDICT", ELO_BLUE, 90),
            ("OBSERVE", ELO_GREEN, 0),
            ("CORRECT", ELO_GOLD, -90),
            ("REPEAT", TEXT_GRAY, 180),
        ]

        radius = 2.2
        boxes = VGroup()
        for label, color, angle_deg in stages:
            angle_rad = angle_deg * DEGREES
            pos = radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])

            box = RoundedRectangle(
                width=2.0, height=0.8, corner_radius=0.15,
                fill_color=color, fill_opacity=0.2,
                stroke_color=color, stroke_width=2
            )
            box.move_to(pos)

            text = Text(label, font_size=20, color=color, weight=BOLD)
            text.move_to(box)

            boxes.add(VGroup(box, text))

        boxes.move_to(ORIGIN + DOWN * 0.2)

        for b in boxes:
            self.play(FadeIn(b), run_time=1.6)

        # Curved arrows between stages — one per step to show clockwise flow clearly
        for i in range(4):
            ni = (i + 1) % 4
            start_c = boxes[i][0].get_center()
            end_c = boxes[ni][0].get_center()

            diff = end_c - start_c
            mag = np.sqrt(diff[0] ** 2 + diff[1] ** 2 + diff[2] ** 2)
            direction = diff / mag

            # Offset start/end to box edges (half-width ≈ 1.05)
            start_pt = start_c + direction * 1.05
            end_pt = end_c - direction * 1.05

            arrow = CurvedArrow(
                start_pt, end_pt,
                angle=PI / 3,
                color=TEXT_LIGHT,
                stroke_width=2.5
            )
            self.play(Create(arrow), run_time=1.0)

        # Caption
        caption = Text(
            "Rating oscillates toward true skill through iterative correction",
            font_size=20, color=TEXT_LIGHT
        )
        caption.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(caption, shift=UP * 0.3), run_time=4)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene4_2_UpdateEquation(MovingCameraScene):
    """Scene 4.2: The Update Equation."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Update Equation", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1.5)

        # Main formula - centered, large
        formula = MathTex(
            r"R'_A", r"=", r"R_A", r"+", r"K", r"(", r"S_A", r"-", r"E_A", r")",
            font_size=60
        )
        formula[0].set_color(ELO_GREEN)   # R'_A
        formula[2].set_color(ELO_BLUE)    # R_A
        formula[4].set_color(ELO_GOLD)    # K
        formula[6].set_color(ELO_GREEN)   # S_A
        formula[8].set_color(ELO_RED)     # E_A
        formula.move_to(UP * 1.2)

        self.play(Write(formula, run_time=8))
        self.wait(1.2)

        # Zoom in on the full formula before annotating
        self.play(
            self.camera.frame.animate.scale(0.65).move_to(formula.get_center()),
            run_time=3.2
        )
        self.wait(2.8)
        self.play(
            self.camera.frame.animate.scale(1 / 0.65).move_to(ORIGIN),
            run_time=2.8
        )

        # Brace labels - use Brace for clean formula annotation
        labels_data = [
            (formula[2], "Old Rating", ELO_BLUE, DOWN),
            (formula[4], "Sensitivity", ELO_GOLD, UP),
            (formula[6], "Actual\nScore", ELO_GREEN, DOWN),
            (formula[8], "Expected\nScore", ELO_RED, DOWN),
        ]

        braces = VGroup()
        for target, text, color, direction in labels_data:
            brace = Brace(target, direction, color=color)
            lbl = brace.get_text(text)
            lbl.set_color(color)
            braces.add(VGroup(brace, lbl))

        self.play(
            LaggedStart(*[GrowFromCenter(b[0]) for b in braces], lag_ratio=0.1),
            LaggedStart(*[FadeIn(b[1]) for b in braces], lag_ratio=0.1),
            run_time=6
        )

        # Surprise factor highlight
        surprise_eq = MathTex(r"\underbrace{S_A - E_A}_{\text{Surprise Factor}}", font_size=36, color=ELO_PURPLE)
        surprise_eq.move_to(DOWN * 2.5)

        surprise_box = SurroundingRectangle(surprise_eq, color=ELO_PURPLE, buff=0.2, corner_radius=0.1)

        self.play(Write(surprise_eq), Create(surprise_box), run_time=4)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene4_3_OutperformanceExample(Scene):
    """Scene 4.3: Outperformance - Rating rises."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Outperformance  ->  Rating Rises", font_size=40, color=ELO_GREEN)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1.5)

        # Scenario (left)
        scenario = VGroup(
            Text("Expected score:  E = 0.30  (30%)", font_size=20, color=TEXT_GRAY),
            Text("Actual result:    S = 1.0  (Win)", font_size=20, color=ELO_GREEN),
            Text("K-factor:         K = 32", font_size=20, color=ELO_GOLD),
        )
        scenario.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        scenario.move_to(LEFT * 3.5 + UP * 1)

        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in scenario], lag_ratio=0.15),
            run_time=4
        )

        # Calculation (right)
        calc = VGroup(
            MathTex(r"\Delta = S - E = 1.0 - 0.30 = +0.70", font_size=26, color=ELO_GREEN),
            MathTex(r"R' = 1500 + 32 \times 0.70", font_size=26),
            MathTex(r"R' = 1500 + 22.4", font_size=26),
            MathTex(r"R' = 1522", font_size=32, color=ELO_GREEN),
        )
        calc.arrange(DOWN, buff=0.2)
        calc.move_to(RIGHT * 2.5 + UP * 1)

        for step in calc:
            self.play(Write(step), run_time=2.4)

        result_box = SurroundingRectangle(calc[-1], color=ELO_GREEN, buff=0.12)
        self.play(Create(result_box), run_time=1.6)
        self.play(Indicate(calc[-1], color=ELO_GREEN, scale_factor=1.1), run_time=2)

        # Rating bar visualization
        bar_g = VGroup()
        for x, h, col, label in [(-1.5, 1.5, ELO_BLUE, "1500"), (1.5, 1.72, ELO_GREEN, "1522")]:
            bar = Rectangle(
                width=0.8, height=h,
                fill_color=col, fill_opacity=0.8, stroke_width=0
            )
            bar.move_to([x, -2.8 + h / 2, 0])
            lbl = Text(label, font_size=18, color=col)
            lbl.next_to(bar, DOWN, buff=0.1)
            title = Text("Before" if x < 0 else "After", font_size=15, color=TEXT_GRAY)
            title.next_to(bar, UP, buff=0.1)
            bar_g.add(VGroup(bar, lbl, title))

        rise_arrow = Arrow(
            bar_g[0][0].get_right() + RIGHT * 0.1,
            bar_g[1][0].get_left() + LEFT * 0.1,
            color=ELO_GREEN, buff=0, stroke_width=2
        )
        rise_text = Text("+22 pts", font_size=18, color=ELO_GREEN)
        rise_text.next_to(rise_arrow, UP, buff=0.1)

        self.play(FadeIn(bar_g[0]), run_time=1.6)
        self.play(FadeIn(bar_g[1]), Create(rise_arrow), FadeIn(rise_text), run_time=3.6)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene4_4_UnderperformanceExample(Scene):
    """Scene 4.4: Underperformance - Rating drops.

    FIXED: 32 * 0.80 = 25.6 (not 26).
    Label correctly shows -25.6 pts.
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Underperformance  ->  Rating Drops", font_size=40, color=ELO_RED)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1.5)

        # Scenario
        scenario = VGroup(
            Text("Expected score:  E = 0.80  (80%)", font_size=20, color=TEXT_GRAY),
            Text("Actual result:    S = 0.0  (Loss)", font_size=20, color=ELO_RED),
            Text("K-factor:         K = 32", font_size=20, color=ELO_GOLD),
        )
        scenario.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        scenario.move_to(LEFT * 3.5 + UP * 1)

        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in scenario], lag_ratio=0.15),
            run_time=4
        )

        # Calculation - FIXED: 32 * 0.80 = 25.6
        calc = VGroup(
            MathTex(r"\Delta = S - E = 0.0 - 0.80 = -0.80", font_size=26, color=ELO_RED),
            MathTex(r"R' = 2000 + 32 \times (-0.80)", font_size=26),
            MathTex(r"R' = 2000 - 25.6", font_size=26),
            MathTex(r"R' = 1974.4", font_size=32, color=ELO_RED),
        )
        calc.arrange(DOWN, buff=0.2)
        calc.move_to(RIGHT * 2.5 + UP * 1)

        for step in calc:
            self.play(Write(step), run_time=2.4)

        result_box = SurroundingRectangle(calc[-1], color=ELO_RED, buff=0.12)
        self.play(Create(result_box), run_time=1.6)
        self.play(Indicate(calc[-1], color=ELO_RED, scale_factor=1.1), run_time=2)

        # Rating bar (drops)
        bar_before = Rectangle(width=0.8, height=2.0, fill_color=ELO_BLUE, fill_opacity=0.8, stroke_width=0)
        bar_before.move_to([-1.5, -2.8 + 1.0, 0])
        label_b = Text("2000", font_size=18, color=ELO_BLUE)
        label_b.next_to(bar_before, DOWN, buff=0.1)
        title_b = Text("Before", font_size=15, color=TEXT_GRAY)
        title_b.next_to(bar_before, UP, buff=0.1)

        bar_after = Rectangle(width=0.8, height=1.75, fill_color=ELO_RED, fill_opacity=0.8, stroke_width=0)
        bar_after.move_to([1.5, -2.8 + 0.875, 0])
        label_a = Text("1974", font_size=18, color=ELO_RED)
        label_a.next_to(bar_after, DOWN, buff=0.1)
        title_a = Text("After", font_size=15, color=TEXT_GRAY)
        title_a.next_to(bar_after, UP, buff=0.1)

        drop_arrow = Arrow(
            bar_before.get_top() + RIGHT * 0.4,
            bar_after.get_top() + LEFT * 0.4,
            color=ELO_RED, buff=0.05, stroke_width=2
        )
        # FIXED: label correctly shows -25.6 pts
        drop_text = Text("-25.6 pts", font_size=18, color=ELO_RED)
        drop_text.next_to(drop_arrow, UP, buff=0.1)

        self.play(FadeIn(bar_before), FadeIn(label_b), FadeIn(title_b), run_time=1.6)
        self.play(FadeIn(bar_after), FadeIn(label_a), FadeIn(title_a),
                  Create(drop_arrow), FadeIn(drop_text), run_time=3.6)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene4_5_KFactorSpectrum(Scene):
    """Scene 4.5: K-Factor Spectrum."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The K-Factor Spectrum", font_size=48, color=ELO_GOLD)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1.5)

        # Gradient spectrum bar
        n_segs = 20
        gradient = VGroup()
        bar_width = 10.0
        for i in range(n_segs):
            t = i / (n_segs - 1)
            seg = Rectangle(
                width=bar_width / n_segs, height=0.9,
                fill_color=manim_interpolate_color(ManimColor(ELO_RED), ManimColor(ELO_BLUE), t),
                fill_opacity=0.85, stroke_width=0
            )
            seg.move_to(LEFT * 5 + RIGHT * (bar_width / n_segs) * (i + 0.5) + UP * 0.8)
            gradient.add(seg)

        bar_outline = Rectangle(width=bar_width, height=0.9,
                                stroke_color=WHITE, stroke_width=1.5, fill_opacity=0)
        bar_outline.move_to(gradient.get_center())

        self.play(FadeIn(gradient), Create(bar_outline), run_time=3.6)

        # Labels
        high_k = VGroup(
            Text("K = 40", font_size=26, color=ELO_RED, weight=BOLD),
            Text("New Players", font_size=18, color=TEXT_GRAY),
            Text("Large swings", font_size=15, color=TEXT_GRAY),
            Text("Fast convergence", font_size=15, color=TEXT_GRAY),
        )
        high_k.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        high_k.next_to(gradient, LEFT, buff=0.4)
        high_k.shift(DOWN * 0.5)

        low_k = VGroup(
            Text("K = 10", font_size=26, color=ELO_BLUE, weight=BOLD),
            Text("Veterans", font_size=18, color=TEXT_GRAY),
            Text("Small swings", font_size=15, color=TEXT_GRAY),
            Text("Stable ranking", font_size=15, color=TEXT_GRAY),
        )
        low_k.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        low_k.next_to(gradient, RIGHT, buff=0.4)
        low_k.shift(DOWN * 0.5)

        self.play(FadeIn(high_k, shift=RIGHT * 0.2), FadeIn(low_k, shift=LEFT * 0.2), run_time=3.6)

        # Comparison examples
        demo = VGroup(
            Text("Same surprise (Delta = 0.5),  different impact:", font_size=20, color=TEXT_LIGHT),
            VGroup(
                Text("New player (K=40):  ", font_size=18, color=ELO_RED),
                MathTex(r"\Delta R = 40 \times 0.5 = +20", font_size=22, color=ELO_RED),
            ),
            VGroup(
                Text("Veteran (K=10):      ", font_size=18, color=ELO_BLUE),
                MathTex(r"\Delta R = 10 \times 0.5 = +5", font_size=22, color=ELO_BLUE),
            ),
        )
        for row in demo[1:]:
            row.arrange(RIGHT, buff=0.2)
        demo.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        demo.move_to(DOWN * 2.3)

        self.play(FadeIn(demo, shift=UP * 0.3), run_time=4)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene4_2a_ExplainUpdateEquation(Scene):
    """Scene 4.2a: The Update Equation piece by piece."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Update Equation - Piece by Piece", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)

        formula = MathTex(
            r"R'_A", r"=", r"R_A", r"+", r"K", r"(", r"S_A", r"-", r"E_A", r")",
            font_size=52
        )
        formula[0].set_color(ELO_GREEN)
        formula[2].set_color(ELO_BLUE)
        formula[4].set_color(ELO_GOLD)
        formula[6].set_color(ELO_GREEN)
        formula[8].set_color(ELO_RED)
        formula.move_to(UP * 1.5)
        self.play(Write(formula), run_time=8)

        parts = [
            (formula[2], r"R_A = \text{Old Rating}", "Your current rating before the game", ELO_BLUE),
            (formula[6], r"S_A = \text{Actual Score}", "1 = Win,  0.5 = Draw,  0 = Loss", ELO_GREEN),
            (formula[8], r"E_A = \text{Expected Score}", "Probability you'd win (from Elo formula)", ELO_RED),
            (formula[4], r"K = \text{Sensitivity}", "Max points per game - 10 to 40", ELO_GOLD),
        ]

        prev_grp = None
        for target, math_str, desc_str, color in parts:
            box = SurroundingRectangle(target, color=color, buff=0.08, stroke_width=2)

            math_label = MathTex(math_str, font_size=26, color=color)
            desc_label = Text(desc_str, font_size=17, color=TEXT_GRAY)
            grp = VGroup(math_label, desc_label)
            grp.arrange(DOWN, buff=0.18)
            grp.move_to(DOWN * 0.5)

            anims = [Create(box), FadeIn(grp, shift=DOWN * 0.2)]
            if prev_grp:
                anims.append(FadeOut(prev_grp))
            self.play(*anims, run_time=3.2)
            self.wait(2)
            self.play(FadeOut(box), run_time=0.8)
            prev_grp = grp

        self.play(FadeOut(prev_grp), run_time=1.2)

        # Surprise factor cases
        surprise_title = Text("The Surprise Factor  (S_A - E_A)", font_size=24, color=ELO_GOLD)
        surprise_title.move_to(DOWN * 0.1)

        cases = VGroup(
            Text("Win vs. underdog  (E=0.2):  +0.8  (big boost!)", font_size=17, color=ELO_GREEN),
            Text("Win as expected   (E=0.9):  +0.1  (small gain)", font_size=17, color=TEXT_GRAY),
            Text("Lose as underdog  (E=0.9):  -0.9  (big drop!)", font_size=17, color=ELO_RED),
        )
        cases.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        cases.next_to(surprise_title, DOWN, buff=0.3)

        self.play(FadeIn(surprise_title, shift=DOWN * 0.2), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cases], lag_ratio=0.2), run_time=4)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene4_5a_ExplainKFactor(MovingCameraScene):
    """Scene 4.5a: K-Factor - Speed vs Stability tradeoff."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("K-Factor: Speed vs Stability", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)

        # Rating trajectories
        axes = Axes(
            x_range=[0, 10, 1], y_range=[1400, 1620, 50],
            x_length=9, y_length=3.5, tips=False,
            axis_config={"include_numbers": True, "font_size": 11}
        )
        axes.move_to(DOWN * 0.5)

        x_label = Text("Game #", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Rating", font_size=14, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.15)
        y_label.rotate(90 * DEGREES)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=2.8)

        # High K (volatile)
        high_k_r = [1500, 1540, 1498, 1545, 1490, 1542, 1485, 1537, 1493, 1542]
        high_k_path = VMobject(color=ELO_RED, stroke_width=2.5)
        high_k_path.set_points_smoothly([axes.c2p(i, r) for i, r in enumerate(high_k_r)])
        high_k_lbl = Text("K = 40  (volatile)", font_size=16, color=ELO_RED)
        high_k_lbl.move_to(axes.c2p(9, 1555))

        # Low K (stable)
        low_k_r = [1500, 1510, 1504, 1512, 1508, 1514, 1511, 1516, 1513, 1519]
        low_k_path = VMobject(color=ELO_BLUE, stroke_width=2.5)
        low_k_path.set_points_smoothly([axes.c2p(i, r) for i, r in enumerate(low_k_r)])
        low_k_lbl = Text("K = 10  (stable)", font_size=16, color=ELO_BLUE)
        low_k_lbl.move_to(axes.c2p(9, 1522))

        self.play(Create(high_k_path), FadeIn(high_k_lbl), run_time=6)
        self.play(Create(low_k_path), FadeIn(low_k_lbl), run_time=6)
        self.wait(1.6)

        # Zoom into the right side to compare the two endpoints
        self.play(
            self.camera.frame.animate.scale(0.60).move_to(axes.c2p(8.5, 1535)),
            run_time=3.6
        )
        self.wait(4)
        self.play(
            self.camera.frame.animate.scale(1 / 0.60).move_to(ORIGIN),
            run_time=2.8
        )

        # K-Factor guide table
        table_title = Text("F1 K-Factor Guide", font_size=22, color=ELO_GOLD)
        table_title.to_edge(DOWN, buff=1.2)

        rows = VGroup(
            VGroup(Text("K = 40", font_size=16, color=ELO_RED),
                   Text("Rookie", font_size=16, color=TEXT_GRAY),
                   Text("Fast convergence, volatile", font_size=16, color=TEXT_GRAY)),
            VGroup(Text("K = 20", font_size=16, color=ELO_GOLD),
                   Text("Established", font_size=16, color=TEXT_GRAY),
                   Text("Balanced updates", font_size=16, color=TEXT_GRAY)),
            VGroup(Text("K = 10", font_size=16, color=ELO_BLUE),
                   Text("Veteran", font_size=16, color=TEXT_GRAY),
                   Text("Very stable", font_size=16, color=TEXT_GRAY)),
        )
        for row in rows:
            row.arrange(RIGHT, buff=1.2)
        rows.arrange(DOWN, buff=0.2)
        rows.next_to(table_title, DOWN, buff=0.2)

        table_group = VGroup(table_title, rows)
        table_group.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(table_group), run_time=3.2)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)
