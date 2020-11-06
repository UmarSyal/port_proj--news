if ('speechSynthesis' in window) {
    // Speech Synthesis supported 🎉
    let synth = window.speechSynthesis;

    let storyText = document.querySelector('#storyText').innerText;
    let voiceSelect = document.querySelector('#voice_select');
    let volumeSelect = document.querySelector('#volume_select');
    let rateSelect = document.querySelector('#rate_select');

    let utterThis = new SpeechSynthesisUtterance(storyText);
    let voices = [];
    let audioSettingsChanged = false;

    $('#audio').css('display', 'block')

    function populateVoiceList() {
        voices = synth.getVoices();

        for (let i = 0; i < voices.length; i++) {
            // get only english language voices
            if (voices[i].lang.toLowerCase().indexOf('en') >= 0) {
                let option = document.createElement('option');
                option.textContent = voices[i].name + ' (' + voices[i].lang + ')';

                if (voices[i].default) {
                    option.textContent += ' -- DEFAULT';
                }

                option.setAttribute('data-lang', voices[i].lang);
                option.setAttribute('data-name', voices[i].name);
                voiceSelect.appendChild(option);
            }
        }
    }

    populateVoiceList();
    if (synth.onvoiceschanged !== undefined) {
        synth.onvoiceschanged = populateVoiceList;
    }

    function setAudioSettings(change) {
        let selectedVoiceOption = voiceSelect.selectedOptions[0].getAttribute('data-name');
        let selectedVolumeOption = volumeSelect.selectedOptions[0].value;
        let selectedRateOption = rateSelect.selectedOptions[0].value;

        for (let i = 0; i < voices.length; i++) {
            if (voices[i].name === selectedVoiceOption) {
                utterThis.voice = voices[i];
                break;
            }
        }

        utterThis.volume = parseFloat(selectedVolumeOption);
        utterThis.rate = parseFloat(selectedRateOption);
        audioSettingsChanged = change;
    }

    function changeButtonStyle(style) {
        if (style === 'play') {
            $('#playPause').find('i').removeClass('glyphicon-play glyphicon-repeat').addClass('glyphicon-pause');
            $('#playPause').find('span').text('Pause Audio');
        } else if (style === 'pause' || style === 'stop') {
            $('#playPause').find('i').removeClass('glyphicon-pause glyphicon-repeat').addClass('glyphicon-play');
            $('#playPause').find('span').text('Play Audio')
        } else if (style === 'restart') {
            $('#playPause').find('i').removeClass('glyphicon-pause glyphicon-play').addClass('glyphicon-repeat');
            $('#playPause').find('span').text('Restart Audio')
        }
    }

    $('#playPause').click(function () {
        $('#stop').css('display', 'block')

        // if the current settings are changed through select options,
        // cancel the current utterance and start a new one.
        // else pause, resume or start a new utterance as needed
        if (audioSettingsChanged) {
            synth.cancel();
            setAudioSettings(false);
            synth.speak(utterThis);
            changeButtonStyle('play');
        } else {
            if (synth.paused) {
                setAudioSettings(false);
                synth.resume();
                changeButtonStyle('play');
            } else if (synth.speaking) {
                setAudioSettings(false);
                synth.pause();
                changeButtonStyle('pause');
            } else {
                setAudioSettings(false);
                synth.speak(utterThis);
                changeButtonStyle('play');
            }
        }
    });

    $('#stop').click(function () {
        synth.cancel();
        changeButtonStyle('stop');
        $(this).css('display', 'none')
    });

    $('#voice_select').add('#volume_select').add('#rate_select').on('change', function() {
        setAudioSettings(true);
        changeButtonStyle('restart');
    })

    // on page change, stop the audio
    window.onbeforeunload = function (e) {
        synth.cancel();
    }
} else {
    // Speech Synthesis Not Supported 😣
    console.log("Sorry, your browser doesn't support text to speech!");
}