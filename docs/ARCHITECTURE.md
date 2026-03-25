# ChartForge Architecture

## Overview

ChartForge is a zero-dependency SVG chart generator built in Python. It produces clean, standards-compliant SVG markup directly from data — no rendering engine, browser, or image processing library required.

## Module Structure

```
src/chartforge/
├── __init__.py      # Public API exports
├── config.py        # Pydantic configuration models
├── core.py          # ChartForge main class with chart methods
└── utils.py         # SVG helpers, math utilities, color palettes
```

## Design Principles

### 1. No External Rendering Dependencies

All chart output is pure SVG XML strings. The only runtime dependency is `pydantic` for configuration validation. This means charts can be:

- Embedded directly in HTML
- Saved as `.svg` files
- Rendered in any SVG-capable viewer
- Processed by downstream tools

### 2. Builder Pattern

The `ChartForge` class uses a builder-style API:

```python
chart = ChartForge()
chart.set_size(800, 600)
chart.set_colors(["#FF0000", "#00FF00"])
chart.bar_chart(data, labels, title)
chart.add_legend()
chart.save("output.svg")
```

Each chart method generates the SVG internally. Configuration methods (`set_size`, `set_colors`) modify state before generation. Post-generation methods (`add_legend`, `save`, `to_svg`) operate on the generated SVG.

### 3. Configuration via Pydantic

`ChartConfig` validates all chart parameters:

- Dimensions (width, height) with sensible defaults
- Color palettes with fallback defaults
- Padding and margin values
- Font settings

### 4. SVG Generation

SVG elements are built using helper functions in `utils.py`:

- `svg_rect()` — rectangles for bar charts
- `svg_circle()` — circles for pie/donut
- `svg_line()` / `svg_polyline()` — lines for line charts
- `svg_text()` — labels and titles
- `svg_path()` — arcs for pie/donut slices
- `polar_to_cartesian()` — coordinate math for circular charts

## Data Flow

```
Input Data (lists)
    │
    ▼
ChartConfig (validated)
    │
    ▼
Chart Method (bar/line/pie/donut)
    │
    ├── Compute layout (scaling, positions)
    ├── Generate SVG elements via utils
    └── Compose into full SVG document
    │
    ▼
SVG String (stored in self._svg)
    │
    ├── to_svg() → return string
    ├── save(path) → write to file
    └── add_legend() → append legend group
```

## Coordinate System

SVG uses a top-left origin with Y increasing downward. ChartForge accounts for this:

- **Bar charts**: Bars grow upward from the baseline by computing `y = baseline - bar_height`
- **Line charts**: Data points are mapped with inverted Y
- **Pie/Donut charts**: Use polar coordinates converted to Cartesian with `polar_to_cartesian()`

## Extending with New Chart Types

To add a new chart type:

1. Add a method to `ChartForge` in `core.py`
2. Add any needed SVG primitives to `utils.py`
3. The method should populate `self._svg` with the complete SVG document
4. Write tests verifying the SVG contains expected elements
