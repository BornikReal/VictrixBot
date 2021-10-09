from javascript import require, On, Once
import time
import os
import urllib.request
import threading
import datetime
import re
import ssl

list_of_users = []
tasks_of_users = []
admin_commands = ["bal", "help", "baltop", "pay", "ping", "info", "addbal", "delbal", "update",
                  "resetbal", "chat", "op", "deop", "transfer", "confirm", "seen", "settime", "setdaily", "taskc", "tasku", "stop", "start", "restart", "safemode", "kvinboost"]


def logaddcommand(sender, command):
    f = open("logs\VB_command_logs.txt", "a", encoding="utf-8-sig")
    f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) +
            "|" + sender + " использовал(а) команду: " + command + "\n")
    f.close()


def logaddmessage(message):
    f = open("logs\VB_chat_logs.txt", "a", encoding="utf-8-sig")
    f.write(str(datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S')) + "|" + message + "\n")
    f.close()


def logadderror(errmes):
    f = open("logs\VB_crash_logs.txt", "a", encoding="utf-8-sig")
    f.write(str(datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S')) + "|" + errmes + "\n")
    f.close()


BOT_USERNAME = "VictrixBot"
settings = [2, 3600, 1, 1, 0, 7]
if datetime.datetime.today().weekday() != 5:
    tasks = [2, 3, 1, 1, 1]
else:
    tasks = [5, 1, 1, 1]


def getdate():
    return datetime.datetime.strptime(datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d %H:%M'), "%Y-%m-%d %H:%M")


if os.path.exists("VB_settings.txt"):
    f = open("VB_settings.txt", "r", encoding="utf-8-sig")
    settings = []
    for i in f:
        settings.append(int(i))
    f.close()
else:
    f = open("VB_settings.txt", "w", encoding="utf-8-sig")
    for i in settings:
        f.write(str(i) + "\n")
    f.close()


def ParseMC(givep):
    global tasks
    pos = 0
    list_of_users = []
    tasks_of_users = []
    try:
        fp = urllib.request.urlopen(
            "https://minecorp.ru/clan/Victrix", context=ssl.SSLContext())
        mystr = fp.read().decode("utf8")
        fp.close()
        start = mystr.find("<a", mystr.find("<td>Участники</td>"))
        end = mystr.rfind("a", start, mystr.find("</td>", start)) + 2
        mystr = mystr[start:end]
        while (mystr.find("<a") != -1):
            st = mystr.find("]") + 2
            en = mystr.find("</span>")
            name = mystr[st:en]
            st = mystr.find("<a", st)
            mystr = mystr[st:]
            if (name == "VictrixBot") or (name == "VictrixStatBot"):
                continue
            list_of_users.append([name])
            tasks_of_users.append([name])
            for i in range(1, settings[5]):
                list_of_users[-1].append(0)
            list_of_users[-1].append(pos)
            list_of_users[-1][5] = 1
            list_of_users[-1][6] = getdate()
            for i in range(1, (len(tasks) + 1)):
                tasks_of_users[-1].append(0)
            if (givep):
                pos += 1
    except (urllib.error.URLError, urllib.error.HTTPError, urllib.error.ContentTooShortError):
        print("Minecorp.ru is not available")
        logadderror("Minecorp.ru is not available")
    return [list_of_users, tasks_of_users]


alllist = ParseMC(True)
list_of_users = alllist[0]
tasks_of_users = alllist[1]
date_flag = datetime.date.today()
if os.path.exists("VB_kvin_list.txt"):
    f = open("VB_kvin_list.txt", "r", encoding="utf-8-sig")
    date_bool = True
    for i in f:
        if date_bool:
            date_flag = datetime.datetime.strptime(i[:-1], "%Y-%m-%d").date()
            date_bool = False
        else:
            user_param = i[:-1].split('|')
            for j in list_of_users:
                if user_param[0] == j[0]:
                    for z in range(1, settings[5]):
                        if (z != 6):
                            j[z] = int(user_param[z])
                    j[6] = datetime.datetime.strptime(
                        user_param[6], "%Y-%m-%d %H:%M")
                    if (date_flag != datetime.date.today()):
                        j[3] = 0
                        j[4] = 0
                    else:
                        j[3] = int(user_param[3])
                        j[4] = int(user_param[4])
                    break
    f.close()
    list_of_users.sort(key=lambda x: x[1], reverse=True)

date_flag = datetime.date.today()
if os.path.exists("VB_tasks_list.txt"):
    f = open("VB_tasks_list.txt", "r", encoding="utf-8-sig")
    date_bool = True
    for i in f:
        if date_bool:
            date_flag = datetime.datetime.strptime(i[:-1], "%Y-%m-%d").date()
            if (date_flag != datetime.date.today()):
                break
            else:
                date_bool = False
        else:
            user_param = i[:-1].split('|')
            for j in tasks_of_users:
                if user_param[0] == j[0]:
                    for z in range(1, (len(tasks) + 1)):
                        j[z] = int(user_param[z])
    f.close()

f = open("VB_kvin_list.txt", "w", encoding="utf-8-sig")
f.write(str(datetime.date.today()) + "\n")
for i in list_of_users:
    f.write(i[0])
    for j in range(1, 6):
        f.write("|" + str(i[j]))
    f.write("|" + datetime.datetime.strftime(i[6], '%Y-%m-%d %H:%M'))
    for j in range(7, settings[5]):
        f.write("|" + str(i[j]))
    f.write("\n")
f.close()

f = open("VB_tasks_list.txt", "w", encoding="utf-8-sig")
f.write(str(datetime.date.today()) + "\n")
for i in tasks_of_users:
    f.write(i[0])
    for j in range(1, (len(tasks) + 1)):
        f.write("|" + str(i[j]))
    f.write("\n")
f.close()


def updatelist():
    global list_of_users, tasks_of_users
    try:
        pl_on = re.compile(
            r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', str(bot.players))
        for i in list_of_users:
            name = "username: '" + i[0] + "'"
            if name in pl_on:
                if (i[3] == 0):
                    i[3] = 1
                    i[1] += (settings[3] * i[5])
                    logaddcommand(BOT_USERNAME, str("addbal " +
                                                    i[0] + " " + str(settings[3] * i[5])))
                    Answer(i[0], 0, str(" Вы получили " +
                           str(settings[3] * i[5]) + "₭ за ежедневный вход!"))
    except BaseException:
        print("Updating error")
    alllist = ParseMC(False)
    new_list_of_users = alllist[0]
    new_tasks_of_users = alllist[1]
    for i in list_of_users:
        for j in new_list_of_users:
            if i[0] == j[0]:
                for z in range(1, settings[5]):
                    j[z] = i[z]
                break
    new_list_of_users.sort(key=lambda x: x[1], reverse=True)
    for i in tasks_of_users:
        for j in new_tasks_of_users:
            if i[0] == j[0]:
                for z in range(1, (len(tasks) + 1)):
                    j[z] = i[z]
                break
    if (len(new_list_of_users) > 10):
        list_of_users = new_list_of_users
    if (len(new_tasks_of_users) > 10):
        tasks_of_users = new_tasks_of_users
    f = open("VB_kvin_list.txt", "r", encoding="utf-8-sig")
    date_flag = datetime.date.today()
    for i in f:
        date_flag = datetime.datetime.strptime(i[:-1], "%Y-%m-%d").date()
        break
    f.close()
    if date_flag != datetime.date.today():
        for i in list_of_users:
            i[3] = 0
            i[4] = 0
        for i in tasks_of_users:
            for j in range(1, (len(tasks) + 1)):
                i[j] = 0
    f = open("VB_kvin_list.txt", "w", encoding="utf-8-sig")
    f.write(str(datetime.date.today()) + "\n")
    pos = 0
    for i in list_of_users:
        i[-1] = pos
        pos += 1
        f.write(i[0])
        for j in range(1, 6):
            f.write("|" + str(i[j]))
        f.write("|" + datetime.datetime.strftime(i[6], '%Y-%m-%d %H:%M'))
        for j in range(7, settings[5]):
            f.write("|" + str(i[j]))
        f.write("\n")
    f.close()
    f = open("VB_tasks_list.txt", "w", encoding="utf-8-sig")
    f.write(str(datetime.date.today()) + "\n")
    for i in tasks_of_users:
        f.write(i[0])
        for j in range(1, (len(tasks) + 1)):
            f.write("|" + str(i[j]))
        f.write("\n")
    f.close()
    f = open("VB_settings.txt", "w", encoding="utf-8-sig")
    for i in settings:
        f.write(str(i) + "\n")
    f.close()
    print("Список обновлён")


mineflayer = require('mineflayer')
try:
    bot = mineflayer.createBot({'host': 'classic.minecorp.ru',
                                'port': 25565, 'username': BOT_USERNAME, 'hideErrors': False})
except BaseException:
    print("Failed to creat bot")


def Answer(sender, priority, message):
    if priority == 2:
        print("[SYSTEM MESSAGE]" + message)
    else:
        bot.chat("/corpm " + sender + " " + message)
        time.sleep(settings[0])


def ClearMessage(message):
    message = message.replace("Ⓐ", "")
    message = message.replace("Ⓑ", "")
    message = message.replace("Ⓒ", "")
    message = message.replace("Ⓗ", "")
    message = message.replace("Ⓥ", "")
    message = message.replace("Ⓜ", "")
    message = message.replace("Ⓣ", "")
    message = message.replace("Ⓙ", "")
    message = message.replace("Ⓞ", "")
    message = message.replace(chr(10144), "")
    return message


def bal(sender, command, user, priority):
    if len(command) == 1:
        if (priority == 2):
            Answer(sender, priority, str(
                "Данная команда доступна в консоле только в формате bal [Ник]"))
        else:
            Answer(sender, priority, str("Ваш баланс: " +
                   str(list_of_users[user][1]) + "₭"))
            logaddcommand(sender, ' '.join(command))
    elif len(command) == 2:
        d = True
        for i in list_of_users:
            if command[1].lower() == i[0].lower():
                d = False
                Answer(sender, priority, str(
                    "Баланс " + i[0] + ": " + str(i[1]) + "₭"))
                logaddcommand(sender, ' '.join(command))
                break
        if (d):
            Answer(sender, priority, str(
                "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))
    else:
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: bal [Ник (необязательно)]"))


def help(sender, command, priority):
    if len(command) == 1:
        if (priority == 0):
            Answer(sender, priority, str(
                "Список команд бота: bal, help, baltop, pay, ping, info, seen"))
            Answer(sender, priority, str(
                "Для получения подробной информации по каждой команде используйте help [Комманда]"))
        elif (priority == 1):
            Answer(sender, priority, str(
                "Список команд бота: bal, help, baltop, pay, ping, info, addbal, delbal, update"))
            Answer(sender, priority, str(
                "resetbal, chat, op, deop, transfer, seen, settime, setdaily, taskc, tasku, stop,"))
            Answer(sender, priority, str("restart, safemode, kvinboost"))
            Answer(sender, priority, str(
                "Для получения подробной информации по каждой команде используйте help [Комманда]"))
        else:
            Answer(sender, priority, str(
                "Список команд бота: bal, help, baltop, ping, info, addbal, delbal, update, chat, resetbal, op, deop, transfer, seen, settime, setdaily, taskc, tasku, stop, start, safemode, restart, kvinboost"))
            Answer(sender, priority, str(
                "Для получения подробной информации по каждой команде используйте help [Комманда]"))
    elif len(command) == 2:
        logaddcommand(sender, ' '.join(command))
        if (command[1] == "bal"):
            if (priority != 2):
                Answer(sender, priority, str(
                    "Команда для просмотра вашего или чужого баланса. Формат: bal [Ник (необязательно)]"))
            else:
                Answer(sender, priority, str(
                    "Команда для просмотра баланса игрока. Формат: bal [Ник]"))
        elif (command[1] == "help"):
            Answer(sender, priority, str(
                "Команда для получения справки по командам. Формат: help [Комманда (необязательно)]"))
        elif (command[1] == "baltop"):
            Answer(sender, priority, str(
                "Команда для вывода топ 5 самых богатых игроков клана. Формат: baltop"))
        elif (command[1] == "pay"):
            Answer(sender, priority, str(
                "Команда для передачи квинов другому игроку. Формат: pay [Ник] [Сумма]"))
            Answer(sender, priority, str(
                "За раз можно передать от 5 до 25 квин"))
            Answer(sender, priority, str(
                "Комиссия за перевод: до 10₭ - 3₭, до 15₭ - 5₭, до 20₭ - 7₭, до 25₭ - 10₭"))
        elif (command[1] == "ping"):
            Answer(sender, priority, str(
                "Команда для проверки бота. Формат: ping"))
        elif (command[1] == "info"):
            Answer(sender, priority, str(
                "Команда для вывода информации о боте. Формат: info"))
        elif (command[1] == "seen"):
            Answer(sender, priority, str(
                "Команда для получения информации о наигранном времени. Формат: seen"))
        elif (command[1] in admin_commands):
            if (priority == 0):
                Answer(sender, priority, str(
                    "Информация об этих командах доступна только администраторам."))
            elif (command[1] == "addbal"):
                Answer(sender, priority, str(
                    "Команда для пополнения баланса игрока. Формат: addbal [Ник] [Сумма]"))
            elif (command[1] == "delbal"):
                Answer(sender, priority, str(
                    "Команда для снятия с баланса игрока. Формат: delbal [Ник] [Сумма]"))
            elif (command[1] == "update"):
                Answer(sender, priority, str(
                    "Команда для обновления данных бота. Формат: update"))
            elif (command[1] == "resetbal"):
                Answer(sender, priority, str(
                    "Команда для обнуления квинов игроку. Формат: resetbal [Ник]"))
            elif (command[1] == "chat"):
                Answer(sender, priority, str(
                    "Команда для написания сообщения в клан. чат от имени бота. Формат: chat [Сообщение]"))
            elif (command[1] == "op"):
                Answer(sender, priority, str(
                    "Команда для выдачи прав администратора игроку. Формат: op [Сообщение]"))
            elif (command[1] == "deop"):
                Answer(sender, priority, str(
                    "Команда для снятия прав администратора с игрока. Формат: deop [Сообщение]"))
            elif (command[1] == "transfer"):
                Answer(sender, priority, str(
                    "Команда для перевода баланса без комиссии с одного игрока к другому"))
                Answer(sender, priority, str(
                    "Формат: transfer [Ник игрока, у которго забирают] [Ник игрока получателя] [Сумма]"))
            elif (command[1] == "settime"):
                Answer(sender, priority, str(
                    "Команда для установки времени, необходимого для получения награды, и размера награды"))
                Answer(sender, priority, str(
                    "Формат: settime [Время] [Сумма]"))
            elif (command[1] == "taskc"):
                Answer(sender, priority, str(
                    "Команда для выдачи награды за задание"))
                Answer(sender, priority, str(
                    "Формат: taskc [Ник] [Номер задания]"))
            elif (command[1] == "tasku"):
                Answer(sender, priority, str(
                    "Команда для отмены выполнения задания"))
                Answer(sender, priority, str(
                    "Формат: tasku [Ник] [Номер задания]"))
            elif (command[1] == "stop"):
                Answer(sender, priority, str(
                    "Команда для выключения бота"))
                Answer(sender, priority, str(
                    "Формат: stop"))
            elif (command[1] == "restart"):
                Answer(sender, priority, str(
                    "Команда для перезагрузки бота"))
                Answer(sender, priority, str(
                    "Формат: restart"))
            elif (command[1] == "safemode"):
                Answer(sender, priority, str(
                    "Команда для включения безопасного режима"))
                Answer(sender, priority, str(
                    "Формат: safemode"))
            elif (command[1] == "kvinboost"):
                Answer(sender, priority, str(
                    "Команда для выдачи множителя на выдачу квинов"))
                Answer(sender, priority, str(
                    "Формат: kvinboost [Ник] [Множитель] [Секунды]"))
                Answer(sender, priority, str(
                    "Формат для отключения множителя: kvinboost [Ник]"))
            else:
                Answer(sender, priority, str("Команда не найдена"))
        else:
            Answer(sender, priority, str("Команда не найдена"))
    else:
        Answer(sender, priority, str(
            "Неверный формат команды. Инспользуйте help [Комманда (необязательно)]"))


def baltop(sender, command, priority):
    Answer(sender, priority, str("Топ 5 самых богатых игроков:"))
    for i in range(5):
        if (list_of_users[i][1] != 0):
            Answer(sender, priority, str(
                list_of_users[i][0] + " - " + str(list_of_users[i][1]) + "₭"))
            logaddcommand(sender, ' '.join(command))


def ping(sender, command, priority):
    Answer(sender, priority, str("Понг!"))
    logaddcommand(sender, ' '.join(command))


def info(sender, command, priority):
    Answer(sender, priority, str(
        "₭Квины - это виртуальная валюта клана Victrix, получаемая за выполнение заданий"))
    Answer(sender, priority, str(
        "Полную информацию вы можете найти в нашей беседе ВК или в Discord сервере"))
    Answer(sender, priority, str(
        "Ссылка на ВК - https://clck.ru/XUxxQ Ссылка на ДС - https://clck.ru/XUxwR"))
    Answer(sender, priority, str(
        "VictrixBot v1.3 by Adrian_Silva/BornikReal"))
    logaddcommand(sender, ' '.join(command))


def pay(sender, command, priority, user):
    if (priority == 2):
        Answer(sender, priority, str(
            "Данная команда недоступна для использования в консоли"))
    else:
        if (len(command) != 3):
            Answer(sender, priority, str(
                "Неверный формат команды. Правильный формат: pay [Ник] [Сумма]"))
        elif (not command[2].isdigit()):
            Answer(sender, priority, str(
                "Неверный формат команды. Правильный формат: pay [Ник] [Сумма]"))
        elif (int(command[2]) < 5) or (int(command[2]) > 25):
            Answer(sender, priority, str(
                "Минимальная сумма для перевода 5 квин, максимальная 25 квин."))
        else:
            d = True
            for i in list_of_users:
                if command[1].lower() == i[0].lower():
                    d = False
                    amount = int(command[2])
                    commis = 0
                    if (amount <= 10):
                        commis = 3
                    elif (amount <= 15):
                        commis = 5
                    elif (amount <= 20):
                        commis = 7
                    elif (amount <= 25):
                        commis = 10
                    if (list_of_users[user][1] - amount - commis) < 0:
                        Answer(sender, priority, str(
                            "Недостаточно средств на вашем счету."))
                        break
                    else:
                        list_of_users[user][1] -= (amount + commis)
                        i[1] += amount
                        updatelist()
                        Answer(sender, priority, str(
                            "Вы отправили " + command[2] + "₭ игроку " + i[0] + ". Комиссия " + str(commis) + "₭"))
                        Answer(i[0], 0, str(" Вы получили " +
                               command[2] + "₭ от игрока " + sender))
                        logaddcommand(sender, ' '.join(command))
                        break
            if (d):
                Answer(sender, priority, str(
                    "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def addbal(sender, command, priority):
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    else:
        if (len(command) != 3):
            Answer(sender, priority, str(
                "Неверный формат команды. Правильный формат: addbal [Ник] [Сумма]"))
        elif (not command[2].isdigit()):
            Answer(sender, priority, str(
                "Неверный формат команды. Правильный формат: addbal [Ник] [Сумма]"))
        else:
            d = True
            for i in list_of_users:
                if command[1].lower() == i[0].lower():
                    d = False
                    i[1] += int(command[2])
                    updatelist()
                    Answer(sender, priority, str(
                        "На счёт этого игрока положены квины."))
                    Answer(i[0], 0, str(
                        " Вам начислено на счёт " + command[2] + "₭"))
                    logaddcommand(sender, ' '.join(command))
                    break
            if (d):
                Answer(sender, priority, str(
                    "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def delbal(sender, command, priority):
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    else:
        if (len(command) != 3):
            Answer(sender, priority, str(
                "Неверный формат команды. Правильный формат: delbal [Ник] [Сумма]"))
        elif (not command[2].isdigit()):
            Answer(sender, priority, str(
                "Неверный формат команды. Правильный формат: delbal [Ник] [Сумма]"))
        else:
            d = True
            for i in list_of_users:
                if command[1].lower() == i[0].lower():
                    d = False
                    i[1] -= int(command[2])
                    if i[1] < 0:
                        i[1] = 0
                    updatelist()
                    Answer(sender, priority, str(
                        "С счета этого игрока сняты квины."))
                    Answer(i[0], 0, str(
                        " С вашего счёта сняты " + command[2] + "₭"))
                    logaddcommand(sender, ' '.join(command))
                    break
            if (d):
                Answer(sender, priority, str(
                    "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def update(sender, command, priority):
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    else:
        updatelist()
        Answer(sender, priority, str("Список успешно обновлён!"))
        logaddcommand(sender, ' '.join(command))


def resetbal(sender, command, priority):
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif len(command) != 2:
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: resetbal [Ник]"))
    else:
        d = True
        for i in list_of_users:
            if i[0].lower() == command[1].lower():
                d = False
                i[1] = 0
                Answer(sender, priority, str(
                    "Баланс этого игрока обнулён"))
                Answer(i[0], 0, str("Ваш баланс обнулён"))
                updatelist()
                logaddcommand(sender, ' '.join(command))
        if (d):
            Answer(sender, priority, str(
                "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def chat(sender, command, priority):
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    else:
        bot.chat("=" + ' '.join(command[1:]))
        logaddcommand(sender, ' '.join(command))


def op(sender, command, priority):
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif len(command) != 2:
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: op [Ник]"))
    else:
        d = True
        for i in list_of_users:
            if i[0].lower() == command[1].lower():
                d = False
                if (i[2] == 1):
                    Answer(sender, priority, str(
                        "У данного игрока уже есть права администратора"))
                else:
                    i[2] = 1
                    Answer(sender, priority, str(
                        "Данному игроку выданы права администратора"))
                    Answer(i[0], 0, str(" Вам выданы права администратора"))
                    logaddcommand(sender, ' '.join(command))
        if (d):
            Answer(sender, priority, str(
                "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def deop(sender, command, priority):
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif len(command) != 2:
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: deop [Ник]"))
    else:
        d = True
        for i in list_of_users:
            if i[0].lower() == command[1].lower():
                d = False
                if (i[2] == 0):
                    Answer(sender, priority, str(
                        "У данного игрока нет прав администратора"))
                else:
                    i[2] = 0
                    Answer(sender, priority, str(
                        "С этого игрока сняты права администратора"))
                    Answer(i[0], 0, str(" С вас сняли права администратора"))
                    logaddcommand(sender, ' '.join(command))
        if (d):
            Answer(sender, priority, str(
                "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def transfer(sender, command, priority):
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif (len(command) != 4):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: transfer [Ник] [Сумма]"))
    elif (not command[3].isdigit()):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: transfer [Ник] [Сумма]"))
    else:
        user1 = -1
        user2 = -1
        for i in list_of_users:
            if command[1].lower() == i[0].lower():
                user1 = list_of_users.index(i)
            elif command[2].lower() == i[0].lower():
                user2 = list_of_users.index(i)
            if (user1 != -1) and (user2 != -1):
                break
        if (user1 != -1) and (user2 != -1):
            amount = int(command[3])
            if (list_of_users[user1][1] - amount) < 0:
                Answer(sender, priority, str(
                    "Недостаточно средств на счету игрока."))
            else:
                list_of_users[user2][1] += amount
                list_of_users[user1][1] -= amount
                Answer(sender, priority, str(
                    "Вы отправили " + command[3] + "₭ игроку " + list_of_users[user2][0] + " со счёта " + list_of_users[user1][0]))
                Answer(list_of_users[user2][0], 0, str(
                    " Вам начислено на счёт " + command[3] + "₭"))
                Answer(list_of_users[user2][0], 0, str(
                    " С вашего счёта сняты " + command[3] + "₭"))
                logaddcommand(sender, ' '.join(command))
                updatelist()
        else:
            Answer(sender, priority, str(
                "Один или оба не были найдены в клане. Если это ошибка, повторите позже или используйте update"))


def seen(sender, command, priority, user):
    global list_of_users, settings
    if (priority == 2):
        Answer(sender, priority, str(
            "Данная команда недоступна для использования в консоли"))
    else:
        Answer(sender, priority, str("Следующая награда будет через " +
                                     str(int(list_of_users[user][4])) + "/" + str(settings[1]) + " сек."))
        if (list_of_users[user][5] > 1):
            Answer(sender, priority, str("Ваше {0}X увелечение квинов будет действовать до {1}".format(
                str(list_of_users[user][5]), datetime.datetime.strftime(list_of_users[user][6], '%Y-%m-%d %H:%M'))))
        logaddcommand(sender, ' '.join(command))


def settime(sender, command, priority):
    global settings, settings
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif (len(command) != 3):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: settime [Время] [Сумма]"))
    elif (not command[1].isdigit()) or (not command[2].isdigit()):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: settime [Время] [Сумма]"))
    else:
        settings[1] = int(command[1])
        settings[2] = int(command[2])
        updatelist()
        Answer(sender, priority, str(
            "Вы изменили условия и награждение за онлайн"))
        logaddcommand(sender, ' '.join(command))


def setdaily(sender, command, priority):
    global settings
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif (len(command) != 2):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: setdaily [Сумма]"))
    elif (not command[1].isdigit()):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: setdaily [Сумма]"))
    else:
        settings[3] = int(command[1])
        updatelist()
        Answer(sender, priority, str(
            "Вы изменили условия и награждение за ежедневный вход"))
        logaddcommand(sender, ' '.join(command))


def taskc(sender, command, priority):
    global settings, task_of_users, delay
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif (len(command) != 3):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: taskc [Ник] [Номер задания]"))
    elif (not command[2].isdigit()):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: taskc [Ник] [Номер задания]"))
    else:
        num = int(command[2])
        if (num < 1) or (num > len(tasks)):
            Answer(sender, priority, str("Такое задание не существует"))
        else:
            d = True
            for i in tasks_of_users:
                if command[1].lower() == i[0].lower():
                    d = False
                    if (i[num] == 1):
                        Answer(sender, priority, str(
                            "Данное задание уже было выполнено этим игроком"))
                    else:
                        for j in list_of_users:
                            if j[0] == i[0]:
                                i[num] = 1
                                j[1] += (tasks[num - 1] * j[5])
                                updatelist()
                                Answer(i[0], 0, str(
                                    " Вам начислено на счёт " + str(tasks[num - 1] * j[5]) + "₭"))
                                Answer(sender, priority, str(
                                    "Данное задание помечено как выполненное для этого игрока"))
                                logaddcommand(sender, ' '.join(command))
                                break
                    break
            if (d):
                Answer(sender, priority, str(
                    "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def tasku(sender, command, priority):
    global settings, task_of_users, delay
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif (len(command) != 3):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: tasku [Ник] [Номер задания]"))
    elif (not command[2].isdigit()):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: tasku [Ник] [Номер задания]"))
    else:
        num = int(command[2])
        if (num < 1) or (num > len(tasks)):
            Answer(sender, priority, str("Такое задание не существует"))
        else:
            d = True
            for i in tasks_of_users:
                if command[1].lower() == i[0].lower():
                    d = False
                    if (i[num] == 0):
                        Answer(sender, priority, str(
                            "Данное задание не было выполнено этим игроком"))
                    else:
                        for j in list_of_users:
                            if j[0] == i[0]:
                                i[num] = 0
                                j[1] -= (tasks[num - 1] * j[5])
                                updatelist()
                                Answer(i[0], 0, str(
                                    " С вашего счёта сняты " + str(tasks[num - 1] * j[5]) + "₭"))
                                Answer(sender, priority, str(
                                    "Данное задание помечено как невыполненное для этого игрока"))
                                logaddcommand(sender, ' '.join(command))
                                break
                    break
            if (d):
                Answer(sender, priority, str(
                    "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def stop_bot(sender, command, priority):
    global bot
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    else:
        Answer(sender, priority, str("Бот выключается"))
        logaddcommand(sender, ' '.join(command))
        bot.end()


def restart_bot(sender, command, priority):
    global bot, bot_online
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    else:
        Answer(sender, priority, str("Бот перезагружается"))
        logaddcommand(sender, ' '.join(command))
        bot_online = False
        bot.end()


def start_bot(sender, command, priority):
    global bot_online
    if (priority != 2):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    else:
        Answer(sender, priority, str("Бот включается"))
        logaddcommand(sender, ' '.join(command))
        bot_online = False


def safemode(sender, command, priority):
    global bot
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    else:
        if (settings[4] == 0):
            settings[4] = 1
            bot.chat("=Бот работает в безопасном режиме. Функционал ограничен")
            logaddcommand(sender, ' '.join(command))
        elif (priority == 2):
            settings[4] = 0
            bot.chat("=Бот работает в обычном режиме. Функционал восстановлен")
            logaddcommand(sender, ' '.join(command))
        else:
            Answer(sender, priority, str(
                "Недостаточно прав для выполнения данной команды!"))


def kvinboost(sender, command, priority, user):
    global list_of_users, task_of_users
    if (priority == 0):
        Answer(sender, priority, str(
            "Недостаточно прав для выполнения данной команды!"))
    elif (len(command) == 2):
        d = True
        for i in list_of_users:
            if i[0].lower() == command[1].lower():
                d = False
                if i[5] == 1:
                    Answer(sender, priority, str(
                        "У этого игрока нет активных усилителей"))
                else:
                    i[5] = 1
                    Answer(sender, priority, str(
                        "Теперь этот игрок получает стандартное число квинов за задания"))
                    Answer(i[0], 0, str(
                        "Теперь вы получаете стандартное число квинов за задания"))
                    updatelist()
                    logaddcommand(sender, ' '.join(command))
        if (d):
            Answer(sender, priority, str(
                "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))
    elif (len(command) != 4):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: kvinboost [Ник] [Множитель] [Сек.]"))
    elif (not command[2].isdigit()) and (not command[3].isdigit()):
        Answer(sender, priority, str(
            "Неверный формат команды. Правильный формат: kvinboost [Ник] [Множитель] [Сек.]"))
    else:
        d = True
        for i in list_of_users:
            if i[0].lower() == command[1].lower():
                d = False
                if int(command[2]) <= 1:
                    Answer(sender, priority, str(
                        "Введен недопустимый множитель"))
                elif int(command[3]) <= 0:
                    Answer(sender, priority, str(
                        "Введено недопустимое число секунд"))
                else:
                    i[5] = int(command[2])
                    i[6] = getdate() + datetime.timedelta(seconds=int(command[3]))
                    Answer(sender, priority, str(
                        "Теперь этот игрок получает {0}X квинов за выполнение заданий до {1}".format(command[2], datetime.datetime.strftime(i[6], '%Y-%m-%d %H:%M'))))
                    print(i)
                    Answer(i[0], 0, str("Теперь вы получаете {0}X квинов за выполнение заданий до {1}".format(
                        command[2], datetime.datetime.strftime(i[6], '%Y-%m-%d %H:%M'))))
                    updatelist()
                    logaddcommand(sender, ' '.join(command))
        if (d):
            Answer(sender, priority, str(
                "Данного игрока нет в клане. Если это ошибка, подождите или используйте update"))


def ComReact(sender, command, priority, user):
    if (command[0].lower() == "bal"):
        bal(sender, command, user, priority)
    elif (command[0].lower() == "help"):
        help(sender, command, priority)
    elif (command[0].lower() == "baltop"):
        baltop(sender, command, priority)
    elif (command[0].lower() == "ping"):
        ping(sender, command, priority)
    elif (command[0].lower() == "info"):
        info(sender, command, priority)
    elif (command[0].lower() == "pay"):
        if (settings[4] == 1):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            pay(sender, command, priority, user)
    elif (command[0].lower() == "addbal"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            addbal(sender, command, priority)
    elif (command[0].lower() == "delbal"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            delbal(sender, command, priority)
    elif (command[0].lower() == "update"):
        update(sender, command, priority)
    elif (command[0].lower() == "resetbal"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            resetbal(sender, command, priority)
    elif (command[0].lower() == "chat"):
        chat(sender, command, priority)
    elif (command[0].lower() == "op"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            op(sender, command, priority)
    elif (command[0].lower() == "deop"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            deop(sender, command, priority)
    elif (command[0].lower() == "transfer"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            transfer(sender, command, priority)
    elif (command[0].lower() == "seen"):
        seen(sender, command, priority, user)
    elif (command[0].lower() == "settime"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            settime(sender, command, priority)
    elif (command[0].lower() == "setdaily"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            setdaily(sender, command, priority)
    elif (command[0].lower() == "taskc"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            taskc(sender, command, priority)
    elif (command[0].lower() == "tasku"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            tasku(sender, command, priority)
    elif (command[0].lower() == "stop"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            stop_bot(sender, command, priority)
    elif (command[0].lower() == "restart"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            restart_bot(sender, command, priority)
    elif (command[0].lower() == "start"):
        start_bot(sender, command, priority)
    elif (command[0].lower() == "safemode"):
        safemode(sender, command, priority)
    elif (command[0].lower() == "kvinboost"):
        if (settings[4] == 1) and (priority != 2):
            Answer(sender, priority, str(
                "Данная команда недоступна в безопасном режиме"))
        else:
            kvinboost(sender, command, priority, user)
    else:
        Answer(sender, priority, str(
            "Такой команды нет. Используйте help для получения информации о командах"))


bot_online = False


def CreateBot():
    global bot, bot_online
    bot.end()
    try:
        bot = mineflayer.createBot(
            {'host': 'classic.minecorp.ru', 'port': 25565, 'username': BOT_USERNAME, 'hideErrors': False})

        @On(bot, 'login')
        def Login(this):
            global settings, list_of_users
            bot.chat("/l XEv9ZVxuLNeE4tpD")
            time.sleep(settings[0])
            bot.chat("/clan home")
            time.sleep(settings[0])

        @On(bot, 'messagestr')
        def Stati(this, message, msgp, jsonMsg):
            print(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + "|" + message)
            logaddmessage(message)
            if ((msgp == "chat") or (msgp == "system")) and (('Я]' in message) or ((BOT_USERNAME + "]") in message)) and (message[0] != "<"):
                message = ClearMessage(message)
                command = message[(message.find(" ", message.find("]")) + 1):]
                sender = message[1:message.find(" ")]
                if (not sender[0].isalpha()):
                    sender = sender[1:]
                d = True
                for i in list_of_users:
                    if sender.lower() == i[0].lower():
                        d = False
                        sender = i
                        break
                if (not d):
                    command = command.split()
                    ComReact(sender[0], command, sender[2], sender[-1])
            else:
                if ("У тебя мут" in message):
                    logadderror(message)

        @On(bot, 'death')
        def Respawn(this):
            global bot
            time.sleep(5)
            bot.chat("/clan home")
            time.sleep(settings[0])
            logadderror("Bot died")

        @On(bot, 'error')
        def ErrorGet(this, err):
            global bot_online
            print(str(err))
            logadderror(str(err))
            bot_online = False

        @On(bot, 'kicked')
        def Kicked(this, reason, loggedln):
            global bot, bot_online
            bot.end()
            print(str(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')) + "|" + str(reason))
            logadderror(str(reason))
            bot_online = False
    except BaseException:
        print("Failed to create Bot\n")
        logadderror("Failed to create Bot")
        bot_online = False


def main():
    time.sleep(10)
    while True:
        try:
            bot.chat(
                "=Присоединяйтесь к нам в ВК и Discord, чтобы следить за всеми обновлениями и мероприятиями в клане")
            time.sleep(settings[0])
            bot.chat(
                "=Ссылка на ВК - https://clck.ru/XUxxQ Ссылка на ДС - https://clck.ru/XUxwR")
            time.sleep(settings[0])
            if datetime.datetime.today().weekday() == 4:
                bot.chat(
                    "=Также напоминаем, что завтра проходит КВ, и за его посещение можно получить 5 квинов. Будем ждать :)")
                time.sleep(settings[0])
        except BaseException:
            print("Bot not found\n")
            logadderror("Bot not found")
        for i in range(12):
            updatelist()
            time.sleep(300)


def cons_inp():
    while True:
        text = input("")
        if text[:2] == "v!":
            sender = BOT_USERNAME
            priority = 2
            text = text[2:].split()
            user = -1
            ComReact(sender, text, priority, user)
        else:
            try:
                bot.chat(text)
            except BaseException:
                print("Bot not found\n")
                logadderror("Bot not found")


def bot_control():
    while True:
        global list_of_users, bot_online
        if (not bot_online):
            time.sleep(5)
            bot_online = True
            CreateBot()
        try:
            time1 = time.perf_counter()
            time.sleep(1)
            pl_on = re.compile(
                r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', str(bot.players))
            d = False
            for i in list_of_users:
                if (i[6] <= getdate()):
                    i[5] = 1
                name = str("username: '" + i[0] + "'")
                if name in pl_on:
                    i[4] += int(time.perf_counter() - time1)
                    if (i[4] >= settings[1]):
                        i[4] = 0
                        d = True
                        i[1] += (settings[2] * i[5])
                        logaddcommand(BOT_USERNAME, str("addbal " +
                                                        i[0] + " " + str(settings[2] * i[5])))
                        Answer(i[0], i[2], str(
                            "Вам начислены квины за онлайн в размере: " + str(settings[2] * i[5]) + "₭"))
            if d:
                updatelist()
        except BaseException:
            print("Updating error\n")
            logadderror("Updating error")


main_thread = threading.Thread(target=main)
cons_thread = threading.Thread(target=cons_inp)
timer_thread = threading.Thread(target=bot_control)
main_thread.start()
cons_thread.start()
timer_thread.start()