@cls
@echo :: Bat file to generate an obfuscated Python build using marshal + zlib + base64 encoding
@echo off
@echo == Generating obfuscate version of the mp3.py file...

@python -c "import zlib,base64,marshal;code=open('mp3.py','rb').read();payload=base64.b64encode(zlib.compress(marshal.dumps(compile(code,'x','exec')))).decode();open('mp3_obf.py','w').write(f\"import base64,zlib,marshal;exec(marshal.loads(zlib.decompress(base64.b64decode('{payload}'))))\")"
@echo ---
@echo Status: (should be) Done!
@echo ---
dir /b /od
@echo ---


