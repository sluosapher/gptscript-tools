import argparse
from simplegmail import Gmail
from simplegmail.query import construct_query

class GmailMessage:
    datetime: str  # date and time the email was sent
    sender:str  # email address of the sender
    subject:str  # subject of the email
    html:str  # html content of the email
    text:str  # text content of the email
    
AGENT_LABEL = "read_by_agent"

def receive_new_email(senders:list, days:int, retrieve:int=1)->list[GmailMessage]:
    '''
    Receive specified number of new emails from gmail inbox sent by the senders in the list, and received in the last days days.
    Return a list of GmailMessage objects.
    Parameters:
    - senders: list of email addresses of the senders. If empty, emails from all senders will be received.
    - days: 0 or positive interger. number of days to look back for new emails. If 0, all emails of all time will be received.
    - retrieve: 0 or positive interger. number of emails to retrieve. If 0, all emails will be received.
    '''
    # check if days is a non-negative integer
    if not isinstance(days, int) or days < 0:
        raise ValueError("days should be a non-negative integer.")
    
    # check if retrieve is a non-negative integer
    if not isinstance(retrieve, int) or retrieve < 0:
        raise ValueError("retrieve should be a non-negative integer.")
   
    
    # Construct the query. If days is 0, don't include it in the query.
    if days == 0:
        query_params = {
            'unread': True,
            'sender': senders
        }
    else:
        query_params = {
            'newer_than': (days, "day"),
            'unread': True,
            'sender': senders
        }

    gmail = Gmail()

    labels = gmail.list_labels()

    # To find a label by the name that you know (just an example):
    read_by_agent_label = list(filter(lambda x: x.name == AGENT_LABEL, labels))[0]


    # construct_query() will create both query strings and "or" them together.
    messages = gmail.get_messages(query=construct_query(query_params))

    # if retrieve>0, retrieve only the first 'retrieve' messages
    if retrieve > 0:
        # print(f"retrieving {retrieve} messages")
        messages = messages[:retrieve]

    allMessages = []

    for message in messages:
        # add label to the message
        message.add_label(read_by_agent_label)

        # mark the message as read
        message.mark_as_read()

        # create a GmailMessage object
        gmailMessage = GmailMessage()
        gmailMessage.datetime = message.date
        gmailMessage.sender = message.sender
        gmailMessage.subject = message.subject
        gmailMessage.html = message.html
        # gmailMessage.text = message.plain

        allMessages.append(gmailMessage)
    
    return allMessages

def main():
    parser = argparse.ArgumentParser(description='Receive new emails from gmail inbox sent by the senders in the list, and received in the last days days.')
    parser.add_argument('--senders', type=str, help='list of email addresses of the senders, separated by comma. If empty, emails from all senders will be received.')
    parser.add_argument('--days', type=int, help='number of days to look back for new emails')
    parser.add_argument('--retrieve', type=int, default=1, help='number of emails to retrieve. If 0, all emails will be received.')

    args = parser.parse_args()

    if args.senders:
        if len(args.senders.strip())>0:
            senders = args.senders.split(",")
            # trim the spaces
            senders = [sender.strip() for sender in senders]
        else:
            senders = []
    else:
        senders = []
        

    days = args.days
    retrieve = args.retrieve

    messages = receive_new_email(senders, days, retrieve)




    if len(messages) > 0:
        print(f"the length of messages is {len(messages)}")
        print("Received messages: ")
        for message in messages:
            print("Sender: " + message.sender)
            print("Subject: " + message.subject)
            print("html Content: \n\n" + message.html)
            # print("Text Content: \n\n" + message.text)
            print("-------------------------------------------------")
    else:
        print("No new messages received")



if __name__ == "__main__":
# # Users should call this program by specifying the senders and days. Example:
# # python receive_new_email.py --senders="user1@company1.com, user2@company2.com", --days=1 --retrieve=2

#     parser = argparse.ArgumentParser(description='Receive new emails from gmail inbox sent by the senders in the list, and received in the last days days.')
#     parser.add_argument('--senders', type=str, help='list of email addresses of the senders, separated by comma. If empty, emails from all senders will be received.')
#     parser.add_argument('--days', type=int, help='number of days to look back for new emails')
#     parser.add_argument('--retrieve', type=int, default=1, help='number of emails to retrieve. If 0, all emails will be received.')

#     args = parser.parse_args()

#     senders = args.senders.split(",") if args.senders else []
#     # trim the spaces
#     senders = [sender.strip() for sender in senders]

#     days = args.days
#     retrieve = args.retrieve

#     messages = receive_new_email(senders, days, retrieve)
#     print("Received messages: ")
#     for message in messages:
#         print("Sender: " + message.sender)
#         print("Subject: " + message.subject)
#         print("html Content: \n\n" + message.html)
#         # print("Text Content: \n\n" + message.text)
#         print("-------------------------------------------------")

    main()


   