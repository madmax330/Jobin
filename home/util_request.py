from home.base_classes import BaseContainer


class RequestUtil(BaseContainer):

    def __init__(self):
        super(RequestUtil, self).__init__()
        self._container_name = 'Request Util'

    #
    #
    #       USER REQUESTS
    #
    #

    def get_login_info(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            return {
                'email': email,
                'password': password
            }
        else:
            self.add_error('Email and password cannot be blank.')
            return None

    def get_user_info(self, request):
        email = request.POST.get('email')
        c_email = request.POST.get('confirm_email')
        password = request.POST.get('password')
        c_password = request.POST.get('confirm_password')

        if email and c_email and password and c_password:
            if email == c_email:
                if password == c_password:
                    return {
                        'username': email,
                        'email': email,
                        'password': password
                    }
                else:
                    self.add_error('Passwords do not match.')
                    return None
            else:
                self.add_error('Emails do not match.')
                return None
        else:
            self.add_error('Email and password fields cannot be left blank.')
            return None

    def get_user_change_info(self, request):
        email = request.POST.get('email')
        c_email = request.POST.get('confirm_email')
        password = request.POST.get('password')
        c_password = request.POST.get('confirm_password')
        old_password = request.POST.get('old_password')

        if not old_password:
            self.add_error('Current password not found.')
            return None

        if email and password:
            self.add_error('You cannot change email and password at the same time.')
            return None

        if email:
            if email == c_email:
                return {
                    'email': email,
                    'old_password': old_password,
                    'password': False
                }
            else:
                self.add_error('Emails do not match.')
                return None

        if password:
            if password == c_password:
                return {
                    'password': password,
                    'old_password': old_password,
                    'email': False
                }

        self.add_error('Invalid request.')
        return None

    #
    #
    #       COMPANY REQUESTS
    #
    #

    def get_company_info(self, request):
        name = request.POST.get('company_name')
        address = request.POST.get('company_address')
        city = request.POST.get('company_city')
        state = request.POST.get('company_state')
        zipcode = request.POST.get('company_zipcode')
        country = request.POST.get('company_country')
        phone = request.POST.get('company_phone')
        website = request.POST.get('company_website')
        startup = request.POST.get('company_startup')
        industry = request.POST.get('company_industry')

        info = {
            'name': name,
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'country': country,
            'phone': phone,
            'website': website,
            'is_startup': (True if startup == 'True' else False),
            'industry': industry
        }

        return self.__check_company_info(info)

    def get_suggestion_info(self, request):
        topic = request.POST.get('suggestion_topic')
        suggestion = request.POST.get('suggestion')
        importance = request.POST.get('suggestion_importance')

        if topic and suggestion and importance:
            try:
                temp = int(importance)
                if not(0 < temp < 10):
                    self.add_error('Importance must be between 0 and 10.')
                    return None
            except ValueError:
                self.add_error('Importance must be a numerical value.')
                return None
            return {
                'topic': topic,
                'suggestion': suggestion,
                'importance': int(importance),
            }
        else:
            self.add_error('All fields are required.')
            return None

    def __check_company_info(self, info):
        flag = True
        if not info['name']:
            self.add_error('Company name cannot be empty.')
            flag = False
        if not info['address']:
            self.add_error('Company address cannot be empty.')
            flag = False
        if not info['city']:
            self.add_error('Company city cannot be empty.')
            flag = False
        if not info['state']:
            self.add_error('Company state cannot be empty.')
            flag = False
        if not info['zipcode']:
            self.add_error('Company zipcode cannot be empty.')
            flag = False
        if not info['country']:
            self.add_error('Company country cannot be empty.')
            flag = False

        if flag:
            return info
        else:
            return None

    #
    #
    #       STUDENT REQUESTS
    #
    #

    def get_student_info(self, request):
        first = request.POST.get('student_first_name')
        last = request.POST.get('student_last_name')
        dob = request.POST.get('student_dob')
        address = request.POST.get('student_address')
        city = request.POST.get('student_city')
        state = request.POST.get('student_state')
        zipcode = request.POST.get('student_zipcode')
        country = request.POST.get('student_country')
        program = request.POST.get('student_program')
        major = request.POST.get('student_major')
        graduate = request.POST.get('student_grad')
        phone = request.POST.get('student_phone')
        lin = request.POST.get('student_linked')
        work = request.POST.get('student_work')

        info = {
            'firstname': first,
            'lastname': last,
            'dob': dob,
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'country': country,
            'program': program,
            'major': major,
            'graduate': (True if graduate == 'True' else False),
            'phone': phone,
            'linkedin': lin,
            'work_eligible': (True if work == 'True' else False),
        }

        return self.__check_student_info(info)

    def __check_student_info(self, info):
        flag = True
        if not info['firstname']:
            self.add_error('Student first name cannot be empty.')
            flag = False
        if not info['lastname']:
            self.add_error('Student last name cannot be empty.')
            flag = False
        if not info['dob']:
            self.add_error('Student date of birth cannot be empty.')
            flag = False
        if not info['address']:
            self.add_error('Student address cannot be empty.')
            flag = False
        if not info['city']:
            self.add_error('Student city cannot be empty.')
            flag = False
        if not info['state']:
            self.add_error('Student state cannot be empty.')
            flag = False
        if not info['zipcode']:
            self.add_error('Student zipcode cannot be empty.')
            flag = False
        if not info['country']:
            self.add_error('Student country cannot be empty.')
            flag = False
        if not info['program']:
            self.add_error('Student program cannot be empty.')
            flag = False
        if not info['major']:
            self.add_error('Student major cannot be empty.')
            flag = False

        if flag:
            return info
        else:
            return None

    #
    #
    #       POST REQUESTS
    #
    #

    def get_post_info(self, request):
        title = request.POST.get('post_title')
        wage = request.POST.get('post_wage')
        wage_interval = request.POST.get('post_wage_interval')
        openings = request.POST.get('post_openings')
        start = request.POST.get('post_start')
        end = request.POST.get('post_end')
        deadline = request.POST.get('post_deadline')
        description = request.POST.get('post_description')
        requirements = request.POST.get('post_requirements')
        programs = request.POST.get('post_programs')
        t = request.POST.get('post_type')
        cover = request.POST.get('post_cover')

        info = {
            'title': title,
            'wage': wage,
            'wage_interval': wage_interval,
            'openings': openings,
            'start_date': start,
            'end_date': end,
            'deadline': deadline,
            'description': description,
            'requirements': requirements,
            'programs': programs,
            'type': t,
            'cover_instructions': cover,
        }

        return self.__check_post_info(info)

    def get_student_post_filter(self, request):
        location = request.GET.get('location_filter')
        keyword = request.GET.get('keyword_filter')

        if location or keyword:
            return {
                'location': location,
                'keyword': keyword
            }
        else:
            self.add_error('Filter values are empty.')
            return None

    def get_cover_letter(self, request):
        letter = request.POST.get('cover_letter')

        if letter:
            return letter
        self.add_error('Cover not found.')
        return None

    def get_applications_filter(self, request):
        schools = request.POST.get('filter_schools')
        majors = request.POST.get('filter_majors')
        gpa = request.POST.get('filter_gpa')
        saved = request.POST.get('filter_saved')
        keep = request.POST.get('filter_keep')

        if not(majors or schools or gpa or (saved == 'True')):
            return {}
        else:
            if gpa:
                try:
                    temp = float(gpa)
                    if not(0 < int(temp) < 4):
                        self.add_error('GPA must be a numerical value between 0 and 4.0.')
                        return None
                except ValueError:
                    self.add_error('GPA must be a numerical value between 0 and 4.0.')
                    return None
            return {
                'schools': schools if schools else '',
                'majors': majors if majors else '',
                'gpa': gpa if gpa else '',
                'saved': True if saved == 'True' else False,
                'keep': False if keep == 'False' else True,
            }

    def __check_post_info(self, info):
        flag = True
        if not info['title']:
            self.add_error('Post title cannot be empty.')
            flag = False
        if not info['description']:
            self.add_error('Post description cannot be empty.')
            flag = False
        if not info['requirements']:
            self.add_error('Post requirements cannot be empty.')
            flag = False
        if not info['type']:
            self.add_error('Post type cannot be empty.')
            flag = False

        if flag:
            return info
        else:
            return None

    #
    #
    #       EVENT REQUESTS
    #
    #

    def get_event_info(self, request):
        title = request.POST.get('event_title')
        start = request.POST.get('event_start')
        end = request.POST.get('event_end')
        st = request.POST.get('event_start_time')
        et = request.POST.get('event_end_time')
        web = request.POST.get('event_website')
        address = request.POST.get('event_address')
        city = request.POST.get('event_city')
        state = request.POST.get('event_state')
        zipcode = request.POST.get('event_zipcode')
        country = request.POST.get('event_country')
        description = request.POST.get('event_description')

        info = {
            'title': title,
            'start_date': start,
            'end_date': end,
            'start_time': st,
            'end_time': et,
            'website': web,
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'country': country,
            'description': description,
        }

        return self.__check_event_info(info)

    def __check_event_info(self, info):
        flag = True
        if not info['title']:
            self.add_error('Event title cannot be empty.')
            flag = False
        if not info['start_date']:
            self.add_error('Event start date cannot be empty.')
            flag = False
        if not info['start_time']:
            self.add_error('Event start time cannot be empty.')
            flag = False
        if not info['description']:
            self.add_error('Event description cannot be empty.')
            flag = False

        if flag:
            return info
        else:
            return None

    #
    #
    #       RESUME REQUESTS
    #
    #

    def get_resume_info(self, request):
        name = request.POST.get('resume_name')
        gpa = request.POST.get('resume_gpa')

        if name and gpa:
            return {
                'name': name,
                'gpa': gpa,
            }
        else:
            self.add_error('Resume name and GPA cannot be empty.')
            return None

    def get_school_info(self, request):
        name = request.POST.get('school_name')
        program = request.POST.get('school_program')
        level = request.POST.get('school_level')
        start = request.POST.get('school_start')
        end = request.POST.get('school_end')
        current = request.POST.get('school_current')

        if name and level:
            return {
                'name': name,
                'program': program,
                'level': level,
                'start': start,
                'end': end,
                'is_current': (True if current == 'True' else False),
            }
        else:
            self.add_error('School name and level cannot be empty.')
            return None

    def get_language_info(self, request):
        name = request.POST.get('language_name')
        level = request.POST.get('language_level')

        if name and level:
            return {
                'name': name,
                'level': level,
            }
        else:
            self.add_error('Language name and level cannot be empty.')
            return None

    def get_experience_info(self, request):
        title = request.POST.get('experience_title')
        start = request.POST.get('experience_start')
        end = request.POST.get('experience_end')
        current = request.POST.get('experience_current')
        description = request.POST.get('experience_description')
        company = request.POST.get('experience_company')
        t = request.POST.get('experience_type')

        if title and t and start:
            return {
                'title': title,
                'start': start,
                'end': end,
                'is_current': (True if current == 'True' else False),
                'description': description,
                'company': company,
                'experience_type': t,
            }
        else:
            self.add_error('Experience title, start date and type cannot be empty.')
            return None

    def get_award_info(self, request):
        title = request.POST.get('award_title')
        date = request.POST.get('award_date')
        description = request.POST.get('award_description')
        t = request.POST.get('award_type')

        if title and t:
            return {
                'title': title,
                'date': date,
                'description': description,
                'award_type': t,
            }
        else:
            self.add_error('Award title and type cannot be empty.')
            return None

    def get_skill_info(self, request):
        name = request.POST.get('skill_name')
        level = request.POST.get('skill_level')

        if name and level:
            return {
                'name': name,
                'level': level,
            }
        else:
            self.add_error('Skill name and level cannot be empty.')
            return None

    def get_reference_info(self, request):
        name = request.POST.get('reference_name')
        affiliation = request.POST.get('reference_affiliation')
        email = request.POST.get('reference_email')

        if name and affiliation and email:
            return {
                'name': name,
                'affiliation': affiliation,
                'email': email
            }
        else:
            self.add_error('All reference fields are required.')
            return None


