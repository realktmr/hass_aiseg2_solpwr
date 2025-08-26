# Panasonic AiSEG2 Solar Power Monitor for Home Assistant

このプログラムはchatGPTによって作成しております。
作者自身はプログラムに詳しくなく自身で動作確認をしているのみです。



用途そしては、現在の太陽光発電量と消費電力量を取得して発電余力を算出します。
発電余力がある時に電池の充電やその他機器の使用を行えるようにスマートスイッチと組み合わせて使うことを想定しています。



## インストール方法

マニュアルインストールにみ対応です。
一連のファイルをzipでダウンロードして、Home Assisstantのconfigディレクトリにある（なければ作る）、custom\_componentsディレクトリに
custom\_components/hass\_aise2\_powerをそのままコピーして Home Assistantを再起動すれば「統合追加」でAiSEG2というデバイスを追加してください。
必要なhost、username、passwordを入力すれば、動き始めるはずです。



## 動作確認環境

動作確認は以下の環境で行っています。

Panasonic AiSEG2(MKN704)： ファームウェア Ver.2.97I-03

Home Assistant ：UGREEN NASync アプリセンター 1.1.0.0004  (Home Assistant Container core 2025.5.3)





## 参考

他にAiSEGから情報を取り出すHome Assistant用カスタムコンポーネントは以下のようなものがあるようです。



・hiroaki0923さんのaiseg2-brige：各回路の日次の電力積算情報を取得してHome Assistantのエネルギー管理に使えるコンポーネント。（私も使わせていただいて頂いております）

　https://github.com/hiroaki0923/aiseg2-bridge



・banban525さんのechonetlite2mqtt：こちらは機器操作を目的にしたコンポーネントのようです。（私は使ってません）

 https://github.com/banban525/echonetlite2mqtt

