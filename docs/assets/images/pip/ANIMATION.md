# Pip animation assets

`pip-robot.png` is the original 3D mascot reference image.
`pip.json` is the Lottie animation format containing vector paths, claymorphic gradients, skeletal keyframes, and markers (`idle`, `greeting`, `reading`).
`docs/javascripts/lottie.min.js` provides the lightweight SVG runtime for Lottie animations.

The mascot animation system uses a fluid vector puppet engine designed to eliminate the stiff "cardboard cutout" feel of 2D sliced sprites:

## Architecture & Visuals
- **Harmonic Breathing & Hovering**: The body and ground shadow float in a synchronized 3.2s sine wave.
- **Antenna Spring Physics**: The antenna wobbles naturally with delayed inertia relative to body and head motion.
- **Eye Blinking**: The smiling eyes (`^ ^`) blink realistically every 4 seconds.
- **Waving Arm (Greeting Pose)**: The right arm smoothly waves back and forth with elastic spring easing when hovered or focused.
- **Interactive Reading Pose**: When the chat panel opens, the orange book opens with visible reading pages, the head tilts down, and eyes scan back and forth across the lines.
- **Speech Bubble**: The launcher tooltip is formatted as a responsive speech bubble pointing directly at Pip with a pop-spring entrance.
- **Focus Ring Elimination**: Removed the tight rectangular `:focus-visible` outline around the launcher, replacing it with an ambient soft glow to keep Pip unconstrained.

## States
- `idle`: Smooth continuous breathing float, antenna lag wobble, periodic eye blink, breathing shadow.
- `greeting`: Head tilt, lively waving hand loop, speech bubble pop-in.
- `reading`: Relaxed pose, book opened, head tilted down reading, eyes scanning.
