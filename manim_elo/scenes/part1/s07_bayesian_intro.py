# Section 7: The Bayesian Frontier
# 6 Scenes introducing probabilistic thinking

from manim import *
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *
import numpy as np


class Scene7_1_PointVsDistribution(Scene):
    """Scene 7.1: Point Estimates vs Distributions."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("A New Way of Thinking", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)

        # Point estimate (left)
        point_title = Text("Classical Elo", font_size=24, color=TEXT_GRAY)
        point_title.move_to(LEFT * 3.5 + UP * 1.5)

        point_value = MathTex(r"\text{Skill} = 2000", font_size=32, color=ELO_BLUE)
        point_value.next_to(point_title, DOWN, buff=0.5)

        point_line = NumberLine(x_range=[1800, 2200, 100], length=4, include_numbers=True, font_size=14)
        point_line.next_to(point_value, DOWN, buff=0.5)

        point_dot = Dot(point_line.n2p(2000), color=ELO_BLUE, radius=0.15)

        self.play(
            FadeIn(point_title, shift=DOWN * 0.2),
            Write(point_value),
            Create(point_line),
            FadeIn(point_dot),
            run_time=6
        )

        # Arrow
        arrow = Arrow(LEFT * 0.5, RIGHT * 0.5, color=TEXT_GRAY)
        arrow.move_to(ORIGIN)
        arrow_label = Text("Evolve", font_size=16, color=TEXT_GRAY)
        arrow_label.next_to(arrow, UP, buff=0.1)
        self.play(Create(arrow), FadeIn(arrow_label), run_time=2)

        # Distribution (right)
        dist_title = Text("Bayesian", font_size=24, color=ELO_GREEN)
        dist_title.move_to(RIGHT * 3.5 + UP * 1.5)

        dist_value = MathTex(r"\text{Skill} \sim \mathcal{N}(2000, 50^2)", font_size=28, color=ELO_GREEN)
        dist_value.next_to(dist_title, DOWN, buff=0.5)

        # Bell curve axes (compact)
        axes = Axes(
            x_range=[1800, 2200, 100],
            y_range=[0, 0.01, 0.005],
            x_length=4,
            y_length=2,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.next_to(dist_value, DOWN, buff=0.3)

        def normal(x):
            return (1 / (50 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 2000) / 50) ** 2)

        curve = axes.plot(normal, x_range=[1800, 2200], color=ELO_GREEN)
        area = axes.get_area(curve, x_range=[1800, 2200], color=ELO_GREEN, opacity=0.3)

        self.play(
            FadeIn(dist_title, shift=DOWN * 0.2),
            Write(dist_value),
            Create(axes),
            Create(curve),
            FadeIn(area),
            run_time=6
        )

        # Caption
        caption = Text(
            "We don't KNOW skill; we have BELIEFS about skill",
            font_size=22,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption, shift=UP * 0.3), run_time=6)
        self.wait(35)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene7_2_BayesTheorem(Scene):
    """Scene 7.2: Bayes' Theorem Introduction."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Bayes' Theorem", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)

        # The formula
        formula = MathTex(
            r"P(\theta|D)", r"=",
            r"\frac{P(D|\theta) \cdot P(\theta)}{P(D)}",
            font_size=44
        )
        formula.move_to(UP * 1)

        # Color code parts
        formula[0].set_color(ELO_GREEN)   # Posterior
        formula[2].set_color(ELO_GOLD)    # Likelihood/whole fraction

        self.play(Write(formula), run_time=8)

        # Brace labels (use Brace for clean annotation)
        brace_post = Brace(formula[0], UP, color=ELO_GREEN)
        brace_post_lbl = brace_post.get_text("Posterior")
        brace_post_lbl.set_color(ELO_GREEN)

        brace_like = Brace(formula[2], DOWN, color=ELO_GOLD)
        brace_like_lbl = brace_like.get_text("Likelihood x Prior / Evidence")
        brace_like_lbl.set_color(ELO_GOLD)

        self.play(
            LaggedStart(
                AnimationGroup(GrowFromCenter(brace_post), FadeIn(brace_post_lbl)),
                AnimationGroup(GrowFromCenter(brace_like), FadeIn(brace_like_lbl)),
                lag_ratio=0.2
            ),
            run_time=6
        )

        # Verbal explanation row
        verbal = VGroup(
            Text("Updated Belief", font_size=20, color=ELO_GREEN),
            Text("=", font_size=20, color=TEXT_GRAY),
            Text("Evidence Match", font_size=20, color=ELO_GOLD),
            Text("x", font_size=20, color=TEXT_GRAY),
            Text("Prior Belief", font_size=20, color=ELO_BLUE)
        )
        verbal.arrange(RIGHT, buff=0.3)
        verbal.move_to(DOWN * 1.5)
        self.play(FadeIn(verbal, shift=UP * 0.2), run_time=6)

        # Key insight
        insight_box = RoundedRectangle(
            width=7.5, height=0.8, corner_radius=0.1,
            fill_color=ELO_BLUE, fill_opacity=0.12,
            stroke_color=ELO_BLUE, stroke_width=1.5
        )
        insight_box.to_edge(DOWN, buff=0.5)
        insight = Text(
            "Combine what you knew with what you observed",
            font_size=22, color=TEXT_LIGHT
        )
        insight.move_to(insight_box)
        self.play(FadeIn(insight_box), FadeIn(insight, shift=UP * 0.2), run_time=4)
        self.wait(35)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene7_3_RankingContext(Scene):
    """Scene 7.3: The Ranking Context - Prior to Posterior."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Bayes in Ranking", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)

        # Three components in a row
        prior = VGroup(
            MathTex(r"P(\text{skill})", font_size=32, color=ELO_BLUE),
            Text("Prior belief", font_size=18, color=TEXT_GRAY),
            Text("before the match", font_size=16, color=TEXT_GRAY)
        )
        prior.arrange(DOWN, buff=0.15)
        prior.move_to(LEFT * 4 + UP * 0.5)

        likelihood = VGroup(
            MathTex(r"P(\text{result}|\text{skill})", font_size=32, color=ELO_GOLD),
            Text("Likelihood", font_size=18, color=TEXT_GRAY),
            Text("of this result given skill", font_size=16, color=TEXT_GRAY)
        )
        likelihood.arrange(DOWN, buff=0.15)
        likelihood.move_to(ORIGIN + UP * 0.5)

        posterior = VGroup(
            MathTex(r"P(\text{skill}|\text{result})", font_size=32, color=ELO_GREEN),
            Text("Posterior belief", font_size=18, color=TEXT_GRAY),
            Text("after the match", font_size=16, color=TEXT_GRAY)
        )
        posterior.arrange(DOWN, buff=0.15)
        posterior.move_to(RIGHT * 4 + UP * 0.5)

        # Arrows between components
        arrow1 = Arrow(prior.get_right() + RIGHT * 0.1,
                       likelihood.get_left() + LEFT * 0.1, color=TEXT_GRAY)
        arrow2 = Arrow(likelihood.get_right() + RIGHT * 0.1,
                       posterior.get_left() + LEFT * 0.1, color=TEXT_GRAY)

        self.play(FadeIn(prior, shift=RIGHT * 0.2), run_time=3.2)
        self.play(Create(arrow1), run_time=1.2)
        self.play(FadeIn(likelihood, shift=DOWN * 0.2), run_time=3.2)
        self.play(Create(arrow2), run_time=1.2)
        self.play(FadeIn(posterior, shift=LEFT * 0.2), run_time=3.2)

        # Example box at bottom
        ex_box = RoundedRectangle(
            width=9.5, height=2.0, corner_radius=0.12,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_GOLD, stroke_width=1.5
        )
        ex_box.to_edge(DOWN, buff=0.4)

        example = VGroup(
            Text("Example:", font_size=20, color=TEXT_LIGHT, weight=BOLD),
            Text("Prior: Player rated ~2000 (uncertain)  |  Beats a 2200: supports HIGHER skill", font_size=17, color=TEXT_GRAY),
            Text("Posterior: Belief shifts up, uncertainty shrinks", font_size=17, color=ELO_GREEN)
        )
        example.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        example.move_to(ex_box)

        self.play(FadeIn(ex_box), FadeIn(example, shift=UP * 0.2), run_time=6)
        self.wait(35)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene7_4_GaussianGhost(Scene):
    """Scene 7.4: The Gaussian Ghost - Updating beliefs.

    FIXED: posterior_label placed at axes.c2p(2100, 0.005) + UP*0.3
    to avoid overlapping the top of the bell curve.
    No emoji in text.
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Updating Ghost", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)

        # Axes
        axes = Axes(
            x_range=[1600, 2400, 200],
            y_range=[0, 0.006, 0.002],
            x_length=10,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 14}
        )
        axes.shift(DOWN * 0.5)

        x_label = Text("Skill Rating", font_size=18, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)

        self.play(Create(axes), FadeIn(x_label), run_time=4)

        # Prior: wide, uncertain (new player)
        mean1, std1 = 1900, 150

        def prior_pdf(x):
            return (1 / (std1 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean1) / std1) ** 2)

        prior_curve = axes.plot(prior_pdf, x_range=[1600, 2400], color=ELO_BLUE)
        prior_area = axes.get_area(prior_curve, x_range=[1600, 2400], color=ELO_BLUE, opacity=0.3)

        # Prior label: positioned clearly above the curve peak, shifted left to avoid overlap
        prior_label = Text("Prior (uncertain)", font_size=16, color=ELO_BLUE)
        prior_label.move_to(axes.c2p(1700, 0.0035) + UP * 0.3)
        prior_label_bg = BackgroundRectangle(prior_label, fill_opacity=0.80, buff=0.06)

        self.play(Create(prior_curve), FadeIn(prior_area), FadeIn(prior_label_bg), FadeIn(prior_label), run_time=6)
        self.wait(20)

        # After win: shift right, narrower (more certain)
        mean2, std2 = 2000, 100

        def posterior_pdf(x):
            return (1 / (std2 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean2) / std2) ** 2)

        posterior_curve = axes.plot(posterior_pdf, x_range=[1600, 2400], color=ELO_GREEN)
        posterior_area = axes.get_area(posterior_curve, x_range=[1600, 2400], color=ELO_GREEN, opacity=0.3)

        # FIXED: posterior_label placed at right side, well above axes top edge
        # Use axes.c2p(2100, 0.005) + UP*0.3 to clear the bell curve peak
        posterior_label = Text("After win (more certain!)", font_size=16, color=ELO_GREEN)
        posterior_label.move_to(axes.c2p(2200, 0.005) + UP * 0.3)
        posterior_label_bg = BackgroundRectangle(posterior_label, fill_opacity=0.80, buff=0.06)

        # Win event label (no emoji)
        win_label = Text("Player wins!", font_size=20, color=ELO_GOLD, weight=BOLD)
        win_label.to_edge(RIGHT, buff=0.8)
        win_label.shift(UP * 1.5)
        self.play(FadeIn(win_label, shift=DOWN * 0.2), run_time=2)

        # Transform prior to posterior
        self.play(
            Transform(prior_curve, posterior_curve),
            Transform(prior_area, posterior_area),
            FadeOut(prior_label_bg), FadeOut(prior_label),
            FadeIn(posterior_label_bg), FadeIn(posterior_label),
            run_time=8
        )

        # Key observations (no emoji - use text)
        observations = VGroup(
            Text("Mean shifted right (skill higher)", font_size=18, color=ELO_GREEN),
            Text("Curve narrower (less uncertainty)", font_size=18, color=ELO_GREEN)
        )
        observations.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        observations.to_edge(DOWN, buff=0.4)
        self.play(
            LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in observations], lag_ratio=0.3),
            run_time=4
        )
        self.wait(35)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene7_5_ScorpionAnalogy(Scene):
    """Scene 7.5: The USS Scorpion Analogy - Search theory."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Search Analogy", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)

        # Story setup
        story = Text(
            "1968: USS Scorpion submarine lost in the Atlantic",
            font_size=22, color=TEXT_GRAY
        )
        story.move_to(UP * 1.8)
        self.play(FadeIn(story, shift=DOWN * 0.2), run_time=4)

        # Grid of ocean squares
        grid_size = 4
        cell_size = 0.8

        grid = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                cell = Square(
                    side_length=cell_size,
                    fill_color=ELO_BLUE,
                    fill_opacity=0.25 - 0.05 * (i + j),
                    stroke_color=TEXT_GRAY
                )
                cell.move_to([
                    -1.5 + j * cell_size,
                    0.5 - i * cell_size,
                    0
                ])
                prob = round(0.25 - 0.015 * (i + j), 2)
                prob_text = Text(f"{int(prob * 100)}%", font_size=10, color=TEXT_WHITE)
                prob_text.move_to(cell)
                grid.add(VGroup(cell, prob_text))

        grid.move_to(LEFT * 2.5)
        self.play(FadeIn(grid, shift=RIGHT * 0.2), run_time=4)

        # Search explanation (right)
        explain = VGroup(
            Text("Bayesian Search:", font_size=20, color=ELO_GOLD, weight=BOLD),
            Text("  Each square has P(sub here)", font_size=16, color=TEXT_GRAY),
            Text("  Search a square, find nothing", font_size=16, color=TEXT_GRAY),
            Text("  P(here) down, P(elsewhere) up", font_size=16, color=ELO_GREEN)
        )
        explain.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        explain.move_to(RIGHT * 3 + UP * 0.3)
        self.play(
            LaggedStart(*[FadeIn(e, shift=LEFT * 0.2) for e in explain], lag_ratio=0.15),
            run_time=6
        )

        # Simulate searching a square
        search_text = Text("Search square A...", font_size=18, color=ELO_GOLD)
        search_text.move_to(RIGHT * 3 + DOWN * 1.5)
        self.play(FadeIn(search_text, shift=UP * 0.2), run_time=2)

        # Highlight searched cell
        self.play(grid[0][0].animate.set_fill(ELO_RED, opacity=0.3), run_time=2)

        # Redistribute belief
        result = Text("Nothing found -> redistribute belief", font_size=16, color=TEXT_LIGHT)
        result.move_to(RIGHT * 3 + DOWN * 2.2)
        self.play(FadeIn(result, shift=UP * 0.2), run_time=3.2)

        # Increase opacity of other cells
        self.play(
            *[grid[i][0].animate.set_fill(ELO_GREEN, opacity=0.3) for i in range(1, len(grid))],
            run_time=3.2
        )

        # Connection to rating
        connection_box = RoundedRectangle(
            width=9, height=0.8, corner_radius=0.1,
            fill_color=ELO_GOLD, fill_opacity=0.1,
            stroke_color=ELO_GOLD, stroke_width=1.5
        )
        connection_box.to_edge(DOWN, buff=0.4)
        connection = Text(
            "Same principle: observing OUTCOMES updates BELIEF about skill",
            font_size=19, color=ELO_GOLD
        )
        connection.move_to(connection_box)
        self.play(FadeIn(connection_box), FadeIn(connection, shift=UP * 0.2), run_time=6)
        self.wait(35)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene7_6_TrueSkill(Scene):
    """Scene 7.6: Microsoft TrueSkill - Two-number tracking."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Microsoft TrueSkill", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)

        # Year / context
        subtitle = Text("2006  |  Xbox Live Matchmaking", font_size=20, color=TEXT_GRAY)
        subtitle.next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(subtitle, shift=DOWN * 0.2), run_time=2)

        # Key innovation title
        innovation = Text("Two numbers per player:", font_size=24, color=ELO_GOLD)
        innovation.move_to(UP * 1)
        self.play(FadeIn(innovation, shift=UP * 0.2), run_time=3.2)

        # mu and sigma boxes
        mu_box = RoundedRectangle(
            width=3.5, height=2.2, corner_radius=0.15,
            fill_color=ELO_BLUE, fill_opacity=0.12,
            stroke_color=ELO_BLUE, stroke_width=1.5
        )
        mu_box.move_to(LEFT * 3 + DOWN * 0.5)

        mu_content = VGroup(
            MathTex(r"\mu", font_size=48, color=ELO_BLUE),
            Text("Skill estimate", font_size=18, color=TEXT_GRAY),
            Text("(mean of distribution)", font_size=14, color=TEXT_GRAY)
        )
        mu_content.arrange(DOWN, buff=0.1)
        mu_content.move_to(mu_box)

        sigma_box = RoundedRectangle(
            width=3.5, height=2.2, corner_radius=0.15,
            fill_color=ELO_PURPLE, fill_opacity=0.12,
            stroke_color=ELO_PURPLE, stroke_width=1.5
        )
        sigma_box.move_to(RIGHT * 3 + DOWN * 0.5)

        sigma_content = VGroup(
            MathTex(r"\sigma", font_size=48, color=ELO_PURPLE),
            Text("Uncertainty", font_size=18, color=TEXT_GRAY),
            Text("(std dev of distribution)", font_size=14, color=TEXT_GRAY)
        )
        sigma_content.arrange(DOWN, buff=0.1)
        sigma_content.move_to(sigma_box)

        self.play(
            FadeIn(mu_box), FadeIn(mu_content, shift=RIGHT * 0.2),
            run_time=3.2
        )
        self.play(
            FadeIn(sigma_box), FadeIn(sigma_content, shift=LEFT * 0.2),
            run_time=3.2
        )

        # Display rating formula
        rating_formula = MathTex(
            r"R = \mu - 3\sigma",
            font_size=36, color=TEXT_LIGHT
        )
        rating_formula.move_to(DOWN * 2.1)
        fbox = SurroundingRectangle(rating_formula, color=ELO_GOLD, buff=0.15, corner_radius=0.1)

        rating_label = Text("Conservative Display Rating", font_size=18, color=TEXT_GRAY)
        rating_label.next_to(rating_formula, DOWN, buff=0.2)

        self.play(Write(rating_formula), Create(fbox), FadeIn(rating_label), run_time=4)

        # Explanation
        explanation = VGroup(
            Text("New player: low mu, high sigma  ->  low R", font_size=18, color=TEXT_GRAY),
            Text("Veteran: stable mu, low sigma  ->  R close to mu", font_size=18, color=TEXT_GRAY)
        )
        explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        explanation.to_edge(DOWN, buff=0.4)
        self.play(
            LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in explanation], lag_ratio=0.3),
            run_time=4
        )
        self.wait(35)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene7_2a_ExplainBayesTheorem(Scene):
    """Scene 7.2a: Bayes' Theorem with concrete numbers."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Bayes' Theorem with Numbers", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)

        # The formula with color coding
        formula = MathTex(
            r"P(\theta|D)", r"=",
            r"\frac{P(D|\theta) \cdot P(\theta)}{P(D)}",
            font_size=40
        )
        formula[0].set_color(ELO_GREEN)
        formula[2].set_color(ELO_GOLD)
        formula.move_to(UP * 1.5)
        self.play(Write(formula), run_time=6)

        # Set up the example
        question = Text("Question: Is this rookie ELITE?", font_size=24, color=ELO_GOLD)
        question.move_to(UP * 0.5)
        self.play(FadeIn(question, shift=DOWN * 0.2), run_time=2)

        # Step-by-step calculation (left column)
        steps = VGroup(
            VGroup(
                Text("Prior:", font_size=20, color=ELO_BLUE),
                MathTex(r"P(\text{elite}) = 0.10", font_size=24, color=ELO_BLUE),
                Text("Only 10% of rookies are elite", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                Text("Likelihood:", font_size=20, color=ELO_GOLD),
                MathTex(r"P(\text{wins F2} | \text{elite}) = 0.80", font_size=24, color=ELO_GOLD),
                Text("80% of elite drivers won F2", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                Text("Evidence:", font_size=20, color=TEXT_GRAY),
                MathTex(r"P(\text{wins F2}) = 0.15", font_size=24, color=TEXT_GRAY),
                Text("15% of all rookies won F2", font_size=14, color=TEXT_GRAY)
            ),
        )

        for step in steps:
            step.arrange(DOWN, buff=0.06)
        steps.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        steps.move_to(LEFT * 3 + DOWN * 1)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.2), run_time=3.2)
            self.wait(1.2)

        # Calculation (right column)
        calc = VGroup(
            MathTex(r"P(\text{elite} | \text{won F2})", font_size=24, color=ELO_GREEN),
            MathTex(r"= \frac{0.80 \times 0.10}{0.15}", font_size=28, color=TEXT_WHITE),
            MathTex(r"= \frac{0.08}{0.15}", font_size=28, color=TEXT_WHITE),
            MathTex(r"= 0.53", font_size=36, color=ELO_GREEN),
        )
        calc.arrange(DOWN, buff=0.15)
        calc.move_to(RIGHT * 3 + DOWN * 0.5)

        for line in calc:
            self.play(FadeIn(line, shift=DOWN * 0.2), run_time=2.4)
            self.wait(0.8)

        result_box = SurroundingRectangle(calc[-1], color=ELO_GREEN, buff=0.1, corner_radius=0.08)
        self.play(Create(result_box), run_time=2)
        self.play(Indicate(calc[-1], color=ELO_GREEN, scale_factor=1.1), run_time=2)

        # Probability bar update
        self.play(*[FadeOut(m) for m in [formula, question, steps, calc, result_box]], run_time=1.2)

        bar_title = Text("Belief Update: 10% -> 53%", font_size=28, color=ELO_GOLD)
        bar_title.move_to(UP * 1.5)
        self.play(FadeIn(bar_title, shift=DOWN * 0.2), run_time=1.2)

        bar_bg = Rectangle(width=8, height=0.8, stroke_color=TEXT_GRAY, fill_opacity=0)
        bar_bg.move_to(DOWN * 0.5)

        prior_bar = Rectangle(
            width=8 * 0.10, height=0.8,
            fill_color=ELO_BLUE, fill_opacity=0.7, stroke_width=0
        )
        prior_bar.align_to(bar_bg, LEFT)
        prior_bar.move_to(DOWN * 0.5, aligned_edge=LEFT)
        prior_label = Text("Prior: 10%", font_size=16, color=ELO_BLUE)
        prior_label.next_to(bar_bg, UP, buff=0.2)

        self.play(Create(bar_bg), FadeIn(prior_bar), FadeIn(prior_label), run_time=2)

        # Animate growth to posterior
        posterior_bar = Rectangle(
            width=8 * 0.53, height=0.8,
            fill_color=ELO_GREEN, fill_opacity=0.7, stroke_width=0
        )
        posterior_bar.align_to(bar_bg, LEFT)
        posterior_bar.move_to(DOWN * 0.5, aligned_edge=LEFT)
        posterior_label = Text("Posterior: 53%", font_size=16, color=ELO_GREEN)
        posterior_label.next_to(bar_bg, UP, buff=0.2)

        self.play(
            Transform(prior_bar, posterior_bar),
            Transform(prior_label, posterior_label),
            run_time=6
        )

        insight = Text(
            "One strong piece of evidence (winning F2) flipped the odds from unlikely to likely!",
            font_size=18, color=ELO_GOLD
        )
        insight.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(insight, shift=UP * 0.3), run_time=4)
        self.wait(35)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene7_6a_ExplainTrueSkill(Scene):
    """Scene 7.6a: TrueSkill's conservative rating R = mu - 3*sigma explained.

    FIXED: new_player and veteran examples kept in top half of screen,
    well away from the takeaway at the bottom. ex_title at DOWN*0.2,
    player examples start at DOWN*1.1, ensuring no overlap.
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("TrueSkill's Conservative Rating", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)

        # The formula
        formula = MathTex(
            r"R", r"=", r"\mu", r"-", r"3", r"\sigma",
            font_size=56
        )
        formula[0].set_color(ELO_GREEN)
        formula[2].set_color(ELO_BLUE)
        formula[4].set_color(ELO_PURPLE)
        formula[5].set_color(ELO_PURPLE)
        formula.move_to(UP * 1.5)
        self.play(Write(formula), run_time=6)

        # What each part means (3 columns, well spaced)
        parts = VGroup(
            VGroup(
                MathTex(r"\mu", font_size=36, color=ELO_BLUE),
                Text("Best estimate of skill", font_size=17, color=TEXT_GRAY),
                Text("(center of bell curve)", font_size=13, color=TEXT_GRAY)
            ),
            VGroup(
                MathTex(r"\sigma", font_size=36, color=ELO_PURPLE),
                Text("How uncertain we are", font_size=17, color=TEXT_GRAY),
                Text("(width of bell curve)", font_size=13, color=TEXT_GRAY)
            ),
            VGroup(
                MathTex(r"3\sigma", font_size=36, color=ELO_PURPLE),
                Text("Safety margin", font_size=17, color=TEXT_GRAY),
                Text("(99.7% confident above R)", font_size=13, color=ELO_GREEN)
            ),
        )
        for p in parts:
            p.arrange(DOWN, buff=0.06)
        parts.arrange(RIGHT, buff=1.2)
        parts.move_to(DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in parts], lag_ratio=0.2),
            run_time=4
        )
        self.wait(20)

        # Transition to two-player examples
        self.play(FadeOut(parts), run_time=1.2)

        # ex_title at DOWN*0.2 (title)
        ex_title = Text("Two Players - Same mu, Different sigma", font_size=22, color=ELO_GOLD)
        ex_title.move_to(DOWN * 0.2)
        self.play(FadeIn(ex_title, shift=DOWN * 0.2), run_time=1.2)

        # New player examples start at DOWN*1.1 to avoid overlapping ex_title
        # New player box
        new_box = RoundedRectangle(
            width=4.5, height=1.8, corner_radius=0.12,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_RED, stroke_width=1.5
        )
        new_box.move_to(LEFT * 3 + DOWN * 1.9)

        new_player = VGroup(
            Text("New Player (5 games)", font_size=18, color=ELO_RED, weight=BOLD),
            MathTex(r"\mu = 25, \quad \sigma = 8.33", font_size=22, color=TEXT_WHITE),
            MathTex(r"R = 25 - 3(8.33) = 0", font_size=22, color=ELO_RED),
        )
        new_player.arrange(DOWN, buff=0.12)
        new_player.move_to(new_box)

        # Veteran box
        vet_box = RoundedRectangle(
            width=4.5, height=1.8, corner_radius=0.12,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_GREEN, stroke_width=1.5
        )
        vet_box.move_to(RIGHT * 3 + DOWN * 1.9)

        veteran = VGroup(
            Text("Veteran (500 games)", font_size=18, color=ELO_GREEN, weight=BOLD),
            MathTex(r"\mu = 35, \quad \sigma = 1.0", font_size=22, color=TEXT_WHITE),
            MathTex(r"R = 35 - 3(1.0) = 32", font_size=22, color=ELO_GREEN),
        )
        veteran.arrange(DOWN, buff=0.12)
        veteran.move_to(vet_box)

        self.play(
            FadeIn(new_box), FadeIn(new_player, shift=RIGHT * 0.2),
            run_time=3.2
        )
        self.play(
            FadeIn(vet_box), FadeIn(veteran, shift=LEFT * 0.2),
            run_time=3.2
        )

        # Indicate the R values
        self.play(Indicate(new_player[-1], color=ELO_RED, scale_factor=1.1), run_time=2)
        self.play(Indicate(veteran[-1], color=ELO_GREEN, scale_factor=1.1), run_time=2)

        # Takeaway (bottom edge - safe distance from boxes above)
        takeaway_box = RoundedRectangle(
            width=9, height=0.8, corner_radius=0.1,
            fill_color=ELO_GOLD, fill_opacity=0.12,
            stroke_color=ELO_GOLD, stroke_width=1.5
        )
        takeaway_box.to_edge(DOWN, buff=0.6)
        takeaway = Text(
            "You must PROVE your skill (reduce sigma) before your rating rises",
            font_size=19, color=ELO_GOLD
        )
        takeaway.move_to(takeaway_box)
        self.play(FadeIn(takeaway_box), FadeIn(takeaway, shift=UP * 0.2), run_time=4)
        self.wait(35)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)
