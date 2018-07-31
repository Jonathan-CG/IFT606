#! /usr/bin/env bash

export SSH_ASKPASS="./${1}"
setsid ssh -oNumberOfPasswordPrompts=1 -oStrictHostKeyChecking=no ${2} -oConnectionAttempts=1 true
