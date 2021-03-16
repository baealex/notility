var solveCaptcha = false;

document.querySelector('#comment').addEventListener('submit', function(e) {
    if(!solveCaptcha) {
        e.preventDefault();
        document.querySelector('#captcha').style.display = 'block'
    }
});

function onSubmit(token) {
    solveCaptcha = true;
    document.querySelector('#comment').captcha.value = token;
    document.querySelector('#comment').submit();
}

if(self !== top) {
    
} else {
    // location.href = "https://www.notion.so/{{ pk }}";
}