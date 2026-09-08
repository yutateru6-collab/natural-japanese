# SOURCES.md

`note-writing` は、ユーザー独自のnote編集方針を中心に、複数の公開Agent Skill / writing skillから有効な設計思想を選別して再設計した独自統合スキルです。

本文やルールを単純連結したものではありません。
媒体、文体、ユーザーの好みに合わない規則は意図的に採用していません。

## 1. ユーザー独自のnote編集方針

基礎になったもの:

- タイトル候補3案
- 冒頭3行3案
- 1499字以内を既定
- 生活感、違和感、自虐、少し笑える比喩
- きれいな教訓にしすぎない
- 太字は「変な芯」へ
- ハッシュタグ5〜7
- 関連記事導線
- 見出し画像3案と生成プロンプト
- 実在しない体験・台詞・関連記事を作らない

この方針が最上位の編集思想です。

## 2. coji/natural-japanese

Repository:
https://github.com/coji/natural-japanese

License: MIT

採用した考え方:

- 文単位の自然さと記事構成を分けて扱う
- 語順、主述、読点、直訳調を独立して点検する
- 生成時制約と事後レビューを分ける
- style-profileでユーザー固有の文体を上書きする

このForkではさらに、root `style-profile.md` に読点少なめのユーザー設定を追加済みです。

## 3. AgriciDaniel/claude-blog

Repository:
https://github.com/AgriciDaniel/claude-blog

License: MIT

参考にしたもの:

- 執筆前のbrief / outline
- 書いた後の品質ゲート
- author voice profileを別レイヤーにする設計
- fact-checkを独立工程にする考え方
- タイトル、SEO、画像、監査をモジュール化する設計
- 「ユーザーを最初のレビュー担当にしない」という品質思想

採用しなかったもの:

- 2000〜2500語を既定とする長文SEOブログ設計
- 全記事への大量統計、FAQ、Key Takeaways、schema、チャートの強制
- Google/AI citation最適化を記事の中心目標に置くこと

noteの短いエッセイや個人記事には過剰なためです。

## 4. j1nn0/skills

Repository:
https://github.com/j1nn0/skills

License: MIT

主に参考にしたskill:

- `blog-writing-guide-ja`
- `blog-idea-grilling`
- `writing-ja`
- `fact-check-ja`
- `blog-ops`

参考にしたもの:

- 「記事の企画・構成」と「文レベルの推敲」を分離する
- 書く前に企画の芯を決める
- 読者の疑問順で構成する
- 節の厚みを均等にしない
- 書き手の声を本文全体へ通す
- SEO目的だけの定義節・FAQを追加しない
- 事実確認を別工程へ切り出す

技術ブログ固有の規則は、一般note記事には持ち込んでいません。

## 5. iKora128/stop-ai-slop-jp

Repository:
https://github.com/iKora128/stop-ai-slop-jp

License: MIT

参考にしたもの:

- AI臭を単語リストだけでなく「書き手の不在」として捉える
- 抽象語、壮大化、均一なリズムを疑う
- 二項対比の反復を避ける
- 全段落を同じ型で着地させない
- ユーザーの自虐、皮肉、中間温度を過度に消さない
- 横文字メタファーやAI偏愛語を文脈なしに撒かない

そのまま採用しなかったもの:

- 特定の見出し型を一律禁止すること
- 語彙を単語単位で全面禁止すること
- 伝聞表現を機械的に増やすこと
- 「毒」を人間らしさの必須条件にすること

ユーザーの文章ではユーモアと自虐は残しますが、攻撃性を人工的に追加しません。

## 6. igapyon/igapyon-agent-skills

Repository:
https://github.com/igapyon/igapyon-agent-skills

License: Apache-2.0

主に参考にしたskill:

- `igapyon-note-writer`

参考にしたもの:

- noteという媒体に合わせて本文と掲載情報を分ける
- ハッシュタグ、公開情報、関連記事等を捏造しない
- 1文1段落を機械的な標準にしない
- note向け画像工程を本文執筆と分ける

同skill固有の「みくく」文体や技術エッセイ運用は採用していません。

## 統合時の判断基準

採用条件は次の3つ。

1. ユーザーのnote記事に実際に効く
2. 既存のユーザー文体を薄めない
3. ハルシネーションや過剰最適化のリスクを下げる

機能が高度でも、この3条件を満たさないものは採用しません。

## ライセンス

この `note-writing` ディレクトリ内の新規文章は独自に再構成したものです。
公開リポジトリから大きな文章ブロックをコピーするのではなく、設計上の考え方を参考にしています。

参考元のライセンス:

- coji/natural-japanese: MIT
- AgriciDaniel/claude-blog: MIT
- j1nn0/skills: MIT
- iKora128/stop-ai-slop-jp: MIT
- igapyon/igapyon-agent-skills: Apache-2.0

元リポジトリの著作権・ライセンスは各プロジェクトに帰属します。
