# storyteller
Forward dictionary of Korean Proverbs

[Reverse dictionary of Korean Proverbs (using BERT model)](https://github.com/eubinecto/wisdomify)

## Quick Start

Install virtualenv (if you already installed, you can skip):
~~~bash
pip3 install virtualenv
~~~

Clone this project and set up a virtualenv:
~~~bash
git clone https://github.com/ArtemisDicoTiar/storyteller
cd storyteller
virtualenv storyteller
source storyteller/bin/activate  # activate the virtualenv
pip3 install -r ./requirements.txt  # install the required libraries onto the virtualenv
~~~

After installing all packages: 

If you are trying to download proverbs from opendict(우리말샘), you MUST have your own api token.

The format of .env file should be like:

~~~.env
opendict_api="{your api token}"
~~~

After you add .env file, the project will automatically use your api token using "secrets.py".

Now the project structure should be look like the following.

~~~
.
├── README.md
├── .env
├── storyteller  -> virtualenv
├── collect
│   └── main
│       ├── downloader.py
│       ├── modifiers
│       │   ├── exampleOrganiser.py
│       │   └── opendictOrganiser.py
│       ├── parsers
│       │   ├── definitions
│       │   │   ├── namuwikiParser.py
│       │   │   ├── opendictParser.py
│       │   │   └── wikiquoteParser.py
│       │   └── examples
│       │       ├── daumDictCrawl.py
│       │       ├── naverDictCrawl.py
│       │       └── utils.py
│       └── paths.py
├── requirements.txt
└── secrets.py
~~~

Your storyteller gives you:
~~~bash
python3 -m storyteller.main.downloader --{arg} {arg value}
~~~

Arguments:
* which (which type of data do you want to be heard?)
    * definition (default)
    * example
* where (you are calling the data from)
    * (if which is **definition**)
        * wikiquote (default)
        * namuwiki
        * opendict
    * (if which is **example**)
        * naverdict (default)
        * daumdict
        * koreauniveristy 
        * corpuskorean
        * kaist
* target (if which is example, which proverbs do you want to download)
    * wikiquote (default)
    * namuwiki
    * opendict

Example
~~~bash
python3 -m storyteller.main.downloader --which example --where daumdict --target wikiquote
~~~
