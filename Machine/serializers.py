# -*- coding: utf-8 -*-
import models as md
from rest_framework import serializers
from django.db import transaction

class TreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = md.Tree
        fields = (
            'tree_id', 'tree_name', 'file_path', 'file_status', 'tree_path', 'png_path', 'status', 'description', 'classify'
        )


class TwoKSerializer(serializers.ModelSerializer):

    class Meta:
        model = md.towK
        fields = (
            'kid', 'dataName', 'clusterNum', 'pngPath', 'description', 'file_path'
        )