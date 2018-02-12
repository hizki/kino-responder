import imaplib
import time
import email

conn = imaplib.IMAP4_SSL('imap.gmail.com', port = 993)
conn.login(username,password)
conn.select('[Gmail]/Drafts')

conn.append("[Gmail]/Drafts",
            '',
            imaplib.Time2Internaldate(time.time()),
            str(email.message_from_string('TEST')))