# ttn-serverless-demo
Demo for setting up a Serverless TTN integration

This is the demo app which was shown during the The Things Network Conference.

You can find the slides on [slideshare](https://speakerdeck.com/svdgraaf/the-things-network-end-to-end-serverless-applications).

BEWARE
------
This is a demo to show you how to setup an example integration, this is no way a comprehensive setup, but it will get you started with a simple setup

Setup
-----

- Checkout the code
- Make sure you have two values in you environment (`export FOO="bar"`):
  o TTN_KEY: The value of your key (you can create them in the TTN console)
  o DYNAMODB_TABLE: The name of the table you want to create (serverless will create it for you)
- Be sure you have setup your AWS credentials (eg `~/.aws/credentials`)
- Deploy the app with `serverless deploy`
- The output will contain the endpoint for your `uplink`, copy that url.
- Go into the TTN console, and setup an http integration, point the endpoint to your `uplink` endpoint. Make sure you set it to `POST`
- The connections are setup, you can test a payload using: `echo "19.6" | xxd -pu | xargs ttnctl devices simulate my-device;`
