
class Questions:
    go_back = "⬅  Geri Git"
    highest_res = "En yüksek"
    lowest_res = "En düşük"
    to_be_downloaded = "İndirmek"
    to_be_watched = "İzlemek"
    @staticmethod
    def get_show_name_question(dr):
        return [
            {
                'type': 'input',
                'name': 'show_name',
                'message': 'Bir dizi giriniz: ',
                'validate': lambda val: len(dr.get_suggested_shows(val)) >= 1 or "Dizi bulunamadı"
        }]
    @staticmethod
    def get_select_type():
        return [
            {
            'type': 'list',
            'name': 'selected_type',
            'message': 'İndirmek mi istiyorsunuz yoksa izlemek mi?',
            'choices': [Questions.to_be_downloaded, Questions.to_be_watched]
            }
        ]
    @staticmethod
    def get_select_res_question():
        return [
            {
            'type': 'list',
            'name': 'selected_res',
            'message': 'Hangi çözünürlüğü istiyorsunuz?',
            'choices': [Questions.highest_res, "1080p", "720p", "480p", Questions.lowest_res]
            }
        ]
    @staticmethod
    def get_select_show_question(choices: list):
        return [
            {
            'type': 'list',
            'name': 'selected_show',
            'message': 'Seçtiğiniz dizi hangisi?',
            'choices': choices
            }
        ]
    @staticmethod
    def get_select_season_question(choices: list):
        return [
        {
        'type': 'list',
        'name': 'selected_season',
        'message': 'Hangi sezondan istiyorsunuz?',
        'choices': choices
        }
    ]
        
    @staticmethod
    def get_select_episodes_question(episodes: list):
        return [
            {
                'type': 'checkbox',

                'name': 'selected_episodes',
                'message': 'Hangi bölümleri istiyorsunuz?',
                'choices': [{"name": '{0}. Bölüm - {1}'.format(str(idx+1), i["title"])} for idx, i in enumerate(episodes)],
                'validate': lambda answer: answer >= 1 or 'En az bir tane bölüm seçmek zorundasınız.'  
            }
        ]