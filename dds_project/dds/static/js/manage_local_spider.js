import { singleSpiderManagerCommands } from './spider_manager_constants.js';


export class LocalSpiderController {
    init (command) {
        if (command === singleSpiderManagerCommands.RUN) {
            this.runCurrentSpider();
        }
    }
    runCurrentSpider() {
        const xhr = new XMLHttpRequest();
        const runSpiderPath = 'temp/path/';
        xhr.open("POST", runSpiderPath, true);

        xhr.setRequestHeader(
            "Content-type", "application/x-www-form-urlencoded");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                // Request finished. Do processing here.
            }
        };
        xhr.send({run_spider: true});
    }
}
