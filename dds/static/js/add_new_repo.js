import csrftoken from './base_setup.js';

export class AddNewRepo {
    constructor(form) {
        this.form = form;
    }
    init() {
        this.form.onsubmit = function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            formData.append('is_ajax_submit', true);
            fetch(getNewRepoPath, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            }).then((response) => {
                window.history.pushState({}, '', `${signupPath}`);
                return response.text();
            }).then((data) => {
                document.getElementsByClassName('body')[0].innerHTML = data;
            }).catch((error) => {
                console.log(error);
            });
        };
    }
}
