from django.core.exceptions import ValidationError
from django.db import models
from django import forms
import datetime

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def validate_name(value):
    for i in value:
        if i.isdigit():
            raise ValidationError("Use Letters only")
        elif (i < 'a' or i > 'z') and (i < 'A' or i > 'Z'):
            raise ValidationError("Name should be in alphabets without space")


def validate_mobile(val):
    if len(val) > 10 or len(val) < 10:
        raise ValidationError("10 Digits Required")
    for i in val:
        if i not in digits:
            raise ValidationError("10 Digits Required")


def validate_pass_out_Year(val):
    if len(val) < 4:
        raise ValidationError("4 Digits Required")
    for i in val:
        if i not in digits:
            raise ValidationError("4 Digits Required")
    if int(val) > datetime.datetime.now().year - 1:
        raise ValidationError("Year is not proper")


def validate_latest_education(val):
    validate_name(val)


def validate_branch(val):
    validate_name(val)


def validate_percentages(val):
    float_digits = digits
    float_digits.append('.')
    if float(val) < 32.00:
        raise ValidationError("Not Qualified %age should be at least 32.00")
    if len(val) > 5 or len(val) < 5:
        raise ValidationError("This is a Float/Double Field  example: 72.71")
    for i in val:
        if i not in float_digits:
            raise ValidationError("Incorrect Input")


def validate_university_or_college(value):
    for i in value:
        if i.isdigit():
            raise ValidationError("Use Letters only")


class DateInput(forms.DateInput):
    input_type = 'date'


class LaraEnquiry(models.Model):
    STATE = (
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
        # UT
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Chandigarh', 'Chandigarh'),
        ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Ladakh', 'Ladakh'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Puducherry', 'Puducherry'),
    )

    CHOICE_GENDER = [('M', 'Male'), ('F', 'Female'), ('O', 'Others')]

    name = models.CharField(max_length=100, validators=[validate_name])
    # lastname = models.CharField(max_length=100, validators=[validate_name])
    mobile = models.CharField(max_length=10, validators=[validate_mobile])
    email = models.EmailField()
    pass_out_Year = models.CharField(max_length=4, validators=[validate_pass_out_Year])
    latest_education = models.CharField(max_length=100, validators=[validate_latest_education])
    branch = models.CharField(max_length=100, validators=[validate_branch])
    percentages = models.CharField(max_length=5, validators=[validate_percentages])
    university_or_college = models.CharField(max_length=100, validators=[validate_university_or_college])
    state = models.CharField(max_length=100, choices=STATE)
    source = models.CharField(max_length=100, null=True, default=True)
    date = models.DateField(auto_now_add=True, null=True)
    Gender = models.CharField(max_length=50, choices=CHOICE_GENDER, default='M', null=True)
    appointment_date = models.DateField()

    # id_follow = models.

    def __str__(self):
        return self.name


class LaraEnquiryForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "First Name"}))
    mobile = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Mobile"}))
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Email"}))
    pass_out_Year = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Year of Passout"}))
    latest_education = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Latest Education"}))
    branch = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Branch"}))
    percentages = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Percentages"}))
    university_or_college = forms.CharField(label='',
                                            widget=forms.TextInput(attrs={'placeholder': "University/College"}))

    Gender = forms.ChoiceField(
        label='Gender',
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')],
        initial='M',
        widget=forms.RadioSelect()
    )

    class Meta:
        verbose_name = 'Lara-Enquiry'
        verbose_name_plural = "Lara-Enquiry's"
        model = LaraEnquiry
        exclude = ['date', 'source']
        widgets = {
            'appointment_date': DateInput(),
        }


class FollowUp(models.Model):
    day_called = models.DateField()
    Enquiry_name = models.OneToOneField(LaraEnquiry, on_delete=models.CASCADE, null=False, blank=False)
    response = models.TextField()

    def __str__(self):
        return self.Enquiry_name.name


class FollowUpForm(forms.ModelForm):
    response = forms.CharField(label='',
                               widget=forms.Textarea(attrs={
                                   "placeholder": "Response", 'row': 1, 'cols': 30, 'style': 'height: 4em;'
                               }))

    class Meta:
        model = FollowUp
        fields = ['id', 'day_called', 'Enquiry_name', 'response']
        widgets = {
            'day_called': DateInput(),
        }
