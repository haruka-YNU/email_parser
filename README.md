# email_parser

email_parser is based on the python2 eamil module.
email_parser can help you to extract header informations and mail content from a .eml file. 
Also can help you to save the attachment to the place you want.

## Requirements
1. You need Python 2.7 or later  
2. lxml python packages is installed 
```
sudo pip install lxml
```

## The installation

To clone the whole project into your computer.
And *cd* into the project folder.
To run this command
```
python setup.py install
```
If there are any permissions issues, try to use *sudo*.

## Example usages

email_parser is designed to be used as an API for other tools. The following is
an example of how to use the email_parser API in your own Python tools:

```python
from email_parser import parser
from pprint import pprint

#First you need to instantiate a parser object
#Two parameters is needed here
#The first one is the path of the .eml file that you want to parse.
#The second one is the path of saving attachments 
par = parser('path/to/emlfile', 'path/to/saving_attachments')
result = par.parse_email()
pprint(result)
```

Example output:

```
{
 'Attachment': ['Tata Claim Form 1.docx'],
 'AttachmentHash': ['df8c59f8392588681b09288338ade4a4'],
 'AttachmentType': ['.docx'],
 'FileHash': 'd41d8cd98f00b204e9800998ecf8427e',
 'FileName': 'sample1.eml',
 'MailArticle': '\n'
                '\n'
                'CONGRATULATIONS!\n'
                '\n'
                'YOUR EMAIL ID/IDENTITY HAS EMERGED AS ONE OF OUR LUCKY '
                'WINNERS IN THE\n'
                '2016 TATA EMAIL AWARD WIN PROMO. TO CLAIM YOUR WON PRIZE, '
                'KINDLY CHECK\n'
                'THE ATTACHED TATA CLAIM FORM,\n'
                'FILL UP YOUR BIO DATA CORRECTLY AND SEND TO OUR CLAIMS '
                'DEPARTMENT VIA\n'
                'EMAIL ID:uktataclaims@mit.tc FOR IMMEDIATE PROCESSING.\n'
                '\n'
                'REGARDS,\n'
                'TATA TEAM.\n',
 'MailCc': None,
 'MailDate': '2017-03-15 22:21:04+00:00',
 'MailID': '<201703152221.v2FML42I005385@rs101.zol.co.zw>',
 'MailReceiver': 'uktataclaims@mit.tc',
 'MailSender': '"TATA GROUP LONDON UK" <tata.mailselector@info.org.uk>',
 'MailSubject': 'PREMIUM SELECTION',
 'Urls': None
}
```

Copyright (c) 2017 haruka
