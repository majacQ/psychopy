from builtins import object
from pathlib import Path

from psychopy import visual, event
from psychopy.alerts._errorHandler import _BaseErrorHandler
from psychopy.visual import Window
from psychopy.visual import TextBox2
from psychopy.visual.textbox2.fontmanager import FontManager
import pytest
from psychopy.tests import utils

# cd psychopy/psychopy
# py.test -k textbox --cov-report term-missing --cov visual/textbox


@pytest.mark.textbox
class Test_textbox(object):
    def setup_class(self):
        self.win = Window([128,128], pos=[50,50], allowGUI=False, autoLog=False)
        self.error = _BaseErrorHandler()
        self.textbox = TextBox2(self.win, "", "Noto Sans",
                                pos=(0, 0), size=(1, 1), units='height',
                                letterHeight=0.1, colorSpace="rgb")

    def teardown_class(self):
        self.win.close()

    def test_glyph_rendering(self):

        # Add all Noto Sans fonts to cover widest possible base of handles characters
        for font in ["Noto Sans", "Noto Sans HK", "Noto Sans JP", "Noto Sans KR", "Noto Sans SC", "Noto Sans TC", "Niramit", "Indie Flower"]:
            self.textbox.fontMGR.addGoogleFont(font)
        # Some exemplar text to test basic TextBox rendering
        exemplars = [
            # An English pangram
            {"text": "A PsychoPy zealot knows a smidge of wx, but JavaScript is the question.",
             "font": "Noto Sans",
             "screenshot": "exemplar_1.png"},
            # The same pangram in IPA
            {"text": "ə saɪkəʊpaɪ zɛlət nəʊz ə smidge ɒv wx, bʌt ˈʤɑːvəskrɪpt ɪz ðə ˈkwɛsʧən",
                "font": "Noto Sans",
                "screenshot": "exemplar_2.png"},
            # The same pangram in Hangul
            {"text": "아 프시초피 제알롣 크노W스 아 s믿게 오f wx, 붇 자v앗c립t 잇 테 q왯디온",
             "font": "Noto Sans KR",
             "screenshot": "exemplar_3.png"},
            # A noticeably non-standard font
            {"text": "A PsychoPy zealot knows a smidge of wx, but JavaScript is the question.",
             "font": "Indie Flower",
             "screenshot": "exemplar_4.png",
            }
        ]
        # Some text which is likely to cause problems if something isn't working
        tykes = [
            # Text which doesn't render properly on Mac (Issue #3203)
            {"text": "कोशिकायें",
             "font": "Noto Sans",
             "screenshot": "tyke_1.png"},
            # Thai text which old Text component couldn't handle due to Pyglet
            {"text": "ขาว แดง เขียว เหลือง ชมพู ม่วง เทา",
             "font": "Niramit",
             "screenshot": "tyke_2.png"
             }
        ]
        # Test each case and compare against screenshot
        for case in exemplars + tykes:
            self.textbox.reset()
            self.textbox.fontMGR.addGoogleFont(case['font'])
            self.textbox.font = case['font']
            self.textbox.text = case['text']
            self.win.flip()
            self.textbox.draw()
            if case['screenshot']:
                # Uncomment to save current configuration as desired
                filename = "textbox_{}_{}".format(self.textbox._lineBreaking, case['screenshot'])
                #self.win.getMovieFrame(buffer='back').save(Path(utils.TESTS_DATA_PATH) / filename)
                utils.compareScreenshot(Path(utils.TESTS_DATA_PATH) / filename, self.win, crit=20)

    def test_colors(self):
        self.textbox.text = "A PsychoPy zealot knows a smidge of wx, but JavaScript is the question."
        # Some exemplar text to test basic colors
        exemplars = [
            # White on black in rgb
            {"color": (1, 1, 1), "fillColor": (-1,-1,-1), "borderColor": (-1,-1,-1), "space": "rgb",
             "screenshot": "colors_WOB.png"},
            # White on black in named
            {"color": "white", "fillColor": "black", "borderColor": "black", "space": "rgb",
             "screenshot": "colors_WOB.png"},
            # White on black in hex
            {"color": "#ffffff", "fillColor": "#000000", "borderColor": "#000000", "space": "hex",
             "screenshot": "colors_WOB.png"},
            {"color": "red", "fillColor": "yellow", "borderColor": "blue", "space": "rgb",
             "screenshot": "colors_exemplar1.png"},
            {"color": "yellow", "fillColor": "blue", "borderColor": "red", "space": "rgb",
             "screenshot": "colors_exemplar2.png"},
            {"color": "blue", "fillColor": "red", "borderColor": "yellow", "space": "rgb",
             "screenshot": "colors_exemplar3.png"},
        ]
        # Some colors which are likely to cause problems if something isn't working
        tykes = [
            # Text only
            {"color": "white", "fillColor": None, "borderColor": None, "space": "rgb",
             "screenshot": "colors_tyke1.png"},
            # Fill only
            {"color": None, "fillColor": "white", "borderColor": None, "space": "rgb",
             "screenshot": "colors_tyke2.png"},
            # Border only
            {"color": None, "fillColor": None, "borderColor": "white", "space": "rgb",
            "screenshot": "colors_tyke3.png"},
        ]
        # Test each case and compare against screenshot
        for case in exemplars + tykes:
            # Raise error if case spec does not contain all necessary keys
            if not all(key in case for key in ["color", "fillColor", "borderColor", "space", "screenshot"]):
                raise KeyError(f"Case spec for test_colors in class {self.__class__.__name__} ({__file__}) invalid, test cannot be run.")
            # Apply params from case spec
            self.textbox.colorSpace = case['space']
            self.textbox.color = case['color']
            self.textbox.fillColor = case['fillColor']
            self.textbox.borderColor = case['borderColor']
            for lineBreaking in ('default', 'uax14'):
                self.win.flip()
                self.textbox.draw()
            if case['screenshot']:
                # Uncomment to save current configuration as desired
                    filename = "textbox_{}_{}".format(self.textbox._lineBreaking, case['screenshot'])
                    # self.win.getMovieFrame(buffer='back').save(Path(utils.TESTS_DATA_PATH) / filename)
                    utils.compareScreenshot(Path(utils.TESTS_DATA_PATH) / filename, self.win, crit=20)

    def test_basic(self):
        pass

    def test_something(self):
        # to-do: test visual display, char position, etc
        pass
            
    def test_alerts(self):
        noFontTextbox = TextBox2(self.win, "", font="Raleway Dots", bold=True)
        assert (self.error.alerts[0].code == 4325)


def test_font_manager():
        # Create a font manager
        mgr = FontManager()
        # Check that it finds fonts which should be pre-packaged with PsychoPy in the resources folder
        assert bool(mgr.getFontNamesSimilar("Open Sans"))
        # Check that it doesn't find fonts which aren't installed as default
        assert not bool(mgr.getFontNamesSimilar("Dancing Script"))
        # Check that it can install fonts from Google
        mgr.addGoogleFont("Hanalei")
        # Check that these fonts are found once installed
        assert bool(mgr.getFontNamesSimilar("Hanalei"))


@pytest.mark.uax14
class Test_uax14_textbox(Test_textbox):
    """Runs the same tests as for Test_textbox, but with the textbox set to uax14 line breaking"""
    def setup_class(self):
        Test_textbox.setup_class(self)
        self.textbox._lineBreaking = 'uax14'
