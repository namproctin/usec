#! /usr/bin/env bash

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
reset=`tput sgr0`

VERSION='0.0.1'
TEMP_DIR=$(pwd)/crawl
LEVEL=1


type wget >/dev/null 2>&1 || {
  echo "${red}x${reset} we use wget to download websites"
  echo "Please install wget"
  exit 1
}

usage(){
  echo "Usage: ./script.sh [options] <URL> <TEXT>"
  echo ""
  echo "Options:"
  echo "  -l, --level           specify recursion maximum depth level depth."
  echo "  -v, --version         show program version and exit"
}


version(){
  echo $VERSION
}

# Convert known long options to short options
for arg in "$@"; do
  shift
  case "$arg" in
    --help)
      set -- "$@" "-h"
      ;;
    --version)
      set -- "$@" "-v"
      ;;
    --level)
      set -- "$@" "-l"
      ;;
    *)
      set -- "$@" "$arg"
      ;;
  esac
done

# Process option flags
while getopts "hvl:" opt; do
  case $opt in
    h )
      usage
      exit 0
      ;;
    v )
      version
      exit 0
      ;;
    l )
      if [[ ! $OPTARG =~ ^[0-9]+$ ]]; then
        echo "Invalid argument for --level: ${OPTARG}"
        echo "Please enter a number instead"
        exit 1
      fi
      LEVEL="$OPTARG"
      ;;
    * )
      usage
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# show help if run without arguments
if [ $# -ne 2 ]; then
  usage
  exit 0
fi

URL=$1
TEXT=$2


# clean out temporary directory
mkdir -p $TEMP_DIR
rm -rf $TEMP_DIR/*


echo "${green} >>> ${reset} using wget to mirror site"
# wget params
# -k correct links to absolute links
# --flow-tags only follow link from a tag
# -l depth
cd $TEMP_DIR
wget -m -k --follow-tags=a -l$LEVEL $URL 2>&1 | grep '^--' --line-buffered | awk '{print "Downloading... "$3}'
grep -R $TEXT .


# clean up
echo "${green} >>> ${reset} cleaning up"
rm -rf $TEMP_DIR
