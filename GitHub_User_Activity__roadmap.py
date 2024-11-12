import requests
import json
from collections import Counter


class API:
    @staticmethod
    def get_events(username):
        url = f'https://api.github.com/users/{username}/events'
        response = requests.get(url)
        if response.ok:
            return json.loads(response.text)
        else:
            raise ValueError(f'Произошла ошибка. Код статуса: {response.status_code}')

    @staticmethod
    def check_user_exists(username):
        url = f'https://api.github.com/users/{username}'
        response = requests.get(url)
        return response.status_code == 200


class Model:
    def __init__(self, api):
        self.api: API = api

    def make_events_list(self, username):
        events = self.api.get_events(username)
        if not events:
            return []
        return [f'{event['type']}&{event['repo']['name']}' for event in events]

    @staticmethod
    def count_events(events_list):
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
            'IssuesEvent': 'Открыл, закрыл или изменил статус issue',
            'MemberEvent': 'Изменил настройки участников',
            'PublicEvent': 'Сделал репозиторий публичным',
            'PullRequestEvent': 'Pull request',
            'PushEvent': 'Отправил изменения в репозиторий',
            'ReleaseEvent': 'Выпустил новую версии проекта',
            'SponsorshipEvent': 'Спонсировал разработчика или проект',
            'WatchEvent': 'Начал следить за репозиторием',
        }
        self.username = 'iLLusianist'

    @staticmethod
    def show_title():
        print('---GitHub User Activity---')

    def get_user_input(self):
        self.username = input('\nВведите ник пользователя GitHub > ')
        return self.username

    @staticmethod
    def show_message(message):
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
            username = self.view.get_user_input()
            try:
                if not self.model.api.check_user_exists(username):
                    raise ValueError(f'Пользователь {username} не найден')

                events = self.model.make_events_list(username)
                if not events:
                    self.view.show_error()
                    continue
                counted_events = self.model.count_events(events)
                self.view.show_events(counted_events)

            except ValueError as e:
                self.view.show_message(e)
            except Exception as e:
                self.view.show_message(f'Произошла непредвиденная ошибка: {e}')


if __name__ == '__main__':
    api_client = API()
    view = View()
    model = Model(api_client)
    controller = Controller(model, view)
    controller.run()
