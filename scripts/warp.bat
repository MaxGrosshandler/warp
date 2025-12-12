@set PYTHONIOENCODING=utf-8
@powershell -noprofile -c "cmd /c \"$(warp %* $(doskey /history)[-2])\"; [Console]::ResetColor();"
