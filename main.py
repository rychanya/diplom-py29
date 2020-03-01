from api import VKAPI
import json

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


def main(name_or_id, n):
    vk = VKAPI(TOKEN)
    user_id = vk.get_id_from_name_or_id(name_or_id)
    if user_id:
        print(f'User id {user_id}')
    else:
        print('User not found. Continue with current user.')
    print('Try get users groups')
    groups = vk.groups_get(user_id)
    if groups:
        print(f'Find {len(groups)} groups.')
    else:
        print('User don`t have any groups.')
        return
    print('Try get friends.')
    friends = vk.friends_get(user_id)
    if friends:
        print(f'Find {len(friends)} friends.')
    else:
        print('User don`t have any friends.')
        return
    friends_count = len(friends)
    groups_out = {}
    for number, friend in enumerate(friends, start=1):
        print(f'Parse {number} of {friends_count}')
        friend_groups = vk.groups_get(friend)
        for group in friend_groups:
            if group in groups:
                groups_out.setdefault(group, 0)
                groups_out[group] += 1
    groups = [group for group, value in groups_out.items() if value <= n]
    if groups:
        print('Try get groups info')
        json_data = vk.groups_getById(', '.join(map(str, groups)))
        if json_data:
            with open('groups.json', mode='w', encoding='utf8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
                print('Data saved to file')


if __name__ == '__main__':
    name_or_id = 'rychanya'  # Имя или id пользователя
    N = 2  # Не более N человек
    main(name_or_id, N)
