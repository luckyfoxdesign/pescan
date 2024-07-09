from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pdf_parser
import db
import re
import utils
import pdfplumber
import pandas as pd
# import meter_readings
# import reference_information
# import recalculations
import service_charges
import interactions_with_organizations
# import transaction
import json
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/upload": {"origins": "https://pesbit.ru"}})

ALLOWED_EXTENSIONS = {'pdf'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        
        try:
            with pdfplumber.open(file) as pdf:
                array_of_strings = pdf_parser.extract_text_as_paragraphs(pdf)
                personal_number, invoice_date = find_invoice_details(array_of_strings)

                if personal_number:
                    transformed_date = utils.transform_date(invoice_date)
                    if transformed_date is None:
                        return jsonify({"error": "Invalid invoice date format"}), 400

                    try:
                        metadata = db.static_metadata()

                        matched_tables_dfs = pdf_parser.process(pdf, metadata)

                        monthly_data_df = get_sql_calls(matched_tables_dfs, transformed_date, metadata)

                        json_output = generate_json(monthly_data_df)

                    except Exception as e:
                        print(f"EXCEPTION: {e}")
                        return jsonify({"error": str(e)}), 500

                    return jsonify({
                        "data": json.loads(json_output)
                    }), 200
                else:
                    return jsonify({"error": "Not a bill"}), 400
        except Exception as e:
            print(f"EXCEPTION: {e}")
            return jsonify({"error": "Not pdf document"}), 400
    else:
        return jsonify({"error": "File not allowed"}), 400


def generate_json(monthly_data_df):
    # Преобразование числовых столбцов к правильному типу
    monthly_data_df['interactions_with_organizations']['начисленозапериодруб'] = monthly_data_df['interactions_with_organizations']['начисленозапериодруб'].str.replace(',', '.').astype(float)
    monthly_data_df['interactions_with_organizations']['перерасчетруб'] = monthly_data_df['interactions_with_organizations']['перерасчетруб'].str.replace(',', '.').astype(float)
    monthly_data_df['service_charges']['начисленозапериодруб'] = monthly_data_df['service_charges']['начисленозапериодруб'].str.replace(',', '.').astype(float)

    # Объединение двух DataFrame по 'кодорганизации'
    merged_df = monthly_data_df['interactions_with_organizations'].merge(
        monthly_data_df['service_charges'],
        on='кодорганизации',
        how='left',
        suffixes=('_организация', '_услуга')
    )

    # Группировка данных по организациям и пересчет сумм
    organization_sums = merged_df.groupby('кодорганизации').agg({
        'наименованиеорганизации': 'first',
        'расчетныйпериод': 'first',
        'перерасчетруб': 'first',
        'начисленозапериодруб_организация': 'first'
    }).reset_index()

    # Создание списка для конвертации в JSON
    result_list = []
    for org_code in merged_df['кодорганизации'].unique():
        org_data = merged_df[merged_df['кодорганизации'] == org_code]
        services = org_data[['видуслуги', 'начисленозапериодруб_услуга']].drop_duplicates().to_dict('records')
        
        # Переименование ключей для services
        renamed_services = []
        for service in services:
            renamed_service = {
                "service_name": service['видуслуги'],
                "service_charge": round(service['начисленозапериодруб_услуга'], 2) if pd.notnull(service['начисленозапериодруб_услуга']) else None
            }
            renamed_services.append(renamed_service)

        org_info = organization_sums[organization_sums['кодорганизации'] == org_code].iloc[0]
        org_dict = {
            "organization_code": int(org_code),
            "organization_name": org_info['наименованиеорганизации'],
            "organization_charge": round(org_info['начисленозапериодруб_организация'], 2),
            "recalculation": round(org_info['перерасчетруб'], 2),
            "services_list": renamed_services,
            "calculation_period": org_info['расчетныйпериод']
        }

        result_list.append(org_dict)

    # Конвертация в JSON строку
    json_output = json.dumps(result_list, ensure_ascii=False, indent=4)
    return json_output

def get_sql_calls(matched_tables_dfs, transformed_date, metadata):
    
    df_sc = service_charges.process(matched_tables_dfs['service_charges'], metadata, transformed_date)
    df_iwo = interactions_with_organizations.process(matched_tables_dfs['organizations'], transformed_date)

    monthly_data_df = {
        'interactions_with_organizations': df_iwo,
        'service_charges': df_sc
    }

    return monthly_data_df

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_invoice_details(paragraphs):
    number_pattern = r"Лицевой счет для оплаты:\s*(\d+)\s*К оплате"
    date_pattern = r"СЧЕТ на (\d{2}\.\d{2}\.\d{4}) Реквизиты"

    invoice_number = None
    invoice_date = None

    for p in paragraphs:
        if not invoice_number:
            number_match = re.search(number_pattern, p)
            if number_match:
                invoice_number = number_match.group(1)

        if not invoice_date:
            date_match = re.search(date_pattern, p)
            if date_match:
                invoice_date = date_match.group(1)

        if invoice_number and invoice_date:
            break

    return invoice_number, invoice_date

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
