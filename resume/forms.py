from django import forms
from .models import Resume, Language, Experience, Award, School, Skill, Reference
from .models import SkillLink, LanguageLink, ExperienceLink, AwardLink, SchoolLink, ReferenceLink


class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        exclude = ('is_complete', 'status',)


class FileResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ('file_resume',)

    def clean(self):
        clean_data = super(FileResumeForm, self).clean()
        file = clean_data['file_resume']
        if file.size > 4 * 1024 * 1024:
            raise forms.ValidationError({'file_resume': 'The file size for your file resume cannot exceed 4MB.'})
        arr = file.name.split('.')
        ext = arr[len(arr)-1]
        if not len(arr) > 1:
            raise forms.ValidationError({'file_resume': 'The file extension is not recognized. (It must be a PDF)'})
        if not ext.lower() == 'pdf':
            raise forms.ValidationError({'file_resume': 'The file must be a PDF.'})


class NewLanguageForm(forms.ModelForm):

    class Meta:
        model = Language
        fields = '__all__'


class EditLanguageForm(forms.ModelForm):

    class Meta:
        model = Language
        fields = ('name', 'level',)


class NewLanguageLinkForm(forms.ModelForm):
    class Meta:
        model = LanguageLink
        fields = '__all__'


class NewExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = '__all__'

    def clean(self):
        clean_data = super(NewExperienceForm, self).clean()
        end = clean_data.get('end')
        curr = clean_data.get('is_current')
        if curr == 'False':
            if not end:
                raise forms.ValidationError({'end': "End date must be specified if this isn't your current position."})
        if end:
            start = clean_data.get('start')
            if end < start:
                raise forms.ValidationError({'start': 'Start date must be before end date.'})


class EditExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ('title', 'start', 'end', 'description', 'company', 'experience_type', 'is_current')

    def clean(self):
        clean_data = super(EditExperienceForm, self).clean()
        end = clean_data.get('end')
        curr = clean_data.get('is_current')
        if curr == 'False':
            if not end:
                raise forms.ValidationError({'end': "End date must be specified if this isn't your current position."})
        if end:
            start = clean_data.get('start')
            if end < start:
                raise forms.ValidationError({'start': 'Start date must be before end date.'})


class NewExperienceLinkForm(forms.ModelForm):

    class Meta:
        model = ExperienceLink
        fields = '__all__'


class NewAwardForm(forms.ModelForm):

    class Meta:
        model = Award
        fields = '__all__'


class EditAwardForm(forms.ModelForm):

    class Meta:
        model = Award
        fields = ('title', 'date', 'description', 'award_type',)


class NewAwardLinkForm(forms.ModelForm):

    class Meta:
        model = AwardLink
        fields = '__all__'


class NewSchoolForm(forms.ModelForm):

    class Meta:
        model = School
        fields = '__all__'

    def clean(self):
        clean_data = super(NewSchoolForm, self).clean()
        end = clean_data.get('end')
        curr = clean_data.get('is_current')
        if curr == 'False':
            if not end:
                raise forms.ValidationError({'end': "End date must be specified if this isn't your current position."})
        if end:
            start = clean_data.get('start')
            if end < start:
                raise forms.ValidationError({'start': 'Start date must be before end date.'})


class EditSchoolForm(forms.ModelForm):

    class Meta:
        model = School
        fields = ('name', 'program', 'level', 'start', 'end', 'is_current',)

    def clean(self):
        clean_data = super(EditSchoolForm, self).clean()
        end = clean_data.get('end')
        curr = clean_data.get('is_current')
        if curr == 'False':
            if not end:
                raise forms.ValidationError({'end': "End date must be specified if this isn't your current position."})
        if end:
            start = clean_data.get('start')
            if end < start:
                raise forms.ValidationError({'start': 'Start date must be before end date.'})


class NewSchoolLinkForm(forms.ModelForm):

    class Meta:
        model = SchoolLink
        fields = '__all__'


class NewSkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = '__all__'


class EditSkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ('name', 'level',)


class NewSkillLinkForm(forms.ModelForm):

    class Meta:
        model = SkillLink
        fields = '__all__'


class NewReferenceForm(forms.ModelForm):

    class Meta:
        model = Reference
        fields = '__all__'


class EditReferenceForm(forms.ModelForm):

    class Meta:
        model = Reference
        exclude = ('student',)


class NewReferenceLinkForm(forms.ModelForm):

    class Meta:
        model = ReferenceLink
        fields = '__all__'



