import requests
import json
import os

class SocialPanel:
  
  BASE_URL = "https://api.famosos.me/api"

  def __init__(self) -> None:
    self.s = requests.Session()
    self.token = None
    self.s.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    if self.verifyAuth() == False:
      self.login()

  def login(self):
    payload = {
      "email": "admin@admin.com",
      "password": "admin",
      "rememberDevice": True
    }
    r = self.s.post(f'{self.BASE_URL}/login', data=json.dumps(payload))

    if r.status_code == 200:
      print("Logged in successfully")
      data = r.json()
      token = data["token"]
      self.token = f"Bearer {token}"
      open(f"{os.getcwd()}/token.txt", "w").write(token)

  def verifyAuth(self):
    token = open(f"{os.getcwd()}/token.txt", "r").read()
    r = self.s.get(f'{self.BASE_URL}/auth/verify', headers={"Authorization": token})
    if r.status_code == 200:
      self.token = token
      return True
    else:
      return False
    
  def getFacebooksAccounts(self):
    r = self.s.get('/dashboard/social-networks/facebook', headers={"Authorization": self.token})
    return r.json()
  
  def getInstagramAccounts(self):
    r = self.s.get('/dashboard/social-networks/instagram', headers={"Authorization": self.token})
    return r.json()
  
  def getLinkedinAccounts(self):
    r = self.s.get('/dashboard/social-networks/linkedin', headers={"Authorization": self.token})
    return r.json()
  
  def getTikTokAccounts(self):
    r = self.s.get('/dashboard/social-networks/tiktok', headers={"Authorization": self.token})
    return r.json()

