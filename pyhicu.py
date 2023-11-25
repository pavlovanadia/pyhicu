#!/usr/bin/env python3
import argparse
from enum import Enum  # you have a limited set of moves -> enum is a good concept to utilize here
import numpy as np
import matplotlib.pyplot as plt


class Move(Enum):
    """
    Enum  representing possible movement directions in a 2D space: Up, Down, Right, and Left.

    Methods:
    turn_right() and turn_left(): Return the new `Move` direction after a right or left turn.
    get_delta(): Returns the coordinate delta (change in x and y) for the given move.
    """
    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"

    def turn_right(self):
        return {
            Move.UP: Move.RIGHT,
            Move.RIGHT: Move.DOWN,
            Move.DOWN: Move.LEFT,
            Move.LEFT: Move.UP
        }[self]

    def turn_left(self):
        return {
            Move.UP: Move.LEFT,
            Move.LEFT: Move.DOWN,
            Move.DOWN: Move.RIGHT,
            Move.RIGHT: Move.UP
        }[self]

    def get_delta(self):
        return {
            Move.UP: (0, 1),
            Move.DOWN: (0, -1),
            Move.RIGHT: (1, 0),
            Move.LEFT: (-1, 0)
        }[self]


def parse_args():
    parser = argparse.ArgumentParser(
        usage="hilbert.py",
        description="Generate a Hilbert curve for a specified iteration."
    )

    parser.add_argument(
        "-i", "--iteration", default=0, type=int, help="Number of iterations (integer)"
    )
    # not sure whether it affects anything:
    parser.add_argument(
        "--fig_size", "--fs", default=6, type=int, help="Side of a picture (inches)"
    )
    parser.add_argument(
        "--dot_color", "--dc", default="#4f5152", type=str, help="Dot color (hex code or colorname)"
    )
    parser.add_argument(
        "--line_color", "--lc", default="violet", type=str, help="Line color (hex code or colorname)"
    )
    parser.add_argument(
        "--output", "-o", default="hilbert_output.png", type=str, help="Output filename"
    )

    parser.add_argument("--dot_size_factor",
                        default=1.5,
                        type=float,
                        help="Factor to adjust dot size")
    parser.add_argument("--line_width_factor",
                        default=1.5,
                        type=float,
                        help="Factor to adjust line width")
    parser.add_argument("--dpi",
                        default=300,
                        type=int,
                        help="Dots per inch for the output image")
    # You also may add some params validation
    args = parser.parse_args()
    if args.iteration < 0:
        raise ValueError("Iteration must be a non-negative integer")
    if args.fig_size <= 0:
        raise ValueError("Figure size must be a positive number")
    return args


def hilbert_core(iteration):
    """
    Recursively generates a sequence of moves to create a Hilbert curve of a given iteration.

    Returns:
    list: A sequence of `Move` enum members to draw the Hilbert curve.
    """
    if iteration == 0:
        return []
    else:
        new_iteration = iteration - 1
        previous = hilbert_core(iteration=new_iteration)
        previous_right = [move.turn_right() for move in previous]
        previous_left = [move.turn_left() for move in previous]
        return previous_right + [Move.UP] + previous + [Move.RIGHT] + previous + [Move.DOWN] + previous_left


def moves2coordinates(moves):
    """
    Converts a sequence of 'Move' enum members into a corresponding sequence of 2D coordinates.

    Returns:
    A list of coordinate tuples (x, y) representing the coordinates after each move in the sequence.
    """
    coords = [(0, 0)]

    for move in moves:
        prev = coords[-1]
        delta = move.get_delta()
        current = (prev[0] + delta[0], prev[1] + delta[1])
        coords.append(current)

    return coords


def hilbert_curve(iteration):
    """Generates a 2D NumPy array of coordinates representing a Hilbert curve of a given iteration."""
    return np.array(moves2coordinates(hilbert_core(iteration)))


def visualize_hilbert_curve(iteration, fig_size, dot_color, line_color, filename,
                            dot_size_factor=1.5, line_width_factor=1.5, dpi=300):
    """Generates and visualizes a Hilbert curve of a given iteration, saving the plot to a file."""
    plt.figure(figsize=(fig_size, fig_size))
    dot_size = 2 ** (1 / (iteration + 1)) * dot_size_factor
    coords = hilbert_curve(iteration)
    plt.plot(coords[:, 0], coords[:, 1], color=line_color, linewidth=dot_size / line_width_factor)
    plt.scatter(coords[:, 0], coords[:, 1], marker="o", color=dot_color, s=dot_size)
    plt.yticks([])
    plt.xticks([])
    try:
        plt.savefig(filename, bbox_inches="tight", pad_inches=0, dpi=dpi)
    except Exception as e:
        print(f"Error saving file: {e}")
    plt.close()


def main():
    args = parse_args()
    visualize_hilbert_curve(
        args.iteration,
        args.fig_size,
        args.dot_color,
        args.line_color,
        args.output,
        args.dot_size_factor,
        args.line_width_factor,
        args.dpi
    )


if __name__ == "__main__":
    main()
