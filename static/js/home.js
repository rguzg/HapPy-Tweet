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

// Gets classifiers from backend and saves the information on sessionStorage and requests tweets from get_tweets()
async function prepare_front(){
    try {
        let request = await fetch('/api/classifier');
        if (!request.ok) {
            throw Error("Classifiers couldn't be loaded");
        } else {
            let classifiers = await request.json();
            
            classifiers.forEach(classifier => {
                sessionStorage.setItem(classifier.name, 0);
                get_tweets(classifier.name).then(() => {
                    let language_container = document.querySelector(`#pills-${classifier.name}`);
                    language_container.removeChild(document.querySelector(`#${classifier.name}-load`));
                });

            });


        }
    } catch (error) {
        alert(Error);
    }
}

async function get_tweets(language){
    let currentPage = sessionStorage.getItem(language);
    try{
        let request = await fetch(`/api/tweets/${language}/${currentPage}`);
        if (!request.ok) {
            throw Error("Tweets couldn't be loaded");
        } else {
            let tweets = await request.json();
            
            let language_container = document.querySelector(`#pills-${language}`);
            
            // TODO: Make foreach async so that endtext gets inserted properly
            tweets.forEach(tweet => {
                tweet_container = createTweet(tweet.tweet_id);
                language_container.appendChild(tweet_container);
            });
            
            language_container.appendChild(createEndText());
        }
    } catch (error) {
        alert(error);
    }
}

// Creates a container for the tweet and creates a tweet widget inside of it using Twitter Widgets
function createTweet(tweet_id){
    let container = document.createElement('div');
    container.setAttribute('data-tweetid', tweet_id);
    
    twttr.widgets.createTweet(tweet_id, container, {conversation: 'none'});
    
    return container;
}

function createEndText(){
    let text = document.createElement('p');
    text.id = 'bottom'
    text.innerHTML = "Looks like you've reached the end...";
    
    return text;
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

function getCurrentTab(){
    return document.querySelector('.active').dataset.language;
}

window.onscroll = () => {
    let title = document.querySelector('#header-title');
    
    // Holds current position of the document
    let position = document.querySelector('body').getBoundingClientRect();
    
    // Checks when page is scrolled 100 units down
    if (position.y >= -100) {
        title.classList.remove("h-slide-bottom");
        title.classList.add("h-slide-top");
    } else {
        // When page is scrolled down:
        title.classList.remove("h-slide-top");
        title.classList.add("h-slide-bottom");
        title.classList.remove("h-display-none");
    }
    
    // TODO: Non jQuery implementarion
    // Checks when page is scrolled to the bottom
    if($(window).scrollTop() + $(window).height() == $(document).height()) {
        let language = getCurrentTab()
        let currentPage = Number(sessionStorage.getItem(language));
        currentPage++

        sessionStorage.setItem(language, currentPage);

        get_tweets(language).then(() => {
            let language_container = document.querySelector(`#pills-${language}`);
            language_container.removeChild(document.querySelector(`#bottom`));
        });
    }
};

window.onload = () => {
    document.querySelector('.tab-pane').classList.add("active", "show")
    document.querySelector('.nav-link').classList.add("active")
    
    get_user_data();
    prepare_front();
};


