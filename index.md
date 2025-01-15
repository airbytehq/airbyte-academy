---
layout: default
title: Home
---

# Courses

<ul>
  {% for course in site.courses %}
    {% if course.layout == 'course' %}
      <li>
        <a href="{{ course.url | relative_url }}">{{ course.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
