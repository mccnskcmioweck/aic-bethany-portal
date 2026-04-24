import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_portal.settings')
django.setup()
from django.contrib.auth.models import User
from members.models import MemberProfile, ServiceRequest, ChurchPosition
from events.models import Event
from sermons.models import Sermon, Announcement
from groups.models import ChurchGroup, GroupMembership
from reports.models import AttendanceReport, SundaySchoolReport, OfferingReport, SpiritualProgramReport
from datetime import date, time, timedelta
from decimal import Decimal

print("Creating positions...")
positions = [
    ('Chairman','leadership',1),('Vice Chairman','leadership',2),('Secretary','leadership',3),
    ('Vice Secretary','leadership',4),('Treasurer','leadership',5),('Vice Treasurer','leadership',6),
    ('Senior Pastor','ministry',7),('Associate Pastor','ministry',8),('Elder','ministry',9),
    ('Deacon','ministry',10),('Deaconess','ministry',11),('Sunday School Superintendent','committee',12),
    ('Choir Director','committee',13),('Youth Leader','committee',14),
    ('Women Fellowship Chairman','committee',15),('Men Fellowship Chairman','committee',16),
    ('Evangelism Coordinator','committee',17),('Welfare Officer','committee',18),('Cell Group Leader','other',19),
]
for name, cat, order in positions:
    ChurchPosition.objects.get_or_create(name=name, defaults={'category':cat,'order':order})
print(f"  {ChurchPosition.objects.count()} positions ready")

print("Creating users...")
def make_user(username, first, last, email, password, is_staff=False):
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, email, password)
        u.first_name=first; u.last_name=last; u.is_staff=is_staff; u.save()
        return u
    return User.objects.get(username=username)

admin = make_user('admin','Church','Admin','admin@aicbethany-kabarnet.co.ke','admin123',True)
rev = make_user('pastor.john','John','Kamau','pastor@aicbethany-kabarnet.co.ke','church123')
mary = make_user('mary.wanjiku','Mary','Wanjiku','mary@aicbethany-kabarnet.co.ke','church123')
peter = make_user('peter.kipng','Peter','Kipng\'etich','peter@aicbethany-kabarnet.co.ke','church123')
victor = make_user('victor.njoroge','Victor','Njoroge','victor@gmail.com','member123')
grace = make_user('grace.achieng','Grace','Achieng','grace@gmail.com','member123')
pending1 = make_user('james.koech','James','Koech','james@gmail.com','member123')
pending2 = make_user('faith.rotich','Faith','Rotich','faith@gmail.com','member123')

MemberProfile.objects.get_or_create(user=admin, defaults={'status':'active','position':ChurchPosition.objects.get(name='Chairman')})
MemberProfile.objects.get_or_create(user=rev, defaults={'status':'active','position':ChurchPosition.objects.get(name='Senior Pastor'),'phone':'+254711111111'})
MemberProfile.objects.get_or_create(user=mary, defaults={'status':'active','position':ChurchPosition.objects.get(name='Deaconess'),'phone':'+254722222222'})
MemberProfile.objects.get_or_create(user=peter, defaults={'status':'active','position':ChurchPosition.objects.get(name='Elder'),'phone':'+254733333333'})
MemberProfile.objects.get_or_create(user=victor, defaults={'status':'active','phone':'+254744444444','approved_by':admin})
MemberProfile.objects.get_or_create(user=grace, defaults={'status':'active','phone':'+254755555555','approved_by':admin})
MemberProfile.objects.get_or_create(user=pending1, defaults={'status':'pending','phone':'+254766666666'})
MemberProfile.objects.get_or_create(user=pending2, defaults={'status':'pending','phone':'+254777777777'})
print("  Users and profiles created")

today = date.today()
print("Creating events...")
events_data = [
    ('Sunday Service','service','Main sanctuary worship',today+timedelta(days=2),time(9,0),'AIC Bethany Main Hall'),
    ('Youth Bible Study','youth','Weekly Bible study for youth',today+timedelta(days=5),time(16,0),'Youth Hall'),
    ("Women's Fellowship",'women','Monthly fellowship and prayer',today+timedelta(days=8),time(10,0),'Fellowship Hall'),
    ('Community Outreach','outreach','Food distribution and prayer',today+timedelta(days=12),time(8,0),'Kabarnet Town'),
]
for title,cat,desc,dt,st,venue in events_data:
    Event.objects.get_or_create(title=title,defaults={'category':cat,'description':desc,'date':dt,'start_time':st,'venue':venue,'is_public':True,'created_by':admin})
print(f"  {Event.objects.count()} events")

print("Creating sermons...")
sermons_data = [
    ('Walking in Faith','Hebrews 11:1-6',today-timedelta(days=7),'A message on true faith.','Faith Series'),
    ('The Power of Prayer','Matthew 6:5-15',today-timedelta(days=14),'Understanding the Lords Prayer.',''),
    ('Love One Another','John 13:34-35',today-timedelta(days=21),'The standard of Christs love.','Love Series'),
]
for title,ref,dt,summary,series in sermons_data:
    Sermon.objects.get_or_create(title=title,defaults={'scripture_reference':ref,'sermon_date':dt,'summary':summary,'preacher':rev,'series':series,'video_url':'https://www.youtube.com/'})

print("Creating announcements...")
Announcement.objects.get_or_create(title='Sunday Service Times',defaults={'content':'First service 7:00 AM | Second service 9:30 AM. All welcome!','priority':'normal','is_active':True,'start_date':today,'end_date':today+timedelta(days=60),'created_by':admin})
Announcement.objects.get_or_create(title='AGM Notice',defaults={'content':'Annual General Meeting – last Sunday of the month after 2nd service. All members must attend.','priority':'high','is_active':True,'start_date':today,'end_date':today+timedelta(days=30),'created_by':admin})

print("Creating groups...")
groups_data = [
    ('Christian Men Fellowship','fellowship','Fellowship for men.',peter,'Every Saturday',time(8,0),'Fellowship Hall'),
    ('Christian Women Fellowship','fellowship','Fellowship for women.',mary,'Every Saturday',time(10,0),'Main Hall'),
    ('Christian Youth Fellowship','fellowship','Youth aged 13–35.',rev,'Every Friday',time(17,0),'Youth Hall'),
    ('Choir','spiritual','AIC Bethany Choir.',rev,'Wednesday & Saturday',time(17,0),'Sanctuary'),
    ('Praise & Worship Team','spiritual','Leads worship services.',rev,'Every Saturday',time(16,0),'Sanctuary'),
    ('Intercessory Prayer Team','spiritual','Dedicated prayer warriors.',peter,'Every Tuesday',time(6,0),'Prayer Room'),
    ('Drama Ministry','spiritual','Gospel through drama.',None,'Monthly',None,'Fellowship Hall'),
    ('Sunday School','ministry','Nurturing children in the Word.',mary,'Every Sunday',time(8,30),'Sunday School Block'),
]
created_groups = {}
for name,gtype,desc,leader,mday,mtime,venue in groups_data:
    g,_ = ChurchGroup.objects.get_or_create(name=name,defaults={'group_type':gtype,'description':desc,'leader':leader,'meeting_day':mday,'meeting_time':mtime,'meeting_venue':venue,'is_active':True})
    created_groups[name]=g
GroupMembership.objects.get_or_create(group=created_groups['Christian Men Fellowship'],member=victor,defaults={'role':'member'})
GroupMembership.objects.get_or_create(group=created_groups['Christian Women Fellowship'],member=grace,defaults={'role':'member'})
GroupMembership.objects.get_or_create(group=created_groups['Choir'],member=victor,defaults={'role':'member'})
print(f"  {ChurchGroup.objects.count()} groups")

print("Creating service requests...")
ServiceRequest.objects.get_or_create(member=victor,request_type='prayer',subject='Prayer for family',defaults={'description':'Requesting prayer for my mother who is unwell.','status':'assigned','assigned_to':rev})
ServiceRequest.objects.get_or_create(member=grace,request_type='counseling',subject='Marriage counseling',defaults={'description':'We would like to schedule a counseling session.','status':'pending'})

print("Creating attendance reports...")
for dt,stype,total,men,women,youth,children,visitors,converts in [
    (today,'sunday_first',180,60,75,30,15,8,2),
    (today,'sunday_second',210,70,90,35,15,12,3),
    (today-timedelta(days=3),'wednesday',95,30,40,20,5,3,0),
    (today-timedelta(days=7),'sunday_first',165,55,70,28,12,6,1),
]:
    AttendanceReport.objects.get_or_create(date=dt,service_type=stype,defaults={'total_attendance':total,'men':men,'women':women,'youth':youth,'children':children,'visitors':visitors,'new_converts':converts,'presiding_minister':rev,'recorded_by':admin})

print("Creating offering reports...")
for dt,stype,gen,thank,bldg,tc,tm in [
    (today,'sunday_first',Decimal('12500'),Decimal('3200'),Decimal('5000'),Decimal('4500'),Decimal('1200')),
    (today,'sunday_second',Decimal('18000'),Decimal('4500'),Decimal('7500'),Decimal('6800'),Decimal('1800')),
    (today-timedelta(days=7),'sunday_first',Decimal('11000'),Decimal('2800'),Decimal('4500'),Decimal('4000'),Decimal('1100')),
]:
    OfferingReport.objects.get_or_create(date=dt,service_type=stype,defaults={'general_offering':gen,'thanksgiving_offering':thank,'building_fund':bldg,'tithes_cash':tc,'tithes_mpesa':tm,'counted_by':'Mary Wanjiku & Peter Kipngetich','verified_by':rev,'recorded_by':admin})

print("Creating Sunday School reports...")
SundaySchoolReport.objects.get_or_create(date=today,defaults={'lesson_topic':'The Armour of God','scripture_text':'Ephesians 6:10-18','teacher':mary,'nursery_class':8,'junior_class':15,'middle_class':18,'senior_class':12,'teachers_present':5,'memory_verse':'Be strong in the Lord','recorded_by':admin})

print("Creating program reports...")
SpiritualProgramReport.objects.get_or_create(program_type='choir',date=today-timedelta(days=2),defaults={'title':'Saturday Choir Rehearsal','leader':rev,'members_present':22,'total_members':28,'activity_summary':'Rehearsed 4 songs for Sunday service.','achievements':'Good progress on 3-part harmony','prayer_items':'Pray for more tenors','upcoming_plans':'Performance at Sunday 2nd service','recorded_by':admin})
SpiritualProgramReport.objects.get_or_create(program_type='praise_worship',date=today-timedelta(days=2),defaults={'title':'Praise & Worship Rehearsal','leader':rev,'members_present':8,'total_members':10,'activity_summary':'Rehearsed worship set for Sunday.','recorded_by':admin})

print("\n✅ All seed data loaded!")
print("\nLogin credentials:")
print("  Admin:   admin / admin123  (full access + Admin Panel)")
print("  Member:  victor.njoroge / member123  (active member)")
print("  Pending: james.koech / member123  (awaiting approval)")
