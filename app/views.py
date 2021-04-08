from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import LaraEnquiry, LaraEnquiryForm, FollowUp, FollowUpForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def is_valid_query_index(name, email, university_or_college):
    return name != '' and name is not None or email != '' and email is not None or university_or_college != '' and\
           university_or_college is not None


def is_valid_query_follow1(date):
    return date != '' and date is not None


@login_required(login_url='login')
def index(request):
    """
    Main View for data
    """
    fields = LaraEnquiry.objects.all()
    count = LaraEnquiry.objects.count()
    name = request.GET.get('q')
    email = request.GET.get('q')
    university_or_college = request.GET.get('q')

    if is_valid_query_index(name, email, university_or_college):
        search_fields = fields.filter(
            Q(name__icontains=name) | Q(email__icontains=email) |
            Q(university_or_college__icontains=university_or_college)  # ~Q means not
        )
        return render(request, 'app/index.html', {'fields': search_fields, 'total_count': count})  # 'follow': follow

    return render(request, 'app/index.html', {'fields': fields, 'total_count': count})


@login_required(login_url='login')
def form_data(request):
    """
    Model FORM / html form where user can enter all the details of a person and store it in database
    """
    form = LaraEnquiryForm()
    """ creating object of Model Form """

    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    if LaraEnquiry.objects.filter(email=email).exists() or LaraEnquiry.objects.filter(mobile=mobile).exists():
        messages.info(request, "Duplication of Email Or Mobile Number!")
        return redirect(request.META['HTTP_REFERER'])
    """ if email or mobile exists """

    ref_1 = request.POST.get('ref1')
    ref_2 = request.POST.get('ref12')
    ref_3 = request.POST.get('ref13')
    ref_4 = request.POST.get('ref2')
    """ These are the fields from info_form.html these fields does not belong to our model form 
        The data stored here in ref_1, ref_2, ref_3 and ref_4 is used to store the same data in database 
    """

    if request.method == 'POST':
        """ When POSTING data """
        form = LaraEnquiryForm(request.POST)
        """ form object """

        if form.is_valid():
            """ if everything is valid """
            form1 = form.save(commit=False)
            """ Returns object that hasn't been saved yet in database
                As we are doing custom processing before saving the object
            """
            if ref_1:
                form1.source = str(ref_1) + " | " + str(ref_2) + " | " + str(ref_3)
                """ If there is data inside reference
                    Then add it to src field
                """
            else:
                form1.source = ref_4
                """
                if there is no data in previous reference
                """

            form1.save()
            """
            save after custom processing
            """

            messages.success(request, 'Record Created')
            """ simple popup message and got to home page """
            return redirect('/')

    """ for the first time go to this page """
    return render(request, 'app/info_form.html', {'form': form})


@login_required(login_url='login')
def update(request, pk):
    """ Update is almost same like form_data
        We use pk here just to get a particular data and then we can customize it
    """

    ref_1 = request.POST.get('ref1')
    ref_2 = request.POST.get('ref12')
    ref_3 = request.POST.get('ref13')

    ref_4 = request.POST.get('ref2')

    f = LaraEnquiry.objects.get(id__iexact=pk)  # attr
    n = str(f.source)  # source name / ref by
    set_source = tuple(n.split())  # tuple of src / ref by ---> actually for ref-by
    data = LaraEnquiry.objects.get(id=pk)
    all_fields = LaraEnquiry.objects.all()
    form = LaraEnquiryForm(instance=data)

    if request.method == 'POST':
        form = LaraEnquiryForm(request.POST, instance=data)
        if form.is_valid():
            form1 = form.save(commit=False)

            if ref_1:
                form1.source = str(ref_1) + " | " + str(ref_2) + " | " + str(ref_3)
            else:
                form1.source = ref_4

            form1.save()
            messages.success(request, "Record Updated")
            return render(request, 'app/index.html', {'fields': all_fields})

    if len(set_source) > 1:
        """ if it is not just from dropdown """
        first = set_source[0]
        sec = set_source[2]
        third = set_source[4]
        return render(request, 'app/update.html', {'form': form, 'first': first, 'sec': sec, 'third': third})
    else:
        """ if from dropdown """
        src = set_source[0]
        return render(request, 'app/update.html', {'form': form, 'src': src})


@login_required(login_url='login')
def delete(request, pk):
    """ Deleting a particular entry"""
    student = LaraEnquiry.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        return HttpResponse("<center>Deleted<br>Close this window and refresh</center>")

    return render(request, 'app/delete.html', {'student': student})


@login_required(login_url='login')
def follow_up_form(request):
    form = FollowUpForm()
    """
    Model FORM an html form where user can select a person
    and fill all other fields and store it in database
    """
    if request.method == 'POST':
        form = FollowUpForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Followup Created")
            return redirect('followupall')
    return render(request, 'app/follow_up_form.html', {'form': form})


@login_required(login_url='login')
def follow_up_all(request):
    """ Get all data from database for followUp's """
    data = FollowUp.objects.all()
    count = FollowUp.objects.count()
    date = request.GET.get('q')
    response = request.GET.get('q2')
    if is_valid_query_follow1(date):
        search_fields = data.filter(
                Q(day_called=date)
                # ~Q means not
            )
        return render(request, 'app/follow_up_all.html', {'all_data': search_fields, 'total_count': count})

    if is_valid_query_follow1(response):
        search_fields = data.filter(
            Q(response__icontains=response)
        )
        return render(request, 'app/follow_up_all.html', {'all_data': search_fields, 'total_count': count})

    return render(request, 'app/follow_up_all.html', {'all_data': data, 'total_count': count})


@login_required(login_url='login')
def follow_up_detail(request, pk):
    """ Get Data from Database as per PK"""
    follow = FollowUp.objects.get(id=pk)
    data = FollowUpForm(instance=follow)
    if request.method == 'POST':
        data = FollowUpForm(request.POST, instance=follow)
        if data.is_valid():
            data.save()
            messages.success(request, "Followup Updated")
            return redirect('followupall')
    return render(request, 'app/followup_detail.html', {'follow': data})


@login_required(login_url='login')
def follow_up_delete(request, pk):
    """ Deleting a particular entry from followup """
    enquiry = FollowUp.objects.get(id=pk)
    if request.method == 'POST':
        enquiry.delete()
        return HttpResponse("<center>Deleted<br>Close this window and refresh</center>")

    return render(request, 'app/delete.html', {'enquiry': enquiry})


def login_form(request):
    """
    User login
    """
    if request.user.is_authenticated:
        return redirect("/")
    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.method == 'POST':
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome Sir!")
            return redirect("/")
        else:
            messages.info(request, 'username or password incorrect')

    return render(request, 'app/login/login.html')


def logout_user(request):
    """ logout user """
    logout(request)
    return redirect('login')
