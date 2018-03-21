from time import sleep
from operator import itemgetter
import datetime
import matplotlib.pyplot as plt
import vk


def get_token():
    file = open("access_token.txt", "r")
    access_token = file.read()
    file.close()
    return access_token[:-1]


def get_group(api):
    users_groups = api.groups.get(v=5.73)
    return users_groups['items']


def get_age(day, month, year):
    now = datetime.datetime.now()
    if (int(day) > now.day and int(month) >= now.month) or (int(month) > now.month):
        return now.year - int(year) - 1
    return now.year - int(year)


def create_dict(list_members, sex, birthdays, fnames, mnames):
    for member in list_members:
        names = member['first_name']
        if member['sex'] == 1:
            sex['female'] += 1
            if str(names) not in fnames:
                fnames['{}'.format(names)] = 1
            else:
                fnames['{}'.format(names)] += 1
        elif member['sex'] == 2:
            sex['male'] += 1
            if str(names) not in mnames:
                mnames['{}'.format(names)] = 1
            else:
                mnames['{}'.format(names)] += 1
        else:
            sex['None'] += 1
        try:
            day, month, year = member['bdate'].split('.')
            age = get_age(day, month, year)
            if str(age) not in birthdays:
                birthdays['{}'.format(age)] = 1
            else:
                birthdays['{}'.format(age)] += 1
        except Exception:
            continue


def get_members_of_public(api, list_group):
    offset = 0
    members_o_f_group = []
    birthdays = {}
    fnames = {}
    mnames = {}
    sex = {'male': 0, 'female': 0, 'None': 0}
    while True:
        part_of_users = api.groups.getMembers(group_id=list_group[0], offset=offset, count=1000, v=5.73,fields='bdate, sex')
        if not part_of_users['items']:
            return [members_o_f_group, birthdays, sex, fnames, mnames]
        members_o_f_group.extend(part_of_users['items'])
        create_dict(part_of_users['items'], sex, birthdays, fnames, mnames)
        offset += 1000
        sleep(0.25)


def get_diagram(api, Data, public_name):
    piecesAGE = Data[1].values()
    textAGE = Data[1].keys()

    plt.pie(piecesAGE,
            labels=textAGE,
            shadow=1,
            startangle=90,
            autopct='%1.1f%%')
    plt.text(-1.5, 1.05,
             'Всего в группе \n {} участников'.format(len(Data[0])),
             size='large')
    plt.text(-1.5, -1.05,
             'Из них:\n {} - мужчины \n {} - женщины\n {} - пол не указан'.format(Data[2]['male'], Data[2]['female'], Data[2]['None']),
             size='large')
    F = sorted(Data[3].items(), key=itemgetter(1),reverse=True)
    M = sorted(Data[4].items(), key=itemgetter(1),reverse=True)
    plt.text(-1.7,-1.2,'Самое популярное женское имя {}\n Самое популярное мужское имя {}'.format(F[1], M[1]), size='large')
    plt.title('Диаграмма возрастов\n{}'.format(public_name))
    plt.show()
session = vk.Session(access_token=get_token())
api = vk.API(session)
list_group = get_group(api)
public_name = api.groups.getById(group_id=list_group[0], fields='name', v=5.73)[0]['name']
sleep(0.25)
Data = get_members_of_public(api, list_group)
get_diagram(api, Data, public_name)
