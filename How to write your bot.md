How to write your bot using ALQUIST
===================================
Alquist is dialogue manager created by Jakub Konrád and Petr Marek.

## General tips
### Start of the dialogue
When writing yaml representation of your bot, keep in mind that the initial state for your bot should be called ``init``
Ihere always needs to be ``init`` state in your yaml representation.

For example:

	init:
        type: message_text
        properties:
            text: Hello, my name is Talkatron 3000
        transitions: 
            next_state: state2

### Transitions
Each state must have transitions field, since it is used in constructor. 
Parameter of transition is key ``next_state`` and name of state, where you want to go after the execution of state. The state can be even from different flow.
 ``conditional_exists`` and ``conditional_equal`` has different transition parameters. See State descriptions section.

For example:

	state1:
        type: message_text
        properties:
            text: Hello World!
        transitions: 
            next_state: state2
 
If the transitions field is empty, conversation ends after executing current state.

For example:

	state1:
        type: message_text
        properties:
            text: Hello World!
        transitions: 
        
If the transitions field is missing, the default transition is to next state in yaml file. If there is no next state in the yaml file, the dialogue ends.

For example:

	state1:
        type: message_text
        properties:
            text: Hello World!
            
Use ``flow: flow_name`` parameter in the transitions field to jump to the first state of different flow.

For example:

	state1:
        type: message_text
        properties:
            text: Hello World! 
        transitions: 
            flow: flow_name


### State construction
States have UNIQUE ``name`` across all your flows. There can't be two states with the same name.

Each state declaration must contain fields ``type`` declaring the state type,
``properties`` containing the state parameters, and ``transitions`` which holds information about next state

	[name]:
        type: [state_type]
        properties:
            [state_properties]
        transitions:
            [state_transitions]
            
     
### Invoking session context        
To use a variable from the session context, use ``'{{variable}}'``
Examples:

	state1:
        type: message_text
        properties:
            text: My name is '{{name}}'
        transitions:

Bot replaces ``'{{name}}'`` with value of the ``name`` key saved in the session context and sends ie. "My name is Max"

	state1:
        type: conditional_equal
        properties:
            value1: '{{ intent }}'
            value2: greeting
        transitions:
            equal: positive_case
            notequal: negative_case

Bot replaces ``'{{intent}}'`` with value of the ``intent`` key saved in the session context and compares it with string "greeting".


### Distribution of dialogue between multiple flows
Dialogue can be distributed between multiple yaml files. Each file contains one flow. Place flows into one folder and use it's path as program argument.

### Intent transitions
If your bot supports multiple topics and you want to allow user to switch between them any time, you will like Intent transitions.
Intent transitions allows you to define nodes to which dialogue will jump, if specific intent is detected. Intent transitions are defined
as follows in the yaml file.

    name: flow1
    intent_transitions:
        intent1: state1 #name_of_intent: state_to_transition
        intent2: state2
        intent3: state1
    states: 
        state1:
            ...

Intent has to be trained in the Wit.ai as one of entity with the name ``intent``. Intents are checked every time, user inputs something.

### Delays
You can define delay between two following outputs or between user's input and output by ``delay`` property. The delay is not implemented as 
time delay directly in Alquist. The length of delay is send to client in the response instead. Client has to implement delay itself. Delay is
specified in the milliseconds. Delay has effect on states showing some output text only.

    state1:
        type: message_text
        properties:
            text: Text to show after 1000 milliseconds
            delay: 1000
        transitions:
            next_state: state2


## State descriptions
### message_text
message_text sends a message to user.

Example:

	[name]:
        type: message_text
        properties:
            text: [message_text]
        transitions:
            next_state: [next_state_name]
``text`` field contains a string, string can contain HTML tags **REQUIRED**

``next_state`` field contains name of the next state

Default property values:
* ``text``: *Your message here.*


### message_text_random
message_text_random sends a message from the list at random to user.

Example:

	[name]:
        type: message_text_random
        properties:
            responses:
                - [response1]
                - [response2]
        transitions:
            next_state: [next_state_name]
``responses`` field contains strings with responses to be selected at random, strings can contain HTML tags **REQUIRED**

``next_state`` field contains name of the next state

Default property values:
* ``responses``: *Your messages here.* 


### message_buttons
message_buttons is used to display predefined respones in the form of buttons to the user.

Example:

	[name]:
        type: message_buttons
        properties:
            buttons:
                - label: [label1]
                  next_state: [next_state_from_button1]
                  type: [type_of_button1]
                - label: [label2]
                  next_state: [next_state_from_button1]
                  type: [type_of_button2]
        transitions:
            next_state: [next_state_name]
``buttons`` field contains definitions of individul buttons (i.e. their labels and state transitions), **REQUIRED**
    
- ``label`` text shown on button

- ``next_state`` state to jump after click on button

- ``type`` type of button, can be any string, must be implemented on the client side

``next_state_from_button1`` state to transition to from button 1

``next_state`` field contains name of the next state


### message_iframe
message_iframe is used to display iframes containing arbitrary HTML content like formatted text or images

Example:
    
    [name]:
        type: message_iframe
        properties:
            url: [url]
            width: [iframes width (percents)]
            height: [iframe's height (pixels)]
            align: [iframe's align]
            scrolling: [yes/no]
``url`` contains iframe's address, **REQUIRED**

``width`` width of iframe in percents (integer only)

``height`` height of iframe in pixels (integer only)

``align`` iframe's align, possible values are 'left', 'right' and 'center'

``scrolling`` determines scrolling of iframe, only two possible values are 'yes' and 'no'

### change_context
change_context is used to change session context independently on user input.

Example:

	[name]:
        type: change_context
        properties:
            del_keys:
                - [del_entity1]
                - [del_entity2]
            update_keys:
               [up_entity1]: [value1]
               [up_entity1]: [label2]
        transitions:
            next_state: [next_state_name]
``del_keys`` field with keys to be deleted, **REQUIRED**

``update_keys`` field with keys to be updated, **REQUIRED**

``next_state`` field contains name of the next state


### input_user
input_user sends user a prompt, waits for user response and saves entities from the response to the context. 

Example:

	[name]:
        type: input_user
        properties:
            entities:
                entity1: [nlp_entity_name]
            log_json: true
            require_match: true
        transitions:
            match: state1
            notmatch: state2

``entities`` this field contains entities to save to context, **REQUIRED**

> ``entity1`` context key, under which the value is saved,
> ``nlp_entity_name`` name of the entity in the nlp

``log_json`` true/false, determines if latest user response should be saved in context for later use

``require_match`` true/false, determines if entities from the entity field need to be present in order to continue
> *we recommend to use* ``require_match`` *only for matching single entity, for multiple entities sequence of conditional states is preferred*

``match`` field contains name of the state used when the entities are matched or require_match is false

``notmatch`` field contains name of the state used when the entities are not matched


Default property values:

* ``log_json``: *false*
* ``require_match``: *false*


### input_context
input_context from the last user response saved to context via ``log_json: true`` and loads its entities.

Example:

	[name]:
        type: input_context
        properties:
            entities:
                entity1: [nlp_entity_name]
        transitions:
            next_state: [next_state_name]
``entities`` this field contains entities to save to context, **REQUIRED**
> ``entity1`` context key under which the value is saved
> ``nlp_entity_name`` name of the entity in the nlp

``next_state`` field contains name of the next state



### conditional_equal
conditional_equal branches dialog according to the equality of two values.

Example:

	[name]:
        type: conditional_equal
        properties:
            value1: [val1]
            value2: [val2]
        transitions: 
            equal: [positive_case]
            notequal: [negative_case]
``value1`` field contains first value to compare, **REQUIRED**

``value2`` field contains second value to compare, **REQUIRED**

``equal`` field contains a name of state to transition into in case values are equal, **REQUIRED**

``notequal`` field contains a name of state to transition into in case values are NOT equal, **REQUIRED**

### conditional_exists
conditional_exists branches dialog according to the existence of a value in context.

Example:

	[name]:
        type: conditional_exists
        properties:
            key: '{{context_key}}'
        transitions: 
            exists: [positive_case]
            notexists: [negative_case]
``key`` contains a key to search for in context in special format, **REQUIRED**

``exists`` field contains a name of state to transition into in case key exists, **REQUIRED**

``notexists`` field contains a name of state to transition into in case the key does NOT exist, **REQUIRED**

### UserDefinedState
You can define our own state. Keep in mind, that the name of your state type should be the same as name of your class, defining the state.
Place your states to ``states.user`` directory https://github.com/AlquistManager/alquist/tree/master/states/user. Each state has to be placed
in the separate file named the same as the state type name. There is example of HelloWorld state here.
