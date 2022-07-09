

set -ex



python run_py_test.py
if [[ $($PYTHON -c 'import cv2; print(cv2.__version__)') != $PKG_VERSION ]]; then exit 1; fi
python -c "import cv2, re; assert re.search('Lapack:\s+YES', cv2.getBuildInformation())"
pip list
test $(pip list | grep opencv-python | wc -l) -eq 1
exit 0
