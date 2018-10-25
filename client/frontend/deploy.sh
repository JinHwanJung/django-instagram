#!/usr/bin/env bash
# create react-app
# https://github.com/facebook/create-react-app
yarn create react-app my-app

# scass
yarn add sass-loader node-sass

# eslint
npm install -g eslint
eslint --lnit  ## 일단은 popular guid 에서 선택
# https://eslint.org/docs/user-guide/configuring (린트설정 참고)
## 추가로 아래도 설치해서 WebStom (preference -> Languges & Framework -> ESLint) 에 연결
sudo npm install eslint-plugin-react eslint-plugin-jsx-a11y eslint-plugin-import -g
sudo npm install -g eslint-config-airbnb
sudo npm install -g eslint-config-standard
sudo npm install -g eslint-plugin-node
sudo npm install -g eslint-plugin-promise
sudo npm install -g eslint-plugin-standard
