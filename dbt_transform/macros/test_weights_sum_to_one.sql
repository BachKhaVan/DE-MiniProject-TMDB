{% test weights_sum_to_one(model, group_column, weight_column, tolerance=0.000001) %}
    select {{ group_column }}
    from {{ model }}
    group by {{ group_column }}
    having abs(sum({{ weight_column }}) - 1.0) > {{ tolerance }}
{% endtest %}
