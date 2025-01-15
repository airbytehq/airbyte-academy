---
layout: default
title: Home
---

# Available Courses

<ul>
  {% for course in site.courses %}
    {% if course.layout == 'course' %}
      <li>
        <a href="{{ course.url | relative_url }}">{{ course.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
