"""Tests for ChartForge core chart generation."""

import os
import tempfile

from chartforge import ChartForge, ChartConfig


class TestBarChart:
    """Tests for bar chart generation."""

    def test_bar_chart_contains_svg_elements(self) -> None:
        """Bar chart SVG should contain rect elements and viewBox."""
        cf = ChartForge()
        svg = cf.bar_chart([10, 20, 30], ["A", "B", "C"], "Test Bar")

        assert "<svg" in svg
        assert "viewBox" in svg
        assert "<rect" in svg
        assert "Test Bar" in svg
        assert "</svg>" in svg

    def test_bar_chart_labels_present(self) -> None:
        """Bar chart should include all provided labels."""
        cf = ChartForge()
        svg = cf.bar_chart([5, 15, 25], ["Jan", "Feb", "Mar"])

        assert "Jan" in svg
        assert "Feb" in svg
        assert "Mar" in svg

    def test_bar_chart_empty_data(self) -> None:
        """Bar chart with empty data should still produce valid SVG."""
        cf = ChartForge()
        svg = cf.bar_chart([], [], "Empty")

        assert "<svg" in svg
        assert "</svg>" in svg


class TestLineChart:
    """Tests for line chart generation."""

    def test_line_chart_contains_polyline(self) -> None:
        """Line chart should contain a polyline element."""
        cf = ChartForge()
        svg = cf.line_chart([10, 25, 18, 42], ["Q1", "Q2", "Q3", "Q4"], "Trend")

        assert "<polyline" in svg
        assert "Trend" in svg
        assert "<circle" in svg

    def test_line_chart_custom_size(self) -> None:
        """Line chart with custom size should reflect in viewBox."""
        cf = ChartForge()
        cf.set_size(1200, 900)
        svg = cf.line_chart([1, 2, 3], ["A", "B", "C"])

        assert 'viewBox="0 0 1200 900"' in svg


class TestPieChart:
    """Tests for pie chart generation."""

    def test_pie_chart_contains_paths(self) -> None:
        """Pie chart should contain path elements for slices."""
        cf = ChartForge()
        svg = cf.pie_chart([40, 30, 20, 10], ["A", "B", "C", "D"], "Share")

        assert "<path" in svg
        assert "Share" in svg

    def test_pie_chart_percentages(self) -> None:
        """Pie chart should display percentage labels."""
        cf = ChartForge()
        svg = cf.pie_chart([50, 50], ["Half", "Half"], "50-50")

        assert "50%" in svg


class TestDonutChart:
    """Tests for donut chart generation."""

    def test_donut_chart_contains_paths(self) -> None:
        """Donut chart should contain path elements."""
        cf = ChartForge()
        svg = cf.donut_chart([25, 25, 25, 25], ["A", "B", "C", "D"], "Donut")

        assert "<path" in svg
        assert "Donut" in svg


class TestOutputMethods:
    """Tests for to_svg, save, and add_legend."""

    def test_to_svg_returns_generated_svg(self) -> None:
        """to_svg() should return the same string as the chart method."""
        cf = ChartForge()
        svg = cf.bar_chart([1, 2, 3], ["X", "Y", "Z"])
        assert cf.to_svg() == svg

    def test_save_writes_file(self) -> None:
        """save() should write the SVG to a file."""
        cf = ChartForge()
        cf.bar_chart([10, 20], ["A", "B"])

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "chart.svg")
            cf.save(path)
            assert os.path.exists(path)
            with open(path, "r") as f:
                content = f.read()
            assert "<svg" in content

    def test_add_legend(self) -> None:
        """add_legend() should inject legend elements into the SVG."""
        cf = ChartForge()
        cf.bar_chart([10, 20, 30], ["Alpha", "Beta", "Gamma"], "Legend Test")
        svg = cf.add_legend()

        assert "Alpha" in svg
        assert "Beta" in svg
        assert "Gamma" in svg

    def test_custom_colors(self) -> None:
        """Custom colors should be used in generated SVG."""
        cf = ChartForge()
        cf.set_colors(["#FF0000", "#00FF00", "#0000FF"])
        svg = cf.bar_chart([10, 20, 30], ["R", "G", "B"])

        assert "#FF0000" in svg
        assert "#00FF00" in svg
        assert "#0000FF" in svg


class TestConfig:
    """Tests for ChartConfig validation."""

    def test_default_config(self) -> None:
        """Default config should have expected values."""
        cfg = ChartConfig()
        assert cfg.width == 800
        assert cfg.height == 600
        assert len(cfg.palette) == 10

    def test_custom_config(self) -> None:
        """ChartForge should accept a custom config."""
        cfg = ChartConfig(width=1000, height=700, padding=80)
        cf = ChartForge(config=cfg)
        svg = cf.bar_chart([5], ["X"])
        assert 'viewBox="0 0 1000 700"' in svg
