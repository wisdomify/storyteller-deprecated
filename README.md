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
virtualenv storytellerEnv
source storytellerEnv/bin/activate  # activate the virtualenv
pip3 install -r ./requirements.txt  # install the required libraries onto the virtualenv
~~~

After installing all packages: 

If you are trying to download proverbs from opendict(우리말샘), you MUST have your own api token.

The format of .env file should be like:

~~~.env
opendict_api="{your api token}"
gw_username="{SSH gateway instance username}"
gw_host="{SSH gateway instance address}"
gw_pkey="{SSH gateway instance ssh public key}"
gw_port="{SSH gateway instance's ssh port}"
db_username="{Database username}"
db_host="{Database internal address}"
db_password="{Database password}"
db_port="{Database port}"
storyteller_schema="{storyteller's schema name}"
~~~

After you add .env file, the project will automatically use your api token using "secrets.py".

Now the project structure should be look like the following.

~~~
.
├── README.md
├── .env
├── requirements.txt
└── storyteller
    ├── collect
    │   ├── modifiers
    │   │   └── exampleOrganiser.py
    │   ├── parsers
    │   │   ├── definitions
    │   │   │   ├── namuwikiParser.py
    │   │   │   ├── opendictParser.py
    │   │   │   └── wikiquoteParser.py
    │   │   └── examples
    │   │       ├── daumDictCrawl.py
    │   │       ├── koreaUniversityCrawl.py
    │   │       └── naverDictCrawl.py
    │   └── utils
    │       ├── morphAnalysis.py
    │       └── proverbUtils.py
    ├── examples
    │   └── collect
    │       ├── explore_parsers_definitions.py
    │       ├── explore_parsers_examples.py
    │       ├── explore_utils_morphAnalysis.py
    │       └── explore_utils_proverbUtils.py
    ├── main
    │   └── dl_data.py
    ├── paths.py
    ├── secrets.py
    └── tests
~~~
Your storyteller gives you:
~~~bash
python3 -m storyteller.main.dl_data --{arg} {arg value}
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
python3 -m storyteller.main.dl_data --which example --where daumdict --target wikiquote
~~~
