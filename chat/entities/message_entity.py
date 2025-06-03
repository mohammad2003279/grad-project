from chat.schemas.message_schema import MessageSchema

class MessageEntity:
    def __init__(self, information: MessageSchema):
        self.sender_id = information.sender_id
        self.receiver_id = information.receiver_id
        self.content = information.content
        self.sent_at = information.sent_at
        self.delivered_at = information.delivered_at
        self.status = information.status


'''
    the message status should be pending unless the use case decides otherwise
'''