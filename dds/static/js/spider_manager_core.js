import { singleSpiderManagerCommands } from './spider_manager_constants.js';
import csrftoken from "./base_setup.js";


class SpiderManagerCore {
    /*
    Main single spider manager class. It initializes classes which
    should be loaded simultaneously with page. Put these classes
    in array before passing to the constructor, note that each class
    must have init method.
    */
    constructor (initClasses) {
        if (initClasses.length > 0 && initClasses.every(this.checkInitClasses)) {
            this.initClasses = initClasses;
        }
    }
    init () {
        for (let classInstance in this.initClasses) {
            classInstance.init();
        }
    }
    checkInitClasses (initClass) {
        return (typeof initClass === 'function'
            && (/^\s*class\s+/).test(initClass.toString())
            && initClass.hasOwnProperty('init'));
    }
}

let initialClassInstancesArray = [];
const spiderManagerCore = new SpiderManagerCore(initialClassInstancesArray);
spiderManagerCore.init();


const newRepoForm = document.getElementById('new-repo-form');
newRepoForm.onsubmit = function (e) {
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


const changeSpiderStateBtns = document.getElementsByClassName('ctrl-btn');
for (let btn of changeSpiderStateBtns) {
    btn.addEventListener('click', function () {
        import('./manage_local_spider.js')
            .then(({LocalSpiderController}) => {
                let command = '';
                if (btn.id === 'run-spider') {
                    command = singleSpiderManagerCommands.RUN;
                }
                else if (btn.id === 'stop-spider') {
                    command = singleSpiderManagerCommands.STOP;
                }
                new LocalSpiderController(command);
            });
    }, false);
}
