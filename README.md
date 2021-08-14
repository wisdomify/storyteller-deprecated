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
Your storyteller gives you the raw data with dvc:
Therefore, you must install dvc.

~~~bash
pip install 'dvc[s3]'
dvc pull
~~~
Then you will be able to see the data on `./data`
