# ttn-serverless-demo
Demo app for setting up a Serverless The Things Network integration.

This is the demo app which was shown during the The Things Network Conference.

This was part of my talk for the Things Conference, you can view my [slides](https://speakerdeck.com/svdgraaf/the-things-network-end-to-end-serverless-applications) here, and watch my talk on youtube here:

[![Serverless end to end Lorawan solutions](https://github.com/svdgraaf/serverless-ttn-demo/blob/master/talk-intro.png?raw=true)](https://www.youtube.com/watch?v=DCTrIQcLa4Y)

BEWARE
------
This is a demo to show you how to setup an example integration, this is no way a comprehensive setup, but it will get you started with a simple setup

Architecture
------------
![Architeture](https://github.com/svdgraaf/serverless-ttn-demo/blob/master/architecture.png?raw=true)

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
