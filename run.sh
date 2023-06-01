# Setup client
cd client
python3 -m venv .
source bin/activate
pip install -r requirements.txt
python3 main.py &

# Setup server
cd ..
cd server 
npm i
npm start