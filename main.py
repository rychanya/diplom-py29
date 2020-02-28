import requests
from time import time, sleep
import vkexception
import json


TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


class VKAPI:

    def __init__(self, token):
        self.token = token
        self.last_call_api = time()

    def _vk_method(self, method, **kwargs):
        URL = f'https://api.vk.com/method/{method}'
        kwargs.update(
            {
                'v': '5.52',
                'access_token': self.token,
            }
        )
        try:
            delta = time() - self.last_call_api
            if delta < .4:
                sleep(.4 - delta)
            response = requests.get(URL, kwargs, timeout=10)
            response.raise_for_status()
            self.last_call_api = time()
            json = response.json()
            self._raise(json)
            return json
        except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as error:
            print(error)
        except vkexception.VKTooManyRequests as error:
            sleep(.4)
            print(error)
            self._vk_method(method, **kwargs)
        except (vkexception.VKPermissionDenied, vkexception.VKUserWasDeletedOrBanned) as error:
            print(error)

    def _raise(self, data):
        if 'error' in data:
            error_code = data['error'].get('error_code')
            error_msg = data['error'].get('error_msg')
            if error_code == 7 or error_code == 15:
                raise vkexception.VKPermissionDenied(error_msg)
            elif error_code == 6:
                raise vkexception.VKTooManyRequests(error_msg)
            elif error_code == 18:
                raise vkexception.VKUserWasDeletedOrBanned(error_msg)
            else:
                print(data)
                raise vkexception.VKOtherException(error_msg)
        elif 'response' in data:
            return
        else:
            raise vkexception.VKOtherException(error_msg)

    def resolve_screen_name(self, screen_name: str):
        json = self._vk_method('resolveScreenName', screen_name=screen_name)
        if not json:
            return
        try:
            if json['response'] and json['response']['type'] == 'user':
                return json['response']['object_id']
        except KeyError:
            pass

    def groups_get(self, user_id):
        # 30 260
        json = self._vk_method('groups.get', user_id=user_id)
        if not json:
            return set()
        try:
            return set(json['response']['items'])
        except KeyError:
            return set()

    def friends_get(self, user_id):
        # 30
        json = self._vk_method('friends.get', user_id=user_id)
        if not json:
            return []
        try:
            return json['response']['items']
        except KeyError:
            return []

    def groups_getById(self, groups_id):
        params = {
            'group_ids': groups_id,
            'fields': ['name', 'id', 'members_count']
        }
        json = self._vk_method('groups.getById', **params)
        if not json:
            return

        def parse_group(json_group):
            return {
                'name': json_group['name'],
                'gid': json_group['id'],
                'members_count': json_group['members_count']
                }
        return [parse_group(group) for group in json['response']]

    def execute(self):
        # 12 13
        pass


vk = VKAPI(TOKEN)
user_id = vk.resolve_screen_name('rychanya')
user_groups = vk.groups_get(user_id)
for friend in vk.friends_get(user_id):
    friend_groups = vk.groups_get(friend)
    user_groups = user_groups - friend_groups
if user_groups:
    json_data = vk.groups_getById(', '.join(map(str, user_groups)))
    if json_data:
        with open('groups.json', mode='w', encoding='utf8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
