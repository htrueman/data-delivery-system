import csrftoken from "./base_setup.js";
import { singleSpiderManagerCommands } from './spider_manager_constants.js';


export class LocalSpiderController {
    constructor(command) {
        if (Object.values(singleSpiderManagerCommands).includes(command)) {
            LocalSpiderController.changeCurrentSpiderState(command);
        }
    }
    static changeCurrentSpiderState(command) {
        let formData = new FormData();
        if (command === singleSpiderManagerCommands.RUN) {
            const form = document.getElementById('ctrl-form');
            const pythonSelectValue = form.querySelector('select').value;
            formData = new FormData(form);
            formData.append('python_version', pythonSelectValue);
        }
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
