import requests
import json
from collections import Counter

class API:
    def get_events(self, username):
        url = f'https://api.github.com/users/{username}/events'
        response = requests.get(url)
        if response.ok:
            return json.loads(response.text)
        else: raise ValueError(f'Произошла ошибка. Код статуса: {response.status_code}')

class Model:
    def __init__(self, api_client):
        self.api_client: API = api_client

    def make_events_list(self, username):
        events = self.api_client.get_events(username)
        if not events:
            return []
        return [f'{event['type']}&{event['repo']['name']}' for event in events]
        
    def count_events(self, events_list):
        return [[key.split('&')[0], key.split('&')[1], value] for key, value in Counter(events_list).items()]

class View:
    def __init__(self):
        self.event_type_description = {
            'CommitCommentEvent': 'Добавил комментарий к коммиту',
            'CreateEvent': 'Создал ветку, тег или репозиторий',
            'DeleteEvent': 'Удалил ветку или тег',
            'ForkEvent': 'Создана вилка репозитория для других пользователей',
            'GollumEvent': 'Обновлена Wiki страницы',
            'IssueCommentEvent': 'Добавил комментарий к issue',
            'IssuesEvent': 'Открыл, закрыл или измененил статус issue',
            'MemberEvent': 'Измененил настройки участников',
            'PublicEvent': 'Сделал репозиторий публичным',
            'PullRequestEvent': 'Pull request',
            'PushEvent': 'Отправил изменения в репозиторий',
            'ReleaseEvent': 'Выпустил новую версии проекта',
            'SponsorshipEvent': 'Спонсированл разработчика или проект',
            'WatchEvent': 'Начал следить за репозиторием',
            }
        self.username = 'iLLusianist'

    def show_title(self):
        print('---GitHub User Activity---')

    def get_user_input(self):
        self.username = input('\nВведите ник пользователя GitHub > ')
        return self.username

    def show_message(self, message):
        print(message)

    def show_error(self):
        self.show_message(f'Пользователь с ником {self.username} не имеет активности за последние 90 дней')

    def show_events(self, events):
        self.show_message(f'\nДействия пользователя {self.username} за последние 90 дней:\n------')
        for event in events:
            event_type, event_repo, event_count = event
            event_type_description = self.event_type_description.get(event_type, 'Неизвестный тип события')
            print_events = f'{event_type_description} {event_repo} {event_count} раз(а)'
            self.show_message(print_events)
        self.show_message('------')
        
class Controller:
    def __init__(self, model, view):
        self.view: View = view
        self.model: Model = model
    
    def run(self):
        self.view.show_title()
        while True:
            user_input = self.view.get_user_input()
            try:
                events = self.model.make_events_list(user_input)
                if not events:
                    self.view.show_error()
                    continue
                counted_events = self.model.count_events(events)
                self.view.show_events(counted_events)
            except Exception as e: 
                print(str(e))

if __name__=='__main__':
    api_client = API()
    view = View()
    model = Model(api_client)
    controller = Controller(model, view)
    controller.run()