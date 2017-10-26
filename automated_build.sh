# clone pages repo
# cd /tmp
# git clone git@github.com:cornelltech/events.git/ build

# rebuild page
# cd build
# cd events

python contentful_data_importer.py # write new data to files
export PYTHONIOENCODING=utf-8
python build_site.py > docs/index.html

# push newly built repo
git config --global user.email "rachel.sobel@cornell.edu"
git config --global user.name "Rachel Sobel"

git add docs/
git commit -m "Automated rebuild on update"
git push origin master
