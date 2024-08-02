
import asyncio
import json
from urllib.parse import urljoin
from azure.identity import InteractiveBrowserCredential
from msgraph import GraphServiceClient
import sys
import os
import requests
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

tenant_id = "yyyyyyyyyy" # your company tenant_id 


""" https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Overview
"""

"""
You need to create an application in azure portal   (with an auth login redirected to http://localhost:8400 )
and to set client_id here :
"""
client_id ="xxxxxxx" # app id (client)  https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade


credential = InteractiveBrowserCredential(
    client_id=client_id,
    tenant_id=tenant_id,
)
scopes = ["User.Read","Files.Read","Files.Read.All"]
client = GraphServiceClient(credentials=credential, scopes=scopes)


# Function to get the access token
async def get_access_token():
    token =  credential.get_token(*scopes)
    #print(f"Access Token: {token.token}")
    return token
# Run the function to get the access token
access_token = asyncio.run(get_access_token())

dic = {}
used_quota = 0

def get_versions_and_size(item_id,drive_id,headers):
        """
        GET /drives/{drive-id}/items/{item-id}/versions
        """
        global used_quota
        versions_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/versions"
        while True:
            response = requests.get(versions_url, headers=headers)
            if response.status_code != 200:
                print(f"Error fetching versions: {response.text}")
                return

            data = json.loads(response.text)
            size = 0 
            d = dic[drive_id+'_'+item_id]
            for version in data["value"]:
                print(f"\tVersion ID: {version['id']} ",end="")
                print(f"Size : {version.get('size', 'N/A')}")
                if version.get('size', 'N/A') !=  'N/A':
                    size += float(version.get('size'))
            if size != 0:
                d['size'] = size
                dic[drive_id+'_'+item_id] = d # summed size with versions size
            used_quota += size
            # Handle pagination if necessary
            if "@odata.nextLink" in data:
                versions_url = data["@odata.nextLink"]
            else:
                break



def list_onedrive_content(drive_url, access_token,parent_name=None,item_id=None,drive_id=None):
    headers = {
        "Authorization": f"Bearer {access_token.token}"
    }

    if item_id:
        url = f"{GRAPH_API_ENDPOINT}/drives/{drive_id}/items/{item_id}/children"
    else:
        url = f"{GRAPH_API_ENDPOINT}/me/drive/root/children"
    # response = requests.get( GRAPH_API_ENDPOINT + drive_url, headers=headers)
    # response.raise_for_status()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        for item in data["value"]:
            # if parent_name:
            #     print("[%s]" % parent_name,end="")
            print(f"Name: {item['name']}, Size: {item.get('size', 'N/A') } ",end="")
            try:
                if item['folder']:
                    print(f"Type: Folder")
                    list_onedrive_content(drive_url, access_token,item['name'],item['id'],item["parentReference"]["driveId"])
   
            except:
                print(f"Type: File")
                size = 0
                if item.get('size','N/A') != 'N/A':
                    size += float(item.get('size'))
                dic[item["parentReference"]["driveId"]+'_'+item['id']] = { 'name' : item['name'] , 'size':size}
                if item["parentReference"]["driveId"]:                    
                    get_versions_and_size(item['id'],item["parentReference"]["driveId"],headers)
    else:
        print("Error fetching data.")
     

list_onedrive_content("/me/drive/root/children",access_token)

print(dic)
dic.sort(key=lambda x: x['size'])

print(dic)
print("Disk quota size used : ",used_quota," Bytes")
