let msgContainer = document.querySelector('.message__container');
let msgRemovedBtn = document.querySelector('.msg__remove__btn');


msgRemovedBtn.addEventListener('click', () => {
    if(msgContainer) {
        msgContainer.style.display = 'none';
    }
});



