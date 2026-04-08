"""
Scene 4: The F1 Paradox
Explains why standard ELO rating fails for Formula 1.

This scene covers:
- The asymmetry problem in F1
- The car vs driver confusion
- Thought experiment: swapping drivers and cars
- Why standard ELO gives absurd results
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *


class F1ParadoxIntro(Scene):
    """Introduction to the F1 problem."""
    
    def construct(self):
        title = Text("The F1 Paradox", font_size=52, color=RED)
        subtitle = Text("When Perfect Math Fails", font_size=32, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1)
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(subtitle))


class ChessVsF1(Scene):
    """Compare Chess symmetry with F1 asymmetry."""
    
    def construct(self):
        title = Text("Chess vs Formula 1", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Chess side
        chess_title = Text("Chess", font_size=32, color=TEAL)
        chess_title.shift(UP * 1.5 + LEFT * 3.5)
        
        chess_props = VGroup(
            Text("✓ Same pieces", font_size=22, color=WHITE),
            Text("✓ Same board", font_size=22, color=WHITE),
            Text("✓ Same rules", font_size=22, color=WHITE),
            Text("= SYMMETRIC", font_size=24, color=TEAL),
        )
        chess_props.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        chess_props.shift(UP * 0.2 + LEFT * 3.5)
        
        # F1 side
        f1_title = Text("Formula 1", font_size=32, color=ORANGE)
        f1_title.shift(UP * 1.5 + RIGHT * 3.5)
        
        f1_props = VGroup(
            Text("✗ Different cars", font_size=22, color=RED),
            Text("✗ Different power", font_size=22, color=RED),
            Text("✗ Different downforce", font_size=22, color=RED),
            Text("= ASYMMETRIC", font_size=24, color=ORANGE),
        )
        f1_props.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        f1_props.shift(UP * 0.2 + RIGHT * 3)
        
        # Dividing line
        divider = DashedLine(UP * 1.8, DOWN * 2, color=GREY, dash_length=0.1)
        
        self.play(Write(chess_title), Write(f1_title), run_time=1)
        self.play(Create(divider), run_time=0.5)
        
        self.play(Write(chess_props), Write(f1_props), run_time=2)
        
        self.wait(1)
        
        # The problem
        problem = Text(
            "ELO assumes symmetry that doesn't exist in F1",
            font_size=28, color=YELLOW
        )
        problem.shift(DOWN * 2)
        
        box = SurroundingRectangle(problem, color=YELLOW, buff=0.15)
        
        self.play(Write(problem), Create(box), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class TheThoughtExperiment(Scene):
    """The famous driver-car swap thought experiment."""
    
    def construct(self):
        title = Text("A Thought Experiment", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Setup scenario
        scenario_text = Text(
            "Imagine two drivers racing...",
            font_size=28, color=WHITE
        )
        scenario_text.shift(UP * 1.5)
        
        self.play(Write(scenario_text), run_time=1)
        
        # Driver A: World Champion in slow car
        driver_a_box = self.create_driver_card(
            "Max Verstappen",
            "4x World Champion",
            "Haas",
            TEAL, RED
        )
        driver_a_box.shift(LEFT * 3.5)
        
        # Driver B: Rookie in fast car
        driver_b_box = self.create_driver_card(
            "Logan Sargeant",
            "Rookie",
            "Red Bull",
            ORANGE, LIGHT_BLUE
        )
        driver_b_box.shift(RIGHT * 3.5)
        
        self.play(FadeIn(driver_a_box), FadeIn(driver_b_box), run_time=1.5)
        self.wait(1)
        
        # The question
        question = Text("Who wins the race?", font_size=36, color=YELLOW)
        question.shift(DOWN * 1)
        
        self.play(Write(question), run_time=1)
        self.wait(1)
        
        # Answer
        answer = Text("Logan (in the Red Bull)", font_size=32, color=ORANGE)
        answer.shift(DOWN * 1.8)
        
        self.play(Write(answer), run_time=1)
        self.wait(1)
        
        # What ELO concludes
        elo_conclusion = VGroup(
            Text("What Standard ELO Concludes:", font_size=26, color=RED),
            Text("\"Logan Sargeant > Max Verstappen\"", font_size=30, color=RED),
        )
        elo_conclusion.arrange(DOWN, buff=0.1)
        elo_conclusion.shift(DOWN * 2.8)
        
        self.play(Write(elo_conclusion), run_time=1.5)
        
        # X mark
        x_mark = Text("✗", font_size=60, color=RED)
        x_mark.next_to(elo_conclusion, RIGHT, buff=0.3)
        
        self.play(Write(x_mark), run_time=0.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    def create_driver_card(self, name, status, team, driver_color, team_color):
        """Create a driver info card."""
        box = RoundedRectangle(
            corner_radius=0.15, width=4.5, height=3,
            fill_color=DARK_BG, fill_opacity=0.9,
            stroke_color=driver_color, stroke_width=2
        )
        
        name_text = Text(name, font_size=24, color=driver_color)
        status_text = Text(status, font_size=18, color=GREY)
        
        car_label = Text("Driving:", font_size=16, color=WHITE)
        team_text = Text(team, font_size=22, color=team_color)
        
        content = VGroup(name_text, status_text, car_label, team_text)
        content.arrange(DOWN, buff=0.15)
        content.move_to(box.get_center())
        
        return VGroup(box, content)


class EloMisattribution(Scene):
    """Show how ELO misattributes car performance to driver skill."""
    
    def construct(self):
        title = Text("The Attribution Problem", font_size=40, color=ORANGE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # What ELO sees
        elo_sees = Text("What Standard ELO 'Sees':", font_size=28, color=GREY)
        elo_sees.shift(UP * 1.5)
        
        self.play(Write(elo_sees), run_time=0.8)
        
        # Simple box: Person
        elo_box = RoundedRectangle(
            corner_radius=0.1, width=3, height=2,
            fill_color=LIGHT_BLUE, fill_opacity=0.3,
            stroke_color=LIGHT_BLUE, stroke_width=2
        )
        elo_box.shift(LEFT * 2.5)
        
        elo_label = Text("Player", font_size=24, color=LIGHT_BLUE)
        elo_label.move_to(elo_box.get_center())
        
        elo_rating = Text("Rating: 1800", font_size=18, color=WHITE)
        elo_rating.next_to(elo_box, DOWN, buff=0.2)
        
        self.play(Create(elo_box), Write(elo_label), Write(elo_rating), run_time=1)
        
        # Versus sign
        vs = Text("vs", font_size=24, color=GREY)
        
        self.play(Write(vs), run_time=0.3)
        
        # What F1 actually has
        reality = Text("What F1 Actually Has:", font_size=28, color=GREY)
        reality.shift(UP * 1.5 + RIGHT * 3)
        
        self.play(Write(reality), run_time=0.8)
        
        # Stacked boxes: Driver + Car
        driver_box = RoundedRectangle(
            corner_radius=0.1, width=3, height=1,
            fill_color=TEAL, fill_opacity=0.3,
            stroke_color=TEAL, stroke_width=2
        )
        driver_box.shift(RIGHT * 3 + UP * 0.3)
        
        driver_label = Text("Driver", font_size=20, color=TEAL)
        driver_label.move_to(driver_box.get_center())
        
        car_box = RoundedRectangle(
            corner_radius=0.1, width=3, height=1,
            fill_color=ORANGE, fill_opacity=0.3,
            stroke_color=ORANGE, stroke_width=2
        )
        car_box.shift(RIGHT * 3 + DOWN * 0.7)
        
        car_label = Text("Car", font_size=20, color=ORANGE)
        car_label.move_to(car_box.get_center())
        
        # Plus sign between them
        plus = Text("+", font_size=36, color=WHITE)
        plus.move_to((driver_box.get_center() + car_box.get_center()) / 2)
        
        self.play(
            Create(driver_box), Write(driver_label),
            Write(plus),
            Create(car_box), Write(car_label),
            run_time=1.5
        )
        
        self.wait(1)
        
        # The problem statement
        problem = VGroup(
            Text("ELO has ONE variable for performance", font_size=24, color=WHITE),
            Text("F1 has TWO: Driver + Car", font_size=24, color=WHITE),
            Text("ELO CONFLATES them!", font_size=28, color=RED),
        )
        problem.arrange(DOWN, buff=0.15)
        problem.shift(DOWN * 2)
        
        self.play(Write(problem), run_time=2)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class RealWorldExamples(Scene):
    """Show real examples where ELO would fail."""
    
    def construct(self):
        title = Text("Real Examples of ELO Failure", font_size=40, color=RED)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        examples = [
            ("2020", "George Russell fills in at Mercedes", 
             "Qualifies P2, leads race", "Would ELO say he was always better than Hamilton?", RED),
            ("2014", "Vettel moves to Ferrari",
             "Goes from 4x Champion to midfield", "Did he suddenly lose skill? No - the car changed!", ORANGE),
            ("2023", "Ricciardo returns at AlphaTauri",
             "Struggles in slower car", "Is he worse than his 2018 Red Bull self?", YELLOW),
        ]
        
        y_pos = 1
        for year, event, result, question, color in examples:
            info_box = RoundedRectangle(
                corner_radius=0.1, width=11, height=1.4,
                fill_color=color, fill_opacity=0.1,
                stroke_color=color, stroke_width=1.5
            )
            info_box.shift(UP * y_pos)
            
            year_text = Text(year, font_size=20, color=color)
            year_text.align_to(info_box, LEFT).shift(RIGHT * 0.2)
            
            event_text = Text(event, font_size=18, color=WHITE)
            event_text.next_to(year_text, RIGHT, buff=0.2)
            
            result_text = Text(f"→ {result}", font_size=16, color=GREY)
            result_text.next_to(info_box, ORIGIN).shift(DOWN * 0.2)
            
            self.play(
                Create(info_box),
                Write(year_text), Write(event_text), Write(result_text),
                run_time=1
            )
            
            y_pos -= 1.6
        
        self.wait(2)
        
        # Conclusion
        conclusion = Text(
            "The car is a confounding variable that ELO cannot handle",
            font_size=26, color=YELLOW
        )
        conclusion.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(Write(conclusion), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class TheRequirement(Scene):
    """State what we need to solve this problem."""
    
    def construct(self):
        title = Text("What Do We Need?", font_size=44, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.5)
        
        self.play(Write(title), run_time=1)
        
        # Requirements
        requirements = VGroup(
            Text("1. A way to separate Driver Skill from Car Performance", 
                 font_size=26, color=WHITE),
            Text("2. A method to 'handicap' the car advantage", 
                 font_size=26, color=WHITE),
            Text("3. A framework that updates beliefs, not just counts", 
                 font_size=26, color=WHITE),
        )
        requirements.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        requirements.shift(UP * 0.3)
        
        for req in requirements:
            self.play(Write(req), run_time=1)
            self.wait(0.3)
        
        self.wait(1)
        
        # The answer
        answer_box = RoundedRectangle(
            corner_radius=0.15, width=8, height=2,
            fill_color=LIGHT_BLUE, fill_opacity=0.15,
            stroke_color=LIGHT_BLUE, stroke_width=3
        )
        answer_box.shift(DOWN * 1.8)
        
        answer_text = Text("Bayesian Inference", font_size=44, color=LIGHT_BLUE)
        answer_subtext = Text(
            "A statistical framework designed for exactly this",
            font_size=22, color=WHITE
        )
        
        answer_text.move_to(answer_box.get_center() + UP * 0.3)
        answer_subtext.move_to(answer_box.get_center() + DOWN * 0.4)
        
        self.play(Create(answer_box), run_time=0.8)
        self.play(Write(answer_text), run_time=1)
        self.play(Write(answer_subtext), run_time=1)
        
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Transition
        next_title = Text("Next: Bayesian Inference", font_size=48, color=LIGHT_BLUE)
        self.play(Write(next_title), run_time=1)
        self.wait(1)
        self.play(FadeOut(next_title))


if __name__ == "__main__":
    pass
