class CoreModuleInitializer {
    constructor () {}
    static init (classInstance) {
        classInstance.init();
    }
}

const newRepoForm = document.getElementById('new-repo-form');
if (newRepoForm) {
    import('./add_new_repo.js')
        .then(({AddNewRepo}) => {
            CoreModuleInitializer.init(new AddNewRepo(newRepoForm));
        });
}

const changeSpiderStateBtns = document.getElementsByClassName('ctrl-btn');
if (changeSpiderStateBtns.length > 0) {
    import('./change_spider_state.js')
        .then(({ChangeSpiderState}) => {
            CoreModuleInitializer.init(new ChangeSpiderState(changeSpiderStateBtns));
        });
}
