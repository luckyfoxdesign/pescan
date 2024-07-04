# import mysql.connector
# import os

# def get_mysql_connection():
#     """
#     Создает и возвращает подключение к базе данных MySQL.
#     :return: объект подключения к базе данных MySQL
#     """
#     return mysql.connector.connect(
#         host=os.getenv('DB_HOST'),
#         user=os.getenv('MARIADB_USER'),
#         password=os.getenv('MARIADB_PASSWORD'),
#         database=os.getenv('MARIADB_DATABASE')
#     )

# def get_column_metadata():
#     """
#     Извлекает метаданные колонок из базы данных.
#     :return: список кортежей с метаданными колонок
#     """
#     connection = get_mysql_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT table_name, column_name, description FROM column_metadata")
#     metadata = cursor.fetchall()
#     cursor.close()
#     # connection.close()

    # return metadata

def static_metadata():
    return [
        ('building_info', 'common_area_MKD', 'Площадь мест общего пользования МКД кв.м'), 
        ('building_info', 'common_area_MKD_with_attics_and_basements', 'Площадь мест общего пользования МКД с чердаками и подвалами кв.м'), 
        ('building_info', 'id', 'Идентификатор записи'), 
        ('building_info', 'invoice_date_id', 'Идентификатор даты выставления счета'), 
        ('building_info', 'total_area', 'Общая площадь помещения кв.м'), 
        ('building_info', 'total_area_with_individual_heating', 'Общая площадь помещений с индивидуальным отоплением кв.м'), 
        ('building_info', 'total_non_residential_area_MKD', 'Общая площадь нежилых помещений МКД кв.м'), 
        ('building_info', 'total_residential_area_MKD_IJHD', 'Общая площадь жилых помещений МКД/ИЖД кв.м'), 
        ('interactions_with_organizations', 'amount_due', 'Сумма к оплате'), 
        ('interactions_with_organizations', 'balance_penalties', 'Баланс на начало периода за пени'), 
        ('interactions_with_organizations', 'balance_services', 'Баланс на начало периода за услуги'), 
        ('interactions_with_organizations', 'billing_period', 'Расчетный период YYYY-MM-01'), 
        ('interactions_with_organizations', 'charged_penalties', 'Начислено за период за пени'), 
        ('interactions_with_organizations', 'charged_services', 'Начислено за период за услуги'), 
        ('interactions_with_organizations', 'id', 'Идентификатор записи'), 
        ('interactions_with_organizations', 'invoice_date_id', 'Идентификатор даты выставления счета'), 
        ('interactions_with_organizations', 'organization_id', 'Идентификатор организации'), 
        ('interactions_with_organizations', 'outgoing_balance_penalties', 'Исходящий баланс за пени'), 
        ('interactions_with_organizations', 'outgoing_balance_services', 'Исходящий баланс за услуги'), 
        ('interactions_with_organizations', 'paid_penalties', 'Оплачено за пени'), 
        ('interactions_with_organizations', 'paid_services', 'Оплачено за услуги'), 
        ('interactions_with_organizations', 'payment_due_date', 'Срок оплаты до YYYY-MM-DD'), 
        ('interactions_with_organizations', 'recalculation_penalties', 'Перерасчет за пени'), 
        ('interactions_with_organizations', 'recalculation_services', 'Перерасчет за услуги'), 
        ('invoice_dates', 'id', 'Идентификатор даты выставления счета'), 
        ('invoice_dates', 'invoice_date', 'Дата выставления счета'), 
        ('meter_readings', 'current_reading', 'Текущие показания'), 
        ('meter_readings', 'id', 'Идентификатор записи'), 
        ('meter_readings', 'invoice_date_id', 'Идентификатор даты выставления счета'), 
        ('meter_readings', 'last_reading', 'Последние показания'), 
        ('meter_readings', 'meter_number', 'Номер прибора учета'), 
        ('meter_readings', 'next_verification_date', 'Дата очередной поверки'), 
        ('meter_readings', 'reading_date', 'Дата показаний'), 
        ('meter_readings', 'service_id', 'Идентификатор услуги'), 
        ('organizations', 'code', 'Код организации'), 
        ('organizations', 'id', 'Идентификатор организации'), 
        ('organizations', 'name', 'Наименование организации'), 
        ('recalculations', 'amount', 'Сумма перерасчета'), 
        ('recalculations', 'id', 'Идентификатор записи'), 
        ('recalculations', 'invoice_date_id', 'Идентификатор даты выставления счета'), 
        ('recalculations', 'organization_id', 'Идентификатор организации'), 
        ('recalculations', 'reason', 'Основание перерасчета'), 
        ('recalculations', 'service_id', 'Идентификатор услуги'), 
        ('reference_information', 'calculation_method', 'Распределение объема'), 
        ('reference_information', 'calculation_method_description', '1 - весь дом, 2 - жилые помещения, 3 - нежилые помещения, 4 - паркинг '), 
        ('reference_information', 'consumption', 'Расход'), 
        ('reference_information', 'current_reading_ODPU', 'Текущие показания ОДПУ'), 
        ('reference_information', 'id', 'Идентификатор записи'), 
        ('reference_information', 'invoice_date_id', 'Идентификатор даты выставления счета'), 
        ('reference_information', 'service_id', 'Идентификатор услуги'), 
        ('reference_information', 'total_volume_of_communal_resources_home', 'Суммарный объем коммунальных ресурсов в помещениях дома'), 
        ('reference_information', 'total_volume_of_communal_resources_soi', 'Суммарный объем коммунальных ресурсов на СОИ'), 
        ('services', 'id', 'Идентификатор услуги'), 
        ('services', 'name', 'Название услуги'), 
        ('services', 'unit', 'Единица измерения'), 
        ('service_charges', 'benefits', 'Льгота'), 
        ('service_charges', 'calculation_method', 'Способ определения обьема услуги'), 
        ('service_charges', 'calculation_method_description', '1 - норматив, 2 - показания ПУ, 3 - средний показатель потребления, 4 - показания общедомового прибора учета (ОДПУ), 5 - общая площадь, 6 - другое '), 
        ('service_charges', 'charged_for_period', 'Начислено за период'), 
        ('service_charges', 'charge_without_benefits', 'Начислено без учета льготы'), 
        ('service_charges', 'charge_with_pk', 'Размер превыш.платы с учетом ПК,руб.'), 
        ('service_charges', 'id', 'Идентификатор записи'), 
        ('service_charges', 'invoice_date_id', 'Идентификатор даты выставления счета'), 
        ('service_charges', 'organization_id', 'Идентификатор организации'), 
        ('service_charges', 'pk_coefficient', 'Размер повыш.коэфф-та (ПК)'), 
        ('service_charges', 'rate_per_unit', 'Тариф руб./ед.изм.'), 
        ('service_charges', 'service_id', 'Идентификатор услуги'), 
        ('service_charges', 'service_volume', 'Объем услуги')
        ]