# list_index Filter
```twig
{% for s in data %}
    <tr>
        <th scope="row">{{ s|list_index:0|date:'Y-m-d H:i' }}</th>
        {% for i in sensor_names  %}
        <td{% if not s|list_index:forloop.counter %} class="highlight warning"{% endif %}>{{ s|list_index:forloop.counter|default:'-' }}{% if s|list_index:forloop.counter %}°{{ temp_unit }}{% endif %}</td>
        {% endfor %}
    </tr>
{% endfor %}
```

---

# Assign Tag
```twig
{% assign temp 2 %}
{% assign temp sensor.id %}
```


# Range Tag
```twig
{% range 100 as my_range %}
{% for i in my_range %}
  {{ i }}: Something I want to repeat\n
{% endfor %}
```