import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

