# Configure postfix as relay for macOS Sierra – Sonoma
My purpose is to be able to send emails from my macOS terminal using postfix as a relay, so my AI agent in gptscript can send me emails.

I followed the original source https://gist.github.com/loziju/66d3f024e102704ff5222e54a4bfd50e, but with some modifications.

## 1. Create a new Gmail account
I suggest to create a new Gmail account for this purpose. That means, the AI agent will use a separate email account to send emails to you, and it will not mess up with your primary email account.

1. Register a new Gmail account, such as myagent@gmail.com. In the rest of this instruction, I will call this email address as 'agent email address'.

2. For better security, follow [this instruction](https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237) to create an app password for the agent email address. This app password will be used as the password in the postfix configuration.

## 2.  Edit postfix configuration file

1.  `sudo vi /etc/postfix/main.cf`
2.  Ensure that the following values are set:
    ```
    mail_owner = _postfix
    setgid_group = _postdrop
    ```
3.  Add the following lines at the end of the file:
    ```
    # Postfix as relay
    #
    #Gmail SMTP
    relayhost=smtp.gmail.com:587
    #Hotmail SMTP
    #relayhost=smtp.live.com:587
    #Yahoo SMTP
    #relayhost=smtp.mail.yahoo.com:465
    # Enable SASL authentication in the Postfix SMTP client.
    smtp_sasl_auth_enable=yes
    smtp_sasl_password_maps=hash:/etc/postfix/sasl_passwd
    smtp_sasl_security_options=noanonymous
    smtp_sasl_mechanism_filter=plain
    # Enable Transport Layer Security (TLS), i.e. SSL.
    smtp_use_tls=yes
    smtp_tls_security_level=encrypt
    tls_random_source=dev:/dev/urandom
    ```

## 3.  Create sasl_passwd file

1.  `sudo sh -c 'echo "\nsmtp.gmail.com:587 myagent@gmail.com:agent_password" >> /etc/postfix/sasl_passwd'`
    Replace myagent@gmail.com and agent_password with actual values of the agent email address and the app password.
2.  `sudo postmap /etc/postfix/sasl_passwd`

## 4.  Autorun postfix on boot and restart postfix

1.  Copy the postfix master plist out of System folder.
    ```
    sudo cp /System/Library/LaunchDaemons/com.apple.postfix.master.plist /Library/LaunchDaemons/org.postfix.custom.plist
    ```
2.  `sudo vi /Library/LaunchDaemons/org.postfix.custom.plist`
3.  Change the label value from `com.apple.postfix.master` to `org.postfix.custom`

    Remove these lines to prevent exiting after 60s
    ```
      <string>-e</string>
      <string>60</string>
    ```
    Add these lines before `</dict>`
    ```
      <key>KeepAlive</key>
      <true/>
      <key>RunAtLoad</key>
      <true/>
    ```
6.  Relaunch the daemon.
    ```
    sudo launchctl unload /Library/LaunchDaemons/org.postfix.custom.plist
    sudo launchctl load /Library/LaunchDaemons/org.postfix.custom.plist
    ```
7.  Check that daemon has started.
    ```
    sudo launchctl list | grep org.postfix
    ```

## 5.  Test

1.  `echo "Test sending email from Postfix" | mail -s "Test Postfix" recipient@domain.com`

    Change `recipient@domain.com` with a valid email with mailbox access for easy checking. The email will be sent from the agent email address.
2.  Check mail queue and possible delivery errors with `mailq`.
3.  Check mail log with `tail -f /var/log/mail.log`.