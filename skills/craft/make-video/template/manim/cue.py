"""How long a Manim scene waits for a word. Pure, so it is tested without Manim installed."""
FPS = 30
LATE = 3 / FPS  # A change up to 0.1s after its word still reads as on the word; one real voice ran a cue 1 frame late


def wait_for(now, target, where):
    """Seconds to wait from `now` to `target`, 0 when within a frame. Raises when the scene is more than LATE behind."""
    late = now - target
    if late > LATE + 1e-9:
        raise ValueError(f"{where} is spoken at {target:.2f}s, but the animation before it runs to {now:.2f}s. Shorten that animation by {late:.2f}s.")
    return target - now if target - now >= 1 / FPS else 0
