# Section 11: Physics-Informed Priors - Telemetry Sub-Model
# 5 Scenes covering telemetry analysis

from manim import *
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *
import numpy as np


class Scene11_1_TelemetryTruth(Scene):
    """Scene 11.1: Telemetry Doesn't Lie."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Telemetry: The Hidden Truth", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Scenario
        scenario = VGroup(
            Text("Race Result: P10", font_size=24, color=ELO_RED),
            Text("Reason: Terrible pit strategy", font_size=18, color=TEXT_GRAY)
        )
        scenario.arrange(DOWN, buff=0.15)
        scenario.move_to(LEFT * 3.5 + UP * 1)
        
        self.play(FadeIn(scenario), run_time=3.2)
        
        # vs
        vs = Text("BUT", font_size=28, color=ELO_GOLD)
        vs.move_to(UP * 1)
        
        self.play(Write(vs), run_time=1.2)
        
        # Telemetry shows
        telemetry = VGroup(
            Text("Telemetry shows: P3 pace!", font_size=24, color=ELO_GREEN),
            Text("Lap times, sector speeds, tire deg", font_size=18, color=TEXT_GRAY)
        )
        telemetry.arrange(DOWN, buff=0.15)
        telemetry.move_to(RIGHT * 3.5 + UP * 1)
        
        self.play(FadeIn(telemetry), run_time=3.2)
        
        # Visual: Fake telemetry trace
        axes = Axes(
            x_range=[0, 60, 10],
            y_range=[90, 110, 5],
            x_length=8,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.shift(DOWN * 1.2)
        
        x_label = Text("Lap", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        
        y_label = Text("Lap Time (s)", font_size=14, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=3.2)
        
        # Lap time trace with outlier
        np.random.seed(42)
        times = 95 + np.random.normal(0, 0.5, 60)
        times[25:35] = 102  # Pit window disaster
        
        points = [axes.c2p(i, t) for i, t in enumerate(times)]
        trace = VMobject(color=ELO_BLUE)
        trace.set_points_smoothly(points)
        
        self.play(Create(trace), run_time=6)
        
        # Highlight bad strategy window
        bad_box = Rectangle(
            width=1.5, height=1.5,
            stroke_color=ELO_RED, stroke_width=2,
            fill_opacity=0
        )
        bad_box.move_to(axes.c2p(30, 102))
        bad_label = Text("Strategy failure", font_size=12, color=ELO_RED)
        bad_label.next_to(bad_box, UP, buff=0.1)
        
        self.play(Create(bad_box), FadeIn(bad_label), run_time=3.2)
        
        # Caption
        caption = Text(
            "Use telemetry to recover TRUE skill hidden by external factors",
            font_size=18,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.6)
        
        self.play(Write(caption), run_time=4)
        
        self.wait(22)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene11_2_KalmanFilter(Scene):
    """Scene 11.2: Kalman Filter State Estimation."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Kalman Filter", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        subtitle = Text("Cleaning noisy telemetry data", font_size=20, color=TEXT_GRAY)
        subtitle.next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=1.0)
        
        # State vector
        state = MathTex(
            r"x = \begin{bmatrix} s \\ v \\ a \end{bmatrix}",
            font_size=36
        )
        state.move_to(LEFT * 4 + UP * 0.5)
        
        state_labels = VGroup(
            Text("s = position", font_size=16, color=TEXT_GRAY),
            Text("v = velocity", font_size=16, color=TEXT_GRAY),
            Text("a = acceleration", font_size=16, color=TEXT_GRAY)
        )
        state_labels.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        state_labels.next_to(state, DOWN, buff=0.3)
        
        self.play(Write(state), FadeIn(state_labels), run_time=4)
        
        # Noisy vs Clean visualization
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 350, 100],
            x_length=6,
            y_length=3,
            tips=False,
            axis_config={"font_size": 12}
        )
        axes.move_to(RIGHT * 2 + DOWN * 0.5)
        
        self.play(Create(axes), run_time=2)
        
        # Noisy data (GPS)
        np.random.seed(42)
        t = np.linspace(0, 100, 50)
        true_speed = 300 - 5 * (t / 30)  # Braking
        noisy_speed = true_speed + np.random.normal(0, 15, 50)
        
        noisy_points = [axes.c2p(ti, si) for ti, si in zip(t, noisy_speed)]
        noisy_dots = VGroup(*[Dot(p, radius=0.03, color=ELO_RED) for p in noisy_points])
        noisy_label = Text("Raw GPS (noisy)", font_size=12, color=ELO_RED)
        noisy_label.move_to(axes.c2p(80, 320))
        
        self.play(FadeIn(noisy_dots), FadeIn(noisy_label), run_time=3.2)
        
        # Filtered (smooth)
        filtered_points = [axes.c2p(ti, si) for ti, si in zip(t, true_speed)]
        filtered_line = VMobject(color=ELO_GREEN)
        filtered_line.set_points_smoothly(filtered_points)
        filtered_label = Text("Kalman filtered", font_size=12, color=ELO_GREEN)
        filtered_label.move_to(axes.c2p(80, 230))
        
        self.play(Create(filtered_line), FadeIn(filtered_label), run_time=6)
        
        # Caption
        caption = Text(
            "Optimal fusion of noisy measurements -> Clean estimates",
            font_size=18,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.4)
        
        self.play(Write(caption), run_time=4)
        
        self.wait(22)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene11_3_KalmanEquations(Scene):
    """Scene 11.3: Kalman Update Equations."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Kalman Filter Equations", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Predict step
        predict_label = Text("Predict:", font_size=24, color=ELO_GOLD)
        predict_label.move_to(UP * 1.5 + LEFT * 4)
        
        predict = MathTex(
            r"\hat{x}_{k|k-1} = F\hat{x}_{k-1}",
            font_size=32
        )
        predict.next_to(predict_label, RIGHT, buff=0.3)
        
        self.play(Write(predict_label), Write(predict), run_time=4)
        
        # Update step
        update_label = Text("Update:", font_size=24, color=ELO_GREEN)
        update_label.move_to(UP * 0.5 + LEFT * 4)
        
        update = MathTex(
            r"\hat{x}_k = \hat{x}_{k|k-1} + K_k(z_k - H\hat{x}_{k|k-1})",
            font_size=28
        )
        update.next_to(update_label, RIGHT, buff=0.3)
        
        self.play(Write(update_label), Write(update), run_time=4)
        
        # Kalman gain
        gain_label = Text("Kalman Gain:", font_size=24, color=ELO_PURPLE)
        gain_label.move_to(DOWN * 0.5 + LEFT * 4)
        
        gain = MathTex(
            r"K_k = P_{k|k-1}H^T(HP_{k|k-1}H^T + R)^{-1}",
            font_size=26
        )
        gain.next_to(gain_label, RIGHT, buff=0.3)
        
        self.play(Write(gain_label), Write(gain), run_time=4)
        
        # Intuition
        intuition = VGroup(
            Text("Intuition:", font_size=20, color=ELO_GOLD),
            Text("• K high -> Trust measurement more", font_size=16, color=TEXT_GRAY),
            Text("• K low -> Trust prediction more", font_size=16, color=TEXT_GRAY)
        )
        intuition.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        intuition.move_to(DOWN * 2.2)
        
        self.play(FadeIn(intuition), run_time=4)
        
        self.wait(22)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene11_4_BrakingAggression(Scene):
    """Scene 11.4: Braking Aggression Index."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Braking Aggression Index", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Jerk definition
        jerk_def = MathTex(
            r"j(t) = \frac{da}{dt}",
            font_size=36
        )
        jerk_def.move_to(LEFT * 3 + UP * 1)
        
        jerk_label = Text("Jerk = rate of acceleration change", font_size=16, color=TEXT_GRAY)
        jerk_label.next_to(jerk_def, DOWN, buff=0.2)
        
        self.play(Write(jerk_def), FadeIn(jerk_label), run_time=4)
        
        # BAI formula
        bai = MathTex(
            r"BAI_i = \mathbb{E}[a_{brake}] - \lambda \cdot \text{Var}[j(t)]",
            font_size=32
        )
        bai.move_to(RIGHT * 2 + UP * 1)
        
        bai_box = SurroundingRectangle(bai, color=ELO_GOLD, buff=0.15)
        
        self.play(Write(bai), Create(bai_box), run_time=4)
        
        # Visual: Two brake profiles
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[-50, 0, 10],
            x_length=5,
            y_length=2.5,
            tips=False,
            axis_config={"font_size": 10}
        )
        axes.move_to(DOWN * 1.5)
        
        x_label = Text("Distance into braking zone (m)", font_size=12, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.15)
        
        y_label = Text("Decel (m/s^2)", font_size=12, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.1)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=3.2)
        
        # Smooth driver: gradual buildup
        smooth_x = np.linspace(0, 100, 50)
        smooth_y = -45 * (1 - np.exp(-smooth_x / 30))
        smooth_line = VMobject(color=ELO_BLUE)
        smooth_line.set_points_smoothly([axes.c2p(x, y) for x, y in zip(smooth_x, smooth_y)])
        smooth_label = Text("Smooth", font_size=12, color=ELO_BLUE)
        smooth_label.move_to(axes.c2p(85, -40))
        smooth_label_bg = BackgroundRectangle(smooth_label, fill_opacity=0.80, buff=0.05)

        # Aggressive driver: sharp spike
        aggro_x = np.linspace(0, 100, 50)
        aggro_y = -48 * np.tanh(aggro_x / 10 - 1) - 2
        aggro_y = np.clip(aggro_y, -50, 0)
        aggro_line = VMobject(color=ELO_RED)
        aggro_line.set_points_smoothly([axes.c2p(x, y) for x, y in zip(aggro_x, aggro_y)])
        aggro_label = Text("Aggressive", font_size=12, color=ELO_RED)
        aggro_label.move_to(axes.c2p(30, -25))
        aggro_label_bg = BackgroundRectangle(aggro_label, fill_opacity=0.80, buff=0.05)

        self.play(
            Create(smooth_line), FadeIn(smooth_label_bg), FadeIn(smooth_label),
            Create(aggro_line), FadeIn(aggro_label_bg), FadeIn(aggro_label),
            run_time=6
        )
        
        # Interpretation
        interpretation = Text(
            "High decel + Low jerk variance = Skill (not recklessness)",
            font_size=18,
            color=ELO_GREEN
        )
        interpretation.to_edge(DOWN, buff=0.3)
        
        self.play(Write(interpretation), run_time=4)
        
        self.wait(22)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene11_5_FrictionCircle(Scene):
    """Scene 11.5: The Friction Circle (g-g diagram)."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("The Friction Circle", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Formula — positioned on left to avoid overlapping with circle on right
        formula = MathTex(
            r"F_x^2 + F_y^2 \leq (\mu N)^2",
            font_size=36
        )
        formula.move_to(UP * 1.2 + LEFT * 3)

        formula_text = Text(
            "Total tire force limited by friction",
            font_size=18,
            color=TEXT_GRAY
        )
        formula_text.next_to(formula, DOWN, buff=0.2)

        self.play(Write(formula), FadeIn(formula_text), run_time=4)

        # g-g diagram — positioned on right side
        circle = Circle(radius=1.8, color=ELO_GOLD, stroke_width=2)
        circle.move_to(RIGHT * 2.5 + DOWN * 0.5)

        # Axes through center
        h_line = Line(LEFT * 2.2, RIGHT * 2.2, color=TEXT_GRAY)
        h_line.move_to(circle.get_center())
        v_line = Line(DOWN * 2.2, UP * 2.2, color=TEXT_GRAY)
        v_line.move_to(circle.get_center())

        # Labels
        brake_label = Text("Brake", font_size=14, color=TEXT_GRAY)
        brake_label.move_to(circle.get_center() + DOWN * 2.1)

        accel_label = Text("Accelerate", font_size=14, color=TEXT_GRAY)
        accel_label.move_to(circle.get_center() + UP * 2.1)

        left_label = Text("Left", font_size=14, color=TEXT_GRAY)
        left_label.move_to(circle.get_center() + LEFT * 2.3)

        right_label = Text("Right", font_size=14, color=TEXT_GRAY)
        right_label.move_to(circle.get_center() + RIGHT * 2.3)

        self.play(
            Create(circle),
            Create(h_line), Create(v_line),
            FadeIn(brake_label), FadeIn(accel_label),
            FadeIn(left_label), FadeIn(right_label),
            run_time=6
        )

        # Sample data points (driver pushing limits)
        np.random.seed(42)
        angles = np.random.uniform(0, 2 * np.pi, 30)
        radii = np.random.uniform(1.4, 1.75, 30)  # Close to limit

        points = VGroup()
        for a, r in zip(angles, radii):
            dot = Dot(
                circle.get_center() + r * np.array([np.cos(a), np.sin(a), 0]),
                radius=0.05,
                color=ELO_GREEN
            )
            points.add(dot)

        self.play(FadeIn(points), run_time=4)

        # Annotation
        skill_note = Text(
            "Elite drivers operate at edge of circle",
            font_size=18,
            color=ELO_GREEN
        )
        skill_note.to_edge(DOWN, buff=0.3)
        
        self.play(Write(skill_note), run_time=4)
        
        self.wait(22)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene11_3a_ExplainKalmanCycle(Scene):
    """Scene 11.3a: Kalman Filter in Plain English."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Kalman Filter in Plain English", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)

        # Two-box diagram: PREDICT → UPDATE
        predict_box = VGroup(
            Rectangle(width=3.5, height=2, fill_color=ELO_BLUE, fill_opacity=0.15, stroke_color=ELO_BLUE),
            Text("PREDICT", font_size=24, color=ELO_BLUE),
            MathTex(r"\hat{x} = F \cdot \hat{x}_{prev}", font_size=20, color=TEXT_WHITE),
            Text("Use physics to\nguess next state", font_size=12, color=TEXT_GRAY),
        )
        predict_box[1].move_to(predict_box[0].get_top() + DOWN * 0.3)
        predict_box[2].move_to(predict_box[0].get_center())
        predict_box[3].move_to(predict_box[0].get_bottom() + UP * 0.35)
        predict_box.move_to(LEFT * 3 + UP * 0.3)

        update_box = VGroup(
            Rectangle(width=3.5, height=2, fill_color=ELO_GREEN, fill_opacity=0.15, stroke_color=ELO_GREEN),
            Text("UPDATE", font_size=24, color=ELO_GREEN),
            MathTex(r"\hat{x} = \hat{x} + K(z - H\hat{x})", font_size=18, color=TEXT_WHITE),
            Text("Blend prediction\nwith measurement", font_size=12, color=TEXT_GRAY),
        )
        update_box[1].move_to(update_box[0].get_top() + DOWN * 0.3)
        update_box[2].move_to(update_box[0].get_center())
        update_box[3].move_to(update_box[0].get_bottom() + UP * 0.35)
        update_box.move_to(RIGHT * 3 + UP * 0.3)

        arrow = Arrow(predict_box[0].get_right(), update_box[0].get_left(), color=ELO_GOLD, buff=0.2)
        arrow_label = Text("Measure z_k", font_size=14, color=ELO_GOLD)
        arrow_label.next_to(arrow, UP, buff=0.1)

        self.play(FadeIn(predict_box), run_time=4)
        self.play(Create(arrow), FadeIn(arrow_label), run_time=2)
        self.play(FadeIn(update_box), run_time=4)

        # Feedback loop arrow — arcs over the top of both boxes
        loop_arrow = CurvedArrow(
            update_box[0].get_top() + LEFT * 0.5,
            predict_box[0].get_top() + RIGHT * 0.5,
            color=ELO_PURPLE, angle=-PI/5
        )
        loop_label = Text("Repeat", font_size=14, color=ELO_PURPLE)
        loop_label.next_to(loop_arrow, UP, buff=0.05)
        self.play(Create(loop_arrow), FadeIn(loop_label), run_time=2)

        self.wait(12)

        # Kalman Gain explanation
        self.play(*[FadeOut(m) for m in [predict_box, update_box, arrow, arrow_label,
                    loop_arrow, loop_label]], run_time=1.2)

        kg_title = Text("The Kalman Gain K", font_size=28, color=ELO_GOLD)
        kg_title.next_to(header, DOWN, buff=0.4)
        self.play(FadeIn(kg_title), run_time=1.2)

        kg_formula = MathTex(
            r"K_k = \frac{P_{k|k-1} H^T}{H P_{k|k-1} H^T + R}",
            font_size=32, color=TEXT_WHITE
        )
        kg_formula.move_to(UP * 0.2)
        self.play(Write(kg_formula), run_time=4)

        kg_explain = VGroup(
            Text("K ~ 1 (high): Trust the SENSOR -> measurement dominates", font_size=16, color=ELO_GREEN),
            Text("K ~ 0 (low): Trust the PHYSICS -> prediction dominates", font_size=16, color=ELO_BLUE),
            Text("K balances model confidence vs measurement noise", font_size=16, color=TEXT_GRAY),
        )
        kg_explain.arrange(DOWN, buff=0.15)
        kg_explain.move_to(DOWN * 1)
        self.play(FadeIn(kg_explain), run_time=4)

        # F1 takeaway
        takeaway = Text(
            "In F1: Kalman filters smooth noisy GPS/telemetry into clean performance data",
            font_size=18, color=ELO_GOLD
        )
        takeaway.to_edge(DOWN, buff=0.3)
        self.play(Write(takeaway), run_time=4)

        self.wait(22)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene11_5a_ExplainFrictionCircle(Scene):
    """Scene 11.5a: The Physics of Grip — Friction Circle."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Physics of Grip", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)

        # Formula
        formula = MathTex(
            r"F_x^2 + F_y^2 \leq (\mu N)^2",
            font_size=44
        )
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=6)

        # Component explanations
        parts = VGroup(
            VGroup(
                MathTex(r"F_x", font_size=24, color=ELO_BLUE),
                Text("= Longitudinal (braking/accel)", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                MathTex(r"F_y", font_size=24, color=ELO_GREEN),
                Text("= Lateral (cornering)", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                MathTex(r"\mu N", font_size=24, color=ELO_RED),
                Text("= Maximum total grip", font_size=14, color=TEXT_GRAY)
            ),
        )
        for p in parts:
            p.arrange(RIGHT, buff=0.2)
        parts.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        parts.move_to(LEFT * 3.5 + DOWN * 0.3)
        self.play(FadeIn(parts), run_time=3.2)

        # Draw the friction circle
        circle_center = RIGHT * 2.5 + DOWN * 0.5
        circle = Circle(radius=1.5, color=ELO_RED, stroke_width=2)
        circle.move_to(circle_center)

        x_ax = Arrow(circle_center + LEFT * 2, circle_center + RIGHT * 2, color=TEXT_GRAY, buff=0, stroke_width=1)
        y_ax = Arrow(circle_center + DOWN * 2, circle_center + UP * 2, color=TEXT_GRAY, buff=0, stroke_width=1)

        fx_label = MathTex(r"F_x", font_size=14, color=ELO_BLUE)
        fx_label.next_to(x_ax, RIGHT, buff=0.1)
        fy_label = MathTex(r"F_y", font_size=14, color=ELO_GREEN)
        fy_label.next_to(y_ax, UP, buff=0.1)

        self.play(Create(x_ax), Create(y_ax), FadeIn(fx_label), FadeIn(fy_label), run_time=2)
        self.play(Create(circle), run_time=4)

        # Force vector rotating around the edge
        force_vec = Arrow(
            circle_center, circle_center + RIGHT * 1.5,
            color=ELO_GOLD, buff=0, stroke_width=3
        )
        force_label = Text("F", font_size=16, color=ELO_GOLD)
        force_label.next_to(force_vec.get_end(), UR, buff=0.05)

        self.play(Create(force_vec), FadeIn(force_label), run_time=2)

        # Animate rotation
        angle_tracker = ValueTracker(0)

        def update_vec(mob):
            a = angle_tracker.get_value()
            end = circle_center + 1.5 * np.array([np.cos(a), np.sin(a), 0])
            mob.become(Arrow(circle_center, end, color=ELO_GOLD, buff=0, stroke_width=3))

        def update_label(mob):
            mob.next_to(force_vec.get_end(), UR, buff=0.05)

        force_vec.add_updater(update_vec)
        force_label.add_updater(update_label)

        self.play(angle_tracker.animate.set_value(TAU), run_time=12, rate_func=linear)

        force_vec.remove_updater(update_vec)
        force_label.remove_updater(update_label)

        # Key insight
        insight = VGroup(
            Text("All braking (F_x = uN) -> F_y = 0 -> can't turn!", font_size=16, color=ELO_RED),
            Text("All cornering (F_y = uN) -> F_x = 0 -> can't brake!", font_size=16, color=ELO_BLUE),
            Text("Elite drivers operate at the EDGE of the circle", font_size=16, color=ELO_GREEN),
        )
        insight.arrange(DOWN, buff=0.1)
        insight.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(insight), run_time=4)

        self.wait(22)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)
