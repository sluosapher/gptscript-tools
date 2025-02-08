#!/bin/bash

# Define a function to display the help message
display_help() {
    echo "Usage: $0 <email_addresses> <newer_than_days> <retrieval_count>"
    echo "<email_addresses> is the sender's email address. Multiple email addresses can be separated by commas."
    echo "<newer_than_days> is the number of days to look back for new emails. Use 0 to receive emails of all time."
    echo "<retrieval_count> is the number of emails to retrieve. Use 0 to retrieve all emails."
    echo "Fox example: <$0 \"user1@company1.com, user2@company2.com\" 7 10> will retrieve up to 10 emails newer than 7 days from the two users inboxes."
}
# Display the number of arguments passed to the script
echo "Number of arguments: $#"

# list all the arguments
echo "All arguments: $@"
# Display the first argument
echo "First argument: $1"
# Display the second argument
echo "Second argument: $2"
# Display the third argument
echo "Third argument: $3"


# Display the help message if the script is run without any arguments or with the -h flag
if [ "$#" -ne 3 ] || [ "$1" == "-h" ]; then
    #Print error message
    echo "Error: Invalid number of arguments"
    display_help
    exit 1
fi


EMAIL_ADDRESS=$1
NEWER_THAN_DAYS=$2
RETRIEVAL_COUNT=$3

DIR=/Users/sluo/development/gptscript-tools/
VENV=$DIR/venv/bin/activate

cd $DIR
source $VENV

cd $DIR/gmail

# exec python receive_by_address.py "$EMAIL_ADDRESS"
exec python receive_new_email.py --senders="$EMAIL_ADDRESS" --days=$NEWER_THAN_DAYS --retrieve=$RETRIEVAL_COUNT