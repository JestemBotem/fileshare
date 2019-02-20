# Task
1. Please create a system that allows you to transfer files and URL addresses in a secure way. In the task, use Django generic views to support the forms, and Django REST API to build the API.
2. The application should provide logged-in users (for the purposes of the task, users can be created by command or using the admin panel) the form accepting the file or the URL that we want to protect. After sending it to the user, the generated new unique address (within the application) and the generated password should be displayed. The generated link should be valid for 24 hours. This part should be covered by tests.
3. After clicking generated link, you should see a form that allows you to enter your password. If it is compatible with the password generated in the database, then the user is redirected to a protected URL or to download process of the protected file. The number of correct password additions should be counted for each link.
4. For each logged-in user, the User Agent from which he made the last query, should be remembered, i.e. refreshed with each request sent, to any sub-page within the system (User Agent is available in the request header).
5. It should also be possible to manage the application using the admin panel, in particular changing the password assigned to the element.
6. The application also provides APIs similar to created forms, a secured part for adding new elements, and an unsecured one to enter the password.
7. In addition, a secured endpoint should be created to provide information on the number of items of each type, added every day, that have been visited at least once (see example).

Example:

October 25, 2017, added:

file that you have visited 5 times

the link that has been visited 2 times

October 26, 2017, added:

file that has been visited 2 times

another file that has not been visited even once

a link that has not been visited even once

The result of the query should be:

```{
    "2017-10-25": {

        "files": 1,

        "links": 1

    },

    "2017-10-26": {

        "files": 1,

        "links": 0

    },
}``



Functionalities:
A form that adds links or files for protection
Generating links protected with a password
Expiry of links after a specified time
A form that allows you to go to a secured link or download a protected file
Counting correct redirects
User Agent saving
REST API
the secured endpoint for adding elements
the secured endpoint for downloading statistics (see example)
an open endpoint to access secure items (if the password was correct)
Admin panel​​
System assumptions:

The use of Django generic views
The use of Django REST framework
The generated link is valid for 24 hours
The mechanism of adding elements for protection should be covered by tests
Changing the password for secure items using the admin panel

Additional rules & hints

​​The application's code should be kept in a public repository so that we can read it, pull it and build it ourselves. Remember to include README file or at least basic notes on application requirements and setup - we should be able to easily and quickly get it running.
Written application must be hosted and publicly available for us online - we recommend Heroku.