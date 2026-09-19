# Writing on GitHub II

https://justiceconder.medium.com/writing-on-github-ii-db7c157f21da

2020-08-26

![Image 3](https://miro.medium.com/v2/resize:fit:700/1*Q3AZnYp1Qrdqu34AUnJwuQ.png)

In a [previous post](https://medium.com/@justiceconder/writing-on-github-c35ddd12bfd8), I spoke about moving to GitHub as a technical writing platform. In this post, I will address some of the challenges I faced, methods of resolution, and future goals as I continue down this journey. If you want to know the exact reasons I have made this change you can review that [previous post](https://medium.com/@justiceconder/writing-on-github-c35ddd12bfd8).

But just to recap some of the largest points:

*   Knowledge workers should be consistently producing useful content
*   The most precise way of measuring and collaborating on that content is with a version control system
*   GitHub naturally presents itself as an ideal platform for this

**Writing Modes**

When I first started down this path, I wasn’t accustomed to writing in markdown. I typically did all my writing in Google Docs. After migrating some of my existing writing projects to a GitHub repository with this [addon](https://www.buymeacoffee.com/docstomarkdown), I cloned them to my local machine and started looking for a good markdown editor. This is where things got strange. It seems that writing in markdown has become something of a rising trend to the degree that there are several paid editors on the market with some even requiring a paid subscription. That kind of blew my mind. A subscription text editor? Thankfully, I didn’t capitulate and decided to just use [Visual Studio Code](https://code.visualstudio.com/) as my editor. I had to brush up on the IDE interface, staging and committing changes, and package installation. I few things I liked about this setup were:

*   No third-party access to my repository
*   Unambiguous git interactions
*   Side-by-side rendering of markdown content
*   A Grammarly extension (removed from the market place but still available [here](https://github.com/znck/grammarly/releases/tag/v0.12.2))
*   Options to use “second/external brain” approaches with things like [Foam](https://foambubble.github.io/foam/)

The exercise proved beneficial but one aspect of the workflow I still really didn’t like was the Grammarly integration. By accident, I discovered that editing files directly from within the browser on the GitHub website itself proved sufficient for most things I wanted to do. Talk about going full circle. After adding [GitHub Writer](https://github.com/ckeditor/github-writer), a browser extension that made editing markdown files even more friendly and realizing that the [Grammarly browser extension](https://support.grammarly.com/hc/en-us/articles/115000091552-Install-the-Grammarly-browser-extension) worked as well when this extension was enabled, I started to really fall into a groove. What’s cool is that all my content is still available locally if needed (meaning I can interact with it with any application on my machine) but still conveniently available to be edited within a browser window. It’s really the best of both worlds.

 

**Image Management**

Image paths in GitHub repositories can be tricky. While GitHub does offer an [image hosting CDN](https://gist.github.com/vinkla/dca76249ba6b73c5dd66a4e986df4c8d) mechanism, there is no mechanism to view-all-uploaded or [delete images](https://stackoverflow.com/questions/33215211/github-how-do-i-delete-an-attachment-in-github-issues) once uploaded. I didn’t want to use dropbox as that entire domain can be blocked on some corporate networks so landed on a slick [Imgur](https://imgur.com/) workflow that handles my local screenshot needs as well. With this [mac app](https://github.com/mileswd/mac2imgur) and an Imgur account, you can drag and drop images to be uploaded or just take any screenshot and it will be uploaded to your account and the link copied to your clipboard.

**Organization and Workflow**

I am staying organized on priorities and in-flight work with a [GitHub project board](https://github.com/features/project-management/). I recommend creating your main project board at the topmost level of your GitHub account so you can use a single cross-cutting board to link issues to any of your repositories. If you make it at the level of a single repository then it is scoped to that repository. Milestones can be used to create a cadence if you are working in sprints.

My workflow starts with creating an issue. I’ll add miscellaneous thoughts into the issue as ideas come to me on a topic and also talk through issues with peers. When it seems the ideas are fleshed out sufficiently, then a new markdown file can be created in the relevant repo and a first draft created and committed from those developed notes in the issue. This is [the issue](https://github.com/singularityhacker/Content/issues/2) that started this very post.

**Presenting Content**

I’m most frequently working in private repositories but have a need to present content to people who don’t have access. This is where [HackMD](https://hackmd.io/) comes in. It allows me to pull in content from any repo (even private) and present it [as a slideshow](https://hackmd.io/c/tutorials/%2Fs%2Fhow-to-create-slide-deck). Any updates to that file in git can be pulled into the HackMD version and it also allows pushing the other direction as well.

**Future Steps**

One of the several motivations I had in making the move to writing on GitHub was to encourage a don’t-break-the-chain pattern. This is useful as can be seen from my commit history since June. I even went to the trouble of adding my commit-graph to my Apple watch with [this app](https://apps.apple.com/us/app/contributions-for-github/id1153432612). I consider this a good first pass at what I’m trying to accomplish but I think I’m increasingly eager to move into the next step of quantifying this output.

The next logical step will be to quantify daily word count, and not just commits. The GitHub commit-graph counts two commits of one word each as more than a single commit of a thousand words so it’s really not a good proxy of consistent content creation. Just like lines of code, word count is not a determining factor of good work but it means some activity/effort is happening. I’m hopeful that I’ll be able to accomplish something like this with a [GitHub action](https://github.com/features/actions). Secondly, I’d really like to be “releasing” more frequently. If authoring can be construed as development and publishing (as a presentation, article, or documentation) can be viewed as deployment, then I need to deploy a lot more frequently.

This is the conclusion of my second update on this journey. Feel free to follow me on [Medium](https://medium.com/@justiceconder) or [GitHub](https://github.com/singularityhacker) to get updates or possibly collaborate on future endeavors.

[Github](https://medium.com/tag/github?source=post_page---footer_tags--db7c157f21da-----------------------------------------)

[Technical Writing](https://medium.com/tag/technical-writing?source=post_page---footer_tags--db7c157f21da-----------------------------------------)

[Automation](https://medium.com/tag/automation?source=post_page---footer_tags--db7c157f21da-----------------------------------------)

[DevOps](https://medium.com/tag/devops?source=post_page---footer_tags--db7c157f21da-----------------------------------------)
