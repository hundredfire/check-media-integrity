import os
import shutil
import unittest
from unittest.mock import patch
from io import StringIO
import sys
from check_mi import main

class TestFolderExclusion(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_temp_dir'
        os.makedirs(os.path.join(self.test_dir, 'folder1', 'subfolder1'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'folder2', 'subfolder2'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'folder3'), exist_ok=True)

        with open(os.path.join(self.test_dir, 'folder1', 'file1.txt'), 'w') as f:
            f.write('file1')
        with open(os.path.join(self.test_dir, 'folder1', 'subfolder1', 'file2.txt'), 'w') as f:
            f.write('file2')
        with open(os.path.join(self.test_dir, 'folder2', 'file3.txt'), 'w') as f:
            f.write('file3')
        with open(os.path.join(self.test_dir, 'folder2', 'subfolder2', 'file4.txt'), 'w') as f:
            f.write('file4')
        with open(os.path.join(self.test_dir, 'folder3', 'file5.txt'), 'w') as f:
            f.write('file5')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('check_mi.arg_parser')
    @patch('sys.stdout', new_callable=StringIO)
    def test_exclude_one_folder(self, mock_stdout, mock_arg_parser):
        excluded_folder = os.path.join(self.test_dir, 'folder2')
        mock_arg_parser.return_value.checkpath = self.test_dir
        mock_arg_parser.return_value.is_recurse = True
        mock_arg_parser.return_value.excluded_folders = [excluded_folder]
        mock_arg_parser.return_value.is_disable_image = True
        mock_arg_parser.return_value.is_enable_media = True
        mock_arg_parser.return_value.is_disable_pdf = True
        mock_arg_parser.return_value.is_disable_extra = True
        mock_arg_parser.return_value.timeout = 120
        mock_arg_parser.return_value.threads = 1
        mock_arg_parser.return_value.zero_detect = 0
        mock_arg_parser.return_value.csv_filename = None
        main()
        self.assertIn('Number of bad/processed files: 0 / 3', mock_stdout.getvalue())

    @patch('check_mi.arg_parser')
    @patch('sys.stdout', new_callable=StringIO)
    def test_exclude_multiple_folders(self, mock_stdout, mock_arg_parser):
        excluded_folder1 = os.path.join(self.test_dir, 'folder1')
        excluded_folder2 = os.path.join(self.test_dir, 'folder3')
        mock_arg_parser.return_value.checkpath = self.test_dir
        mock_arg_parser.return_value.is_recurse = True
        mock_arg_parser.return_value.excluded_folders = [excluded_folder1, excluded_folder2]
        mock_arg_parser.return_value.is_disable_image = True
        mock_arg_parser.return_value.is_enable_media = True
        mock_arg_parser.return_value.is_disable_pdf = True
        mock_arg_parser.return_value.is_disable_extra = True
        mock_arg_parser.return_value.timeout = 120
        mock_arg_parser.return_value.threads = 1
        mock_arg_parser.return_value.zero_detect = 0
        mock_arg_parser.return_value.csv_filename = None
        main()
        self.assertIn('Number of bad/processed files: 0 / 2', mock_stdout.getvalue())

    @patch('check_mi.arg_parser')
    @patch('sys.stdout', new_callable=StringIO)
    def test_exclude_subfolder(self, mock_stdout, mock_arg_parser):
        excluded_folder = os.path.join(self.test_dir, 'folder1', 'subfolder1')
        mock_arg_parser.return_value.checkpath = self.test_dir
        mock_arg_parser.return_value.is_recurse = True
        mock_arg_parser.return_value.excluded_folders = [excluded_folder]
        mock_arg_parser.return_value.is_disable_image = True
        mock_arg_parser.return_value.is_enable_media = True
        mock_arg_parser.return_value.is_disable_pdf = True
        mock_arg_parser.return_value.is_disable_extra = True
        mock_arg_parser.return_value.timeout = 120
        mock_arg_parser.return_value.threads = 1
        mock_arg_parser.return_value.zero_detect = 0
        mock_arg_parser.return_value.csv_filename = None
        main()
        self.assertIn('Number of bad/processed files: 0 / 4', mock_stdout.getvalue())

    @patch('check_mi.arg_parser')
    @patch('sys.stdout', new_callable=StringIO)
    def test_exclude_with_hash(self, mock_stdout, mock_arg_parser):
        folder_with_hash = os.path.join(self.test_dir, 'folder#4')
        os.makedirs(folder_with_hash, exist_ok=True)
        with open(os.path.join(folder_with_hash, 'file6.txt'), 'w') as f:
            f.write('file6')

        mock_arg_parser.return_value.checkpath = self.test_dir
        mock_arg_parser.return_value.is_recurse = True
        mock_arg_parser.return_value.excluded_folders = [folder_with_hash]
        mock_arg_parser.return_value.is_disable_image = True
        mock_arg_parser.return_value.is_enable_media = True
        mock_arg_parser.return_value.is_disable_pdf = True
        mock_arg_parser.return_value.is_disable_extra = True
        mock_arg_parser.return_value.timeout = 120
        mock_arg_parser.return_value.threads = 1
        mock_arg_parser.return_value.zero_detect = 0
        mock_arg_parser.return_value.csv_filename = None
        main()
        self.assertIn('Number of bad/processed files: 0 / 5', mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
