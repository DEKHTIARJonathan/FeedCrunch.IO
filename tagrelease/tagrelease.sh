#!/bin/sh

echo "CREATE GIT TAG"
echo "$TRAVIS_BRANCH"
echo "$TRAVIS_BUILD_NUMBER"
echo "$TRAVIS_REPO_SLUG"
git config --global user.email "contact@jonathandekhtiar.eu"
git config --global user.name "DEKHTIAR Jonathan - via Travis CI"
TAG_DATE=$(date -u "+%Y-%m-%d")
export GIT_TAG="build-$TRAVIS_BRANCH-$TAG_DATE-$TRAVIS_BUILD_NUMBER"
git tag $GIT_TAG -a -m "Generated tag from TravisCI build $TRAVIS_BUILD_NUMBER"
echo "TravisCI build tagged with $GIT_TAG"
export RELEASE_URL="https://github.com/$TRAVIS_REPO_SLUG/releases/download/$GIT_TAG/$ARTIFACT_NAME"
echo "Set URL to $RELEASE_URL"
