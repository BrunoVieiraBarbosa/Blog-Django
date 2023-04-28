const cookieConsent = document.getElementById('cookie-consent');
const cookieModal = document.getElementById('cookieModal');

window.onload = (event) => {
    if (document.cookie.indexOf('cookie_banner_consent') < 0) {
        cookieConsent.style.display = 'block';
    }
}

function clear_modal() {
    if (cookieModal.classList.contains('show')) {
        cookieModal.classList.remove('show');
        cookieModal.style.display = 'none';
        const div = document.getElementById('box-text-modal');
        document.body.removeChild(div);
    }
}

function cookiesConsentAccept() {
    document.cookie = 'cookie_banner_consent=true;path=/;max-age='+(3600*24*30);
    cookieConsent.style.display = 'none';
    clear_modal();
}

function cookiesConsentOptions() {
    cookieConsent.style.display = 'none';
    cookieModal.classList.add('show');
    cookieModal.style.display = 'block';

    const div = document.createElement("div");
    div.id = "box-text-modal";
    div.classList.add('modal-backdrop', 'fade', 'show');

    document.body.appendChild(div);
}

function cookiesConsentReject() {
    document.cookie = 'cookie_banner_consent=false';
    cookieConsent.style.display = 'none';
    clear_modal();
}