from .diziroll import DiziRoll as dr

class Questions:
    go_back = "⬅  Geri Git"
    def get_show_name_question():
        return [
            {
                'type': 'input',
                'name': 'show_name',
                'message': 'İndirilecek dizinin adını yazınız: ',
                'validate': lambda val: len(dr.get_suggested_shows(val)) > 1 or "Dizi bulunamadı"
        }]
    
    def get_select_show_question(choices: list):
        return [
            {
            'type': 'list',
            'name': 'selected_show',
            'message': 'Hangi diziyi indirmek istiyorsunuz?',
            'choices': choices
            }
        ]
    def get_select_season_question(choices: list):
        return [
        {
        'type': 'list',
        'name': 'selected_season',
        'message': 'Hangi sezonu indirmek istiyorsunuz?',
        'choices': choices
        }
    ]
        
    def get_select_episodes_question(episodes: list):
        return [
            {
                'type': 'checkbox',

                'name': 'selected_episodes',
                'message': 'Hangi bölümleri indirmek istiyorsunuz?',
                'choices': [{"name": '{0}. Bölüm - {1}'.format(str(idx+1), i["title"])} for idx, i in enumerate(episodes)],
                'validate': lambda answer: 'En az bir tane bölüm seçmek zorundasınız.' \
                    if len(answer) == 0 else True
            }
        ]