# ChartForge

[![CI](https://github.com/officethree/ChartForge/actions/workflows/ci.yml/badge.svg)](https://github.com/officethree/ChartForge/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**SVG chart generator** — a Python library that generates beautiful SVG charts from data, with zero external rendering dependencies.

Supports **bar**, **line**, **pie**, and **donut** charts out of the box.

## Architecture

```mermaid
graph TD
    A[User Data] --> B[ChartForge Core]
    B --> C{Chart Type}
    C --> D[Bar Chart]
    C --> E[Line Chart]
    C --> F[Pie Chart]
    C --> G[Donut Chart]
    D --> H[SVG Builder]
    E --> H
    F --> H
    G --> H
    H --> I[SVG String Output]
    I --> J[Save to File]
    I --> K[Inline Embedding]

    subgraph Configuration
        L[Color Palettes] --> B
        M[Size Settings] --> B
        N[ChartConfig] --> B
    end
```

## Quickstart

### Installation

```bash
pip install chartforge
```

Or install from source:

```bash
git clone https://github.com/officethree/ChartForge.git
cd ChartForge
pip install -e .
```

### Usage

```python
from chartforge import ChartForge

# Create a chart instance
chart = ChartForge()

# Generate a bar chart
svg = chart.bar_chart(
    data=[45, 72, 38, 91, 56],
    labels=["Mon", "Tue", "Wed", "Thu", "Fri"],
    title="Weekly Sales"
)

# Save to file
chart.save("weekly_sales.svg")

# Or get the raw SVG string
svg_string = chart.to_svg()
```

### More Examples

```python
from chartforge import ChartForge

cf = ChartForge()

# Line chart
cf.line_chart(
    data=[10, 25, 18, 42, 35, 60],
    labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    title="Revenue Trend"
)
cf.save("revenue.svg")

# Pie chart with custom colors
cf.set_colors(["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"])
cf.pie_chart(
    data=[35, 25, 20, 20],
    labels=["Product A", "Product B", "Product C", "Product D"],
    title="Market Share"
)
cf.save("market_share.svg")

# Donut chart
cf.donut_chart(
    data=[40, 30, 20, 10],
    labels=["Desktop", "Mobile", "Tablet", "Other"],
    title="Traffic Sources"
)
cf.add_legend()
cf.save("traffic.svg")

# Custom dimensions
cf.set_size(1200, 800)
cf.bar_chart(
    data=[88, 65, 92, 71],
    labels=["Q1", "Q2", "Q3", "Q4"],
    title="Quarterly Performance"
)
cf.save("quarterly.svg")
```

## Features

- Zero external dependencies for rendering (only `pydantic` for config validation)
- Clean, well-formed SVG output with proper `viewBox`
- Built-in color palettes with custom palette support
- Automatic scaling and label positioning
- Legend generation
- File saving and raw SVG string access

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
make test

# Lint
make lint

# Format
make format
```

## Inspiration

Inspired by data visualization and SVG generation trends — the idea that creating charts should be as simple as passing data, without heavyweight rendering engines or browser dependencies.

---

Built by [Officethree Technologies](https://officethree.com) | Made with love and AI
