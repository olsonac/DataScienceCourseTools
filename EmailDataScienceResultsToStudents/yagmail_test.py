import sys

import yagmail

# yagmail.register('olsonadatascience@gmail.com', 'DS!01@UoB')

contents="blah, blah, blah..."
ComponentName="assignment x"
email="a.c.olson@bham.ac.uk"
yag=yagmail.SMTP()
yag.send(to=email,\
        subject="Marks for component: "+ComponentName,\
        contents=contents)
print("Sending results for ",ComponentName," to ",email)