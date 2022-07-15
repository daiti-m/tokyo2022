#!/usr/local/bin/gawk -f
FNR == 1 { printf("%s\t", $0); }
/投票率/ {
    if (match($0, /[0-9.]+/)) {
        print substr($0, RSTART, RLENGTH);
    }
}

