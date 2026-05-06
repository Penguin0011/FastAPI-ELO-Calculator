# Section 9: Plackett-Luce for Rank-Ordered Lists
# 4 Scenes covering multi-competitor modeling

from manim import *
from manim.utils.color.core import interpolate_color as manim_interpolate_color
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *
import numpy as np


class Scene9_1_BeyondPairwise(Scene):
    """Scene 9.1: Beyond Pairwise Comparison."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Beyond Pairwise Comparison", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Elo approach
        elo_box = VGroup(
            Text("Elo Approach", font_size=24, color=ELO_RED),
            Text("Race -> 190 pairwise results", font_size=18, color=TEXT_GRAY),
            Text("Process each independently", font_size=18, color=TEXT_GRAY)
        )
        elo_box.arrange(DOWN, buff=0.15)
        elo_box.move_to(LEFT * 3.5 + UP * 0.5)
        
        elo_rect = SurroundingRectangle(elo_box, color=ELO_RED, buff=0.2)
        
        self.play(FadeIn(elo_box), Create(elo_rect), run_time=4)
        
        # vs
        vs = Text("vs", font_size=24, color=TEXT_GRAY)
        vs.move_to(UP * 0.5)
        
        self.play(Write(vs), run_time=1.2)
        
        # Plackett-Luce approach
        pl_box = VGroup(
            Text("Plackett-Luce", font_size=24, color=ELO_GREEN),
            Text("Race = single observation", font_size=18, color=TEXT_GRAY),
            Text("20-position ordering", font_size=18, color=TEXT_GRAY)
        )
        pl_box.arrange(DOWN, buff=0.15)
        pl_box.move_to(RIGHT * 3.5 + UP * 0.5)
        
        pl_rect = SurroundingRectangle(pl_box, color=ELO_GREEN, buff=0.2)
        
        self.play(FadeIn(pl_box), Create(pl_rect), run_time=4)
        
        # Visual: permutation representation
        perm_label = Text("Race result as permutation:", font_size=20, color=TEXT_LIGHT)
        perm_label.move_to(DOWN * 1.5)
        
        # Positions with drivers
        positions = VGroup()
        for i in range(5):
            pos = Text(f"P{i+1}", font_size=16, color=TEXT_GRAY)
            pos.move_to(LEFT * 4 + RIGHT * i * 2 + DOWN * 2)
            
            driver = Rectangle(
                width=0.8, height=0.5,
                fill_color=ELO_GOLD,
                fill_opacity=0.6
            )
            driver.next_to(pos, DOWN, buff=0.1)
            driver_num = Text(f"D{[3,7,1,4,2][i]}", font_size=14, color=TEXT_WHITE)
            driver_num.move_to(driver)
            
            positions.add(VGroup(pos, driver, driver_num))
        
        dots = Text("...", font_size=24, color=TEXT_GRAY)
        dots.move_to(RIGHT * 4 + DOWN * 2)
        
        self.play(Write(perm_label), run_time=2)
        self.play(FadeIn(positions), FadeIn(dots), run_time=4)
        
        # Caption
        caption = Text(
            "π = (D3, D7, D1, D4, D2, ..., D15) is ONE observation",
            font_size=20,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.4)
        
        self.play(Write(caption), run_time=4)
        
        self.wait(3.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene9_2_SequentialSurvival(Scene):
    """Scene 9.2: Sequential Survival Model."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Sequential Elimination", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Intuition
        intuition = Text(
            "Think of a race as sequential elimination:",
            font_size=22,
            color=TEXT_LIGHT
        )
        intuition.move_to(UP * 1.5)
        
        self.play(Write(intuition), run_time=4)
        
        # Step 1: P1
        step1 = VGroup(
            Text("P1:", font_size=20, color=ELO_GOLD),
            Text("Fastest among ALL 20", font_size=18, color=TEXT_GRAY),
            MathTex(r"P(\text{Ver wins}) = \frac{v_{Ver}}{\sum_{all} v_i}", font_size=24)
        )
        step1.arrange(RIGHT, buff=0.3)
        step1.move_to(UP * 0.5 + LEFT * 1)
        
        self.play(FadeIn(step1), run_time=3.2)
        
        # Visual: 20 dots, one highlighted
        dots1 = VGroup()
        for i in range(20):
            dot = Dot(radius=0.08, color=ELO_BLUE if i > 0 else ELO_GREEN)
            dot.move_to(RIGHT * 4 + UP * 0.5 + UP * (i % 5) * 0.3 + RIGHT * (i // 5) * 0.3)
            dots1.add(dot)
        
        self.play(FadeIn(dots1), run_time=2)
        
        # Step 2: P2
        step2 = VGroup(
            Text("P2:", font_size=20, color=ELO_GOLD),
            Text("Fastest among remaining 19", font_size=18, color=TEXT_GRAY),
            MathTex(r"P(\text{Ham is P2}) = \frac{v_{Ham}}{\sum_{rest} v_i}", font_size=24)
        )
        step2.arrange(RIGHT, buff=0.3)
        step2.move_to(DOWN * 0.3 + LEFT * 1)
        
        self.play(FadeIn(step2), run_time=3.2)
        
        # Visual: remove one dot
        dots2 = dots1.copy()
        dots2.shift(DOWN * 0.8)
        dots2[0].set_opacity(0.3)  # Removed
        dots2[1].set_color(ELO_GREEN)  # New winner
        
        self.play(FadeIn(dots2), run_time=2)
        
        # Continue cascade
        cascade = VGroup(
            Text("P3: Fastest among 18...", font_size=18, color=TEXT_GRAY),
            Text("P4: Fastest among 17...", font_size=18, color=TEXT_GRAY),
            Text("...", font_size=24, color=TEXT_GRAY),
            Text("P20: Last one remaining", font_size=18, color=TEXT_GRAY)
        )
        cascade.arrange(DOWN, buff=0.2)
        cascade.move_to(DOWN * 2 + LEFT * 2)
        
        self.play(FadeIn(cascade), run_time=4)
        
        self.wait(3.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene9_3_LikelihoodFormula(Scene):
    """Scene 9.3: The Likelihood Formula."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Plackett-Luce Likelihood", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Main formula
        formula = MathTex(
            r"P(\pi) = \prod_{k=1}^{n} \frac{\exp(s_{\pi_k})}{\sum_{l=k}^{n} \exp(s_{\pi_l})}",
            font_size=44
        )
        formula.move_to(UP * 1)
        
        self.play(Write(formula), run_time=8)
        
        # Box it
        box = SurroundingRectangle(formula, color=ELO_GOLD, buff=0.2)
        self.play(Create(box), run_time=2)
        
        # Break down components
        components = VGroup(
            MathTex(r"\pi", font_size=32, color=ELO_BLUE),
            Text("= Race finishing order", font_size=18, color=TEXT_GRAY),
            MathTex(r"s_i", font_size=32, color=ELO_GREEN),
            Text("= Latent skill of driver i", font_size=18, color=TEXT_GRAY),
            MathTex(r"\exp(s_i)", font_size=32, color=ELO_GOLD),
            Text("= 'Strength' parameter", font_size=18, color=TEXT_GRAY)
        )
        components.arrange_in_grid(rows=3, cols=2, buff=(0.5, 0.3))
        components.move_to(DOWN * 1.5)
        
        self.play(FadeIn(components), run_time=6)
        
        # Key observation
        observation = Text(
            "Denominator shrinks as positions fill → Information content varies",
            font_size=20,
            color=ELO_GOLD
        )
        observation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(observation), run_time=6)
        
        self.wait(3.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene9_4_InformationWeighting(Scene):
    """Scene 9.4: Information Weighting - Top matters more."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Information Weighting", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Key insight
        insight = Text(
            "Not all positions carry equal information",
            font_size=24,
            color=TEXT_LIGHT
        )
        insight.move_to(UP * 1.5)
        
        self.play(Write(insight), run_time=4)
        
        # Visual: bar chart of information content
        axes = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 14}
        )
        axes.shift(DOWN * 0.5)
        
        x_label = Text("Position", font_size=16, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        
        y_label = Text("Information", font_size=16, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)
        y_label.rotate(90 * DEGREES)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=4)
        
        # Bars with decreasing height
        bars = VGroup()
        heights = [9, 8, 7, 6, 5.5, 5, 4.5, 4, 3.5, 3, 2.8, 2.5, 2.3, 2.1, 1.9, 1.7, 1.5, 1.3, 1.1, 0.9]

        for i, h in enumerate(heights):
            bar = Rectangle(
                width=0.35,
                height=h * 0.3,
                fill_color=manim_interpolate_color(ManimColor(ELO_GREEN), ManimColor(ELO_RED), i / 19),
                fill_opacity=0.8,
                stroke_width=0
            )
            bar.move_to(axes.c2p(i + 0.5, h / 2))
            bar.align_to(axes.c2p(0, 0), DOWN)
            bars.add(bar)
        
        self.play(FadeIn(bars), run_time=6)
        
        # Annotations
        p1_label = Text("P1 vs P2: Big deal!", font_size=16, color=ELO_GREEN)
        p1_label.move_to(axes.c2p(3, 9.5))
        
        p19_label = Text("P19 vs P20: Meh", font_size=16, color=ELO_RED)
        p19_label.move_to(axes.c2p(17, 3))
        
        self.play(FadeIn(p1_label), FadeIn(p19_label), run_time=3.2)
        
        # Reason
        reason = VGroup(
            Text("Why?", font_size=20, color=ELO_GOLD),
            Text("P1: Beat 19 others -> large denominator", font_size=16, color=TEXT_GRAY),
            Text("P20: 'Beat' nobody -> tiny denominator", font_size=16, color=TEXT_GRAY)
        )
        reason.arrange(DOWN, buff=0.15)
        reason.to_edge(DOWN, buff=0.3)
        
        self.play(FadeIn(reason), run_time=4)
        
        self.wait(3.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene9_4a_ExplainPLLikelihood(Scene):
    """Scene 9.4a: Plackett-Luce Likelihood — Step by Step."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Plackett-Luce: Step by Step", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)

        # The big formula
        formula = MathTex(
            r"P(\pi) = \prod_{k=1}^{n} \frac{e^{s_{\pi_k}}}{\sum_{l=k}^{n} e^{s_{\pi_l}}}",
            font_size=40
        )
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=6)

        # Step 1: A race as sequential elimination
        step_title = Text("A Race as Sequential Picks", font_size=22, color=ELO_GOLD)
        step_title.next_to(formula, DOWN, buff=0.4)
        self.play(FadeIn(step_title), run_time=1.2)

        # 4-driver example with strength scores
        drivers = [
            ("VER", 3.0, ELO_RED),
            ("HAM", 2.5, ELO_BLUE),
            ("LEC", 2.0, ELO_GREEN),
            ("NOR", 1.5, ELO_PURPLE),
        ]

        scores_text = VGroup()
        for name, score, color in drivers:
            row = Text(f"{name}: s = {score}", font_size=16, color=color)
            scores_text.add(row)
        scores_text.arrange(RIGHT, buff=1)
        scores_text.move_to(DOWN * 0.3)
        self.play(FadeIn(scores_text), run_time=2)

        # Calculate exp scores
        import math
        exp_scores = [(name, math.exp(score), color) for name, score, color in drivers]
        total = sum(e for _, e, _ in exp_scores)

        # Stage 1: P(VER wins from all 4)
        stages = VGroup()

        s1_total = sum(e for _, e, _ in exp_scores)
        s1 = VGroup(
            Text("Stage 1: Who finishes P1? (from 4)", font_size=16, color=ELO_GOLD),
            MathTex(
                r"P(\text{VER}) = \frac{e^{3.0}}{e^{3.0}+e^{2.5}+e^{2.0}+e^{1.5}} = "
                + f"{exp_scores[0][1]/s1_total:.2f}",
                font_size=20, color=ELO_RED
            )
        )
        s1.arrange(DOWN, buff=0.08)

        s2_total = sum(e for _, e, _ in exp_scores[1:])
        s2 = VGroup(
            Text("Stage 2: Who finishes P2? (from 3)", font_size=16, color=ELO_GOLD),
            MathTex(
                r"P(\text{HAM}) = \frac{e^{2.5}}{e^{2.5}+e^{2.0}+e^{1.5}} = "
                + f"{exp_scores[1][1]/s2_total:.2f}",
                font_size=20, color=ELO_BLUE
            )
        )
        s2.arrange(DOWN, buff=0.08)

        s3_total = sum(e for _, e, _ in exp_scores[2:])
        s3 = VGroup(
            Text("Stage 3: Who finishes P3? (from 2)", font_size=16, color=ELO_GOLD),
            MathTex(
                r"P(\text{LEC}) = \frac{e^{2.0}}{e^{2.0}+e^{1.5}} = "
                + f"{exp_scores[2][1]/s3_total:.2f}",
                font_size=20, color=ELO_GREEN
            )
        )
        s3.arrange(DOWN, buff=0.08)

        stages = VGroup(s1, s2, s3)
        stages.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        stages.move_to(DOWN * 2)

        for stage in stages:
            self.play(FadeIn(stage), run_time=2.4)
            self.wait(1.2)

        # Final multiply
        p_total = (exp_scores[0][1]/s1_total) * (exp_scores[1][1]/s2_total) * (exp_scores[2][1]/s3_total)

        self.play(*[FadeOut(m) for m in [step_title, scores_text, stages, formula]], run_time=1.2)

        final = VGroup(
            Text("Multiply all stages:", font_size=22, color=ELO_GOLD),
            MathTex(
                f"P(\\text{{VER→HAM→LEC→NOR}}) = {exp_scores[0][1]/s1_total:.2f} \\times "
                f"{exp_scores[1][1]/s2_total:.2f} \\times {exp_scores[2][1]/s3_total:.2f} = {p_total:.3f}",
                font_size=24, color=ELO_GREEN
            ),
            Text("The full ranking probability — product of each stage!", font_size=16, color=TEXT_GRAY)
        )
        final.arrange(DOWN, buff=0.2)
        final.move_to(ORIGIN)

        self.play(FadeIn(final), run_time=4)
        final_box = SurroundingRectangle(final[1], color=ELO_GREEN, buff=0.1)
        self.play(Create(final_box), run_time=2)

        self.wait(3.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene9_5a_ExplainInfoWeighting(Scene):
    """Scene 9.5a: Why P1 Matters More Than P10."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Why P1 Matters More Than P10", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)

        # Step 1: P1 is chosen from ALL drivers
        step1 = Text("(1) P1 is selected from ALL 20 drivers", font_size=22, color=ELO_GOLD)
        step1.next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(step1), run_time=1.2)

        p1_explain = VGroup(
            Text("Being the BEST of 20 is very informative", font_size=18, color=TEXT_GRAY),
            MathTex(r"\text{Pool size} = 20 \text{ drivers}", font_size=24, color=ELO_GREEN)
        )
        p1_explain.arrange(DOWN, buff=0.15)
        p1_explain.move_to(UP * 0.3)
        self.play(FadeIn(p1_explain), run_time=2.4)
        self.wait(2)

        # Step 2: P10 is picked from remaining 11
        step2 = Text("(2) P10 is selected from remaining 11", font_size=22, color=ELO_GOLD)
        step2.next_to(header, DOWN, buff=0.3)
        self.play(FadeOut(step1), FadeIn(step2), run_time=1.2)

        p10_explain = VGroup(
            Text("Being best of 11 is less selective", font_size=18, color=TEXT_GRAY),
            MathTex(r"\text{Pool size} = 11 \text{ drivers}", font_size=24, color=ELO_RED)
        )
        p10_explain.arrange(DOWN, buff=0.15)
        p10_explain.next_to(p1_explain, DOWN, buff=0.3)
        self.play(FadeIn(p10_explain), run_time=2.4)
        self.wait(2)

        # Step 3: Bar chart of information by position
        self.play(*[FadeOut(m) for m in [step2, p1_explain, p10_explain]], run_time=1.2)
        step3 = Text("(3) Information Content by Position", font_size=22, color=ELO_GOLD)
        step3.next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(step3), run_time=1.2)

        positions = list(range(1, 21))
        pool_sizes = list(range(20, 0, -1))
        # Normalize information ~ log(pool_size)
        import math
        info_values = [math.log(p) for p in pool_sizes]
        max_info = max(info_values)

        bars = VGroup()
        for i, (pos, info) in enumerate(zip(positions, info_values)):
            bar_height = (info / max_info) * 3.0
            t = i / 19  # interpolation 0 to 1
            color = interpolate_color(ManimColor(ELO_GREEN), ManimColor(ELO_RED), t)
            bar = Rectangle(
                width=0.35, height=max(bar_height, 0.05),
                fill_color=color, fill_opacity=0.7,
                stroke_width=0.5
            )
            bar.move_to(LEFT * 5 + RIGHT * i * 0.5 + DOWN * 1.5, aligned_edge=DOWN)
            bars.add(bar)

        self.play(FadeIn(bars), run_time=4)

        # Labels for P1 and P20
        p1_label = Text("P1", font_size=10, color=TEXT_WHITE)
        p1_label.next_to(bars[0], DOWN, buff=0.1)
        p5_label = Text("P5", font_size=10, color=TEXT_WHITE)
        p5_label.next_to(bars[4], DOWN, buff=0.1)
        p10_label = Text("P10", font_size=10, color=TEXT_WHITE)
        p10_label.next_to(bars[9], DOWN, buff=0.1)
        p20_label = Text("P20", font_size=10, color=TEXT_WHITE)
        p20_label.next_to(bars[19], DOWN, buff=0.1)

        self.play(FadeIn(p1_label), FadeIn(p5_label), FadeIn(p10_label), FadeIn(p20_label), run_time=2)

        y_label = Text("Information (more ->)", font_size=14, color=TEXT_GRAY)
        y_label.next_to(bars, LEFT, buff=0.3)
        self.play(FadeIn(y_label), run_time=1.2)

        # Takeaway
        takeaway = Text(
            "Podium battles tell us the most about true skill; backmarker results are noisy",
            font_size=18, color=ELO_GOLD
        )
        takeaway.to_edge(DOWN, buff=0.3)
        self.play(Write(takeaway), run_time=4)

        self.wait(3.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)
