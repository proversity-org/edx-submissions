import logging
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from submissions.api import SubmissionRequestError, get_submissions

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_oauth.authentication import OAuth2Authentication

log = logging.getLogger(__name__)


@login_required()
def get_submissions_for_student_item(request, course_id, student_id, item_id):
    """Retrieve all submissions associated with the given student item.

    Developer utility for accessing all the submissions associated with a
    student item. The student item is specified by the unique combination of
    course, student, and item.

    Args:
        request (dict): The request.
        course_id (str): The course id for this student item.
        student_id (str): The student id for this student item.
        item_id (str): The item id for this student item.

    Returns:
        HttpResponse: The response object for this request. Renders a simple
            development page with all the submissions related to the specified
            student item.

    """
    student_item_dict = dict(
        course_id=course_id,
        student_id=student_id,
        item_id=item_id,
    )
    context = dict(**student_item_dict)
    try:
        submissions = get_submissions(student_item_dict)
        context["submissions"] = submissions
    except SubmissionRequestError:
        context["error"] = "The specified student item was not found."

    return render_to_response('submissions.html', context)


class StudentSubmissionsDetailView(ViewSet):
    """Retrieve all submissions associated with the given student item.

    Developer utility for accessing all the submissions associated with a
    student item. The student item is specified by the unique combination of
    course, student, and item.

    Args:
        request (dict): The request.
        course_id (str): The course id for this student item.
        student_id (str): The student id for this student item.
        item_id (str): The item id for this student item.

    Returns:
        HttpResponse: The response object for this request. Renders a simple
            development page with all the submissions related to the specified
            student item.

    """

    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, student_id, course_id, item_type, item_id):
        try:
            student_item_dict = dict(
                course_id=course_id,
                student_id=student_id,
                item_id=item_id,
                item_type=item_type
            )

            print "get api submissions"
            print student_item_dict

            submissions = get_submissions(student_item_dict)
            return Response(submissions)
        except SubmissionRequestError:
            return Response(
                {"error": "The specified student item was not found."},
                status=status.HTTP_404_NOT_FOUND
            )



