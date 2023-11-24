#!/usr/bin/env python3

import argparse

import numpy as np
from itertools import product

import matplotlib.pyplot as plt


TR = {
    "u": "r",
    "r": "u",
    "d": "l",
    "l": "d",
    "": ""
}
TL = {
    "u": "l",
    "r": "d",
    "d": "r",
    "l": "u",
    "": ""
}


def parse_args():
    parser = argparse.ArgumentParser(
        usage="hilbert.py",
        description="Generate a Hilbert curve for a specified ineration."
    )

    parser.add_argument(
        "-i", "--iteration", default=0, type=int, help="Number of iterations (integer)"
    )
    parser.add_argument(
        "--fs", default=5, type=int, help="Side of a picture (inches)"
    )
    parser.add_argument(
        "--dc", default="#4f5152", type=str, help="Dot color (hex code or colorname)"
    )
    parser.add_argument(
        "--lc", default="violet", type=str, help="Line color (hex code or colorname)"
    )
    parser.add_argument(
        "-o", "--output", default="hilbert_outp.png", type=str, help="Output filename"
    )

    return parser.parse_args()


def hilbert_core(iteration=0):
    if iteration == 0:
        return ""
    else:
        new_iteration = iteration - 1
        previous = hilbert_core(iteration=new_iteration)
        previous_right = "".join([TR[mv] for mv in previous])
        previous_left = "".join([TL[mv] for mv in previous])
        return f"{previous_right}u{previous}r{previous}d{previous_left}"


def moves2cordinates(moves):
    coords = [(0, 0)]

    for move in moves:
        prev = coords[-1]

        if move == "u":
            current = (prev[0], prev[1] + 1)

        elif move == "d":
            current = (prev[0], prev[1] - 1)
        
        elif move == "r":
            current = (prev[0] + 1, prev[1])

        elif move == "l":
            current = (prev[0] - 1, prev[1])
        
        else:
            raise ValueError(f"Invalid move combination: move {move} does not exist.")
        
        coords.append(current)
    
    return coords


def hilbert_curve(iteration=0):
    return moves2cordinates(hilbert_core(iteration=iteration))


def hilbert_vis(it, fs, dc, lc, filename):
    plt.figure(figsize=(fs, fs))
    dot_size = 2 ** (1 / (it + 1))
    coords = np.array(hilbert_curve(it))
    plt.plot(coords[:, 0], coords[:, 1], c=lc, linewidth=dot_size / 1.5)
    plt.scatter(coords[:, 0], coords[:, 1], marker="o", color=dc, s=dot_size)
    plt.yticks([])
    plt.xticks([])
    plt.savefig(filename, bbox_inches="tight", pad_inches=0, dpi=300)


if __name__ == "__main__":
    args = parse_args()
    iteration = args.iteration
    figside = args.fs
    dotcol = args.dc
    linecol = args.lc
    outp = args.output

    hilbert_vis(it=iteration, fs=figside, dc=dotcol, lc=linecol, filename=outp)

