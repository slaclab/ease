'''
Convenience wrapper for email functionality. Setup with alerts in mind 

heavily copied from : https://docs.python.org/3/library/email-examples.html


'''
# Import smtplib for the actual sending function                                
import smtplib                                                                  
                                                                                
# Import the email modules we'll need                                           
from email.mime.text import MIMEText                                            
from email.mime.multipart import MIMEMultipart                                           
                               
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class EmailWrapper:
    """
    Convenience tool for EASE's email sending
    """
    def __init__(self, host, host_email):
        """
        Get information required to configure server at each send.

        Parameters
        ----------
        host : string
            name of the server (e.g. 'psmail')

        host_email : string
            name of sending email. For example: use "EASE" to send emails from
            EASE@slac.stanford.edu. 
        """
        self.host = host
        self.host_email = host_email
    
    
    def send_file(self, to, subj, textfile):
        """
        send file's contents as email

        Paramters
        ---------
        to : string
            full email of intended recipient

        subj : string
            subject line for email

        textfile : string
            path to text file being sent
        """
        # Open a plain text file for reading.  For this example, assume that            
        # the text file contains only ASCII characters.                                 
        with open(textfile) as fp:                                                      
            # Create a text/plain message                                               
            msg = MIMEText(fp.read())                                                   
                                                                                        
        # me == the sender's email address                                              
        # you == the recipient's email address                                          
        msg['Subject'] = subj                             
        msg['From'] = self.host_email                                                            
        msg['To'] = to
                                                                                        
        # Send the message via our own SMTP server.                                     
        s = smtplib.SMTP(self.host)                                                      
        s.send_message(msg)                                                             
        s.quit()


    def send_text(self, to, subj, content):
        """
        send string as contents of email

        Paramters
        ---------
        to : string
            full email of intended recipient

        subj : string
            subject line for email

        textfile : string
            text to place in email
        """

        msgRoot = MIMEMultipart()
        text = content
        email_part = MIMEText(text,'plain')
        msgRoot.attach(email_part)
        
        msgRoot['Subject'] = subj
        msgRoot['From'] = self.host_email
        if type(to) == list:
            msgRoot['To'] = ",".join(to)
        else:
            msgRoot['To'] = to

        # Send the message via our own SMTP server.  
        s = smtplib.SMTP(self.host)  
        s.send_message(msgRoot)    
        s.quit()

    def send_html(self, to, subj, content):
        """
        send html as contents of email

        Paramters
        ---------
        to : string
            full email of intended recipient

        subj : string
            subject line for email

        textfile : string
            html to place in email
        """
        msgRoot = MIMEMultipart()
        text = content
        email_part = MIMEText(text,'html')
        msgRoot.attach(email_part)
        
        msgRoot['Subject'] = subj
        msgRoot['From'] = self.host_email
        if type(to) == list:
            msgRoot['To'] = ",".join(to)
        else:
            msgRoot['To'] = to
            
 
        # Send the message via our own SMTP server.                                     
        s = smtplib.SMTP(self.host)                                                      
        try:
            s.sendmail(self.host_email,to,msgRoot.as_string())
        except smtplib.SMTPRecipientsRefused:                                   
            logging.error('All recipient addresses refused.')            
        except smtplib.SMTPDataError:                                           
            logging.error('The SMTP server refused to accept the message data.')
        except smtplib.SMTPConnectError:                                        
            logging.error('Error occurred during establishment of a connection with the server.')
        except smtplib.SMTPHeloError:                                           
            logging.error('The server refused our HELO message.')
        except smtplib.SMTPException:
            logging.error('SMTPlib failed to send email')

        s.quit()


    def html_wrapper(self,msg):
        """
        Convenience function for wrapping html with boilerplate header/footer.

        Paramters
        ---------
        msg : string
            string to be wrapped in html header and footer. html formatted
            message is reccommended. 
        """
        header = """
            <html>
            <body>
            <head></head>
            <body>
        """
        footer = """
            </body>
            </html>
        """
        return header + msg + footer

if __name__ == '__main__':
    u = EmailWrapper('psmail','EASE')
    to = 'email@email.com'
    u.send_file(to,'file','ex.txt')
    u.send_text(to,'test_text','sample email contents')
    u.send_html(to,'test_html',
        """\
        <html>
        <head></head>
            <body>
                <p>Hi!<br>
                How are you?<br>
                Here is the <a href="https://www.python.org">link</a>
                you wanted.
                </p>
            </body>
        </html>
        """
    )

    u.send_html(to,'wrapped_msg',u.html_wrapper("hi"))








