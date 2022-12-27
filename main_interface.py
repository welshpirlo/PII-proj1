import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QDialog
import psycopg2
from psycopg2.extras import DictCursor
import pandas
import model
import mamdani_inference


class Interface(QDialog):
    def __init__(self):
        super(Interface, self).__init__()
        loadUi("main_interface_skeleton.ui", self)
        self.setWindowTitle("Fuzzy Intellectual Interface")
        mamdani_inference.preprocessing(model.input_lvs, model.output_lv)

        self.makeComboBox()
        self.makeComboBox2()

        onlyInt = QIntValidator()
        onlyInt.setRange(0, 201)
        self.dist_line.setValidator(onlyInt)

        onlyInt2 = QIntValidator()
        onlyInt2.setRange(0, 2001)
        self.price_line.setValidator(onlyInt2)

        onlyInt3 = QIntValidator()
        onlyInt3.setRange(0, 21)
        self.time_line.setValidator(onlyInt3)

        onlyInt4 = QIntValidator()
        onlyInt4.setRange(0, 11)
        self.space_line.setValidator(onlyInt4)

        self.comboBox.currentTextChanged.connect(self.getTextFromList)
        self.comboBox_2.currentTextChanged.connect(self.getTextFromList2)

        self.pushButton.clicked.connect(self.makeCalculation)
        self.pushButton_2.clicked.connect(self.closeFunk)

    def closeFunk(self):
        self.dist_line.clear()
        self.price_line.clear()
        self.time_line.clear()
        self.space_line.clear()


    def makeCalculation(self):
        distance = int(self.dist_line.text()) - self.distances()
        price = int(self.price_line.text())
        time = int(self.time_line.text())
        space = int(self.space_line.text())
        crisps = (distance, price, time, space)
        res = mamdani_inference.process(model.input_lvs, model.output_lv, model.rule_base, crisps)
        print(crisps, res, sep='\t')
        self.label_3.setText(str(res[1]).upper() + "\n\nCoef: " + str(res[0]))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)

    def getTextFromList(self, index):
        city = index
        print(city)
        self.ultimateCity = city

    def getTextFromList2(self, index):
        city = index
        print(city)
        self.ultimateCity2 = city

    def makeComboBox(self):
        conn = psycopg2.connect(dbname='shapley', user='postgres',
                                password='qwerty', host='localhost')
        df = pandas.read_sql_query("SELECT * FROM city ", con=conn)
        dfnum = df['name'].tolist()
        number = len(dfnum)
        for i in range (0, number):
            self.comboBox.addItem(str(df.at[i, 'name']))
        conn.close()

    def makeComboBox2(self):
        conn = psycopg2.connect(dbname='shapley', user='postgres',
                                password='qwerty', host='localhost')
        df = pandas.read_sql_query("SELECT * FROM city ", con=conn)
        dfnum = df['name'].tolist()
        number = len(dfnum)
        for i in range(0, number):
            self.comboBox_2.addItem(str(df.at[i, 'name']))
        conn.close()

    def convert_city_to_id(self, tableData):
        if tableData == "Vinnytsya":
            id = 0
        else:
            conn = psycopg2.connect(dbname='shapley', user='postgres',
                                    password='qwerty', host='localhost')
            cursor = conn.cursor(cursor_factory=DictCursor)

            db_data = "SELECT city_dest FROM city INNER JOIN distance" \
                      " ON city.id = distance.city_dest WHERE name='" + tableData + "' LIMIT 1"

            cursor.execute(db_data)
            records = cursor.fetchall()
            id = records[0][0]

            cursor.close()
            conn.close()
        return id

    def distances(self):
        city1 = self.convert_city_to_id(self.ultimateCity)
        city2 = self.convert_city_to_id(self.ultimateCity2)

        conn = psycopg2.connect(dbname='shapley', user='postgres',
                                password='qwerty', host='localhost')
        cursor = conn.cursor(cursor_factory=DictCursor)

        db_data = "SELECT distance FROM distance WHERE (city_origin = '" + str(city1) + "' AND city_dest='" + str(
            city2) + "')" \
                      "OR (city_origin = '" + str(city2) + "' AND city_dest='" + str(city1) + "')"
        cursor.execute(db_data)
        records = cursor.fetchall()
        dist1 = records[0][0]

        return dist1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    reg = Interface()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(reg)
    widget.setFixedHeight(540)
    widget.setFixedWidth(960)
    widget.showNormal()
    sys.exit(app.exec_())