from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from  selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import csv
import socket
import nmap
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#path = "C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(path)
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://myip.ms/")
print(driver.title)
'''
search = driver.find_element(By.ID,"query")
'''
search = driver.find_element(By.ID,'home_txt')
search_input_by_user = input("Enter the name of the person that you looking for: ")
search.send_keys(str(search_input_by_user))
search_box = driver.find_element(By.ID,"home_submit")
search_box.send_keys(Keys.ENTER)
# wait for the IP address and links to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hostinfo")))
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/view/ip_addresses/')]")))

# extract the IP address
ip_address = driver.find_element(By.CLASS_NAME, "hostinfo").text

# extract the href links into a list
links = driver.find_elements(By.XPATH, "//a[contains(@href,'/view/ip_addresses/')]")

# extract the href links
hrefs = [link.get_attribute('href') for link in links]

# write the IP address and href links to a CSV file
with open('ip_addresses2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['IP Address', ip_address])
    writer.writerow(['Href Links'])
    for href in hrefs:
        writer.writerow([href])

# function to scan the IP address and return the port, service, and version
def scan_ip(ip_address):
    scanner = nmap.PortScanner()
    scanner.scan(ip_address, arguments='-sV')
    for host in scanner.all_hosts():
        for port in scanner[host]['tcp']:
            port_info = scanner[host]['tcp'][port]
            return port, port_info['name'], port_info['version']

# read the IP address from the CSV file
with open('ip_addresses2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader) # read the header row
    try:
        ip_address = next(reader)[1]
    except IndexError:
        ip_address = ''

# scan the IP address and get the port, service, and version
if ip_address:
    port, service, version = scan_ip(ip_address)
else:
    port, service, version = '', '', ''

# update the CSV file with the port, service, and version
with open('ip_addresses2.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([port, service, version])

# read the updated CSV file and print the contents
with open('ip_addresses2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)


time.sleep(100)
driver.quit()

