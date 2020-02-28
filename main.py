from api import VKAPI
import json

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


if __name__ == '__main__':
    vk = VKAPI(TOKEN)
    user_id = vk.get_id_from_name_or_id('6765675')
    print(user_id)
    user_groups = vk.groups_get(user_id)
    print(user_groups)
    '''
    for friend in vk.friends_get(user_id):
        friend_groups = vk.groups_get(friend)
        user_groups = user_groups - friend_groups
    if user_groups:
        json_data = vk.groups_getById(', '.join(map(str, user_groups)))
        if json_data:
            with open('groups.json', mode='w', encoding='utf8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
                '''
