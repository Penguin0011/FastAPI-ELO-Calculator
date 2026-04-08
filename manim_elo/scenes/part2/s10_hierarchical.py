# Section 10: Hierarchical Bayesian Modeling Structure
# 6 Scenes covering latent variable decomposition

from manim import *
import numpy as np
import sys
sys.path.append('..')
from utils.colors import *


class Scene10_1_LatentDecomposition(Scene):
    """Scene 10.1: The Latent Variable Decomposition."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Hierarchical Decomposition", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # The formula
        formula = MathTex(
            r"\lambda_{ijr}", r"=", r"\alpha_i", r"+", r"\beta_j", r"+", r"\gamma_{ij}", r"+", r"\epsilon_{ijr}",
            font_size=44
        )
        formula.move_to(UP * 1)
        
        # Color each component
        formula[0].set_color(TEXT_WHITE)  # Outcome
        formula[2].set_color(ELO_BLUE)     # Driver
        formula[4].set_color(ELO_GOLD)     # Constructor
        formula[6].set_color(ELO_GREEN)    # Track
        formula[8].set_color(ELO_PURPLE)   # Noise
        
        self.play(Write(formula), run_time=2)
        
        # Legend
        legend = VGroup(
            VGroup(Dot(color=ELO_BLUE), Text("α = Driver skill", font_size=18, color=TEXT_GRAY)),
            VGroup(Dot(color=ELO_GOLD), Text("β = Constructor advantage", font_size=18, color=TEXT_GRAY)),
            VGroup(Dot(color=ELO_GREEN), Text("γ = Track-specific effect", font_size=18, color=TEXT_GRAY)),
            VGroup(Dot(color=ELO_PURPLE), Text("ε = Random noise", font_size=18, color=TEXT_GRAY))
        )
        
        for item in legend:
            item.arrange(RIGHT, buff=0.2)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.move_to(DOWN * 1.5)
        
        self.play(FadeIn(legend), run_time=1)
        
        # Visual: Stacked bar
        stack = VGroup()
        heights = [1.5, 1.2, 0.6, 0.3]
        colors = [ELO_BLUE, ELO_GOLD, ELO_GREEN, ELO_PURPLE]
        labels = ["Driver", "Car", "Track", "Noise"]
        
        current_y = -3
        for h, c, l in zip(heights, colors, labels):
            bar = Rectangle(
                width=2.5, height=h,
                fill_color=c, fill_opacity=0.7,
                stroke_color=WHITE, stroke_width=1
            )
            bar.move_to(RIGHT * 3.5 + UP * (current_y + h/2))
            label = Text(l, font_size=14, color=TEXT_WHITE)
            label.move_to(bar)
            stack.add(VGroup(bar, label))
            current_y += h
        
        equals = Text("=", font_size=32)
        equals.move_to(RIGHT * 1 + DOWN * 1.5)
        
        result_bar = Rectangle(
            width=2.5, height=3.6,
            fill_color=TEXT_GRAY, fill_opacity=0.5,
            stroke_color=WHITE
        )
        result_bar.move_to(LEFT * 2 + DOWN * 1.2)
        result_label = Text("Observed\nPerformance", font_size=14, color=TEXT_WHITE)
        result_label.move_to(result_bar)
        
        self.play(
            FadeIn(result_bar), FadeIn(result_label),
            Write(equals),
            FadeIn(stack),
            run_time=1.5
        )
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene10_2_IdentifiabilityProblem(Scene):
    """Scene 10.2: The Identifiability Problem."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("The Identifiability Problem", font_size=44, color=ELO_RED)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Problem statement
        problem = Text(
            "We observe α + β, but not α and β separately",
            font_size=24,
            color=TEXT_LIGHT
        )
        problem.move_to(UP * 1.5)
        
        self.play(Write(problem), run_time=1)
        
        # Example: One driver per team
        case1 = VGroup(
            Text("Case 1: One driver per team", font_size=20, color=ELO_RED),
            Text("α and β perfectly collinear", font_size=16, color=TEXT_GRAY),
            Text("Infinite solutions!", font_size=16, color=ELO_RED)
        )
        case1.arrange(DOWN, buff=0.15)
        case1.move_to(LEFT * 3.5 + DOWN * 0.3)
        case1_box = SurroundingRectangle(case1, color=ELO_RED, buff=0.15)
        
        self.play(FadeIn(case1), Create(case1_box), run_time=1)
        
        # Example: Two drivers per team
        case2 = VGroup(
            Text("Case 2: Two drivers per team", font_size=20, color=ELO_GREEN),
            Text("Difference identified!", font_size=16, color=TEXT_GRAY),
            Text("But absolute level floats", font_size=16, color=ELO_GOLD)
        )
        case2.arrange(DOWN, buff=0.15)
        case2.move_to(RIGHT * 3.5 + DOWN * 0.3)
        case2_box = SurroundingRectangle(case2, color=ELO_GREEN, buff=0.15)
        
        self.play(FadeIn(case2), Create(case2_box), run_time=1)
        
        # Solution hint
        solution = VGroup(
            Text("Solution:", font_size=22, color=ELO_GOLD),
            Text("Hierarchical priors provide anchoring", font_size=18, color=TEXT_GRAY)
        )
        solution.arrange(DOWN, buff=0.1)
        solution.move_to(DOWN * 2.5)
        
        self.play(FadeIn(solution), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene10_3_DriverPriors(Scene):
    """Scene 10.3: Driver Priors from Feeder Series."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Prior from Feeder Series", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Hierarchy visualization
        f3 = Rectangle(width=2, height=0.7, fill_color="#666666", fill_opacity=0.5)
        f3_label = Text("F3", font_size=18)
        f3_label.move_to(f3)
        f3_group = VGroup(f3, f3_label)
        f3_group.move_to(DOWN * 2)
        
        f2 = Rectangle(width=2, height=0.7, fill_color=ELO_BLUE, fill_opacity=0.5)
        f2_label = Text("F2", font_size=18)
        f2_label.move_to(f2)
        f2_group = VGroup(f2, f2_label)
        f2_group.move_to(DOWN * 1)
        
        f1 = Rectangle(width=2, height=0.7, fill_color=ELO_GOLD, fill_opacity=0.7)
        f1_label = Text("F1", font_size=18)
        f1_label.move_to(f1)
        f1_group = VGroup(f1, f1_label)
        f1_group.move_to(ORIGIN)
        
        arrows = VGroup(
            Arrow(f3_group.get_top(), f2_group.get_bottom(), color=TEXT_GRAY, buff=0.1),
            Arrow(f2_group.get_top(), f1_group.get_bottom(), color=TEXT_GRAY, buff=0.1)
        )
        
        hierarchy = VGroup(f3_group, f2_group, f1_group, arrows)
        hierarchy.move_to(LEFT * 3.5 + DOWN * 0.5)
        
        self.play(FadeIn(hierarchy), run_time=1)
        
        # Prior formula
        formula = MathTex(
            r"\mu_{\alpha_i}^{(0)} = f(\text{F2 Performance}_i)",
            font_size=32
        )
        formula.move_to(RIGHT * 2 + UP * 0.5)
        
        self.play(Write(formula), run_time=1)
        
        # Examples
        examples = VGroup(
            Text("F2 Champion → High F1 prior", font_size=18, color=ELO_GREEN),
            Text("Mid-pack F2 → Average prior", font_size=18, color=TEXT_GRAY),
            Text("Pay driver (no F2) → Lower prior", font_size=18, color=ELO_RED)
        )
        examples.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        examples.move_to(RIGHT * 2 + DOWN * 1.5)
        
        self.play(FadeIn(examples), run_time=1)
        
        # Caption
        caption = Text(
            "Success in junior series informs initial F1 belief",
            font_size=20,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.4)
        
        self.play(Write(caption), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene10_4_ConstructorEvolution(Scene):
    """Scene 10.4: Constructor Evolution - Autoregressive model."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Constructor Strength Evolution", font_size=44, color=ELO_GOLD)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Formula
        formula = MathTex(
            r"\beta_j^{(t)} \sim \mathcal{N}(\beta_j^{(t-1)}, \sigma_\beta^2)",
            font_size=40
        )
        formula.move_to(UP * 1)
        
        self.play(Write(formula), run_time=1.5)
        
        # Interpretation
        interp = Text(
            "Next season's strength ≈ This season's + Random drift",
            font_size=22,
            color=TEXT_LIGHT
        )
        interp.move_to(UP * 0.3)
        
        self.play(Write(interp), run_time=1)
        
        # Time series visualization
        axes = Axes(
            x_range=[2018, 2024, 1],
            y_range=[0, 100, 20],
            x_length=8,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 12}
        )
        axes.shift(DOWN * 1.5)
        
        x_label = Text("Season", font_size=14, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        
        y_label = Text("Constructor β", font_size=14, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2)
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.8)
        
        # Constructor trajectories
        # Mercedes
        merc_points = [(2018, 90), (2019, 88), (2020, 95), (2021, 85), (2022, 50), (2023, 65)]
        merc_line = VMobject(color="#00D2BE")
        merc_line.set_points_smoothly([axes.c2p(x, y) for x, y in merc_points])
        merc_label = Text("Mercedes", font_size=12, color="#00D2BE")
        merc_label.next_to(axes.c2p(2023, 65), RIGHT, buff=0.1)
        
        # Red Bull
        rb_points = [(2018, 70), (2019, 68), (2020, 72), (2021, 90), (2022, 98), (2023, 95)]
        rb_line = VMobject(color="#0600EF")
        rb_line.set_points_smoothly([axes.c2p(x, y) for x, y in rb_points])
        rb_label = Text("Red Bull", font_size=12, color="#0600EF")
        rb_label.next_to(axes.c2p(2023, 95), RIGHT, buff=0.1)
        
        self.play(
            Create(merc_line), FadeIn(merc_label),
            Create(rb_line), FadeIn(rb_label),
            run_time=2
        )
        
        # Strong autocorrelation note
        note = Text(
            "Strong autocorrelation: Good team likely stays good",
            font_size=18,
            color=ELO_GOLD
        )
        note.to_edge(DOWN, buff=0.3)
        
        self.play(Write(note), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene10_5_RuleChangeInflation(Scene):
    """Scene 10.5: Rule Change Inflation - Resetting priors."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Regulation Changes", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Timeline with rule changes
        timeline = Line(LEFT * 5, RIGHT * 5, color=TEXT_GRAY)
        timeline.move_to(UP * 0.5)
        
        self.play(Create(timeline), run_time=0.5)
        
        # Years
        years = ["2013", "2014", "2021", "2022"]
        positions = [-3, -1, 1, 3]
        
        for year, pos in zip(years, positions):
            dot = Dot(timeline.get_center() + RIGHT * pos, color=TEXT_GRAY)
            label = Text(year, font_size=14)
            label.next_to(dot, DOWN, buff=0.1)
            self.play(FadeIn(dot), FadeIn(label), run_time=0.2)
        
        # Highlight major changes
        change_2014 = VGroup(
            Text("V6 Hybrid Era", font_size=16, color=ELO_RED),
            Text("Complete reset", font_size=12, color=TEXT_GRAY)
        )
        change_2014.arrange(DOWN, buff=0.05)
        change_2014.move_to(timeline.get_center() + RIGHT * (-1) + UP * 0.8)
        
        change_2022 = VGroup(
            Text("Ground Effect Era", font_size=16, color=ELO_RED),
            Text("Complete reset", font_size=12, color=TEXT_GRAY)
        )
        change_2022.arrange(DOWN, buff=0.05)
        change_2022.move_to(timeline.get_center() + RIGHT * 3 + UP * 0.8)
        
        self.play(FadeIn(change_2014), FadeIn(change_2022), run_time=0.8)
        
        # Variance inflation
        inflation_formula = MathTex(
            r"\sigma_\beta^2 \uparrow \uparrow",
            font_size=36,
            color=ELO_RED
        )
        inflation_formula.move_to(DOWN * 1)
        
        inflation_text = Text(
            "Prior variance 'inflates' → Model relies more on new data",
            font_size=20,
            color=TEXT_LIGHT
        )
        inflation_text.next_to(inflation_formula, DOWN, buff=0.3)
        
        self.play(Write(inflation_formula), Write(inflation_text), run_time=1.5)
        
        # Caption
        caption = Text(
            "New regulations = New game → Less trust in historical performance",
            font_size=18,
            color=ELO_GOLD
        )
        caption.to_edge(DOWN, buff=0.4)
        
        self.play(Write(caption), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene10_6_ThurstoneMosteller(Scene):
    """Scene 10.6: Thurstone-Mosteller Approximation."""
    
    def construct(self):
        self.camera.background_color = DARK_BG
        
        header = Text("Thurstone-Mosteller Model", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)
        
        # Core assumption
        assumption = MathTex(
            r"P_i \sim \mathcal{N}(s_i, \sigma^2)",
            font_size=36
        )
        assumption.move_to(UP * 1)
        
        assumption_text = Text(
            "Performance drawn from Gaussian centered on skill",
            font_size=20,
            color=TEXT_LIGHT
        )
        assumption_text.next_to(assumption, DOWN, buff=0.2)
        
        self.play(Write(assumption), FadeIn(assumption_text), run_time=1.5)
        
        # Comparison
        comparison = MathTex(
            r"P(i > j) \approx \Phi\left(\frac{s_i - s_j}{\sigma\sqrt{2}}\right)",
            font_size=32
        )
        comparison.move_to(DOWN * 0.5)
        
        self.play(Write(comparison), run_time=1)
        
        # Benefit
        benefit = VGroup(
            Text("Why useful?", font_size=22, color=ELO_GOLD),
            Text("• Enables Expectation Propagation", font_size=18, color=TEXT_GRAY),
            Text("• Fast approximate inference", font_size=18, color=TEXT_GRAY),
            Text("• Gaussian messages → Easy to combine", font_size=18, color=TEXT_GRAY)
        )
        benefit.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        benefit.move_to(DOWN * 2)
        
        self.play(FadeIn(benefit), run_time=1)
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene10_1a_ExplainHierarchical(Scene):
    """Scene 10.1a: Decomposing Performance λ = α + β + γ + ε."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("Decomposing Performance", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"\lambda_{ijr}", r"=", r"\alpha_i", r"+", r"\beta_j", r"+",
            r"\gamma_{ij}", r"+", r"\varepsilon_{ijr}",
            font_size=44
        )
        formula[2].set_color(ELO_BLUE)      # alpha
        formula[4].set_color(ELO_GOLD)      # beta
        formula[6].set_color(ELO_GREEN)     # gamma
        formula[8].set_color(ELO_PURPLE)    # epsilon
        formula.move_to(UP * 1.5)
        self.play(Write(formula), run_time=1.5)

        # Show each component with icon/description
        components = [
            (r"\alpha_i", "Driver Skill", "How good is the DRIVER?", ELO_BLUE, "🏎️"),
            (r"\beta_j", "Car Strength", "How good is the CAR?", ELO_GOLD, "🔧"),
            (r"\gamma_{ij}", "Track Fit", "How well does driver suit this track?", ELO_GREEN, "🏁"),
            (r"\varepsilon_{ijr}", "Random Noise", "Luck, weather, incidents", ELO_PURPLE, "🎲"),
        ]

        comp_group = VGroup()
        for math_str, title, desc, color, icon in components:
            row = VGroup(
                MathTex(math_str, font_size=28, color=color),
                Text(f"  {title}", font_size=18, color=color),
                Text(desc, font_size=14, color=TEXT_GRAY)
            )
            row.arrange(RIGHT, buff=0.3)
            comp_group.add(row)

        comp_group.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        comp_group.move_to(DOWN * 0.3)

        for comp in comp_group:
            self.play(FadeIn(comp), run_time=0.6)

        self.wait(0.5)

        # Worked example
        self.play(FadeOut(comp_group), run_time=0.3)

        example = VGroup(
            Text("Example: Hamilton at Silverstone 2020", font_size=22, color=ELO_GOLD),
            MathTex(r"\alpha_{\text{HAM}} = 90", font_size=22, color=ELO_BLUE),
            MathTex(r"\beta_{\text{Mercedes}} = 80", font_size=22, color=ELO_GOLD),
            MathTex(r"\gamma_{\text{HAM,Silverstone}} = 15", font_size=22, color=ELO_GREEN),
            MathTex(r"\varepsilon = -3", font_size=22, color=ELO_PURPLE),
            MathTex(r"\lambda = 90 + 80 + 15 + (-3) = 182", font_size=28, color=TEXT_WHITE),
        )
        example.arrange(DOWN, buff=0.15)
        example.move_to(DOWN * 0.8)

        for line in example:
            self.play(FadeIn(line), run_time=0.4)
        
        box = SurroundingRectangle(example[-1], color=ELO_GREEN, buff=0.1)
        self.play(Create(box), run_time=0.5)

        takeaway = Text(
            "Separating these lets us credit driver skill vs car advantage",
            font_size=18, color=ELO_GOLD
        )
        takeaway.to_edge(DOWN, buff=0.3)
        self.play(Write(takeaway), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene10_4a_ExplainAutoregressive(Scene):
    """Scene 10.4a: How Car Strength Drifts Over Time."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("How Car Strength Drifts Over Time", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        formula = MathTex(
            r"\beta_j^{(t)}", r"\sim", r"\mathcal{N}", r"(",
            r"\beta_j^{(t-1)}", r",", r"\sigma_\beta^2", r")",
            font_size=44
        )
        formula[0].set_color(ELO_GOLD)
        formula[4].set_color(ELO_BLUE)
        formula[6].set_color(ELO_RED)
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=1.5)

        # Translation
        transl = VGroup(
            Text("In words:", font_size=20, color=ELO_GOLD),
            Text("Next season's car ≈ this season's car + random drift", font_size=18, color=TEXT_GRAY),
        )
        transl.arrange(DOWN, buff=0.1)
        transl.move_to(UP * 0.3)
        self.play(FadeIn(transl), run_time=0.5)

        # σ_β explanation
        sigma_explain = VGroup(
            MathTex(r"\sigma_\beta^2", font_size=28, color=ELO_RED),
            Text("controls how MUCH can change per season:", font_size=16, color=TEXT_GRAY),
        )
        sigma_explain.arrange(RIGHT, buff=0.3)
        sigma_explain.move_to(DOWN * 0.5)
        self.play(FadeIn(sigma_explain), run_time=0.5)

        # Two examples
        examples = VGroup(
            VGroup(
                Text("Small σ²_β: gradual evolution", font_size=16, color=ELO_GREEN),
                Text("e.g., Mercedes 2014–2020", font_size=14, color=TEXT_GRAY)
            ),
            VGroup(
                Text("Large σ²_β: sudden shifts", font_size=16, color=ELO_RED),
                Text("e.g., regulation changes", font_size=14, color=TEXT_GRAY)
            ),
        )
        for ex in examples:
            ex.arrange(DOWN, buff=0.06)
        examples.arrange(RIGHT, buff=2)
        examples.move_to(DOWN * 1.3)
        self.play(FadeIn(examples), run_time=0.8)

        # Random walk animation
        self.play(*[FadeOut(m) for m in [transl, sigma_explain, examples, formula]], run_time=0.3)

        rw_title = Text("Random Walk: Car Strength Over Seasons", font_size=22, color=ELO_GOLD)
        rw_title.next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(rw_title), run_time=0.3)

        axes = Axes(
            x_range=[2014, 2024, 2], y_range=[60, 100, 10],
            x_length=10, y_length=3.5, tips=False,
            axis_config={"include_numbers": True, "font_size": 10}
        )
        axes.move_to(DOWN * 0.5)

        x_label = Text("Season", font_size=12, color=TEXT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.15)
        y_label = Text("Car Strength β", font_size=12, color=TEXT_GRAY)
        y_label.next_to(axes.y_axis, LEFT, buff=0.1)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.5)

        # Small drift (Mercedes-like)
        merc_ratings = [92, 93, 91, 90, 88, 89, 87, 86, 78, 85]
        merc_line = VMobject(color=ELO_GREEN)
        merc_pts = [axes.c2p(2014 + i, r) for i, r in enumerate(merc_ratings)]
        merc_line.set_points_smoothly(merc_pts)
        merc_label = Text("Mercedes (small σ²)", font_size=12, color=ELO_GREEN)
        merc_label.move_to(axes.c2p(2023, 87))

        # Large drift (regulation-affected team)
        reg_ratings = [70, 72, 71, 68, 65, 80, 85, 90, 88, 92]
        reg_line = VMobject(color=ELO_RED)
        reg_pts = [axes.c2p(2014 + i, r) for i, r in enumerate(reg_ratings)]
        reg_line.set_points_smoothly(reg_pts)
        reg_label = Text("Red Bull (large σ²)", font_size=12, color=ELO_RED)
        reg_label.move_to(axes.c2p(2023, 93))

        self.play(Create(merc_line), FadeIn(merc_label), run_time=1.5)
        self.play(Create(reg_line), FadeIn(reg_label), run_time=1.5)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)


class Scene10_6a_ExplainThurstone(Scene):
    """Scene 10.6a: The Gaussian Shortcut (Thurstone-Mosteller)."""

    def construct(self):
        self.camera.background_color = DARK_BG

        header = Text("The Gaussian Shortcut", font_size=44, color=ELO_BLUE)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=1)

        # Formula
        formula = MathTex(
            r"P(i > j) \approx \Phi\left(\frac{s_i - s_j}{\sigma\sqrt{2}}\right)",
            font_size=40
        )
        formula.move_to(UP * 1.3)
        self.play(Write(formula), run_time=1.5)

        # Step-by-step derivation
        steps = VGroup(
            MathTex(r"P_i \sim \mathcal{N}(s_i, \sigma^2)", font_size=24, color=TEXT_WHITE),
            Text("Each performance is a random draw", font_size=14, color=TEXT_GRAY),
            MathTex(r"P_i - P_j \sim \mathcal{N}(s_i - s_j, 2\sigma^2)", font_size=24, color=ELO_GOLD),
            Text("Difference of normals is also normal", font_size=14, color=TEXT_GRAY),
            MathTex(r"P(i > j) = P(P_i - P_j > 0) = \Phi\left(\frac{s_i-s_j}{\sigma\sqrt{2}}\right)", font_size=24, color=ELO_GREEN),
            Text("Standard Gaussian CDF calculation", font_size=14, color=TEXT_GRAY),
        )
        steps.arrange(DOWN, buff=0.15)
        steps.move_to(DOWN * 0.5)

        for i in range(0, len(steps), 2):
            self.play(FadeIn(steps[i]), FadeIn(steps[i+1]), run_time=0.8)
            self.wait(0.3)

        # Why useful?
        self.play(*[FadeOut(m) for m in [steps, formula]], run_time=0.3)

        why = VGroup(
            Text("Why Use This Approximation?", font_size=24, color=ELO_GOLD),
            Text("• Gaussian messages are computationally cheap", font_size=16, color=TEXT_GRAY),
            Text("• Products of Gaussians remain Gaussian", font_size=16, color=TEXT_GRAY),
            Text("• Φ (probit) ≈ σ (sigmoid) — nearly identical curves!", font_size=16, color=ELO_GREEN),
        )
        why.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        why.move_to(ORIGIN)
        self.play(FadeIn(why), run_time=1)

        takeaway = Text(
            "The probit approximation makes Bayesian updates tractable",
            font_size=18, color=ELO_GOLD
        )
        takeaway.to_edge(DOWN, buff=0.3)
        self.play(Write(takeaway), run_time=1)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
