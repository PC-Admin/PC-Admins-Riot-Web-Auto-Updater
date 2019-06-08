

# PC-Admin's riot-web auto updater script.
#
# Install beautifulsoup4 with:
# $ sudo apt install python3-pip
# $ pip3 install beautifulsoup4
#
# Needs crontab:
# 0 0 1 * * /usr/bin/python3 /home/username/autoupdateriot/autoupdateriot.py

from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import re
import datetime

# returns the redirected link
def get_redirected_url(url):
    request = u.geturl(url)
    return request


# Python code to remove duplicate elements
def Remove_Duplicates(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


releaseurl = "https://github.com/vector-im/riot-web/releases/latest"

#connect to a URL

html = urlopen(releaseurl)
bsObj = BeautifulSoup(html.read(), "html.parser");

link_list = []

for link in bsObj.find_all('a'):
	#print(link.get('href'))
	link_list.append(link.get('href'))

# Contains final list of URLs
new_link_list = []

# compile list of relevant links

for link in link_list:
	if "tar.gz" in link:
		new_link_list.append(link)

for link in link_list:
	if "tar.gz.asc" in link:
		new_link_list.append(link)

# remove other unnecessary links

for link in new_link_list:
	if "archive" in link:
		new_link_list.remove(link)

for link in new_link_list:
	if "src" in link:
		new_link_list.remove(link)

# Remove duplicate links

new_link_list = Remove_Duplicates(new_link_list)

print("\nPrinting new link list!\n")
for link in new_link_list:
	print(link)

# Append links to be resolvable

new_link_list = [ "https://github.com" + x for x in new_link_list]

print("\nPrinting appended new link list!\n")
for link in new_link_list:
	print(link)


pre_file_names = []
file_names = []

for link in new_link_list:
	# Download the files
	stdoutdata = subprocess.getoutput("wget " + link)
	#print(stdoutdata)
	# Splits links into arrays of strings
	pre_file_names.append(link.split("/"))

# Collect file names from those arrays
file_names.append(pre_file_names[0][-1])
file_names.append(pre_file_names[1][-1])

print("\n")
for file_name in file_names:
	print(file_name + " was downloaded!\n")

# Collect riot version
riot_version = re.sub(".tar.gz","",file_names[0])

print("Riot version is: " + riot_version + "\n")

# Complete GPG Verification

stdoutdata = subprocess.getoutput("gpg --verify " + file_names[1] + " " + file_names[0])

print(stdoutdata)

# not collecting subprocess output correctly!! :(

if "Good signature from" in stdoutdata:
	print("\nGPG check has succeeded!")

	print("\nUnpacking .tar.gz file...")
	stdoutdata = subprocess.getoutput("tar -xf " + file_names[0])
	print(stdoutdata)

	print("Wiping old nginx files...")
	stdoutdata = subprocess.getoutput("sudo rm -r /usr/share/nginx/html/*")
	print(stdoutdata)

	print("Copying new riot-web files over...")
	stdoutdata = subprocess.getoutput("sudo cp -r ./" + riot_version + "/* /usr/share/nginx/html/")
	print(stdoutdata)

	print("Copying new modification files over...")
	stdoutdata = subprocess.getoutput("sudo cp -r /home/pcadmin/autoupdateriot/tocopy/* /usr/share/nginx/html/")
	print(stdoutdata)

	print("Restarting Nginx service...")
	stdoutdata = subprocess.getoutput("sudo service nginx restart")
	print(stdoutdata)

	# Clean up riot files!
	print("Cleaning up files...")
	stdoutdata = subprocess.getoutput("rm -r ./riot-*")
	print(stdoutdata)

	todays_date = datetime.datetime.today().strftime('%Y-%m-%d')
	print("Todays date:\n")
	print(todays_date)
	update_string = "Riot-web code update on " + todays_date + " to version: " + riot_version

	print("\nAppending to log...")
	stdoutdata = subprocess.getoutput("echo " + update_string + " >> /home/pcadmin/update_riot.log")
	#print(stdoutdata)

elif "Good signature from" not in stdoutdata:
	print("\nGPG check has failed!!! :(")

	print("\nAppending to log...")
	todays_date = datetime.datetime.today().strftime('%Y-%m-%d')
	stdoutdata = subprocess.getoutput("echo ERROR: GPG check failed on " + todays_date + " >> /home/pcadmin/update_riot.log")
	#print(stdoutdata)



