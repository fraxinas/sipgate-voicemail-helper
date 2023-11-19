# sipgate-voicemail-helper

(CC) 2023 by Andreas Frisch <github@fraxinas.dev>

## OwO what's this?
**`sipgate-voicemail-helper` is smol suite of scripts to help setting up automated voicemail greetings on Sipgate**

## concat_audio.sh
`concat_audio.sh` uses the tool `sox` to build voicemail greetings out of a given intro clip + individual clips from a directory + outro clip

### Usage
`./concat_audio.sh <intro_file> <directory_with_date_files> <outro_file>`
* files can be wav or mp3
* clips in directory MUST be in the pattern `YYYY-MM-DD.*`
* concatenated audio files are placed in the working directory as `AB_YYYY-MM-DD.*` with the same format/extension of the clip file

## sipgate-upload-greeting.py
`sipgate-upload-greeting.py` is used to upload the batch of greetings to the sipgate server

### Usage
`./sipgate-upload-greeting.py '<audio_file_pattern>' <sipgate_token>`
* the `audio_file_pattern` argument uses internal globbing, so it needs to be quoted to prevent command line expansion, e.g.
* `./sipgate-upload-greeting.py 'AB_2023*.wav' <sipgate_token>`
* sipgate supports wav or mp3 format
* the sipgate token can be obtained through https://app.sipgate.com/personal-access-token
* you might have to edit the REST API path if your account uses multiple phonelines

## sipgate-switch-greeting.py
`sipgate-switch-greeting.py` is meant to be periodically called to activate the next date's voicemail greeting

### Usage
`sipgate-switch-greeting.py`
* There are no command line arguments
* the sipgate bearer token and source of event's date table url are defined as constants in the top of the script
* corresponding dates' clips are expected to already be uploaded as voicemail greetings on the sipgate account using `sipgate-upload-greeting.py`
* you might have to edit the REST API path if your account uses multiple phonelines
* this script should be called daily as cronjob

## Requirements
* `sox`
* https://pypi.org/project/beautifulsoup4/
* https://pypi.org/project/requests/
