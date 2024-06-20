import base64
import calendar
import json
import statistics
import time
from datetime import datetime, timedelta, date
from io import BytesIO
from PIL import ImageDraw, ImageFont, Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Sum, Q, Max, Min, Value
from django.db.models.functions import Cast, Concat
from django.db.models import Max, Avg, Sum, ExpressionWrapper, DateTimeField as QDateTimeField, Value
from rest_framework.response import Response
from datetime import datetime, timezone
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
import textwrap

def file_upload(organization_id, file_data, update=False, file_path=None):
    try:
        file_decode = base64.b64decode(file_data['P40_File_Source'])
        file_name = file_data['P40_File_Name']
        file_format = file_data['P40_File_Format']
        location = f'files/{organization_id}/{file_name}.{file_format}'
        uploaded_path = default_storage.save(location,
                                             ContentFile(file_decode))
        if update:
            try:
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
            except:
                pass
    except:
        uploaded_path = file_path
    return uploaded_path

def get_file_source(file_path):

        with open(file_path, 'rb') as file:
            file_content = base64.b64encode(file.read())
            return file_content
        # return env_settings.BASE_D+file_path.url
