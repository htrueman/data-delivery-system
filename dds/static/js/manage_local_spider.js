import { singleSpiderManagerCommands } from './spider_manager_constants.js';
import XhrSetup from './ajax_setup.js';


export class LocalSpiderController {
    init (command) {
        if (command === singleSpiderManagerCommands.RUN) {
            this.runCurrentSpider();
        }
    }
    runCurrentSpider() {
        const runSpiderPath = window.location.pathname;
        const xhr = new XhrSetup('POST', runSpiderPath);
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.send({
            data: JSON.stringify({run_spider: true}),
            success: function (response) {
                console.log(response);
            },
            error: function (errors) {
                console.log(errors);
            }
        });
    }
}
