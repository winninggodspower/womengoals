import subprocess
from flask import render_template

def send_volunteer_email_php(user_info):
        msg = render_template("volunteer_email.html", user = user_info)

        # Command to run the PHP script
        command = ['php', 'php_email_scripts/volunteer_email.php', 'Someone Volluntered To Womensgoal', msg]

        # Run the PHP script from Python
        subprocess.run(command)
        return

def send_contact_email_php(user_info):
        msg = render_template("contact_email.html", user = user_info)

        # Command to run the PHP script
        command = ['php', 'php_email_scripts/volunteer_email.php', 'Womensgoal Contact Form Was Filled', msg]

        # Run the PHP script from Python
        subprocess.run(command)
        return