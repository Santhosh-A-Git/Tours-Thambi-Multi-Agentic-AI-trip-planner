---
name: Aetheric Voyage
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#debec8'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#a68992'
  outline-variant: '#574048'
  surface-tint: '#ffb0cd'
  primary: '#ffb0cd'
  on-primary: '#640039'
  primary-container: '#f751a1'
  on-primary-container: '#570032'
  inverse-primary: '#b4136d'
  secondary: '#ddb7ff'
  on-secondary: '#490080'
  secondary-container: '#6f00be'
  on-secondary-container: '#d6a9ff'
  tertiary: '#bec6e0'
  on-tertiary: '#283044'
  tertiary-container: '#8990a8'
  on-tertiary-container: '#22293d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffd9e4'
  primary-fixed-dim: '#ffb0cd'
  on-primary-fixed: '#3e0022'
  on-primary-fixed-variant: '#8c0053'
  secondary-fixed: '#f0dbff'
  secondary-fixed-dim: '#ddb7ff'
  on-secondary-fixed: '#2c0051'
  on-secondary-fixed-variant: '#6900b3'
  tertiary-fixed: '#dae2fd'
  tertiary-fixed-dim: '#bec6e0'
  on-tertiary-fixed: '#131b2e'
  on-tertiary-fixed-variant: '#3f465c'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.05em
  subtitle-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style

The design system is engineered for a state-of-the-art AI trip planning experience. It targets sophisticated travelers and tech-forward users who value efficiency and a high-tech aesthetic. The visual narrative is rooted in a futuristic "Deep Space" theme, utilizing **Glassmorphism** as its primary stylistic driver. 

By layering translucent surfaces over dark, expansive backgrounds, the UI evokes a sense of depth and advanced intelligence. The emotional response is one of awe, precision, and seamlessness—as if the user is navigating a celestial navigation system powered by a super-intelligent agent.

## Colors

The color palette centers on a "Deep Space" foundation, using a spectrum of **Slate-900 (#0f172a)** to **Gray-950 (#030712)** to create an infinite, immersive backdrop. 

- **Primary & Secondary:** A vibrant gradient from **Cosmic Pink (#ec4899)** to **Electric Purple (#a855f7)** serves as the high-energy accent, used for primary actions and AI-driven insights.
- **Neutral:** A range of muted grays and slates provide balance, ensuring that information hierarchy remains clear without competing with the vibrant accents.
- **Surfaces:** Semi-transparent white and slate overlays (5% to 12% opacity) create the frosted glass effect necessary for the glassmorphism style.

## Typography

This design system utilizes **Inter** exclusively to maintain a systematic, utilitarian, yet modern feel. 

- **Headlines:** Use tighter letter spacing and bold weights to ground the UI.
- **Subtitles:** Rendered in **Slate-400 (#94a3b8)** to provide necessary context without visual clutter.
- **Micro-copy:** Labels should use increased letter-spacing for legibility against dark, blurred backgrounds.
- **Gradient Text:** For high-impact numbers or AI status updates, apply the Primary-to-Secondary gradient to display-level typography.

## Layout & Spacing

The layout philosophy follows a **Fluid Grid** model with generous safe areas to allow the "Deep Space" background to breathe. 

- **Grid:** A 12-column system for desktop, collapsing to 4 columns for mobile.
- **Rhythm:** An 8px linear scale governs all padding and margins. 
- **Panels:** Use side-sheets and floating panels for trip details to maintain the feeling of an "overlay" rather than a hard-coded page change.
- **Responsive:** On mobile, margins reduce to 16px, and glass panels should occupy full-width to maximize screen real estate while retaining background blurs on the header and navigation.

## Elevation & Depth

Depth is achieved through **optical layering** rather than traditional drop shadows.

- **The Void:** The base layer is a dark, solid or slightly radial gradient background.
- **The Veil:** Panels utilize `backdrop-filter: blur(12px)` and a subtle `1px` border with 10% white opacity.
- **Illumination:** Instead of black shadows, use "Glows." Primary buttons and active AI states should emit a soft, localized outer glow using the secondary purple color at very low opacity (15-20%).
- **Stacking:** Higher elevation levels are indicated by increased background opacity (from 5% to 15%) and sharper border definition.

## Shapes

The shape language is consistently **Rounded**, striking a balance between tech-precision and organic approachability.

- **Panels & Cards:** Use a base radius of `1rem` (16px) to maintain a soft, modern look.
- **Interactive Elements:** Buttons and input fields should follow the `0.5rem` (8px) standard for a crisp, professional appearance.
- **Avatars & Icons:** Often placed within circular containers to contrast against the rectangular grid of the trip itinerary.

## Components

### Buttons
- **Primary:** Gradient background (#ec4899 to #a855f7) with white text. Apply a `scale(1.05)` effect and an increased glow on hover.
- **Ghost:** Transparent with a `1px` border (Slate-700) and white text. Subtle blur on the background.

### Frosted Glass Cards
- Used for itinerary items and flight details. 
- `background: rgba(255, 255, 255, 0.05)`.
- `backdrop-filter: blur(16px)`.
- `border: 1px solid rgba(255, 255, 255, 0.1)`.

### Input Fields
- Dark backgrounds (Slate-950) with a 1px border that transitions to the Primary gradient when focused. 
- Placeholder text in Slate-500.

### Chips & Tags
- Used for "Fastest," "Cheapest," or "AI Recommended."
- Small, pill-shaped, with a semi-transparent purple tint and high-contrast white text.

### Progress Indicators (Agentic Pulse)
- A pulsing, blurred orb or a thin animated gradient line at the top of panels to indicate the AI "Agent" is processing data.