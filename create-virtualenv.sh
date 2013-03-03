echo "Please..."

#create virtual enviroment
cd ..

virtualenv --no-site-packages  .
source bin/activate

cd tryton-buildout
pip install -r requirements.txt


#create buildout
mkdir build
python bootstrap.py

./build/bin/buildout




