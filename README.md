# social-network-console-based

  
  

This technical challenge was made with TDD, pytest and Python.

  

Since I wasn't used to working with Python, developing the challenge included learning the syntax and usage of it, as well as the tests sintaxis. This took longer than I expected, and I didn't have enough time to cover serious cases and make improvements. It has been a challenge, especially mocking up dates in a new language, which I love because of the lessons I learned.

  

### Uncovered cases that I would have liked to cover:

  

- Display all messages in wall in descending order by timestamp. Now they are in descending order by timestamp but also by user.

- When following another user, check if is not already stored in `following` dictionary. Now you can follow more than once to the same user and, in wall, messages are duplicated.

- Add more cases with different times in tests when `reads_message_by_username` to be sure if prints correctly.

- When following, check if before and after the 'follows' word there is just one word, as it's done in Posting.

- Create different modules for each scenario (Posting, Reading, Following and Wall), each module with it's tests and test collaborations between them. And that would then be a scalable program for new functionalities.

  

### Improvements:

  

- User management.

- Feedback messages to the user when writes wrong the command, for example "You need to add your username before the arrow. The format is 'username -> message'. Try again". Or when reading others messages and the list is empty, for example "Nothing is posted yet".

  

### About the program:

  

This is a consoled-based program that simulates a social-network.

  

#### To run the application:

- Run this command: `python src/social_network.py`

  

- The console is ready to receive the inputs.

  

- The commands are:

	- To post a message in your timeline: `username -> message`.

		- You can add many messages to the with the same username or others.

		- For example:

			\> Ari -> hola.

			\> Ari -> qué onda?

			\> Sebas -> todo bien.

- To read messages from a user: `username`

	- You will read their messages in descending order by time and and how long ago it was posted.

- To follow someone: `username follows another-username`

- To see youw wall: `username wall`

	- You can see your messages and the messages of the users you have been followed.