# Medieval Peasant Database

The [Medieval Peasant Database (MPDB)](https://medievalpeasants.com) is a free, open-source, and accessible database for the wealth of [England's manorial court documentation](http://www.nationalarchives.gov.uk/help-with-your-research/research-guides/manors-further-research/#3-court-rolls-c1200-1954). The website began as a place to store my own dissertation research. However, the need for archival preservation and to give future scholars access to my work drove me to create the [MPDB.](https://medievalpeasants.com) The website, database, and this source code are the result of these efforts.

### Access 
To access and look through the data currently in the database, simply navigate to the [MPDB.](https://medievalpeasants.com) 

### Contribution
If you wish to contribute to the project code, please [open an Issue](https://github.com/neighlyd/medievalpeasants/issues) or [submit a pull request.](https://github.com/neighlyd/medievalpeasants/pulls)

If you wish to contribute to the project data set, please [contact me.](mailto:neighlyd@gmail.com)

## Source Code and Website

The [MPDB](https://medievalpeasants.com) is primarily intended to be accessed through its website, rather than cloned and run on its own. This is because much of its usefulness relies on the data in its MySQL database. The website structure itself, which this repository represents, is only a portal to that database. I have made the website open sourced to the fullest extent possible for several reasons:

* To increase transparency in the project.
* To ensure that the project will outlive me.
* To aid in security and robustness.
* To encourage further engagement with technology among historians and with history among technologists.


## Technologies

The [MPDB.](https://medievalpeasants.com) was primarily written using [Django](www.djangoproject.com). I used [JQuery](https://jquery.com) and [Datatables](https://datatables.net) to make the website more responsive. These responsive technologies interact with the Django backend using a REST API framework powered by [Django Rest Framework.](https://www.django-rest-framework.org/) This API is read-only at the moment. The data in the data [MPDB.](https://medievalpeasants.com) is currently intended for consumption through the website rather than the API. This is a feature that I will be changing in the future to facilitate further integration with other technologies.

## Challenges and Learnings
Creating and maintaining the [MPDB](https://medievalpeasants.com) came with several challenges and learning opportunities ranging from UX research to teaching myself how to code. Working on the project was an immense opportunity for me.

The first challenge in developing the [MPDB](https://medievalpeasants.com) was understanding what technologies the project needed. I knew that I needed a robust way to store the volume and scope of data I was dealing with. I quickly recognized that spreadsheets and document files were unwieldy and not rigorous enough. This brought me to databases and learning about [database normalization](https://en.wikipedia.org/wiki/Database_normalization).

### Initial Research

I initially coded the [MPDB](https://medievalpeasants.com) in [Access](https://products.office.com/en-us/access). As the connections between peasants, land, and cases became sufficiently complicated, so too did the forms used to enter and edit them. At the same time, I found myself questioning the amount of work that previous historians had done on these topics which was lost to posterity. These two factors led me to search for an easily scalable, web-friendly solution.

I researched several solutions. Because I was already dealing with a relational database, I ruled out [NoSQL](https://en.wikipedia.org/wiki/NoSQL) alternatives such as [MongoDB](https://www.mongodb.com) running on [Node.js.](https://nodejs.org) This led me to choosing between [Ruby on Rails](https://rubyonrails.org) and [Django](https://www.djangoproject.com). I opted for Django due to the simplicity and straightforwardness of [Python](https://www.python.org).

My next challenge was perhaps my largest - I had to learn how to code.

### Learning to Code
After choosing Django as my web framework. I was confronted with the simple fact that I didn't know how to write a single line of code. To implement my vision of a free, open, and accessible repository of medieval court data, I needed to teach myself how to read and write code.

I began using tutorials, blogs, and educational series such as [MIT's opencourseware](https://ocw.mit.edu/index.htm) to learn the fundamentals of Python and coding. I wrote, and rewrote, the [MPDB](https://medievalpeasants.com) as I learned. As the complexity of my project grew, the need to learn more grew as well. Each new speed bump presented itself as an opportunity for me to educate myself on additional features of programming, such as [data structures](https://github.com/neighlyd/algo_practice), reading documentation, [algorithms](https://github.com/neighlyd/algo_practice), [APIs and REST frameworks](https://github.com/neighlyd/node-todo-api), using git, and [contributing to open source projects.](https://github.com/search?q=is%3Apr+author%3Aneighlyd)

### Usability and UX Research

Expanding access to research materials is a core feature the [MPDB.](https://medievalpeasants.com) In order to facilitate this, I engaged in a series of Usability and User Experience research sprints. I contacted several prominent historians within my field and interviewed them. These interviews covered a wide range of topics, including their own research methods, interactions with technologies, where they saw the field moving, and also included usability studies with my website.

I incorporated the feedback and learnings from these interviews into the design and implementation of the [MPDB.](https://medievalpeasants.com)

## TODO
* Setup API to be more responsive to external requests.
* Integrate additional, responsive CRUD elements to expand user engagement. 
* Add unit tests
* Polish code
