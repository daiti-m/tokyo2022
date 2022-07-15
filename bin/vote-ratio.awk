#!/usr/local/bin/gawk -f
BEGIN {
    average = 56.55;
}

{
    area = $1;
    pct = $2;
    printf("%s\t% .3f\n", area, log(pct / average));
}
