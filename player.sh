#!/bin/bash

PlayMyVDI_DIR="absolute/path/to/playMyVDI"
export CITRIX_URL="actual.url"
export CITRIX_USERNAME="firstname.lastname@company.com"
export CITRIX_PASSWORD="password"

echo "Python Version -- Check"
PMVDI_PY_VER=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$PMVDI_PY_VER" -lt "36" ]; then
  echo "\tFAIL"
  echo "playMyVDI requires python 3.6 or greater"
  exit 1
else
  echo "\tPASS"
fi

echo "Python Environment -- Check"
if test -f "$PlayMyVDI_DIR/mypy/bin/activate"; then
  echo "\tPASS"
else
  echo "\tFAIL"

  echo "\tplayMyVDI doesn't have it's environment configured"
  echo "\tEnvironment -- Setup"
  cd $PlayMyVDI_DIR
  python3 -m venv mypy
  pip install --upgrade pip
  echo "\t\tPASS"

  echo "\tRequirements -- Install"
  pip install selenium -y
  echo "\t\tPASS"

  echo "\tCreating the alias"
  export ALIAS_COMMAND="sh $PlayMyVDI_DIR/player.sh"
  echo "alias myvdi=$ALIAS_COMMAND" >~/Users/$USER/.bashrc
fi

echo "Chromium Driver -- Check"
if test -f "$PlayMyVDI_DIR/chromedriver"; then
  echo "\tPASS"
else
  echo "\tFAIL"
  echo "\tplayMyVDI doesn't have chromedriver to automate interactions"
  echo "\tChromedriver -- Download"
  cd $PlayMyVDI_DIR
  curl https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_mac64.zip -o $PlayMyVDI_DIR/chromedriver_mac64.zip
  unzip -d $PlayMyVDI_DIR $PlayMyVDI_DIR/chromedriver_mac64.zip
  rm $PlayMyVDI_DIR/chromedriver_mac64.zip
  echo "\t\tPASS"
fi

export PATH=$PATH:"$PlayMyVDI_DIR/chromedriver"
python3 $PlayMyVDI_DIR/src/driver.py
