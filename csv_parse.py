from datetime import datetime

'''
brief:  Общий класс для парсинга csv данных
        Служит для преобразования строк csv файла в модели и наооборот
'''


class ParseCSVFormat(object):
    @classmethod
    def from_row(cls, row):
        return None

    def to_row(self):
        return []


'''
brief:  Модель для Purchases данных
'''


class PurchasesObject(ParseCSVFormat):
    CN_CREATED = 0
    CN_APP_ID = 1
    CN_COUNTRY = 2
    CN_INSTALL_DATE = 3
    CN_REVENUE = 4

    __CN_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    __slots__ = ("created", "mobile_app_id", "country", "install_date", "revenue")

    @classmethod
    def from_row(cls, row):
        return cls(created=row[cls.CN_CREATED],
                   mobile_app_id=row[cls.CN_APP_ID],
                   country=row[cls.CN_COUNTRY],
                   install_date=row[cls.CN_INSTALL_DATE],
                   revenue=row[cls.CN_REVENUE])

    def to_row(self):
        return [self.created, self.mobile_app_id, self.country, self.install_date, self.revenue]

    def __init__(self, created, mobile_app_id, country, install_date, revenue):
        self.created = datetime.strptime(created, self.__CN_DATETIME_FORMAT)
        self.mobile_app_id = int(mobile_app_id)
        self.country = str(country)
        self.install_date = datetime.strptime(install_date, self.__CN_DATETIME_FORMAT)
        self.revenue = float(revenue)

    def __str__(self):
        return "{0}: {1}/{2} {3} {4}$".format(self.mobile_app_id,
                                              self.created,
                                              self.install_date,
                                              self.country,
                                              self.revenue)

    def __repr__(self):
        return str(self)


'''
brief:  Модель для Installs данных
'''


class InstallsObject(ParseCSVFormat):
    __CN_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    CN_CREATED = 0
    CN_APP_ID = 1
    CN_COUNTRY = 2

    __slots__ = ("created", "mobile_app_id", "country")

    @classmethod
    def from_row(cls, row):
        return cls(created=row[cls.CN_CREATED],
                   mobile_app_id=row[cls.CN_APP_ID],
                   country=row[cls.CN_COUNTRY])

    def to_row(self):
        return [self.created, self.mobile_app_id, self.country]

    def __init__(self, created, mobile_app_id, country):
        self.created = datetime.strptime(created, self.__CN_DATETIME_FORMAT)
        self.mobile_app_id = int(mobile_app_id)
        self.country = str(country)

    def __str__(self):
        return "{0}: {1} {2}".format(self.mobile_app_id,
                                     self.created,
                                     self.country)

    def __repr__(self):
        return str(self)


