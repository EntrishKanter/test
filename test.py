import sqlite3

connect = sqlite3.connect('data.db')
cursor = connect.cursor()


connect.execute("INSERT INTO 'Тест опрос' VALUES(1, 'Опрос', '[{'text': 'hi', 'callback': '5'}]')")
connect.commit()