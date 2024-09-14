import re
import sqlite3
import sys
from datetime import datetime
import requests
from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
new_date = "No"
activeuser = "None"
userr = None

path = "../db/userdata.db"
conn = sqlite3.connect(path)
local = conn.cursor()
local.execute('''
                CREATE TABLE IF NOT EXISTS userdata(
                Username TEXT PRIMARY KEY,
                Password TEXT,
                Email TEXT,
                Date TEXT,
                FromCurrency TEXT,
                ToCurrency TEXT,
                Rate TEXT
                )
                                ''')
conn.close()

class Currency(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = "../ui/allui.ui"
        uic.loadUi(ui_path, self)
        self.setFixedSize(802, 463)
        self.setWindowTitle('Currency Converter')
        self.rates = {}
        self.api_key = "92db9ac3780a4fc59eeb76f1bfa49808"
        self.base_url = "https://openexchangerates.org/api/latest.json"
        self.startup()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetchData)
        self.timer.start(3600000)
        self.fetchData()
        self.after()

    def startup(self):
        if hasattr(self, 'stackedWidget') and hasattr(self, 'main'):
            self.stackedWidget.setCurrentWidget(self.main)
        else:
            print("stackedWidget or Dashboard not found in the UI file")
        self.setupui()
        self.current()
        self.current2()
        self.currencyyyy.setMaxLength(26)
        self.convertcombo.setCurrentIndex(1)
        self.currencycombo.currentTextChanged.connect(self.currenticon)
        self.convertcombo.currentTextChanged.connect(self.currenticon2)
        self.Converted.setEnabled(False)
        self.currencyyyy_2.setEnabled(False)
        self.convert.clicked.connect(self.convertCurrency)
        self.history.clicked.connect(self.datees)
        self.loo.clicked.connect(self.load_items)
        self.history_3.clicked.connect(self.loinscreen)

    def after(self):
        global activeuser
        if activeuser == "None":
            self.loinscreen()
        else:
            self.startup()

    def setupui(self):
        icon = QIcon("../icons/calendar.png")
        self.history.setIcon(icon)
        icon = QIcon("../icons/convert-document (1).png")
        self.history_3.setIcon(icon)
        icon2 = QIcon("../icons/money-transfer-coin-arrow.png")
        self.convert.setIcon(icon2)
        icon3 = QIcon("../icons/circle-user (1).png")
        self.loo.setIcon(icon3)
        self.currencycombo.setStyleSheet("""QComboBox{
                                selection-background-color: rgb(19, 19, 20);
                                background-color: rgb(19, 19, 20);
                                border-radius: 13px;
                                color: rgb(255, 255, 255);
                                padding-left: 48px;
                                font: 87 13pt "Nunito ExtraBold";
                                }
                                QComboBox::drop-down {
                                    subcontrol-origin: padding;
                                    subcontrol-position: top right;
                                    width: 50px;
                                    border-left: 0px solid #8e8e8e;
                                }
                                QComboBox::down-arrow {
                                image: url(../icons/angle-small-down.png);
                                    width: 14px;
                                    height: 14px;
                                }
                                """)
        self.convertcombo.setStyleSheet("""QComboBox{
                                        selection-background-color: rgb(19, 19, 20);
                                        background-color: rgb(19, 19, 20);
                                        border-radius: 13px;
                                        color: rgb(255, 255, 255);
                                        padding-left: 48px;
                                        font: 87 13pt "Nunito ExtraBold";
                                        }
                                        QComboBox::drop-down {
                                            subcontrol-origin: padding;
                                            subcontrol-position: top right;
                                            width: 50px;
                                            border-left: 0px solid #8e8e8e;
                                        }
                                        QComboBox::down-arrow {
                                        image: url(../icons/angle-small-down.png);
                                            width: 14px;
                                            height: 14px;
                                        }
                                        """)

    def current(self):
        currencyselected = self.currencycombo.currentText()
        if currencyselected == "USD":
            self.currentcurrency.setPixmap(
                QtGui.QPixmap("../icons/dollar-sign.png"))
            self.currencyname.setText("American Dollar")
            self.usd()

    def current2(self):
        currencyselected2 = self.convertcombo.currentText()
        if currencyselected2 == "AED":
            self.convertcurrency.setPixmap(
                QtGui.QPixmap("../icons/nigeria.png"))
            self.convertname.setText("Nigerian Naira")

    def currenticon(self):
        currencyselected = self.currencycombo.currentText()
        currencyselected = str(currencyselected)
        if currencyselected == "USD":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/dollar-sign.png"))
            self.currencyname.setText("American Dollar")
            self.usd()
        elif currencyselected == "AED":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/letter-a.png"))
            self.currencyname.setText("Arab Emirates Dirham")
            self.aed()
        elif currencyselected == "NGN":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/nigeria.png"))
            self.currencyname.setText("Nigerian Naira")
            self.ngn()
        elif currencyselected == "ARS":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/argentine.png"))
            self.currencyname.setText("Argentine Peso")
            self.ars()
        elif currencyselected == "AUD":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/australian-dollar.png"))
            self.currencyname.setText("Australian Dollar")
            self.aud()
        elif currencyselected == "BTC":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/bitcoin.png"))
            self.currencyname.setText("Bitcoin")
            self.btc()
        elif currencyselected == "CAD":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/canadian-dollar.png"))
            self.currencyname.setText("Canadian Dollar")
            self.cad()
        elif currencyselected == "EUR":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/euro.png"))
            self.currencyname.setText("Euro")
            self.eur()
        elif currencyselected == "JPY":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/money.png"))
            self.currencyname.setText("Japanese Yen")
            self.jpy()
        elif currencyselected == "GBP":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/pound-sterling.png"))
            self.currencyname.setText("British Pound Sterling")
            self.gbp()
        elif currencyselected == "MXN":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/mexico.png"))
            self.currencyname.setText("Mexican Peso")
            self.mxn()
        elif currencyselected == "DOGE":
            self.currentcurrency.setPixmap(QtGui.QPixmap("../icons/doge.png"))
            self.currencyname.setText("Dogecoin")
            self.doge()
            self.currencyname.setStyleSheet("""padding-left: 10px; border: 0px;
                                                background-color: transparent;
                                                color: rgba(255, 255, 255, 100);
                                                font: 81 6pt "Nunito ExtraBold";""")

    def usd(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def aed(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def ngn(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def ars(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def aud(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "ARS", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def btc(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "ARS", "AUD", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def cad(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def eur(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "JPY", "GBP", "MXN", "DOGE"])

    def jpy(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "GBP", "MXN", "DOGE"])

    def gbp(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "MXN", "DOGE"])

    def mxn(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "DOGE"])

    def doge(self):
        self.convertcombo.clear()
        self.convertcombo.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN"])

    def currenticon2(self):
        currencyselected = self.convertcombo.currentText()
        currencyselected = str(currencyselected)
        if currencyselected == "USD":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/dollar-sign.png"))
            self.convertname.setText("American Dollar")
        elif currencyselected == "AED":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/letter-a.png"))
            self.convertname.setText("Arab Emirates Dirham")
        elif currencyselected == "NGN":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/nigeria.png"))
            self.convertname.setText("Nigerian Naira")
        elif currencyselected == "ARS":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/argentine.png"))
            self.convertname.setText("Argentine Peso")
        elif currencyselected == "AUD":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/australian-dollar.png"))
            self.convertname.setText("Australian Dollar")
        elif currencyselected == "BTC":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/bitcoin.png"))
            self.convertname.setText("Bitcoin")
        elif currencyselected == "CAD":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/canadian-dollar.png"))
            self.convertname.setText("Canadian Dollar")
        elif currencyselected == "EUR":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/euro.png"))
            self.convertname.setText("Euro")
        elif currencyselected == "JPY":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/money.png"))
            self.convertname.setText("Japanese Yen")
        elif currencyselected == "GBP":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/pound-sterling.png"))
            self.convertname.setText("British Pound Sterling")
        elif currencyselected == "MXN":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/mexico.png"))
            self.convertname.setText("Mexican Peso")
        elif currencyselected == "DOGE":
            self.convertcurrency.setPixmap(QtGui.QPixmap("../icons/doge.png"))
            self.convertname.setText("Dogecoin")
            self.convertname.setStyleSheet("""padding-left: 10px; border: 0px;
                                                    background-color: transparent;
                                                    color: rgba(255, 255, 255, 100);
                                                    font: 81 6pt "Nunito ExtraBold";""")

    def fetchData(self):
        url = "https://openexchangerates.org/api/latest.json"
        params = {
            'app_id': '92db9ac3780a4fc59eeb76f1bfa49808'
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            self.rates = data.get('rates', {})
        except requests.RequestException as e:
            self.resultLabel.setText(f"Error fetching data: {e}")
            self.rates = {}


    def convertCurrency(self):
        global userr
        try:
            from_currency = self.currencycombo.currentText()
            to_currency = self.convertcombo.currentText()
            amount = self.currencyyyy.text()
            current_date = datetime.now().date()
            try:
                amount = float(amount)
                if from_currency in self.rates and to_currency in self.rates:
                    base_rate = self.rates[from_currency]
                    target_rate = self.rates[to_currency]
                    converted_amount = amount * (target_rate / base_rate)
                    self.Converted.setPlaceholderText(f"{converted_amount:.2f}")
                    path = "../db/userdata.db"
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS UserHistory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Username TEXT,
                            Date TEXT,
                            FromCurrency TEXT,
                            ToCurrency TEXT,
                            Rate REAL,
                            FOREIGN KEY (Username) REFERENCES userdata(Username)
                        )
                    """)
                    conn.commit()
                    conn.close()
                    items_to_add = [
                        {"Date": current_date.isoformat(), "Converted From": from_currency, "Converted To": to_currency,
                         "Rate": converted_amount}
                    ]
                    seen_items = set()
                    unique_items_to_add = []
                    for item in items_to_add:
                        item_tuple = (item['Date'], item['Converted From'], item['Converted To'], item['Rate'])
                        if item_tuple not in seen_items:
                            unique_items_to_add.append(item)
                            seen_items.add(item_tuple)
                    path44 = "../db/userdata.db"
                    conn = sqlite3.connect(path44)
                    cursor = conn.cursor()
                    for item in unique_items_to_add:
                        cursor.execute("""
                            INSERT INTO UserHistory (Username, Date, FromCurrency, ToCurrency, Rate) 
                            VALUES (?, ?, ?, ?, ?)
                        """, (userr, item['Date'], item['Converted From'], item['Converted To'], item['Rate']))
                    conn.commit()
                    conn.close()
                else:
                    self.Converted.setPlaceholderText("Currency not available")
            except ValueError:
                self.Converted.setPlaceholderText("")
        except Exception as e:
            print(e)

    def load_items(self):
        global userr
        try:
            if hasattr(self, 'stackedWidget') and hasattr(self, 'userinputs'):
                self.stackedWidget.setCurrentWidget(self.userinputs)
            else:
                print("stackedWidget or Dashboard not found in the UI file")
            path = "../db/userdata.db"
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Date, FromCurrency, ToCurrency, Rate 
                FROM UserHistory 
                WHERE Username = ?
            """, (userr,))
            rows = cursor.fetchall()
            conn.close()
            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(4)
            self.table_widget.setHorizontalHeaderLabels(["Date", "From Currency", "To Currency", "Rate"])

            for row_idx, row_data in enumerate(rows):
                self.table_widget.setItem(row_idx, 0, QTableWidgetItem(row_data[0]))
                self.table_widget.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))
                self.table_widget.setItem(row_idx, 2, QTableWidgetItem(row_data[2]))
                self.table_widget.setItem(row_idx, 3, QTableWidgetItem(str(row_data[3])))
                self.table_widget.setColumnWidth(0, 100)
                self.table_widget.setColumnWidth(1, 100)
                self.table_widget.setColumnWidth(2, 100)
                self.table_widget.setColumnWidth(3, 180)
        except Exception as e:
            print(e)
        self.openui()
        self.cancel_3.clicked.connect(self.startup)

    def openui(self):
        icon = QIcon("../icons/cross-small.png")
        self.cancel_3.setIcon(icon)

    def datees(self):
        if hasattr(self, 'stackedWidget') and hasattr(self, 'history_screen'):
            self.stackedWidget.setCurrentWidget(self.history_screen)
        else:
            print("stackedWidget or Dashboard not found in the UI file")
        self.ui()
        self.history_2.clicked.connect(self.startup)
        self.setvalues()
        self.tally.clicked.connect(self.datess)
        self.currenticon3()

    def currenticon3(self):
        currencyselected = self.currencycombo_2.currentText()
        currencyselected = str(currencyselected)
        if currencyselected == "USD":
            self.usd2()
        elif currencyselected == "AED":
            self.aed2()
        elif currencyselected == "NGN":
            self.ngn2()
        elif currencyselected == "ARS":
            self.ars2()
        elif currencyselected == "AUD":
            self.aud2()
        elif currencyselected == "BTC":
            self.btc2()
        elif currencyselected == "CAD":
            self.cad2()
        elif currencyselected == "EUR":
            self.eur2()
        elif currencyselected == "JPY":
            self.jpy2()
        elif currencyselected == "GBP":
            self.gbp2()
        elif currencyselected == "MXN":
            self.mxn2()
        elif currencyselected == "DOGE":
            self.doge2()

    def usd2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def aed2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def ngn2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def ars2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def aud2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "ARS", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def btc2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "ARS", "AUD", "CAD", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def cad2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "EUR", "JPY", "GBP", "MXN", "DOGE"])

    def eur2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "JPY", "GBP", "MXN", "DOGE"])

    def jpy2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "GBP", "MXN", "DOGE"])

    def gbp2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "MXN", "DOGE"])

    def mxn2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "DOGE"])

    def doge2(self):
        self.currencycombo_3.clear()
        self.currencycombo_3.addItems(["USD", "AED", "NGN", "ARS", "AUD", "BTC", "CAD", "EUR", "JPY", "GBP", "MXN"])

    def ui(self):
        icon = QIcon("../icons/cross-small.png")
        self.history_2.setIcon(icon)
        self.yearCombo.setStyleSheet("""QComboBox{
                                            selection-background-color: rgb(19, 19, 20);
                                            background-color: rgb(19, 19, 20);
                                            border-radius: 13px;
                                            color: rgb(255, 255, 255);
                                            padding-left: 15px;
                                            font: 87 13pt "Nunito ExtraBold";
                                            }
                                            QComboBox::drop-down {
                                                subcontrol-origin: padding;
                                                subcontrol-position: top right;
                                                width: 30px;
                                                border-left: 0px solid #8e8e8e;
                                            }
                                        QComboBox::down-arrow {
                                        image: url(../icons/angle-small-down.png);
                                            width: 14px;
                                            height: 14px;
                                        }
                                        """)
        self.monthCombo.setStyleSheet("""QComboBox{
                                            selection-background-color: rgb(19, 19, 20);
                                            background-color: rgb(19, 19, 20);
                                            border-radius: 13px;
                                            color: rgb(255, 255, 255);
                                            padding-left: 15px;
                                            font: 87 13pt "Nunito ExtraBold";
                                            }
                                            QComboBox::drop-down {
                                                subcontrol-origin: padding;
                                                subcontrol-position: top right;
                                                width: 30px;
                                                border-left: 0px solid #8e8e8e;
                                            }
                                        QComboBox::down-arrow {
                                        image: url(../icons/angle-small-down.png);
                                            width: 14px;
                                            height: 14px;
                                        }
                                        """)
        self.currencycombo_2.setStyleSheet("""QComboBox{
                                            selection-background-color: rgb(19, 19, 20);
                                            background-color: rgb(19, 19, 20);
                                            border-radius: 13px;
                                            color: rgb(255, 255, 255);
                                            padding-left: 15px;
                                            font: 87 13pt "Nunito ExtraBold";
                                            }
                                            QComboBox::drop-down {
                                                subcontrol-origin: padding;
                                                subcontrol-position: top right;
                                                width: 30px;
                                                border-left: 0px solid #8e8e8e;
                                            }
                                        QComboBox::down-arrow {
                                        image: url(../icons/angle-small-down.png);
                                            width: 14px;
                                            height: 14px;
                                        }
                                        """)
        self.currencycombo_3.setStyleSheet("""QComboBox{
                                                    selection-background-color: rgb(19, 19, 20);
                                                    background-color: rgb(19, 19, 20);
                                                    border-radius: 13px;
                                                    color: rgb(255, 255, 255);
                                                    padding-left: 15px;
                                                    font: 87 13pt "Nunito ExtraBold";
                                                    }
                                                    QComboBox::drop-down {
                                                        subcontrol-origin: padding;
                                                        subcontrol-position: top right;
                                                        width: 30px;
                                                        border-left: 0px solid #8e8e8e;
                                                    }
                                                QComboBox::down-arrow {
                                                image: url(../icons/angle-small-down.png);
                                                    width: 14px;
                                                    height: 14px;
                                                }
                                                """)

    def setvalues(self):
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        self.monthCombo.addItems(months)
        start_year = 2001
        current_year = 2024
        years = [str(year) for year in range(start_year, current_year + 1)]
        self.yearCombo.addItems(years)

    def get_month_number(self):
        month_name = self.monthCombo.currentText()
        month_map = {
            "January": "01", "February": "02", "March": "03", "April": "04",
            "May": "05", "June": "06", "July": "07", "August": "08",
            "September": "09", "October": "10", "November": "11", "December": "12"
        }
        return month_map.get(month_name, "Invalid Month")

    def fetch_historical_data(self):
        global new_date
        base_currency = self.currencycombo_2.currentText()
        year = self.yearCombo.currentText()
        year = str(year)
        mm = self.monthCombo.currentText()
        mm = self.get_month_number()
        dd = "20"
        newdate = f"{year}-{mm}-{dd}"
        newdate = str(newdate)
        new_date = newdate
        url = f"https://openexchangerates.org/api/historical/{newdate}.json"
        params = {
            'app_id': "92db9ac3780a4fc59eeb76f1bfa49808",
            'base': base_currency
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def datess(self):
        historical_data = self.fetch_historical_data()
        global new_date
        date = new_date
        if not date:
            print("Please enter a date.")
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        if historical_data:
            self.display_data(historical_data)
        else:
            print("No data available.")

    def display_data(self, data):
        year = self.yearCombo.currentText()
        mm = self.monthCombo.currentText()
        specific_currency = self.currencycombo_3.currentText()
        base_currency = data.get('base')
        rates = data.get('rates', {})
        rate = rates.get(specific_currency, None)
        if rate is not None:
            result_text = f" On the 20th of {mm} {year}, {base_currency} was @ {rate} to the {specific_currency}"
            self.currencyyyy_2.setPlaceholderText(result_text)
            return rate
        else:
            self.currencyyyy_2.setPlaceholderText(f"Rate for {specific_currency} not available.")
            return None

    def loinscreen(self):
        global activeuser
        activeuser = "None"
        try:
            if hasattr(self, 'stackedWidget') and hasattr(self, 'login'):
                self.stackedWidget.setCurrentWidget(self.login)
            else:
                print("stackedWidget or Dashboard not found in the UI file")
            self.cancel.clicked.connect(self.startup)
            self.validate.clicked.connect(self.logvalid)
            self.new_2.clicked.connect(self.new__account)
            self.uii()
        except Exception as e:
            print(e)

    def uii(self):
        icon = QIcon("../icons/cross-small.png")
        self.cancel.setIcon(icon)

    def new__account(self):
        if hasattr(self, 'stackedWidget') and hasattr(self, 'new_account'):
            self.stackedWidget.setCurrentWidget(self.new_account)
        else:
            print("stackedWidget or Dashboard not found in the UI file")
        self.loaduii()
        self.newaccount.clicked.connect(self.accountcreate)
        self.cancel_2.clicked.connect(self.loinscreen)

    def loaduii(self):
        icon2 = QIcon("../icons/cross-small.png")
        self.cancel_2.setIcon(icon2)

    def logvalid(self):
        global userr
        user = self.user.text()
        passkey = self.password.text()
        try:
            path = "../db/userdata.db"
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM userdata WHERE Username = ? AND Password = ?", (user, passkey))
            result = cursor.fetchone()
            if result:
                self.yes()
                userr = user
            else:
                self.no()
            conn.close()
        except Exception as e:
            print(e)

    def no(self):
        reset_style = """QLineEdit{
        background-color: rgb(36, 36, 38);
        padding-left: 20px;
        border-radius: 20px;
        color: rgb(255, 255, 255);
        	font: 81 11pt "Nunito ExtraBold";
        }
        QLineEdit:hover{
        border: 0.5px solid rgb(173, 173, 173);}"""
        fields = """border: 0.5px solid red; padding-left: 20px; color: red; font: 75 11pt "Nunito ExtraBold";"""
        error_style = """color: red; border: 0px; font: 75 11pt "Nunito ExtraBold";"""
        reset_error = (""" border: 0px;
                                    font: 75 11pt "Nunito ExtraBold";
                                    color: rgb(179, 179, 179);""")
        self.user.setStyleSheet(fields)
        self.password.setStyleSheet(fields)
        self.label_5.setText("Incorrect username or password")
        self.label_5.setStyleSheet(error_style)
        QTimer.singleShot(2000, lambda: self.label_5.setText("Login"))
        QTimer.singleShot(2000, lambda: self.user.setStyleSheet(reset_style))
        QTimer.singleShot(2000, lambda: self.password.setStyleSheet(reset_style))
        QTimer.singleShot(2000, lambda: self.label_5.setStyleSheet(reset_error))

    def yes(self):
        global activeuser
        activeuser = "Yes"
        self.startup()


    def accountcreate(self):
        try:
            username = self.user_3.text()
            email = self.email.text()
            passkey = self.password_2.text()
            confirm = self.confirm.text()
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            reset_error = (""" border: 0px;
                            font: 75 11pt "Nunito ExtraBold";
                            color: rgb(179, 179, 179);""")
            reset_style = """QLineEdit{
background-color: rgb(36, 36, 38);
padding-left: 20px;
border-radius: 20px;
color: rgb(255, 255, 255);
	font: 81 11pt "Nunito ExtraBold";
}
QLineEdit:hover{
border: 0.5px solid rgb(173, 173, 173);}"""
            fields = """border: 0.5px solid red; padding-left: 20px; color: red; font: 75 11pt "Nunito ExtraBold";"""
            error_style = """color: red; border: 0px; font: 75 11pt "Nunito ExtraBold";"""

            if not username:
                self.user_3.setStyleSheet(fields)
                self.error.setText("Username must not be empty")
                self.error.setStyleSheet(error_style)
                QTimer.singleShot(2000, lambda: self.error.setText("Create a new account"))
                QTimer.singleShot(2000, lambda: self.user_3.setStyleSheet(reset_style))
                QTimer.singleShot(2000, lambda: self.error.setStyleSheet(reset_error))
                return False

            if not email:
                self.email.setStyleSheet(fields)
                self.error.setText("Email must not be empty")
                self.error.setStyleSheet(error_style)
                QTimer.singleShot(2000, lambda: self.error.setText("Create a new account"))
                QTimer.singleShot(2000, lambda: self.email.setStyleSheet(reset_style))
                QTimer.singleShot(2000, lambda: self.error.setStyleSheet(reset_error))
                return False

            if not re.match(email_regex, email):
                self.error.setText("Invalid email format")
                self.email.setStyleSheet(fields)
                self.error.setStyleSheet(error_style)
                QTimer.singleShot(2000, lambda: self.error.setText("Create a new account"))
                QTimer.singleShot(2000, lambda: self.email.setStyleSheet(reset_style))
                QTimer.singleShot(2000, lambda: self.error.setStyleSheet(reset_error))
                return False

            if not passkey or len(passkey) < 6:
                self.password_2.setStyleSheet(fields)
                self.error.setText("Password must be at least 6 characters long")
                self.error.setStyleSheet(error_style)
                QTimer.singleShot(2000, lambda: self.error.setText("Create a new account"))
                QTimer.singleShot(2000, lambda: self.password_2.setStyleSheet(reset_style))
                QTimer.singleShot(2000, lambda: self.error.setStyleSheet(reset_error))
                return False

            if passkey != confirm:
                self.password_2.setStyleSheet(fields)
                self.confirm.setStyleSheet(fields)
                self.error.setText("Password must match")
                self.error.setStyleSheet(error_style)
                QTimer.singleShot(2000, lambda: self.error.setText("Create a new account"))
                QTimer.singleShot(2000, lambda: self.password_2.setStyleSheet(reset_style))
                QTimer.singleShot(2000, lambda: self.confirm.setStyleSheet(reset_style))
                QTimer.singleShot(2000, lambda: self.error.setStyleSheet(reset_error))
                return False
        except Exception as e:
            print(e)
        self.createuser()
        print("Success")

    def createuser(self):
        username = self.user_3.text()
        email = self.email.text()
        passkey = self.password_2.text()
        try:
            path2 = "../db/userdata.db"
            conn = sqlite3.connect(path2)
            local = conn.cursor()
            local.execute('''
                    INSERT INTO userdata (Username, Password, Email)
                    VALUES (?, ?, ?);
                ''', (username, passkey, email))
            self.loinscreen()
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Currency()
    window.show()
    sys.exit(app.exec_())
