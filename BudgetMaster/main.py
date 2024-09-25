import os
import datetime
import time
import functools


def dec_while(func):
    """
    Декоратор, который будет выполнять переданную функцию, пока она возвращает False
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        greeting_answer = func(*args, **kwargs)
        while greeting_answer == 0:
            greeting_answer = func(*args, **kwargs)
        return greeting_answer
    return wrapper

class WrongPassword(Exception):
    """
    Исключение, возбуждающееся при неправильном вводе пароля три раза
    """
    pass

class User:
    """
    Класс, отвечающий за инициализацию пользователя
    """
    
    def __init__(self, user_name, password, path):
        self.user_name = user_name
        self.password = password
        self.path = path

    def info(self):
        """
        Выводит информацию о текущем пользователе
        """
        print(f'Имя пользователя: {self.user_name}')
        print(f'Пароль: {self.password}')
        print(f'Путь до личной директории: {self.path}')

    @staticmethod
    def registration(user_name, password):
        """
        Статический метод регистрации нового пользователя
        """

        try:
            os.mkdir('users/' + user_name)
            user_path = 'users/' + user_name

            password_file = open(user_path + '/password.txt', 'w')
            password_file.write(password)
            password_file.close()

            category_file = open(user_path + '/categories.txt', 'w')
            category_file.close()

            print(f'\nПоздравляем, {user_name}, ваш аккаунт успешно создан!\nТеперь войдите в него')
            time.sleep(1)
            return 1

        except FileExistsError:
            print('\nДанное имя занято. Попробуйте другое')
            time.sleep(1)
            return 0

    @staticmethod
    def check_user(user_name, password):
        """
        Статический метод проверки правильности введённых данных уже зарегистрированного пользователя
        """

        user_path = 'users/' + user_name + '/'
        if os.path.isdir(user_path):
            print(f'\nПользователь {user_name} найден!')
            with open(user_path + 'password.txt') as password_file:
                if password == password_file.read():
                    time.sleep(1)
                    return user_path
                if User.check_password(user_name):
                    time.sleep(1)
                    return user_path
        else:
            print('\nПользователя с таким именем не найдено! Повторите ввод данных или создайте аккаунт')
            time.sleep(1)
            return 0

    @staticmethod
    def check_password(user_name):
        """
        Метод, вызывающийся при неправильно введённом пароле
        """

        print('\nВы ввели ваш пароль неверно. Повторите попытку')
        with open('users/' + user_name + '/password.txt') as password_file:
            password = password_file.read()
        for i in range(3):
            inserted_password = input('\nВведите ваш пароль повторно: ')
            if inserted_password == password:
                time.sleep(1)
                return 1
            else:
                print('Пароль неверный!')

        print('\nВы воспользовались трёмя попытками ввода пароля. Доступ запрещён')
        raise WrongPassword('Были израсходованы три попытки ввода пароля. Экстренное завершение программы')


class Categories:
    """
    Класс для управления категориями трат
    """

    def __init__(self, path):
        self.path_categories = path + '/categories.txt'
        with open(self.path_categories, mode='r', encoding='utf-8') as categories:
            self.len = len(categories.readlines())

    def info(self):
        """
        Выводит количество и текущий список категорий
        """

        print(f'Количество категорий: {self.len}')
        time.sleep(1)
        with open(self.path_categories, mode='r+', encoding='utf-8') as categories:
            print(f'Список категорий:\n{[line.strip() for line in categories.readlines()]}')

    def add_category(self, str_of_categories):
        """
        Добавляет введённые категории в файл categories
        """

        lst = list(set([category.strip(' ,.').lower() for category in str_of_categories.split()]))
        lst_for_append = []

        with open(self.path_categories, mode='r+', encoding='utf-8') as categories:
            categories_list = [line.strip() for line in categories.readlines()]

        for category in lst:
            if category in categories_list:
                print(f'Категория <{category}> уже есть в списке')
                time.sleep(0.5)
                continue
            lst_for_append.append(category)

        if lst_for_append:
            if self.len == 0:
                file = open(self.path_categories, mode='w')
            else:
                file = open(self.path_categories, mode='a')

            for category in lst_for_append:
                self.len += 1
                file.write(category + '\n')
            file.close()
            print('Категории успешно добавлены!')

        else:
            print('Добавлять нечего, все категории и так в списке')

    def delete_category(self, str_of_categories):
        """
        Удаляет введённые категории из файла categories
        """

        if self.len:
            lst = list(set([category.strip(' ,.').lower() for category in str_of_categories.split()]))

            with open(self.path_categories, mode='r', encoding='utf-8') as categories:
                categories_list = [line.strip() for line in categories.readlines()]

            for category in lst:
                if category not in categories_list:
                    print(f'Категории <{category}> нет в списке')
                    time.sleep(0.5)
                    continue
                categories_list.remove(category)
                self.len -= 1

            file = open(self.path_categories, mode='w')
            if self.len != 0:
                for category in categories_list:
                    file.write(category + '\n')
            file.close()
            print('Категории успешно удалены!')

        else:
            print('Удалять нечего, список пустой')

    def delete_all(self):
        """
        Удаляет все категории из списка
        """

        self.len = 0

        file = open(self.path_categories, 'w')
        file.close()

        print('Все категории успешно удалены!')


class Wastes:
    """
    Класс, отвечающий за манипулирование тратами пользователя
    """

    def __init__(self, path):
        self.path = path

    @dec_while
    def add_waste(self):
        """
        Добавляет затраты в файл за определённый день
        """

        while True:
            answer = input('\nЗа какой день вы хотите внести затраты?\n1 - за сегодня\n2 - за другую дату\n0 - выйти в меню\n')
            if (answer == '1') or (answer == '2'):
                break
            elif answer == '0':
                return 1
            else:
                print('Неверный ввод! Повторите попытку или введите 0 для выхода в меню')
                time.sleep(1)

        if answer == '1':
            data = datetime.date.today().strftime('%d_%m_%y')
        elif answer == '2':
            data = input('\nВведите необходимую дату в формате дд.мм.гг: ')
            try:
                day, month, year = data.split('.')
                datetime.date(int(year), int(month), int(day))
                data = '_'.join(data.split('.'))
            except:
                print('Неверный ввод! Попробуйте ещё раз!')
                time.sleep(1)
                return 0

        try:
            file = open(self.path + data + '.txt', mode='a')
        except:
            file = open(self.path + data + '.txt', mode='w')

        with open(self.path + '/categories.txt', mode='r', encoding='utf-8') as categories:
            categories = [line.strip() for line in categories.readlines()]
        print(f'Список доступных категорий:\n{categories}')

        while True:
            try:
                waste = input('\nВведите категорию и сумму через пробел\nЕсли хотите закончить, введите ноль\n').split()
                category, summa = waste[0], int(waste[1])
            except:
                if waste[0] == '0':
                    file.close()
                    return 0
                print('Неверный формат ввода! Попробуйте ещё раз')
                time.sleep(1)
                continue

            if category not in categories:
                print(f'Категории <{category}> нет в записанных категориях! Добавьте её в категории, прежде чем использовать\n')
                time.sleep(0.5)
            else:
                file.write(' '.join(waste) + '\n')
                print('Затрата внесена!')
                time.sleep(0.5)

    @dec_while
    def delete_waste(self):
        """
        Удаляет трату за определённый день
        """

        while True:
            answer = input('\nЗа какой день вы хотите удалить затраты?\n1 - за сегодня\n2 - за другую дату\n0 - выйти в меню\n')
            if (answer == '1') or (answer == '2'):
                break
            elif answer == '0':
                return 1
            else:
                print('Неверный ввод! Повторите попытку или введите 0 для выхода в меню')
                time.sleep(1)

        if answer == '1':
            data = datetime.date.today().strftime('%d_%m_%y')
        elif answer == '2':
            data = input('\nВведите необходимую дату в формате дд.мм.гг: ')
            try:
                day, month, year = data.split('.')
                datetime.date(int(year), int(month), int(day))
                data = '_'.join(data.split('.'))
            except:
                print('Неверный ввод! Попробуйте ещё раз!')
                time.sleep(1)
                return 0

        try:
            with open(self.path + data + '.txt', mode='r', encoding='utf-8') as wastes:
                wastes = [line.strip() for line in wastes.readlines()]
            print(f'Траты за {data}:')
            for index, waste in enumerate(wastes, 1):
                print(f'{index}: {waste}')
                time.sleep(0.5)
        except:
            print(f'Трат за {data} нет! Возврат в меню удаления\n')
            time.sleep(1)
            return 0


        while True:
            index = int(input('\nВведите индекс траты, которую хотите удалить или введите ноль, чтобы выйти в меню удаления\n'))
            try:
                print(f'Удаление траты <{wastes.pop(index - 1)}> прошло успешно!')

                if wastes:
                    print('\nОставшиеся траты:')
                    for index, waste in enumerate(wastes, 1):
                        print(f'{index}: {waste}')
                        time.sleep(0.5)
                else:
                    print('\nВы удалили все траты! Возврат в меню удаления\n')
                    os.remove(self.path + data + '.txt')
                    time.sleep(1)
                    return 0

            except:
                if index == '0':
                    file = open(self.path + data + '.txt', mode='w')
                    for waste in wastes:
                        file.write(waste + '\n')
                    file.close()
                    return 0
                print('Неверный формат ввода или неверный индекс траты! Попробуйте ещё раз')
                time.sleep(1)
                continue

    @dec_while
    def info(self):
        """
        Выводит информацию о тратах за определённую дату
        """

        while True:
            answer = input('\nЗа какой день вы хотите просмотреть информацию о затратах?\n1 - за сегодня\n2 - за другую дату\n0 - выйти в меню\n')
            if (answer == '1') or (answer == '2'):
                break
            elif answer == '0':
                return 1
            else:
                print('Неверный ввод! Повторите попытку или введите 0 для выхода в меню')
                time.sleep(1)

        if answer == '1':
            data = datetime.date.today().strftime('%d_%m_%y')
        elif answer == '2':
            data = input('\nВведите необходимую дату в формате дд.мм.гг: ')
            try:
                day, month, year = data.split('.')
                datetime.date(int(year), int(month), int(day))
                data = '_'.join(data.split('.'))
            except:
                print('Неверный ввод! Попробуйте ещё раз!')
                time.sleep(1)
                return 0

        try:
            with open(self.path + data + '.txt', mode='r', encoding='utf-8') as wastes:
                wastes = [line.strip() for line in wastes.readlines()]
        except:
            print(f'Трат за {data} нет! Возврат в меню информации\n')
            time.sleep(1)
            return 0

        while True:
            answer = input('\nКакую информацию вы хотите просмотреть за этот день? Введите порядковый номер\n'
                           '1 - Просмотреть все затраты\n'
                           '2 - Просмотреть затраты по определённой категории\n'
                           '0 - Возврат в меню информации\n')

            if (answer == '1') or (answer == '2'):
                break
            elif answer == '0':
                return 1
            else:
                print('Неверный ввод! Повторите попытку или введите 0 для выхода в меню\n')
                time.sleep(1)

        if answer == '1':
            print(f'Траты за {data}:')
            for index, waste in enumerate(wastes, 1):
                print(f'{index}: {waste}')
                time.sleep(0.5)
            time.sleep(1)
            return 0

        elif answer == '2':
            with open(self.path + '/categories.txt', mode='r', encoding='utf-8') as categories:
                categories = [line.strip() for line in categories.readlines()]

            with open(self.path + data + '.txt', mode='r', encoding='utf-8') as wastes:
                wastes = [line.strip() for line in wastes.readlines()]

            while True:
                print(f'Список доступных категорий:\n{categories}')
                answer = input('\nВведите категорию, по которой хотите посмотреть затраты или введите 0, чтобы выйти в меню информации: ')

                try:
                    summa = sum(map(lambda waste: int(waste[1]), filter(lambda waste: waste[0] == answer, [line.split() for line in wastes])))
                    print(f'\nСуммарные затраты по категории <{answer}> = {summa}')
                    time.sleep(1)
                    return 0
                except:
                    if answer == '0':
                        return 0
                    print('Неверный формат ввода или трат такой категории за данный день нет!')


@dec_while
def greeting():
    """
    Функция приветствия пользователя при запуске программы
    """

    print('\nДобро пожаловать в программу BudgetManager!')
    answer = input('Введите 0, если хотите зарегистрироваться в программе. Введите 1, если уже зарегистрированы\n')

    if answer not in ('0', '1'):
        print('Некорректный ввод!')
        time.sleep(1)
        return 0

    if answer == '1':
        while True:
            try:
                user_name, password = input('\nВведите имя пользователя и пароль через пробел для входа в приложение:\n').split()
            except ValueError:
                print('Некорректный ввод. Попробуйте ещё раз')
                continue

            answer = User.check_user(user_name, password)
            if answer != 0:
                print(f'Добро пожаловать {user_name}!')
                time.sleep(1)
                return user_name, password, answer
            else:
                answer = input('Хотите попробовать войти в аккаунт ещё раз? (Да или нет)\nЕсли необходимо создать аккаунт выберите "нет"\n')
                if answer.lower() == 'да':
                    time.sleep(1)
                    continue
                elif answer.lower() == 'нет':
                    time.sleep(1)
                    return 0
                else:
                    print('Некорректный ввод!')
                    time.sleep(1)
                    return 0

    elif answer == '0':
        while True:
            try:
                user_name, password = input('\nВведите имя пользователя и пароль через пробел для регистрации в приложении:\n').split()
            except ValueError:
                print('Некорректный ввод. Попробуйте ещё раз')
                continue

            if User.registration(user_name, password):
                time.sleep(1)
                return 0
            else:
                answer = input('Хотите попробовать создать аккаунт ещё раз? (Да или нет)\n')
                if answer.lower() == 'да':
                    time.sleep(1)
                    continue
                elif answer.lower() == 'нет':
                    time.sleep(1)
                    return 0
                else:
                    print('Некорректный ввод!')
                    time.sleep(1)
                    return 0

@dec_while
def main():
    """
    Ну тут и так всё понятно
    """

    while True:
        answer = input('\nЧто вы хотите сделать сегодня?\n'
                       '1 - Действия с категориями\n'
                       '2 - Действия с затратами\n'
                       '0 - Выход из приложения\n')
        time.sleep(0.5)

        if answer not in ('1', '2', '0'):
            print('Некорректный ввод! Повторите попытку')
            time.sleep(1)
            continue

        if answer == '1':
            while True:
                answer_category = input('\nДоступные действия с категориями:\n'
                               '1 - Вывести информацию о текущих категориях\n'
                               '2 - Добавить категории\n'
                               '3 - Удалить определённые категории\n'
                               '4 - Удалить все категории\n'
                               '0 - Возврат в меню\n')

                if answer_category not in ('1', '2', '3', '4', '0'):
                    print('Некорректный ввод! Повторите попытку')
                    time.sleep(1)
                    continue
                elif answer_category == '1':
                    categories.info()
                    time.sleep(1)
                    continue
                elif answer_category in ('2', '3'):
                    answer_for = input('\nВведите необходимые категории через пробел: ')
                    if answer_category == '2':
                        categories.add_category(answer_for)
                        time.sleep(1)
                    else:
                        categories.delete_category(answer_for)
                        time.sleep(1)
                    continue
                elif answer_category == '4':
                    categories.delete_all()
                    time.sleep(1)
                    continue
                else:
                    time.sleep(1)
                    return 0

        elif answer == '2':
            while True:
                answer_waste = input('\nДоступные действия с затратами:\n'
                                        '1 - Вывести информацию о затратах за определённый день\n'
                                        '2 - Добавить затраты за определённый день\n'
                                        '3 - Удалить затраты за определённый день\n'
                                        '0 - Возврат в меню\n')

                if answer_waste not in ('1', '2', '3', '0'):
                    print('Некорректный ввод! Повторите попытку')
                    time.sleep(1)
                    continue
                elif answer_waste == '1':
                    wastes.info()
                    time.sleep(1)
                    continue
                elif answer_waste == '2':
                    wastes.add_waste()
                    time.sleep(1)
                    continue
                elif answer_waste == '3':
                    wastes.delete_waste()
                    time.sleep(1)
                    continue
                else:
                    time.sleep(1)
                    return 0

        else:
            print('До новых встреч!')
            return 1



user = User(*greeting())
categories = Categories(user.path)
wastes = Wastes(user.path)

print(f'\nЗдравствуйте, {user.user_name}!')
print(f'Если вы впервые в этом приложении, то сначала рекомендуется завести список категорий, по которым будут фиксироваться траты.')
time.sleep(0.5)

main()


