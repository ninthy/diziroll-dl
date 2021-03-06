from json import dump
from .questions import Questions as q
import requests
import subprocess
from fake_useragent import UserAgent

from rich import print as rprint

from youtube_dl import YoutubeDL

from rich.progress import Progress, BarColumn, SpinnerColumn, ProgressColumn, TimeRemainingColumn, DownloadColumn

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
    def __init__(self):
        pass
    
    def get_episode(self, id: int):
        response = requests.get(endpoints["episode"].format(str(id)), headers=headers)
        try:
            data = response.json()
            if not data["status"]:
                return None
            return data["data"]
        except Exception as e:
            print(e)
            return None

    def get_show(self, slug: str):
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
    def download_subtitle(url: str, path: str):
        query = f'youtube-dl "{url}" -o "{path}.vtt" --quiet'
        print(query)
        process = subprocess.Popen(query, shell=True, stdout=None )#, stdout=subprocess.PIPE)
        process.wait()
        
    @staticmethod
    def download_video(url: str, path: str):
        query = f'youtube-dl "{url}" -o "{path}.mp4" --quiet'
        process = subprocess.Popen(query, shell=True, stdout=None)#, stdout=subprocess.PIPE)
        process.wait()

    def get_suggested_shows(self, name: str):
        response = requests.post(endpoints["search"], data={"term": name}, headers=headers)
        try:
            data = response.json()
            if not data["status"]:
                return None
            series = data["data"]["series"]
            return series
        except Exception as e:
            print(e)
            return None
   
    
    def get_episodes_from_season(self, total_episodes: list, selected_res_answer: str, season: str):
        episodes = []
        with Progress(SpinnerColumn(), "[progress.description]{task.description}", BarColumn(complete_style="green", style="yellow", finished_style="red"), "[progress.percentage]{task.percentage:>3.0f}%", TimeRemainingColumn()) as progress:
            task = progress.add_task("[yellow]?[/yellow] B??l??mler ??ekiliyor..", total=len(total_episodes))
            for idx, i in enumerate(total_episodes):
                episode = self.get_episode(i["id"])
                if not episode:
                    rprint("[red]![/red] Bir hata olu??tu.")
                    continue
                episode_title = '{season} {idx}. B??l??m - {title}'.format(season=season["title"], idx=i["sequence"], title=i["title"])
                sources = episode["sources"]
                subtitles = episode["subtitles"]
                subtitle_src = [i["src"] for i in subtitles if i["srclang"] == "tr"][0]
                global source
                for i in sources:
                    if i["label"] == selected_res_answer:
                        source = i
                        break
                    elif selected_res_answer == q.highest_res:
                        highest_res = str(max([int(i["res"]) for i in sources]))
                        if i["res"] == highest_res:
                            source = i
                            break
                    elif selected_res_answer == q.lowest_res:
                        lowest_res = str(min([int(i["res"]) for i in sources]))
                        
                        if i["res"] == lowest_res:
                            source = i
                            break                 
                progress.update(task, description=f"[yellow]{episode_title}[/yellow] ??ekildi.", advance=1)
                
                episodes.append((source["src"], subtitle_src, episode_title, season))
        return episodes