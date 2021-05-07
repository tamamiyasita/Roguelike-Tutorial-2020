import sys
import logging
import logging.handlers
import logging.config

# ルートロガーの作成　ログレベルはdebug
_root_logger = logging.getLogger("")
_root_logger.setLevel(logging.DEBUG)

# Formatterの作成(時刻、ログレベル、モジュール名、関数名、行番号：logメッセージ を出力)
_simpleFormatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-7s %(module)-13s %(funcName)-6s %(lineno)4s: %(message)s")

# コンソール用ハンドラの作成。　標準出力へ出力、　ログレベル＝debug, 書式は上記と同じ
_consoleHandler = logging.StreamHandler(sys.stdout)
_consoleHandler.setLevel(logging.DEBUG)
_consoleHandler.setFormatter(_simpleFormatter)

# コンソール用ハンドラをルートロガーに追加
_root_logger.addHandler(_consoleHandler)

# ファイル用ハンドラの作成、ファイル名はlogging_log ログレベルはinfo ファイルサイズは1MB、バックアップfileは2こ、ｴﾝｺｰﾃﾞｨﾝｸﾞはutf-8
_fileHandler = logging.handlers.RotatingFileHandler(
    filename="logging_log", maxBytes=1000000, backupCount=2, encoding="utf-8")

_fileHandler.setLevel(logging.INFO)
_fileHandler.setFormatter(_simpleFormatter)

# ファイル用ハンドラをルートロガーに追加
_root_logger.addHandler(_fileHandler)
