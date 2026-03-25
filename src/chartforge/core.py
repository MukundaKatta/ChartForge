"""Core ChartForge class — SVG chart generation engine."""

from __future__ import annotations

import os
from typing import Sequence

from chartforge.config import ChartConfig, DEFAULT_PALETTE
from chartforge.utils import (
    arc_path,
    color_at,
    nice_ticks,
    svg_circle,
    svg_close,
    svg_line,
    svg_open,
    svg_path,
    svg_polyline,
    svg_rect,
    svg_text,
)


class ChartForge:
    """SVG chart generator.

    Generates bar, line, pie, and donut charts as clean SVG strings
    from simple Python data structures.

    Usage:
        chart = ChartForge()
        chart.bar_chart([10, 20, 30], ["A", "B", "C"], "My Chart")
        chart.save("chart.svg")
    """

    def __init__(self, config: ChartConfig | None = None) -> None:
        self._config = config or ChartConfig()
        self._svg: str = ""
        self._labels: list[str] = []
        self._data: list[float] = []
        self._title: str = ""
        self._chart_type: str = ""

    # -- Configuration methods --

    def set_colors(self, palette: list[str] | Sequence[str]) -> "ChartForge":
        """Set a custom color palette."""
        self._config.palette = list(palette)
        return self

    def set_size(self, width: int, height: int) -> "ChartForge":
        """Set chart dimensions."""
        self._config.width = width
        self._config.height = height
        return self

    # -- Chart generators --

    def bar_chart(
        self,
        data: list[float] | list[int],
        labels: list[str],
        title: str = "",
    ) -> str:
        """Generate a bar chart SVG.

        Args:
            data: Numeric values for each bar.
            labels: Label for each bar.
            title: Optional chart title.

        Returns:
            Complete SVG string.
        """
        cfg = self._config
        self._store_meta(data, labels, title, "bar")

        w, h = cfg.width, cfg.height
        pad = cfg.padding
        chart_left = pad + 40  # room for Y-axis labels
        chart_right = w - pad
        chart_top = pad + (30 if title else 0)
        chart_bottom = h - pad - 20  # room for X-axis labels

        chart_w = chart_right - chart_left
        chart_h = chart_bottom - chart_top

        n = len(data)
        if n == 0:
            self._svg = svg_open(w, h, cfg.background_color) + svg_close()
            return self._svg

        max_val = max(max(data), 0.001)
        ticks = nice_ticks(0, max_val)
        tick_max = ticks[-1] if ticks else max_val

        svg = svg_open(w, h, cfg.background_color)

        # Title
        if title:
            svg += svg_text(
                w / 2, pad, title,
                font_size=cfg.title_font_size,
                font_family=cfg.font_family,
                weight="bold",
            )

        # Grid lines and Y-axis labels
        if cfg.show_grid:
            for tick in ticks:
                y = chart_bottom - (tick / tick_max) * chart_h
                svg += svg_line(chart_left, y, chart_right, y, stroke="#E0E0E0")
                svg += svg_text(
                    chart_left - 8, y + 4, self._fmt_num(tick),
                    font_size=cfg.label_font_size,
                    font_family=cfg.font_family,
                    anchor="end",
                    fill="#666666",
                )

        # Baseline
        svg += svg_line(chart_left, chart_bottom, chart_right, chart_bottom, stroke="#999999")

        # Bars
        bar_total_width = chart_w / n
        gap = bar_total_width * cfg.bar_gap
        bar_width = bar_total_width - gap

        for i, val in enumerate(data):
            bar_h = (val / tick_max) * chart_h
            x = chart_left + i * bar_total_width + gap / 2
            y = chart_bottom - bar_h
            color = color_at(cfg.palette, i)

            svg += svg_rect(x, y, bar_width, bar_h, fill=color, rx=2)

            # Value label above bar
            svg += svg_text(
                x + bar_width / 2, y - 6, self._fmt_num(val),
                font_size=cfg.label_font_size - 1,
                font_family=cfg.font_family,
                fill="#444444",
            )

            # X-axis label
            svg += svg_text(
                x + bar_width / 2, chart_bottom + 16, labels[i] if i < len(labels) else "",
                font_size=cfg.label_font_size,
                font_family=cfg.font_family,
                fill="#444444",
            )

        svg += svg_close()
        self._svg = svg
        return svg

    def line_chart(
        self,
        data: list[float] | list[int],
        labels: list[str],
        title: str = "",
    ) -> str:
        """Generate a line chart SVG.

        Args:
            data: Numeric values for each point.
            labels: Label for each point on the X-axis.
            title: Optional chart title.

        Returns:
            Complete SVG string.
        """
        cfg = self._config
        self._store_meta(data, labels, title, "line")

        w, h = cfg.width, cfg.height
        pad = cfg.padding
        chart_left = pad + 40
        chart_right = w - pad
        chart_top = pad + (30 if title else 0)
        chart_bottom = h - pad - 20

        chart_w = chart_right - chart_left
        chart_h = chart_bottom - chart_top

        n = len(data)
        if n == 0:
            self._svg = svg_open(w, h, cfg.background_color) + svg_close()
            return self._svg

        max_val = max(max(data), 0.001)
        min_val = min(min(data), 0)
        ticks = nice_ticks(min_val, max_val)
        tick_min = ticks[0] if ticks else min_val
        tick_max = ticks[-1] if ticks else max_val
        tick_range = tick_max - tick_min if tick_max != tick_min else 1

        svg = svg_open(w, h, cfg.background_color)

        # Title
        if title:
            svg += svg_text(
                w / 2, pad, title,
                font_size=cfg.title_font_size,
                font_family=cfg.font_family,
                weight="bold",
            )

        # Grid lines and Y-axis labels
        if cfg.show_grid:
            for tick in ticks:
                y = chart_bottom - ((tick - tick_min) / tick_range) * chart_h
                svg += svg_line(chart_left, y, chart_right, y, stroke="#E0E0E0")
                svg += svg_text(
                    chart_left - 8, y + 4, self._fmt_num(tick),
                    font_size=cfg.label_font_size,
                    font_family=cfg.font_family,
                    anchor="end",
                    fill="#666666",
                )

        # Baseline
        svg += svg_line(chart_left, chart_bottom, chart_right, chart_bottom, stroke="#999999")

        # Compute points
        points: list[tuple[float, float]] = []
        step = chart_w / max(n - 1, 1)
        for i, val in enumerate(data):
            x = chart_left + i * step
            y = chart_bottom - ((val - tick_min) / tick_range) * chart_h
            points.append((x, y))

        # Line
        line_color = color_at(cfg.palette, 0)
        svg += svg_polyline(points, stroke=line_color, stroke_width=2.5)

        # Data points and labels
        for i, (px, py) in enumerate(points):
            svg += svg_circle(px, py, 4, fill=line_color)

            # X-axis label
            svg += svg_text(
                px, chart_bottom + 16, labels[i] if i < len(labels) else "",
                font_size=cfg.label_font_size,
                font_family=cfg.font_family,
                fill="#444444",
            )

        svg += svg_close()
        self._svg = svg
        return svg

    def pie_chart(
        self,
        data: list[float] | list[int],
        labels: list[str],
        title: str = "",
    ) -> str:
        """Generate a pie chart SVG.

        Args:
            data: Numeric values for each slice.
            labels: Label for each slice.
            title: Optional chart title.

        Returns:
            Complete SVG string.
        """
        return self._circular_chart(data, labels, title, chart_type="pie")

    def donut_chart(
        self,
        data: list[float] | list[int],
        labels: list[str],
        title: str = "",
    ) -> str:
        """Generate a donut chart SVG.

        Args:
            data: Numeric values for each slice.
            labels: Label for each slice.
            title: Optional chart title.

        Returns:
            Complete SVG string.
        """
        return self._circular_chart(data, labels, title, chart_type="donut")

    def _circular_chart(
        self,
        data: list[float] | list[int],
        labels: list[str],
        title: str,
        chart_type: str,
    ) -> str:
        """Internal method for pie and donut charts."""
        cfg = self._config
        self._store_meta(data, labels, title, chart_type)

        w, h = cfg.width, cfg.height
        pad = cfg.padding
        title_offset = 30 if title else 0

        n = len(data)
        total = sum(data)
        if n == 0 or total == 0:
            self._svg = svg_open(w, h, cfg.background_color) + svg_close()
            return self._svg

        cx = w / 2
        cy = (h + title_offset) / 2
        radius = min(w - 2 * pad, h - 2 * pad - title_offset) / 2 * 0.85
        inner_radius = radius * 0.55 if chart_type == "donut" else 0

        svg = svg_open(w, h, cfg.background_color)

        # Title
        if title:
            svg += svg_text(
                w / 2, pad, title,
                font_size=cfg.title_font_size,
                font_family=cfg.font_family,
                weight="bold",
            )

        # Slices
        angle = 0.0
        for i, val in enumerate(data):
            sweep = (val / total) * 360
            if sweep < 0.1:
                angle += sweep
                continue

            color = color_at(cfg.palette, i)
            path_d = arc_path(cx, cy, radius, angle, angle + sweep, inner_radius)
            svg += svg_path(path_d, fill=color, stroke="#FFFFFF", stroke_width=2)

            # Slice label (placed at midpoint angle)
            from chartforge.utils import polar_to_cartesian

            label_radius = radius * 0.7 if inner_radius == 0 else (radius + inner_radius) / 2
            mid_angle = angle + sweep / 2
            lx, ly = polar_to_cartesian(cx, cy, label_radius, mid_angle)

            pct = val / total * 100
            if sweep > 15:  # Only label slices large enough
                svg += svg_text(
                    lx, ly + 4,
                    f"{pct:.0f}%",
                    font_size=cfg.label_font_size,
                    font_family=cfg.font_family,
                    fill="#FFFFFF",
                    weight="bold",
                )

            angle += sweep

        svg += svg_close()
        self._svg = svg
        return svg

    # -- Output methods --

    def to_svg(self) -> str:
        """Return the current SVG string."""
        return self._svg

    def save(self, path: str) -> None:
        """Save the current SVG to a file.

        Args:
            path: File path to write the SVG to.
        """
        if not self._svg:
            raise ValueError("No chart has been generated yet. Call a chart method first.")
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self._svg)

    def add_legend(self) -> str:
        """Append a legend to the current SVG.

        Returns:
            Updated SVG string with legend included.
        """
        if not self._svg or not self._labels:
            return self._svg

        cfg = self._config
        # Insert legend before closing </svg> tag
        legend_y_start = cfg.height - cfg.padding + 10
        legend_x = cfg.padding + 40

        legend = ""
        for i, label in enumerate(self._labels):
            color = color_at(cfg.palette, i)
            lx = legend_x + (i % 4) * 160
            ly = legend_y_start + (i // 4) * 20

            legend += svg_rect(lx, ly - 8, 12, 12, fill=color, rx=2)
            legend += svg_text(
                lx + 18, ly + 3, label,
                font_size=cfg.label_font_size,
                font_family=cfg.font_family,
                anchor="start",
                fill="#444444",
            )

        # Insert before </svg>
        self._svg = self._svg.replace("</svg>", legend + "</svg>")
        return self._svg

    # -- Private helpers --

    def _store_meta(
        self,
        data: list[float] | list[int],
        labels: list[str],
        title: str,
        chart_type: str,
    ) -> None:
        """Store chart metadata for legend generation and other post-processing."""
        self._data = [float(v) for v in data]
        self._labels = list(labels)
        self._title = title
        self._chart_type = chart_type

    @staticmethod
    def _fmt_num(val: float) -> str:
        """Format a number for display — drop trailing .0 for integers."""
        if val == int(val):
            return str(int(val))
        return f"{val:.1f}"
