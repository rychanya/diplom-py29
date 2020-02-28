from api import VKAPI
import json

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


class User:
    def __init__(self, name_or_id):
        self.vk = VKAPI(TOKEN)
        self.user_id = self.vk.get_id_from_name_or_id(name_or_id)
        if self.user_id:
            print(f'User id {self.user_id}')
        else:
            print('User not found. Continue with current user.')

    def get_groups(self):
        print('Try get users groups')
        self.groups = vk.groups_get(self.user_id)
        if self.groups:
            print(f'Find {len(self.groups)} groups.')
        else:
            print('User don`t have any groups.')

    def get_friends(self):
        print('Try get friends.')
        self.friends = self.vk.friends_get(self.user_id)
        if self.friends:
            print(f'Find {len(self.friends)} friends.')
        else:
            print('User don`t have any friends.')

if __name__ == '__main__':
    vk = VKAPI(TOKEN)
    name_or_id = 'rychanya'
    user = User(name_or_id)
    user.get_groups()
    user.get_friends()
    for friend in user.friends:
        friend_groups = vk.groups_get(friend)
        user_groups = user_groups - friend_groups
    if user_groups:
        json_data = vk.groups_getById(', '.join(map(str, user_groups)))
        if json_data:
            with open('groups.json', mode='w', encoding='utf8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
                
