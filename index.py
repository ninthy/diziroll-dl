from .lib.diziroll import DiziRoll as dr
from PyInquirer import prompt, print_json
from .lib.questions import Questions as q
from os import path
import os
from colorama import init, Fore, Back

VERSION = 1.0

init()
clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

if __name__ == "__main__":
    clear()
    print(Fore.RED +  
    f"""
 ____  _     _ ____       _ _   ____  _     
|  _ \(_)___(_)  _ \ ___ | | | |  _ \| |    
| | | | |_  / | |_) / _ \| | | | | | | |    
| |_| | |/ /| |  _ < (_) | | | | |_| | |___ 
|____/|_/___|_|_| \_\___/|_|_| |____/|_____| 
                                             by {Fore.YELLOW + '@ninthy' + Fore.RED} 
                                                 {Fore.GREEN + 'v' + str(VERSION) + Fore.RED}
    """
    + Fore.RESET)
    
    suggested_show = prompt(q.get_show_name_question())['show_name']
    shows = dr.get_suggested_shows(suggested_show)
    if not shows:
        print("! Diziroll'a bağlanılamadı.")
        exit()
    
    while 1:
        
        
        selected_show_answer = prompt(q.get_select_show_question([i["name"] for i in shows]))["selected_show"]
        selected_show = list(filter(lambda x: x["name"] == selected_show_answer, shows))[0]
        show = dr.get_show(selected_show["url"][1::])
        if not show:
            print("! Diziroll'a bağlanılamadı.")
            break
        folder_name = show['slug']
        if not path.isdir(folder_name):
            os.mkdir(folder_name)
        
        while 1:
            titles = [i["title"] for i in show["seasons"]]
            titles.append(q.go_back)
            
            selected_season_answer = prompt(q.get_select_season_question(titles))["selected_season"]
            print(selected_season_answer)
            if selected_season_answer == q.go_back:
                break

            selected_season = [i for i in show["seasons"] if i["title"] == selected_season_answer][0]
            
            selected_episode_answers = prompt(q.get_select_episodes_question(selected_season["episodes"]))["selected_episodes"]
            print(len(selected_episode_answers))
            total_episodes = selected_season["episodes"][:len(selected_episode_answers)]
            
            for idx, i in enumerate(total_episodes):
                episode = dr.get_episode(i["id"])
                if not episode:
                    print("! Bir hata oluştu")
                    continue
                
                episode_title = '{0}. Bölüm - {1}'.format(str(idx+1), i["title"])
                sources = episode["sources"]
                subtitles = episode["subtitles"]
                subtitle_src = [i["src"] for i in subtitles if i["srclang"] == "tr"][0]
                hd_source = [i for i in sources if i["res"] == "480"][0]

                source_path = path.join(os.getcwd(), folder_name, episode_title)
                dr.download_subtitle(subtitle_src, path=source_path)
                dr.download_video(url=hd_source["src"], path=source_path)
                print("! ", episode_title, "videosu indirildi.")
                # open("test.json", "w", encoding="utf-8").write(json.dumps(episode))
            
            break
        break

"""
todo -
    subtitles
    error handling
    
"""