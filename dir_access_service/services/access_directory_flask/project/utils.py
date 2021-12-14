# All required dependecies
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import pandas as pd
import datetime

from email.mime.base import MIMEBase

# from email import encoders
# from email.message import Message
# from email.mime.audio import MIMEAudio
# from email.mime.image import MIMEImage

import tempfile

# # #New: Needs pip install
# # from html5print import HTMLBeautifier
# # from pyquery import PyQuery as pq


#================================== HELPER FUNCTION - Add css to email table ====================================================================

# def add_css(html):
#     """Adds css style to html table.

#     Parameters: 
#     ----------
#     values: HTML table
#     dtypes: Triple quoted string 

#     Returns: HTML + CSS (for HTML table only)
#     -------

#     Credits: THOMAS 
#     ------- 

#     """
#     def set_row_color(index, tr):
#         if index % 2 == 0:
#             pq(tr).css({
#                 'background-color': '#eee',
#             })

#     d = pq(html)

#     d.find('table').css({
#         'border': 'none',
#         'border-collapse': 'collapse',
#     })

#     d.find('th').css({
#         'background-color': '#174887',
#         'color': 'white',
#         'text-align': 'left',
#     })

#     d.find('tbody tr').each(set_row_color)

#     d.find('th, td').css({
#         'padding': '5px',
#     })

#     d.find('td').css({
#         'border-top': '1px solid #dee2e6',
#     })

#     # html_out = htmlmin.minify(d.outer_html(), remove_empty_space=True)
#     html_out = HTMLBeautifier.beautify(d.outer_html(), 4)
#     #print(html_out)
#     return html_out 
# #----------------------------------------------------------------------


# def get_greeting():
#     import datetime
#     currentTime = datetime.datetime.now()
#     if currentTime.hour < 12:
#         return 'Good morning'
#     elif 12<= currentTime.hour < 18:
#         return 'Good afternoon'
#     else:
#         return 'Good evening'


def create_attachement(user_name):
    """Create html attachment by converting dataframe into html by using pandas to_html() method.

    Parameters:
    ----------

    values: DataFrame
    dtypes: DataFrame Object

    Returns: String representation of HTML.
    -------

    """
    attchments = f""" 
        <html>
            <head><title>Batch Upload Completed!</title> </head>
            <!-- main CSS -->
            <body>
                <p>
                    Hi {user_name}, <br><br>

                    <p>
                        New Batch Upload has been completed as of - {datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}
                    </p>

                        <br>
                        <p>(This is an automated email.)</p>
                        <br>
                
                        Thanks and Regards,<br>
                        Vida Analytics
                    </p>
                </p> 
            </body>
        </html>                            
        """
    return attchments

# #====================================================================================================================
# #CSV ATTACHMENT

# def csv_attchment(dataframe, file_name, send_from, send_to, server, username, password, SUBJECT, attachments=()):
#     # Create a temporary directory for the attachment
#     with tempfile.TemporaryDirectory() as tmpdir:
#         path = os.path.join(tmpdir, file_name)
#         with open(path, 'w', newline='\n') as fp:
#             # Write to the temporary file and send
# #             print(qle_df)
#             fp.write(dataframe.to_csv(index=False))
#             fp.flush()
#             fp.seek(0)
#             email_message = send_file(path, send_from, send_to, server, username, password, SUBJECT, attachments)
#         fp.close()
#         return email_message

# #====================================================================================================================

#General email sending function
def send_email(send_from, send_to, server, username, password, user_name, use_tls=True):
    """Sends email to Vida analytics team as a new request set value returns from create_new_request() method

    Parameters:

    values: String of email credentials
    dtypes: String

    Returns:  
    -------
    Print success message.

    """
    #assert isinstance(send_to, list)
    #Gets request status
    
    
    SUBJECT = f"Batch Upload Completed!"

    # email USER Credentials and Multipart message 
    msg = MIMEMultipart('alternative')
    msg['From'] = send_from
    #msg['To'] = COMMASPACE.join(send_to)
    msg['To'] = 'datta.tele@vidacapitalinc.com'
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = SUBJECT

    #attached_text = text + repr(new_delta_request)
    #if text:
    #    msg.preamble = text

    html_attachment = MIMEText(f"""{create_attachement(user_name)}""", 'html')
    msg.attach(html_attachment)
    print("Added attachedment to message")
    smtp = smtplib.SMTP(server)
    if use_tls:
        smtp.starttls()
    
    smtp.login(username, password)
    print("Completed login process")
    #print("Send from, to, msg: ", send_from, send_to, msg.as_string())
    smtp.sendmail(send_from, send_to, msg.as_string())
    print("Sent an email to user!")
    smtp.quit()
    #print("Sent an email to user!")
    #email_message = msg.as_string()
    #return email_message
    return msg.as_string()
    return "Nothing to send!"
