# AERIUS API examples 

## Introduction 

AERIUS has some [documentation available online](https://connect.aerius.nl/api/), but no active Python examples. Their [GitLab repository](https://gitlab.com/AERIUS/aerius-connect-examples) didn't work for me, and their help desk confirmed that only the Swagger documentation is current. That also has some issues though: when uploading the GML files, the example seems to generate incorrect JSON information, with brackets in the wrong place (they [mention this](https://connect.aerius.nl/api/?urls.primaryName=WNB%20berekeningen) in the documentation themselves). All in all, I found it confusing to get the Python API working, and saw no other examples on GitHub, so I decided to write some, out of curiosity. 

The code is very rudimentary, but it works well enough, and should serve as a basis for adding more functions as needed. 

## Overview 

You place a GML file (generated through the AERIUS web calculator, exporting _Invoerbestanden_ after entering all the information) into the GML folder. Those are basically XML files, so you can modify them after, but I found it helpful to have the initial set-up. You then set your API key in the ```get_report()``` function. 

```python
def get_report() -> None: 
    """Example for the report generation. Set your API key here. 
    """
    logger = get_logger(__name__) 
    api_key = "[...]" 
    gml_file = "test2.gml" 
    file_dest = "output.zip"
```

Then, point the code to your GML file, set a desired output file name, and let it run. 

It usually takes around a minute to run everything. Once it's done, the service sends back a ZIP containing another GML file with a huge amount of information (~5 MB compressed, 126 MB uncompressed). 

## Future changes 

I may add command line arguments to make it easier to use. However, given the current simplicity of the code, editing it directly is probably preferable. I haven't looked into the GML file output much yet - that could be a nice extension to the code. 

## Requesting API key 

To start, you have to generate an API key. I advise doing that via [their website](https://connect.aerius.nl/api/?urls.primaryName=Gemeenschappelijk#/user/generateApiKey) (under _Try it out_). You can also do it via the code, with ```request_api_key```. You can then set that in the code. You'll get an email back with the API key in there. 

## Disclaimer 

I don't see any information about rate limitations on the website, and didn't encounter issues even when running the code a few times during debugging. I would advise keeping the status query rate high though (one second by default) and not sending too many report requests at once though. 

I made this over the weekend because I got curious if I could get it working - this is not a serious project. 