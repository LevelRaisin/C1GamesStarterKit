cd /Users/raymond/c1/C1GamesStarterKit
rm submit.zip
mkdir compile_134789
cp -r $1 compile_134789/python-algo
cd compile_134789
zip -r ../submit.zip python-algo -x "*__pycache__*" -x "*errorFile*"
cd ..
rm -r compile_134789

