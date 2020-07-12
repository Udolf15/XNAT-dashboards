from saved_data_processing import data_formatter_pp_DB
from pymongo import MongoClient
import json

# Code for fetching data from DB
try:
    with open('utils/db_config.json') as json_file:
        db_json = json.load(json_file)
except OSError:
    print("db_json not found")
    exit(1)

client = MongoClient(db_json['url'])
db = client[db_json['db']]
existing_user = db.users_data.find_one({'username': 'testUser'})

formatter_object_connected = data_formatter_pp_DB.Formatter(
        'testUser', existing_user['info'], 'CENTRAL_OASIS_CS')


def test_get_projects_details():

    project_details = formatter_object_connected.get_projects_details()

    assert type(project_details['Imaging Sessions']) == dict
    assert type(project_details['Total Sessions']) == int
    assert type(project_details['user(s)']) == list
    assert type(project_details['member(s)']) == list
    assert type(project_details['Collaborator(s)']) == list
    assert type(project_details['Owner(s)']) == list
    assert type(project_details['last_accessed(s)']) == list
    assert type(project_details['insert_user(s)']) == str
    assert type(project_details['insert_date']) == str
    assert type(project_details['access']) == str
    assert type(project_details['name']) == str
    assert type(project_details['last_workflow']) == str


def test_get_subjects_details():

    subject_details = formatter_object_connected.get_subjects_details()

    assert type(subject_details['Number of Subjects']) == int
    assert type(subject_details['Age Range']) == dict
    assert type(subject_details['Gender']) == dict
    assert type(subject_details['Handedness']) == dict


def test_get_experiments_details():

    experiment_details = formatter_object_connected.get_experiments_details()

    assert type(experiment_details['Number of Experiments']) == int
    assert type(experiment_details['Experiments/Subject']) == dict
    assert type(experiment_details['Experiment Types']) == dict


def test_get_scans_details():

    experiment_details = formatter_object_connected.get_scans_details()

    assert type(experiment_details['Number of Scans']) == int
    assert type(experiment_details['Scans/Subject']) == dict
    assert type(experiment_details['Scans Quality']) == dict
    assert type(experiment_details['Scan Types']) == dict
    assert type(experiment_details['XSI Scan Types']) == dict
