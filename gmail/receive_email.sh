#!/bin/bash

# The syntax for calling this script is:
# ./receive_email.sh "<email_address>, <email_address>, ..." <newer_than_days> <retrieval_count>
# Parameters:
# <email_address> is the email address to receive emails from. Multiple email addresses can be separated by commas.
# <newer_than_days> is the number of days to look back for new emails.
# <retrieval_count> is the number of emails to retrieve.

# check if the script is run with 3 arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <email_address> <newer_than_days> <retrieval_count>"
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