import json
import pandas as pd
from asgiref.sync import sync_to_async
from adrf.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import Cross , Long
from core.api.serializers import ResultSerailizer
from trainer.helper import TrainHandler



class CoreViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    

    @sync_to_async(thread_sensitive=False)
    def get_trained_handler(self, data_cross, data_long):
        train_handler = TrainHandler(data_cross, data_long)
        train_handler.train("xgboost")
        return train_handler
    
    @sync_to_async(thread_sensitive=False)
    def get_cross_queryset(self, offset=None, limit=None):
        return Cross.objects.values_by_col_name(offset=offset, limit=limit)
    
    @sync_to_async(thread_sensitive=False)
    def get_long_queryset(self, offset=None, limit=None):
        return Long.objects.values_by_col_name(offset=offset, limit=limit)
    
    async def rf_result(self, request):
        #! using pagination will raise KeyError, (problem with Training)
        #* if data become big traing it may take time, it is better to create a background task (maybe use celery) 
        #* the down side would be no instance response
        cross_data = await self.get_cross_queryset()
        long_data = await self.get_long_queryset()
        df_cross = pd.DataFrame(cross_data)
        df_long = pd.DataFrame(long_data)
        train_handler = await self.get_trained_handler(df_cross, df_long)
        rf_result = train_handler.get_rf_result()
        return Response(rf_result)

        
    async def y_result(self, request):
        #! using pagination will raise KeyError, (problem with Training)
        #* if data become big traing it may take time, it is better to create a background task (maybe use celery) 
        #* the down side would be no instance response
        cross_data = await self.get_cross_queryset()
        long_data = await self.get_long_queryset()
        df_cross = pd.DataFrame(cross_data)
        df_long = pd.DataFrame(long_data)
        train_handler = await self.get_trained_handler(df_cross, df_long)
        prob_y = train_handler.get_prob_y()
        return Response(prob_y.tolist())
        

    #! I do not like this approach, too complication. (maybe just use pagination on model level then use serializer to combine the data, lazy evaluation)
    async def data(self, request):
        paginator = self.pagination_class()
        
        offset = paginator.get_offset(request)
        try:
            limit = paginator.get_limit(request) // 2
        except Exception:
            limit = paginator.default_limit

        cross_data = await self.get_cross_queryset(offset, limit)
        long_data = await self.get_long_queryset(offset, limit)
        df_cross = pd.DataFrame(cross_data)
        df_long = pd.DataFrame(long_data)

        combined_df = pd.concat([df_cross, df_long], ignore_index=True)

        combined_records = combined_df.to_json(orient='records')

        return Response(json.loads(combined_records))
    
    async def store_result(self, request):
        serializer = ResultSerailizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = await serializer.asave(user_id=request.user.id)
        return Response(json.loads(data), status=201)