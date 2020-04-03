# 大分県 新型コロナウイルス感染症対策サイト用のデータ

## 貢献の仕方

Issues にあるいろいろな修正にご協力いただけると嬉しいです。

## ライセンス

本ソフトウェアは、[MITライセンス](./LICENSE.txt)の元提供されています。

# 開発者向け情報

## 環境構築の手順

- Python3.7.x


## development以外は Pull Request は禁止です。

#### 基本的なブランチ
| 目的 | ブランチ | 確認URL | 備考 |
| ---- | -------- | ---- | ---- |
| 開発 | development | https://dev-data-covid19-oita.netlify.com/data.json | base branch。基本はこちらに Pull Requestを送ってください |
| 本番 | master | https://data-covid19-oita.netlify.com/data.json | 管理者以外の Pull Request は禁止です |

#### システムで利用しているブランチ
| 目的 | ブランチ | 確認URL | 備考 |
| ---- | -------- | ---- | ---- |
| 本番サイト | production | https://data-covid19-oita.netlify.com/data.json | サイトで使用されるデータのURL |