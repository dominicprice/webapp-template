#!/bin/sh

fatal() {
	error "$1"
	exit 1
}

error() {
	printf "\033[0;31mfatal: %s\033[0m\n" "$1"
}

warn() {
	printf "\033[0;33mfatal: %s\033[0m\n" "$1"
}

info() {
	[ -n "$VERBOSE" ] && printf "\033[0;36minfo: %s\033[0m\n" "$1"
}

usage() {
	echo "usage: $0 [-h|--help] [-q|--quiet] ][-o OUTPUT_DIR] INPUTFILE"
}

help() {
	usage
	echo "genlogo.sh generates multiple image formats for"
	echo "your website logo"
	echo " - imagemagick must be available in your PATH"
	echo " - If the input is an svg file, inkscape must be available in your PATH"
}

# parse args
INPUT_FILE=
IS_SVG=
OUTDIR="$PWD/frontend/public"
VERBOSE=1
while [ -n "$1" ]; do
	case "$1" in
		"-h"|"--help")
			help
			exit 0
			;;
		"-o")
			shift
			OUTDIR="$1"
			;;
		"-q"|"--quiet")
			VERBOSE=
			;;
		*.svg)
			[ -z "$INPUT_FILE" ] || fatal "too many input files"
			INPUT_FILE="$1"
			IS_SVG=1
			;;
		*)
			[ -z "$INPUT_FILE" ] || fatal "too many input files"
			INPUT_FILE="$1"
			;;
	esac
	shift
done

if [ -z "$INPUT_FILE" ]; then
	usage
	fatal "invalid arguments"
fi

# find magick/convert
MAGICK="$(command -v magick)" \
	|| MAGICK="$(command -v convert)" \
	|| fatal "could not find imagemagick"

# create logo.png
info "$INPUT_FILE -> $OUTDIR/logo.png"
if [ -n "$IS_SVG" ]; then
	inkscape \
		"$INPUT_FILE" \
		-o "$OUTDIR/logo.png" \
		|| fatal "failed to convert svg"
else
	cp \
		"$INPUT_FILE" \
		"$OUTDIR/logo.png" \
		|| fatal "failed to copy logo"
fi

# determine input dimensions
WIDTH="$(identify -ping -format '%w' "$OUTDIR/logo.png")" \
	|| fatal "failed to determine input image width"
HEIGHT="$(identify -ping -format '%h' "$OUTDIR/logo.png")" \
	|| fatal "failed to determine input image height"

if [ "$WIDTH" -ne "$HEIGHT" ]; then
	warn "width ($WIDTH) != height ($HEIGHT): output may be distorted"
fi
if [ "$WIDTH" -lt 512 ]; then
	warn "dimensions of input (${WIDTH}x${HEIGHT}) are smaller than"
	warn "512x512, larger outputs will be scaled up"
fi


# create logoX.png
for size in 512 192 168 144 96 72 64 48 32 24 16; do
	info "generating $OUTDIR/logo$size.png"
	"$MAGICK" \
		"$OUTDIR/logo.png" \
		-resize "${size}x${size}" \
		"$OUTDIR/logo$size.png" \
		|| fatal "failed to generate logo of size $size"
done

# create favicon.ico
info "generating $OUTDIR/favicon.ico"
"$MAGICK" \
	"$OUTDIR/logo64.png" \
	"$OUTDIR/logo48.png" \
	"$OUTDIR/logo32.png" \
	"$OUTDIR/logo16.png" \
	"$OUTDIR/favicon.ico" \
	|| fatal "failed to generate favicon"

# remove smaller files
info "cleaning up..."
rm \
	"$OUTDIR/logo64.png" \
	"$OUTDIR/logo32.png" \
	"$OUTDIR/logo16.png"
