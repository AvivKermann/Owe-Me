
# Owe-Me - a Web Based Application To Keep Track Of Debts.
#### Video Demo:  https://youtu.be/ZGotTwaUXs4
#### Description:

This is a web-based application created using HTML, CSS, and Python with the Flask framework. The primary purpose of this application is to help users keep track of their financial transactions, specifically tracking debts and credits between users. Users can add new debts, mark debts as settled, and view their transaction history.

## Features:

- User Authentication: Users can register, log in, and log out securely.
- Add Debts: Users can add new debts specifying the debtor, amount, and description.
- Close Debts: Users can mark debts as settled, updating the database automatically.
- View Debts Owed: Users can see a list of all the debts they owe to other people.
- View Debts Owed to You: Users can see a list of all the debts other people owe to them.
- Transaction History: Users can view a history of all debts, including whether they have been settled or not.

## Files Overview:

- in the app.py file there is the intire backend code that handles all of the routing and database intractions and calculations.
- in the templets directory there is all the html file that needed to be rendered for the project, most of them take the layout of layout.html
so if changes are needed most likley they will be changed in a single location.
- helpers.py is a file that defines a few key function to run authentication and more and is being imported to app.py
- in static there is the css style sheet and controls everything and a logo file that i added to the website.
- owned.db is the sqlite3 db file



## Installation:

1. Clone this repository to your local machine:

2. Navigate to the project directory:

3. Install the required Python packages using pip:
pip install -r requiremnts.txt


4. Set up your database. You can use SQLite or another database of your choice.
for the making of this project sqlite3 was used, other DB's might have some issue regarding the code.

5. Configure the database connection in the `config.py` file.

6. Run the application:
while in the application directory run commend: flask run and click the link.

on a personal note i am so grateful for this opportunity to learn from David and the rest of the teaching staff and for that i will owe you guys forever!, from the bottom of my heart thank you guys so much for the amount of effort that was put into this course.
thanks for much for the time to read this and hopefully wel'l meet again in CS50W.
aviv kermann, israel, 2023







