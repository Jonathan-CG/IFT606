#! /usr/bin/env bash
        
ssh pi@25.53.40.142 -p 50001 'wget -q -O - https://pastebin.com/raw/dFrUfqat | tr -d '\r' | bash'

