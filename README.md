# INF142_Assigntment1
Assignment in the UIB course INF142 where made a server-client model. A server is started and assigns roles to clients, then clients communicate each other by receiving or giving advice based on the role they were assigned.

## Getting Started

### Prerequisites
For this project we elected to use the rich library for some formatting to make text clearer.

For the library and its functions see: https://github.com/Textualize/rich

The library is in [requirements.txt](requirements.txt), but in case it doens't install you can install it with ``pip``:

``python -m pip install rich``

If you do not wish to use the rich library or cannot install it, the text formatting will be weird but should still be readable.

An example of what the text looks like without rich:

![wrong text ex](https://user-images.githubusercontent.com/78080565/222165433-fb064895-228f-4d38-9839-b30fdf370768.PNG)

An example of what the text looks like with rich:

![correct text example](https://user-images.githubusercontent.com/78080565/222166299-589b95e8-63d1-4130-9ca6-15194f66e018.png)

## How to run
1. Run ``server.py``

2. Run ``client.py`` to get the role of advisee, and then write your question and hit enter

3. Run another instance of ``client.py`` until you get the advisor role (might take a few tries)

4. In your advisor instance of the program, write your answer and hit enter

5. As both client and server, write ***y*** if you want a new role and ***n*** if you do not.

## Authors
* **Andreas Søland Henriksen** - [andreashenriksen](https://github.com/andreashenriksen)
* **Emil Eldøen** - [Emil-Eldooen](https://github.com/Emil-Eldooen)
