import csrftoken from "./base_setup.js";


export class LocalSpiderController {
    constructor(command) {
        LocalSpiderController.runCurrentSpider(command);
    }
    static runCurrentSpider(command) {
        const form = document.getElementById("ctrl-form");
        const formData = new FormData(form);
        formData.append('id', controllerId);
        formData.append('execution_status', command);

        fetch(runSpiderPath, {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });
    }
}
