POC for using testability.js
============================

# Wait what ? 

This is just a proof of concept that utilizes following projects:
 * https://github.com/alfonso-presa/testability.js
 * https://github.com/alfonso-presa/testability-browser-bindings

Upstream projects - when injected into sut - will mock certain asyncronous
parts of javascript and provides a interface that can be used to query if
anything is running in the background..

# What needs to be done

* Find a way to hook the implementation of "Wait For Testability Ready"
  functionality into selenium library
* Find and document strategies to inject testability code into sut. Currently
  im just injecting them with script tags. Key thing here is that the js part
  should be injected into SUT as early as possible but with my limited
  experience with selenium/robot & seleniumlibrary, i dunno how  .. 
  but other strategies could be:
  * mitm proxy that modifies the html before its received by selenium/browser
  * provide keywords to inject the code into running sut
  * something  else ? 
  Key issue 

# Running

## Flask app
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=webapp
flask run
```

## Robot test

```
source venv/bin/activate
robot tb.robot
```

Also, you need webdriver and browsers installed .. 

# Browser compatibility

you could pass --variable BROWSER:Firefox or  --BROWSER:Chromne see how things
work in each browser .. 

Known issue is that atleast chrome, not sure about other webkit based
browsers, doesnt trigger transition start event.


