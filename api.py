import requests
from time import time, sleep

import vkexception

class VKAPI:

    def __init__(self, token, method_time_out=.4):
        self.token = token
        self.last_call_api = time()
        self.method_time_out = method_time_out

    def _vk_method(self, method, **kwargs):
        URL = f'https://api.vk.com/method/{method}'
        kwargs.update(
            {
                'v': '5.52',
                'access_token': self.token,
            }
        )
        if (time() - self.last_call_api) < self.method_time_out:
            sleep(self.method_time_out)
        self.last_call_api = time()
        response = requests.get(URL, kwargs, timeout=10)
        response.raise_for_status()
        json = response.json()
        return json


    def _raise(self, data):
        if 'error' in data:
            error_code = data['error'].get('error_code')
            error_msg = data['error'].get('error_msg')
            raise vkexception.VKBaseException(error_code, error_msg)
        elif 'response' in data:
            return
        else:
            raise vkexception.VKOtherException(data)

    def resolve_screen_name(self, screen_name: str):
        json = self._vk_method('resolveScreenName', screen_name=screen_name)
        self._raise(json)
        try:
            if json['response'] and json['response']['type'] == 'user':
                return json['response']['object_id']
        except KeyError:
            pass

    
    def get_id_from_name_or_id(self, user_name_or_id):
        try:
            return int(user_name_or_id)
        except ValueError:
            return self.resolve_screen_name(user_name_or_id)


    def groups_get(self, user_id):
        # 30 260
        json = self._vk_method('groups.get', user_id=user_id)
        self._raise(json)
        try:
            return set(json['response']['items'])
        except KeyError:
            pass
        return set()

    def friends_get(self, user_id):
        # 30
        json = self._vk_method('friends.get', user_id=user_id)
        self._raise(json)
        try:
            return json['response']['items']
        except KeyError:
            pass
        return []

    def groups_getById(self, groups_id):
        params = {
            'group_ids': groups_id,
            'fields': ['name', 'id', 'members_count']
        }
        json = self._vk_method('groups.getById', **params)
        self._raise(json)
        try:
            return [self.parse_group(group) for group in json['response']]
        except KeyError:
            pass
        return []


    @staticmethod
    def parse_group(json_group):
        return {
            'name': json_group['name'],
            'gid': json_group['id'],
            'members_count': json_group['members_count']
            }

    def execute(self):
        # 12 13
        pass