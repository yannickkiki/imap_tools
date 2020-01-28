import os
import unittest
import datetime
from tests.utils import MailboxTestCase

from tests.data import MESSAGE_ATTRIBUTES
from imap_tools import MailMessage


class MessageTest(MailboxTestCase):

    def test_live(self):
        none_type = type(None)
        for mailbox in self.mailbox_set.values():
            mailbox.folder.set(mailbox.folder_test_base)
            for message in mailbox.fetch():
                self.assertIn(type(message.uid), (str, none_type))
                self.assertIs(type(message.subject), str)
                self.assertIs(type(message.from_), str)
                self.assertIn(type(message.from_values), (dict, none_type))
                self.assertIs(type(message.date), datetime.datetime)
                self.assertIs(type(message.date_str), str)
                self.assertIs(type(message.text), str)
                self.assertIs(type(message.html), str)
                self.assertIs(type(message.headers), dict)

                self.assertIs(type(message.to), tuple)
                for i in message.to:
                    self.assertIs(type(i), str)
                self.assertIs(type(message.to_values), tuple)
                for i in message.to_values:
                    self.assertIs(type(i), dict)

                self.assertIs(type(message.cc), tuple)
                for i in message.cc:
                    self.assertIs(type(i), str)
                self.assertIs(type(message.cc_values), tuple)
                for i in message.cc_values:
                    self.assertIs(type(i), dict)

                self.assertIs(type(message.bcc), tuple)
                for i in message.bcc:
                    self.assertIs(type(i), str)
                self.assertIs(type(message.bcc_values), tuple)
                for i in message.bcc_values:
                    self.assertIs(type(i), dict)

                self.assertIs(type(message.flags), tuple)
                for i in message.flags:
                    self.assertIs(type(i), str)

                for att in message.attachments:
                    self.assertIs(type(att.filename), str)
                    self.assertIs(type(att.content_type), str)
                    self.assertIs(type(att.payload), bytes)

    def test_attributes(self):
        msg_attr_set = {'subject', 'from_', 'to', 'cc', 'bcc', 'date', 'date_str', 'text', 'html',
                        'headers', 'from_values', 'to_values', 'cc_values', 'bcc_values'}
        att_attr_set = {'filename', 'content_type', 'payload'}
        for file_name in MESSAGE_ATTRIBUTES.keys():
            message_data = MESSAGE_ATTRIBUTES[file_name]
            for msg_path in ('../tests/messages/{}.eml'.format(file_name), 'tests/messages/{}.eml'.format(file_name)):
                if not os.path.exists(msg_path):
                    continue
                with open(msg_path, 'rb') as f:
                    bytes_data = f.read()
            message = MailMessage.from_bytes(bytes_data)
            for msg_attr in msg_attr_set:
                self.assertEqual(getattr(message, msg_attr), message_data[msg_attr])
            for att_i, att in enumerate(message.attachments):
                for att_attr in att_attr_set:
                    self.assertEqual(getattr(att, att_attr), message_data['attachments'][att_i][att_attr])


if __name__ == "__main__":
    unittest.main()
