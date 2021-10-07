import requests
import subprocess
from fake_useragent import UserAgent



ua = UserAgent()
endpoints = {
    "search": "https://api.diziroll.com/v1/search/suggest",
    "episode": "https://api.diziroll.com/v1/episode/source?episode_id={0}&debug=1",
    "main": "https://api.diziroll.com/v1/series?slug={0}&fields%5B%5D=series.seasons&fields%5B%5D=series.seasons.episodes"
}

headers = {
    "Referer": "https://www.diziroll.com/",
    "sec-ch-ua": '" Not;A Brand";v="99", "Opera GX";v="79", "Chromium";v="93"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "User-Agent": ua.random
}  


class DiziRoll:  
    
    @staticmethod
    def get_episode(id: int):
        response = requests.get(endpoints["episode"].format(str(id)), headers=headers)
        try:
            data = response.json()
            if not data["status"]:
                return None
            return data["data"]
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_show(slug: str):
        response = requests.get(endpoints["main"].format(slug), headers=headers)
        try:
            data = response.json()
            
            if not data["status"]:
                return None
            return data["data"]
        except Exception as e:
            print(e)
            return None
    
    
    @staticmethod
    def download_video(url: str, path: str):
        query = f'youtube-dl "{url}" -o "{path}.mp4"'
        process = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE)
        process.wait()
        
    @staticmethod
    def download_subtitle(url: str, path: str):
        query = f'youtube-dl "{url}" -o "{path}.vtt"'
        process = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE)
        process.wait()
        
    @staticmethod
    def get_suggested_shows(name: str):
        response = requests.post(endpoints["search"], data={"term": name}, headers=headers)
        try:
            data = response.json()
            if not data["status"]:
                return None
            return data["data"]["series"]
        except Exception as e:
            print(e)
            return None
            