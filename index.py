from re import T
from src.questions import Questions as q
from src.diziroll import DiziRoll as dr
from PyInquirer import prompt
from os import path
import os
from rich import print as rprint
import subprocess
from rich.progress import Progress, BarColumn, SpinnerColumn, ProgressColumn, TimeRemainingColumn, DownloadColumn
from multiprocessing import Pool

VERSION = 2.6

clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
diziroll = dr()

if __name__ == "__main__":
    while 1:
        clear()
        rprint(f"""[red]
     ____  _     _ ____       _ _   ____  _     
    |  _ \(_)___(_)  _ \ ___ | | | |  _ \| |    
    | | | | |_  / | |_) / _ \| | | | | | | |    
    | |_| | |/ /| |  _ < (_) | | | | |_| | |___ 
    |____/|_/___|_|_| \_\___/|_|_| |____/|_____| 
                                                 [yellow]by github.com/ninthy[/yellow] 
                                                     [green]v{str(VERSION)}[/green][/red]
        """)
        suggested_show = prompt(q.get_show_name_question(diziroll))['show_name']
        shows = diziroll.get_suggested_shows(name=suggested_show)
        if not shows:
            rprint("[red]![/red] Diziroll'a bağlanılamadı.")
            exit()
        
        while 1:
            selected_show_answer = prompt(q.get_select_show_question([i["name"] for i in shows] + [q.go_back]))["selected_show"]
            if selected_show_answer == q.go_back:
                break
            selected_show = list(filter(lambda x: x["name"] == selected_show_answer, shows))[0]
            show = diziroll.get_show(selected_show["url"][1::])
            if not show:
                rprint("[red]![/red] Diziroll'a bağlanılamadı.")
                break
            folder_name = show['slug']
            selected_type = prompt(q.get_select_type())["selected_type"]
            is_downloadable = selected_type == q.to_be_downloaded
            while 1:
                titles = [i["title"] for i in show["seasons"]] + [q.go_back]


                selected_season_answer = prompt(q.get_select_season_question(titles))["selected_season"]
                if selected_season_answer == q.go_back:
                    break
                selected_season = [i for i in show["seasons"] if i["title"] == selected_season_answer][0]

                selected_episode_answers = prompt(q.get_select_episodes_question(selected_season["episodes"]))["selected_episodes"]
                if len(selected_episode_answers) == 0:
                    continue

                episodes = selected_season["episodes"]
                selected_res_answer = prompt(q.get_select_res_question())["selected_res"]
                total_episodes = []
                for episode in episodes:
                    for i in selected_episode_answers:
                        idx = int(i[0])
                        if int(episode["sequence"]) == idx:
                            total_episodes.append(episode)
                            break
                
                if len(total_episodes) == 0:
                    rprint("[red]![/red] Diziroll'a bağlanılamadı.")
                    exit(0)
                episodes = diziroll.get_episodes_from_season(total_episodes, selected_res_answer, selected_season)
                if not is_downloadable:
                    query = "mpv "+' '.join([('--{ "' +i[0]+'" --sub-files="' + i[1] + '" --force-media-title="' +i[2]+ '" --term-playing-msg="'+i[2] + '" --title="'+i[2] +'" --}') for i in episodes])
                    p = subprocess.Popen(query)
                    rprint("[yellow]? [cyan]mpv[/cyan] açıldı, bölümleri oynatma listesinden seçebilir veya geçebilirsiniz.[/yellow]")
                    print(query)
                    input()
                    exit()
                if not path.isdir(folder_name):
                    os.mkdir(folder_name)
                with Progress(SpinnerColumn(), "[progress.description]{task.description}", BarColumn(style="yellow", complete_style="green", finished_style="red"), "[progress.percentage]{task.percentage:>3.0f}%", TimeRemainingColumn()) as progress:
                    task = progress.add_task("[yellow]?[/yellow] Bölümler indiriliyor..", total=len(episodes))
                    for episode in episodes:                    
                        src, subtitle_src, episode_title, season = episode
                        print(src, subtitle_src)
                        season_path = path.join(os.getcwd(), folder_name, season["slug"])
                        if not path.isdir(season_path):
                            os.mkdir(season_path)
                        
                        source_path = path.join(season_path,  episode_title)
                        
                        progress.update(task, description=f"{episode_title} altyazı indiriliyor.")
                        dr.download_subtitle(url=subtitle_src, path=source_path)
                        progress.update(task, description=f"{episode_title} altyazı indirildi.")
                        progress.update(task, description=f"{episode_title} video indiriliyor.")
                        dr.download_video(url=src, path=source_path)
                        progress.update(task, description=f"{episode_title} video indirildi.", advance=1)
                    progress.update(task, description="İndirme işlemi bitti: [yellow]%s" % source_path.split('\\')[:-1], completed=True)
                # open("test.json", "w", encoding="utf-8").write(json.dumps(episode))

                break
            break
"""
todo -
    progress bar for downloading
    mpv playlist media name
"""
