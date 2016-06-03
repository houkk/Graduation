# -*- coding: utf-8 -*-
import models as md
import rest_framework_filters as filters

# filter

class TreeFilter(filters.FilterSet):

    tree_name = filters.AllLookupsFilter(name="tree_name", lookup_type='contains')
    file_status = filters.AllLookupsFilter(name="file_status", lookup_type='contains')
    status = filters.AllLookupsFilter(name="status", lookup_type='contains')
    description = filters.AllLookupsFilter(name="description", lookup_type='contains')
    classify = filters.AllLookupsFilter(name="classify", lookup_type='exact')

    class Meta:
        model = md.Tree


class TwoKFilter(filters.FilterSet):

    dataName = filters.AllLookupsFilter(name="dataName", lookup_type='contains')
    clusterNum = filters.AllLookupsFilter(name="clusterNum", lookup_type='exact')
    description = filters.AllLookupsFilter(name="description", lookup_type='contains')

    class Meta:
        model = md.towK