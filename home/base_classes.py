from .forms import NewMessageForm, NewNotificationForm


class BaseContainer:

    def __init__(self):  # Initialize the base util class
        self.__errors = []
        self._container_name = 'Base Container'
        self._form = None
        self._codes = ['success', 'warning', 'danger']
        self.__form = None

    def get_errors(self):  # return list of errors
        return self.__errors

    def get_form_errors(self):
        return self.__form.errors

    def add_error(self, err):  # add a new error to the list
        msg = '-- ' + self._container_name + ' -- ' + err
        self.__errors.append(msg)

    def add_form_errors(self, form=None):  # add errors from django forms
        if form:
            f = form
        else:
            f = self._form
        for key, value in f.errors.items():
            for x in value:
                msg = key + ': ' + x
                self.add_error(msg)

    def save_form(self, form=None):
        self.__form = (form if form else self._form)

    def get_form(self):
        return self.__form

    def add_error_list(self, l):  # add a list of errors (used to add errors from another container class)
        self.__errors.extend(l)

    def new_message(self, is_student, user, msg, code):
        if not self.__check_code(code):
            return False
        info = {
            'code': self._codes[code],
            'student': (user.id if is_student else None),
            'company': (None if is_student else user.id),
            'message': (msg if msg else 'Invalid Request.'),
        }
        form = NewMessageForm(info)
        if form.is_valid():
            form.save()
            return True
        else:
            self.add_form_errors(form)
            return False

    def new_notification(self, is_student, user, msg, code):
        info = {
            'code': code,
            'student': (user.id if is_student else None),
            'company': (None if is_student else user.id),
            'message': (msg if msg else 'Invalid Request.'),
        }
        form = NewNotificationForm(info)
        if form.is_valid():
            form.save()
            return True
        else:
            self.add_form_errors(form)
            return False

    def __check_code(self, code):
        if 2 >= code >= 0:
            return True
        else:
            self.add_error('Invalid message code.')
            return False




