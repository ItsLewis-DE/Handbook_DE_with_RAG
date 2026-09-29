# Pip animation assets

The live mascot is an inline SVG assembled in `docs/javascripts/chat.js` and styled in `docs/stylesheets/chat.css`. `pip-robot.png` is the original visual reference; `pip.json` is a legacy Lottie asset, not the active animation controller.

## Behavior

- On arrival, Pip gives a brief wave with diminishing amplitude, then lowers its arm. The shoulder leads the forearm and wrist; the antenna settles after the head moves.
- Feet remain planted while the upper body breathes subtly, with pauses between breaths. During quiet intervals, Pip gently shifts its weight and counterbalances its head. The ground shadow stays beneath the feet.
- A mouse within 200 CSS pixels draws Pip's gaze, with bounded head tilt and eye movement. Eyes respond over 160 ms; the head follows after 100 ms with a slower 420 ms transition. A five-second greeting cooldown prevents repeated passes from restarting the wave. Keyboard focus also triggers a greeting.
- Starting 5 seconds after arrival or resuming, Pip lifts the book for 350 ms, then opens and reads it for 6.8 seconds. This leaves time to finish the delayed two-line eye scan. Pip looks up for 650 ms while still holding the book, then closes it and settles its arms over 1 second. A varied 5–10 second rest begins after closing. This cycle runs without mouse interaction; a greeting already in progress finishes before reading starts. During the book sequence, Pip does not start another greeting. A continuous cover and shared spine join the pages, with both hands supporting the outside edges.
- Blinks occur at varied intervals, with occasional double blinks. Reading eye movement and blinking use separate SVG groups so they can coexist.
- Opening chat or hiding the browser tab clears animation timers and pauses CSS animations. Closing chat or returning to the tab resumes from a relaxed pose.
- Reduced-motion preference disables gestures, gaze tracking, blinking, and breathing, including when the preference changes while the page is open. Chat remains usable.

## Implementation

`animateMascot` owns pose, balance, gaze, and blink timers, nearby-pointer tracking, and pause/resume behavior. Pointer updates are coalesced with `requestAnimationFrame`. CSS variables carry bounded gaze offsets; separate SVG groups isolate balance, breathing, gaze, reading scans, and blinks. Joint origins remain explicit. No external animation runtime is required by the live mascot.

The launcher uses a 93 × 116 px mascot on desktop and 77 × 96 px on mobile. Its label remains still and keyboard focus is indicated by a visible ring around the label.

**Regression check.**

After building the site, run `uv run scripts/check_pip_reading.py`. It verifies the staged reading sequence and rest after closing, with nearby and moving pointers, restored focus after closing chat, no interaction, and a mobile viewport, plus hand placement and reduced-motion behavior. Randomness is fixed during the check so the rest interval is reproducible.
