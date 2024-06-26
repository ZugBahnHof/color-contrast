import unittest
from color_contrast import AccessibilityLevel, check_contrast


class ContrastCheckTestCase(unittest.TestCase):
    BG = "#123456"
    FG = {
        0: "#404040",
        AccessibilityLevel.AA18: "#888888",
        AccessibilityLevel.AA: "#AAAAAA",
        AccessibilityLevel.AAA: "#DDDDDD",
    }

    def test_accessible(self):
        self.assertTrue(check_contrast("#fff", "#000"))
        self.assertTrue(check_contrast("#fff", "#000000"))
        self.assertTrue(check_contrast("#fff", "black"))

        self.assertTrue(check_contrast("#ffffff", "#000"))
        self.assertTrue(check_contrast("#ffffff", "#000000"))
        self.assertTrue(check_contrast("#ffffff", "black"))

        self.assertTrue(check_contrast("white", "#000"))
        self.assertTrue(check_contrast("white", "#000000"))
        self.assertTrue(check_contrast("white", "black"))

    def test_inaccessible(self):
        self.assertFalse(check_contrast("#123456", "#123456"))

    def test_aa18(self):
        self.assertFalse(
            check_contrast(self.FG[0], self.BG, level=AccessibilityLevel.AA18)
        )
        self.assertTrue(
            check_contrast(
                self.FG[AccessibilityLevel.AA18], self.BG, level=AccessibilityLevel.AA18
            )
        )
        self.assertTrue(
            check_contrast(
                self.FG[AccessibilityLevel.AA], self.BG, level=AccessibilityLevel.AA18
            )
        )
        self.assertTrue(
            check_contrast(
                self.FG[AccessibilityLevel.AAA], self.BG, level=AccessibilityLevel.AA18
            )
        )

    def test_aa(self):
        self.assertFalse(
            check_contrast(self.FG[0], self.BG, level=AccessibilityLevel.AA)
        )
        self.assertFalse(
            check_contrast(
                self.FG[AccessibilityLevel.AA18], self.BG, level=AccessibilityLevel.AA
            )
        )
        self.assertTrue(
            check_contrast(
                self.FG[AccessibilityLevel.AA], self.BG, level=AccessibilityLevel.AA
            )
        )
        self.assertTrue(
            check_contrast(
                self.FG[AccessibilityLevel.AAA], self.BG, level=AccessibilityLevel.AA
            )
        )

    def test_aaa(self):
        self.assertFalse(
            check_contrast(self.FG[0], self.BG, level=AccessibilityLevel.AAA)
        )
        self.assertFalse(
            check_contrast(
                self.FG[AccessibilityLevel.AA18], self.BG, level=AccessibilityLevel.AAA
            )
        )
        self.assertFalse(
            check_contrast(
                self.FG[AccessibilityLevel.AA], self.BG, level=AccessibilityLevel.AAA
            )
        )
        self.assertTrue(
            check_contrast(
                self.FG[AccessibilityLevel.AAA], self.BG, level=AccessibilityLevel.AAA
            )
        )


if __name__ == "__main__":
    unittest.main()
