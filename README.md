# one_drive_full
This python script permits to identify problems in your onedrive folder when it says it is full (but apparently not)

At time of writing, onedrive really sucks saying it is full, and provide no way to identify where your folder grows.

This script will list your onedrive folder content and computes size of each file, including size of versioned files 

# setup
pip install -r requirements.txt


# Allowing the script to access your onedrive folder 
To use this script, you will need to create an app in azure portal (now microsoft entra) to allow to login with your microsoft account 
to access your onedrive 

When your app is created , you MUST fill in these variables in the script:
* tenant_id : tenant id of your business id
* client_id : (app id) in the script 
