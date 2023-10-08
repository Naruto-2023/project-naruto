def move():

    import imapclient
    import CRED

    imap_server = 'imap.gmail.com'

    with imapclient.IMAPClient(imap_server) as mail:
        mail.login(CRED.user, CRED.pw)
        source_mailbox = 'INBOX'
        target_mailbox = 'processed'
        mail.select_folder(source_mailbox)
        messages = mail.search(['NOT SEEN'])
        mail.move(messages, target_mailbox)
        mail.logout()