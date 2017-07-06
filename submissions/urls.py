from django.conf.urls import patterns, url
from .views import StudentSubmissionsDetailView

urlpatterns = patterns(
    'submissions.views',
    url(
        r'^(?P<student_id>[^/]+)/(?P<course_id>[^/]+)/(?P<item_id>[^/]+)$',
        'get_submissions_for_student_item'
    ),
    url(
        r'^v1/submissions/(?P<student_id>[^/]+)/(?P<course_id>[^/]+)/(?P<item_type>[^/]+)/(?P<item_id>[^/]+)$',
        StudentSubmissionsDetailView.as_view({'get': 'get'}), name="student-submissions-detail"
    ),
)
