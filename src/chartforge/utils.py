"""SVG helper functions, color palettes, coordinate math, and path generation."""

import math
from xml.sax.saxutils import escape


def svg_open(width: int, height: int, background: str = "#FFFFFF") -> str:
    """Generate the opening SVG tag with viewBox and background."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">\n'
        f'  <rect width="{width}" height="{height}" fill="{escape(background)}" />\n'
    )


def svg_close() -> str:
    """Generate the closing SVG tag."""
    return "</svg>\n"


def svg_rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    rx: float = 0,
    opacity: float = 1.0,
) -> str:
    """Generate an SVG rectangle element."""
    parts = [
        f'  <rect x="{x:.1f}" y="{y:.1f}" '
        f'width="{width:.1f}" height="{height:.1f}" '
        f'fill="{escape(fill)}"'
    ]
    if rx > 0:
        parts[0] += f' rx="{rx:.1f}"'
    if opacity < 1.0:
        parts[0] += f' opacity="{opacity:.2f}"'
    parts[0] += " />\n"
    return parts[0]


def svg_circle(cx: float, cy: float, r: float, fill: str, opacity: float = 1.0) -> str:
    """Generate an SVG circle element."""
    s = f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{escape(fill)}"'
    if opacity < 1.0:
        s += f' opacity="{opacity:.2f}"'
    s += " />\n"
    return s


def svg_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str = "#CCCCCC",
    stroke_width: float = 1.0,
    dash: str | None = None,
) -> str:
    """Generate an SVG line element."""
    s = (
        f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{escape(stroke)}" stroke-width="{stroke_width:.1f}"'
    )
    if dash:
        s += f' stroke-dasharray="{dash}"'
    s += " />\n"
    return s


def svg_polyline(points: list[tuple[float, float]], stroke: str, stroke_width: float = 2.0) -> str:
    """Generate an SVG polyline element."""
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'  <polyline points="{pts}" fill="none" '
        f'stroke="{escape(stroke)}" stroke-width="{stroke_width:.1f}" '
        f'stroke-linejoin="round" stroke-linecap="round" />\n'
    )


def svg_text(
    x: float,
    y: float,
    text: str,
    font_size: int = 12,
    font_family: str = "Arial, Helvetica, sans-serif",
    fill: str = "#333333",
    anchor: str = "middle",
    weight: str = "normal",
    rotate: float | None = None,
) -> str:
    """Generate an SVG text element."""
    s = (
        f'  <text x="{x:.1f}" y="{y:.1f}" '
        f'font-size="{font_size}" font-family="{escape(font_family)}" '
        f'fill="{escape(fill)}" text-anchor="{anchor}" font-weight="{weight}"'
    )
    if rotate is not None:
        s += f' transform="rotate({rotate:.1f},{x:.1f},{y:.1f})"'
    s += f">{escape(text)}</text>\n"
    return s


def svg_path(d: str, fill: str = "none", stroke: str = "none", stroke_width: float = 1.0) -> str:
    """Generate an SVG path element."""
    return (
        f'  <path d="{d}" fill="{escape(fill)}" '
        f'stroke="{escape(stroke)}" stroke-width="{stroke_width:.1f}" />\n'
    )


def svg_group(content: str, transform: str = "") -> str:
    """Wrap content in an SVG group with optional transform."""
    if transform:
        return f'  <g transform="{transform}">\n{content}  </g>\n'
    return f"  <g>\n{content}  </g>\n"


def polar_to_cartesian(
    cx: float, cy: float, radius: float, angle_deg: float
) -> tuple[float, float]:
    """Convert polar coordinates to Cartesian (SVG coordinate system)."""
    angle_rad = math.radians(angle_deg - 90)  # Start from top (12 o'clock)
    x = cx + radius * math.cos(angle_rad)
    y = cy + radius * math.sin(angle_rad)
    return x, y


def arc_path(
    cx: float,
    cy: float,
    radius: float,
    start_angle: float,
    end_angle: float,
    inner_radius: float = 0,
) -> str:
    """Generate an SVG arc path for pie/donut slices.

    Args:
        cx, cy: Center coordinates.
        radius: Outer radius.
        start_angle, end_angle: Angles in degrees (0 = top, clockwise).
        inner_radius: Inner radius for donut charts (0 for pie).

    Returns:
        SVG path data string.
    """
    start_outer = polar_to_cartesian(cx, cy, radius, start_angle)
    end_outer = polar_to_cartesian(cx, cy, radius, end_angle)

    sweep = end_angle - start_angle
    large_arc = 1 if sweep > 180 else 0

    if inner_radius > 0:
        # Donut slice
        start_inner = polar_to_cartesian(cx, cy, inner_radius, end_angle)
        end_inner = polar_to_cartesian(cx, cy, inner_radius, start_angle)

        d = (
            f"M {start_outer[0]:.2f} {start_outer[1]:.2f} "
            f"A {radius} {radius} 0 {large_arc} 1 {end_outer[0]:.2f} {end_outer[1]:.2f} "
            f"L {start_inner[0]:.2f} {start_inner[1]:.2f} "
            f"A {inner_radius} {inner_radius} 0 {large_arc} 0 "
            f"{end_inner[0]:.2f} {end_inner[1]:.2f} Z"
        )
    else:
        # Full pie slice
        d = (
            f"M {cx:.2f} {cy:.2f} "
            f"L {start_outer[0]:.2f} {start_outer[1]:.2f} "
            f"A {radius} {radius} 0 {large_arc} 1 {end_outer[0]:.2f} {end_outer[1]:.2f} Z"
        )

    return d


def scale_values(
    values: list[float], target_min: float, target_max: float
) -> list[float]:
    """Scale a list of values to a target range."""
    if not values:
        return []
    v_min = min(values)
    v_max = max(values)
    if v_max == v_min:
        mid = (target_min + target_max) / 2
        return [mid] * len(values)
    return [
        target_min + (v - v_min) / (v_max - v_min) * (target_max - target_min) for v in values
    ]


def nice_ticks(v_min: float, v_max: float, num_ticks: int = 5) -> list[float]:
    """Generate nicely rounded tick values for an axis."""
    if v_max == v_min:
        return [v_min]
    raw_step = (v_max - v_min) / num_ticks
    magnitude = 10 ** math.floor(math.log10(raw_step))
    residual = raw_step / magnitude
    if residual <= 1.5:
        nice_step = magnitude
    elif residual <= 3.0:
        nice_step = 2 * magnitude
    elif residual <= 7.0:
        nice_step = 5 * magnitude
    else:
        nice_step = 10 * magnitude

    start = math.floor(v_min / nice_step) * nice_step
    ticks: list[float] = []
    val = start
    while val <= v_max + nice_step * 0.01:
        ticks.append(round(val, 10))
        val += nice_step
    return ticks


def color_at(palette: list[str], index: int) -> str:
    """Get a color from the palette, cycling if needed."""
    return palette[index % len(palette)]
