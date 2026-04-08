# Section 8: Bradley-Terry-Luce Model
# 4 Scenes covering the theoretical foundations

from manim import *
import numpy as np
import sys
sys.path.append('..')
from utils.colors import *


class Scene8_1_BTLFoundation(Scene):
    """Scene 8.1: The BTL Foundation - Latent strength ratio."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Bradley-Terry-Luce Model", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        subtitle = Text("The mathematical foundation of pairwise comparison", font_size=20, color=TEXT_GRAY)
        subtitle.next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=0.5)
        
        # Core idea
        idea = Text("Each competitor has a latent 'strength' parameter", font_size=22, color=TEXT_LIGHT)
        idea.move_to(UP * 1)
        
        self.play(Write(idea), run_time=1)
        
        # Formula
        formula = MathTex(
            r"P(i > j) = \frac{v_i}{v_i + v_j}",
            font_size=44
        )
        formula.move_to(ORIGIN)
        formula.set_color_by_tex("v_i", ELO_BLUE)
        formula.set_color_by_tex("v_j", ELO_RED)
        
        self.play(Write(formula), run_time=1.5)
        
        # Visual: two bars
        bar_i = Rectangle(width=0.8, height=2, fill_color=ELO_BLUE, fill_opacity=0.7)
        bar_i.move_to(LEFT * 2.5 + DOWN * 2)
        label_i = MathTex(r"v_i", font_size=24, color=ELO_BLUE)
        label_i.next_to(bar_i, DOWN, buff=0.1)
        name_i = Text("Player i", font_size=16, color=TEXT_GRAY)
        name_i.next_to(label_i, DOWN, buff=0.1)
        
        bar_j = Rectangle(width=0.8, height=1.3, fill_color=ELO_RED, fill_opacity=0.7)
        bar_j.move_to(RIGHT * 2.5 + DOWN * 2)
        bar_j.align_to(bar_i, DOWN)
        label_j = MathTex(r"v_j", font_size=24, color=ELO_RED)
        label_j.next_to(bar_j, DOWN, buff=0.1)
        name_j = Text("Player j", font_size=16, color=TEXT_GRAY)
        name_j.next_to(label_j, DOWN, buff=0.1)
        
        self.play(
            FadeIn(bar_i), FadeIn(label_i), FadeIn(name_i),
            FadeIn(bar_j), FadeIn(label_j), FadeIn(name_j),
            run_time=1
        )
        
        # Probability calculation
        prob_calc = MathTex(
            r"P(i > j) = \frac{2.0}{2.0 + 1.3} \approx 60\%",
            font_size=28,
            color=ELO_GREEN
        )
        prob_calc.move_to(DOWN * 2 + RIGHT * 0)
        
        self.play(Write(prob_calc), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene8_2_LogDomain(Scene):
    """Scene 8.2: Log-Domain Transformation - Recovers logistic."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Log-Domain Transformation", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Original form
        original = MathTex(
            r"P(i > j) = \frac{v_i}{v_i + v_j}",
            font_size=36
        )
        original.move_to(UP * 1.5 + LEFT * 3)
        original_label = Text("BTL form", font_size=18, color=TEXT_GRAY)
        original_label.next_to(original, DOWN, buff=0.2)
        
        self.play(Write(original), FadeIn(original_label), run_time=1)
        
        # Transformation
        arrow = Arrow(LEFT * 0.5, RIGHT * 0.5, color=ELO_GOLD)
        arrow.move_to(UP * 1.5)
        trans_label = Text("Let s = log(v)", font_size=16, color=ELO_GOLD)
        trans_label.next_to(arrow, UP, buff=0.1)
        
        self.play(Create(arrow), FadeIn(trans_label), run_time=0.5)
        
        # Log form
        log_form = MathTex(
            r"P(i > j) = \sigma(s_i - s_j)",
            font_size=36
        )
        log_form.move_to(UP * 1.5 + RIGHT * 3)
        log_label = Text("Logistic form", font_size=18, color=TEXT_GRAY)
        log_label.next_to(log_form, DOWN, buff=0.2)
        
        self.play(Write(log_form), FadeIn(log_label), run_time=1)
        
        # Sigmoid definition
        sigmoid = MathTex(
            r"\sigma(x) = \frac{1}{1 + e^{-x}}",
            font_size=32,
            color=ELO_GREEN
        )
        sigmoid.move_to(DOWN * 0.3)
        
        self.play(Write(sigmoid), run_time=1)
        
        # Connection to Elo
        connection = VGroup(
            Text("This IS the Elo formula!", font_size=24, color=ELO_GOLD),
            MathTex(r"10^x = e^{x \ln 10}", font_size=24, color=TEXT_GRAY),
            Text("Just a change of base", font_size=18, color=TEXT_GRAY)
        )
        connection.arrange(DOWN, buff=0.2)
        connection.move_to(DOWN * 2)
        
        box = SurroundingRectangle(connection, color=ELO_GOLD, buff=0.2)
        
        self.play(Write(connection), Create(box), run_time=1.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene8_3_Intransitivity(Scene):
    """Scene 8.3: The Intransitivity Problem - Rock-paper-scissors."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("The Intransitivity Problem", font_size=44, color=ELO_RED)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Standard assumption
        assumption = Text(
            "Standard assumption: A > B and B > C implies A > C",
            font_size=22,
            color=TEXT_LIGHT
        )
        assumption.move_to(UP * 1.5)
        
        self.play(Write(assumption), run_time=1)
        
        # But F1 is different...
        but = Text("But in F1...", font_size=24, color=ELO_GOLD)
        but.move_to(UP * 0.7)
        
        self.play(Write(but), run_time=0.5)
        
        # Three cars in a cycle
        # Positions on a triangle
        positions = [
            UP * 0.5,
            DOWN * 1.5 + LEFT * 2,
            DOWN * 1.5 + RIGHT * 2
        ]
        
        cars = [
            {"name": "Low Drag", "track": "Monza", "color": ELO_BLUE},
            {"name": "Balanced", "track": "Silverstone", "color": ELO_GOLD},
            {"name": "High DF", "track": "Monaco", "color": ELO_RED}
        ]
        
        car_groups = VGroup()
        for pos, car in zip(positions, cars):
            rect = Rectangle(
                width=1.8, height=0.8,
                fill_color=car["color"], fill_opacity=0.6,
                stroke_color=car["color"]
            )
            rect.move_to(pos)
            name = Text(car["name"], font_size=14, color=TEXT_WHITE)
            name.move_to(rect)
            track = Text(f'wins at {car["track"]}', font_size=12, color=TEXT_GRAY)
            track.next_to(rect, DOWN, buff=0.1)
            car_groups.add(VGroup(rect, name, track))
        
        self.play(FadeIn(car_groups), run_time=1)
        
        # Arrows showing cycle
        arrows = VGroup()
        for i in range(3):
            start = positions[i]
            end = positions[(i + 1) % 3]
            
            # Offset to avoid overlap
            direction = end - start
            direction = direction / np.linalg.norm(direction)
            
            arrow = Arrow(
                start + direction * 0.6,
                end - direction * 0.6,
                color=ELO_GREEN,
                buff=0.1
            )
            arrows.add(arrow)
        
        self.play(Create(arrows), run_time=1)
        
        # Cycle label
        cycle = Text("Cyclic dominance!", font_size=24, color=ELO_RED)
        cycle.move_to(DOWN * 3)
        
        self.play(Write(cycle), run_time=0.8)
        
        # RPS analogy
        rps = Text(
            "Like Rock-Paper-Scissors: no global ranking possible",
            font_size=20,
            color=TEXT_GRAY
        )
        rps.to_edge(DOWN, buff=0.3)
        
        self.play(Write(rps), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene8_4_HodgeDecomposition(Scene):
    """Scene 8.4: Hodge Decomposition - Gradient vs Curl."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Hodge Decomposition", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        subtitle = Text("Separating global skill from local interactions", font_size=20, color=TEXT_GRAY)
        subtitle.next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=0.5)
        
        # Formula
        formula = MathTex(
            r"s_{ij}", r"=", r"(r_i - r_j)", r"+", r"\epsilon_{ij}",
            font_size=40
        )
        formula.move_to(UP * 1)
        
        formula[0].set_color(TEXT_WHITE)    # Observed
        formula[2].set_color(ELO_BLUE)       # Gradient
        formula[4].set_color(ELO_RED)        # Curl
        
        self.play(Write(formula), run_time=1.5)
        
        # Labels
        obs_label = Text("Observed edge", font_size=16, color=TEXT_GRAY)
        obs_label.next_to(formula[0], DOWN, buff=0.5)
        
        grad_label = Text("Gradient", font_size=16, color=ELO_BLUE)
        grad_label.next_to(formula[2], DOWN, buff=0.5)
        
        curl_label = Text("Curl", font_size=16, color=ELO_RED)
        curl_label.next_to(formula[4], DOWN, buff=0.5)
        
        self.play(FadeIn(obs_label), FadeIn(grad_label), FadeIn(curl_label), run_time=0.8)
        
        # Visual: Flow diagram
        # Gradient = smooth flow
        gradient_group = VGroup()
        grad_title = Text("Gradient Component", font_size=18, color=ELO_BLUE)
        grad_title.move_to(LEFT * 3.5 + DOWN * 1.5)
        
        # Smooth arrows flowing down
        for i in range(3):
            arrow = Arrow(
                LEFT * 4 + DOWN * (1.8 + i * 0.4),
                LEFT * 3 + DOWN * (2.0 + i * 0.4),
                color=ELO_BLUE,
                stroke_width=2
            )
            gradient_group.add(arrow)
        
        grad_desc = Text("Global transitive skill", font_size=14, color=TEXT_GRAY)
        grad_desc.next_to(gradient_group, DOWN, buff=0.1)
        
        self.play(Write(grad_title), Create(gradient_group), FadeIn(grad_desc), run_time=1)
        
        # Curl = vortex
        curl_group = VGroup()
        curl_title = Text("Curl Component", font_size=18, color=ELO_RED)
        curl_title.move_to(RIGHT * 3.5 + DOWN * 1.5)
        
        # Circular arrows
        center = RIGHT * 3.5 + DOWN * 2.3
        for angle in [0, 120, 240]:
            start_a = angle * DEGREES
            end_a = (angle + 90) * DEGREES
            arc = Arc(
                radius=0.5,
                start_angle=start_a,
                angle=0.5 * PI,
                color=ELO_RED
            )
            arc.move_to(center)
            arc.add_tip(tip_length=0.15)
            curl_group.add(arc)
        
        curl_desc = Text("Specific matchup effects", font_size=14, color=TEXT_GRAY)
        curl_desc.move_to(RIGHT * 3.5 + DOWN * 3.2)
        
        self.play(Write(curl_title), Create(curl_group), FadeIn(curl_desc), run_time=1)
        
        # Summary
        summary = Text(
            "Hodge: Cleanly separate 'who is better overall' from 'matchup quirks'",
            font_size=18,
            color=ELO_GOLD
        )
        summary.to_edge(DOWN, buff=0.3)
        
        self.play(Write(summary), run_time=1.5)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene8_1a_ExplainBTL(Scene):
    """Scene 8.1a: BTL — Strength Ratios as Probabilities."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("BTL: Strength Ratios as Probabilities", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"P(i > j) = \frac{v_i}{v_i + v_j}",
            font_size=44
        )
        formula.move_to(UP * 1.5)
        self.play(Write(formula), run_time=1.5)

        # Step 1 — What is v?
        step1 = Text("① What is v?", font_size=22, color=ELO_GOLD)
        step1.move_to(LEFT * 4.5 + DOWN * 0.2)
        self.play(FadeIn(step1), run_time=0.3)

        v_explain = VGroup(
            Text("v = hidden 'strength' number", font_size=18, color=TEXT_GRAY),
            Text("Always positive (like a weight)", font_size=16, color=TEXT_GRAY),
            Text("Higher v = stronger competitor", font_size=16, color=ELO_GREEN)
        )
        v_explain.arrange(DOWN, buff=0.1)
        v_explain.move_to(DOWN * 1)
        self.play(FadeIn(v_explain), run_time=0.8)
        self.wait(0.8)

        # Step 2 — Worked example
        self.play(FadeOut(step1), FadeOut(v_explain), run_time=0.3)
        step2 = Text("② Worked Example", font_size=22, color=ELO_GOLD)
        step2.move_to(LEFT * 4.5 + DOWN * 0.2)
        self.play(FadeIn(step2), run_time=0.3)

        ex = VGroup(
            Text("Hamilton: v = 80     Verstappen: v = 120", font_size=20, color=TEXT_GRAY),
            MathTex(r"P(\text{HAM} > \text{VER}) = \frac{80}{80+120} = \frac{80}{200} = 40\%",
                    font_size=28, color=ELO_BLUE),
            MathTex(r"P(\text{VER} > \text{HAM}) = \frac{120}{80+120} = \frac{120}{200} = 60\%",
                    font_size=28, color=ELO_RED),
        )
        ex.arrange(DOWN, buff=0.2)
        ex.move_to(DOWN * 1)
        self.play(FadeIn(ex), run_time=1)
        self.wait(0.5)

        # Step 3 — They sum to 100%
        self.play(FadeOut(step2), FadeOut(ex), run_time=0.3)
        step3 = Text("③ Key Property", font_size=22, color=ELO_GOLD)
        step3.move_to(LEFT * 4.5 + DOWN * 0.2)
        self.play(FadeIn(step3), run_time=0.3)

        symmetry = VGroup(
            MathTex(r"P(i > j) + P(j > i) = 1", font_size=36, color=ELO_GREEN),
            Text("Probabilities always sum to 100% — guaranteed!", font_size=18, color=TEXT_GRAY),
        )
        symmetry.arrange(DOWN, buff=0.2)
        symmetry.move_to(DOWN * 0.5)
        symmetry_box = SurroundingRectangle(symmetry, color=ELO_GREEN, buff=0.15)
        self.play(FadeIn(symmetry), Create(symmetry_box), run_time=1)

        # Pie chart visual
        pie_center = RIGHT * 4 + DOWN * 0.5
        circle = Circle(radius=1.2, color=TEXT_GRAY, stroke_width=2)
        circle.move_to(pie_center)

        # 40% blue, 60% red
        arc_blue = AnnularSector(
            inner_radius=0, outer_radius=1.2,
            angle=0.4 * TAU, start_angle=PI/2,
            color=ELO_BLUE, fill_opacity=0.6
        )
        arc_blue.move_to(pie_center)

        arc_red = AnnularSector(
            inner_radius=0, outer_radius=1.2,
            angle=0.6 * TAU, start_angle=PI/2 + 0.4 * TAU,
            color=ELO_RED, fill_opacity=0.6
        )
        arc_red.move_to(pie_center)

        pie_label_b = Text("40%", font_size=16, color=TEXT_WHITE)
        pie_label_b.move_to(pie_center + UP * 0.5 + LEFT * 0.3)
        pie_label_r = Text("60%", font_size=16, color=TEXT_WHITE)
        pie_label_r.move_to(pie_center + DOWN * 0.3 + RIGHT * 0.1)

        self.play(FadeIn(arc_blue), FadeIn(arc_red), FadeIn(pie_label_b), FadeIn(pie_label_r), run_time=0.8)

        takeaway = Text(
            "BTL: the probability is simply each player's share of the total strength pool",
            font_size=16, color=ELO_GOLD
        )
        takeaway.to_edge(DOWN, buff=0.4)
        self.play(Write(takeaway), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene8_2a_ExplainLogSigmoid(Scene):
    """Scene 8.2a: From Ratios to the Sigmoid — the log-domain connection."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("From Ratios to the Sigmoid", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Step 1 — Start with BTL
        step1 = MathTex(r"\text{Start: } \frac{v_i}{v_i + v_j}", font_size=32, color=TEXT_WHITE)
        step1.move_to(UP * 1.2)
        self.play(Write(step1), run_time=0.8)

        # Step 2 — Divide top/bottom by v_j
        step2 = MathTex(
            r"= \frac{v_i / v_j}{1 + v_i / v_j}", r"\quad \text{(divide by } v_j \text{)}",
            font_size=28, color=TEXT_WHITE
        )
        step2.move_to(UP * 0.4)
        self.play(Write(step2), run_time=0.8)

        # Step 3 — Let r = v_i/v_j, take log
        step3 = VGroup(
            MathTex(r"\text{Let } s = \log(v), \quad s_i - s_j = \log(v_i/v_j)", font_size=24, color=ELO_GOLD),
        )
        step3.move_to(DOWN * 0.3)
        self.play(Write(step3), run_time=0.8)

        # Step 4 — Result is the sigmoid
        step4 = MathTex(
            r"= \frac{e^{s_i - s_j}}{1 + e^{s_i - s_j}} = \frac{1}{1 + e^{-(s_i - s_j)}} = \sigma(s_i - s_j)",
            font_size=28, color=ELO_GREEN
        )
        step4.move_to(DOWN * 1.2)
        result_box = SurroundingRectangle(step4, color=ELO_GREEN, buff=0.1)
        self.play(Write(step4), Create(result_box), run_time=1.5)

        self.wait(1)

        # Clear and show sigmoid plot
        self.play(*[FadeOut(m) for m in [step1, step2, step3, step4, result_box]], run_time=0.3)

        # Step 5 — Plot
        plot_title = Text("The Sigmoid Curve", font_size=24, color=ELO_GOLD)
        plot_title.next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(plot_title), run_time=0.3)

        axes = Axes(
            x_range=[-6, 6, 2], y_range=[0, 1, 0.25],
            x_length=10, y_length=3.5, tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.move_to(DOWN * 0.5)

        x_label = MathTex(r"s_i - s_j", font_size=18, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = MathTex(r"P(i > j)", font_size=18, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)

        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        curve = axes.plot(sigmoid, x_range=[-6, 6], color=ELO_GREEN)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), Create(curve), run_time=1.5)

        # Mark key point: s_i = s_j -> 50%
        dot_50 = Dot(axes.c2p(0, 0.5), color=ELO_GOLD, radius=0.1)
        dot_label = Text("Equal skill → 50%", font_size=14, color=ELO_GOLD)
        dot_label.next_to(dot_50, UR, buff=0.1)
        self.play(FadeIn(dot_50), FadeIn(dot_label), run_time=0.5)

        # Step 6 — Connection to Elo
        connection = VGroup(
            Text("This IS the Elo formula!", font_size=22, color=ELO_GOLD),
            MathTex(r"\sigma(s_i - s_j) = \frac{1}{1+10^{(R_j - R_i)/400}}", font_size=24, color=TEXT_WHITE),
            Text("(just uses base-10 instead of base-e, and scales by 400)", font_size=14, color=TEXT_GRAY)
        )
        connection.arrange(DOWN, buff=0.1)
        connection.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(connection), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene8_4a_ExplainHodge(Scene):
    """Scene 8.4a: Hodge Decomposition — What Stays vs What Rotates."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Hodge: What Stays vs What Rotates", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"s_{ij}", r"=", r"(r_i - r_j)", r"+", r"\varepsilon_{ij}",
            font_size=44
        )
        formula[0].set_color(TEXT_WHITE)
        formula[2].set_color(ELO_BLUE)
        formula[4].set_color(ELO_RED)
        formula.move_to(UP * 1.5)
        self.play(Write(formula), run_time=1.5)

        # Gradient component
        grad = VGroup(
            MathTex(r"(r_i - r_j)", font_size=32, color=ELO_BLUE),
            Text("= Gradient (Global Ranking)", font_size=18, color=TEXT_GRAY),
            Text("Consistent with a total ordering", font_size=14, color=TEXT_GRAY),
            Text("If A > B and B > C, then A > C", font_size=14, color=ELO_GREEN)
        )
        grad.arrange(DOWN, buff=0.08)
        grad.move_to(LEFT * 3.5 + DOWN * 0.5)

        # Curl component
        curl = VGroup(
            MathTex(r"\varepsilon_{ij}", font_size=32, color=ELO_RED),
            Text("= Curl (Matchup-Specific)", font_size=18, color=TEXT_GRAY),
            Text("NOT consistent with a ranking", font_size=14, color=TEXT_GRAY),
            Text("A > B, B > C, but C > A!", font_size=14, color=ELO_RED)
        )
        curl.arrange(DOWN, buff=0.08)
        curl.move_to(RIGHT * 3.5 + DOWN * 0.5)

        self.play(FadeIn(grad), FadeIn(curl), run_time=1)
        self.wait(1)

        # Rock-Paper-Scissors analogy
        self.play(FadeOut(grad), FadeOut(curl), run_time=0.3)

        rps_title = Text("Rock-Paper-Scissors = Pure Curl", font_size=24, color=ELO_GOLD)
        rps_title.move_to(DOWN * 0.3)
        self.play(FadeIn(rps_title), run_time=0.3)

        # Triangle diagram
        a_pos = UP * 0.5 + LEFT * 0
        b_pos = DOWN * 1 + LEFT * 1.5
        c_pos = DOWN * 1 + RIGHT * 1.5

        dot_a = VGroup(Circle(radius=0.3, color=ELO_BLUE, fill_opacity=0.5), Text("A", font_size=18))
        dot_b = VGroup(Circle(radius=0.3, color=ELO_GREEN, fill_opacity=0.5), Text("B", font_size=18))
        dot_c = VGroup(Circle(radius=0.3, color=ELO_RED, fill_opacity=0.5), Text("C", font_size=18))

        dots_grp = VGroup(dot_a, dot_b, dot_c)
        dot_a.move_to(a_pos + DOWN * 1.5)
        dot_b.move_to(b_pos + DOWN * 1.5)
        dot_c.move_to(c_pos + DOWN * 1.5)

        arrow_ab = Arrow(dot_a.get_bottom(), dot_b.get_top(), color=ELO_BLUE, buff=0.3)
        arrow_bc = Arrow(dot_b.get_right(), dot_c.get_left(), color=ELO_GREEN, buff=0.3)
        arrow_ca = Arrow(dot_c.get_top(), dot_a.get_bottom(), color=ELO_RED, buff=0.3)

        label_ab = Text("A > B", font_size=12, color=TEXT_GRAY)
        label_ab.next_to(arrow_ab, LEFT, buff=0.1)
        label_bc = Text("B > C", font_size=12, color=TEXT_GRAY)
        label_bc.next_to(arrow_bc, DOWN, buff=0.1)
        label_ca = Text("C > A", font_size=12, color=TEXT_GRAY)
        label_ca.next_to(arrow_ca, RIGHT, buff=0.1)

        self.play(
            FadeIn(dots_grp),
            Create(arrow_ab), Create(arrow_bc), Create(arrow_ca),
            FadeIn(label_ab), FadeIn(label_bc), FadeIn(label_ca),
            run_time=1.5
        )

        no_ranking = Text("No global ranking exists! This is all curl.", font_size=16, color=ELO_RED)
        no_ranking.next_to(dots_grp, DOWN, buff=0.8)
        self.play(FadeIn(no_ranking), run_time=0.5)

        # F1 connection
        f1_note = Text(
            "F1: some tracks suit some cars — creating 'curl' that Hodge separates out",
            font_size=16, color=ELO_GOLD
        )
        f1_note.to_edge(DOWN, buff=0.3)
        self.play(Write(f1_note), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
