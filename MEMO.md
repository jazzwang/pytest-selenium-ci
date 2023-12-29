[TOC]

# 2023-12-29

## Goal: create a lab for running Selenium with PyTest using Github Actions and Gitlab CI

- ( 2023-12-29 15:45 )
- Learn new skills:
    - PyTest
        - https://docs.pytest.org/en/stable/
    - pipx
        - https://github.com/pypa/pipx
        - https://pipx.pypa.io/stable/
    - Poetry
        - https://python-poetry.org/

## Sub-Goal: Github Action

* ( 2023-12-29 15:42 )
* Reference: 
    - https://dev.to/delrayo/executing-selenium-test-with-pythonpytest-using-github-actions-317c
    - https://dev.to/iamibi/add-coverage-report-with-pytest-and-gitlab-ci-3e9p
* ( 2023-12-29 15:48 )
* Test with Github CodeSpace
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ cd /tmp
@jazzwang ➜ /tmp $ wget https://raw.githubusercontent.com/dylanaraps/neofetch/master/neofetch
@jazzwang ➜ /tmp $ chmod a+x neofetch 
@jazzwang ➜ /tmp $ ./neofetch 
            .-/+oossssoo+\-.               codespace@codespaces-ad2973 
        ´:+ssssssssssssssssss+:`           --------------------------- 
      -+ssssssssssssssssssyyssss+-         OS: Ubuntu 20.04.6 LTS x86_64 
    .ossssssssssssssssssdMMMNysssso.       Host: Microsoft Corporation Virtual Machine 
   /ssssssssssshdmmNNmmyNMMMMhssssss\      Kernel: 6.2.0-1018-azure 
  +ssssssssshmydMMMMMMMNddddyssssssss+     Uptime: 24 mins 
 /sssssssshNMMMyhhyyyyhmNMMMNhssssssss\    Packages: 628 (dpkg) 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Shell: bash 5.0.17 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   Terminal: vscode 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   CPU: AMD EPYC 7763 (2) @ 3.241GHz 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   Memory: 1905MiB / 7929MiB 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+
.ssssssssdMMMNhsssssssssshNMMMdssssssss.                           
 \sssssssshNMMMyhhyyyyhdNMMMNhssssssss/                            
  +sssssssssdmydMMMMMMMMddddyssssssss+
   \ssssssssssshdmNNNNmyNMMMMhssssss/
    .ossssssssssssssssssdMMMNysssso.
      -+sssssssssssssssssyyyssss+-
        `:+ssssssssssssssssss+:`
            .-\+oossssoo+/-.
```
* let's start with installing pipx and poetry
* ( 2023-12-29 16:03 )
* saw multiple warning:
```bash
  WARNING: The script pkginfo is installed in '/usr/local/python/3.10.13/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```
* this should be because of the symbolic links of Github codespace `~/.python` folder and PATH environment variable setting
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ python -V
Python 3.10.13
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ whoami 
codespace
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ which python3
/home/codespace/.python/current/bin/python3
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ ls -alh /usr/local/python/
total 32K
drwxrwsr-x 1 codespace python 4.0K Dec  8 04:58 .
drwxr-xr-x 1 root      root   4.0K Dec  8 04:59 ..
drwxrwsr-x 1 codespace python 4.0K Dec  8 04:58 3.10.13
drwxrwsr-x 1 codespace python 4.0K Dec  8 04:59 3.9.18
lrwxrwxrwx 1 codespace python    7 Dec  8 04:58 current -> 3.10.13
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ ls -al /home/codespace/.python
total 12
drwxrwsr-x 2 codespace codespace 4096 Dec  8 05:02 .
drwxrwsr-x 1 codespace codespace 4096 Dec 29 15:54 ..
lrwxrwxrwx 1 codespace codespace   25 Dec  8 05:02 current -> /usr/local/python/current
```
* supress the warning by adding the PATH environment variable
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ export PATH=$PATH:/usr/local/python/3.10.13/bin
```
* ( 2023-12-29 16:08 )
* Initialize the current project with poetry using
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ poetry init

This command will guide you through creating your pyproject.toml config.

Package name [pytest-selenium-ci]:  
Version [0.1.0]:  
Description []:  Lab for running Selenium with PyTest using Github Actions and Gitlab CI
Author [Jazz Yao-Tsung Wang <jazzwang@users.noreply.github.com>, n to skip]:  
License []:  APL-2.0
Compatible Python versions [^3.10]:  

Would you like to define your main dependencies interactively? (yes/no) [yes] 
You can specify a package in the following forms:
  - A single name (requests): this will search for matches on PyPI
  - A name and a constraint (requests@^2.23.0)
  - A git url (git+https://github.com/python-poetry/poetry.git)
  - A git url with a revision (git+https://github.com/python-poetry/poetry.git#develop)
  - A file path (../my-package/my-package.whl)
  - A directory (../my-package/)
  - A url (https://example.com/packages/my-package-0.1.0.tar.gz)

Package to add or search for (leave blank to skip): pytest
Found 20 packages matching pytest
Showing the first 10 matches

Enter package # to add, or the complete package name if it is not listed []:
 [ 0] pytest
 [ 1] pytest123
 [ 2] 131228_pytest_1
 [ 3] pytest-pingguo-pytest-plugin
 [ 4] pytest-collect-pytest-interinfo
 [ 5] pytest-symbols
 [ 6] pytest-circleci
 [ 7] exgrex-pytest
 [ 8] pytest-pythonpath
 [ 9] pytest-faker
 [ 10] 
 > 0
Enter the version constraint to require (or leave blank to use the latest version): 
Using version ^7.4.3 for pytest

Add a package (leave blank to skip): coverage
Found 20 packages matching coverage
Showing the first 10 matches

Enter package # to add, or the complete package name if it is not listed []:
 [ 0] coverage
 [ 1] coverage-lcov
 [ 2] tester_coverage
 [ 3] esg-coverage
 [ 4] plot-coverage
 [ 5] coverage-fixpaths
 [ 6] mkdocs-coverage
 [ 7] moon-coverage
 [ 8] sequana-coverage
 [ 9] coverage2img
 [ 10] 
 > 0
Enter the version constraint to require (or leave blank to use the latest version): 
Using version ^7.4.0 for coverage

Add a package (leave blank to skip): 

Would you like to define your development dependencies interactively? (yes/no) [yes] 
Package to add or search for (leave blank to skip): 

Generated file

[tool.poetry]
name = "pytest-selenium-ci"
version = "0.1.0"
description = "Lab for running Selenium with PyTest using Github Actions and Gitlab CI"
authors = ["Jazz Yao-Tsung Wang <jazzwang@users.noreply.github.com>"]
license = "APL-2.0"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
pytest = "^7.4.3"
coverage = "^7.4.0"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


Do you confirm generation? (yes/no) [yes]
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ tree
.
├── LICENSE
├── MEMO.md
├── README.md
└── pyproject.toml

0 directories, 4 files
```
* ( 2023-12-29 16:31 )
* add `selenium` and `webdriver-manager`
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ poetry add selenium
Using version ^4.16.0 for selenium

Updating dependencies
Resolving dependencies... (0.7s)

Package operations: 13 installs, 0 updates, 0 removals

  • Installing attrs (23.1.0)
  • Installing h11 (0.14.0)
  • Installing idna (3.6)
  • Installing outcome (1.3.0.post0)
  • Installing sniffio (1.3.0)
  • Installing sortedcontainers (2.4.0)
  • Installing pysocks (1.7.1)
  • Installing trio (0.23.2)
  • Installing wsproto (1.2.0)
  • Installing certifi (2023.11.17)
  • Installing trio-websocket (0.11.1)
  • Installing urllib3 (2.1.0)
  • Installing selenium (4.16.0)

Writing lock file
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ poetry add webdriver-manager
Using version ^4.0.1 for webdriver-manager

Updating dependencies
Resolving dependencies... (0.5s)

Package operations: 4 installs, 0 updates, 0 removals

  • Installing charset-normalizer (3.3.2)
  • Installing python-dotenv (1.0.0)
  • Installing requests (2.31.0)
  • Installing webdriver-manager (4.0.1)

Writing lock file
```
* ( 2023-12-29 16:32 )
* add `conftest.py` for PyTest
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ cat > conftest.py << EOF
import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium import webdriver


@pytest.fixture()
def setup(request):
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())

    chrome_options = Options()
    options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
    for option in options:
        chrome_options.add_argument(option)

    request.cls.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


    yield request.cls.driver
    request.cls.driver.close()
EOF
```
* ( 2023-12-29 16:39 )
* create `test_web01.py` for PyTest
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ cat > test_web01.py << EOF
import pytest

@pytest.mark.usefixtures("setup")
class TestExampleOne:
    def test_title(self):
        self.driver.get('https://www.delrayo.tech')
        assert self.driver.title == "DelRayo.tech - Delrayo Tech"

    def test_title_blog(self):
        self.driver.get('https://www.delrayo.tech/blog')
        print(self.driver.title)

EOF
```
* create `.github/workflows/test01.yaml` for Github Action
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ mkdir -p .github/workflows/
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ cat > .github/workflows/test01.yaml << EOF
# .github/workflows/test01.yaml
name: test01
on:
  workflow_dispatch:  
jobs:
  test01:
    runs-on: ubuntu-latest
    steps:
      - name: Check out this repo
        uses: actions/checkout@v2
     #Setup Python   
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install software
        run: sudo apt-get install -y chromium-browser
      - name: Install the necessary packages
        run: pip install requests webdriver-manager selenium pytest
      - name: Run the PytTest script
        run: pytest -rA
EOF
```
* ( 2023-12-29 16:51 )
* test run :P
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ pip install requests webdriver-manager selenium pytest
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ sudo apt-get update
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ sudo apt-get install -y chromium-browser
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ pytest -rA
ImportError while loading conftest '/workspaces/pytest-selenium-ci/conftest.py'.
conftest.py:5: in <module>
    from webdriver_manager.utils import ChromeType
E   ModuleNotFoundError: No module named 'webdriver_manager.utils'
```
* ( 2023-12-29 16:52 )
* OK. I need to tune the conftest.py
* Let's add source code as 1st draft commit
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ git add .github/ conftest.py test_web01.py pyproject.toml MEMO.md 
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ git commit -m "draft commit"
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ git push
```
* ( 2023-12-29 17:02 )
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ code conftest.py 
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ git diff conftest.py
diff --git a/conftest.py b/conftest.py
index 2eebcff..901c18e 100644
--- a/conftest.py
+++ b/conftest.py
@@ -1,16 +1,14 @@
 import pytest
+from selenium import webdriver
 from selenium.webdriver.chrome.options import Options
-from selenium.webdriver.chrome.service import Service
+from selenium.webdriver.chrome.service import Service as ChromeService
 from webdriver_manager.chrome import ChromeDriverManager
-from webdriver_manager.utils import ChromeType
-from selenium import webdriver
-
 
 @pytest.fixture()
 def setup(request):
-    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
+    chrome_service = ChromeService(ChromeDriverManager().install())
 
-    chrome_options = Options()
+    chrome_options = webdriver.ChromeOptions()
     options = [
     "--headless",
     "--disable-gpu",
```
* ( 2023-12-29 17:07 )
* 2nd test run
```bash
@jazzwang ➜ /workspaces/pytest-selenium-ci (main) $ pytest -rA
====================================================================================== test session starts ======================================================================================
platform linux -- Python 3.10.13, pytest-7.4.3, pluggy-1.3.0
rootdir: /workspaces/pytest-selenium-ci
plugins: anyio-4.1.0
collected 2 items                                                                                                                                                                               

test_web01.py EE                                                                                                                                                                          [100%]

============================================================================================ ERRORS =============================================================================================
__________________________________________________________________________ ERROR at setup of TestExampleOne.test_title __________________________________________________________________________

request = <SubRequest 'setup' for <Function test_title>>

    @pytest.fixture()
    def setup(request):
>       chrome_service = ChromeService(ChromeDriverManager().install())

conftest.py:9: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/chrome.py:40: in install
    driver_path = self._get_driver_binary_path(self.driver)
/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/core/manager.py:40: in _get_driver_binary_path
    file = self._download_manager.download_file(driver.get_driver_download_url(os_type))
/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/drivers/chrome.py:32: in get_driver_download_url
    driver_version_to_download = self.get_driver_version_to_download()
/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/core/driver.py:48: in get_driver_version_to_download
    return self.get_latest_release_version()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <webdriver_manager.drivers.chrome.ChromeDriver object at 0x7f53c2fb1cf0>

    def get_latest_release_version(self):
        determined_browser_version = self.get_browser_version_from_os()
        log(f"Get LATEST {self._name} version for {self._browser_type}")
        if determined_browser_version is not None and version.parse(determined_browser_version) >= version.parse("115"):
            url = "https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build.json"
            response = self._http_client.get(url)
            response_dict = json.loads(response.text)
            determined_browser_version = response_dict.get("builds").get(determined_browser_version).get("version")
            return determined_browser_version
        # Remove the build version (the last segment) from determined_browser_version for version < 113
>       determined_browser_version = ".".join(determined_browser_version.split(".")[:3])
E       AttributeError: 'NoneType' object has no attribute 'split'

/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/drivers/chrome.py:64: AttributeError
------------------------------------------------------------------------------------- Captured stderr setup -------------------------------------------------------------------------------------
/bin/sh: 1: google-chrome: not found
/bin/sh: 1: google-chrome-stable: not found
/bin/sh: 1: google-chrome-beta: not found
/bin/sh: 1: google-chrome-dev: not found
/bin/sh: 1: google-chrome: not found
/bin/sh: 1: google-chrome-stable: not found
/bin/sh: 1: google-chrome-beta: not found
/bin/sh: 1: google-chrome-dev: not found
_______________________________________________________________________ ERROR at setup of TestExampleOne.test_title_blog ________________________________________________________________________

request = <SubRequest 'setup' for <Function test_title_blog>>

    @pytest.fixture()
    def setup(request):
>       chrome_service = ChromeService(ChromeDriverManager().install())

conftest.py:9: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/chrome.py:40: in install
    driver_path = self._get_driver_binary_path(self.driver)
/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/core/manager.py:40: in _get_driver_binary_path
    file = self._download_manager.download_file(driver.get_driver_download_url(os_type))
/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/drivers/chrome.py:32: in get_driver_download_url
    driver_version_to_download = self.get_driver_version_to_download()
/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/core/driver.py:48: in get_driver_version_to_download
    return self.get_latest_release_version()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <webdriver_manager.drivers.chrome.ChromeDriver object at 0x7f53c2fb1bd0>

    def get_latest_release_version(self):
        determined_browser_version = self.get_browser_version_from_os()
        log(f"Get LATEST {self._name} version for {self._browser_type}")
        if determined_browser_version is not None and version.parse(determined_browser_version) >= version.parse("115"):
            url = "https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build.json"
            response = self._http_client.get(url)
            response_dict = json.loads(response.text)
            determined_browser_version = response_dict.get("builds").get(determined_browser_version).get("version")
            return determined_browser_version
        # Remove the build version (the last segment) from determined_browser_version for version < 113
>       determined_browser_version = ".".join(determined_browser_version.split(".")[:3])
E       AttributeError: 'NoneType' object has no attribute 'split'

/usr/local/python/3.10.13/lib/python3.10/site-packages/webdriver_manager/drivers/chrome.py:64: AttributeError
------------------------------------------------------------------------------------- Captured stderr setup -------------------------------------------------------------------------------------
/bin/sh: 1: google-chrome: not found
/bin/sh: 1: google-chrome-stable: not found
/bin/sh: 1: google-chrome-beta: not found
/bin/sh: 1: google-chrome-dev: not found
/bin/sh: 1: google-chrome: not found
/bin/sh: 1: google-chrome-stable: not found
/bin/sh: 1: google-chrome-beta: not found
/bin/sh: 1: google-chrome-dev: not found
==================================================================================== short test summary info ====================================================================================
ERROR test_web01.py::TestExampleOne::test_title - AttributeError: 'NoneType' object has no attribute 'split'
ERROR test_web01.py::TestExampleOne::test_title_blog - AttributeError: 'NoneType' object has no attribute 'split'
======================================================================================= 2 errors in 0.24s =======================================================================================
```
* ( 2023-12-29 17:08 )
* it means that I should modify the selenium webdriver for `chromium-browser`