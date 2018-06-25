from django.db import models

# Added imports
# from django.utils import timezone

class ServiceUnit(models.Model):
    """"Creates and associates with a database relation that store data about a service unit / facility.
    i.e. [Ministry, Organisation, firm, etc.]"""
    # Setting custom Primary key
    unit_id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=30)
    # Defining possible service unit types to form a lookup.
    ministry = 'min'
    organization = 'org'
    firm = 'firm'
    other = 'other'
    unit_choice = (
        ('select','Select Type of service unit'),
    	(ministry, 'Ministry'),
    	(organization,'Organization'),
    	(firm,'Firm'),
    	(other,'Others')
    )
    # Creating a choice of service units
    unit_type = models.CharField(
    	max_length=15,
    	choices=unit_choice,
        default='select',
    )
    unit_description = models.TextField(max_length=1024)
    unit_logo = models.CharField(max_length=500)
    unit_featured_image = models.CharField(max_length=500)
    unit_cover_photo = models.CharField(max_length=500)
    # Defining what to be returned for each instance
    def __str__(self):
        return "%s(%s)", self.unit_name, self.unit_id
    # Enforcing custom table name
    class Meta:
        db_table = "ServiceUnit"
    # End class Meta
# End class ServiceUnit

# Model for service unit branches
class Branch(models.Model):
    """"Creates and associates with a database relation that store data about a branch of an organization"""
    # Setting custom Primary key
    branch_id = models.AutoField(primary_key=True)
    # Setting foreign key
    unit_id = models.ForeignKey(ServiceUnit, on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=30)    
    # Defining possible branch levels to form a lookup.
    branch_level_choice = (
        ('main', 'Main Branch'),
        ('other','Other Branch')
    )
    # Creating a choice of service units Branch levels
    branch_level = models.CharField(
        max_length=15,
        choices=branch_level_choice,
        default='other',
    )
    registration_date = models.DateTimeField()
    # Defining a display string for each instance
    def __str__(self):
        return self.branch_name
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Branch"
    # End class Meta
# End class Branch

# Model for branch location
class Location(models.Model):
    """"Creates and associates with a database relation that store data about a branch location information"""
    # Setting foreign key
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # Location attributes
    district = models.CharField(max_length=15)
    county = models.CharField(max_length=15,null = True,blank = True)
    sub_county = models.CharField(max_length=15,null = True,blank = True)
    parish = models.CharField(max_length=15,null = True,blank = True)
    town = models.CharField(max_length=15)
    zone = models.CharField(max_length=15,null = True,blank = True)
    unique_direction = models.CharField(max_length=15,null = True,blank = True)
    # Defining a display string for each instance
    def __str__(self):
        return "%s - %s", self.district, self.town
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Location"
    # End class Meta
# End class Location

# Model for branch Contact information
class Contact(models.Model):
    """"Creates and associates with a database relation that store data about a branch contacts information"""
    # Setting foreign key
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # Contact attributes
    mobile_number = models.CharField(max_length=15)
    office_number = models.CharField(max_length=15,null = True,blank = True)
    fax_number = models.CharField(max_length=15,null = True,blank = True)
    email_address = models.EmailField(max_length=15,null = True,blank = True)

    # Defining a display string for each instance
    def __str__(self):
        if (self.mobile_number == "") and (self.office_number != ""):
            return self.office_number
        # End if 1
        if (self.mobile_number != "") and (self.office_number == ""):
            return self.mobile_number
        # End if 2
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Contact"
    # End class Meta
# End class Contact

# Model for branch department
class Department(models.Model):
    """"Creates and associates with a database relation that store data about a department."""
    # Department primary key
    department_id = models.CharField(primary_key=True, max_length = 30)
    # Setting foreign key
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # Department attributes
    department_name = models.CharField(max_length=50)
    department_description = models.TextField(max_length=1024)
    # Defining a display string for each instance
    def __str__(self):
        return self.department_name
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Department"
    # End class Meta
# End class Department

# Model for office under department of a branch
class Office(models.Model):
    """"Creates and associates with a database relation that store data about an office"""
    # Office primary key
    office_id = models.CharField(primary_key=True, max_length = 30)
    # Setting foreign key
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    # Department attributes
    office_name = models.CharField(max_length=50)
    office_description = models.TextField(max_length=1024)
    office_working_time_choice  = (
        ('default', 'Standard Working Dime and Days'),
        ('custom', 'Set Custom Working Time for office'),
    )
    office_working_time  = models.CharField(
        max_length=30,
        choices=office_working_time_choice,
        default='default',
    )
    # Defining a display string for each instance
    def __str__(self):
        return self.office_name
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Office"
    # End class Meta
# End class Office

# Model for Custom working time for an office
class WorkingTime(models.Model):
    """"Creates and associates with a database relation that store data about an office working hours"""
    # Setting foreign key
    office_id = models.ForeignKey(Office, on_delete=models.CASCADE)
    # working time attributes
    week_day = models.CharField(max_length=3)
    work_start_time = models.TimeField(default='08:00:00:00')
    work_end_time = models.TimeField(default='17:00:00:00')
    # Defining a display string for each instance
    def __str__(self):
        pass
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "WorkingTime"
    # End class Meta
# End class WorkingTime

# Staff model
class Staff(models.Model):
    """"Creates and associates with a database relation that store data about a staff member"""
    # staff primary key
    staff_id = models.CharField(primary_key=True, max_length=30)
    # Setting foreign key
    office_id = models.ForeignKey(Office, on_delete=models.CASCADE)
    # staff attributes
    staff_first_name = models.CharField(max_length=15)
    staff_last_name = models.CharField(max_length=15)
    staff_profile_photo = models.CharField(max_length=512)
    staff_designation_choices = (
        ('system_admin', 'System administrator'),
        ('Official', 'Official'),
        ('receptionist', 'Receptionist'),
        ('select','Select Staff Designation')
    )
    # Creating choices for staff
    staff_designation = models.CharField(
        max_length=15,
        choices=staff_designation_choices,
        default='select',
    )
    about_staff = models.TextField(max_length=512)
    # Defining a display string for each instance
    def __str__(self):
        return "%s %s (%)", self.staff_first_name, self.staff_last_name, self.staff_id
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Staff"
    # End class Meta
# End class Staff

# user model
class User(models.Model):
    """"Creates and associates with a database relation that store data about a system user"""
    # Setting foreign key
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # User attributes
    user_name = models.CharField(unique=True,max_length=15)
    user_password = models.CharField(max_length=100)
    # Defining a display string for each instance
    def __str__(self):
        return self.user_name
    # Enforcing custom table name
    class Meta:
        db_table = "User"
    # End class Meta
# End class User

# System administrator model
class SystemAdmin(models.Model):
    """"Creates and associates with a database relation that store data about a system administrator"""
    # Setting foreign key
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # User attributes
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    admin_level_choices = (
        ('unit-admin', 'Main System administrator'),
        ('branch-admin', 'Branch system administrator'),
        ('select','Select administrator level')
    )
    # Creating choices for staff
    admin_level = models.CharField(
        max_length=30,
        choices=admin_level_choices,
        default='select',
    )
    # Defining a display string for each instance
    def __str__(self):
        return self.staff_id
    # End function __str__()

    #Enforcing custom table name
    class Meta:
        db_table = "SystemAdmin"
    # End class Meta
# End class SystemAdmin

# Avails model
class Avails(models.Model):
    """"Creates and associates with a database relation that store data about availing process relationship"""
    # Setting foreign key
    availer = models.CharField(max_length = 15)
    availed = models.ForeignKey(Staff, on_delete=models.CASCADE)
    session_start = models.DateTimeField()
    session_stop = models.DateTimeField()
    # Defining a display string for each instance
    def __str__(self):
        return "%s Availed %s", self.availer, self.availed
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Avails"
    # End class Meta
# End class Avails

# Appointment model
class Appointment(models.Model):
    """"Creates and associates with a database relation that store data about official - client appointment"""
    # Appointment primary key
    appointment_id = models.CharField(primary_key=True,max_length = 30)
    # Setting foreign key
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # appointment attributes
    placement_time = models.DateTimeField()
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    reason = models.TextField(max_length=512)
    appointment_mode_choices = (
        ('pend', 'Pending'),
        ('canc', 'Canceled'),
        ('fwd', 'Forwarded'),
        ('conf', 'Confirmed'),
        ('setd', 'Settled'),
        ('non','None')
    )
    # Creating mode choices for appointment
    appointment_mode = models.CharField(
        max_length=15,
        choices=appointment_mode_choices,
        default='non',
    )
    # Defining a display string for each instance
    def __str__(self):
        return self.appointment_id
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Appointment"
    # End class Meta
# End class Appointment

# Client model
class Client(models.Model):
    """"Creates and associates with a database relation that store data about a client from public"""
    # Setting foreign key
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    # client attributes
    client_first_name = models.CharField(max_length=15)
    client_last_name = models.CharField(max_length=15)
    client_contact = models.CharField(max_length=15)
    client_location_district = models.CharField(max_length=15)
    client_location_town = models.CharField(max_length=15)
    # Defining a display string for each instance
    def __str__(self):
        return "%s %s", self.client_first_name, self.client_last_name
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Client"
    # End class Meta
# End class Client

# Model for Custom working time for an office
class Schedule(models.Model):
    """"Creates and associates with a database relation that store data about official monthly schedule"""
    # Setting foreign key
    staff_id = models.ForeignKey(Office, on_delete=models.CASCADE)
    # schedule attributes
    sch_date = models.DateField('Date when Schedule is made',max_length=3)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # If reason is Appointment, default sch_reason is "Appointment.
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    # If any other reason".
    sch_reason = models.TextField(max_length=512)
    # Defining a display string for each instance
    def __str__(self):
        sch = "Scheduled on %s. Schedule duration [from %s to %s]", self.sch_date, self.start_time, self.end_time
        return sch
    # End function __str__()

    # Enforcing custom table name
    class Meta:
        db_table = "Schedule"
    # End class Meta
# End class Schedule
