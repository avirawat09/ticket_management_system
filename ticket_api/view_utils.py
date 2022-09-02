from ticket_api.serializers import EventLogSerializer
import json
from django.core import serializers
def insert_to_event_log(issue_id, issues, new_issue):
    print('issues are below')
    
    for key, value in  new_issue.items():
        event_log_json  = {}
        event_log_json["issue_id"] = issue_id
        event_log_json["updated_field"] = key
        event_log_json["previous_value"] = issues.get_key_value(key)
        event_log_json["new_value"] = value
        print(event_log_json)
        print(new_issue)
        event_serializer = EventLogSerializer(data = event_log_json)
        print(event_serializer)
        if event_serializer.is_valid():
            event_serializer.save()




def json_serialized(obj):
    return json.loads(serializers.serialize('json', list(obj)))
    
