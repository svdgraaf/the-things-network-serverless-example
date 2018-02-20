# ttn-serverless-demo
Demo for setting up a Serverless TTN integration

This is the demo app which was shown during the The Things Network Conference.

You can find the slides on [slideshare](https://speakerdeck.com/svdgraaf/the-things-network-end-to-end-serverless-applications).

BEWARE
------
This is a demo to show you how to setup an example integration, this is no way a comprehensive setup, but it will get you started with a simple setup

Setup
-----

- Checkout the code (eg: `git clone https://github.com/svdgraaf/serverless-ttn-demo.git`), or download the [zip](https://github.com/svdgraaf/serverless-ttn-demo/archive/master.zip)
- Install the [NPM](https://www.npmjs.com/) dependencies: `npm install`
- Make sure you have your `TTN_APP` key (you can create them in the TTN console) in your environment (eg: `export TTN_KEY=ttn-account-v2.o7...` in your terminal)
- Be sure you have setup your [AWS credentials](https://serverless.com/framework/docs/providers/aws/guide/credentials/) (eg `~/.aws/credentials`)
- Deploy the app with `sls deploy`
- The output will contain the endpoint for your `uplink`, copy that url.
- Go into the TTN console, and setup an http integration, point the endpoint to your `uplink` endpoint. Make sure you set it to `POST`. The demo doesn't do ANY authentication
- Done. The connections are setup, you can test a payload using: `echo "19.6" | xxd -pu | xargs ttnctl devices simulate my-device-name;`
- Check that the value ends up in the created DynamoDB table (by default it's called `ttn_serverless_demo`)
- ...
- Profit!
