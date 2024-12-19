import sqlite3
import random

from flask import Flask, render_template, request
from HTML_Scraping import classes, spells, backgrounds, races

app = Flask(__name__)


def initialization(info):
    sp0 = ["Отсутствует"]
    sp1 = ["Отсутствует"]
    sp2 = ["Отсутствует"]
    sp3 = ["Отсутствует"]
    sp4 = ["Отсутствует"]
    sp5 = ["Отсутствует"]
    sp6 = ["Отсутствует"]
    sp7 = ["Отсутствует"]
    for i in spells:
        if i[1] == '0':
            sp0.append(i[0])
        elif i[1] == '1':
            sp1.append(i[0])
        elif i[1] == '2':
            sp2.append(i[0])
        elif i[1] == '3':
            sp3.append(i[0])
        elif i[1] == '4':
            sp4.append(i[0])
        elif i[1] == '5':
            sp5.append(i[0])
        elif i[1] == '6':
            sp6.append(i[0])
        elif i[1] == '7':
            sp7.append(i[0])
    return render_template('Character_Create.html', classes=classes, races=races, backgrounds=backgrounds, info=info,
                           spells0list=sp0,
                           spells1list=sp1,
                           spells2list=sp2,
                           spells3list=sp3,
                           spells4list=sp4,
                           spells5list=sp5,
                           spells6list=sp6,
                           spells7list=sp7)


@app.route('/', methods=['GET', 'POST'])
def starter():
    info = ["", "", "", "", "", "", 0, 1, 10, 10, 10, 10, 10, 10, 10, "30 футов", "", "", "", ""]
    if request.method == "POST":
        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS characters
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL,
                              charName TEXT  NOT NULL,
                              class TEXT NOT NULL,
                              race TEXT NOT NULL,
                              bg TEXT NOT NULL,
                              wv TEXT NOT NULL,
                              xp INTEGER NOT NULL,
                              level INTEGER NOT NULL,
                              strength INTEGER NOT NULL,
                              dexterity INTEGER NOT NULL,
                              constitution INTEGER NOT NULL,
                              intelligence INTEGER NOT NULL,
                              wisdom INTEGER NOT NULL,
                              charisma INTEGER NOT NULL,
                              armor INTEGER NOT NULL,
                              movement INTEGER NOT NULL, 
                              maxHP INTEGER NOT NULL,
                              currentHP INTEGER NOT NULL,
                              diceHP TEXT NOT NULL)''')
        info = [request.form.get("name"), request.form.get("charName"), request.form.get("class"),
                request.form.get("race"), request.form.get("bg"), request.form.get("wv"),
                request.form.get("xp"), request.form.get("level"), request.form.get("s"),
                request.form.get("d"),
                request.form.get("c"), request.form.get("i"), request.form.get("w"),
                request.form.get("ch"),
                request.form.get("armor"), request.form.get("movement"), request.form.get("maxhp"),
                request.form.get("currenthp"), request.form.get("dicehp")]
        sql = """
                        INSERT INTO characters (
                            name, charName, class, race, bg, wv, xp, level, 
                            strength, dexterity, constitution, intelligence, wisdom, charisma,
                            armor, movement, maxHP, currentHP, diceHP
                        ) VALUES (
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}'
                        )
                    """.format(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8],
                               info[9], info[10], info[11], info[12], info[13], info[14], info[15], info[16],
                               info[17], info[18])
        cursor.execute(sql)
        conn.commit()
        conn.close()
    return initialization(info)


@app.route('/loaded', methods=['GET', 'POST'])
def loader():
    info = ["", "", "", "", "", "", 0, 1, 10, 10, 10, 10, 10, 10, 10, "30 футов", "", "", "", ""]
    if request.method == "POST":
        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM characters WHERE name='{}' AND charName='{}'".format(
            request.form.get("player_login"), request.form.get("character_login"))).fetchone()
        if res:
            for i in range(19):
                info[i] = res[i + 1]
    return initialization(info)


@app.route('/randomed', methods=['GET', 'POST'])
def randomer():
    info = ["", "", "", "", "", "", 0, 1, 10, 10, 10, 10, 10, 10, 10, "30 футов", "", "", "", ""]
    info[2] = random.choice(classes)
    info[3] = random.choice(races)
    info[4] = random.choice(backgrounds)
    info[5] = random.choice(['Законопослушный добрый', 'Законопослушный нейтральный', 'Законопослушный злой',
                             'Нейтральный добрый', 'Нейтральный добрый', 'Нейтральный злой',
                             'Хаотичный добрый', 'Хаотичный нейтральный', 'Хаотичный злой'])
    info[7] = random.randint(1, 20)
    for i in range(6):
        arr = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
        arr.sort()
        info[8 + i] = arr[1] + arr[2] + arr[3]
    info[18] = random.choice(['1d6', '1d8', '1d10', '1d12'])
    x = int(info[18][2:])
    for i in range(info[7]):
        x += random.randint(1, int(info[18][2:]))
    info[16] = x
    info[17] = info[16]
    return initialization(info)


if __name__ == '__main__':
    app.run(debug=True)

