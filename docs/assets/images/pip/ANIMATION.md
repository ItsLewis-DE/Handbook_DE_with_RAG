# Pip animation assets

The live mascot is an inline SVG assembled in `docs/javascripts/chat.js` and styled in `docs/stylesheets/chat.css`. `pip-robot.png` is the original visual reference; `pip.json` is a legacy Lottie asset, not the active animation controller.

## Behavior

- On arrival, Pip gives a brief three-beat wave, then lowers its arm. The shoulder leads the forearm and wrist; the antenna settles after the head moves.
- Feet remain planted while the upper body breathes subtly. The ground shadow stays beneath the feet.
- A mouse within 200 CSS pixels draws Pip's gaze, with bounded head tilt and eye movement. A five-second greeting cooldown prevents repeated passes from restarting the wave. Keyboard focus also triggers a greeting.
- Starting 5 seconds after arrival or resuming, Pip opens the book and reads for 3.5 seconds. It then closes the book over 650 ms and waits a full 5 seconds before opening again (9.15 seconds between reading starts). The rest interval starts after closing, not when reading begins. This cycle runs without mouse interaction and is not postponed by pointer movement, greetings, or keyboard focus. While reading, Pip keeps its gaze on the pages. A continuous cover and shared spine join the pages, with both hands supporting the outside edges.
- Blinks occur at varied intervals, with occasional double blinks. Reading eye movement and blinking use separate SVG groups so they can coexist.
- Opening chat or hiding the browser tab clears animation timers and pauses CSS animations. Closing chat or returning to the tab resumes from a relaxed pose.
- Reduced-motion preference disables gestures, gaze tracking, blinking, and breathing, including when the preference changes while the page is open. Chat remains usable.

## Implementation

`animateMascot` owns pose and blink timers, nearby-pointer tracking, and pause/resume behavior. Pointer updates are coalesced with `requestAnimationFrame`. CSS variables carry bounded gaze offsets; SVG groups retain explicit joint origins. No external animation runtime is required by the live mascot.

The launcher uses a 93 × 116 px mascot on desktop and 77 × 96 px on mobile. Its label remains still and keyboard focus is indicated by a visible ring around the label.

**Regression check.**

After building the site, run `uv run scripts/check_pip_reading.py`. It verifies a full five-second rest after closing the book with a parked nearby pointer, restored focus after closing chat, and no interaction, plus hand placement and reduced-motion behavior.
