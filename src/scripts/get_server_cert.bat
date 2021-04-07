@echo off

rem ---------------------------------------------------------------------------
rem -- Get the server's certificate from SERVER:PORT
rem -- Update the variables to fit your needs
rem ---------------------------------------------------------------------------

set OPENSSL="c:\Program Files (x86)\OpenSSL-Win32\bin\openssl.exe"
set SERVER=localhost
set PORT=8200
set CACERT=server_cert.pem

%OPENSSL% openssl s_client -showcerts -servername %SERVER% -connect %SERVER%:%PORT% > %CACERT%
