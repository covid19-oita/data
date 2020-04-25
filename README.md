# 大分県 新型コロナウイルス感染症対策サイト用のデータ

Issues にあるいろいろな修正にご協力いただけると嬉しいです。

## ライセンス

本ソフトウェアは、[MITライセンス](./LICENSE.txt)の元提供されています。

## 開発者向け情報

### 開発環境

- Python3.7.x

### 基本的なブランチ

| 目的 | ブランチ | 確認URL | 備考 |
| ---- | -------- | ---- | ---- |
| 本番 | master | https://data-covid19-oita.netlify.app/ | base branch。こちらにPull Requestを送ってください |

master が更新されると、`/json` 配下のファイルが確認URLにホスティングされます。

例) https://data-covid19-oita.netlify.app/data.json
