import unittest
from backup import BackUpTool
import os
import shutil


class Test(unittest.TestCase):
    def test_basic(self):
        but = BackUpTool()
        but.do_source_backup_directory('test_data')
        but.do_primary_backup_directory('other_path')
        but.do_info(None)
        but.do_init(None)
        but.do_status(None)
        but.do_backup(None)
        but.do_source_backup_directory('final_path')
        but.do_restore(None)
        but.do_quit(None)

        self.assertTrue(os.path.samefile(
            r'test_data\some_file.txt',
            r'final_path\some_file.txt'
        ))
        self.assertTrue(os.path.samefile(
            r'test_data\normal_folder\file.txt',
            r'final_path\normal_folder\file.txt'
        ))
        self.assertTrue(os.path.samefile(
            r'test_data\.hidden_folder\in_hidden.txt',
            r'final_path\.hidden_folder\in_hidden.txt'
        ))
        self.assertTrue(os.path.samefile(
            r'test_data\.hidden_file.txt',
            r'final_path\.hidden_file.txt'
        ))

if __name__ == "__main__":
    unittest.main()
