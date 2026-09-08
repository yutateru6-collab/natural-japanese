# SOURCES.md

`x-writing` は、このForkの `style-profile.md` と `natural-japanese` を最上位に置きつつ、公開されているSNS/X向けAgent Skillの設計思想を選別して再設計した独自統合スキルです。

外部スキルをそのまま連結・コピーしたものではありません。
Xのアルゴリズムやエンゲージメントに関する時限性の高い主張は、文章品質の恒久ルールへ入れていません。

## 1. このFork独自の方針

最優先で守るもの:

- 読点を増やしすぎない
- 少しくだけた自然な日本語
- 自虐やしょうもないユーモアを必要な場所だけ残す
- note本文の単なる短縮版にしない
- 元素材にない体験、数字、実績、会話を作らない
- 煽りを本文より強くしない
- きれいな教訓やCTAを毎回足さない
- note記事作成時はX投稿案もセットで出せる

この方針が外部スキルより上位です。

## 2. sergebulaev/x-skills

Repository:
https://github.com/sergebulaev/x-skills

License: MIT

主に参考にしたskill:

- `x-repurposer`
- `x-hook-extractor`
- `x-humanizer`
- `x-post-writer`
- `x-thread-builder`

採用した考え方:

- 再利用はコピー&短縮ではなく、元素材の「芯」を抜いて媒体向けに再構成する
- 元媒体固有の前置き、CTA、ハッシュタグ壁などを外す
- 一つの主張・体験・数字を一投稿の中心にする
- フックは外から貼るのではなく、元素材の強い要素から作る
- 他人の成功投稿からは表現ではなく構造を抽出する
- Humanizerは意味と本人の声を守り、過剰修正を避ける
- スレッドに人工的な“パンチ投稿”を挟まない

採用しなかったもの:

- 「2026アルゴリズムではこの型が有利」とする固定ルール
- 独自コーパスの倍率やエンゲージメント数値を恒久ルールにすること
- 外部リンクを常に本文から外すなどの一律ルール
- 特定語、記号、構造を単発出現だけで全面禁止すること
- Publora等の投稿ツール固有ワークフロー

理由:
アルゴリズム、UI、利用者行動は変化し、独自計測値をこちらで再現検証できないため。文章品質と事実性に直接効く設計だけ残した。

## 3. social-media-skills/skills

Repository:
https://github.com/social-media-skills/skills

License: MIT

主に参考にしたskill:

- `voice-builder`
- `hook-writer`
- `text-post-and-microblog`

採用した考え方:

- 声は「親しみやすい」などの形容詞ではなく、実際の文章サンプルから再現可能な規則として抽出する
- 語彙、構文、修辞、構成、姿勢、negative spaceを分けて見る
- サンプルが少なければ低信頼度として扱い、人格を捏造しない
- フックは本文の真実から掘り出し、本文が回収できる約束だけをする
- 一つの投稿では一つの中心アイデアへ絞る
- 過剰装飾、エンゲージメントベイト、AI的な定型フォーマットを避ける

採用しなかったもの:

- 「白余白で読了時間が○%上がる」など外部数値を固定ルールにすること
- 特定プラットフォームの最適文字数を恒久化すること
- WoopSocial等の投稿サービス固有ワークフロー
- 毎投稿で返信を促すことを必須化する設計

## 4. 統合時の判断基準

採用条件:

1. 元素材の意味と事実を守る
2. このユーザーの日本語の声を薄めない
3. note→Xの再利用に実際に効く
4. Xの仕様変更に弱い一時的ノウハウではない
5. 誤情報、誇張、AI臭を増やさない

この5条件を満たさないルールは、高度そうでも採用しない。

## 5. ファイル構成

- `SKILL.md` — ルーティングと全体工程だけ
- `references/hooks.md` — フック抽出・比較・選択
- `references/repurpose.md` — note/長文からXへの再構成
- `references/voice-and-humanizer.md` — 本人の声と過剰修正防止
- `references/threads.md` — スレッドの判断と構成
- `references/audit.md` — 公開前のBlocker/Warning監査

一つのルールを複数ファイルへ重複記載しないことを原則とする。

## 6. ライセンス

この `x-writing` ディレクトリ内の文章は、公開リポジトリから大きな文章ブロックをコピーせず、参考にした設計思想を日本語X運用向けに再構成しています。

参考元:

- sergebulaev/x-skills — MIT License, Copyright (c) 2026 Sergey Bulaev
- social-media-skills/skills — MIT License, Copyright (c) 2026 Frank Heijdenrijk

元リポジトリの著作権とライセンスは各プロジェクトに帰属します。
