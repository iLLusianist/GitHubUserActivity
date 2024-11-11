import requests
import json

class Model:
    def __init__(self):
        self.status_codes = {
            301: 0,
            304: 0,
            403: 0,
            404: 0
            }

    def get_events(self, username):
        url = f'https://api.github.com/users/{username}/events'
        response = requests.get(url)
        if self.check_response_status(response.status_code) == 1:
            content = response.text
            return json.loads(content)
        else: raise ValueError(f'Произошла ошибка. Код статуса: {response.status_code}')

    def check_response_status(self, status_code):
        return self.status_codes[status_code]

    def make_events_list(self, username = 'iLLusianist'):
        events = self.get_events(username)
        merged_events_list = []
        for event in events:
            merged_events_list.append(f'{event['type']}&{event['repo']['name']}')
        return merged_events_list
        
    def count_events(self, events_list):
        counted_events = []
        for event in sorted(set(events_list)):
            event_count = events_list.count(event)
            event_text = event.split('&')
            counted_events.append([event_text[0], event_text[1], event_count])
        return counted_events

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

    def __str__(self):
        return('---GitHub User Activity---')

    def get_user_input(self, prompt: str):
        return input(prompt)

    def show_events(self, events):
        for event in events:
            event_type_description = ''
            event_type, event_repo, event_count = event[0], event[1], event[2]
            if str(event_type) in self.event_type_description:
                event_type_description = self.event_type_description[str(event_type)]
            else: event_type_description = 'Неизвестный тип события'
            print_events = f'{event_type_description} {event_repo} {event_count} раз(а)'
            self.show_message(print_events)

    def show_message(self, message):
        print(message)
        
class Controller:
    def __init__(self, model, view):
        self.view: View = view
        self.model: Model = model
    
    def run(self):
        print(View())
        while True:
            user_input = self.view.get_user_input('\nВведите ник пользователя GitHub > ')
            try:
                events = self.model.make_events_list(user_input)
                if events == []:
                    self.view.show_message(f'Пользователь с ником {user_input} не имеет активности за последние 90 дней')
                counted_events = self.model.count_events(events)
                if counted_events:
                    self.view.show_events(counted_events)
            except Exception as ex: 
                print(ex)

if __name__=='__main__':
    view = View()
    model = Model()
    controller = Controller(model, view)
    controller.run()