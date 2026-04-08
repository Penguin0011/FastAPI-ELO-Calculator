"""
Scene 5: Bayesian Inference Primer
Introduces Bayesian inference as the solution to the F1 problem.

This scene covers:
- The philosophy of Bayesian thinking
- Prior, Likelihood, and Posterior
- Updating beliefs with evidence
- The "noisy experiment" metaphor
"""

from manim import *
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.colors import *


class BayesianIntro(Scene):
    """Introduction to Bayesian thinking."""
    
    def construct(self):
        title = Text("Bayesian Inference", font_size=52, color=LIGHT_BLUE)
        subtitle = Text("A Different Way of Thinking", font_size=28, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(subtitle))


class FrequentistVsBayesian(Scene):
    """Contrast frequentist vs Bayesian approaches."""
    
    def construct(self):
        title = Text("Two Schools of Thought", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Frequentist side
        freq_title = Text("Standard ELO\n(Frequentist)", font_size=28, color=ORANGE)
        freq_title.shift(UP * 1 + LEFT * 3.5)
        
        freq_desc = VGroup(
            Text("\"Count wins and losses\"", font_size=20, color=WHITE),
            Text("\"More data = better estimates\"", font_size=20, color=WHITE),
            Text("\"Past performance = future\"", font_size=20, color=WHITE),
        )
        freq_desc.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        freq_desc.shift(DOWN * 0.3 + LEFT * 4)
        
        # Bayesian side
        bayes_title = Text("Bayesian\nApproach", font_size=28, color=LIGHT_BLUE)
        bayes_title.shift(UP * 1 + RIGHT * 3.5)
        
        bayes_desc = VGroup(
            Text("\"Update beliefs with evidence\"", font_size=20, color=WHITE),
            Text("\"Account for uncertainty\"", font_size=20, color=WHITE),
            Text("\"Model hidden variables\"", font_size=20, color=WHITE),
        )
        bayes_desc.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        bayes_desc.shift(DOWN * 0.3 + RIGHT * 2.5)
        
        # Divider
        divider = DashedLine(UP * 1.5, DOWN * 1.5, color=GREY)
        
        self.play(Write(freq_title), Write(bayes_title), Create(divider), run_time=1)
        self.play(Write(freq_desc), Write(bayes_desc), run_time=2)
        
        self.wait(1)
        
        # Key difference
        key_diff = VGroup(
            Text("Key Difference:", font_size=26, color=GOLD),
            Text("Bayesian can model HIDDEN VARIABLES like car performance!", 
                 font_size=22, color=YELLOW),
        )
        key_diff.arrange(DOWN, buff=0.1)
        key_diff.shift(DOWN * 2)
        
        self.play(Write(key_diff), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class TheBayesianCycle(Scene):
    """Visualize the Prior -> Evidence -> Posterior cycle."""
    
    def construct(self):
        title = Text("The Bayesian Cycle", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Create three nodes
        prior_circle = Circle(radius=1, color=TEAL, stroke_width=3)
        prior_circle.shift(LEFT * 4)
        prior_text = Text("Prior\nBelief", font_size=22, color=TEAL)
        prior_text.move_to(prior_circle.get_center())
        prior_group = VGroup(prior_circle, prior_text)
        
        evidence_circle = Circle(radius=1, color=ORANGE, stroke_width=3)
        evidence_text = Text("Evidence\n(Data)", font_size=22, color=ORANGE)
        evidence_text.move_to(evidence_circle.get_center())
        evidence_group = VGroup(evidence_circle, evidence_text)
        
        posterior_circle = Circle(radius=1, color=GOLD, stroke_width=3)
        posterior_circle.shift(RIGHT * 4)
        posterior_text = Text("Posterior\n(Updated)", font_size=22, color=GOLD)
        posterior_text.move_to(posterior_circle.get_center())
        posterior_group = VGroup(posterior_circle, posterior_text)
        
        # Arrows connecting them
        arrow1 = Arrow(
            prior_circle.get_right(), evidence_circle.get_left(),
            color=WHITE, stroke_width=2, buff=0.1
        )
        arrow2 = Arrow(
            evidence_circle.get_right(), posterior_circle.get_left(),
            color=WHITE, stroke_width=2, buff=0.1
        )
        
        # Animate appearance
        self.play(Create(prior_circle), Write(prior_text), run_time=1)
        self.play(GrowArrow(arrow1), run_time=0.5)
        self.play(Create(evidence_circle), Write(evidence_text), run_time=1)
        self.play(GrowArrow(arrow2), run_time=0.5)
        self.play(Create(posterior_circle), Write(posterior_text), run_time=1)
        
        self.wait(1)
        
        # Descriptions below
        prior_desc = Text("What we believed\nBEFORE the data", font_size=16, color=GREY)
        prior_desc.next_to(prior_circle, DOWN, buff=0.3)
        
        evidence_desc = Text("The new\nobservation", font_size=16, color=GREY)
        evidence_desc.next_to(evidence_circle, DOWN, buff=0.3)
        
        posterior_desc = Text("What we believe\nAFTER the data", font_size=16, color=GREY)
        posterior_desc.next_to(posterior_circle, DOWN, buff=0.3)
        
        self.play(
            Write(prior_desc), Write(evidence_desc), Write(posterior_desc),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Loop arrow (posterior becomes new prior)
        loop_arrow = CurvedArrow(
            posterior_circle.get_top() + RIGHT * 0.5,
            prior_circle.get_top() + LEFT * 0.5,
            color=PURPLE, stroke_width=2, angle=-PI/2
        )
        loop_text = Text("Next race's Prior", font_size=16, color=PURPLE)
        loop_text.next_to(loop_arrow, UP, buff=0.1)
        
        self.play(Create(loop_arrow), Write(loop_text), run_time=1.5)
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class BayesianF1Example(Scene):
    """Concrete F1 example using Bayesian reasoning."""
    
    def construct(self):
        title = Text("Bayesian Thinking in F1", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Prior belief
        step1_title = Text("1. Prior Belief", font_size=28, color=TEAL)
        step1_title.shift(UP * 1.5 + LEFT * 4)
        
        step1_content = VGroup(
            Text("\"Max Verstappen is an 1800-rated driver\"", font_size=22, color=WHITE),
            Text("Based on: 4 World Championships, history", font_size=18, color=GREY),
        )
        step1_content.arrange(DOWN, buff=0.1)
        step1_content.shift(UP * 0.7 + LEFT * 2)
        
        self.play(Write(step1_title), run_time=0.5)
        self.play(Write(step1_content), run_time=1)
        self.wait(0.5)
        
        # Evidence (the race)
        step2_title = Text("2. Evidence (The Race)", font_size=28, color=ORANGE)
        step2_title.shift(UP * 1.5 + RIGHT * 2.5)
        
        step2_content = VGroup(
            Text("Max finishes P1 in his Red Bull", font_size=22, color=WHITE),
        )
        step2_content.shift(UP * 0.7 + RIGHT * 2)
        
        self.play(Write(step2_title), run_time=0.5)
        self.play(Write(step2_content), run_time=0.8)
        self.wait(0.5)
        
        # The twist - checking probability
        twist = VGroup(
            Text("THE TWIST:", font_size=24, color=YELLOW),
            Text("We check: How PROBABLE was this result?", font_size=22, color=WHITE),
        )
        twist.arrange(DOWN, buff=0.1)
        twist.shift(DOWN * 0.5)
        
        self.play(Write(twist), run_time=1.5)
        self.wait(1)
        
        # Case 1: In a rocket ship
        case1 = RoundedRectangle(
            corner_radius=0.1, width=5, height=1.3,
            fill_color=DARK_GREY, fill_opacity=0.5,
            stroke_color=TEAL, stroke_width=1.5
        )
        case1.shift(DOWN * 2 + LEFT * 2.8)
        
        case1_text = VGroup(
            Text("If in dominant car:", font_size=18, color=TEAL),
            Text("P1 was 99% likely", font_size=16, color=GREY),
            Text("→ Weak evidence, rating barely changes", font_size=16, color=ELO_NEUTRAL),
        )
        case1_text.arrange(DOWN, buff=0.05)
        case1_text.move_to(case1.get_center())
        
        # Case 2: In a tractor
        case2 = RoundedRectangle(
            corner_radius=0.1, width=5, height=1.3,
            fill_color=DARK_GREY, fill_opacity=0.5,
            stroke_color=ORANGE, stroke_width=1.5
        )
        case2.shift(DOWN * 2 + RIGHT * 2.8)
        
        case2_text = VGroup(
            Text("If in slow car:", font_size=18, color=ORANGE),
            Text("P1 was 1% likely", font_size=16, color=GREY),
            Text("→ Strong evidence, rating jumps!", font_size=16, color=ELO_POSITIVE),
        )
        case2_text.arrange(DOWN, buff=0.05)
        case2_text.move_to(case2.get_center())
        
        self.play(
            Create(case1), Write(case1_text),
            Create(case2), Write(case2_text),
            run_time=2
        )
        
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class NoisyExperiment(Scene):
    """The 'noisy experiment' metaphor."""
    
    def construct(self):
        title = Text("The 'Noisy Experiment' View", font_size=40, color=LIGHT_BLUE)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Core idea
        idea = VGroup(
            Text("Every race is a NOISY EXPERIMENT", font_size=32, color=WHITE),
            Text("We're trying to measure: Driver Skill", font_size=26, color=TEAL),
            Text("But the Car adds NOISE to our measurement", font_size=26, color=ORANGE),
        )
        idea.arrange(DOWN, buff=0.3)
        idea.shift(UP * 0.8)
        
        self.play(Write(idea), run_time=2)
        self.wait(1)
        
        # Visual: Signal + Noise
        signal_box = RoundedRectangle(
            corner_radius=0.1, width=3, height=1.5,
            fill_color=TEAL, fill_opacity=0.3,
            stroke_color=TEAL, stroke_width=2
        )
        signal_box.shift(DOWN * 1.3 + LEFT * 3)
        signal_label = Text("SIGNAL\n(Driver Skill)", font_size=20, color=TEAL)
        signal_label.move_to(signal_box.get_center())
        
        plus_sign = Text("+", font_size=48, color=WHITE)
        plus_sign.shift(DOWN * 1.3)
        
        noise_box = RoundedRectangle(
            corner_radius=0.1, width=3, height=1.5,
            fill_color=ORANGE, fill_opacity=0.3,
            stroke_color=ORANGE, stroke_width=2
        )
        noise_box.shift(DOWN * 1.3 + RIGHT * 3)
        noise_label = Text("NOISE\n(Car Performance)", font_size=20, color=ORANGE)
        noise_label.move_to(noise_box.get_center())
        
        equals_sign = Text("=", font_size=48, color=WHITE)
        equals_sign.shift(DOWN * 2.8 + LEFT * 1.5)
        
        result_box = RoundedRectangle(
            corner_radius=0.1, width=4, height=1,
            fill_color=PURPLE, fill_opacity=0.3,
            stroke_color=PURPLE, stroke_width=2
        )
        result_box.shift(DOWN * 2.8 + RIGHT * 1.5)
        result_label = Text("Race Result (Position)", font_size=18, color=PURPLE)
        result_label.move_to(result_box.get_center())
        
        self.play(
            Create(signal_box), Write(signal_label),
            Write(plus_sign),
            Create(noise_box), Write(noise_label),
            run_time=1.5
        )
        self.wait(0.5)
        
        self.play(
            Write(equals_sign),
            Create(result_box), Write(result_label),
            run_time=1
        )
        
        self.wait(1)
        
        # Key insight
        insight = Text(
            "Bayesian methods let us mathematically 'subtract' the noise!",
            font_size=26, color=YELLOW
        )
        insight.to_edge(DOWN).shift(UP * 0.3)
        
        self.play(Write(insight), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class DistributionVisualization(Scene):
    """Show how distributions narrow with more data."""
    
    def construct(self):
        title = Text("Belief Distributions", font_size=40, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.3)
        
        self.play(Write(title), run_time=1)
        
        # Create axes
        axes = Axes(
            x_range=[1200, 2200, 200],
            y_range=[0, 0.01, 0.002],
            x_length=10,
            y_length=3.5,
            axis_config={"color": GREY, "include_tip": False},
        )
        axes.shift(DOWN * 0.5)
        
        x_label = Text("Driver Rating", font_size=18, color=GREY)
        x_label.next_to(axes, DOWN, buff=0.2)
        
        y_label = Text("Probability Density", font_size=16, color=GREY)
        y_label.next_to(axes, LEFT, buff=0.2).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1)
        
        # Wide prior distribution (high uncertainty)
        import numpy as np
        
        def gaussian(x, mu, sigma):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
        
        # Prior: Wide distribution
        prior_graph = axes.plot(
            lambda x: gaussian(x, 1500, 200),
            x_range=[1200, 2200],
            color=TEAL,
            stroke_width=3
        )
        prior_label = Text("Prior (High Uncertainty)", font_size=18, color=TEAL)
        prior_label.shift(UP * 1.5 + LEFT * 2)
        
        self.play(Create(prior_graph), Write(prior_label), run_time=1.5)
        self.wait(1)
        
        # After some races: Medium distribution
        medium_graph = axes.plot(
            lambda x: gaussian(x, 1700, 100),
            x_range=[1200, 2200],
            color=ORANGE,
            stroke_width=3
        )
        medium_label = Text("After 10 Races", font_size=18, color=ORANGE)
        medium_label.shift(UP * 1.5)
        
        self.play(Create(medium_graph), Write(medium_label), run_time=1.5)
        self.wait(1)
        
        # After many races: Narrow distribution
        narrow_graph = axes.plot(
            lambda x: gaussian(x, 1800, 50),
            x_range=[1200, 2200],
            color=GOLD,
            stroke_width=3
        )
        narrow_label = Text("After 50 Races (Low Uncertainty)", font_size=18, color=GOLD)
        narrow_label.shift(UP * 1.5 + RIGHT * 2)
        
        self.play(Create(narrow_graph), Write(narrow_label), run_time=1.5)
        
        self.wait(1)
        
        # Explanation
        explanation = Text(
            "More races → More confidence in our estimate → Narrower distribution",
            font_size=22, color=WHITE
        )
        explanation.to_edge(DOWN).shift(UP * 0.3)
        
        self.play(Write(explanation), run_time=1.5)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])


class BayesianConclusion(Scene):
    """Conclude and transition to the F1 model."""
    
    def construct(self):
        title = Text("Why Bayesian for F1?", font_size=44, color=GOLD)
        title.to_edge(UP).shift(DOWN * 0.5)
        
        self.play(Write(title), run_time=1)
        
        # Summary benefits
        benefits = VGroup(
            Text("✓ Models hidden variables (Car Performance)", font_size=26, color=TEAL),
            Text("✓ Updates beliefs proportional to 'surprise'", font_size=26, color=TEAL),
            Text("✓ Accounts for car quality as a 'handicap'", font_size=26, color=TEAL),
            Text("✓ Separates Signal (Driver) from Noise (Car)", font_size=26, color=TEAL),
        )
        benefits.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        benefits.center()
        
        for benefit in benefits:
            self.play(Write(benefit), run_time=0.8)
        
        self.wait(2)
        
        # Transition
        transition = Text(
            "Now let's see how we implement this...",
            font_size=32, color=ORANGE
        )
        transition.shift(DOWN * 2)
        
        self.play(Write(transition), run_time=1.5)
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        next_title = Text("Next: Composite Effective Strength", font_size=44, color=LIGHT_BLUE)
        self.play(Write(next_title), run_time=1)
        self.wait(1)
        self.play(FadeOut(next_title))


if __name__ == "__main__":
    pass
