# Section 1: Introduction - The Quantitative Architecture of Skill
# 3 Scenes: Title & Hook, Latent Variable Problem, Evolution Timeline

from manim import *
import sys
sys.path.append('..')
from utils.colors import *


class Scene1_1_TitleHook(Scene):
    """Scene 1.1: Title & Hook - The central question of ranking."""

    def construct(self):
        self.camera.background_color = DARK_BG

        # Main title
        title = Text(
            "The Mathematics of Ranking",
            font_size=60,
            color=ELO_BLUE,
            weight=BOLD
        )
        title.move_to(UP * 1.5)

        # Three domain labels
        domains = VGroup(
            Text("Chess", font_size=32, color=ELO_BLUE),
            Text("Formula 1", font_size=32, color=ELO_GOLD),
            Text("Esports", font_size=32, color=ELO_GREEN),
        )
        domains.arrange(RIGHT, buff=2.0)
        domains.move_to(DOWN * 0.2)

        # Dots below each domain
        dots = VGroup(*[
            Dot(radius=0.1, color=d.get_color()).next_to(d, DOWN, buff=0.3)
            for d in domains
        ])

        # Animate title
        self.play(Write(title, run_time=1.5, rate_func=smooth))
        self.wait(0.3)

        for domain, dot in zip(domains, dots):
            self.play(
                FadeIn(domain, shift=UP * 0.2),
                FadeIn(dot),
                run_time=0.5
            )

        self.wait(0.8)

        # The central question
        question_box = Rectangle(
            width=8, height=1.1,
            fill_color=DARKER_BG, fill_opacity=0.8,
            stroke_color=ELO_GOLD, stroke_width=2
        )
        question_box.move_to(DOWN * 2.2)

        question = Text(
            "How do we objectively compare skill?",
            font_size=36,
            color=ELO_GOLD
        )
        question.move_to(question_box)

        self.play(
            FadeIn(question_box),
            Write(question, run_time=1.2),
        )
        self.wait(2)

        self.play(
            *[FadeOut(mob, shift=UP * 0.3) for mob in self.mobjects],
            run_time=0.8
        )


class Scene1_2_LatentVariable(Scene):
    """Scene 1.2: The Latent Variable Problem - Skill is hidden."""

    def construct(self):
        self.camera.background_color = DARK_BG

        # Header
        header = Text("The Core Problem", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        # Skill orb in center with glow
        glow = Circle(radius=1.4, color=ELO_GOLD, fill_opacity=0.15, stroke_width=0)
        skill_orb = Circle(radius=0.9, color=ELO_GOLD, fill_opacity=0.7, stroke_width=2)
        skill_orb.set_fill(ELO_GOLD, opacity=0.6)
        skill_label = Text("True Skill", font_size=22, color=DARKER_BG, weight=BOLD)
        skill_group = VGroup(glow, skill_orb)
        skill_group.move_to(ORIGIN + LEFT * 0.5)
        skill_label.move_to(skill_orb)

        self.play(
            FadeIn(glow, scale=0.5),
            GrowFromCenter(skill_orb),
            FadeIn(skill_label),
            run_time=1.2
        )

        # "skill is hidden" label
        hidden_label = Text("Hidden", font_size=28, color=TEXT_GRAY)
        hidden_label.move_to(skill_orb.get_center() + DOWN * 1.5)
        hidden_arrow = Arrow(
            hidden_label.get_top() + UP * 0.1,
            skill_orb.get_bottom() + DOWN * 0.1,
            color=TEXT_GRAY, buff=0.1, stroke_width=2
        )

        self.play(FadeIn(hidden_label), Create(hidden_arrow), run_time=0.8)

        # Performance observations orbiting
        obs_data = [
            ("Win", ELO_GREEN, 80),
            ("Loss", ELO_RED, 140),
            ("Win", ELO_GREEN, 200),
            ("Draw", TEXT_GRAY, 270),
            ("Win", ELO_GREEN, 330),
            ("Loss", ELO_RED, 20),
        ]

        observations = VGroup()
        center = skill_orb.get_center()
        radius = 2.4

        for label, color, angle_deg in obs_data:
            angle_rad = angle_deg * DEGREES
            pos = center + radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            dot = Dot(pos, color=color, radius=0.12)
            text = Text(label, font_size=16, color=color)
            text.next_to(dot, UP * np.cos(angle_rad) + RIGHT * np.sin(angle_rad), buff=0.12)
            line = DashedLine(center, pos, stroke_width=1, color=TEXT_GRAY, dash_length=0.1)
            observations.add(VGroup(dot, text, line))

        self.play(
            LaggedStart(*[FadeIn(obs, scale=0.5) for obs in observations], lag_ratio=0.1),
            run_time=1.5
        )

        # Caption
        caption = Text(
            "Skill cannot be measured directly - only inferred from results",
            font_size=24,
            color=TEXT_LIGHT
        )
        caption.to_edge(DOWN, buff=0.7)

        self.play(FadeIn(caption, shift=UP * 0.3), run_time=1)
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class Scene1_3_EvolutionTimeline(Scene):
    """Scene 1.3: The Evolution Timeline - 70 years of progress."""

    def construct(self):
        self.camera.background_color = DARK_BG

        # Header
        header = Text("The Evolution of Ranking", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.7)
        self.play(Write(header), run_time=1)

        # Timeline
        timeline = Line(LEFT * 5.5, RIGHT * 5.5, color=TEXT_GRAY, stroke_width=2)
        timeline.shift(DOWN * 0.2)

        self.play(Create(timeline), run_time=0.8)

        # Era data
        eras = [
            {"year": "1950s", "name": "Harkness", "desc": "Linear Arithmetic",
             "color": ELO_RED, "x": -4.0},
            {"year": "1960s", "name": "Elo", "desc": "Probability Theory",
             "color": ELO_BLUE, "x": 0.0},
            {"year": "2000s", "name": "TrueSkill", "desc": "Bayesian Inference",
             "color": ELO_GREEN, "x": 4.0}
        ]

        for i, era in enumerate(eras):
            dot = Dot(point=[era["x"], -0.2, 0], radius=0.16, color=era["color"])

            year_t = Text(era["year"], font_size=18, color=TEXT_GRAY)
            year_t.next_to(dot, DOWN, buff=0.35)

            name_t = Text(era["name"], font_size=30, color=era["color"], weight=BOLD)
            name_t.next_to(dot, UP, buff=0.5)

            desc_t = Text(era["desc"], font_size=17, color=TEXT_GRAY)
            desc_t.next_to(name_t, UP, buff=0.15)

            self.play(
                GrowFromCenter(dot),
                FadeIn(year_t, shift=DOWN * 0.2),
                FadeIn(name_t, shift=UP * 0.2),
                FadeIn(desc_t, shift=UP * 0.2),
                run_time=0.9
            )
            self.wait(0.4)

        # Downward labels for limitations
        limitations = [
            ("Fails at extremes", -4.0),
            ("Fails for F1", 0.0),
            ("Handles uncertainty", 4.0),
        ]

        for text, x in limitations:
            lim = Text(text, font_size=14, color=TEXT_GRAY, slant=ITALIC)
            lim.move_to([x, -1.6, 0])
            self.play(FadeIn(lim, shift=DOWN * 0.2), run_time=0.4)

        # Innovation arrows between eras
        for x_start, x_end, label in [(-3.5, -0.5, "First standardization"),
                                       (0.5, 3.5, "Embrace uncertainty")]:
            arrow = Arrow(
                [x_start, -0.2, 0], [x_end, -0.2, 0],
                color=TEXT_GRAY, stroke_width=2, buff=0.1,
                max_tip_length_to_length_ratio=0.08
            )
            ann = Text(label, font_size=13, color=TEXT_GRAY)
            ann.move_to([(x_start + x_end) / 2, 0.25, 0])
            self.play(Create(arrow), FadeIn(ann), run_time=0.6)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
