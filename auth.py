import json
from xmlrpc.client import ProtocolError
import requests
from twisted.python import failure
from twisted.internet import reactor
from quarry.types.uuid import UUID
from quarry.net.client import ClientFactory, SpawningClientProtocol
from quarry.net import auth, crypto
from twisted.internet import reactor

def make_profile(accessToken):
    """
    Support online mode
    """
    url = "https://api.minecraftservices.com/minecraft/profile"
    headers = {'Authorization': 'Bearer ' + accessToken}
    response = requests.request("GET", url, headers=headers)
    result = response.json()
    myUuid = UUID.from_hex(result['id'])
    myUsername = result['name']
    return auth.Profile('(skip)', accessToken, myUsername, myUuid)
