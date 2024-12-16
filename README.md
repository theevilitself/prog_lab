##ЛР3
ЛР3 перенесена в отдельный [репозиторий](https://github.com/theevilitself/TynyDB_prog_lab)


## ЛР1

Команда запуска

shell
```
./random_num.py | ./divide.py | ./sqrt.py
```
___

## ЛР2

Примеры работы

__Пример 1__

shell
```
tei@TEI-LINUX:~/prog/2$ ./greeting.py
Hey, what's your name?
Simon
Nice to see you, Simon!
Hey, what's your name?
JOHN
Nice to see you, JOHN!
Hey, what's your name?
^C
Goodbye!
```
__Пример 2__

shell
```
tei@TEI-LINUX:~/prog/2$ ./greeting.py < names.txt 2> err.txt
Nice to see you, Jack!
Nice to see you, Alex!
```

err.txt
``` 
Error: Name 'sonya' needs to start in uppercase!
Error: Name 'Hfiuyi899r9-ujfl' contains invalid characters: 8, 9, 9, 9, -
```
