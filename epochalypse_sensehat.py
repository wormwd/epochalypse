#!/usr/bin/env python

import math
import time

from sense_hat import SenseHat

COLORS = {"black": (0, 0, 0), "red": (255, 0, 0), "blue": (0, 0, 255)}
SENSE = SenseHat()
GRADIENT_DURATION = 0.75
GRADIENT_STEPS = 20
TS_MAX = 2**32 - 1


def main():
    # Start at at the beginning of a second
    wait_until(math.floor(time.time()) + 1)
    # Initially we have nothing to transition from
    old_pixels = None
    while True:
        start = time.time()
        # Integer of the current timestamp
        now = math.floor(start)
        next_run = now + 1
        # Pixel array of current time, reversed so the least significant bit is first
        elapsed = [
            "red" if c == "1" else "black" for c in list(bin(now)[2:].zfill(32))
        ][::-1]
        # Pixel array of the inverse
        remaining = [
            "blue" if c == "1" else "black"
            for c in list(bin(TS_MAX - now)[2:].zfill(32))
        ][::-1]
        # Grid of remaining time above the current time
        new_pixels = list(COLORS[i] for i in remaining + elapsed)
        # No transition if this is the first run
        if old_pixels is None:
            old_pixels = new_pixels
        # Run transition animation
        transition(old_pixels, new_pixels)
        # Remember old state for next transition animation
        old_pixels = new_pixels
        # wait for next run
        wait_until(next_run)


def transition(before, after):
    # Loop for each gradient step
    for step in range(GRADIENT_STEPS):
        # Compute each pixel based on the old and new values and the current gradient step
        pixels = [gradient(b, a, step) for b, a in zip(before, after)]
        # Set the display for the current gradient step
        SENSE.set_pixels(pixels)
        # Pause a little bit so the animation is visible
        time.sleep(GRADIENT_DURATION / GRADIENT_STEPS)
    SENSE.set_pixels(after)


def gradient(before, after, step):
    # Calculate the gradient
    return tuple(
        [
            math.floor(before[i] * ((GRADIENT_STEPS - step) / GRADIENT_STEPS))
            + math.ceil(after[i] * (step / GRADIENT_STEPS))
            for i in range(3)
        ]
    )


def wait_until(ts):
    # Duration between current time and the target timestamp
    delay = float(ts) - time.time()
    # Wait until the target timestamp, if it is in the future
    if delay > 0:
        time.sleep(delay)


if __name__ == "__main__":
    main()