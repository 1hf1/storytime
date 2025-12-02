#Setup Instructions

## Step 1: Fork/pull this repository from Github to your local machine

## Step 2: Install conda, create and activate a new environment called StoryTime and install the dependencies listed in requirements.txt:
'''
conda create -n StoryTime
conda activate StoryTime
pip install -r requirements.txt
'''

## Step 3: Ensure that npm is installed on your machine. If not, install it using the following command:
'''
npm install -g npm
'''

## Step 4: Install the frontend dependencies listed in package.json:
'''
cd frontend
npm install
'''

## Step 5: Add backend API keys
Since OpenAI immediately revokes publicly shared keys, you may need to add a new OPENAI_API_KEY to the backend/.env file. You can generate a new key by visiting https://platform.openai.com/account/api-keys. You may also need to add a new PERPLEXITY_API_KEY to the backend/.env file. You can generate a new key by visiting perplexity AI and going to your account settings, and then accessing the 'API' tab. 