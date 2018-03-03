import csrftoken from "./ajax_csrf_token_setup.js";


export class LocalSpiderController {
    constructor(command) {
        LocalSpiderController.runCurrentSpider(command);
    }
    static runCurrentSpider(command) {
        fetch(runSpiderPath, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                id: controllerId,
                execution_status: command
            })
        });
    }
}
