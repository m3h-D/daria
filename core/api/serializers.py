import json
from adrf import serializers
from core.utils import MongoHelper
from core.models import Result
from bson.json_util import default


class ResultSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ["result"]

    async def asave(self, **kwargs):
        collection = MongoHelper().collection("core_result")
        data = self.validated_data
        data.update(kwargs)
        collection.insert_one(data)
        return json.dumps(data, default=default)
