class customemail:
    
    def __init__(self, recipient, sender, senderPw, subject, message, attachmentLocation):
        self.recipient = recipient
        self.sender = sender
        self.senderPw = senderPw
        self.subject = subject
        self.message = message
        self.attachmentLocation = attachmentLocation
