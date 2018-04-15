import { singleSpiderManagerCommands } from './spider_manager_constants.js';

export class ChangeSpiderState {
    constructor(changeSpiderStateBtns) {
        this.changeSpiderStateBtns = changeSpiderStateBtns;
    }
    init() {
        for (let btn of this.changeSpiderStateBtns) {
            btn.addEventListener('click', function () {
                import('./manage_local_spider.js')
                    .then(({LocalSpiderController}) => {
                        let command = '';
                        if (btn.name === 'run') {
                            command = singleSpiderManagerCommands.RUN;
                        }
                        else if (btn.name === 'stop') {
                            command = singleSpiderManagerCommands.STOP;
                        }
                        new LocalSpiderController(command);
                    });
            }, false);
        }
    }
}
