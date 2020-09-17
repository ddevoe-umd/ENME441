#!/usr/bin/python3

# Utility to modify Pi system files to install
# the ssmtp email utility, and set up the rc.local file to automatically
# email the Pi IP address on boot.  
#
# Instructions:
#   1. Set up your Gmail account.  You MUST use a non-UMD Gmail account. It
#      it recommended that you set up a "junk" account to use just for this
#      class.  Do the following:
#         A. Choose a password without symbols. In particilar "%", "#", and 
#            "\" may cause problems.
#         B. From a web browser on your laptop, log into the Gmail account.
#         C. Click your account icon, and select the "Google Account" button.
#         D. Under "Sign in & Security" scroll down to "Allow less secure apps"
#            and switch this option to ON.
#
#  2. Run setup.py from a terminal:

#            sudo python3 setup.py           
#
#      Follow all on-screen instructions carefully!
#
# If everything went well, you can now shut down the Pi from the desktop, or
# by typing the following into the terminal:
#            sudo shutdown -h now
#
# If you made an error in one of your usernames or passwords, you can
# re-run the setup.py utility.

import subprocess
from os import system
import sys


def fileout(filepath, lines, permissions=0):
  # if permissions are provided, assume a new file is desired,
  # otherwise append to an existing file:
  if permissions:  
    write_or_append = 'w+'  # overwrite existing file
  else:
    write_or_append = 'a'   # append to file
  # Edit the file:
  try:
    f = open(filepath, write_or_append)
  except Exception as e:
    print("\n\nError while accessing " + filepath + " : \n", e, "\n\n")
  else: # write all lines to new file
    for line in lines:
      f.write(line)
      f.write('\n')
  finally:
    f.close()
  if permissions:
    system('sudo chmod ' + permissions + ' ' + filepath)
    system('sudo chown root ' + filepath)
    system('sudo chgrp root ' + filepath)



def main():
  
  # ********************************************************************
  # startup:
  system('clear')
  # should really use subprocess instead of os.system here, but the
  # syntax for some commands is simple enough that os.system works ok
  print("\n                    ENME441 Pi Email Setup")
  print("==================================================================")
  print("Your Pi must be connected to the Internet when running this code,\n")
  print("and the code MUST be run as sudo!\n")
  print("When prompted, enter all requested information. If prompted with")
  print("just 'Password:' alone, enter the password for the Pi user")
  print("(default password = raspberry)\n")
  print("==================================================================\n")

 
  # ********************************************************************
  # msmtp.conf mail utility setup:
  print("\nGmail setup")
  print("---------------------\n")
  print('Enter your Gmail account info. Your UMD Gmail address WILL')
  print('NOT WORK -- you must use a PERSONAL Gmail account to allow')
  print('the Pi to send emails through Gmail.\n')
  username = input('Enter your Gmail username: ').strip()
  password = input('Enter your Gmail password: ').strip()
  # get rid of anything beyond the username itself, 
  # e.g. remove "@gmail.com":
  idx = username.find("@")
  if idx>0:
    username = username[:idx]
  username = username.strip() 
  print("\nUpdating apt-get, please wait... (enter Pi password if asked)")
  system('sudo apt-get update')
  print("Installing msmtp...")
  system('sudo apt-get install msmtp ca-certificates')
  print("\nmsmtp mail utility has been installed\n")
  filepath = "/etc/msmtprc"
  lines = [
    'account default',
    'host smtp.gmail.com',
    'port 587',
    'logfile /tmp/msmtp.log',
    'tls on',
    'tls_starttls on',
    'tls_trust_file /etc/ssl/certs/ca-certificates.crt',
    'auth on',
    'user ' + username + '@gmail.com',
    'password ' + password ]
  fileout(filepath, lines, '666')
  print(filepath + " has been updated\n")
  

  # ********************************************************************
  # rc.local setup:
  print('Setting up /etc/rc.local for IP email at boot...')
  filepath = "/etc/rc.local"
  lines = [
    '#!/bin/sh -e',
    '#',
    '# This script is executed at the end of each multiuser runlevel.',
    '# To enable or disable this script change the execution bits',
    '#',
    '# Print the IP address',
    '_IP=$(hostname -I) || true',
    'if [ "$_IP" ]; then',
    '  printf "IP address = %s\n" "$_IP"',
    'fi',
    '',
    'sleep 15',
    'message="Pi IP = $(hostname -I)"',
    'echo "Subject: $message" |msmtp --from=default -t '+username+'@gmail.com'
    '',
    'exit 0'  ]
  fileout(filepath, lines, '755')
  print(filepath + " has been updated\n")


  # ********************************************************************
  # Enable wait for network at boot:
  system('sudo raspi-config nonint do_boot_wait 0')
  print('Wait for network at boot enabled\n')


  # ********************************************************************
  # all done:
  print('**************************************\nSetup complete.\n')
  print('If you made an error in your username or password, run the')
  print('utility again to correct the entries.\n')
  print('Before rebooting or shutting down, reconnect to your current')
  print('WiFi network using the GUI to ensure that it is entered into')
  print('the wpa_supplicants.conf file.\n')
  print('After connecting your WiFi, reboot via "sudo reboot" or')
  print('shutdown your via "sudo shutdown -h."\n')


if __name__ == "__main__":
  main()

