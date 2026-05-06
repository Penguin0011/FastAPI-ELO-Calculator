# Scene 0: The GOAT Question - YouTube Introduction
# 4 Scenes: Basketball Debate, Soccer Debate, Cross-Sport Problem, The Question

from manim import *
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from utils.colors import *
import numpy as np

_ASSETS = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'images')
JORDAN_IMG  = os.path.join(_ASSETS, 'jordan.jpg')
LEBRON_IMG  = os.path.join(_ASSETS, 'lebron.jpg')
MESSI_IMG   = os.path.join(_ASSETS, 'messi.jpg')
RONALDO_IMG = os.path.join(_ASSETS, 'ronaldo.jpg')


class Scene0_1_BasketballDebate(MovingCameraScene):
    """Scene 0.1: LeBron James vs Michael Jordan - The Greatest Debate."""

    def construct(self):
        self.camera.background_color = DARK_BG

        # Opening hook
        hook = Text("The Greatest of All Time", font_size=52, color=ELO_GOLD, weight=BOLD)
        hook.to_edge(UP, buff=0.6)
        self.play(Write(hook, run_time=6))
        self.wait(1.6)

        # Divider
        divider = Line(UP * 2.8, DOWN * 3.2, color=TEXT_GRAY, stroke_width=2)
        self.play(Create(divider), run_time=2)

        # ---- LEFT: Michael Jordan ----
        mj_name = Text("Michael Jordan", font_size=36, color=ELO_RED, weight=BOLD)
        mj_name.move_to(LEFT * 3.2 + UP * 1.8)

        mj_img = ImageMobject(JORDAN_IMG)
        mj_img.set_height(2.0)
        mj_img.move_to(LEFT * 3.2 + UP * 0.6)
        mj_border = Rectangle(
            width=mj_img.width + 0.14, height=mj_img.height + 0.14,
            stroke_color=ELO_RED, stroke_width=3, fill_opacity=0
        )
        mj_border.move_to(mj_img)

        mj_stats = VGroup(
            Text("6x NBA Champion", font_size=18, color=TEXT_LIGHT),
            Text("6x Finals MVP", font_size=18, color=TEXT_LIGHT),
            Text("5x Regular Season MVP", font_size=18, color=TEXT_LIGHT),
            Text("30.1 career PPG", font_size=18, color=TEXT_LIGHT),
            Text("Never lost in the Finals", font_size=18, color=ELO_GOLD),
        )
        mj_stats.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        mj_stats.move_to(LEFT * 3.2 + DOWN * 1.5)

        # ---- RIGHT: LeBron James ----
        lbj_name = Text("LeBron James", font_size=36, color=ELO_BLUE, weight=BOLD)
        lbj_name.move_to(RIGHT * 3.2 + UP * 1.8)

        lbj_img = ImageMobject(LEBRON_IMG)
        lbj_img.set_height(2.0)
        lbj_img.move_to(RIGHT * 3.2 + UP * 0.6)
        lbj_border = Rectangle(
            width=lbj_img.width + 0.14, height=lbj_img.height + 0.14,
            stroke_color=ELO_BLUE, stroke_width=3, fill_opacity=0
        )
        lbj_border.move_to(lbj_img)

        lbj_stats = VGroup(
            Text("4x NBA Champion", font_size=18, color=TEXT_LIGHT),
            Text("4x Finals MVP", font_size=18, color=TEXT_LIGHT),
            Text("4x Regular Season MVP", font_size=18, color=TEXT_LIGHT),
            Text("27.2 career PPG", font_size=18, color=TEXT_LIGHT),
            Text("All-time scoring leader", font_size=18, color=ELO_GOLD),
        )
        lbj_stats.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        lbj_stats.move_to(RIGHT * 3.2 + DOWN * 1.5)

        # VS label
        vs_text = Text("VS", font_size=42, color=ELO_GOLD, weight=BOLD)
        vs_text.move_to(ORIGIN + UP * 0.6)

        self.play(
            FadeIn(mj_name, shift=RIGHT * 0.3),
            FadeIn(lbj_name, shift=LEFT * 0.3),
            run_time=3.2
        )
        self.play(
            FadeIn(mj_img), FadeIn(mj_border),
            FadeIn(lbj_img), FadeIn(lbj_border),
            Write(vs_text),
            run_time=3.2
        )
        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT * 0.15) for s in mj_stats], lag_ratio=0.12),
            LaggedStart(*[FadeIn(s, shift=LEFT * 0.15) for s in lbj_stats], lag_ratio=0.12),
            run_time=5.6
        )
        self.wait(2.4)

        # ---- ZOOM into a key stat clash ----
        zoom_group = VGroup(
            mj_stats[0].copy(),  # "6x NBA Champion"
            lbj_stats[0].copy(),  # "4x NBA Champion"
        )
        zoom_bg = Rectangle(
            width=8.5, height=1.5,
            fill_color=DARKER_BG, fill_opacity=0.92,
            stroke_color=ELO_GOLD, stroke_width=2
        )
        zoom_bg.move_to(DOWN * 2.8)

        zoom_mj = Text("MJ: 6 rings", font_size=26, color=ELO_RED, weight=BOLD)
        zoom_mj.move_to(DOWN * 2.65 + LEFT * 2.2)
        zoom_vs = Text("vs", font_size=22, color=TEXT_GRAY)
        zoom_vs.move_to(DOWN * 2.65)
        zoom_lbj = Text("LeBron: 4 rings", font_size=26, color=ELO_BLUE, weight=BOLD)
        zoom_lbj.move_to(DOWN * 2.65 + RIGHT * 2.4)
        zoom_note = Text("But 6 attempts vs 10 attempts...", font_size=18, color=ELO_GOLD, slant=ITALIC)
        zoom_note.move_to(DOWN * 3.25)

        self.play(FadeIn(zoom_bg), run_time=1.6)
        self.play(
            Write(zoom_mj), Write(zoom_vs), Write(zoom_lbj),
            run_time=3.2
        )
        # Camera zoom into the debate area
        self.play(
            self.camera.frame.animate.scale(0.72).move_to(DOWN * 2.75),
            run_time=4
        )
        self.play(FadeIn(zoom_note, shift=UP * 0.2), run_time=3.2)
        self.wait(2)

        # Zoom back out
        self.play(
            self.camera.frame.animate.scale(1 / 0.72).move_to(ORIGIN),
            run_time=3.2
        )

        # Conflict: no clear answer
        conflict = Text(
            "Stats favor Jordan — but context makes it complicated",
            font_size=20, color=TEXT_GRAY, slant=ITALIC
        )
        conflict.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(conflict, shift=UP * 0.2), run_time=3.2)
        self.wait(2.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene0_2_SoccerDebate(MovingCameraScene):
    """Scene 0.2: Messi vs Ronaldo - The Other Greatest Debate."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Another Sport, Same Question", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)

        divider = Line(UP * 2.5, DOWN * 3.2, color=TEXT_GRAY, stroke_width=2)
        self.play(Create(divider), run_time=2)

        # ---- LEFT: Messi ----
        messi_name = Text("Lionel Messi", font_size=36, color=ELO_BLUE, weight=BOLD)
        messi_name.move_to(LEFT * 3.2 + UP * 1.8)

        messi_img = ImageMobject(MESSI_IMG)
        messi_img.set_height(2.0)
        messi_img.move_to(LEFT * 3.2 + UP * 0.6)
        messi_border = Rectangle(
            width=messi_img.width + 0.14, height=messi_img.height + 0.14,
            stroke_color=ELO_BLUE, stroke_width=3, fill_opacity=0
        )
        messi_border.move_to(messi_img)

        messi_stats = VGroup(
            Text("8x Ballon d'Or", font_size=18, color=TEXT_LIGHT),
            Text("4x UCL titles", font_size=18, color=TEXT_LIGHT),
            Text("2022 World Cup winner", font_size=18, color=ELO_GOLD),
            Text("91 goals in a calendar year", font_size=18, color=TEXT_LIGHT),
            Text("Most goals for one club (672)", font_size=18, color=TEXT_LIGHT),
        )
        messi_stats.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        messi_stats.move_to(LEFT * 3.2 + DOWN * 1.4)

        # ---- RIGHT: Ronaldo ----
        ronaldo_name = Text("Cristiano Ronaldo", font_size=34, color=ELO_RED, weight=BOLD)
        ronaldo_name.move_to(RIGHT * 3.2 + UP * 1.8)

        ronaldo_img = ImageMobject(RONALDO_IMG)
        ronaldo_img.set_height(2.0)
        ronaldo_img.move_to(RIGHT * 3.2 + UP * 0.6)
        ronaldo_border = Rectangle(
            width=ronaldo_img.width + 0.14, height=ronaldo_img.height + 0.14,
            stroke_color=ELO_RED, stroke_width=3, fill_opacity=0
        )
        ronaldo_border.move_to(ronaldo_img)

        ronaldo_stats = VGroup(
            Text("5x Ballon d'Or", font_size=18, color=TEXT_LIGHT),
            Text("5x UCL titles", font_size=18, color=TEXT_LIGHT),
            Text("Most international goals (130+)", font_size=18, color=ELO_GOLD),
            Text("Won titles in 4 leagues", font_size=18, color=TEXT_LIGHT),
            Text("906 career goals (all-time record)", font_size=18, color=TEXT_LIGHT),
        )
        ronaldo_stats.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        ronaldo_stats.move_to(RIGHT * 3.2 + DOWN * 1.4)

        vs_text = Text("VS", font_size=42, color=ELO_GOLD, weight=BOLD)
        vs_text.move_to(ORIGIN + UP * 0.6)

        self.play(
            FadeIn(messi_name, shift=RIGHT * 0.3),
            FadeIn(ronaldo_name, shift=LEFT * 0.3),
            run_time=3.2
        )
        self.play(
            FadeIn(messi_img), FadeIn(messi_border),
            FadeIn(ronaldo_img), FadeIn(ronaldo_border),
            Write(vs_text),
            run_time=3.2
        )
        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT * 0.15) for s in messi_stats], lag_ratio=0.12),
            LaggedStart(*[FadeIn(s, shift=LEFT * 0.15) for s in ronaldo_stats], lag_ratio=0.12),
            run_time=5.6
        )
        self.wait(2.4)

        # Zoom into the Ballon d'Or stat as the key flashpoint
        zoom_bg = Rectangle(
            width=9.5, height=1.6,
            fill_color=DARKER_BG, fill_opacity=0.92,
            stroke_color=ELO_GOLD, stroke_width=2
        )
        zoom_bg.move_to(DOWN * 2.8)
        zoom_messi = Text("Messi: 8 Ballon d'Or", font_size=24, color=ELO_BLUE, weight=BOLD)
        zoom_messi.move_to(DOWN * 2.6 + LEFT * 2.5)
        zoom_vs2 = Text("vs", font_size=22, color=TEXT_GRAY)
        zoom_vs2.move_to(DOWN * 2.6)
        zoom_cr7 = Text("Ronaldo: 5 Ballon d'Or", font_size=24, color=ELO_RED, weight=BOLD)
        zoom_cr7.move_to(DOWN * 2.6 + RIGHT * 2.5)
        zoom_note = Text("But Ronaldo won more UCL titles...", font_size=18, color=ELO_GOLD, slant=ITALIC)
        zoom_note.move_to(DOWN * 3.25)

        self.play(FadeIn(zoom_bg), run_time=1.2)
        self.play(Write(zoom_messi), Write(zoom_vs2), Write(zoom_cr7), run_time=3.2)

        # Zoom in on that debate box
        self.play(
            self.camera.frame.animate.scale(0.70).move_to(DOWN * 2.8),
            run_time=4
        )
        self.play(FadeIn(zoom_note, shift=UP * 0.2), run_time=2.8)
        self.wait(2)
        self.play(
            self.camera.frame.animate.scale(1 / 0.70).move_to(ORIGIN),
            run_time=3.2
        )

        conflict = Text(
            "Two all-timers — different strengths, impossible to compare directly",
            font_size=20, color=TEXT_GRAY, slant=ITALIC
        )
        conflict.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(conflict, shift=UP * 0.2), run_time=3.2)
        self.wait(2.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene0_3_MoreDebates(MovingCameraScene):
    """Scene 0.3: The pattern — every sport has this debate."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Every Sport Has This Problem", font_size=48, color=ELO_BLUE)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header), run_time=1.5)

        # Grid of debates
        debates = [
            ("Tennis",   "Djokovic",  "vs",  "Federer",  ELO_GREEN,  ELO_BLUE),
            ("Golf",     "Nicklaus",  "vs",  "Woods",    ELO_GOLD,   ELO_RED),
            ("Chess",    "Fischer",   "vs",  "Kasparov", ELO_PURPLE, ELO_GOLD),
            ("F1",       "Senna",     "vs",  "Schumacher", ELO_RED,  ELO_BLUE),
        ]

        debate_rows = VGroup()
        for sport, left, vs, right, col_l, col_r in debates:
            sport_lbl = Text(sport + ":", font_size=22, color=TEXT_GRAY, weight=BOLD)
            sport_lbl.set_width(1.8)

            left_lbl = Text(left, font_size=22, color=col_l, weight=BOLD)
            vs_lbl = Text("vs", font_size=18, color=TEXT_GRAY)
            right_lbl = Text(right, font_size=22, color=col_r, weight=BOLD)

            row = VGroup(sport_lbl, left_lbl, vs_lbl, right_lbl)
            row.arrange(RIGHT, buff=0.4)
            debate_rows.add(row)

        debate_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        debate_rows.move_to(LEFT * 1.5 + DOWN * 0.3)

        self.play(
            LaggedStart(*[FadeIn(row, shift=RIGHT * 0.3) for row in debate_rows], lag_ratio=0.2),
            run_time=7.2
        )
        self.wait(1.5)

        # Zoom into one row (Chess) to highlight the meta-problem
        chess_row = debate_rows[2]
        zoom_box = SurroundingRectangle(
            chess_row, color=ELO_GOLD, buff=0.18, corner_radius=0.1, stroke_width=2
        )
        chess_note = Text(
            "Fischer dominated the 70s — Kasparov dominated the 80s-90s",
            font_size=17, color=ELO_GOLD, slant=ITALIC
        )
        chess_note.next_to(chess_row, DOWN, buff=0.25)
        chess_note_bg = SurroundingRectangle(
            chess_note, fill_color=DARKER_BG, fill_opacity=0.85,
            stroke_width=0, buff=0.06
        )

        self.play(Create(zoom_box), run_time=1.6)
        self.play(
            self.camera.frame.animate.scale(0.68).move_to(chess_row.get_center() + DOWN * 0.2),
            run_time=3.6
        )
        self.play(FadeIn(chess_note_bg), FadeIn(chess_note, shift=UP * 0.15), run_time=2.8)
        self.wait(2)
        self.play(
            self.camera.frame.animate.scale(1 / 0.68).move_to(ORIGIN),
            run_time=3.2
        )

        # Universal truth
        truth_box = Rectangle(
            width=9.5, height=1.3,
            fill_color=ELO_BLUE, fill_opacity=0.12,
            stroke_color=ELO_BLUE, stroke_width=2
        )
        truth_box.to_edge(DOWN, buff=0.9)
        truth = Text(
            "The problem is universal: how do we compare greatness objectively?",
            font_size=22, color=TEXT_LIGHT
        )
        truth.move_to(truth_box)

        self.play(FadeIn(truth_box), Write(truth, run_time=4.8))
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=3.2)


class Scene0_4_TheQuestion(MovingCameraScene):
    """Scene 0.4: The central question — can math answer the GOAT debate?"""

    def construct(self):
        self.camera.background_color = DARK_BG

        # Open with the core tension
        tension = VGroup(
            Text("Wins?  Titles?  Stats?  Eye-test?", font_size=30, color=TEXT_GRAY),
            Text("Everyone argues. Nobody agrees.", font_size=28, color=ELO_RED),
        )
        tension.arrange(DOWN, buff=0.4)
        tension.move_to(UP * 1.8)

        self.play(
            LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tension], lag_ratio=0.4),
            run_time=4.8
        )
        self.wait(2.4)

        # The big question
        question_bg = Rectangle(
            width=11, height=1.6,
            fill_color=DARKER_BG, fill_opacity=0.9,
            stroke_color=ELO_GOLD, stroke_width=2.5
        )
        question_bg.move_to(ORIGIN)

        question = Text(
            "What if math could answer this?",
            font_size=40, color=ELO_GOLD, weight=BOLD
        )
        question.move_to(question_bg)

        self.play(FadeIn(question_bg), run_time=1.6)
        self.play(Write(question, run_time=6))
        self.wait(2)

        # Zoom into the question for emphasis
        self.play(
            self.camera.frame.animate.scale(0.80).move_to(question_bg.get_center()),
            run_time=3.6
        )
        self.wait(1.5)
        self.play(
            self.camera.frame.animate.scale(1 / 0.80).move_to(ORIGIN),
            run_time=2.8
        )

        # Sub-questions that follow
        sub_questions = VGroup(
            Text("Is there a number that captures how good a player is?", font_size=21, color=TEXT_LIGHT),
            Text("Can we compare athletes across eras, sports, and competitions?", font_size=21, color=TEXT_LIGHT),
            Text("Can we tell when an upset is really an upset?", font_size=21, color=TEXT_LIGHT),
        )
        sub_questions.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        sub_questions.move_to(DOWN * 1.8)

        # Add bullet dots
        for q in sub_questions:
            dot = Dot(radius=0.07, color=ELO_GOLD)
            dot.next_to(q, LEFT, buff=0.18)
            q.add_to_back(dot)

        self.play(
            LaggedStart(*[FadeIn(q, shift=RIGHT * 0.2) for q in sub_questions], lag_ratio=0.25),
            run_time=6
        )
        self.wait(2)

        # Zoom into the three sub-questions together
        self.play(
            self.camera.frame.animate.scale(0.75).move_to(sub_questions.get_center()),
            run_time=4
        )
        self.wait(2)
        self.play(
            self.camera.frame.animate.scale(1 / 0.75).move_to(ORIGIN),
            run_time=3.2
        )

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2.8)


class Scene0_5_VideoTitle(MovingCameraScene):
    """Scene 0.5: The video title card — let's find out."""

    def construct(self):
        self.camera.background_color = DARK_BG

        # Answer line
        answer = Text("The answer is yes.", font_size=40, color=ELO_GREEN, weight=BOLD)
        answer.move_to(UP * 1.5)

        self.play(Write(answer, run_time=4.8))
        self.wait(2)

        # The system
        system_name = Text("The Elo Rating System", font_size=56, color=ELO_BLUE, weight=BOLD)
        system_name.move_to(UP * 0.3)

        # Underline
        underline = Line(
            system_name.get_left() + DOWN * 0.1,
            system_name.get_right() + DOWN * 0.1,
            color=ELO_GOLD, stroke_width=3
        )

        self.play(Write(system_name, run_time=6))
        self.play(Create(underline), run_time=2)
        self.wait(1.2)

        # Zoom in on the title for a beat
        self.play(
            self.camera.frame.animate.scale(0.82).move_to(system_name.get_center()),
            run_time=3.2
        )
        self.wait(1.5)
        self.play(
            self.camera.frame.animate.scale(1 / 0.82).move_to(ORIGIN),
            run_time=2.8
        )

        # Subtitle
        subtitle = Text(
            "From chess to F1 — the math behind ranking everything",
            font_size=24, color=TEXT_GRAY
        )
        subtitle.move_to(DOWN * 0.5)

        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=4)
        self.wait(2)

        # Teaser bullets
        teaser = VGroup(
            Text("Harkness  ->  Elo  ->  Bayesian Inference", font_size=22, color=ELO_GOLD),
            Text("Chess  •  Formula 1  •  Facemash", font_size=20, color=TEXT_GRAY),
        )
        teaser.arrange(DOWN, buff=0.3)
        teaser.move_to(DOWN * 1.8)

        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in teaser], lag_ratio=0.4),
            run_time=4.8
        )
        self.wait(2)

        # Final zoom out + hold on title card
        self.play(
            self.camera.frame.animate.scale(0.90).move_to(DOWN * 0.2),
            run_time=4
        )
        self.wait(3)
        self.play(
            self.camera.frame.animate.scale(1 / 0.90).move_to(ORIGIN),
            run_time=2.4
        )
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=4)
