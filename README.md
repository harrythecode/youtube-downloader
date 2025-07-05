# YouTube Downloader

A simple tool to download YouTube videos and audio with a multi-language (English/Japanese) user interface.

### Features

- **Multi-language Support**: Automatically switches between English and Japanese based on your system's language settings.
- **Interactive Menu**: Simple, menu-based operation to guide you through the process.
- **Format Selection**: Allows you to choose the desired format and quality before downloading.
- **Testable**: Includes a basic test suite for checking core functionality.

### Directory Structure

```
.
├── youtube-scraper.py      # Main application script
├── requirements.txt        # Project dependencies
├── locales/                # Translation files (for i18n)
│   └── ja/LC_MESSAGES/
├── test/                   # Test code
│   └── test_main.py
└── downloads/              # Default directory for downloaded files
```

### Usage

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Script**
    ```bash
    python youtube-scraper.py
    ```
    The script will launch and display instructions in either English or Japanese.

### How to Test

To run the automated tests locally or in a CI/CD environment:
```bash
python test/test_main.py
```

### License

This project is licensed under the **MIT License**.

---
---

# YouTube ダウンローダー

シンプルな対話形式でYouTubeの動画や音声をダウンロードするツールです。日本語と英語のUIに対応しています。

### 特徴

- **多言語対応**: お使いのシステムの言語設定に応じて、UIが自動で日本語と英語に切り替わります。
- **対話式メニュー**: 分かりやすいメニュー形式で操作をガイドします。
- **フォーマット選択**: ダウンロード前に、希望のファイル形式や品質を選択できます。
- **テスト可能**: 主要な機能を確認するための基本的なテストコードが含まれています。

### ディレクトリ構成

```
.
├── youtube-scraper.py      # メインアプリケーション
├── requirements.txt        # 依存ライブラリ
├── locales/                # 翻訳ファイル (国際化対応)
│   └── ja/LC_MESSAGES/
├── test/                   # テストコード
│   └── test_main.py
└── downloads/              # ダウンロードファイルの保存先
```

### 使い方

1.  **依存ライブラリのインストール**
    ```bash
    pip install -r requirements.txt
    ```

2.  **スクリプトの実行**
    ```bash
    python youtube-scraper.py
    ```
    スクリプトが起動し、システムの言語に応じて日本語または英語で案内が表示されます。

### テストの実行方法

ローカル環境やCI/CD環境で自動テストを実行する場合：
```bash
python test/test_main.py
```

### ライセンス

このプロジェクトは **MITライセンス** のもとで公開されています。