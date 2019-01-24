import unittest
from tests.utils import MailboxTestCase, test_mailbox_name_set, get_test_mailbox


class FoldersTest(MailboxTestCase):
    @classmethod
    def setUpClass(cls):
        # delete temp new folders
        for test_mailbox_name in test_mailbox_name_set:
            mailbox = get_test_mailbox(test_mailbox_name)
            for del_folder in (mailbox.folder_test_new, mailbox.folder_test_new1):
                if mailbox.folder.exists(del_folder):
                    mailbox.folder.delete(del_folder)

    def test_folders(self):
        for mailbox_name, mailbox in self.mailbox_set.items():
            if mailbox_name == 'MAIL_RU':
                continue
            # _pairs_to_dict
            self.assertEqual(mailbox.folder._pairs_to_dict(['a', '1', 'b', '2']), dict(a='1', b='2'))
            with self.assertRaises(ValueError):
                mailbox.folder._pairs_to_dict(['1', '2', '3'])
            # LIST
            folder_list = mailbox.folder.list(mailbox.folder_test)
            self.assertEqual(
                set([i['name'] for i in folder_list]),
                {mailbox.folder_test_base, mailbox.folder_test_temp1, mailbox.folder_test_temp2}
            )
            for folder in folder_list:
                self.assertIs(type(folder['flags']), str)
                self.assertIs(type(folder['delim']), str)
                self.assertIs(type(folder['name']), str)
            # SET, GET
            mailbox.folder.set(mailbox.folder_test_base)
            self.assertEqual(mailbox.folder.get(), mailbox.folder_test_base)
            # CREATE
            mailbox.folder.create(mailbox.folder_test_new)
            folder_list_names = [i['name'] for i in mailbox.folder.list(mailbox.folder_test)]
            self.assertTrue(mailbox.folder_test_new in folder_list_names)
            # EXISTS
            self.assertTrue(mailbox.folder.exists(mailbox.folder_test_new))
            # RENAME
            mailbox.folder.rename(mailbox.folder_test_new, mailbox.folder_test_new1)
            folder_list_names = [i['name'] for i in mailbox.folder.list(mailbox.folder_test)]
            self.assertTrue(mailbox.folder_test_new1 in folder_list_names)
            self.assertFalse(mailbox.folder_test_new in folder_list_names)
            # DELETE
            mailbox.folder.delete(mailbox.folder_test_new1)
            folder_list_names = [i['name'] for i in mailbox.folder.list(mailbox.folder_test)]
            self.assertFalse(mailbox.folder_test_new1 in folder_list_names)
            # STATUS
            for status_key, status_val in mailbox.folder.status(mailbox.folder_test_base).items():
                self.assertIs(type(status_key), str)
                self.assertIs(type(status_val), str)


if __name__ == "__main__":
    unittest.main()
