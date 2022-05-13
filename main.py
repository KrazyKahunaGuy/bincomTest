from flask import Flask, render_template, request
import mysql.connector

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = mysql.connector.connect(
    host=app.config['DB_HOST'],
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    database=app.config['DB_NAME'],
    port=app.config['DB_PORT']
)

cursor = db.cursor(buffered=True)


@ app.route('/')
def index():
    return render_template('index.html')


@ app.route('/question1')
def question1(polling_unit_current=None):
    polling_unit_id = request.args.get('polling_unit')

    def get_polling_units():
        result = []
        sql = 'SELECT uniqueid FROM polling_unit'
        cursor.execute(sql)
        for row in cursor:
            result.append(row[0])
        return result

    def get_polling_ids(polling_id):
        result = []
        sql = 'SELECT * FROM announced_pu_results WHERE polling_unit_uniqueid = {}'.format(
            polling_id)
        cursor.execute(sql)
        for row in cursor:
            result.append(row[2:4])
        return result
    if polling_unit_id == None:
        return render_template('result_individual_polling_unit.html', polling_units=get_polling_units())

    return render_template('result_individual_polling_unit.html', result=get_polling_ids(polling_unit_id), polling_unit_id=polling_unit_id, polling_units=get_polling_units(), polling_unit_current=polling_unit_current)


@ app.route('/question2')
def question2(lga_name=None):
    lga_id = request.args.get('lga')

    def get_lgas():
        result = []
        sql = 'SELECT * FROM lga'
        cursor.execute(sql)
        for row in cursor:
            result.append(row[1:3])
        return result

    def get_lga_name(lga_id):
        sql = 'SELECT * FROM lga WHERE lga_id = {}'.format(lga_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[2]

    def get_polling_unit_uniqueid_by_lga_id(lga_id):
        result = []
        sql = 'SELECT uniqueid FROM polling_unit WHERE lga_id = {}'.format(
            lga_id)
        cursor.execute(sql)
        for i in cursor:
            result.append(i[0])
        return result

    def get_result_by_polling_unit_uniqueid(polling_unit_uniqueid):
        result = []
        sql = 'SELECT * FROM announced_pu_results WHERE polling_unit_uniqueid = {}'.format(
            polling_unit_uniqueid)
        cursor.execute(sql)
        for i in cursor:
            result.append(i)
        return result

    def get_result_by_lga_id(lga_id):
        result = []
        polling_unit_uniqueid_list = get_polling_unit_uniqueid_by_lga_id(
            lga_id)
        for polling_unit_uniqueid in polling_unit_uniqueid_list:
            result.append(get_result_by_polling_unit_uniqueid(
                polling_unit_uniqueid))
        return result

    def get_total_score_by_lga_id(lga_id):
        results = []
        result = get_result_by_lga_id(lga_id)
        for i in result:
            for j in i:
                results.append(j[3])
        results = sum(results)
        return results

    if lga_id is None:
        return render_template('result_total_polling_unit_by_lga.html', lgas=get_lgas())
    else:
        return render_template('result_total_polling_unit_by_lga.html', lgas=get_lgas(), result=get_total_score_by_lga_id(lga_id), lga_name=get_lga_name(lga_id))


@ app.route('/question3')
def question3(party_abbreviation=None):
    party_abbreviation = request.args.get('party')

    def get_parties():
        result = []
        sql = 'SELECT partyid FROM party'
        cursor.execute(sql)
        for i in cursor:
            result.append(i[0])
        return result

    def get_polling_unit_uniqueid_by_party_abbreviation(party_abbreviation):
        result = []
        sql = 'SELECT polling_unit_uniqueid FROM announced_pu_results WHERE party_abbreviation = "{}"'.format(
            party_abbreviation[:4])
        cursor.execute(sql)
        for i in cursor:
            result.append(i[0])
        return result

    def get_result_by_polling_unit_uniqueid(polling_unit_uniqueid):
        result = []
        sql = 'SELECT * FROM announced_pu_results WHERE polling_unit_uniqueid = {}'.format(
            polling_unit_uniqueid)
        cursor.execute(sql)
        for i in cursor:
            result.append(i)
        return result

    def get_result_by_party_abbreviation(party_abbreviation):
        result = []
        sql = 'SELECT * FROM announced_pu_results WHERE party_abbreviation = "{}"'.format(
            party_abbreviation)
        cursor.execute(sql)
        for i in cursor:
            result.append((i[1], i[3]))
        return result

    result = get_result_by_party_abbreviation(party_abbreviation)

    if party_abbreviation is None:
        return render_template('result_polling_unit_by_party.html', parties=get_parties())
    return render_template('result_polling_unit_by_party.html', parties=get_parties(), result=result, party_abbreviation=party_abbreviation)
