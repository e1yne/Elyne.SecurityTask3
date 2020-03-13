import configparser
import os
from datetime import datetime, timedelta
import time

timeout = 15
val1 = "/val1/"
val2 = "/val2/"
logpath="/private/var/log/testlog.log"

Files = (os.listdir(val1)) #список файлов из папки val1

# создаём словарь: конфиг:файл из папки val1, который в нем описан, чтобы легче было искать
Dict={}
for file in os.listdir(val2):
    if file != "default.cfg":
        f = open(val2 + file, mode='r')
        a=f.readline().replace("name:","")
        a=a.replace("\n","")
        Dict[a] = file
        f.close()

# функция для вычленения дататайм'а из строки лога и проверки его соответствия диапазону времени N,заданному для сигнатуры N
def Time_in_range(nlogline, x):
    logtime = nlogline[0:15]
    logtime += (" "+ str(datetime.now().year))
    logtime = datetime.strptime(logtime, '%b %d %H:%M:%S %Y')
    signtime = datetime.now()- timedelta(minutes=x)
    if (logtime<=datetime.now()) and (logtime>=signtime):
        return True
    else:
        return False

# проверяем файлы из папки val1 по условиям из задания
print("################### Запуск проверки файлов ###################")
for file in Files:
    print("\n_______________________ Файл %s _______________________" % file)
    with open(val2 + "default.cfg", mode='r') as default:
        flag = False
        for line in default:
            if file in line:#если файл есть в конфиге default.cfg
                flag = True
                delta = datetime.now() - (datetime.utcfromtimestamp(os.path.getmtime(val1 + file)))
                delta = delta.total_seconds() % 60 # сколько минут назад было произведено изменение файла
                if (delta<=timeout):
                    print("[1.01]: Файл %s был обновлён за последние 15 минут" % file)
                else:
                    print("[1.02]: Файл %s не был обновлён за последние 15 минут" % file)
                break
        if not flag:
            try:
                path = val2+Dict[file] # нашли конфиг-файл с именем проверяемого файла
                print("[2.00]: Проверка сигнатур для файла %s, содержащихся в конфиге %s:" % (file,Dict[file]))
                f = open(path)
                a = f.readline()# объявляем переменную и "перескакиваем" через первую строку с названием файла
                for line in f:
                    if 'signature' in line:
                        n = int(a) # время N для сигнатуры N из предыдущей строки
                        if n == 0:
                            n=timeout
                        total=False # флаг для проверки,что line появлялась в файле лога за n последних минут
                        with open(logpath) as log:
                            i=True 
                            for logline in log:
                                if i:
                                    logline=logline[3:] # отбрасываем символы начала документа в первой строке (особенность тестового лог-файла)
                                i=False
                                if Time_in_range(logline, n):
                                    if (line.replace("\n","") in logline): 
                                        if (file in logline):
                                            total=True
                                else: 
                                    break #если время в логах вышло за пределы искомого диапазона, перестаем искать сигнатуру в логе
                            if total:
                                print("[2.01]: Сигнатура %s встречается в логах testlog.log за время %d мин." % (line.replace("\n",""), n))
                            else:
                                print("[2.02]: Сигнатура %s не встречалась в логах testlog.log за %d мин." % (line.replace("\n",""), n))
                    a=line.replace("\n","")
                f.close()
            except KeyError:
                print("[3.00]:Информация о конфигурации файла %s отсутствует" % file)

print("######################### Завершено! #########################")