<#
    reads in a json and converts specified fields to int (-1 for non-int)
    script then sorts by specified field(s) and outputs them to $outFileName

    use -descending if sorting by descending
#>

param(
    [string]$jsonFile,
    [string]$outFileName,
    [string[]]$sortBy,
    [string[]]$fieldsToConvert,
    [switch] $descending
)

function toInt 
{ 
    param( [string] $val ) 
    
    $retInt = 0; 
    if([int]::TryParse($val, [ref]$retInt))
    { 
        return $retInt
    }
    else
    { 
        return -1
    }; 
}

$content = Get-Content $jsonFile | ConvertFrom-Json
$content | ForEach-Object{ 
    foreach($field in $fieldsToConvert) {
        $_."$field" = toInt $_."$field"
    } 
}

$content | Sort-Object -Property $sortBy -Descending:$descending | ConvertTo-Json > $outFileName