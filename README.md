run `make` to install it, then do `make DIR=/wherever/your/files/are/ run` to
run it. All of the converted files will be placed in a directory called
`shortened` under the path you supply.
Requires either an OSX or Linux environment, plus the program `ffmpeg` to be
installed

You can adjust the THRESHOLD and SIZE_LIMIT variables to change what it
considers the threshold of silence to be, and the maximum length in minutes of
what it will convert.
