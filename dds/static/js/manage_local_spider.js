import { singleSpiderManagerCommands } from './spider_manager_constants.js';
import csrftoken from "./ajax_csrf_token_setup.js";


export class LocalSpiderController {
    init (command) {
        if (command === singleSpiderManagerCommands.RUN) {
            this.runCurrentSpider();
        }
    }
    static runCurrentSpider() {
        const runSpiderPath = window.location.pathname;

        fetch(runSpiderPath, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({run_spider: true})
        });
    }
}
