# Help to fix onedrive is full
At time of writing, onedrive really sucks saying it is full, and provide no way to identify where your folder grows.

This python script permits to identify problems in your onedrive folder when it says it is full (but apparently not)

This script will list your onedrive folder content and computes size of each file, including size of versioned files 
Once you identified the biggest files in your onedrive folder (including their revisions taking disk size), you will be able to 
remove some versions of these files. 

I quickly made this script from scratch, to identify problems in my onedrive.Then, any improvements are welcomed :-) 

# example result

        [evaluation]Name: detection_coco_evaluator.py, Size: 30652 Type: File
                  Version ID: 1.0 Size : 30652
        [evaluation]Name: evaluator.py, Size: 8448 Type: File
                Version ID: 1.0 Size : 8448
        [evaluation]Name: instance_evaluation.py, Size: 4938 Type: File
                Version ID: 1.0 Size : 4938
        [custom_oneformer]Name: modeling, Size: 214918 Type: Folder
        [modeling]Name: backbone, Size: 38656 Type: Folder
        [backbone]Name: __init__.py, Size: 51 Type: File
                Version ID: 1.0 Size : 51
        [backbone]Name: dinat.py, Size: 11101 Type: File

# setup
pip install -r requirements.txt


# Allowing the script to access your onedrive folder 
To use this script, it will need to login to your onedrive account. That's a bit tricky...
The login process uses interactivebrowser credential with help of your browser  . refs https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.interactivebrowsercredential?view=azure-python0


To achieve it , you will need to create an app in azure portal (now microsoft entra) to allow to login with your microsoft account 
to access your onedrive 

Define the auth reply   as http://localhost:8400 when creating the application

When your app is created , you MUST fill in these variables in the script:
* tenant_id : tenant id of your business id
* client_id : (app id) in the script 

You will need to allow these authorizations to the application:
"User.Read","Files.Read","Files.Read.All"
