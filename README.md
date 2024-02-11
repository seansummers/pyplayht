# pyplayht: Unofficial optimized client for PlayHT API

Library for using the PlayHT API v2.

Currently also implements a cli that receives text lines on stdin
and outputs wav bytes on stdout.

```bash
python -m pyplayht < text.txt > speech.wav
```

## Configuration

For the cli, it is expected to have the following environment variables set:

* PLAY_HT_USER_ID
* PLAY_HT_API_KEY
