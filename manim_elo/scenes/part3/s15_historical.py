# Section 15: Visual Analysis of Historical Eras
# 5 Scenes covering data visualization

from manim import *
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *
import numpy as np


class Scene15_1_RidgePlot(Scene):
    """Scene 15.1: The Ridge Plot (Joy Plot)."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Ridge Plot: Skill Distributions", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Create multiple overlapping distributions
        drivers = ["Verstappen", "Hamilton", "Leclerc", "Norris", "Rookie"]
        means = [2600, 2450, 2350, 2300, 2100]
        stds = [30, 40, 50, 55, 100]
        colors = [ELO_BLUE, "#00D2BE", ELO_RED, ELO_GOLD, TEXT_GRAY]
        
        distributions = VGroup()
        for i, (name, mean, std, color) in enumerate(zip(drivers, means, stds, colors)):
            # Create x values for this distribution
            x_vals = np.linspace(1900, 2800, 100)
            y_vals = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_vals - mean) / std) ** 2)
            
            # Scale and position
            y_vals = y_vals / y_vals.max() * 0.45  # Normalize each curve to peak at 0.45 units
            
            # Create curve
            points = [
                np.array([(x - 2350) / 100, y - 1.5 + i * 0.6, 0])
                for x, y in zip(x_vals, y_vals)
            ]
            
            curve = VMobject(color=color, fill_opacity=0.4, stroke_width=2)
            curve.set_points_smoothly(points)
            curve.set_fill(color, opacity=0.4)
            
            # Label with background box to prevent overlap with curves
            label = Text(name, font_size=14, color=color)
            label.move_to([-5.8, -1.5 + i * 0.6, 0])
            label_bg = SurroundingRectangle(
                label, fill_color=DARK_BG, fill_opacity=0.85,
                stroke_width=0, buff=0.06
            )
            
            distributions.add(VGroup(curve, label_bg, label))
        
        self.play(FadeIn(distributions), run_time=8)
        
        # X-axis
        x_axis = Line(LEFT * 4.5, RIGHT * 4.5, color=TEXT_GRAY)
        x_axis.shift(DOWN * 2.2)
        
        x_labels = VGroup()
        for val in [2000, 2200, 2400, 2600, 2800]:
            label = Text(str(val), font_size=12, color=TEXT_GRAY)
            label.move_to([(val - 2350) / 100, -2.5, 0])
            x_labels.add(label)
        
        axis_label = Text("Skill Rating", font_size=16, color=TEXT_GRAY)
        axis_label.next_to(x_axis, DOWN, buff=0.4)
        
        self.play(
            Create(x_axis),
            FadeIn(x_labels),
            FadeIn(axis_label),
            run_time=3.2
        )
        
        # Caption
        caption = Text(
            "Narrow curve = High certainty | Wide curve = Uncertain",
            font_size=20,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.2)
        
        self.play(Write(caption), run_time=4)
        
        self.wait(20)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene15_2_OverlapProbability(Scene):
    """Scene 15.2: Overlap Probability - Who is really better?"""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Who Is Really Better?", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Two overlapping distributions
        axes = Axes(
            x_range=[2000, 2600, 100],
            y_range=[0, 0.02, 0.005],
            x_length=8,
            y_length=3.5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.shift(DOWN * 0.5)
        
        self.play(Create(axes), run_time=2)
        
        # Driver A
        def pdf_a(x):
            return (1 / (50 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 2400) / 50) ** 2)
        
        curve_a = axes.plot(pdf_a, x_range=[2000, 2600], color=ELO_BLUE)
        area_a = axes.get_area(curve_a, x_range=[2000, 2600], color=ELO_BLUE, opacity=0.3)
        label_a = Text("Driver A: 2400 +/- 50", font_size=16, color=ELO_BLUE)
        label_a.move_to(axes.c2p(2500, 0.018))
        
        # Driver B
        def pdf_b(x):
            return (1 / (60 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 2350) / 60) ** 2)
        
        curve_b = axes.plot(pdf_b, x_range=[2000, 2600], color=ELO_RED)
        area_b = axes.get_area(curve_b, x_range=[2000, 2600], color=ELO_RED, opacity=0.3)
        label_b = Text("Driver B: 2350 +/- 60", font_size=16, color=ELO_RED)
        label_b.move_to(axes.c2p(2200, 0.015))
        
        self.play(
            Create(curve_a), FadeIn(area_a), FadeIn(label_a),
            run_time=4
        )
        self.play(
            Create(curve_b), FadeIn(area_b), FadeIn(label_b),
            run_time=4
        )
        
        # Overlay region
        question = Text(
            "P(B is actually better than A) = ?",
            font_size=22,
            color=ELO_GOLD
        )
        question.move_to(DOWN * 2.8)
        
        self.play(Write(question), run_time=4)
        
        # Answer
        answer = Text(
            "~20% — The uncertainty matters!",
            font_size=20,
            color=ELO_GREEN
        )
        answer.to_edge(DOWN, buff=0.3)
        
        self.play(Write(answer), run_time=4)
        
        self.wait(20)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene15_3_HHITimeline(MovingCameraScene):
    """Scene 15.3: HHI Competitive Balance Timeline.

    Smaller axes + camera zoom-ins highlight each dominant era without
    the graph crowding the header or caption zones.
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Competitive Balance Over Time", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)

        # Subtitle
        subtitle = Text(
            "Herfindahl-Hirschman Index (HHI) of race wins",
            font_size=20,
            color=TEXT_GRAY
        )
        subtitle.next_to(header, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=1.0)

        # Smaller axes — zoom-ins carry the era detail
        axes = Axes(
            x_range=[1950, 2025, 10],
            y_range=[0, 0.8, 0.2],
            x_length=8,
            y_length=2.8,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 10}
        )
        axes.shift(DOWN * 0.6)

        x_label = Text("Year", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.15)

        y_label = Text("HHI (Concentration)", font_size=12, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.15)
        y_label.rotate(90 * DEGREES)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=3.2)

        # Simulated HHI data — seeded for reproducibility
        np.random.seed(7)
        years = list(range(1950, 2024))
        hhi_values = []
        for y in years:
            base = 0.25
            if 1988 <= y <= 1991:   # McLaren dominance
                base = 0.60
            elif 2000 <= y <= 2004: # Ferrari dominance
                base = 0.65
            elif 2014 <= y <= 2016: # Mercedes dominance
                base = 0.70
            elif 2022 <= y <= 2023: # Red Bull dominance
                base = 0.75
            elif y == 2021:         # Closest title fight in years
                base = 0.15
            hhi_values.append(np.clip(base + np.random.normal(0, 0.04), 0, 0.78))

        hhi_trace = VMobject(color=ELO_BLUE, stroke_width=2.5)
        hhi_trace.set_points_smoothly([
            axes.c2p(y, h) for y, h in zip(years, hhi_values)
        ])

        self.play(Create(hhi_trace), run_time=8)
        self.wait(1.2)

        # Era zoom data: (zoom_year, hhi_peak, label_text, label_color, label_direction)
        eras = [
            (1989, 0.62, "McLaren\n1988–91", ELO_GOLD, UP),
            (2002, 0.67, "Ferrari\n2000–04",  ELO_RED,  UP),
            (2015, 0.72, "Mercedes\n2014–16", "#00D2BE", UP),
            (2021, 0.12, "2021\nmax competition!", ELO_GREEN, DOWN),
        ]

        era_labels = []   # keep references for final FadeOut

        for year, hhi, text, col, direction in eras:
            zoom_center = axes.c2p(year, hhi)

            # Zoom into this era
            self.play(
                self.camera.frame.animate.scale(0.50).move_to(zoom_center),
                run_time=3
            )

            # Annotation with BackgroundRectangle — shown while zoomed
            lbl = Text(text, font_size=12, color=col)
            lbl.move_to(axes.c2p(year, hhi) + direction * 0.18)
            lbl_bg = BackgroundRectangle(lbl, fill_opacity=0.80, buff=0.06)
            dot = Dot(axes.c2p(year, hhi), color=col, radius=0.07)

            self.play(FadeIn(dot), FadeIn(lbl_bg), FadeIn(lbl), run_time=2)
            self.wait(2.8)

            # Zoom back to full view
            self.play(
                self.camera.frame.animate.scale(1 / 0.50).move_to(ORIGIN),
                run_time=2.6
            )

            era_labels.extend([dot, lbl_bg, lbl])

        # Caption — visible at full scale
        caption = Text(
            "Dominant eras create spikes; rule changes restore competition",
            font_size=20,
            color=TEXT_LIGHT
        )
        caption.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(caption, shift=UP * 0.3), run_time=4)
        self.wait(20)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene15_4_EraAdjusted(Scene):
    """Scene 15.4: Era-Adjusted Trajectories."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Era-Adjusted Career Trajectories", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Create axes
        axes = Axes(
            x_range=[0, 20, 5],
            y_range=[2000, 2800, 200],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.shift(DOWN * 0.3)
        
        x_label = Text("Career Season", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        
        y_label = Text("Era-Adjusted Rating", font_size=12, color=TEXT_GRAY)
        y_label.next_to(axes, LEFT, buff=0.25)
        y_label.rotate(90 * DEGREES)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=3.2)
        
        # Fangio (wide uncertainty)
        fangio_mean = [2200, 2350, 2450, 2550, 2600, 2650, 2680, 2650]
        fangio_std = 100  # Wide band
        
        fangio_line = VMobject(color=ELO_GOLD)
        fangio_line.set_points_smoothly([axes.c2p(i, v) for i, v in enumerate(fangio_mean)])
        
        # Uncertainty band
        fangio_upper = VMobject(color=ELO_GOLD, stroke_opacity=0.3)
        fangio_upper.set_points_smoothly([axes.c2p(i, v + fangio_std) for i, v in enumerate(fangio_mean)])
        fangio_lower = VMobject(color=ELO_GOLD, stroke_opacity=0.3)
        fangio_lower.set_points_smoothly([axes.c2p(i, v - fangio_std) for i, v in enumerate(fangio_mean)])
        
        fangio_label = Text("Fangio (1950s)", font_size=14, color=ELO_GOLD)
        fangio_label.move_to(axes.c2p(6, 2800))
        
        self.play(
            Create(fangio_line),
            Create(fangio_upper), Create(fangio_lower),
            FadeIn(fangio_label),
            run_time=4
        )
        
        # Hamilton (narrow uncertainty)
        hamilton_mean = [2300 + i * 25 for i in range(18)]
        hamilton_std = 30  # Narrow band
        
        hamilton_line = VMobject(color="#00D2BE")
        hamilton_line.set_points_smoothly([axes.c2p(i, v) for i, v in enumerate(hamilton_mean)])
        
        hamilton_upper = VMobject(color="#00D2BE", stroke_opacity=0.3)
        hamilton_upper.set_points_smoothly([axes.c2p(i, v + hamilton_std) for i, v in enumerate(hamilton_mean)])
        hamilton_lower = VMobject(color="#00D2BE", stroke_opacity=0.3)
        hamilton_lower.set_points_smoothly([axes.c2p(i, v - hamilton_std) for i, v in enumerate(hamilton_mean)])
        
        hamilton_label = Text("Hamilton (2007-)", font_size=14, color="#00D2BE")
        hamilton_label.move_to(axes.c2p(15, 2650))
        
        self.play(
            Create(hamilton_line),
            Create(hamilton_upper), Create(hamilton_lower),
            FadeIn(hamilton_label),
            run_time=4
        )
        
        # Caption
        caption = Text(
            "Width = Uncertainty | More races -> More certainty",
            font_size=20,
            color=TEXT_LIGHT
        )
        caption.to_edge(DOWN, buff=0.3)
        
        self.play(Write(caption), run_time=4)
        
        self.wait(20)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)


class Scene15_5_PeakComparison(Scene):
    """Scene 15.5: Peak Rating Comparison."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("GOAT Comparison: Peak Ratings", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1.5)
        
        # Bar chart with error bars
        drivers = ["Fangio", "Senna", "Schumacher", "Hamilton", "Verstappen"]
        peaks = [2680, 2720, 2750, 2770, 2720]
        errors = [100, 60, 45, 30, 35]
        colors = [ELO_GOLD] * 5
        
        bars = VGroup()
        x_positions = [-4, -2, 0, 2, 4]
        
        for name, peak, err, x in zip(drivers, peaks, errors, x_positions):
            # Bar height scaled
            height = (peak - 2500) / 100
            bar = Rectangle(
                width=1,
                height=height,
                fill_color=ELO_BLUE,
                fill_opacity=0.7,
                stroke_color=WHITE
            )
            bar.move_to([x, height/2 - 1.5, 0])
            
            # Error bar
            error_line = Line(
                [x, height - 1.5 - err/100, 0],
                [x, height - 1.5 + err/100, 0],
                color=ELO_RED,
                stroke_width=3
            )
            top_cap = Line([x-0.15, height - 1.5 + err/100, 0], [x+0.15, height - 1.5 + err/100, 0], color=ELO_RED)
            bot_cap = Line([x-0.15, height - 1.5 - err/100, 0], [x+0.15, height - 1.5 - err/100, 0], color=ELO_RED)
            
            # Label
            label = Text(name, font_size=16, color=TEXT_GRAY)
            label.move_to([x, -2.2, 0])
            
            # Peak value
            value = Text(str(peak), font_size=12, color=ELO_GREEN)
            value.next_to(bar, UP, buff=0.1)
            
            bars.add(VGroup(bar, error_line, top_cap, bot_cap, label, value))
        
        self.play(FadeIn(bars), run_time=6)
        
        # Insight
        insight = Text(
            "Peaks similar, but confidence varies based on data availability",
            font_size=20,
            color=ELO_GOLD
        )
        insight.to_edge(DOWN, buff=0.4)
        
        self.play(Write(insight), run_time=4)
        
        self.wait(20)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)
