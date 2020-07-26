from saved_data_processing import data_formatter_DB

formatter_object_connected = data_formatter_DB.Formatter('testUser')


def test_get_projects_details():

    projects = 1
    project_details = formatter_object_connected.get_projects_details(projects)

    assert project_details == 1

    projects = [
        {'project_access': 'private', 'id': 'id1'},
        {'project_access': 'private', 'id': 'id1'}]

    project_details = formatter_object_connected.get_projects_details(projects)

    assert type(project_details['Number of Projects']) == int
    assert type(project_details['Projects Visibility']) == dict


def test_get_subjects_details():

    subjects = 1
    subject_details = formatter_object_connected.get_subjects_details(subjects)

    assert subject_details == 1

    subjects = [
        {
            'project': 'p1', 'ID': 'sb1', 'age': 50,
            'handedness': 'left', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb2', 'age': 10,
            'handedness': 'left', 'gender': 'F'},
        {
            'project': 'p3', 'ID': 'sb3', 'age': 20,
            'handedness': 'right', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb4', 'age': 50,
            'handedness': 'left', 'gender': 'F'},
        {
            'project': 'p3', 'ID': 'sb5', 'age': 90,
            'handedness': 'left', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb6', 'age': 74,
            'handedness': 'left', 'gender': 'F'}]

    subject_details = formatter_object_connected.get_subjects_details(
        subjects)

    assert type(subject_details['Number of Subjects']) == int
    assert type(subject_details['Age Range']) == dict
    assert type(subject_details['Gender']) == dict
    assert type(subject_details['Handedness']) == dict
    assert type(subject_details['Subjects/Project']) == dict


def test_get_experiments_details():

    experiments = 1
    experiments_details = formatter_object_connected.get_experiments_details(
        experiments)

    assert experiments_details == 1

    experiments = [
        {
            'project': 'p1', 'ID': 'exp1',
            'xsiType': 't1', 'subject_ID': 'sb1'},
        {
            'project': 'p1', 'ID': 'exp2',
            'xsiType': 't1', 'subject_ID': 'sb1'},
        {
            'project': 'p1', 'ID': 'exp3',
            'xsiType': 't3', 'subject_ID': 'sb3'},
        {
            'project': 'p2', 'ID': 'exp4',
            'xsiType': 't2', 'subject_ID': 'sb3'},
        {
            'project': 'p2', 'ID': 'exp5',
            'xsiType': 't1', 'subject_ID': 'sb3'},
        {
            'project': 'p3', 'ID': 'exp6',
            'xsiType': 't2', 'subject_ID': 'sb2'},
        {
            'project': 'p4', 'ID': 'exp7',
            'xsiType': 't1', 'subject_ID': 'sb3'}]

    experiment_details = formatter_object_connected.get_experiments_details(
        experiments)

    assert type(experiment_details['Number of Experiments']) == int
    assert type(experiment_details['Experiments/Subject']) == dict
    assert type(experiment_details['Experiments/Project']) == dict
    assert type(experiment_details['Experiment Types']) == dict


def test_get_scans_details():

    scans = 1
    scans_details = formatter_object_connected.get_scans_details(
        scans)

    assert scans_details == 1

    scans = [
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb1',
            'xnat:imagescandata/id': 'sc1', 'xnat:imagescandata/type': 't1',
            'project': 'p1', 'xsiType': 'tx1',
            'xnat:imagesessiondata/subject_id': 'sb3'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb2',
            'xnat:imagescandata/id': 'sc4', 'xnat:imagescandata/type': 't1',
            'project': 'p1', 'xsiType': 'tx1',
            'xnat:imagesessiondata/subject_id': 'sb1'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb1',
            'xnat:imagescandata/id': 'sc3', 'xnat:imagescandata/type': 't3',
            'project': 'p3', 'xsiType': 'tx2',
            'xnat:imagesessiondata/subject_id': 'sb2'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb2',
            'xnat:imagescandata/id': 'sc2', 'xnat:imagescandata/type': 't3',
            'project': 'p4', 'xsiType': 'tx2',
            'xnat:imagesessiondata/subject_id': 'sb1'}]

    scans_details = formatter_object_connected.get_scans_details(
        scans)

    assert type(scans_details['Number of Scans']) == int
    assert type(scans_details['Scans/Subject']) == dict
    assert type(scans_details['Scans/Project']) == dict
    assert type(scans_details['Scans Quality']) == dict
    assert type(scans_details['Scan Types']) == dict
    assert type(scans_details['XSI Scan Types']) == dict
