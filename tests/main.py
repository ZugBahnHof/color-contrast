import unittest

from colour import Color

from color_contrast import AccessibilityLevel, check_contrast, modulate, ModulationMode


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

        self.assertTrue(check_contrast("#000", "#fff"))
        self.assertTrue(check_contrast("#000", "#ffffff"))
        self.assertTrue(check_contrast("#000", "white"))

        self.assertTrue(check_contrast("#000000", "#fff"))
        self.assertTrue(check_contrast("#000000", "#ffffff"))
        self.assertTrue(check_contrast("#000000", "white"))

        self.assertTrue(check_contrast("black", "#fff"))
        self.assertTrue(check_contrast("black", "#ffffff"))
        self.assertTrue(check_contrast("black", "white"))

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

    def test_modulate_no_action_needed(self):
        a, b = Color("#fff"), Color("#000")
        a_, b_, success = modulate(a, b)

        self.assertEqual(a, a_)
        self.assertEqual(b, b_)
        self.assertTrue(success)

    def test_modulate_no_action_needed_inv(self):
        a, b = Color("#000"), Color("#fff")
        a_, b_, success = modulate(a, b, mode=ModulationMode.BACKGROUND)

        self.assertEqual(a, a_)
        self.assertEqual(b, b_)
        self.assertTrue(success)

    def test_modulate_fg_brighter(self):
        a, b = Color("#444"), Color("#000")
        a_, b_, success = modulate(a, b)

        self.assertNotEqual(a, a_)
        self.assertEqual(Color("#757575"), a_)
        self.assertEqual(b, b_)
        self.assertTrue(success)

    def test_modulate_fg_brighter_hue_sat(self):
        a, b = Color("#0d5eaf"), Color("#000")
        a_, b_, success = modulate(a, b)

        self.assertNotEqual(a, a_)
        self.assertEqual(a.get_hue(), a_.get_hue())
        self.assertEqual(a.get_saturation(), a_.get_saturation())
        self.assertEqual(Color("#1074d8"), a_)
        self.assertEqual(b, b_)
        self.assertTrue(success)

    def test_modulate_fg_darker(self):
        a, b = Color("#eee"), Color("#fff")
        a_, b_, success = modulate(a, b)

        self.assertNotEqual(a, a_)
        self.assertEqual(Color("#767676"), a_)
        self.assertEqual(b, b_)
        self.assertTrue(success)

    def test_modulate_fg_darker_hue_sat(self):
        a, b = Color("#0d5eaf"), Color("#888888")
        a_, b_, success = modulate(a, b)

        self.assertNotEqual(a, a_)
        self.assertEqual(a.get_hue(), a_.get_hue())
        self.assertEqual(a.get_saturation(), a_.get_saturation())
        self.assertEqual(Color("#052240"), a_)
        self.assertEqual(b, b_)
        self.assertTrue(success)

    def test_modulate_bg_brighter(self):
        a, b = Color("#000"), Color("#444")
        a_, b_, success = modulate(a, b, mode=ModulationMode.BACKGROUND)

        self.assertEqual(a, a_)
        self.assertNotEqual(b, b_)
        self.assertEqual(Color("#757575"), b_)
        self.assertTrue(success)

    def test_modulate_bg_brighter_hue_sat(self):
        a, b = Color("#000"), Color("#0d5eaf")
        a_, b_, success = modulate(a, b, mode=ModulationMode.BACKGROUND)

        self.assertEqual(a, a_)
        self.assertNotEqual(b, b_)
        self.assertEqual(b.get_hue(), b_.get_hue())
        self.assertEqual(b.get_saturation(), b_.get_saturation())
        self.assertEqual(Color("#1074d8"), b_)
        self.assertTrue(success)

    def test_modulate_bg_darker(self):
        a, b = Color("#fff"), Color("#eee")
        a_, b_, success = modulate(a, b, mode=ModulationMode.BACKGROUND)

        self.assertEqual(a, a_)
        self.assertNotEqual(b, b_)
        self.assertEqual(Color("#767676"), b_)
        self.assertTrue(success)

    def test_modulate_bg_darker_hue_sat(self):
        a, b = Color("#888888"), Color("#0d5eaf")
        a_, b_, success = modulate(a, b, mode=ModulationMode.BACKGROUND)

        self.assertEqual(a, a_)
        self.assertNotEqual(b, b_)
        self.assertEqual(b.get_hue(), b_.get_hue())
        self.assertEqual(b.get_saturation(), b_.get_saturation())
        self.assertEqual(Color("#052240"), b_)
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
