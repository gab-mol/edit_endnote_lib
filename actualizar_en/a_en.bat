@echo off
for %%f in (..\actualizar_en\journals\*.enw) do (
    start "" "%%f"
    echo ..
    echo ################################
    echo cargando : %%f
    echo #####################
    echo ..
    timeout /t 3 /nobreak 
)
REM `timeout /t 5 /nobreak >nul` para que no se imprima mensaje de espera por terminal