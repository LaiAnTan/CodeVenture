import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

# flake8: noqa
from test_const import TEST_ASSET
from src.frontend.edu_windows.edu_module_editor import ModuleEditor
from src.frontend.edu_windows.helper_class.assetWindow import AssetWindow
from src.frontend.edu_windows.helper_class.paragraphEntry import ParagraphEntryForm
from src.frontend.edu_windows.helper_class.assetPreview import AssetPreview
from src.frontend.edu_windows.helper_class.assetWindow import AssetWindow
from src.frontend.ui_app import App

class TestModuleExport(unittest.TestCase):
    """
    Simulates the expected behavior when an educator makes a
    new module

    If no error message is produced, it is safe to assume the module
    can be correctly exported
    """

    @classmethod
    def setUpClass(cls) -> None:
        App()

    def setUp(self) -> None:
        self.md_editor = ModuleEditor(None)
        self.datafile_editor = self.md_editor.data_editor

    # Test Paragraph Entry

    def test_adding_paragraph_entry(self) -> None:
        """
        Test adding a paragraph entry point
        """

        # add a paragraph widget

        # simulate user changing option to Paragraph

        self.datafile_editor.chosen_para_type.set('Paragraph')
        paragraph_entry = self.datafile_editor.add_entry_point()

        # check if Paragraph entry widget is added
        self.assertEqual(
            self.datafile_editor.content_frame.get_tracking_no(),
            1,
            'Entry point failed to be added'
        )

        # check type of widget added is paragraph entry point
        self.assertIsInstance(
            paragraph_entry,
            ParagraphEntryForm,
            'Wrong type of entry point added'
        )

    def test_pasting_paragraph_no_newline(self) -> None:
        """
        Test pasting a paragraph into a paragraph entry point
        with no newline
        """

        # add a paragraph widget

        # simulate user changing option to Paragraph
        self.datafile_editor.chosen_para_type.set('Paragraph')
        paragraph_entry = self.datafile_editor.add_entry_point()

        # simulate user pasting data into paragraph
        self.md_editor.winfo_toplevel().clipboard_clear()
        self.md_editor.winfo_toplevel().clipboard_append('Foo Bar')
        paragraph_entry.focus()
        # PasteData is binded to Ctrl+V
        # - pressing control V is
        #   equivalent to calling PasteData
        paragraph_entry.PasteData()

        # check content of Paragraph Entry Widget
        self.assertEqual(
            paragraph_entry.getData()[1],
            'Foo Bar',
            'Content is not pasted properly'
        )

    def test_pasting_paragraph_newlines(self) -> None:
        """
        Test pasting a paragraph into a paragraph entry point
        with newlines
        """

        # add a paragraph widget

        # simulate user changing option to Paragraph
        self.datafile_editor.chosen_para_type.set('Paragraph')
        paragraph_entry = self.datafile_editor.add_entry_point()

        # simulate user pasting data into paragraph
        self.md_editor.winfo_toplevel().clipboard_clear()
        self.md_editor.winfo_toplevel().clipboard_append('Foo\nBar\nBaz')
        paragraph_entry.PasteData()

        # check amount of new widget made
        self.assertEqual(
            self.datafile_editor.content_frame.get_tracking_no(),
            3,
            'Amount of widget created isnt the expeceted value 3'
        )

        # check value in each paragraph entry
        expected_value = ['Foo', 'Bar', 'Baz']
        for index, entry in enumerate(self.datafile_editor.content_frame.get_tracking_list()):
            self.assertEqual(
                entry.getData()[1],
                expected_value[index],
                'Content is not pasted properly'
            )
    
    def test_exporting_paragraph_entry(self) -> None:
        """
        Test exporting with a paragraph entry
        """

        # Simulate user adding a paragraph entry point
        self.datafile_editor.chosen_para_type.set('Paragraph')
        paragraph = self.datafile_editor.add_entry_point()
        paragraph.insertData('Hello World!')

        # attempt to export
        content = self.md_editor.GetContentData()
        error = self.md_editor.get_error_list()

        # Content should have the paragraph and asset preview
        # asset preview should have the image inside
        self.assertEqual(
            content,
            [
                ('paragraph', 'Hello World!'),
            ],
            'Content not properly extracted'
        )

        # error should be completely empty
        self.assertEqual(
            len(error),
            0,
            'Error Message generated even though there should not be any'
        )

    def test_backspace_paragraph_entry(self) -> None:
        """
        Test pressing backspace in a empty paragraph
        """

        # add a paragraph widget

        # simulate user changing option to Paragraph
        self.datafile_editor.chosen_para_type.set('Paragraph')
        paragraph_entry = self.datafile_editor.add_entry_point()

        # Remove self is binded to BackSpace
        # - Pressing BackSpace is equivalent to 
        #   calling BackSpace
        paragraph_entry.RemoveSelf()

        # check if Paragraph entry widget is removed
        self.assertEqual(
            self.datafile_editor.content_frame.get_tracking_no(),
            0,
            'Entry point failed to be removed'
        )

    # Test Asset Window

    def test_asset_image_file(self):
        """
        Test importing a valid image file for asset preview window
        """
        # Simulate user adding a new asset
        asset_window = AssetWindow(self.md_editor, 200, 200, self.md_editor.get_asset_list())
        asset_window.chosen_type.set('Picture')
        pic_asset = asset_window.add_new_asset()
        pic_asset.PreviewImage(f'{TEST_ASSET}/test.png')

        self.assertEqual(
            pic_asset.getData(),
            ('image', 'test', f'{TEST_ASSET}/test.png'),
            'Asset not added correctly'
        )

    def test_updating_new_asset(self):
        """
        Test importing a valid image file for asset preview window
        """
        # Simulate user adding a new asset
        asset_window = AssetWindow(self.md_editor, 200, 200, self.md_editor.get_asset_list())
        asset_window.chosen_type.set('Picture')
        pic_asset = asset_window.add_new_asset()
        pic_asset.PreviewImage(f'{TEST_ASSET}/test.png')
        asset_window.save_data()

        self.assertEqual(
            len(self.md_editor.get_asset_list()),
            1,
            'Asset not added succesfully'
        )

        self.assertEqual(
            self.md_editor.get_asset_list()[0],
            ('image', 'test', f'{TEST_ASSET}/test.png'),
            'Asset not added correctly'
        )

    def test_invalid_asset_invalid_file(self):
        """
        Test opening a invalid file for asset preview window
        """
        # Simulate user adding a new asset
        asset_window = AssetWindow(self.md_editor, 200, 200, self.md_editor.get_asset_list())
        asset_window.chosen_type.set('Picture')
        pic_asset = asset_window.add_new_asset()
        pic_asset.PreviewImage(f'{TEST_ASSET}/test.txt')

        error = asset_window.get_error_message()

        # error should be issued
        self.assertEqual(
            len(error),
            1,
            'Error not issued'
        )

        self.assertEqual(
            error[0][1][0],
            'Error in Image Attachment - Invalid File Format',
            'Wrong Error issued'
        )

    def test_invalid_asset_no_file(self):
        """
        Test opening a file that does not exist for asset preview window
        """
        # Simulate user adding a new asset
        asset_window = AssetWindow(self.md_editor, 200, 200, self.md_editor.get_asset_list())
        asset_window.chosen_type.set('Picture')
        pic_asset = asset_window.add_new_asset()
        pic_asset.PreviewImage(f'doesnotexist.png')

        error = asset_window.get_error_message()

        # error should be issued
        self.assertEqual(
            len(error),
            1,
            'Error not issued'
        )

        self.assertEqual(
            error[0][1][0],
            'Error in Image Asset - Unable to Open File',
            'Wrong Error issued'
        )

    # Test Asset Preview

    def test_adding_asset_entry(self) -> None:
        """
        Test adding an asset preview widget
        """

        # add a asset preview widget
        # simulate user changing option to Asset
        self.datafile_editor.chosen_para_type.set('Asset')
        asset_entry = self.datafile_editor.add_entry_point()

        # check if asset preview widget is added
        self.assertEqual(
            self.datafile_editor.content_frame.get_tracking_no(),
            1,
            'Entry point failed to be added'
        )

        # check if type of widget added is asset entry point
        self.assertIsInstance(
            asset_entry,
            AssetPreview,
            'Wrong type of entry point added'
        )

    def test_attaching_valid_asset(self) -> None:
        """
        Test attaching a valid asset onto asset preview widget
        """
        # Simulate user adding a new asset
        asset_window = AssetWindow(self.md_editor, 200, 200, self.md_editor.get_asset_list())
        asset_window.chosen_type.set('Picture')
        pic_asset = asset_window.add_new_asset()
        pic_asset.PreviewImage(f'{TEST_ASSET}/test.png')
        asset_window.save_data()

        # Simulate user adding the picture into a asset preview point
        self.datafile_editor.chosen_para_type.set('Asset')
        asset_preview = self.datafile_editor.add_entry_point()
        asset_preview.displaying_value = pic_asset.getData()
        asset_preview.error = False
        asset_preview.refreshPreview()

        check_errors = asset_preview.getError()
        self.assertTrue(
            len(check_errors) == 0,
            'Error issued even though everything is fine'
        )

    def test_export_valid_asset(self) -> None:
        """
        Test exporting a valid asset preview widget
        """

        # Simulate user adding a new asset
        asset_window = AssetWindow(self.md_editor, 200, 200, self.md_editor.get_asset_list())
        asset_window.chosen_type.set('Picture')
        pic_asset = asset_window.add_new_asset()
        pic_asset.PreviewImage(f'{TEST_ASSET}/test.png')
        asset_window.save_data()

        # Simulate user adding the picture into a asset preview point
        self.datafile_editor.chosen_para_type.set('Asset')
        asset_preview = self.datafile_editor.add_entry_point()
        asset_preview.displaying_value = pic_asset.getData()
        asset_preview.error = False
        asset_preview.refreshPreview()

        # attempt to export
        content = self.md_editor.GetContentData()
        error = self.md_editor.get_error_list()

        # Content should have the paragraph and asset preview
        # asset preview should have the image inside
        self.assertEqual(
            content,
            [
                ('asset', ('image', 'test', f'{TEST_ASSET}/test.png'))
            ],
            'Content not properly extracted'
        )

        # error should be completely empty
        self.assertEqual(
            len(error),
            0,
            'Error Message generated even though there should not be any'
        )

    def test_invalid_unused_asset(self):
        # Simulate user adding a asset preview point
        self.datafile_editor.chosen_para_type.set('Asset')
        self.datafile_editor.add_entry_point()
        # User did not choose what asset to preview

        # attempt to export
        error = self.md_editor.get_error_list()

        # error should be raised
        self.assertEqual(
            len(error),
            1,
            'Error Message not generated'
        )

        self.assertEqual(
            error[0][1][0],
            'Entry Frame is left unused, Remove if not needed',
            'Wrong error message generated'
        )


    def test_invalid_asset_removed_file(self):
        """
        Test exporting with a asset preview widget that contains
        a image that is removed from the asset list
        """
        # Simulate user adding a new asset
        asset_window = AssetWindow(self.md_editor, 200, 200, self.md_editor.get_asset_list())
        asset_window.chosen_type.set('Picture')
        pic_asset = asset_window.add_new_asset()
        pic_asset.PreviewImage(f'{TEST_ASSET}/test.png')
        asset_window.save_data()

        # Simulate user adding the picture into a asset preview point
        self.datafile_editor.chosen_para_type.set('Asset')
        asset_preview = self.datafile_editor.add_entry_point()
        asset_preview.displaying_value = pic_asset.getData()
        asset_preview.error = False
        asset_preview.refreshPreview()

        # Simulate user removing the asset from the asset list
        asset_window = AssetWindow(self.md_editor, 200, 200, self.md_editor.get_asset_list())
        pic_asset = asset_window.asset_frame.get_subframe(0)
        pic_asset.delete_self(confirm=False)
        asset_window.save_data()
        self.md_editor.data_editor.refresh_assets()

        # attempt to export
        error = self.md_editor.get_error_list()

        # error should be completely empty
        self.assertEqual(
            len(error),
            1,
            'Error Message not generated'
        )

        self.assertEqual(
            error[0][1][0],
            'Invalid Asset Chosen',
            'Wrong Error issued'
        )

    def tearDown(self) -> None:
        self.md_editor.destroy()

    @classmethod
    def tearDownClass(cls) -> None:
        App.main.destroy()

if __name__ == "__main__":
    unittest.main()