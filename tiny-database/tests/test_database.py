import pytest
import os
import tempfile
from database.database import Database, EmployeeTable, DepartmentTable



@pytest.fixture
def temp_employee_file():
    """Создаем временный файл для таблицы рабочих."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture
def temp_department_file():
    """Создаем временный файл для таблицы подразделений."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture
def database(temp_employee_file, temp_department_file):
    """Данная фикстура задает БД и определяет таблицы."""
    db = Database()

    employee_table = EmployeeTable()
    employee_table.FILE_PATH = temp_employee_file
    department_table = DepartmentTable()
    department_table.FILE_PATH = temp_department_file

    db.register_table("employees", employee_table)
    db.register_table("departments", department_table)

    return db


def test_insert_employee(database):
    """Тест вставки данных в EmployeeTable."""
    database.insert("employees", "1 Alice 30 70000 101")
    database.insert("employees", "2 Bob 28 60000 102")

    employee_data = database.select("employees", 1, 2)
    assert len(employee_data) == 2
    assert employee_data[0] == {'id': '1', 'name': 'Alice', 'age': '30', 'salary': '70000', 'department_id': '101'}
    assert employee_data[1] == {'id': '2', 'name': 'Bob', 'age': '28', 'salary': '60000', 'department_id': '102'}


def test_unique_index_employee(database):
    """Тест проверки уникальности индексов в EmployeeTable."""
    database.insert("employees", "1 Alice 30 70000 101")

    with pytest.raises(ValueError):
        database.insert("employees", "1 Alice 30 70000 101")  # Дубликат записи


def test_insert_department(database):
    """Тест вставки данных в DepartmentTable."""
    database.insert("departments", "101 HR")
    database.insert("departments", "102 IT")

    department_data = database.select("departments", "HR")
    assert len(department_data) == 1
    assert department_data[0] == {'id': '101', 'department_name': 'HR'}


def test_unique_index_department(database):
    """Тест проверки уникальности индексов в DepartmentTable."""
    database.insert("departments", "101 HR")

    with pytest.raises(ValueError):
        database.insert("departments", "101 HR")  # Дубликат записи


def test_join_employees_departments(database):
    """Тест операции JOIN между EmployeeTable и DepartmentTable."""
    database.insert("employees", "1 Alice 30 70000 101")
    database.insert("employees", "2 Bob 28 60000 102")
    database.insert("departments", "101 HR")
    database.insert("departments", "102 IT")

    join_result = database.join("employees", "departments", join_attr="department_id")

    expected_result = [
        {'id': '1', 'name': 'Alice', 'age': '30', 'salary': '70000', 'department_id': '101', 'department_department_name': 'HR'},
        {'id': '2', 'name': 'Bob', 'age': '28', 'salary': '60000', 'department_id': '102', 'department_department_name': 'IT'}
    ]
    assert join_result == expected_result

