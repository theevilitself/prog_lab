from abc import ABC, abstractmethod
import csv
import os


class SingletonMeta(type):
    """ Синглтон метакласс для Database. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """ Класс-синглтон базы данных с таблицами, хранящимися в файлах. """

    def __init__(self):
        self.tables = {}

    def register_table(self, table_name, table):
        self.tables[table_name] = table

    def insert(self, table_name, data):
        table = self.tables.get(table_name)
        if table:
            table.insert(data)
        else:
            raise ValueError(f"Table {table_name} does not exist.")

        def join(self, table1_name, table2_name, join_attr):
            """Объединение двух таблиц по указанному атрибуту."""
            table1 = self.tables[table1_name].data
            table2 = self.tables[table2_name].data

            result = []
            for row1 in table1:
                for row2 in table2:
                    if row1[join_attr] == row2['id']:
                        merged = {**row1, **row2}
                        result.append(merged)
            return result

        def aggregate(self, data, field, agg_func):
            """Агрегатная функция."""
            values = [float(row[field]) for row in data if row[field].isdigit()]
            if agg_func == "AVG":
                return sum(values) / len(values) if values else 0
            elif agg_func == "MAX":
                return max(values) if values else None
            elif agg_func == "MIN":
                return min(values) if values else None
            elif agg_func == "COUNT":
                return len(values)
            else:
                raise ValueError(f"Unknown aggregate function: {agg_func}")

    def select(self, table_name, *args):
        table = self.tables.get(table_name)
        return table.select(*args) if table else None

    def join(self, table1_name, table2_name, join_attr="department_id"):
        table1 = self.tables.get(table1_name)  # employees
        table2 = self.tables.get(table2_name)  # departments
        if not (table1 and table2):
            raise ValueError("One or both tables do not exist.")

        join_result = []
        for row1 in table1.data:
            for row2 in table2.data:
                if row1[join_attr] == row2["id"]:
                    combined_row = {
                        **row1,
                        **{f"department_{key}": value for key, value in row2.items() if key != "id"}
                    }
                    join_result.append(combined_row)

        return join_result


class Table(ABC):
    """ Абстрактный базовый класс для таблиц с вводом/выводом файлов CSV. """

    @abstractmethod
    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split()))
        self.validate_unique(entry, unique_keys=['id'])  # Проверка уникальности по id
        self.data.append(entry)
        self.save()

    @abstractmethod
    def select(self, *args):
        pass


class EmployeeTable(Table):
    """ Таблица сотрудников с методами ввода-вывода из файла CSV. """
    ATTRS = ('id', 'name', 'age', 'salary', 'department_id')
    FILE_PATH = 'employee_table.csv'

    def __init__(self):
        self.data = []
        self.load()

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split()))
        if self.is_unique(entry):
            self.data.append(entry)
            self.save()
        else:
            raise ValueError("Duplicate entry detected.")

    def is_unique(self, entry):
        return not any(
            row['id'] == entry['id'] and row['department_id'] == entry['department_id']
            for row in self.data
        )

    def select(self, start_id, end_id):
        return [entry for entry in self.data if start_id <= int(entry['id']) <= end_id]

    def save(self):
        with open(self.FILE_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
        else:
            self.data = []


class GoodsTable(Table):
    """Таблица товаров с методами ввода-вывода в CSV."""
    ATTRS = ('id', 'name', 'price', 'department_id')
    FILE_PATH = 'goods_table.csv'

    def __init__(self):
        self.data = []
        self.load()

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split()))
        if any(e['id'] == entry['id'] for e in self.data):
            raise ValueError(f"Duplicate entry with id {entry['id']}")
        self.data.append(entry)
        self.save()

    def select(self, **conditions):
        """Фильтрует данные по переданным условиям."""
        return [
            entry for entry in self.data
            if all(entry[k] == str(v) for k, v in conditions.items())
        ]

    def save(self):
        with open(self.FILE_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
        else:
            self.data = []


class DepartmentTable(Table):
    """ Таблица подразделений с методами ввода-вывода из файла CSV. """
    ATTRS = ('id', 'department_name')
    FILE_PATH = 'department_table.csv'

    def __init__(self):
        self.data = []
        self.load()

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split()))
        if self.is_unique(entry):
            self.data.append(entry)
            self.save()
        else:
            raise ValueError("Duplicate entry detected.")

    def is_unique(self, entry):
        return not any(row['id'] == entry['id'] for row in self.data)

    def select(self, department_name):
        return [entry for entry in self.data if entry['department_name'] == department_name]

    def save(self):
        with open(self.FILE_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
        else:
            self.data = []
