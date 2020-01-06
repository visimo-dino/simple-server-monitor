from time import sleep
from datetime import datetime as dt
import yagmail
from requests import get
from requests.auth import HTTPBasicAuth


SITES = {
    'clima-pm-performance-dash': {
        'url': 'http://climatech.visimo.co',
        'username': 'clima_user',
        'password': 'Cl1m@tech!2019',
        'status': 'up',
        'last_down_at': None
    },
}

RECIPIENTS = [
    'dino@visimoconsulting.com',
    'james@visimoconsulting.com',
]

yag = yagmail.SMTP('noreply@visimoconsulting.com')


def check_site(site_dict):
    res = get(
        site_dict['url'],
        auth=HTTPBasicAuth(site_dict['username'], site_dict['password']),
    )
    status_code = res.status_code
    return status_code

def send_email(sites):
    subject = '************** SITE(S) DOWN **************'
    body = 'The following sites are currently down:\n\n'
    for site in sites:
        body += f"{site['url']}\n"
    yag.send(
        to=RECIPIENTS,
        subject=subject,
        contents=body,
    )    

    
while True:

    # List containing sites that require notification.
    sites_to_alert = []
    
    # Loop through all sites and check their status.
    for site_name, site_dict in SITES.items():
        
        # Do the following if the site's status has just changed from 'up' to
        # down'.
        if site_dict['status'] == 'up' and check_site(site_dict) != 200:

            # Add the site to sites_to_alert.
            sites_to_alert.append(SITES[site_name])
            
            # Set the site's status to 'down' in the dictionary.
            SITES[site_name]['status'] = 'down'
        
        # Do the following if the site is up.
        else:
            
            # Set the site's status as 'up.'
            SITES[site_name]['status'] = 'up'
    
    # Email us any sites that require notification, if any exist.
    if len(sites_to_alert) > 0:
        send_email(sites_to_alert)
    
    # Wait for 30 seconds.
    sleep(60)

