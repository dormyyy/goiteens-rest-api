from app import ma

class ManagerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'login', 'password')


class StatusesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'color')


class SlotsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'date', 'time', 'manager_id', 'status_id', 'week_day')


class CoursesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class GroupsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'course_id', 'name', 'timetable')


class ResultsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'color')

    
class AppointmentsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'zoho_link', 'slot_id', 'course_id', 'name', 'comments')


class RolesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'login', 'role_id')


class WeekSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date_start', 'date_finish')


class TemplateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'manager_id', 'template')


manager_schema = ManagerSchema()
status_schema = StatusesSchema()
slot_schema = SlotsSchema()
course_schema = CoursesSchema()
group_schema = GroupsSchema()
result_schema = ResultsSchema()
appointment_schema = AppointmentsSchema()
role_schema = RolesSchema()
user_schema = UsersSchema()
week_schema = WeekSchema()
template_schema = TemplateSchema()

managers_schema = ManagerSchema(many=True)
statuses_schema = StatusesSchema(many=True)
slots_schema = SlotsSchema(many=True)
courses_schema = CoursesSchema(many=True)
groups_schema = GroupsSchema(many=True)
results_schema = ResultsSchema(many=True)
appointments_schema = AppointmentsSchema(many=True)
roles_schema = RolesSchema(many=True)
users_schema = UsersSchema(many=True)
weeks_schema = WeekSchema(many=True)
templates_schema = TemplateSchema(many=True)