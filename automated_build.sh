# clone pages repo
cd /tmp
git clone https://github.com/cornelltech/events/ build

# rebuild page
cd /tmp/build
python freezer.py

# push newly built repo
git config --global user.email "rachel.sobel@cornell.edu"
git config --global user.name "Rachel Sobel"

git add docs/
git commit -m "Automated rebuild on update"
git push
