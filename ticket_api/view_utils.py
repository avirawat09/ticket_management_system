from ticket_api.serializers import EventLogSerializer
import json
from django.core import serializers
from ticket_api.models import CustomUser, Watcher


def insert_to_event_log(issue_id, issues, new_issue):
    
    for key, value in  new_issue.items():
        event_log_json  = {}
        event_log_json["issue_id"] = issue_id
        event_log_json["updated_field"] = key
        event_log_json["previous_value"] = issues.get_key_value(key)
        event_log_json["new_value"] = value
        event_serializer = EventLogSerializer(data = event_log_json)
        if event_serializer.is_valid():
            event_serializer.save()




def json_serialized(obj):
    return json.loads(serializers.serialize('json', list(obj)))
    

def send_notification_to_watchers(updated_issue_data):
    issue_id = updated_issue_data['id']
    watchers = Watcher.objects.filter(issue_id = issue_id).values_list('user_id')
    watchers_list = [watcher[0] for watcher in watchers]
    emails = CustomUser.objects.filter(pk__in=watchers_list).values_list('email')
    email_list = [username[0] for username in emails]
    print(email_list)
    print(updated_issue_data)
    # TODO: we have issue's updated json that we need to send to watchers and we have emails of watchers with us
    # Implement email support to send this data to watchers