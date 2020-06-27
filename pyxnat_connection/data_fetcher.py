from pyxnat import Interface


class Fetcher:

    SELECTOR = None

    # Initializing the central interface object in the constructor
    def __init__(self, name, password, server):

        SELECTOR = Interface(server=server, user=name, password=password)

        self.SELECTOR = SELECTOR

    def get_projects_details(self):

        try:
            print("Processing............")
            projects = self.SELECTOR.select('xnat:projectData').all().data
        except Exception as e:
            # 500 represent error in url
            if(str(e).find('500') != -1):
                return 500
            # 400 represent error in login details
            elif(str(e).find('401') != -1):
                return 401
            # 1 represent Error in whole url
            else:
                return 1

        # Projects_details is a dictionary which will add details of all
        # projects to the global stats dictionary

        projects_details = {}
        projects_mr_pet_ct = {'mr_count': 0,
                              'ct_count': 0,
                              'pet_count': 0}

        project_acccess = {}

        for item in projects:
            if(item['project_access'] in project_acccess):
                project_acccess[item['project_access']] = \
                    project_acccess[item['project_access']] + 1
            else:
                project_acccess[item['project_access']] = 1

        for project in projects:

            '''
            Looping through each project and create a dictonary that will add
            details like:
            Number of MR, PET and CT present in project to project_details.

            project_details is another dictionary which will have above
            information for each project and will add into the projects_details
            dictionary with the key of project as ID
            '''

            if(project['project_mr_count'] == ''):
                projects_mr_pet_ct['mr_count'] =\
                    projects_mr_pet_ct['mr_count']\
                    + 0
            else:
                projects_mr_pet_ct['mr_count'] =\
                    projects_mr_pet_ct['mr_count']\
                    + int(project['mr_count'])

            if(project['project_pet_count'] == ''):
                projects_mr_pet_ct['pet_count'] =\
                    projects_mr_pet_ct['project_pet_count']\
                    + 0
            else:
                projects_mr_pet_ct['pet_count'] =\
                    projects_mr_pet_ct['pet_count']\
                    + int(project['pet_count'])

            if(project['project_ct_count'] == ''):
                projects_mr_pet_ct['ct_count'] =\
                    projects_mr_pet_ct['ct_count'] \
                    + 0
            else:
                projects_mr_pet_ct['ct_count'] =\
                    projects_mr_pet_ct['ct_count']\
                    + int(project['ct_count'])

        projects_details['Number of Projects'] = len(projects)
        projects_details['Total MR PET CT Sessions'] = projects_mr_pet_ct
        projects_details['Projects Visibility'] = project_acccess

        return projects_details

    def get_subjects_details(self):

        try:
            print("Processing............")

            subjects_data = self.SELECTOR.get('/data/subjects',
                        params= {'columns': 'ID,project,handedness,age,gender'})\
                        .json()['ResultSet']['Result']
        except Exception:
            print("ERROR : Unable to connect to the database")
            return 1

        # Subject_details is a dictionary which will add details of
        # all subjects to the global stats dictionary

        subjects_details = {}

        '''
        Looping through each subject and create a dictonary that will
        add details like Number of left,right and unknown handed subjects,
        gender of each subjects

        project_details is another dictionary which will have above
        information for each project and will add into the projects_details
        dictionary with the key of project as ID

        This also add a dictionary data showing number of
        subjects per project
        '''

        # Subject age information

        age_range = {'10': 0,
                     '20': 0,
                     '30': 0,
                     '40': 0,
                     '50': 0,
                     '60': 0,
                     '70': 0,
                     '80': 0,
                     '90': 0,
                     '100': 0,
                     '100 above': 0}

        for item in subjects_data:

            if(item['age'] == ''):
                continue
            elif(int(item['age']) <= 10):
                age_range['10'] = age_range['10'] + 1
            elif(int(item['age']) <= 20):
                age_range['20'] = age_range['20'] + 1
            elif(int(item['age']) <= 30):
                age_range['30'] = age_range['30'] + 1
            elif(int(item['age']) <= 40):
                age_range['40'] = age_range['40'] + 1
            elif(int(item['age']) <= 50):
                age_range['50'] = age_range['50'] + 1
            elif(int(item['age']) <= 60):
                age_range['60'] = age_range['60'] + 1
            elif(int(item['age']) <= 70):
                age_range['70'] = age_range['70'] + 1
            elif(int(item['age']) <= 80):
                age_range['80'] = age_range['80'] + 1
            elif(int(item['age']) <= 90):
                age_range['90'] = age_range['90'] + 1
            elif(int(item['age']) <= 100):
                age_range['100'] = age_range['100'] + 1
            else:
                age_range['100 above'] = age_range['100 above'] + 1

        # Subject handedness information

        handedness = {'Right': 0, 'Left': 0, 'Ambidextrous': 0}

        for item in subjects_data:

            if(item['handedness'] == ''):
                continue
            if(item['handedness'] == 'right'):
                handedness['Right'] = handedness['Right'] + 1
            elif(item['handedness'] == 'left'):
                handedness['Left'] = handedness['Left'] + 1
            else:
                handedness['Ambidextrous'] = handedness['Ambidextrous'] + 1

        # Subject gender information

        gender = {'Male': 0, 'Female': 0}

        for item in subjects_data:

            if(item['gender'] == ''):
                continue
            if(item['gender'].lower()[:1] == 'm'):
                gender['Male'] = gender['Male'] + 1
            else:
                gender['Female'] = gender['Female'] + 1

        # Subjects per project information

        subjects_per_project = {}

        for item in subjects_data:
            if(item['project'] in subjects_per_project):
                subjects_per_project[item['project']] = \
                    subjects_per_project[item['project']] + 1
            else:
                subjects_per_project[item['project']] = 1

        # Number of subjects information
        subjects_details['Number of Subjects'] = len(subjects_data)

        subjects_details['Subjects/Project'] = subjects_per_project
        subjects_details['Age Range'] = age_range
        subjects_details['Gender'] = gender
        subjects_details['Handedness'] = handedness

        return subjects_details

    def get_experiments_details(self):

        '''
        Using array method to get the experiment information present on XNAT.

        This will add a get_experiment_details key in stats dictionary
        which will have details of number of experiments, experiment per
        project, type of experiment, experiment per subjects.
        '''
        try:
            experiments = self.SELECTOR.array.experiments(
                                            experiment_type='',
                                            columns=['subject_ID']).data
        except Exception:
            return 1

        experiments_details = {}

        experiments_details['Number of Experiments'] = len(experiments)

        # Experiments per project information

        experiments_per_project = {}

        for item in experiments:
            if(item['project'] in experiments_per_project):
                experiments_per_project[item['project']] = \
                    experiments_per_project[item['project']] + 1
            else:
                experiments_per_project[item['project']] = 1

        # Experiments type information

        experiment_type = {}

        for item in experiments:
            if(item['xsiType'] in experiment_type):
                experiment_type[item['xsiType']] = \
                    experiment_type[item['xsiType']] + 1
            else:
                experiment_type[item['xsiType']] = 1

        # Experiments per subject information

        experiments_per_subject = {}

        for item in experiments:
            if(item['subject_ID'] in experiments_per_subject):
                experiments_per_subject[item['subject_ID']] = \
                    experiments_per_subject[item['subject_ID']] + 1
            else:
                experiments_per_subject[item['subject_ID']] = 1

        experiments_details['Experiments/Subject'] = experiments_per_subject
        experiments_details['Experiment Types'] = experiment_type
        experiments_details['Experiments/Project'] = experiments_per_project

        return experiments_details

    def get_scans_details(self):

        '''
        Using array method to get the scans information present on XNAT.

        This will add a get_scans_details key in stats dictionary
        which will have details of number of scans, scans per subject,
        scans per project, scans per experimetn, type of experiment,
        scan quality (usable or unusable), xsi type of scan.
        '''
        try:
            scans = self.SELECTOR.array.scans(
                columns=['xnat:imageScanData/quality',
                         'xnat:imageScanData/type'])
        except Exception:
            return 1

        scan_quality = {'usable_scans': 0,
                        'unusable_scans': 0,
                        'questionable': 0}

        for item in scans:
            if(item['xnat:imagescandata/quality'] == 'usable'):
                scan_quality['usable_scans'] = scan_quality['usable_scans']+1
            elif(item['xnat:imagescandata/quality'] == 'questionable'):
                scan_quality['questionable'] = scan_quality['questionable']+1
            else:
                scan_quality['unusable_scans'] =\
                                    scan_quality['unusable_scans'] + 1

        scans_details = {}

        # Scans type information

        type_dict = {}

        for item in scans:
            if(item['xnat:imagescandata/type'] in type_dict):
                type_dict[item['xnat:imagescandata/type']] =\
                        type_dict[item['xnat:imagescandata/type']] + 1
            else:
                type_dict[item['xnat:imagescandata/type']] = 1

        # Scans xsi type information

        xsi_type_dict = {}

        for item in scans:
            if(item['xsiType'] in xsi_type_dict):
                xsi_type_dict[item['xsiType']] = \
                                    xsi_type_dict[item['xsiType']] + 1
            else:
                xsi_type_dict[item['xsiType']] = 1

        # Scans per project information

        scans_per_project = {}

        for item in scans:
            if(item['project'] in scans_per_project):
                scans_per_project[item['project']] = \
                        scans_per_project[item['project']] + 1
            else:
                scans_per_project[item['project']] = 1

        # Scans per subject information

        scans_per_subject = {}

        for item in scans:
            if(item['xnat:imagesessiondata/subject_id'] in scans_per_subject):
                scans_per_subject[item['xnat:imagesessiondata/subject_id']] = \
                    scans_per_subject[item['xnat:imagesessiondata/subject_id']] + 1
            else:
                scans_per_subject[item['project']] = 1

        scans_details['Scans Quality'] = scan_quality
        scans_details['Scan Types'] = type_dict
        scans_details['XSI Scan Types'] = xsi_type_dict
        scans_details['Scans/Project'] = scans_per_project
        scans_details['Scans/Subject'] = scans_per_subject
        scans_details['Number of Scans'] = len(scans)

        return scans_details

    def get_projects_details_specific(self):

        try:
            print("Processing............")
            projects = self.SELECTOR.select('xnat:projectData').all().data
        except Exception as e:
            # 500 represent error in url
            if(str(e).find('500') != -1):
                return 500
            # 400 represent error in login details
            elif(str(e).find('401') != -1):
                return 401
            # 1 represent Error in whole url
            else:
                return 1

        return [project['id'] for project in projects]
