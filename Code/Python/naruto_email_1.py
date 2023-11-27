import imaplib
import email
import imapclient
import os

#from CRED import user, pw
#import t1

class naruto_email:
    def __init__(self,email_file_loc, email_arc_loc, email_user, email_password):
        self.n_email_file_loc = email_file_loc
        self.n_email_arc_loc = email_arc_loc
        self.n_email_user = email_user
        self.n_email_password = email_password
        print("inside naruto_email")



    def log_in(self):
        print("inside login")
        imap_server = "imap.gmail.com"
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(self.n_email_user, self.n_email_password)
        print("Login Successfully")
        return mail


    def download_file(self,mail):
        flag = 0
        try:
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
                                    filePath = os.path.join(self.n_email_file_loc, fileName)
                                    if not os.path.isfile(filePath):
                                        fp = open(filePath, 'wb')
                                        fp.write(part.get_payload(decode=True))
                                        print("File Downloaded successfully")
                                        fp.close()
        except Exception as err:
            flag = -1
            print("Error Occured while downloading the email attachments",str(err))
            os._exit(-1)

        return flag


    def move_file_to_processed_folder(self):
        print("Inside move_file_to_processed_folder")
        flag = 0
        try:
            imap_server = 'imap.gmail.com'

            with imapclient.IMAPClient(imap_server) as mail:
                mail.login(self.n_email_user,self.n_email_password)
                print("line77",mail)
                source_mailbox = 'INBOX'
                target_mailbox = 'processed'
                mail.select_folder(source_mailbox)
                messages = mail.search(['SEEN'])
                mail.move(messages, target_mailbox)
                mail.logout()
            print("Successfully moved the file into Processed folder")

        except Exception as err:
            flag = -1
            print("Error occured while moving the file into processed  folder")
            os._exit(-1)
        return flag

    def log_out(self,mail):
        mail.close()
        mail.logout()
        print("logged out from email")




def code_start(email_file_loc, email_arc_loc, email_user, email_password):
    naruto = naruto_email(email_file_loc, email_arc_loc, email_user, email_password)

    #Step 1 Logging into Email Server
    login_object = naruto.log_in()

    #Step 2 Downlaod the file from email
    naruto.download_file(login_object)

    # Step 3 Loggin out from the email
    naruto.log_out(login_object)

    #Step 4 Moving the mails to Processed Folder
    naruto.move_file_to_processed_folder()





   # mail = log_in()
    #download_file(mail)
    #log_out(mail)
    # try:
    #     t1.move()
    # except Exception as err:
    #     print("NO FILE FOUND", err)