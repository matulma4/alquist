Alquist
=======
Alquist is dialogue manager created by Jakub Konrád and Petr Marek.

You can test current demo at https://alquistmanager.github.io/alquist-client/?e=https://alquist.herokuapp.com

You can use HTML client https://github.com/konrajak/alquist-client for workig with Alquist.

## Installation
You need Python 3. 

We use WIT.ai as our npl service currently so you will need to install WIT as well

	pip install wit
	
We use PyYaml. You need to install it by

    pip install PyYaml

We use Flask-Cors. You need to install it by

    pip install -U flask-cors

To run Alquist use command

	py -3 main.py
	
You can change Alquist's parameters. They are stored in the ``config.py``.

``port`` field defines the port on which the Alquist will run.

``wit_token`` defines which wit.ai app will you use. For our demo use ``NXOFXMBCIA6YAIXNNWYXJIJPC22AK35V``

``yaml_files_path`` path to folder, where yaml files are located.

For example:

	config = {"port": 5000,
          "wit_token": "NXOFXMBCIA6YAIXNNWYXJIJPC22AK35V",
          "yaml_files_path": "yaml\demo"}

## API

###Request
To communicate with Alquist use POST requests to url, on which the Alquist is running. POST have to contains JSON with fields:

- text
    Contains user's input text. You can leave it blank, if user has nothing to say (when the Alquist starts a dialogue and we need to prompt
    it to start for example).
- state
    Name of state, where we currently are. The state is "init" at the start of dialogue usually. Must contain something every time.
- context
    Json object representing context. There must be empty Json object at least every time.
- session
    ID of session used during logging. Can be empty at the start of dialogue.
    
###Response
Response contains JSON with fields:

- messages
    List of Alquist's answers. Each answer is object.
    - type
        Type of message. It can be ``text``, ``button`` or ``iframe``.
    - payload
        Information about message. It differs according to type of message:
        - ``text`` type
            - text
                Text to show
        - ``button`` type
            - label
                Button's label
            - next_state
                State to transform to after button click
            - type
                Type of button. This field doesn't have any specific values. You can send some string and implement button according to it in client.
        - ``iframe`` type
            - url
                Iframe's url
            - width
                Iframe's width (in the percents)
            - height
                Iframe's width (in the pixels)
            - scrolling
                Will be scrollbar visible?
            - align
                Iframe's align
            
    - delay
        Delay of massage in the milliseconds.        
- state
    Name of new state, where we get to. Use this name in the next request (state field).
- context
    Json object containing updated context. Use this object in the next request (context field).
- session
    Generated ID of session used during logging. Use this ID in the next request (session field).
    
###Example
####Request
    curl -H "Content-Type: application/json; charset=\"utf-8\"" -X POST -d "{\"text\":\"INSERT_INPUT_TEXT\", \"state\":\"INSERT_STATE_NAME\", \"context\":\"INSERT_CONTEXT_OBJECT\", \"session\":\"INSERT_SESSION_ID\"}" "INSERT_ALQUIST_URL"

Specific example:

    curl -H "Content-Type: application/json; charset=\"utf-8\"" -X POST -d "{\"text\":\"Hello world!\", \"state\":\"init\", \"context\":{}, \"session\":\"\"}" "http://127.0.0.1:5000/"

## Docker
Alquist is prepared to be run in a Docker container. The setup process is quite straightforward.
###Building an image
Dockerfile is already present in the main directory. Run ``docker build -t alquist .`` to build the Docker image for Alquist. Alternatively, you can obtain pre-built image from Docker Hub with the ``docker pull alquistmanager/alquist`` command.
###Launching a container
Once the image is built, run the ``run-docker-container.sh`` bash script. There are two parameters required: First is a port you want Alquist to run on and the second is absolute path to your ``.yml`` files.
