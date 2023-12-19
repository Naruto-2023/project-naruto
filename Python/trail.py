import imaplib
import email
import os
from CRED import user, pw
import t1


def log_in():
    imap_server = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(user, pw)
    print("Login Successfully")
    return mail


def download_file(mail):
    mail.select("Inbox")
    data = mail.search(None, 'ALL')
    mail_ids = data[1]
    id_list = mail_ids[0].split(b' ')
    first_email = int(id_list[0])
    latest_email = int(id_list[-1])

    for i in range(latest_email, 0, -1):
        data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_bytes(arr[1])
                email_sub = msg['subject']
                email_date = msg['date']
                print(email_sub)
                if email_sub == 'school_data' or email_sub == 'SCHOOL_DATA':
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
                        fileName = part.get_filename()
                        if bool(fileName):
                            filePath = os.path.join('C:/marksheets', fileName)
                            if not os.path.isfile(filePath):
                                fp = open(filePath, 'wb')
                                fp.write(part.get_payload(decode=True))
                                print("File Downloaded successfully")
                                fp.close()


def log_out(mail):
    mail.close()
    mail.logout()
    print("logged out from email")


mail = log_in()
download_file(mail)
log_out(mail)
try:
    t1.move()
except Exception as err:
    print("NO FILE FOUND", err)
