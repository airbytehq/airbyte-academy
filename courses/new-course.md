---
title: How to add New Course to Thinkific using Hackmd

---

# How to add New Course to Thinkific using Hackmd

## Lesson 1

We're going to use Hackmd to write the content.
Why?
* It's easy and we can work collaborative to build the content;
* Have powerful integration with Github (what we need)
* No other reason...

This Hackmd is a meta markdown course explaining what is needed from our team to format the final format to move the course to Thinkific. So, pay attention :warning: !

## You don't need to say Lesson X here

This is your first lesson. 
We're going to use the claat structure to build courses.

The file format structure must follow the rules:
1. `# Use only for the course title it won't be used to parse content`
2. `## Use to separate lessons`
3. `### If you want a head/title inside a lesson`

Questions? No, okey, let's move on.

## Code, oh yeah, code highlight

You can use code but need to specify the code language.
See examples below:

Grey-unhappy-not-highlighted-code
```
import time
time.sleep(1)
```

Drake meme saying yes. 
```python
import time
time.sleep(1)
```

## Notes and Warnings!!! :lemon: 

We can use notes BUT, please pay attention to this.
Github sometimes do things we don't like, one of them is how they implemented notes/warnings/callouts whatosever in their markdown viewer. 

Instead of using common language of 

::: info
This is a cool info
:::

They use:
> [!Note]
> This is how Github want you to right a note in Markdown.

Anyway, we can use it, but need to follow Github convention here. Use the first won't render.

## Images are important

Just `Cmd+C` and `Cmd+V` to paste images from clipboard. Let's use Hackmd storage and cdn to provide images to our course content in Thinkific. Great right? Because I'd hate to manually post-edit a markdown only because of images.

![image](https://hackmd.io/_uploads/HywHum-dJl.png)

## Publishing a Course

The main idea is to create a new hackmd and link to the https://github.com/airbytehq/airbyte-academy repository. 
So every new change you can push directly to Github, you don't need to copy or move anything from Hackmd at all.
Very simple workflow.

I'll record a video explaining step-by-step, but here is main idea.

You're going to edit your course content.. (btw we can use gifs or jifs)
![image](https://i.gifer.com/2GU.gif)

After you finished editing, go to top right corner:
![image](https://hackmd.io/_uploads/S1P7tQWOke.png)

Then click in Push, this will move your content to Github direclty.
![image](https://hackmd.io/_uploads/HyapFXbOyl.png)

The Github repository have a Github Action will read the edited file and break into individuals markdowns to be places in Thinkific.

The main index of our static website is: https://airbytehq.github.io/airbyte-academy/


## Conclusion

I hope enjoyed how we're going to build LMS content, if you don't like or have suggestions let us know.

![image](https://media0.giphy.com/media/xUPOqo6E1XvWXwlCyQ/giphy.gif?cid=6c09b952j2k02y0k2y18fi39eclqq260b3sc2pl62bg1texs&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g)
Ok this is my first Airbyte Course and sync to Github