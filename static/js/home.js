async function get_user_data(){

    let request = await fetch('/api/user');
    if (!request.ok) {
        throw new Error("Couldn't get user data");
    } else {
        let user_data = await request.json();

        update_name(user_data.name);
        update_username(user_data.screen_name);
        update_picture(user_data.profile_image_url);
        update_header(user_data.profile_banner_url);
    }

}

function update_name(new_name){
    document.querySelector('#name').innerHTML = new_name;
}

function update_username(new_username){
    document.querySelector('#username').innerHTML = `@${new_username}`;
}

function update_picture(new_picture){
    document.querySelector('#picture').style.backgroundImage = `url(${new_picture})` ;
}

function update_header(new_picture){
    document.querySelector('#header').style.backgroundImage = `url(${new_picture})` ;
}

function showHeaderTitleOnScroll(){
    window.onscroll = () => {
        let title = document.querySelector('#header-title');

        // Holds current position of the document
        let position = document.querySelector('body').getBoundingClientRect();

        if (position.y >= -100) {
            title.classList.remove("h-slide-bottom");
            title.classList.add("h-slide-top");
        } else {
            // When page is scrolled down:
            title.classList.remove("h-slide-top");
            title.classList.add("h-slide-bottom");
            title.classList.remove("h-display-none");
        }
    };
}

window.onload = () => {
    document.querySelector('.tab-pane').classList.add("active", "show")
    document.querySelector('.nav-link').classList.add("active")
};

get_user_data();
showHeaderTitleOnScroll();


