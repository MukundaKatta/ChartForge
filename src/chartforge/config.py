"""Configuration models for ChartForge."""

from pydantic import BaseModel, Field


# Default color palette — Tableau 10 inspired
DEFAULT_PALETTE: list[str] = [
    "#4E79A7",
    "#F28E2B",
    "#E15759",
    "#76B7B2",
    "#59A14F",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
    "#9C755F",
    "#BAB0AC",
]


class ChartConfig(BaseModel):
    """Validated configuration for chart generation."""

    width: int = Field(default=800, ge=100, le=4000, description="Chart width in pixels")
    height: int = Field(default=600, ge=100, le=4000, description="Chart height in pixels")
    palette: list[str] = Field(default_factory=lambda: list(DEFAULT_PALETTE))
    padding: int = Field(default=60, ge=0, description="Padding around the chart area")
    title_font_size: int = Field(default=20, ge=8, le=72)
    label_font_size: int = Field(default=12, ge=6, le=36)
    font_family: str = Field(default="Arial, Helvetica, sans-serif")
    background_color: str = Field(default="#FFFFFF")
    show_grid: bool = Field(default=True)
    bar_gap: float = Field(default=0.2, ge=0.0, le=0.8, description="Gap ratio between bars")
