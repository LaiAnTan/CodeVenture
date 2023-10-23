import unittest
import sys
import os

p = os.path.abspath(os.path.join('..'))
sys.path.append(p)

# flake8: noqa
from test_const import TEST_DIR, TEST_ASSET
from src.backend.activity.ac_classes.ac_module import Activity


class TestModuleParsing(unittest.TestCase):
    """Simulates the expected behavior when an activity (any module, quiz, 
    or challange) is parsed"""

    def set_up_test_activity_fast(self, code: str) -> Activity:
        ac_test = Activity(code, Activity.AType.Module)
        ac_test.ModulePath = f'{TEST_ASSET}'
        ac_test.data_file = f'{code}.dat'
        ac_test.read_data_file()
        return ac_test

    ## ParseHeader

    def test_getHeader_return_value(self) -> None:
        ac_test = self.set_up_test_activity_fast('TEST000')
        header = ac_test.getHeaders()

        # getHeader returns a tuple with 4 values [id, title, difficulty, tags]
        self.assertIsInstance(
            header,
            tuple,
            'getHeader does not return a tuple'
        )

        self.assertTrue(
            len(header) == 4,
            'getHeader return value is not 4 values'
        )


    def test_valid_header_parsing(self) -> None:
        """
        Nothing special, just a valid header
        """
        ac_test = self.set_up_test_activity_fast('TEST000')

        test_header = ac_test.getHeaders()
        self.assertEqual(
            test_header,
            ('TEST000', 'Test', 2, ['test_tag', 'test_tag2']),
            'Parsed header is not the same as in data file'
        )

        test_warning = ac_test.getWarning()
        self.assertTrue(
            len(test_warning) == 0,
            'There was warnings dispatch even though there shouldn\'t be'
        )


    def test_invalid_header_invalid_keyword(self) -> None:
        """
        Test invalid keyword in header
        """
        ac_test = self.set_up_test_activity_fast('INVD000')

        test_warnings = ac_test.getWarning()

        # check warning
        self.assertTrue(
            (len(test_warnings) != 0),
            'Warning was not issued'
        )

        # check warning content
        self.assertEqual(
            test_warnings[0],
            ('HEADER', 'Unidentified Keyword {INVALID}'),
            'Wrong Warning Issued'
        )


    def test_invalid_header_no_content(self) -> None:
        """
        Test no field provided for a keyword in header
        """
        ac_test = self.set_up_test_activity_fast('INVD001')

        # ID field has no content
        test_warnings = ac_test.getWarning()

        # check warning
        self.assertTrue(
            (len(test_warnings) != 0),
            'Warning was not issued'
        )

        # check warning content
        self.assertEqual(
            test_warnings[0],
            ('HEADER', 'Keyword ID has no content'),
            'Wrong Warning Issued'
        )


    def test_invalid_header_empty_content(self) -> None:
        """
        Test empty field provided for a keyword in header
        """
        ac_test = self.set_up_test_activity_fast('INVD002')

        # Title has an empty field
        test_warnings = ac_test.getWarning()

        # check warning
        self.assertTrue(
            (len(test_warnings) != 0),
            'Warning was not issued'
        )

        # check warning content
        self.assertEqual(
            test_warnings[0],
            ('HEADER', 'Keyword TITLE content is empty!'),
            'Wrong Warning Issued'
        )


    def test_invalid_header_missing_field(self) -> None:
        """
        Test missing fields in header
        """

        ac_test = self.set_up_test_activity_fast('INVD003')

        # ID and Title are both missing
        test_warnings = ac_test.getWarning()

        # check warning
        self.assertTrue(
            (len(test_warnings) != 0),
            'Warning was not issued'
        )

        # check warning content
        self.assertEqual(
            test_warnings[0],
            ('HEADER', 'Header field is incomplete, missing \'ID\', \'Title\''),
            'Wrong Warning Issued'
        )

    ## ParseContent

    def test_getContent_returnValue(self) -> None:
        ac_test = self.set_up_test_activity_fast('TEST000')
        ac_test.ParseContent()

        content = ac_test.getContent()

        # getContent returns a list
        self.assertIsInstance(
            content,
            list,
            'getContent does not return a list'
        )


    def test_parsing_content(self) -> None:
        """
        Test content parsing
        """
        ac_test = self.set_up_test_activity_fast('TEST000')
        ac_test.ParseContent()

        test_content = ac_test.getContent()

        # check if content matches in data file
        self.assertEqual(
            test_content,
            [
                (Activity.Content_Type.Paragraph, 'Hi From Test!'),
                (Activity.Content_Type.Image, 'IMG001'),
                (Activity.Content_Type.Code, 'CD001')
            ],
            'There are missing content that arent parsed'
        )

        # should not have any warning
        self.assertTrue(
            len(ac_test.getWarning()) == 0,
            'Warning is issued even though there should be none'
        )


    def test_invalid_content_missing_argument(self) -> None:
        """
        Test missing ID in asset lines
        """
        ac_test = self.set_up_test_activity_fast('INVD101')
        ac_test.ParseContent()

        # IMG-CONT in line 2 does not have value associated to it
        test_warnings = ac_test.getWarning()

        # check warning
        self.assertTrue(
            (len(test_warnings) != 0),
            'Warning was not issued'
        )

        # check warning content
        self.assertEqual(
            test_warnings[0],
            ('CONTENT', 'Image Asset in line 2 has no image ID associated to it and will be ignored'),
            'Wrong Warning Issued'
        )

    ## ParseSource

    def test_getSources_return_value(self) -> None:
        """
        Ensures all function return value is as expected
        """

        ac_test = self.set_up_test_activity_fast('TEST000')
        ac_test.ParseSources()

        sources = ac_test.getSources()


        # get sources returns a tuple with 2 dictionaries
        self.assertIsInstance(
            sources,
            tuple,
            'getSources does not return a tuple'
        )

        self.assertTrue(
            len(sources) == 2,
            'There isnt 2 dictionaries in the return value of getSources'
        )

        # image dictionary is a dict data type
        self.assertIsInstance(
            sources[0],
            dict,
            'Image dictionary is not a dictionary data type'
        )

        # code dictionary is a dict data type
        self.assertIsInstance(
            sources[1],
            dict,
            'Code dictionary is not a dictionary data type'
        )


    def test_source_parsing(self) -> None:
        """
        Test source parsing
        """

        ac_test = self.set_up_test_activity_fast('TEST000')
        ac_test.ParseSources()

        test_sources = ac_test.getSources()

        # check if image dictionary was correctly parsed
        self.assertEqual(
            test_sources[0],
            {'IMG001': 'test_pic.png'},
            'Image Sources incorrectly parsed'
        )

        # check if code dictionary was correctly parsed
        self.assertEqual(
            test_sources[1],
            {'CD001': 'test_code'},
            'Code Sources incorrectly parsed'
        )

        # there should be no warning
        self.assertTrue(
            len(ac_test.getWarning()) == 0,
            'Warning is issued even though there should be none'
        )


    def test_invalid_source_no_end(self) -> None:
        """
        Test missing CODE-CONT-END and IMG-CONT-END tags
        """

        ac_test = self.set_up_test_activity_fast('INVD201')
        ac_test.ParseSources()

        # missing IMG-CONT-END tag
        test_warning = ac_test.getWarning()

        # check warning
        self.assertTrue(
            (len(test_warning) != 0),
            'Warning was not issued'
        )

        # check warning content
        self.assertEqual(
            test_warning[0],
            ('SOURCES', 'Delimiter IMG-CONT-END not found, parse ended prematurely'),
            'Wrong Warning Issued'
        )

    def test_invalid_source_empty_field(self) -> None:
        """
        Test missing field for keyword in sources
        """
        ac_test = self.set_up_test_activity_fast('INVD202')
        ac_test.ParseSources()

        # there will be 2 errors
        # in IMG, missing field and delimiter
        # in CD, missing field, but has delimiter
        test_warning = ac_test.getWarning()

        # check warning
        self.assertTrue(
            (len(test_warning) != 0),
            'Warning was not issued'
        )

        self.assertTrue(
            (len(test_warning) == 2),
            'Too little warning issued'
        )

        # check warning content
        self.assertEqual(
            test_warning,
            [
                ('SOURCES', 'Source asset has no value and will be ignored'),
                ('SOURCES', 'Source asset has no value and will be ignored')
            ],
            'Wrong Warning Issued'
        )


if __name__ == "__main__":
    unittest.main()
