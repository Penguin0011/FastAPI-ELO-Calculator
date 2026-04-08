# Custom animation helpers for 3Blue1Brown-style effects

from manim import *
import numpy as np


def create_title_card(title_text, subtitle_text=None, title_color="#1C758A"):
    """Create a 3B1B-style title card."""
    title = Text(title_text, font_size=56, color=title_color)
    if subtitle_text:
        subtitle = Text(subtitle_text, font_size=32, color="#888888")
        subtitle.next_to(title, DOWN, buff=0.4)
        return VGroup(title, subtitle)
    return title


def formula_highlight(formula, indices, color="#F4A261"):
    """Highlight specific parts of a formula."""
    for idx in indices:
        if idx < len(formula):
            formula[idx].set_color(color)
    return formula


def create_brace_label(mobject, text, direction=DOWN, color="#888888"):
    """Create a brace with label below/above a mobject."""
    brace = Brace(mobject, direction, color=color)
    label = brace.get_text(text, font_size=24)
    label.set_color(color)
    return VGroup(brace, label)


def create_number_line_scale(min_val, max_val, length=10, include_ticks=True):
    """Create a horizontal number line for rating visualizations."""
    line = NumberLine(
        x_range=[min_val, max_val, (max_val - min_val) / 10],
        length=length,
        include_ticks=include_ticks,
        include_numbers=True,
        font_size=20
    )
    return line


def create_rating_bar(value, max_value=3000, width=0.5, height=4, 
                      fill_color="#1C758A", bg_color="#333333"):
    """Create a vertical bar chart element for ratings."""
    bg = Rectangle(width=width, height=height, fill_color=bg_color, 
                   fill_opacity=0.3, stroke_width=0)
    filled_height = (value / max_value) * height
    bar = Rectangle(width=width, height=filled_height, 
                    fill_color=fill_color, fill_opacity=0.8, stroke_width=0)
    bar.align_to(bg, DOWN)
    return VGroup(bg, bar)


def create_bell_curve(mean=0, std=1, x_range=(-4, 4), color="#1C758A"):
    """Create a normal distribution bell curve."""
    axes = Axes(
        x_range=[x_range[0], x_range[1], 1],
        y_range=[0, 0.5, 0.1],
        x_length=8,
        y_length=4,
        tips=False
    )
    
    def normal_pdf(x):
        return (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)
    
    curve = axes.plot(normal_pdf, x_range=x_range, color=color)
    return VGroup(axes, curve)


def create_sigmoid_curve(x_range=(-6, 6), color="#1C758A"):
    """Create a sigmoid (logistic) curve for Elo probabilities."""
    axes = Axes(
        x_range=[x_range[0], x_range[1], 2],
        y_range=[0, 1, 0.25],
        x_length=8,
        y_length=4,
        tips=False,
        axis_config={"include_numbers": True}
    )
    
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
    
    curve = axes.plot(sigmoid, x_range=x_range, color=color)
    return VGroup(axes, curve)


def create_comparison_arrow(start, end, label_text, color="#83C167"):
    """Create an arrow with label for comparisons."""
    arrow = Arrow(start, end, color=color, buff=0.1)
    label = Text(label_text, font_size=20, color=color)
    label.next_to(arrow, UP, buff=0.1)
    return VGroup(arrow, label)


def animate_value_change(value_tracker, start, end, run_time=2):
    """Create animation for smoothly changing a value."""
    return value_tracker.animate(run_time=run_time).set_value(end)


def create_stacked_bars(values, labels, colors, bar_width=1, total_height=4):
    """Create stacked bar chart for component decomposition."""
    total = sum(values)
    bars = VGroup()
    current_bottom = -total_height / 2
    
    for i, (val, label, color) in enumerate(zip(values, labels, colors)):
        height = (val / total) * total_height
        bar = Rectangle(
            width=bar_width, 
            height=height,
            fill_color=color,
            fill_opacity=0.8,
            stroke_width=1,
            stroke_color=WHITE
        )
        bar.move_to([0, current_bottom + height/2, 0])
        
        text = Text(label, font_size=16, color=WHITE)
        text.move_to(bar)
        
        bars.add(VGroup(bar, text))
        current_bottom += height
    
    return bars


def create_flow_arrow(start, end, color="#888888", curved=False):
    """Create flow diagram arrow."""
    if curved:
        return CurvedArrow(start, end, color=color)
    return Arrow(start, end, color=color, buff=0.2)


def create_labeled_dot(position, label, color="#1C758A", label_direction=UP):
    """Create a dot with label for highlighting points on graphs."""
    dot = Dot(position, color=color, radius=0.08)
    text = Text(label, font_size=18, color=color)
    text.next_to(dot, label_direction, buff=0.15)
    return VGroup(dot, text)


def create_grid_overlay(rows, cols, width=8, height=6, color="#333333"):
    """Create a grid overlay for probability visualizations."""
    grid = VGroup()
    cell_width = width / cols
    cell_height = height / rows
    
    for i in range(rows):
        for j in range(cols):
            cell = Rectangle(
                width=cell_width,
                height=cell_height,
                stroke_color=color,
                stroke_width=1,
                fill_opacity=0
            )
            cell.move_to([
                -width/2 + cell_width/2 + j * cell_width,
                height/2 - cell_height/2 - i * cell_height,
                0
            ])
            grid.add(cell)
    
    return grid
