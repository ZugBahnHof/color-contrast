import enum

from colour import Color


class AccessibilityLevel(enum.Enum):
    AA18 = 3
    AA = 4.5
    AAA = 7


class ModulationMode(enum.Enum):
    FOREGROUND = "fg"
    BACKGROUND = "bg"
    BOTH = "both"


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
    *,
    level: float | AccessibilityLevel = AccessibilityLevel.AA,
) -> bool:
    """
    Checks whether the contrast between two colors is above a certain threshold.

    :param foreground_color: Foreground (text) color
    :type foreground_color: str | Color
    :param background_color: Background Color (cannot be transparent)
    :type background_color: str | Color
    :param level: Necessary minimum contrast the two colors
    :type level: float | AccessibilityLevel
    :return: Whether the contrast check passes
    :rtype: bool
    """

    if isinstance(level, AccessibilityLevel):
        level = level.value

    fg = Color(foreground_color)
    bg = Color(background_color)

    l1 = get_luminance(fg)
    l2 = get_luminance(bg)

    ratio = (l1 + 0.05) / (l2 + 0.05)
    ratio_i = (l2 + 0.05) / (l1 + 0.05)

    return ratio >= level or ratio_i >= level


def increase_lightness(color: Color, delta: float) -> Color:
    old_hsl = color.hsl

    new_hsl = (old_hsl[0], old_hsl[1], max(0, min(1, old_hsl[2] + delta)))

    return Color(hsl=new_hsl)


def modulate(
    foreground: str | Color,
    background: str | Color,
    *,
    level: float | AccessibilityLevel = AccessibilityLevel.AA,
    mode: ModulationMode = ModulationMode.FOREGROUND,
):
    foreground = Color(foreground)
    background = Color(background)

    l1, l2 = get_luminance(foreground), get_luminance(background)

    # fg Color is brighter
    fg_delta = 1 / 256 if l1 > l2 else -1 / 256

    unsuccessful_stop = False

    while not check_contrast(foreground, background, level=level):
        if (
            foreground.get_luminance() in (0, 1)
            and mode is not ModulationMode.BACKGROUND
        ):
            if mode is ModulationMode.FOREGROUND:
                unsuccessful_stop = True
                break
            elif mode is ModulationMode.BOTH:
                mode = ModulationMode.BACKGROUND
        if (
            background.get_luminance() in (0, 1)
            and mode is not ModulationMode.FOREGROUND
        ):
            if mode is ModulationMode.BACKGROUND:
                unsuccessful_stop = True
                break
            elif mode is ModulationMode.BOTH:
                mode = ModulationMode.FOREGROUND

        match mode:
            case ModulationMode.FOREGROUND:
                foreground = increase_lightness(foreground, fg_delta)

            case ModulationMode.BACKGROUND:
                background = increase_lightness(background, -fg_delta)

            case ModulationMode.BOTH:
                foreground = increase_lightness(foreground, fg_delta)
                background = increase_lightness(background, -fg_delta)

    return foreground, background, not unsuccessful_stop
