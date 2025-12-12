if ((Get-Command "warp").CommandType -eq "Function") {
	warp @args;
	[Console]::ResetColor()
	exit
}

"First time use of thewarp detected. "

if ((Get-Content $PROFILE -Raw -ErrorAction Ignore) -like "*thewarp*") {
} else {
	"  - Adding thewarp intialization to user `$PROFILE"
	$script = "`n`$env:PYTHONIOENCODING='utf-8' `niex `"`$(thewarp --alias)`"";
	Write-Output $script | Add-Content $PROFILE
}

"  - Adding warp() function to current session..."
$env:PYTHONIOENCODING='utf-8'
iex "$($(thewarp --alias).Replace("function warp", "function global:warp"))"

"  - Invoking warp()`n"
warp @args;
[Console]::ResetColor()
