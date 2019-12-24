
@rem ------------------------------------------------------------
@rem Variable Settings
@rem   usually only %TARGET% might be changed
@rem ------------------------------------------------------------
if not DEFINED ARCH       set ARCH=x86_64
if not DEFINED INCLUDE_JRE  set INCLUDE_JRE=YES
if not DEFINED RTM_PY_VER  set RTM_PY_VER=1.1.1

@set PATH_OLD=%PATH%
@set INCLUDE_OPENRTP=YES
@set TARGET=OpenRTM-aist-Python
@set TARGET_WXS=%TARGET%.wxs
@set TARGET_WIXOBJ=%TARGET%.wixobj
echo off
@set TARGET_FULL=%TARGET%_%RTM_PY_VER%-RELEASE_%ARCH%
if "x%ARCH%" == "xx86_64" (
   @set PYTHON_DIR=C:\Python27_x64
   @set OS_ARCH=64-bit OS
) else (
   @set PYTHON_DIR=C:\Python27
   @set OS_ARCH=32-bit OS
)
@set PATH=%WIX%bin;%PYTHON_DIR%;%PATH%
@set PRODUCT_NAME=OpenRTM-aist-%RTM_PY_VER%-RELEASE (%OS_ARCH%) for Python

@rem ------------------------------------------------------------
@rem WixUI Customization Settings
@rem   usually only %WIXUI_RTM% might be changed
@rem ------------------------------------------------------------
@set WIXUI_RTM=WixUI_Mondo_rtm
@set WIXUI_RTM_WXS=%WIXUI_RTM%.wxs
@set WIXUI_RTM_WIXOBJ=%WIXUI_RTM%.wixobj

@rem ------------------------------------------------------------
@rem default distribution package folder
@rem ------------------------------------------------------------
@set DISTRIBUTION=C:\distribution
@set OPENRTM_PY=%DISTRIBUTION%\%TARGET%-%RTM_PY_VER%
if "x%ARCH%" == "xx86_64" (
   @set OMNIORB_PY26=%DISTRIBUTION%\omniORBpy-3.5-win64-python26
   @set OMNIORB_PY27=%DISTRIBUTION%\omniORBpy-3.7-win64-python27
) else (
   @set OMNIORB_PY26=%DISTRIBUTION%\omniORBpy-3.5-Python2.6
   @set OMNIORB_PY27=%DISTRIBUTION%\omniORBpy-3.7-Python2.7
)

@rem ------------------------------------------------------------
@rem Supported languages
@rem   supported languages have to be specified
@rem ------------------------------------------------------------
set LANGUAGES=(ja-jp de-de es-es fr-fr hu-hu it-it ko-kr zh-tw)
copy OpenRTM-aist-Python.wxs.yaml.in OpenRTM-aist-Python.wxs.yaml
echo off
@rem ------------------------------------------------------------
@rem Checking WiX
@rem ------------------------------------------------------------
if "x%WIX%" == "x" (
   echo "Windows Installer XML (WiX) is not installed"
   echo "Please download WiX 3.5 or later from http://wix.sourceforge.net/"
   goto END
)

@rem ------------------------------------------------------------
@rem Import Language-Country, Language codes, Codepages
@rem from langs.txt
@rem http://www.tramontana.co.hu/wix/lesson2.php#2.4
@rem ------------------------------------------------------------
for /F "tokens=1,2,3,4 delims=, " %%i in (langs.txt) do (
    set LC[%%j]=%%j
    set LANG[%%j]=%%k
    set CODE[%%j]=%%l
)

@rem ============================================================
@rem Make OpenRTM-aist-Python file list
@rem ============================================================
python omniORBpy26wxs.py
python omniORBpy27wxs.py
python OpenRTMpywxs.py

@rem ============================================================
@rem compile wxs file and link msi
@rem ============================================================
if "x%ARCH%" == "xx86_64" (
   candle.exe -arch x64 %TARGET_WXS% %WIXUI_RTM_WXS% -dlanguage=1033 -dcodepage=1252
) else (
   candle.exe %TARGET_WXS% %WIXUI_RTM_WXS% -dlanguage=1033 -dcodepage=1252
)
light.exe -ext WixUIExtension -loc WixUI_en-us.wxl ^
      	       -out %TARGET_FULL%.msi %TARGET_WIXOBJ% %WIXUI_RTM_WIXOBJ%

set IDS=1033
setlocal ENABLEDELAYEDEXPANSION

for %%i in %LANGUAGES% do (

    @rem ------------------------------------------------------------
    @rem language ID list
    @rem
    set IDS=!IDS!,!LANG[%%i]!

    @rem ------------------------------------------------------------
    @rem compile wxs file and link msi
    @rem
    if "x%ARCH%" == "xx86_64" (
       candle.exe -arch x64 %TARGET_WXS% %WIXUI_RTM_WXS% -dlanguage=!LANG[%%i]! -dcodepage=!CODE[%%i]!
    ) else (
       candle.exe %TARGET_WXS% %WIXUI_RTM_WXS% -dlanguage=!LANG[%%i]! -dcodepage=!CODE[%%i]!
    )

    if exist WixUI_!LC[%%i]!.wxl (
       light.exe -ext WixUIExtension -ext WixUtilExtension -loc WixUI_!LC[%%i]!.wxl ^
            -out %TARGET_FULL%_!LC[%%i]!.msi %TARGET_WIXOBJ% %WIXUI_RTM_WIXOBJ%
    )
    if not exist WixUI_!LC[%%i]!.wxl (
        light.exe -ext WixUIExtension -ext WixUtilExtension -cultures:!LC[%%i]! ^
            -out %TARGET_FULL%_!LC[%%i]!.msi %TARGET_WIXOBJ% %WIXUI_RTM_WIXOBJ%
    )
    @rem ------------------------------------------------------------
    @rem creating transformation files
    @rem
    torch.exe -p -t language %TARGET_FULL%.msi %TARGET_FULL%_!LC[%%i]!.msi ^
    	      -out !LC[%%i]!.mst

    @rem ------------------------------------------------------------
    @rem embed transformation files
    @rem
    cscript wisubstg.vbs %TARGET_FULL%.msi !LC[%%i]!.mst !LANG[%%i]!

)

@rem ------------------------------------------------------------
@rem here mst embedded msi can be selected languages by 
@rem > msiexec /i SampleMulti.msi TRANSFORMS=":fr-fr.mst"
@rem

@rem ------------------------------------------------------------
@rem Update the summary information stream to list all
@rem supported languages of this package
@rem ------------------------------------------------------------
cscript WiLangId.vbs %TARGET_FULL%.msi Package %IDS%


:END
del *.yaml
@set PATH=%PATH_OLD%

@rem pause;

