import enum

from colour import Color


class AccessibilityLevel(enum.Enum):
    AA18 = 3
    AA = 4.5
    AAA = 7


def get_luminance(color: Color) -> float:
    """
    Calculate the relative luminance of the supplied color.

    Algorithm taken from https://www.w3.org/TR/WCAG21/#dfn-relative-luminance

    :param color: the color to get the luminance from
    :type color: Color
    :return: Luminance value
    :rtype: float
    """

    RsRGB, GsRGB, BsRGB = color.get_rgb()

    R = RsRGB / 12.92 if RsRGB <= 0.04045 else ((RsRGB + 0.055) / 1.055) ** 2.4
    G = GsRGB / 12.92 if GsRGB <= 0.04045 else ((GsRGB + 0.055) / 1.055) ** 2.4
    B = BsRGB / 12.92 if BsRGB <= 0.04045 else ((BsRGB + 0.055) / 1.055) ** 2.4

    luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B

    return luminance


def check_contrast(
    foreground_color: str | Color,
    background_color: str | Color,
    level: AccessibilityLevel = AccessibilityLevel.AA,
) -> bool:
    fg = Color(foreground_color)
    bg = Color(background_color)

    l1 = get_luminance(fg)
    l2 = get_luminance(bg)

    ratio = (l1 + 0.05) / (l2 + 0.05)

    return ratio >= level.value
