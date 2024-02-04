
<div align="center">
<img src="https://i.imgur.com/rV2ndIr.png">
</div>
<h1 align="center">
  Talking Terry
</h1>
<h4 align="center">A hands-free phone that can answer any question powered by GPT-4, LangChain, and APIs from SerpAPI, Yelp, Twilio, and more!</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> 
</p>


## Key Features

* Answers any question!
* Utilizes APIs from SerpAPI, Yelp, Twilio, BruinLearn/Canvas, and Weather API for retrieval-augmented geneneration and to ensure accuracy
* Built with Raspberry Pi, GPS module, microphone, and a speaker
* Saves every conversation to Google Cloud Platform
* Portable and convenient to use
* Remembers and references past conversations

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/downloads/), [OpenAI](https://pypi.org/project/openai/), [Google Cloud CLI](https://cloud.google.com/sdk/docs/install), [pip](https://pip.pypa.io/en/stable/installation/), and [LangChain](https://pypi.org/project/langchain/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/tranbrandon1233/TalkingTerry

# Go into the repository
$ cd TalkingTerry

# Install requirements
$ pip install -r requirements.txt

# Install Google Cloud CLI (if necessary)
$ (New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")

& $env:Temp\GoogleCloudSDKInstaller.exe
  
# Initialize gcloud
$ gcloud init

# Complete authentication
$ gcloud auth application-default login

# Run the app
$ python transcribe.py
```



## Credits

This software uses the following packages:

- [LangChain](https://pypi.org/project/langchain/)
-  [Python](https://www.python.org/downloads/)
- [OpenAI](https://https://openai.com/)
- [Twilio](https://www.twilio.com/)
- [Yelp API](https://docs.developer.yelp.com/docs/yelp-platform)
- [SerpAPI](https://serpapi.com/)
- [Weather API](https://www.weatherapi.com/)
- [BruinLearn/Canvas API](https://bruinlearn.ucla.edu/)


