#!/bin/bash
# concat_audio.sh uses the tool sox to build voicemail greetings
# out of a given intro clip + individual clips from a directory + outro clip

# Check if exactly three arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <intro_file> <directory_with_date_files> <outro_file>"
    exit 1
fi

intro_file=$1
directory=$2
outro_file=$3

# Check if directory exists and is a directory
if [ ! -d "$directory" ]; then
    echo "Provided directory '$directory' does not exist or is not a directory"
    exit 1
fi

# Find files in the directory with the YYYY-MM-DD pattern
files=$(find "$directory" -type f -regextype posix-extended -regex '.*/[0-9]{4}-[0-9]{2}-[0-9]{2}\.[Ww][Aa][Vv]')

# Check if files are found
if [ -z "$files" ]; then
    echo "No files found in the directory with the YYYY-MM-DD pattern"
    exit 1
fi

# Process each file
for file in $files; do
    extension="${file##*.}"
    output_file="AB_${file##*/}"
    sox "$intro_file" "$file" "$outro_file" "$output_file"
    echo "Processed $file into $output_file"
done
