""" from tweety import Twitter


def main():
    tw = Twitter('bth')
    uinfo = tw.get_user_info('elonmusk')
    print(uinfo.profile_image_url_https)

if __name__ == "__main__":
    main() """

import requests
import base64
from urllib.request import urlopen

r = requests.get('https://www.instagram.com/api/v1/users/web_profile_info/?username=creacionesmarfeluis.oficial', headers={
        "X-Ig-App-Id": "936619743392459",
        "cookie": 'datr=V5NRZSbOam8-Xirtaa1z8d70;ig_nrcb=1;ds_user_id=635313269;ig_did=3D073320-75ED-4F7A-A586-F327D63898E3;mid=ZVGTWAALAAF_pqsbxCesHe5C8PRn;sessionid=635313269%3AOxBYa3x4agCJbh%3A11%3AAYfNnGZzzfEDTQuO3AAUC3O1n7WJQYZIFal1zUk6tw;fbm_124024574287414=base_domain=.instagram.com;fbsr_124024574287414=wskWLEFjKd1ZszTa8q0WVH4qErx1mh-dIo0yJxhuG8Q.eyJ1c2VyX2lkIjoiMTQ5NzM0NTg5MCIsImNvZGUiOiJBUUFSa1FINDBaVUVRU1BuQ3hVZVJwOGVPSHl0MEFlYnBxaVZqM1J5cGwxY2M5Y01KaDcxMFB4UGZJMHFRNGpnODZKaDdjbGxIWWk5cFZNX2tNOGlGUmpmTWRwenliZE9IR3I2ZDhxOEs1OEo3QW1nSkd0eVRNcVVCUkhsd2c5aFk1VmlfSVdFb1NFMUk2UjJ2ZGFJWGloN3hQOVFWY1JMYzlhd0hoVGFmVm0yVmFYZnF4MGNfSzdKX01GZzF0eVNVa3QtVGFVWGNGeHRCZTl1b05ydXg0VWVlN3BLZDdOeDhXbWJMMS1PYmk3T3dVU3lVMGRUQVYwTlh3TE4zMzlldzJVd1ItTzR5MjB6Y2xLZktBUXg1dmhDaVA4QnZ1d1Y5bGpXamRndVRIZmg3NWdPR1V2R2VxNm16dUlRdFNmWks0USIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQk8zUVVpalN2Q3pPSlRaQmliVFVaQ1BDY1RhR3A3UlpDbDk0MUF6WkEwMHZ0MDU2OWh4ZjRXZXVQU3hLSG9sbUNzS0Jzb0ZSdHRJNlRLbnQwcXBtMHNhbzFmeDBVQ0IxMkdRZzlTTWFvSG9XU1FaQ1RKWkEwV3NFV3lpQlhyTEZka3cyRHZaQ0FwWkJkOUpzaFJnMkpweVpCMWtsWTdpZzJSVjB0V2h4MkhwSTBhYkhxWkExeEdmbU5FTCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzAwMjc1NTk3fQ;fbsr_124024574287414=wskWLEFjKd1ZszTa8q0WVH4qErx1mh-dIo0yJxhuG8Q.eyJ1c2VyX2lkIjoiMTQ5NzM0NTg5MCIsImNvZGUiOiJBUUFSa1FINDBaVUVRU1BuQ3hVZVJwOGVPSHl0MEFlYnBxaVZqM1J5cGwxY2M5Y01KaDcxMFB4UGZJMHFRNGpnODZKaDdjbGxIWWk5cFZNX2tNOGlGUmpmTWRwenliZE9IR3I2ZDhxOEs1OEo3QW1nSkd0eVRNcVVCUkhsd2c5aFk1VmlfSVdFb1NFMUk2UjJ2ZGFJWGloN3hQOVFWY1JMYzlhd0hoVGFmVm0yVmFYZnF4MGNfSzdKX01GZzF0eVNVa3QtVGFVWGNGeHRCZTl1b05ydXg0VWVlN3BLZDdOeDhXbWJMMS1PYmk3T3dVU3lVMGRUQVYwTlh3TE4zMzlldzJVd1ItTzR5MjB6Y2xLZktBUXg1dmhDaVA4QnZ1d1Y5bGpXamRndVRIZmg3NWdPR1V2R2VxNm16dUlRdFNmWks0USIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQk8zUVVpalN2Q3pPSlRaQmliVFVaQ1BDY1RhR3A3UlpDbDk0MUF6WkEwMHZ0MDU2OWh4ZjRXZXVQU3hLSG9sbUNzS0Jzb0ZSdHRJNlRLbnQwcXBtMHNhbzFmeDBVQ0IxMkdRZzlTTWFvSG9XU1FaQ1RKWkEwV3NFV3lpQlhyTEZka3cyRHZaQ0FwWkJkOUpzaFJnMkpweVpCMWtsWTdpZzJSVjB0V2h4MkhwSTBhYkhxWkExeEdmbU5FTCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzAwMjc1NTk3fQ;'
    })

data = r.json()

posts = []

edges = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

for post in edges:
    imageuri = base64.b64encode(urlopen(post['node']['thumbnail_src']).read()).decode('utf-8')
    posts.append({
        "url_encode": imageuri,
        "url_post": f"https://www.instagram.com/p/{post['shortcode']}"
    })