# Section 3: Arpad Elo and the Physics of Performance
from manim import *
import numpy as np
import sys
sys.path.append('..')
from utils.colors import *


class Scene3_1_EloBackground(Scene):
    """Scene 3.1: Elo's Background - Physicist and chess master."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Arpad Elo  (1903-1992)", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        # Two columns
        physicist = VGroup(
            Text("Physicist", font_size=34, color=ELO_GOLD, weight=BOLD),
            Text("Marquette University", font_size=20, color=TEXT_GRAY),
            Text("Measurement theory", font_size=18, color=TEXT_GRAY),
            Text("Signal vs. noise", font_size=18, color=TEXT_GRAY),
        )
        physicist.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        physicist.move_to(LEFT * 3.5 + UP * 0.3)

        chess = VGroup(
            Text("Chess Master", font_size=34, color=ELO_BLUE, weight=BOLD),
            Text("Competed vs. legends", font_size=20, color=TEXT_GRAY),
            Text("Bobby Fischer", font_size=18, color=TEXT_GRAY),
            Text("Reuben Fine", font_size=18, color=TEXT_GRAY),
        )
        chess.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        chess.move_to(RIGHT * 2.5 + UP * 0.3)

        divider = Line(UP * 2, DOWN * 1.5, color=TEXT_GRAY, stroke_width=1)
        divider.move_to(ORIGIN + DOWN * 0.2)

        self.play(Create(divider), run_time=0.4)
        self.play(FadeIn(physicist, shift=RIGHT * 0.3), run_time=0.9)
        self.play(FadeIn(chess, shift=LEFT * 0.3), run_time=0.9)

        # The key insight
        insight_box = Rectangle(
            width=9, height=1.1,
            fill_color=ELO_BLUE, fill_opacity=0.15,
            stroke_color=ELO_BLUE, stroke_width=2
        )
        insight_box.move_to(DOWN * 2.2)

        insight = Text(
            '"Chess performance is a MEASUREMENT problem"',
            font_size=26, color=TEXT_LIGHT, slant=ITALIC
        )
        insight.move_to(insight_box)

        self.play(FadeIn(insight_box), Write(insight, run_time=1.2))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class Scene3_2_PerformanceRandom(Scene):
    """Scene 3.2: Performance as a Random Variable."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Physics Analogy", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        # Left: rod measurement
        left_title = Text("Measuring a rod", font_size=22, color=TEXT_GRAY)
        left_title.move_to(LEFT * 3.2 + UP * 1.5)

        rod = Rectangle(width=3.5, height=0.35, fill_color=ELO_GOLD, fill_opacity=0.8, stroke_width=0)
        rod.move_to(LEFT * 3.2 + UP * 0.7)
        rod_label = Text("True length = 10 cm", font_size=18, color=TEXT_GRAY)
        rod_label.next_to(rod, DOWN, buff=0.2)

        self.play(FadeIn(left_title), FadeIn(rod), FadeIn(rod_label), run_time=0.8)

        # Scatter of measurements
        measurement_line = Line(LEFT * 5.2, LEFT * 1.2, color=TEXT_GRAY, stroke_width=1.5)
        measurement_line.move_to(LEFT * 3.2 + DOWN * 0.2)

        np.random.seed(42)
        meas_vals = np.random.normal(0, 0.25, 14)
        meas_dots = VGroup(*[
            Dot(measurement_line.get_center() + RIGHT * v * 2.5, color=ELO_BLUE, radius=0.07)
            for v in meas_vals
        ])

        self.play(Create(measurement_line), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.3) for d in meas_dots], lag_ratio=0.04),
            run_time=1.2
        )

        # Right: chess analogy
        right_title = Text("Chess performance", font_size=22, color=TEXT_GRAY)
        right_title.move_to(RIGHT * 3 + UP * 1.5)

        chess_details = VGroup(
            MathTex(r"\mu = \text{True Skill (hidden)}", font_size=22, color=ELO_GOLD),
            MathTex(r"P_{\text{game}} \sim \mathcal{N}(\mu, \sigma^2)", font_size=22, color=ELO_BLUE),
        )
        chess_details.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        chess_details.move_to(RIGHT * 3 + UP * 0.4)

        self.play(FadeIn(right_title), FadeIn(chess_details, shift=LEFT * 0.2), run_time=1)

        # Same idea arrow
        arrow = Arrow(LEFT * 0.8, RIGHT * 1, color=TEXT_GRAY, buff=0.1)
        arrow.move_to(ORIGIN + DOWN * 0.2)
        same_label = Text("Same principle!", font_size=18, color=ELO_GOLD)
        same_label.next_to(arrow, UP, buff=0.15)

        self.play(Create(arrow), FadeIn(same_label), run_time=0.6)

        caption = Text(
            "Performance fluctuates around true skill due to many factors",
            font_size=22, color=TEXT_LIGHT
        )
        caption.to_edge(DOWN, buff=0.7)
        self.play(FadeIn(caption, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class Scene3_3_NormalDistribution(Scene):
    """Scene 3.3: The Normal Distribution Model with sigma shading (68-95-99.7)."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Normal Distribution", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        axes = Axes(
            x_range=[1400, 2600, 200],
            y_range=[0, 0.0025, 0.0005],
            x_length=10, y_length=4.2,
            axis_config={"include_numbers": True, "font_size": 14},
            tips=False
        )
        axes.shift(DOWN * 0.5)

        x_label = Text("Performance Rating", font_size=16, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)

        self.play(Create(axes), FadeIn(x_label), run_time=0.8)

        mean, std = 2000, 200

        def normal_pdf(x):
            return (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)

        # Shaded sigma regions (68-95-99.7) - add from wide to narrow
        for n_sigma, color, opacity in [(3, ELO_BLUE, 0.12), (2, ELO_BLUE, 0.18), (1, ELO_BLUE, 0.28)]:
            area = axes.get_area(
                axes.plot(normal_pdf, x_range=[mean - n_sigma * std, mean + n_sigma * std]),
                x_range=[mean - n_sigma * std, mean + n_sigma * std],
                color=color, opacity=opacity
            )
            self.add(area)

        # Main curve on top
        curve = axes.plot(normal_pdf, x_range=[1400, 2600], color=ELO_BLUE, stroke_width=3)
        self.play(Create(curve), run_time=1.5)

        # Mean line
        mean_line = DashedLine(
            axes.c2p(mean, 0),
            axes.c2p(mean, normal_pdf(mean)),
            color=ELO_GOLD, stroke_width=2
        )
        mean_label = MathTex(r"\mu = 2000", font_size=24, color=ELO_GOLD)
        mean_label.next_to(axes.c2p(mean, normal_pdf(mean)), UP + LEFT * 0.5, buff=0.1)

        self.play(Create(mean_line), FadeIn(mean_label), run_time=0.8)

        # Sigma double arrow (1 std dev)
        std_brace = DoubleArrow(
            axes.c2p(mean, normal_pdf(mean + std) * 0.8),
            axes.c2p(mean + std, normal_pdf(mean + std) * 0.8),
            color=ELO_GREEN, buff=0, stroke_width=2
        )
        std_label = MathTex(r"\sigma \approx 200", font_size=22, color=ELO_GREEN)
        std_label.next_to(std_brace, UP, buff=0.12)

        self.play(Create(std_brace), FadeIn(std_label), run_time=0.8)

        # Sigma region labels
        label_1s = Text("68%", font_size=16, color=TEXT_LIGHT)
        label_1s.move_to(axes.c2p(mean, normal_pdf(mean) * 0.25))
        label_2s = Text("95%", font_size=14, color=TEXT_LIGHT)
        label_2s.move_to(axes.c2p(mean - 320, normal_pdf(mean - 320) * 0.35))

        self.play(FadeIn(label_1s), FadeIn(label_2s), run_time=0.6)

        # Formula box (upper right, away from curve peak)
        formula = MathTex(r"P \sim \mathcal{N}(\mu, \sigma^2)", font_size=34, color=TEXT_WHITE)
        formula.move_to(RIGHT * 3.5 + UP * 2.3)
        fbox = SurroundingRectangle(formula, color=ELO_BLUE, buff=0.18, corner_radius=0.1)

        self.play(Write(formula), Create(fbox), run_time=1)

        interp = Text(
            "68% of games within  +-200 pts  of true skill",
            font_size=22, color=TEXT_LIGHT
        )
        interp.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(interp, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class Scene3_4_DifferenceOfNormals(Scene):
    """Scene 3.4: Difference of Normals - probability of winning."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Who Wins?", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        axes = Axes(
            x_range=[1300, 2700, 200],
            y_range=[0, 0.0025, 0.0005],
            x_length=10, y_length=3.8,
            axis_config={"include_numbers": True, "font_size": 12},
            tips=False
        )
        axes.shift(UP * 0.1)

        self.play(Create(axes), run_time=0.8)

        mean_a, mean_b = 2000, 1800

        def pdf(m):
            def f(x):
                return (1 / (200 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - m) / 200) ** 2)
            return f

        curve_a = axes.plot(pdf(mean_a), x_range=[1300, 2700], color=ELO_BLUE, stroke_width=3)
        curve_b = axes.plot(pdf(mean_b), x_range=[1300, 2700], color=ELO_RED, stroke_width=3)

        # Overlap area (where B beats A — left tail of A overlaps with B)
        overlap_area = axes.get_area(
            axes.plot(pdf(mean_b), x_range=[1700, 2700]),
            x_range=[1700, 2700],
            color=ELO_PURPLE, opacity=0.3
        )

        label_a = Text("Player A: 2000", font_size=18, color=ELO_BLUE)
        label_a.move_to(axes.c2p(2200, pdf(mean_a)(2200)) + UP * 0.4)

        label_b = Text("Player B: 1800", font_size=18, color=ELO_RED)
        label_b.move_to(axes.c2p(1600, pdf(mean_b)(1600)) + UP * 0.4)

        self.play(Create(curve_a), FadeIn(label_a), run_time=0.9)
        self.play(Create(curve_b), FadeIn(label_b), run_time=0.9)
        self.play(FadeIn(overlap_area), run_time=0.6)

        # Key insight box (below curves, not overlapping)
        diff_box = Rectangle(
            width=7, height=1.0,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_GOLD, stroke_width=1.5
        )
        diff_box.to_edge(DOWN, buff=1.2)

        diff_text = Text(
            "Rating difference 200 = exactly 1 standard deviation",
            font_size=20, color=TEXT_LIGHT
        )
        diff_text.move_to(diff_box)

        # CDF formula (below diff_box to avoid overlap with curves)
        formula = MathTex(
            r"E_A = \Phi\!\left(\frac{R_A - R_B}{\sigma\sqrt{2}}\right)",
            font_size=28, color=ELO_BLUE
        )
        formula.to_edge(DOWN, buff=0.2)

        self.play(FadeIn(diff_box), FadeIn(diff_text), run_time=0.7)
        self.play(Write(formula, run_time=1))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class Scene3_5_LogisticTransition(Scene):
    """Scene 3.5: Transition to Logistic Distribution."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("From Normal to Logistic", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        reason = VGroup(
            Text("Empirical data showed:", font_size=22, color=TEXT_LIGHT),
            Text("  Upsets are MORE common than the Normal predicts", font_size=20, color=ELO_GOLD),
            Text("  Normal distribution has too-thin tails", font_size=20, color=TEXT_GRAY),
        )
        reason.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        reason.move_to(UP * 1.5)

        self.play(FadeIn(reason, shift=DOWN * 0.3), run_time=1)

        # Side-by-side comparison of tail shapes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.45, 0.1],
            x_length=9, y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 14},
            tips=False
        )
        axes.move_to(DOWN * 1.5)

        x_lbl = Text("Standardized score", font_size=14, color=TEXT_GRAY)
        x_lbl.next_to(axes.x_axis, DOWN, buff=0.25)

        self.play(Create(axes), FadeIn(x_lbl), run_time=0.7)

        # Normal pdf
        def normal(x):
            return np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)

        # Logistic pdf
        def logistic(x):
            ex = np.exp(-x)
            return ex / (1 + ex) ** 2

        normal_curve = axes.plot(normal, x_range=[-4, 4], color=ELO_BLUE, stroke_width=3)
        logistic_curve = axes.plot(logistic, x_range=[-4, 4], color=ELO_GREEN, stroke_width=3)

        normal_lbl = Text("Normal (thinner tails)", font_size=16, color=ELO_BLUE)
        normal_lbl.move_to(axes.c2p(2.5, 0.3))
        logistic_lbl = Text("Logistic (fatter tails)", font_size=16, color=ELO_GREEN)
        logistic_lbl.move_to(axes.c2p(-2.5, 0.22))

        self.play(Create(normal_curve), FadeIn(normal_lbl), run_time=1)
        self.play(Create(logistic_curve), FadeIn(logistic_lbl), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class Scene3_6_LogisticFormula(Scene):
    """Scene 3.6: The Modern Logistic Elo Formula."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Modern Elo Formula", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        # Main formula - large, centered
        formula = MathTex(
            r"E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}",
            font_size=60
        )
        formula.move_to(UP * 0.8)

        self.play(Write(formula, run_time=2))
        self.wait(0.5)

        # Braces explaining parts
        brace_num = Brace(formula[0][4:5], UP, color=ELO_GREEN)
        brace_num_lbl = brace_num.get_text("Always 1", font_size=18)
        brace_num_lbl.set_color(ELO_GREEN)

        brace_400 = Brace(formula[0][9:12], DOWN, color=ELO_GOLD)
        brace_400_lbl = brace_400.get_text("Scaling: 400 pts = ~24% win chance shift", font_size=16)
        brace_400_lbl.set_color(ELO_GOLD)

        self.play(
            GrowFromCenter(brace_num), FadeIn(brace_num_lbl),
            run_time=0.7
        )
        self.play(
            GrowFromCenter(brace_400), FadeIn(brace_400_lbl),
            run_time=0.7
        )

        # Properties table
        properties = VGroup(
            Text("Guarantees:  0 < E_A < 1  (always valid probability)", font_size=19, color=ELO_GREEN),
            Text("Symmetry:  E_A + E_B = 1  (zero-sum)", font_size=19, color=ELO_BLUE),
            Text("At equal ratings:  E_A = 0.5  (50% each)", font_size=19, color=TEXT_GRAY),
        )
        properties.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        properties.move_to(DOWN * 2.3)

        self.play(
            LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in properties], lag_ratio=0.2),
            run_time=1.2
        )
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class Scene3_7_SigmoidVisualization(Scene):
    """Scene 3.7: The Sigmoid Curve - win probability as a function of rating gap."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Logistic Curve", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        axes = Axes(
            x_range=[-800, 800, 200],
            y_range=[0, 1, 0.25],
            x_length=10, y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 14},
            tips=False,
            y_axis_config={"decimal_number_config": {"num_decimal_places": 2}}
        )
        axes.shift(DOWN * 0.4)

        x_label = Text("Rating Difference  (R_A - R_B)", font_size=16, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Win Probability", font_size=16, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)
        y_label.rotate(90 * DEGREES)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.9)

        def elo_prob(x):
            return 1 / (1 + 10 ** (-x / 400))

        sigmoid_curve = axes.plot(elo_prob, x_range=[-800, 800], color=ELO_BLUE, stroke_width=3.5)
        self.play(Create(sigmoid_curve), run_time=1.5)

        # Key points
        key_points = [
            (0, 0.5, "50% (equal)", TEXT_GRAY, UP),
            (400, elo_prob(400), "76% at +400", ELO_GREEN, UP),
            (-400, elo_prob(-400), "24% at -400", ELO_RED, DOWN),
        ]

        for x, y, label, col, direction in key_points:
            dot = Dot(axes.c2p(x, y), color=col, radius=0.1)
            h_line = DashedLine(axes.c2p(0, y), axes.c2p(x, y), color=col, stroke_width=1)
            v_line = DashedLine(axes.c2p(x, 0), axes.c2p(x, y), color=col, stroke_width=1)
            ann = Text(label, font_size=16, color=col)
            ann.next_to(dot, direction, buff=0.15)
            self.play(Create(h_line), Create(v_line), FadeIn(dot), FadeIn(ann), run_time=0.5)

        # Asymptotic lines
        top_line = DashedLine(axes.c2p(-800, 1), axes.c2p(800, 1), color=TEXT_GRAY,
                              stroke_width=1, dash_length=0.15)
        bot_line = DashedLine(axes.c2p(-800, 0), axes.c2p(800, 0), color=TEXT_GRAY,
                              stroke_width=1, dash_length=0.15)
        self.play(Create(top_line), Create(bot_line), run_time=0.5)

        cap_text = Text(
            "Always between 0 and 1 - impossible outcomes get near-zero (not zero)",
            font_size=18, color=TEXT_LIGHT
        )
        cap_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap_text, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
