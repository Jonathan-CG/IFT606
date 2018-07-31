#! /usr/bin/env bash

export SSH_ASKPASS="./${1}"
setsid ssh -oNumberOfPasswordPrompts=1 -oStrictHostKeyChecking=no pi@24.53.40.142 -p 50001 -o 'ConnectionAttempts=1' true
